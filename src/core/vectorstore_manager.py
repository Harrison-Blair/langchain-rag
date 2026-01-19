from pathlib import Path
from typing import Callable, Optional

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

from src.core.document_manager import DocumentManager


# Type alias for progress callback: (current, total, message)
ProgressCallback = Callable[[int, int, str], None]


class VectorStoreManager:
    """Manages the Chroma vector store and embeddings."""

    UPLOADS_PATH = Path("./data/uploads")
    VECTORSTORE_PATH = Path("./data/vectorstore")

    def __init__(self, embedding_model: str = "nomic-embed-text"):
        self.uploads_path = self.UPLOADS_PATH.resolve()
        self.vectorstore_path = self.VECTORSTORE_PATH.resolve()
        
        self.embedding_model = embedding_model
        self._vectorstore = None
        self._doc_manager = DocumentManager(
            uploads_path=str(self.uploads_path),
            vectorstore_path=str(self.vectorstore_path)
        )

    @property
    def embeddings(self):
        return OllamaEmbeddings(model=self.embedding_model)

    def get_vectorstore(self):
        """Load or create the vector store."""
        if self._vectorstore is None:
            self.vectorstore_path.mkdir(parents=True, exist_ok=True)
            self._vectorstore = Chroma(
                persist_directory=str(self.vectorstore_path),
                embedding_function=self.embeddings
            )
        return self._vectorstore
    
    def build(self, progress_callback: Optional[ProgressCallback] = None, batch_size: int = 10):
        """
        Build the vector store from uploaded documents.
        
        Args:
            progress_callback: Optional callback(current, total, message) for progress updates
            batch_size: Number of chunks to process per batch (for progress reporting)
        """
        import shutil
        
        def report(current: int, total: int, message: str):
            if progress_callback:
                progress_callback(current, total, message)
        
        report(0, 100, "Loading documents...")
        docs = self._doc_manager.load_uploads()

        # Clear existing store
        if self.VECTORSTORE_PATH.exists():
            shutil.rmtree(self.VECTORSTORE_PATH)
        self._vectorstore = None
        
        report(5, 100, "Splitting into chunks...")
        
        # Load and split documents using your DocumentManager
        chunks = self._doc_manager.split_documents(
            docs=docs,
            chunk_size=1024,
            chunk_overlap=200
        )
        
        if not chunks:
            report(100, 100, "No documents found.")
            return 0
        
        total_chunks = len(chunks)
        report(10, 100, f"Creating embeddings for {total_chunks} chunks...")
        
        # Process in batches for progress feedback
        self.vectorstore_path.mkdir(parents=True, exist_ok=True)
        self._vectorstore = None
        
        for i in range(0, total_chunks, batch_size):
            batch = chunks[i:i + batch_size]
            batch_num = i // batch_size + 1
            total_batches = (total_chunks + batch_size - 1) // batch_size
            
            # Calculate progress (10-95% range for embedding phase)
            progress = 10 + int((i / total_chunks) * 85)
            report(progress, 100, f"Processing batch {batch_num}/{total_batches} ({i + len(batch)}/{total_chunks} chunks)")
            
            if self._vectorstore is None:
                # First batch - create the store
                self._vectorstore = Chroma.from_documents(
                    documents=batch,
                    embedding=self.embeddings,
                    persist_directory=str(self.vectorstore_path)
                )
            else:
                # Subsequent batches - add to existing store
                self._vectorstore.add_documents(batch)
        
        report(100, 100, f"Done! Indexed {total_chunks} chunks.")
        return total_chunks
    
    def search(self, query: str, k: int = 4):
        """Search for similar documents."""
        vectorstore = self.get_vectorstore()
        return vectorstore.similarity_search(query, k=k)

    def search_with_scores(self, query: str, k: int = 4):
        """Search with relevance scores."""
        vectorstore = self.get_vectorstore()
        return vectorstore.similarity_search_with_score(query, k=k)