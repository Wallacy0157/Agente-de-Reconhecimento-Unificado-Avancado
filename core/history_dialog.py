import re

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QScrollArea,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from core.components import lang_get
from services.scan_history_service import buscar_scan_detalhe, listar_scans


class HistoryView(QWidget):
    """Reusable scan history view for both the sidebar page and modal dialog."""

    def __init__(self, parent, L: dict, auto_load: bool = True):
        super().__init__(parent)
        self.L = L
        self._loaded = False
        self._setup_ui()
        if auto_load:
            self.load_scan_list()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)

        self.title_label = QLabel(
            lang_get(self.L, "history_dialog.title", "Historico de Varreduras")
        )
        self.title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        main_layout.addWidget(self.title_label)

        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        self.left_panel = QWidget()
        left_layout = QVBoxLayout(self.left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)

        self.scan_list = QListWidget()
        self.scan_list.itemClicked.connect(self._on_item_clicked)
        left_layout.addWidget(self.scan_list)

        self.left_error_widget = QWidget()
        left_error_layout = QVBoxLayout(self.left_error_widget)
        left_error_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.left_error_label = QLabel()
        self.left_error_label.setWordWrap(True)
        self.left_error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_error_layout.addWidget(self.left_error_label)

        self.retry_button = QPushButton(
            lang_get(self.L, "history_dialog.retry", "Tentar novamente")
        )
        self.retry_button.clicked.connect(self.load_scan_list)
        left_error_layout.addWidget(
            self.retry_button, alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.left_error_widget.hide()
        left_layout.addWidget(self.left_error_widget)

        self.left_empty_label = QLabel(
            lang_get(
                self.L,
                "history_dialog.empty",
                "Nenhuma varredura encontrada.",
            )
        )
        self.left_empty_label.setWordWrap(True)
        self.left_empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_empty_label.hide()
        left_layout.addWidget(self.left_empty_label)

        self.splitter.addWidget(self.left_panel)

        self.right_panel = QScrollArea()
        self.right_panel.setWidgetResizable(True)

        self.detail_widget = QWidget()
        self.detail_layout = QVBoxLayout(self.detail_widget)
        self.detail_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.detail_placeholder = QLabel(
            lang_get(
                self.L,
                "history_dialog.no_detail",
                "Selecione uma varredura para ver os detalhes.",
            )
        )
        self.detail_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.detail_placeholder.setWordWrap(True)
        self.detail_layout.addWidget(self.detail_placeholder)

        self.right_panel.setWidget(self.detail_widget)
        self.splitter.addWidget(self.right_panel)
        self.splitter.setSizes([315, 585])
        main_layout.addWidget(self.splitter)

    def showEvent(self, event):
        super().showEvent(event)
        if not self._loaded:
            self.load_scan_list()

    def update_ui_language(self, L):
        self.L = L
        self.title_label.setText(
            lang_get(self.L, "history_dialog.title", "Historico de Varreduras")
        )
        self.retry_button.setText(
            lang_get(self.L, "history_dialog.retry", "Tentar novamente")
        )
        self.left_empty_label.setText(
            lang_get(
                self.L,
                "history_dialog.empty",
                "Nenhuma varredura encontrada.",
            )
        )

    def load_scan_list(self):
        self._loaded = True
        self.scan_list.clear()
        self.scan_list.show()
        self.left_error_widget.hide()
        self.left_empty_label.hide()

        success, result = listar_scans()
        if not success:
            self._show_list_error(result)
            return
        self.show_scan_list(result)

    def show_scan_list(self, scans: list[dict]):
        self.scan_list.clear()
        if not scans:
            self.scan_list.hide()
            self.left_empty_label.show()
            return

        sorted_scans = sorted(
            scans,
            key=lambda scan: (scan.get("scanDate", ""), scan.get("scanTime", "")),
            reverse=True,
        )

        for scan in sorted_scans:
            scan_id = scan.get("id", 0)
            date = scan.get("scanDate", "-")
            time = scan.get("scanTime", "-")
            hosts = scan.get("totalHosts", 0)
            vulns = scan.get("totalVulnerabilities", 0)
            status = scan.get("status", "-")
            text = (
                f"{date}  {time}\n"
                f"Hosts: {hosts}  |  Vulns: {vulns}  |  {status}"
            )
            item = QListWidgetItem(text)
            item.setData(Qt.ItemDataRole.UserRole, scan_id)
            self.scan_list.addItem(item)

    def _on_item_clicked(self, item: QListWidgetItem):
        scan_id = item.data(Qt.ItemDataRole.UserRole)
        if scan_id is not None:
            self.on_scan_selected(scan_id)

    def on_scan_selected(self, scan_id: int):
        success, result = buscar_scan_detalhe(scan_id)
        if not success:
            self._show_detail_error(result)
            return
        self.show_scan_detail(result)

    def show_scan_detail(self, detail: dict):
        self._clear_detail_panel()
        hosts = detail.get("hosts", [])

        if not hosts:
            no_hosts_label = QLabel("Nenhum host encontrado nesta varredura.")
            no_hosts_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.detail_layout.addWidget(no_hosts_label)
            return

        hosts_title = QLabel(
            lang_get(self.L, "history_dialog.hosts", "Hosts Descobertos")
        )
        hosts_title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.detail_layout.addWidget(hosts_title)

        for host in hosts:
            ip = host.get("ip", "-")
            os_info = host.get("os", "Desconhecido") or "Desconhecido"
            host_label = QLabel(f"{ip} - OS: {os_info}")
            host_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            host_label.setContentsMargins(0, 8, 0, 2)
            self.detail_layout.addWidget(host_label)

            open_ports = host.get("openPorts", [])
            if open_ports:
                ports_title = QLabel(
                    f"  {lang_get(self.L, 'history_dialog.ports', 'Portas Abertas')}:"
                )
                ports_title.setFont(QFont("Arial", 9, QFont.Weight.Bold))
                self.detail_layout.addWidget(ports_title)
                for port_info in open_ports:
                    port_num = port_info.get("port", "-")
                    protocol = port_info.get("protocol", "-")
                    service = port_info.get("service", "-")
                    self.detail_layout.addWidget(
                        QLabel(f"    - {port_num}/{protocol} - {service}")
                    )

            vulnerabilities = host.get("vulnerabilities", [])
            if vulnerabilities:
                vulns_title = QLabel(
                    f"  {lang_get(self.L, 'history_dialog.vulnerabilities', 'Vulnerabilidades')}:"
                )
                vulns_title.setFont(QFont("Arial", 9, QFont.Weight.Bold))
                self.detail_layout.addWidget(vulns_title)
                for vuln in vulnerabilities:
                    script = vuln.get("script", "")
                    details = vuln.get("details", "-")
                    cve = self._extract_cve(script)
                    vuln_text = f"    - {details}"
                    if cve:
                        vuln_text += f"  [{cve}]"
                    vuln_label = QLabel(vuln_text)
                    vuln_label.setWordWrap(True)
                    self.detail_layout.addWidget(vuln_label)

        self.detail_layout.addStretch()

    def _show_list_error(self, error_msg: str):
        self.scan_list.hide()
        self.left_empty_label.hide()
        self.left_error_label.setText(
            error_msg
            or lang_get(
                self.L,
                "history_dialog.error.connection",
                "Nao foi possivel conectar ao servidor.",
            )
        )
        self.left_error_widget.show()

    def _show_detail_error(self, error_msg: str):
        self._clear_detail_panel()
        error_label = QLabel(
            error_msg
            or lang_get(
                self.L,
                "history_dialog.error.connection",
                "Nao foi possivel conectar ao servidor.",
            )
        )
        error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        error_label.setWordWrap(True)
        error_label.setStyleSheet("color: #d32f2f;")
        self.detail_layout.addWidget(error_label)

    def _clear_detail_panel(self):
        while self.detail_layout.count():
            child = self.detail_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    @staticmethod
    def _extract_cve(script: str) -> str | None:
        if not script:
            return None
        match = re.search(r"(CVE-\d{4}-\d+)", script, re.IGNORECASE)
        if match:
            return match.group(1).upper()
        match = re.search(r"cve(\d{4})(\d+)", script, re.IGNORECASE)
        if match:
            return f"CVE-{match.group(1)}-{match.group(2)}"
        return None


class HistoryDialog(QDialog):
    def __init__(self, parent, L: dict):
        super().__init__(parent)
        self.setWindowTitle(
            lang_get(L, "history_dialog.title", "Historico de Varreduras")
        )
        self.setMinimumSize(900, 550)
        self.setModal(True)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(HistoryView(self, L, auto_load=True))
