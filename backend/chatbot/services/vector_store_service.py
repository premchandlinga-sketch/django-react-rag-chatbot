import os
from django.conf import settings
from langchain_chroma import Chroma

from chatbot.services.embedding_service import EmbeddingService


class VectorStoreService:

    @staticmethod
    def create_vector_store(chunks, collection_name, file_name=None):
        """
        Create vector store with file_name in metadata for easy deletion later.
        """
        if not chunks:
            raise ValueError("No text could be extracted from the document.")

        embeddings = EmbeddingService.get_embedding_model()

        persist_directory = os.path.join(
            settings.BASE_DIR, "chroma_db", collection_name
        )
        os.makedirs(persist_directory, exist_ok=True)

        # Add file_name to metadata for each chunk
        for chunk in chunks:
            if 'file_name' not in chunk.metadata:
                chunk.metadata['file_name'] = file_name

        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=persist_directory,
            collection_name=collection_name
        )

        return vector_store

    @staticmethod
    def load_vector_store(collection_name):
        embeddings = EmbeddingService.get_embedding_model()

        persist_directory = os.path.join(
            settings.BASE_DIR, "chroma_db", collection_name
        )

        return Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings,
            collection_name=collection_name
        )

    @staticmethod
    def retrieve_documents(query, collection_name, k=4):
        if not collection_name:
            return []

        vector_store = VectorStoreService.load_vector_store(collection_name)
        return vector_store.similarity_search(query=query, k=k)

    @staticmethod
    def delete_document_from_vector_store(collection_name, file_name):
        """Delete all chunks belonging to a specific uploaded file"""
        if not collection_name or not file_name:
            return False

        try:
            vector_store = VectorStoreService.load_vector_store(collection_name)
            
            # Get all items in collection
            collection_data = vector_store._collection.get(include=["metadatas"])
            
            if not collection_data or not collection_data.get('ids'):
                return True

            ids_to_delete = []
            for idx, metadata in enumerate(collection_data['metadatas']):
                if metadata and metadata.get('file_name') == file_name:
                    ids_to_delete.append(collection_data['ids'][idx])

            if ids_to_delete:
                vector_store._collection.delete(ids=ids_to_delete)
                print(f"✅ Deleted {len(ids_to_delete)} chunks for file: {file_name}")
                return True
            else:
                print(f"No chunks found for file: {file_name}")
                return True

        except Exception as e:
            print(f"Error deleting from vector store: {e}")
            return False