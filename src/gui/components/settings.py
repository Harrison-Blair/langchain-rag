from textual.widgets import Static, Label, Switch, Select
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal

class SettingsPanel(Vertical):
    """A custom widget for the settings panel."""
    
    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Label("Model:")
            yield Select([("DeepSeek-R1", "deepseek-r1"), ("Llama 3", "llama3")], prompt="Select Model")
        
        with Horizontal():
            yield Label("Dark Mode:")
            yield Switch(value=True, id="toggle-dark-mode")

    def on_switch_changed(self, event: Switch.Changed) -> None:
        """Handle toggle switch changes."""
        if event.switch.id == "toggle-dark-mode":
            self.app.theme = "textual-dark" if event.value else "textual-light"

    def on_select_changed(self, event: Select.Changed) -> None:
        """Handle select widget changes."""
        self.notify(f"Model settings saved: {event.value}")
