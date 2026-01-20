from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QTextEdit,
    QLabel, QDateEdit, QComboBox
)
from PySide6.QtCore import QDate, QTimer
from services.pages_service import update_page, get_page_by_id


class PageEditorWindow(QWidget):
    def __init__(self, page_id):
        super().__init__()
        self.page_id = page_id
        self.setWindowTitle("Page Editor")

        self.save_timer = QTimer()
        self.save_timer.setSingleShot(True)
        self.save_timer.timeout.connect(self.save)

        self.setup_ui()
        self.load_page()

    def setup_ui(self):
        self.title_input = QLineEdit()
        self.content_input = QTextEdit()

        self.due_date_input = QDateEdit()
        self.due_date_input.setCalendarPopup(True)
        self.due_date_input.setDisplayFormat("yyyy-MM-dd")

        self.status_input = QComboBox()
        self.status_input.addItems(["pending", "done"])

        self.save_status = QLabel("Saved ✓")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Title"))
        layout.addWidget(self.title_input)

        layout.addWidget(QLabel("Content"))
        layout.addWidget(self.content_input)

        layout.addWidget(QLabel("Due Date"))
        layout.addWidget(self.due_date_input)

        layout.addWidget(QLabel("Status"))
        layout.addWidget(self.status_input)

        layout.addWidget(self.save_status)
        self.setLayout(layout)

        # debounce autosave
        self.title_input.textChanged.connect(self.trigger_save)
        self.content_input.textChanged.connect(self.trigger_save)
        self.due_date_input.dateChanged.connect(self.trigger_save)
        self.status_input.currentTextChanged.connect(self.trigger_save)

    def load_page(self):
        page = get_page_by_id(self.page_id)

        self.title_input.setText(page["title"])
        self.content_input.setText(page["content"] or "")

        if page["due_date"]:
            self.due_date_input.setDate(
                QDate.fromString(page["due_date"], "yyyy-MM-dd")
            )
        else:
            self.due_date_input.setDate(QDate.currentDate())

        self.status_input.setCurrentText(page.get("status", "pending"))

    def trigger_save(self):
        self.save_status.setText("Saving...")
        self.save_timer.start(500)  # 500ms debounce

    def save(self):
        update_page(
            self.page_id,
            title=self.title_input.text(),
            content=self.content_input.toPlainText(),
            due_date=self.due_date_input.date().toString("yyyy-MM-dd"),
            status=self.status_input.currentText()
        )
        self.save_status.setText("Saved ✓")
