"""
Document manager for handling file i/o and document operations.
"""
from langchain_community.document_loaders import PyMuPDFLoader

from src.core.config_manager import config_manager

class DocumentManager():
    """Management interface for documents and file operations."""

    def __init__(self) -> None:
        self.directory = config_manager.get_config("document_directory")

    def get_document_list(self) -> list:
        """Retrieve list of documents in the managed directory."""
        import os
        document_names = []
        for root, _, files in os.walk(self.directory):
            for file in files:
                document_names.append(os.path.join(root, file))
        return document_names
    
    def get_documents(self):
        """Load and return documents from the managed directory."""
        documents = []
        for doc in self.get_document_list():
            loader = PyMuPDFLoader(doc)
            documents.extend(loader.load())
        return documents
    
    def get_documents_with_uuids(self):
        """Load documents and assign a unique ID to each."""
        from uuid import uuid4
        documents = self.get_documents()
        uuids = [str(uuid4()) for _ in range(len(documents))]
        return uuids, documents

document_manager = DocumentManager()