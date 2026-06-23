from chatbot.services.document_service import DocumentService

documents = DocumentService.load_pdf(
    "sample.pdf"
)

chunks = DocumentService.split_documents(
    documents
)

print("Pages:", len(documents))

print("Chunks:", len(chunks))

print(chunks[0].page_content[:500])

print(chunks[0].metadata)