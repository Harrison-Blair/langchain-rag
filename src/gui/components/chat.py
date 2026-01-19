from textual.widgets import Static, Input, Button
from textual.app import ComposeResult
from textual.containers import Vertical

class ChatInterface(Vertical):
    """A custom widget for the chat interface."""
    
    def compose(self) -> ComposeResult:
        yield Static("Welcome to RAG Chat", id="chat-history")
        yield Input(placeholder="Ask a question...", id="chat-input")
        yield Button("Send", id="send-button")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        if event.button.id == "send-button":
            # Placeholder for sending message logic
            pass
