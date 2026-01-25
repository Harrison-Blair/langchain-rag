"""
Document manager for handling file i/o and document operations.
"""

from src.core.config_manager import config_manager

class DocumentManager():
    """Management interface for documents and file operations."""

    def __init__(self) -> None:
        self.directory = config_manager.get_config("document_directory")

    def get_document_list(self) -> list:
        """Retrieve list of documents in the managed directory."""
        import os
        documents = []
        for root, _, files in os.walk(self.directory):
            for file in files:
                documents.append(os.path.join(root, file))
        return documents
    
    def get_documents(self):
        pass

document_manager = DocumentManager()