from textual.widgets import Input
from textual.app import ComposeResult
from textual.containers import Vertical, VerticalScroll

class ChatInterface(Vertical):
    """A chat interface component for the chat tab."""

    def compose(self) -> ComposeResult:
        yield VerticalScroll()
        yield Input(placeholder="Type your message here...", id="chat-input")