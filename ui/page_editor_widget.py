from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QTextEdit,
    QLabel, QDateEdit, QComboBox
)
from PySide6.QtCore import QDate, QTimer
from services.pages_service import get_page_by_id, update_page

class PageEditorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.page_id = None

        self.save_timer = QTimer()
        self.save_timer.setSingleShot(True)
        self.save_timer.timeout.connect(self.save)

        self.setup_ui()

    def setup_ui(self):
        self.title = QLineEdit()
        self.content = QTextEdit()
        self.due_date = QDateEdit()
        self.status = QComboBox()
        self.status.addItems(["pending", "done"])
        self.info = QLabel("No page selected")

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.content)
        layout.addWidget(self.due_date)
        layout.addWidget(self.status)
        layout.addWidget(self.info)
        self.setLayout(layout)

        self.title.textChanged.connect(self.trigger_save)
        self.content.textChanged.connect(self.trigger_save)
        self.due_date.dateChanged.connect(self.trigger_save)
        self.status.currentTextChanged.connect(self.trigger_save)

    def load_page(self, page_id):
        self.page_id = page_id
        page = get_page_by_id(page_id)

        self.title.setText(page["title"])
        self.content.setText(page["content"] or "")
        self.status.setCurrentText(page["status"])
        self.due_date.setDate(
            QDate.fromString(page["due_date"], "yyyy-MM-dd")
            if page["due_date"] else QDate.currentDate()
        )
        self.info.setText("Saved ✓")

    def trigger_save(self):
        if self.page_id:
            self.info.setText("Saving...")
            self.save_timer.start(400)

    def save(self):
        if not self.page_id:
            return
        update_page(
            self.page_id,
            title=self.title.text(),
            content=self.content.toPlainText(),
            due_date=self.due_date.date().toString("yyyy-MM-dd"),
            status=self.status.currentText()
        )
        self.info.setText("Saved ✓")
