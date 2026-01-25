"""
Singleton class to manage vector stores within the application.
"""
import chromadb
from chromadb.config import Settings

class VectorStoreManager():
    """Management interface for chromadb vector store."""

    def __init__(self):
        self._client = chromadb.PersistentClient(
            path="./data/vectorstores/",
            settings=Settings(allow_reset=True)
            )
        self.vectorstore = None

    def get_collections(self):
        """Retrieve all collections from the vector store."""
        return self._client.list_collections()
    
    def create_collection(self, name: str):
        """Create a new collection in the vector store."""
        return self._client.create_collection(name=name)
    
    def reset_collections(self):
        """Reset all collections in the vector store."""
        self._client.reset()

vectorstore_manager = VectorStoreManager()