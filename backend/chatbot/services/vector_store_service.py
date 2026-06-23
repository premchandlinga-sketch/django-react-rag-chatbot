from langchain_chroma import Chroma

from chatbot.services.embedding_service import (
    EmbeddingService
)


class VectorStoreService:

    @staticmethod
    def create_vector_store(chunks):

        embeddings = (
            EmbeddingService.get_embedding_model()
        )

        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory="chroma_db"
        )

        return vector_store


    @staticmethod
    def load_vector_store():

        embeddings = (
            EmbeddingService.get_embedding_model()
        )

        vector_store = Chroma(
            persist_directory="chroma_db",
            embedding_function=embeddings
        )

        return vector_store


    @staticmethod
    def retrieve_documents(query, k=3):

        vector_store = (
            VectorStoreService.load_vector_store()
        )

        results = vector_store.similarity_search(
            query=query,
            k=k
        )

        return results