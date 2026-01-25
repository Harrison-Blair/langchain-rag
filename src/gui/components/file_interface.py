from textual.app import ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Collapsible, Button, DirectoryTree

from src.core.vectorstore_manager import vectorstore_manager
from src.core.document_manager import document_manager

class FileInterface(VerticalScroll):
    """A file interface component for the files tab."""
    
    def __init__(self) -> None:
        super().__init__()
        self.vectorstore_manager = vectorstore_manager

    def compose(self) -> ComposeResult:
        with Collapsible(title="Raw Files"): 
            yield DirectoryTree(document_manager.directory, id="file-tree")
            with Horizontal(classes="auto-height"):
                yield Button("Refresh", id="refresh-files")
                yield Button("Open In Explorer", id="open-explorer")
        with Horizontal():
            yield Button("Populate Vectorstore Debug", id="populate-vectorstore")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        button_id = event.button.id
        if button_id == "refresh-files":
            self.refresh_file_tree()
        elif button_id == "open-explorer":
            self.open_in_explorer()
        elif button_id == "populate-vectorstore":
            self.vectorstore_manager.populate_vectorstore()
            self.notify("Vector store has been populated with documents.")

    def refresh_file_tree(self) -> None:
        """Refresh the file tree to reflect current files."""
        file_tree = self.query_one("#file-tree", DirectoryTree)
        file_tree.refresh()

    def open_in_explorer(self) -> None:
        """Open the data directory in the system's file explorer."""
        import os
        import platform
        path = os.path.abspath(self.UPLOAD_DIR)
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            os.system(f"open {path}")
        else:
            os.system(f"xdg-open {path}")