from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter)

class DocumentService:

    @staticmethod
    def load_pdf(pdf_path):

        loader = PyPDFLoader(pdf_path)

        documents = loader.load()

        return documents

    @staticmethod
    def split_documents(documents):

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        chunks = splitter.split_documents(
            documents
       )

        return chunks

     