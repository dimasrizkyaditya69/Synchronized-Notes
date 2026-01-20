from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QListWidget, QListWidgetItem,
    QLineEdit, QComboBox,
    QMessageBox, QMenu, QPushButton, QInputDialog
)
from PySide6.QtCore import Qt

from services.workspace_service import get_workspaces, delete_workspace, create_workspace

from services.pages_service import get_pages, delete_page, create_page


class WorkspaceSidebar(QWidget):
    def __init__(self, user, on_page_selected):
        super().__init__()
        self.user = user
        self.on_page_selected = on_page_selected
        self.current_workspace_id = None

        self.setup_ui()
        self.load_workspaces()

    def create_new_workspace(self):
        name, ok = QInputDialog.getText(
            self, "New Workspace", "Workspace name:"
        )
        if ok and name:
            create_workspace(name, self.user.id)
            self.load_workspaces()

    def create_new_page(self):
        if not self.current_workspace_id:
            return

        title, ok = QInputDialog.getText(
            self, "New Page", "Page title:"
        )
        if ok and title:
            create_page(self.current_workspace_id, title)
            self.load_pages()



    def setup_ui(self):
        self.workspace_list = QListWidget()
        self.workspace_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.workspace_list.customContextMenuRequested.connect(
            self.open_workspace_menu
        )

        self.pages_list = QListWidget()
        self.pages_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.pages_list.customContextMenuRequested.connect(
            self.open_page_menu
        )

        self.new_workspace_btn = QPushButton("+ New Workspace")
        self.new_workspace_btn.clicked.connect(self.create_new_workspace)

        self.new_page_btn = QPushButton("+ New Page")
        self.new_page_btn.clicked.connect(self.create_new_page)
        self.new_page_btn.setEnabled(False)  # aktif setelah workspace dipilih

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search pages...")
        self.search_input.textChanged.connect(self.apply_filters)

        self.status_filter = QComboBox()
        self.status_filter.addItems(["all", "pending", "done"])
        self.status_filter.currentTextChanged.connect(self.apply_filters)

        self.workspace_list.itemClicked.connect(self.select_workspace)
        self.pages_list.itemClicked.connect(self.select_page)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Workspaces"))
        layout.addWidget(self.new_workspace_btn)
        layout.addWidget(self.workspace_list)

        layout.addWidget(QLabel("Pages"))
        layout.addWidget(self.new_page_btn)
        layout.addWidget(self.search_input)
        layout.addWidget(self.status_filter)
        layout.addWidget(self.pages_list)

        self.setLayout(layout)


    # ---------- WORKSPACES ----------

    def load_workspaces(self):
        self.workspace_list.clear()
        res = get_workspaces(self.user.id)

        for w in res.data:
            item = QListWidgetItem(w["name"])
            item.setData(256, w["id"])
            self.workspace_list.addItem(item)

    def select_workspace(self, item):
        self.current_workspace_id = item.data(256)
        self.new_page_btn.setEnabled(True)   # 🔥 INI
        self.load_pages()

    def open_workspace_menu(self, position):
        item = self.workspace_list.itemAt(position)
        if not item:
            return

        menu = QMenu()
        delete_action = menu.addAction("Delete Workspace")
        action = menu.exec(self.workspace_list.mapToGlobal(position))

        if action == delete_action:
            self.confirm_delete_workspace(item)

    def confirm_delete_workspace(self, item):
        workspace_id = item.data(256)
        name = item.text()

        confirm = QMessageBox.question(
            self,
            "Delete Workspace",
            f"Delete workspace '{name}'?\n\nAll pages will be deleted.",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            delete_workspace(workspace_id)
            self.current_workspace_id = None
            self.pages_list.clear()
            self.load_workspaces()

    # ---------- PAGES ----------

    def load_pages(self):
        self.pages_list.clear()
        if not self.current_workspace_id:
            return

        res = get_pages(self.current_workspace_id)

        for p in res.data:
            item = QListWidgetItem(p["title"])
            item.setData(256, p["id"])
            item.setData(257, p["status"])
            self.pages_list.addItem(item)

        self.apply_filters()

    def open_page_menu(self, position):
        item = self.pages_list.itemAt(position)
        if not item:
            return

        menu = QMenu()
        delete_action = menu.addAction("Delete Page")
        action = menu.exec(self.pages_list.mapToGlobal(position))

        if action == delete_action:
            self.confirm_delete_page(item)

    def confirm_delete_page(self, item):
        page_id = item.data(256)
        title = item.text()

        confirm = QMessageBox.question(
            self,
            "Delete Page",
            f"Delete page '{title}'?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            delete_page(page_id)
            self.load_pages()

    # ---------- FILTER ----------

    def apply_filters(self):
        keyword = self.search_input.text().lower()
        status = self.status_filter.currentText()

        for i in range(self.pages_list.count()):
            item = self.pages_list.item(i)
            title_match = keyword in item.text().lower()
            status_match = status == "all" or item.data(257) == status
            item.setHidden(not (title_match and status_match))

    def select_page(self, item):
        self.on_page_selected(item.data(256))
