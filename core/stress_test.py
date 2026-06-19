import asyncio
import time
import statistics
import random
import aiohttp
import threading
from collections import defaultdict
from datetime import datetime, timezone
from core.reporting import format_report_header_text

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

    def _summarize_metrics(self):
        total_sent = sum(data.get("total_sent", 0) for data in self.metrics.values())
        failures = sum(data.get("errors", 0) for data in self.metrics.values())
        http_200 = 0
        all_latencies = []
        for data in self.metrics.values():
            status_codes = data.get("status_codes", {})
            http_200 += status_codes.get(200, 0) + status_codes.get("200", 0)
            all_latencies.extend(data.get("steady_latencies", []))

        avg_latency = statistics.mean(all_latencies) if all_latencies else 0
        return {
            "total_sent": total_sent,
            "http_200": http_200,
            "failures": failures,
            "avg_latency_ms": avg_latency,
        }

    def get_report(self, user_context=None):
        summary = self._summarize_metrics()
        lines = [
            f"\n--- AURA STRESS REPORT: {self.target}:{self.port} ---",
            format_report_header_text("RELATÓRIO DE TESTE DE CARGA", user_context),
            "Resumo do Teste de Carga:",
            f"  Total de requisições enviadas: {summary['total_sent']}",
            f"  Requisições com sucesso (HTTP 200): {summary['http_200']}",
            f"  Falhas: {summary['failures']}",
            f"  Tempo de resposta médio: {summary['avg_latency_ms']:.2f}ms",
            "",
            "Detalhes por endpoint:",
        ]
        for name, data in self.metrics.items():
            lats = data.get('steady_latencies', [])
            total_dispatched = data.get('total_sent', 0)
            p95 = self._get_percentile(lats, 0.95)
            
            lines.append(f"Endpoint: {name}")
            lines.append(f"  RPS Real: {len(lats)/self.duration:.2f}")
            lines.append(f"  P95 Latency: {p95:.2f}ms")
            lines.append(f"  Errors: {data.get('errors', 0)} ({ (data.get('errors', 0)/total_dispatched*100) if total_dispatched > 0 else 0:.1f}%)")
            lines.append(f"  Saturation (Lost): {data.get('total_scheduled', 0) - data.get('total_sent', 0)}")
            
        lines.append("-" * 40)
        return "\n".join(lines)


def _get_percentile_safe(data: list, p: float) -> float:
    """Calcula percentil. Retorna 0.0 se a lista estiver vazia."""
    if not data:
        return 0.0
    sorted_data = sorted(data)
    idx = (len(sorted_data) - 1) * p
    lower = int(idx)
    upper = lower + 1
    weight = idx - lower
    if upper >= len(sorted_data):
        return sorted_data[lower]
    return sorted_data[lower] * (1 - weight) + sorted_data[upper] * weight


def _format_status_codes(status_codes: dict) -> str:
    """Formata status_codes como 'código:contagem' ordenado crescente."""
    if not status_codes:
        return ""
    return ",".join(f"{code}:{count}" for code, count in sorted(status_codes.items()))


def build_stress_test_payload(executor) -> dict:
    """Converte métricas do StressTestExecutor para formato StressTestResultadoRequest."""
    metrics = executor.metrics

    total_enviado = sum(data.get("total_sent", 0) for data in metrics.values())
    quantidade_erros = sum(data.get("errors", 0) for data in metrics.values())
    quantidade_sucesso = sum(
        data.get("status_codes", {}).get(200, 0) + data.get("status_codes", {}).get("200", 0)
        for data in metrics.values()
    )
    if quantidade_sucesso == 0 and total_enviado:
        quantidade_sucesso = max(total_enviado - quantidade_erros, 0)

    cenarios = []
    for name, data in metrics.items():
        lats = data.get("steady_latencies", [])
        p95 = _get_percentile_safe(lats, 0.95)
        status_str = _format_status_codes(data.get("status_codes", {}))

        cenarios.append({
            "nome": name,
            "porta": executor.port,
            "status": status_str,
            "latenciaP95Ms": round(p95, 2)
        })

    now = datetime.now(timezone.utc)
    return {
        "ipAlvo": executor.target,
        "portaAlvo": executor.port,
        "rpsLimite": executor.target_rps,
        "duracaoConfiguracao": executor.duration,
        "totalEnviado": total_enviado,
        "quantidadeSucesso": quantidade_sucesso,
        "quantidadeErros": quantidade_erros,
        "inicio": now.isoformat(),
        "fim": now.isoformat(),
        "cenarios": cenarios
    }