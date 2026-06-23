from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingService:

    @staticmethod
    def get_embedding_model():

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        return embeddings