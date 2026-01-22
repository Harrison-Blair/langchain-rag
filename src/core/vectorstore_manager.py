"""
Singleton class to manage vector stores within the application.
"""
import chromadb

class VectorStoreManager():
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./data/vectorstores/")
        self.vectorstore = None

    def get_collections(self):
        """Retrieve all collections from the vector store."""
        return self.client.list_collections()
    
    def create_collection(self, name: str):
        """Create a new collection in the vector store."""
        return self.client.create_collection(name=name)

vectorstore_manager = VectorStoreManager()