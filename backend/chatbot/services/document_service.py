from langchain_community.document_loaders import PyMuPDFLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocumentService:

    @staticmethod
    def load_pdf(pdf_path):
        """Load PDF with best available loader"""
        try:
            # PyMuPDF is generally better and faster
            loader = PyMuPDFLoader(pdf_path)
            return loader.load()
        except Exception:
            # Fallback to PyPDFLoader
            loader = PyPDFLoader(pdf_path)
            return loader.load()

    @staticmethod
    def split_documents(documents):
        """Split documents into chunks"""
        if not documents:
            return []

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150,
            separators=["\n\n", "\n", ".", "!", "?", " ", ""]
        )

        return text_splitter.split_documents(documents)