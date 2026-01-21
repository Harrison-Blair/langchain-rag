from textual.app import ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.widgets import Collapsible, Button, DirectoryTree

class FileInterface(VerticalScroll):
    """A file interface component for the files tab."""

    def compose(self) -> ComposeResult:
        with Collapsible(title="Files"): 
            with Vertical():
                yield DirectoryTree("./data/", id="file-tree")
                yield Button("Refresh", id="refresh-files")
        yield Button()