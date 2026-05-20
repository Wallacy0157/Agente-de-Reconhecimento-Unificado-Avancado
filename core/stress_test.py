import asyncio
import time
import statistics
import random
import aiohttp
import threading
from collections import defaultdict

class StressTestExecutor:
    def __init__(self, target, port, rps_limit=100, duration=60, workers=50, gradual=False):
        self.target = target
        self.port = port
        self.url = f"http://{target}:{port}"
        
        self.target_rps = rps_limit
        self.duration = duration
        self.num_workers = workers
        self.gradual = gradual 
        self.warmup_duration = 5
        
        self.is_running = False
        self._start_time = 0
        self._shutdown_event = asyncio.Event()

        self.metrics = defaultdict(lambda: {
            "steady_latencies": [],
            "total_scheduled": 0,
            "total_sent": 0,
            "errors": 0,
            "status_codes": defaultdict(int),
            "execution_jitters": []
        })
        
        self.scenarios = [
            {"name": "root_hit", "path": "/", "weight": 0.8, "method": "GET"},
            {"name": "api_search", "path": "/search", "weight": 0.2, "method": "GET"}
        ]

    async def _producer(self, queue):
        interval = 1.0 / self.target_rps
        next_tick = time.monotonic()
        total_reqs = int(self.target_rps * (self.duration + self.warmup_duration))
        
        for _ in range(total_reqs):
            if self._shutdown_event.is_set(): break
            await queue.put(time.monotonic())
            next_tick += interval
            sleep_time = next_tick - time.monotonic()
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)

    async def _worker(self, session, queue):
        timeout = aiohttp.ClientTimeout(total=10)
        while not (self._shutdown_event.is_set() and queue.empty()):
            try:
                scheduled_time = await asyncio.wait_for(queue.get(), timeout=0.5)
            except asyncio.TimeoutError:
                continue

            scenario = random.choices(self.scenarios, weights=[s['weight'] for s in self.scenarios])[0]
            m = self.metrics[scenario['name']]
            m['total_scheduled'] += 1
            
            exec_jitter = (time.monotonic() - scheduled_time) * 1000
            m['execution_jitters'].append(exec_jitter)
            
            start_req = time.perf_counter()
            try:
                m['total_sent'] += 1
                async with session.request(
                    scenario['method'], 
                    f"{self.url}{scenario['path']}", 
                    timeout=timeout
                ) as resp:
                    latency = (time.perf_counter() - start_req) * 1000
                    if time.monotonic() >= (self._start_time + self.warmup_duration):
                        m['steady_latencies'].append(latency)
                    m['status_codes'][resp.status] += 1
            except Exception:
                m['errors'] += 1
            finally:
                queue.task_done()

    async def run_test(self):
        self.is_running = True
        self._start_time = time.monotonic()
        queue = asyncio.Queue(maxsize=self.target_rps) 
        
        connector = aiohttp.TCPConnector(
            limit=self.num_workers,
            keepalive_timeout=30,
            ttl_dns_cache=300
        )
        
        async with aiohttp.ClientSession(connector=connector) as session:
            producer_task = asyncio.create_task(self._producer(queue))
            workers = [asyncio.create_task(self._worker(session, queue)) for _ in range(self.num_workers)]
            
            try:
                await asyncio.wait_for(self._shutdown_event.wait(), timeout=self.duration + self.warmup_duration)
            except asyncio.TimeoutError:
                pass
            
            self._shutdown_event.set()
            await producer_task
            await queue.join()
            
            for w in workers: w.cancel()
        
        self.is_running = False

    def start(self):
        def _run_loop():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(self.run_test())
            finally:
                loop.close()
        
        thread = threading.Thread(target=_run_loop, daemon=True)
        thread.start()

    def stop(self):
        self._shutdown_event.set()

    def _get_percentile(self, data, p):
        if not data: return 0
        data.sort()
        idx = (len(data) - 1) * p
        lower = int(idx)
        upper = lower + 1
        weight = idx - lower
        if upper >= len(data): return data[lower]
        return data[lower] * (1 - weight) + data[upper] * weight

    def get_report(self):
        lines = [f"\n--- AURA STRESS REPORT: {self.target}:{self.port} ---"]
        for name, data in self.metrics.items():
            lats = data['steady_latencies']
            total_dispatched = data['total_sent']
            p95 = self._get_percentile(lats, 0.95)
            
            lines.append(f"Endpoint: {name}")
            lines.append(f"  RPS Real: {len(lats)/self.duration:.2f}")
            lines.append(f"  P95 Latency: {p95:.2f}ms")
            lines.append(f"  Errors: {data['errors']} ({ (data['errors']/total_dispatched*100) if total_dispatched > 0 else 0:.1f}%)")
            lines.append(f"  Saturation (Lost): {data['total_scheduled'] - data['total_sent']}")
            
        lines.append("-" * 40)
        return "\n".join(lines)