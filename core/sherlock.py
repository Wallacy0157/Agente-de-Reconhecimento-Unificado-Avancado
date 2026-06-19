import requests
import json
import os
import urllib.parse
import threading
from datetime import datetime
from ddgs import DDGS
from core.reporting import build_report_header

class SherlockEngine:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }
        self.social_sites = {
            "GitHub": "https://github.com/{}",
            "Instagram": "https://www.instagram.com/{}/",
            "X (Twitter)": "https://x.com/{}",
            "Reddit": "https://www.reddit.com/user/{}",
            "LinkedIn (User)": "https://www.linkedin.com/in/{}/"
        }
        self.people_search_engines = {
            "Webmii": "https://webmii.com/people?n={}",
            "PeekYou": "https://www.peekyou.com/{}",
            "TruePeople": "https://www.truepeoplesearch.com/results?name={}"
        }

    def search_everywhere(self, target, mode="nickname", callback=None, should_stop=None):
        """
        mode: "nickname" ou "full_name"
        """
        results = []
        stop_checker = should_stop or (lambda: False)
        
        if mode == "nickname":
            results.extend(self._direct_search(target, callback, stop_checker))
            if not stop_checker():
                results.extend(self._global_search(f'"{target}"', "Nickname Mention", callback, stop_checker))
        else:
            formatted_name = target.replace(" ", "+")
            results.extend(self._people_search(formatted_name, callback, stop_checker))
            if not stop_checker():
                dork_query = f'"{target}" filetype:pdf OR filetype:txt OR filetype:xlsx'
                results.extend(self._global_search(dork_query, "Potential Leak/Doc", callback, stop_checker))
            if not stop_checker():
                results.extend(self._global_search(f'site:instagram.com "{target}"', "Social Match", callback, stop_checker))

        unique = {item["url"]: item for item in results}
        return list(unique.values())

    def _direct_search(self, username, callback, should_stop):
        found = []
        for site, url_form in self.social_sites.items():
            if should_stop():
                break
            url = url_form.format(username)
            try:
                res = requests.get(url, headers=self.headers, timeout=3)
                if res.status_code == 200 and username.lower() in res.text.lower():
                    item = {"site": site, "url": url, "source": "Direct Hit"}
                    found.append(item)
                    if callback: callback(site, url)
            except: continue
        return found

    def _people_search(self, name, callback, should_stop):
        found = []
        for site, url_form in self.people_search_engines.items():
            if should_stop():
                break
            url = url_form.format(name)
            item = {"site": site, "url": url, "source": "Indexador de Pessoas"}
            found.append(item)
            if callback: callback(site, url)
        return found

    def _global_search(self, query, label, callback, should_stop):
        found = []
        if should_stop():
            return found
        try:
            with DDGS() as ddgs:
                results = ddgs.text(query, max_results=10)
                for r in results:
                    if should_stop():
                        break
                    item = {"site": label, "url": r["href"], "title": r["title"], "source": "Global Search"}
                    found.append(item)
                    if callback: callback(label, r["href"])
        except: pass
        return found

    def save_to_json(self, target, results, base_dir, user_context=None):
        log_dir = os.path.join(base_dir, "logs")
        os.makedirs(log_dir, exist_ok=True)

        now = datetime.now()
        filename = f"sherlock_{target}_{now.strftime('%Y%m%d_%H%M%S')}.json"
        path = os.path.join(log_dir, filename)
        exact_urls = [item.get("url") for item in results if item.get("url")]

        data = {
            "report_header": build_report_header(user_context, now),
            "target": target,
            "date": now.isoformat(),
            "total_found": len(results),
            "exact_urls": exact_urls,
            "summary": {
                "target": target,
                "total_found": len(results),
                "exact_urls": exact_urls,
            },
            "results": results
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        return path


class SherlockExecutor:
    def __init__(self, target, mode):
        self.target = target
        self.mode = mode
        self.engine = SherlockEngine()
        self._results = []
        self._pending_results = []
        self._error = None
        self._stop_event = threading.Event()
        self._state_lock = threading.Lock()
        self._running = False
        self._worker_thread = None

    @property
    def is_running(self):
        with self._state_lock:
            return self._running

    def start(self):
        with self._state_lock:
            if self._running:
                return False
            self._running = True

        self._results = []
        self._pending_results = []
        self._error = None
        self._stop_event.clear()
        self._worker_thread = threading.Thread(target=self._run, daemon=True)
        self._worker_thread.start()
        return True

    def stop(self):
        self._stop_event.set()

    def get_results(self):
        return list(self._results)

    def pop_new_results(self):
        pending = list(self._pending_results)
        self._pending_results.clear()
        return pending

    def get_error(self):
        return self._error

    def save_results(self, base_dir, user_context=None):
        return self.engine.save_to_json(self.target, self._results, base_dir, user_context=user_context)

    def _on_result(self, site, url):
        if self._stop_event.is_set():
            return
        item = {"site": site, "url": url}
        self._pending_results.append(item)

    def _run(self):
        try:
            self._results = self.engine.search_everywhere(
                self.target,
                mode=self.mode,
                callback=self._on_result,
                should_stop=self._stop_event.is_set,
            )
        except Exception as exc:
            self._error = str(exc)
        finally:
            with self._state_lock:
                self._running = False


def build_osint_payload(executor) -> dict:
    """Converte resultados do SherlockExecutor para formato OsintResultadoRequest."""
    from datetime import datetime, timezone

    results = executor.get_results()

    resultados = []
    for item in results:
        resultados.append({
            "site": item.get("site", ""),
            "url": item.get("url", ""),
            "titulo": item.get("title"),
            "fonte": item.get("source"),
        })

    now = datetime.now(timezone.utc)
    return {
        "alvo": executor.target,
        "modo": executor.mode,
        "totalEncontrado": len(results),
        "inicio": now.isoformat(),
        "fim": now.isoformat(),
        "resultados": resultados,
    }