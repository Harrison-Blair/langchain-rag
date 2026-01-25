"""
Singleton class to manage vector stores within the application.
"""
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

from src.core.config_manager import config_manager
from src.core.document_manager import document_manager

class VectorStoreManager():
    """Management interface for chromadb vector store."""

    def __init__(self):
        self._embeddings = OllamaEmbeddings(
            model=config_manager.get_config("embeddings")["model"]
        )
        self.vectorstore = Chroma(
            collection_name="default_collection",
            embedding_function=self._embeddings,
            persist_directory=config_manager.get_config("vectorstore_directory"),
        )

    def populate_vectorstore(self):
        """Populate the vector store with documents."""
        uuids, documents = document_manager.get_documents_with_uuids()
        self.vectorstore.add_documents(documents=documents, ids=uuids)


vectorstore_manager = VectorStoreManager()