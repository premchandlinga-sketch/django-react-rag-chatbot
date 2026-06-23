from chatbot.services.vector_store_service import (
    VectorStoreService
)

results = (
    VectorStoreService.retrieve_documents(
        query="What is machine learning?",
        k=3
    )
)

print("Retrieved:", len(results))

for index, doc in enumerate(results):

    print("\n")
    print("Chunk", index + 1)
    print("-" * 50)

    print(
        doc.page_content[:500]
    )