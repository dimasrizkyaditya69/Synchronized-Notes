from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout,
    QListWidget, QListWidgetItem, QInputDialog, QMessageBox
)

from services.pages_service import get_pages, create_page
from ui.page_editor_window import PageEditorWindow   

# editor (nanti kita bikin)

class PagesWindow(QWidget):
    def __init__(self, user, workspace_id, workspace_name):
        super().__init__()
        self.user = user
        self.workspace_id = workspace_id
        self.setWindowTitle(f"Pages — {workspace_name}")
        self.setup_ui()
        self.load_pages()

    def setup_ui(self):
        self.pages_list = QListWidget()
        self.pages_list.itemDoubleClicked.connect(self.open_page)  # 🔥 penting

        new_button = QPushButton("New Page")
        new_button.clicked.connect(self.create_new_page)

        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.load_pages)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Pages"))
        layout.addWidget(self.pages_list)
        layout.addWidget(new_button)
        layout.addWidget(refresh_button)

        self.setLayout(layout)

    def load_pages(self):
        res = get_pages(self.workspace_id)
        self.pages_list.clear()

        for p in res.data:
            item = QListWidgetItem(p["title"])   # text yg keliatan
            item.setData(256, p["id"])           # simpen page_id (hidden)
            self.pages_list.addItem(item)

    def create_new_page(self):
        title, ok = QInputDialog.getText(self, "New Page", "Page Title:")
        if ok and title:
            create_page(self.workspace_id, title)
            QMessageBox.information(self, "Created", f"Page '{title}' created!")
            self.load_pages()

    def open_page(self, item):
        page_id = item.data(256)
        print("OPEN PAGE:", page_id)  # debug dulu
        self.editor = PageEditorWindow(page_id)
        self.editor.show()
