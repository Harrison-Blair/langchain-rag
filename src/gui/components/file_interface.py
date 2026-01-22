from textual.app import ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Collapsible, Button, DirectoryTree

from src.core.vectorstore_manager import vectorstore_manager

class FileInterface(VerticalScroll):
    """A file interface component for the files tab."""

    UPLOAD_DIR = "./data/uploads/"
    
    def __init__(self) -> None:
        super().__init__()
        self.vectorstore_manager = vectorstore_manager

    def compose(self) -> ComposeResult:
        with Collapsible(title="Raw Files"): 
            yield DirectoryTree(self.UPLOAD_DIR, id="file-tree")
            with Horizontal(classes="auto-height"):
                yield Button("Refresh", id="refresh-files")
                yield Button("Open In Explorer", id="open-explorer")
        with Horizontal():
            yield Button("Get Collections Debug", id="get-collections")
            yield Button("Make Collection Debug", id="make-collection")
            yield Button("Reset collections Debug", id="reset-collections")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        button_id = event.button.id
        if button_id == "refresh-files":
            self.refresh_file_tree()
        elif button_id == "open-explorer":
            self.open_in_explorer()
        elif button_id == "get-collections":
            collections = self.vectorstore_manager.get_collections()
            self.notify(f"Vector Store Collections: {collections}")
        elif button_id == "make-collection":
            self.vectorstore_manager.create_collection("test_collection")
            self.notify("Created test_collection in vector store.")
        elif button_id == "reset-collections":
            self.vectorstore_manager.client.reset()
            self.notify("Vector store collections have been reset.")

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