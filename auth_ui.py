import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QCheckBox, QStackedWidget, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
from services import auth_service

class AuthWindow(QWidget):
    login_successful = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("AURA Security - Autenticação")
        self.setFixedSize(400, 600)
        self.setStyleSheet("background-color: #0B0813;")

        self.layout = QVBoxLayout(self)
        self.stack = QStackedWidget()
        
        self.setup_login_ui()
        self.setup_register_ui()
        
        self.layout.addWidget(self.stack)
        self.stack.setCurrentIndex(0)

    def setup_login_ui(self):
        self.login_page = QWidget()
        layout = QVBoxLayout(self.login_page)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        title = QLabel("Entrar")
        title.setStyleSheet("color: white; font-size: 32px; font-weight: bold;")
        layout.addWidget(title)

        sub_text = QLabel("Se você não tem conta em nosso app")
        sub_text.setStyleSheet("color: #BBBBBB; font-size: 14px;")
        layout.addWidget(sub_text)

        btn_go_reg = QPushButton("Registre-se aqui")
        btn_go_reg.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_go_reg.setStyleSheet("color: #C1128C; text-align: left; font-size: 14px; border: none; background: none;")
        btn_go_reg.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        layout.addWidget(btn_go_reg)

        layout.addSpacing(20)

        self.email_login = self._create_input("Email", "Insira seu e-mail", "✉")
        layout.addLayout(self.email_login)

        self.pass_login = self._create_input("Password", "Digite sua senha", "🔒", is_password=True)
        layout.addLayout(self.pass_login)

        remember = QCheckBox("Lembrar-me")
        remember.setStyleSheet("color: white;")
        layout.addWidget(remember)

        layout.addStretch()

        btn_login = QPushButton("Login")
        btn_login.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_login.setStyleSheet("""
            QPushButton {
                background-color: #C1128C;
                color: white;
                border-radius: 20px;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #A00F75; }
        """)
        btn_login.clicked.connect(self.handle_login)
        layout.addWidget(btn_login)

        self.stack.addWidget(self.login_page)

    def setup_register_ui(self):
        self.register_page = QWidget()
        layout = QVBoxLayout(self.register_page)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(15)

        title = QLabel("Registro")
        title.setStyleSheet("color: white; font-size: 32px; font-weight: bold;")
        layout.addWidget(title)

        sub_text = QLabel("Se você ja tem uma conta registrada")
        sub_text.setStyleSheet("color: #BBBBBB; font-size: 14px;")
        layout.addWidget(sub_text)

        btn_go_log = QPushButton("Logue aqui")
        btn_go_log.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_go_log.setStyleSheet("color: #C1128C; text-align: left; font-size: 14px; border: none; background: none;")
        btn_go_log.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(btn_go_log)

        self.reg_nome = self._create_input("Nome", "Insira seu nome", "👤")
        layout.addLayout(self.reg_nome)

        self.reg_email = self._create_input("Email", "Insira seu e-mail", "✉")
        layout.addLayout(self.reg_email)

        self.reg_user = self._create_input("Usuario", "Insira seu usuario", "👤")
        layout.addLayout(self.reg_user)

        self.reg_pass = self._create_input("Senha", "Insira sua senha", "🔒", is_password=True)
        layout.addLayout(self.reg_pass)

        self.reg_confirm = self._create_input("Confirme a senha", "Confirme sua senha", "🔒", is_password=True)
        layout.addLayout(self.reg_confirm)

        layout.addStretch()

        btn_registrar = QPushButton("Registrar")
        btn_registrar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_registrar.setStyleSheet("""
            QPushButton {
                background-color: #C1128C;
                color: white;
                border-radius: 20px;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #A00F75; }
        """)
        btn_registrar.clicked.connect(self.handle_registrar)
        layout.addWidget(btn_registrar)

        self.stack.addWidget(self.register_page)

    def _create_input(self, label_text, placeholder, icon, is_password=False):
        v_layout = QVBoxLayout()
        v_layout.setSpacing(5)
        
        lbl = QLabel(label_text)
        lbl.setStyleSheet("color: white; font-size: 14px;")
        v_layout.addWidget(lbl)

        h_layout = QHBoxLayout()
        h_layout.setContentsMargins(0, 0, 0, 0)
        
        icon_lbl = QLabel(icon)
        icon_lbl.setStyleSheet("color: white; font-size: 16px;")
        
        edit = QLineEdit()
        edit.setPlaceholderText(placeholder)
        if is_password:
            edit.setEchoMode(QLineEdit.EchoMode.Password)
            
        edit.setStyleSheet("""
            QLineEdit {
                background: transparent;
                border: none;
                border-bottom: 2px solid white;
                color: white;
                padding-bottom: 5px;
            }
        """)
        
        h_layout.addWidget(icon_lbl)
        h_layout.addWidget(edit)
        v_layout.addLayout(h_layout)
        v_layout.input_field = edit
        return v_layout

    def handle_registrar(self):
        email = self.reg_email.input_field.text()
        nome = self.reg_nome.input_field.text()
        username = self.reg_user.input_field.text()
        senha = self.reg_pass.input_field.text()
        confirma = self.reg_confirm.input_field.text()
        try:
            auth_service.registrar(email, nome, username, senha, confirma)
            QMessageBox.information(self, "Sucesso", "Conta criada com sucesso! Faça seu login.")
            self.stack.setCurrentIndex(0)
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

    def handle_login(self):
        self.login_successful.emit("Admin")
        self.close()


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    win = AuthWindow()
    win.show()
    sys.exit(app.exec())
