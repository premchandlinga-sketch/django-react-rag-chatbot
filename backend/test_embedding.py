from chatbot.services.embedding_service import (
    EmbeddingService
)

embeddings = (
    EmbeddingService.get_embedding_model()
)

vector = embeddings.embed_query(
    "What is machine learning?"
)

print("Vector Length:", len(vector))

print(vector[:10])