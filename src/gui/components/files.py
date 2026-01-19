from pathlib import Path
from textual.widgets import DirectoryTree, Button, Static, ProgressBar
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.worker import Worker, WorkerState

from src.core.vectorstore_manager import VectorStoreManager


class FileBrowser(Vertical):
    """A custom widget for the file browser."""

    def __init__(self):
        super().__init__()
        self.vs_manager = VectorStoreManager()

    def compose(self) -> ComposeResult:
        uploads_path = Path("./data/uploads").resolve()
        vectorstore_path = Path("./data/vectorstore").resolve()

        yield DirectoryTree(str(uploads_path), id="uploads-tree")

        chroma_exists = (vectorstore_path / "chroma.sqlite3").exists()
        yield Static(f"Vectorstore: {'✓ Ready' if chroma_exists else '✗ Not built'}", id="vectorstore-status")
        yield Static("Ready", id="build-status")
        yield ProgressBar(total=100, show_eta=False, id="build-progress")
        with Horizontal():
            yield Button("↻ Refresh Files", id="refresh-files")
            yield Button("Build Vectorstore", id="build-vectorstore", variant="primary")

    def on_mount(self) -> None:
        """Hide progress bar initially."""
        self.query_one("#build-progress", ProgressBar).display = False

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        if event.button.id == "refresh-files":
            self.reload_tree()
        elif event.button.id == "build-vectorstore":
            self.build_vectorstore()

    def reload_tree(self) -> None:
        """Reload the directory tree to reflect any file changes."""
        uploads_tree = self.query_one("#uploads-tree", DirectoryTree)
        uploads_tree.reload()
        self.update_vectorstore_status()
        self.notify("File list refreshed")

    def update_vectorstore_status(self) -> None:
        """Update the vectorstore status indicator."""
        vectorstore_path = Path("./data/vectorstore").resolve()
        chroma_exists = (vectorstore_path / "chroma.sqlite3").exists()
        status = self.query_one("#vectorstore-status", Static)
        status.update(f"Vectorstore: {'✓ Ready' if chroma_exists else '✗ Not built'}")

    def build_vectorstore(self) -> None:
        """Start building the vector store in the background."""
        # Show progress bar
        progress_bar = self.query_one("#build-progress", ProgressBar)
        progress_bar.display = True
        progress_bar.progress = 0
        
        # Disable button during build
        build_btn = self.query_one("#build-vectorstore", Button)
        build_btn.disabled = True
        
        # Update status
        status = self.query_one("#build-status", Static)
        status.update("Starting build...")
        
        # Run build in background worker
        self._run_build_worker()

    def _update_progress(self, current: int, total: int, message: str) -> None:
        """Update progress bar and status (called from main thread via call_from_thread)."""
        try:
            progress_bar = self.query_one("#build-progress", ProgressBar)
            progress_bar.progress = current
            
            status = self.query_one("#build-status", Static)
            status.update(message)
        except Exception:
            pass  # Widget might not exist if app is closing

    def _run_build_worker(self) -> None:
        """Run the build in a worker thread."""
        app = self.app  # Capture reference for the closure
        
        def do_build() -> int:
            def progress_callback(current: int, total: int, message: str):
                # Safely update UI from worker thread
                app.call_from_thread(self._update_progress, current, total, message)
            
            return self.vs_manager.build(progress_callback=progress_callback)
        
        self.run_worker(do_build, thread=True, exclusive=True)

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        """Handle worker completion."""
        if event.state == WorkerState.SUCCESS:
            num_chunks = event.worker.result
            self.notify(f"Vectorstore built with {num_chunks} chunks!")
            self.update_vectorstore_status()
            
            status = self.query_one("#build-status", Static)
            status.update(f"Done! Indexed {num_chunks} chunks.")
            
        elif event.state == WorkerState.ERROR:
            self.notify(f"Build failed: {event.worker.error}", severity="error")
            status = self.query_one("#build-status", Static)
            status.update(f"Error: {event.worker.error}")
        
        # Re-enable button and hide progress bar when done
        if event.state in (WorkerState.SUCCESS, WorkerState.ERROR, WorkerState.CANCELLED):
            build_btn = self.query_one("#build-vectorstore", Button)
            build_btn.disabled = False
            
            progress_bar = self.query_one("#build-progress", ProgressBar)
            progress_bar.display = False
