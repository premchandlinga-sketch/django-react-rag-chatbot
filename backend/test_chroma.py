from chatbot.services.document_service import (
    DocumentService
)

from chatbot.services.vector_store_service import (
    VectorStoreService
)

documents = DocumentService.load_pdf(
    "sample.pdf"
)

chunks = DocumentService.split_documents(
    documents
)

vector_store = (
    VectorStoreService.create_vector_store(
        chunks
    )
)

print("Chunks Stored:", len(chunks))