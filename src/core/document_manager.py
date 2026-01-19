from langchain_community.document_loaders import DirectoryLoader, PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocumentManager():
    """A class responsible for loading documents from specified paths."""
    def __init__(self, uploads_path: str, vectorstore_path: str):
        self.uploads_path = uploads_path
        self.vectorstore_path = vectorstore_path

    def load_uploads(self):
        """Load PDF documents from the uploads directory."""
        loader = DirectoryLoader(
            self.uploads_path,
            glob="**/*.pdf",
            loader_cls=PyMuPDFLoader
        )
        documents = loader.load()
        return documents
    
    def split_documents(self, docs, chunk_size: int = 1024, chunk_overlap: int = 200, add_start_index: bool = True):
        """Document splitting logic."""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            add_start_index=add_start_index
        )
        documents = self.load_uploads()
        return text_splitter.split_documents(docs)