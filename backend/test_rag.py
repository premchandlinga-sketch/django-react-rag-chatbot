from chatbot.services.rag_service import (
    RAGService
)

question = input("Ask: ")

response = RAGService.ask(
    question
)

print("\nAnswer:\n")

print(response)