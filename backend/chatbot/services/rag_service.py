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

        if not collection_name:

            return (
                "No documents have been uploaded "
                "for this chat session."
            )

        try:

            retrieved_docs = (
                VectorStoreService.retrieve_documents(
                    query=question,
                    collection_name=collection_name,
                    k=3
                )
            )

        except Exception:

            return (
                "No documents have been uploaded "
                "for this chat session."
            )

        if not retrieved_docs:

            return (
                "I could not find this information "
                "in the uploaded documents."
            )

        context = "\n\n".join(
            [
                doc.page_content
                for doc in retrieved_docs
            ]
        )

        prompt = f"""
You are a document assistant.

Use ONLY the provided context.

If the answer is not present in the context,
reply exactly:

I could not find this information in the uploaded documents.

Conversation History:
{conversation_history}

Context:
{context}

Question:
{question}

Answer:
"""

        llm = LLMService.get_llm()

        response = llm.invoke(prompt)

        return response.content