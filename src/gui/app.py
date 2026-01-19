from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, TabbedContent, TabPane

# Import our new separate components
from src.gui.components.chat import ChatInterface
from src.gui.components.files import FileBrowser
from src.gui.components.settings import SettingsPanel

class DocumentRag(App):
    """A simple Textual app with a header, footer, and some dynamic tab content."""
    
    CSS_PATH = "main.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        with TabbedContent(initial="chat"):
            with TabPane("Chat", id="chat"):
                yield ChatInterface()
            with TabPane("Files", id="files"):
                yield FileBrowser()
            with TabPane("Settings", id="settings"):
                yield SettingsPanel()
        yield Footer()