from chatbot.services.vector_store_service import (
    VectorStoreService
)

from chatbot.services.llm_service import (
    LLMService
)

from chatbot.models import (
    UploadedDocument
)


class RAGService:

    @staticmethod
    def ask(
        question,
        collection_name,
        conversation_history=""
    ):

        if not collection_name:

            return {
                "answer": (
                    "No documents have been uploaded "
                    "for this chat session."
                ),
                "sources": []
            }

        question_lower = question.lower()

        # -------------------------------------------------
        # FILE LISTING INTENT
        # -------------------------------------------------

        file_keywords = [
            "file",
            "files",
            "document",
            "documents",
            "pdf",
            "pdfs",
            "uploaded",
            "upload"
        ]

        file_query_words = [
            "which",
            "what",
            "list",
            "show",
            "tell"
        ]

        if (
            any(
                keyword in question_lower
                for keyword in file_keywords
            )
            and
            any(
                word in question_lower
                for word in file_query_words
            )
        ):

            uploaded_files = (
                UploadedDocument.objects.filter(
                    session__collection_name=
                    collection_name
                )
            )

            if not uploaded_files.exists():

                return {
                    "answer":
                    "No files have been uploaded in this session.",
                    "sources": []
                }

            answer = (
                "The following files are uploaded "
                "in this session:\n\n"
            )

            for index, file in enumerate(
                uploaded_files,
                start=1
            ):

                answer += (
                    f"{index}. {file.file_name}\n"
                )

            return {
                "answer": answer,
                "sources": []
            }

        # -------------------------------------------------
        # SUMMARY INTENT
        # -------------------------------------------------

        summary_keywords = [
            "summary",
            "summarize",
            "overview",
            "topics",
            "topic",
            "document",
            "pdf",
            "chapters",
            "chapter",
            "contents",
            "about this document",
            "what is this document about",
            "give overview",
            "list topics",
            "main topics"
        ]

        k = 3

        if any(
            keyword in question_lower
            for keyword in summary_keywords
        ):

            k = 25

        try:

            retrieved_docs = (
                VectorStoreService.retrieve_documents(
                    query=question,
                    collection_name=collection_name,
                    k=k
                )
            )

        except Exception as e:

            print(e)

            return {
                "answer": (
                    "No documents have been uploaded "
                    "for this chat session."
                ),
                "sources": []
            }

        if not retrieved_docs:

            return {
                "answer": (
                    "I could not find this information "
                    "in the uploaded documents."
                ),
                "sources": []
            }

        context = "\n\n".join(
            [
                doc.page_content
                for doc in retrieved_docs
            ]
        )

        prompt = f"""
You are an intelligent Enterprise RAG Assistant.

You MUST answer ONLY using the supplied context.

Instructions:

1. If the user asks for a summary,
   generate a well-structured summary.

2. If the user asks for topics,
   list the important topics as bullet points.

3. If the user asks what the document is about,
   explain the overall purpose.

4. If the user asks a factual question,
   answer accurately from the context.

5. Never hallucinate.

6. If the answer is unavailable,
reply EXACTLY:

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

        response = llm.invoke(
            prompt
        )

        sources = []

        for doc in retrieved_docs:

            metadata = doc.metadata

            file_name = (
                metadata.get(
                    "source",
                    ""
                )
                .split("\\")[-1]
                .split("/")[-1]
            )

            page = (
                metadata.get(
                    "page",
                    0
                ) + 1
            )

            source = {
                "file": file_name,
                "page": page
            }

            if source not in sources:

                sources.append(
                    source
                )

        answer = response.content.strip()

        # ------------------------------------------
        # Add uploaded files to the response when
        # user asks about files/documents
        # ------------------------------------------

        if (
            any(
                keyword in question_lower
                for keyword in [
                    "file",
                    "files",
                    "document",
                    "documents",
                    "pdf",
                    "pdfs"
                ]
            )
            and
            any(
                keyword in question_lower
                for keyword in [
                    "which",
                    "what",
                    "show",
                    "list",
                    "tell"
                ]
            )
        ):

            uploaded_files = UploadedDocument.objects.filter(
                session__collection_name=collection_name
            )

            if uploaded_files.exists():

                file_list = "\n".join(
                    [
                        f"• {file.file_name}"
                        for file in uploaded_files
                    ]
                )

                answer = (
                    "The following files are uploaded "
                    "in this session:\n\n"
                    f"{file_list}"
                )

        return {
            "answer": answer,
            "sources": sources
        }
        