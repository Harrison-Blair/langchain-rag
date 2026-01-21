from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, TabbedContent, TabPane

from src.gui.components.chat_interface import ChatInterface
from src.gui.components.file_interface import FileInterface

class DocumentRag(App):
    """A simple Textual app with a header, footer, and some dynamic tab content."""
    
    CSS_PATH = "main.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        with TabbedContent(initial="chat"):
            with TabPane("Chat", id="chat"):
                yield ChatInterface()
            with TabPane("Files", id="files"):
                yield FileInterface()
            yield TabPane("Settings", id="settings")
        yield Footer()