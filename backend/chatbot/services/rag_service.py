from chatbot.services.vector_store_service import (
    VectorStoreService
)

from chatbot.services.llm_service import (
    LLMService
)


class RAGService:

    @staticmethod
    def ask(
        question,
        collection_name,
        conversation_history=""
    ):

        retrieved_docs = (
            VectorStoreService.retrieve_documents(
                query=question,
                collection_name=collection_name,
                k=3
            )
        )

        context = "\n\n".join(
            [
                doc.page_content
                for doc in retrieved_docs
            ]
        )

        prompt = f"""
You are a helpful AI assistant.

Conversation History:
{conversation_history}

Context:
{context}

Current Question:
{question}

Answer:
"""

        llm = LLMService.get_llm()

        response = llm.invoke(prompt)

        return response.content