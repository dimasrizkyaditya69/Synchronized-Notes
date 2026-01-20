from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox
)

from services.auth_service import login, register
from ui.app_window import AppWindow


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Synchronized Notes - Login")
        self.setFixedWidth(300)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Synchronized Notes")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        login_button = QPushButton("Login")
        login_button.clicked.connect(self.handle_login)

        register_button = QPushButton("Register")
        register_button.clicked.connect(self.handle_register)

        layout.addWidget(title)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)
        layout.addWidget(register_button)

        self.setLayout(layout)

    # ---------- LOGIN ----------

    def handle_login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not email or not password:
            QMessageBox.warning(self, "Error", "Email dan password wajib diisi.")
            return

        try:
            session, user = login(email, password)

            if user:
                self.app = AppWindow(user)
                self.app.show()
                self.close()

        except Exception as e:
            QMessageBox.warning(self, "Login gagal", str(e))

    # ---------- REGISTER ----------

    def handle_register(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not email or not password:
            QMessageBox.warning(self, "Error", "Email dan password wajib diisi.")
            return

        if len(password) < 6:
            QMessageBox.warning(
                self,
                "Password lemah",
                "Password minimal 6 karakter."
            )
            return

        try:
            register(email, password)
            QMessageBox.information(
                self,
                "Register berhasil",
                "Akun berhasil dibuat.\nSilakan login."
            )
        except Exception as e:
            QMessageBox.warning(self, "Register gagal", str(e))
