from langchain_chroma import Chroma

from chatbot.services.embedding_service import (
    EmbeddingService
)


class VectorStoreService:

    @staticmethod
    def create_vector_store(
        chunks,
        collection_name
    ):

        embeddings = (
            EmbeddingService.get_embedding_model()
        )

        persist_directory = (
            f"chroma_db/{collection_name}"
        )

        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=persist_directory
        )

        return vector_store

    @staticmethod
    def load_vector_store(
        collection_name
    ):

        embeddings = (
            EmbeddingService.get_embedding_model()
        )

        persist_directory = (
            f"chroma_db/{collection_name}"
        )

        vector_store = Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings
        )

        return vector_store

    @staticmethod
    def retrieve_documents(
        query,
        collection_name,
        k=3
    ):

        if not collection_name:

            return []

        vector_store = (
            VectorStoreService.load_vector_store(
                collection_name
            )
        )

        results = vector_store.similarity_search(
            query=query,
            k=k
        )

        return results