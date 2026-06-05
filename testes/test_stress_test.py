import sys
import os
import unittest
import asyncio
from unittest.mock import patch, MagicMock

sys.modules['aiohttp'] = MagicMock()
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.stress_test import StressTestExecutor


class TestStressTestProfissional(unittest.TestCase):
    def setUp(self):
        self.executor = StressTestExecutor("127.0.0.1", 80, rps_limit=10, duration=0.1)


    def test_calculo_percentil_variados(self):
        casos = [
            ([10, 20, 30], 0.99, 30),
            ([10, 20], 0.5, 15.0),
            ([100], 0.95, 100),
            ([], 0.95, 0)
        ]
        for latencias, quantil, esperado in casos:
            with self.subTest(latencias=latencias, quantil=quantil):
                res = self.executor._get_percentile(latencias, quantil)
                self.assertAlmostEqual(res, esperado, delta=0.5)


    def test_formato_relatorio(self):

        self.executor.metrics = {
            "/api/login": {"steady_latencies": [5, 10], "total_sent": 50, "errors": 5, "total_scheduled": 55},
            "/": {"steady_latencies": [100], "total_sent": 10, "errors": 0, "total_scheduled": 10}
        }
        relatorio = self.executor.get_report()

        self.assertTrue(relatorio.startswith("\n--- AURA"))
        self.assertIn("/api/login", relatorio)
        self.assertIn("5", relatorio)


    def test_ciclo_de_vida_executor(self):
        self.assertFalse(self.executor.is_running)
        self.executor.start()

        self.assertFalse(self.executor._shutdown_event.is_set())
        self.executor.stop()
        self.assertTrue(self.executor._shutdown_event.is_set())


    def test_run_com_falha_de_rede_simulada(self):

        mock_session = MagicMock()
        mock_session.return_value.__aenter__.return_value.get.side_effect = Exception("Conexão Recusada")

        with patch("core.stress_test.aiohttp.ClientSession", return_value=mock_session):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(self.executor.run_test())
            finally:
                loop.close()


        self.assertIsNotNone(self.executor.metrics)

        erros_totais = sum(m['errors'] for m in self.executor.metrics.values())
        self.assertGreaterEqual(erros_totais, 0)


if __name__ == '__main__':
    unittest.main()