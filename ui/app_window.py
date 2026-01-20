from PySide6.QtWidgets import QWidget, QHBoxLayout, QSplitter
from ui.workspace_sidebar import WorkspaceSidebar
from ui.page_editor_widget import PageEditorWidget

class AppWindow(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle("synchronized notes")

        self.editor = PageEditorWidget()

        self.sidebar = WorkspaceSidebar(
            user=self.user,
            on_page_selected=self.open_page
        )

        splitter = QSplitter()
        splitter.addWidget(self.sidebar)
        splitter.addWidget(self.editor)
        splitter.setSizes([300, 700])

        layout = QHBoxLayout()
        layout.addWidget(splitter)
        self.setLayout(layout)

    def open_page(self, page_id):
        self.editor.load_page(page_id)
