from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout,
    QListWidget, QListWidgetItem, QInputDialog, QMessageBox
)
from services.workspace_service import get_workspaces, create_workspace
from ui.pages_window import PagesWindow  # NEW

class WorkspaceWindow(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle("Your Workspaces")
        self.setup_ui()
        self.load_workspaces()

    def setup_ui(self):
        self.workspace_list = QListWidget()
        self.workspace_list.itemDoubleClicked.connect(self.open_workspace)  # NEW

        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.load_workspaces)

        new_button = QPushButton("New Workspace")
        new_button.clicked.connect(self.create_new_workspace)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Hello {self.user.email}!"))
        layout.addWidget(self.workspace_list)
        layout.addWidget(refresh_button)
        layout.addWidget(new_button)
        self.setLayout(layout)

    def load_workspaces(self):
        res = get_workspaces(self.user.id)
        self.workspace_list.clear()

        for w in res.data:
            item = QListWidgetItem(w["name"])
            item.setData(256, w["id"])  # simpan workspace_id
            self.workspace_list.addItem(item)

    def create_new_workspace(self):
        name, ok = QInputDialog.getText(self, "New Workspace", "Workspace Name:")
        if ok and name:
            create_workspace(name, self.user.id)
            QMessageBox.information(self, "Created", f"Workspace '{name}' created!")
            self.load_workspaces()

    def open_workspace(self, item):
        workspace_id = item.data(256)
        self.pages = PagesWindow(self.user, workspace_id, item.text())
        self.pages.show()
