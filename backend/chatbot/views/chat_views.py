from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from chatbot.models import (
    ChatSession,
    ChatMessage
)

from chatbot.services.rag_service import (
    RAGService
)


class ChatAPIView(APIView):

    def post(self, request):

        session_id = request.data.get(
            "session_id"
        )

        question = request.data.get(
            "question"
        )

        if not session_id:

            return Response(
                {
                    "error": "session_id is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not question:

            return Response(
                {
                    "error": "question is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            session = ChatSession.objects.get(
                id=session_id
            )

        except ChatSession.DoesNotExist:

            return Response(
                {
                    "error": "Session not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        ChatMessage.objects.create(
            session=session,
            role="user",
            content=question
        )

        recent_messages = (
            ChatMessage.objects.filter(
                session=session
            )
            .order_by("-created_at")[:5]
        )

        history = []

        for message in reversed(recent_messages):

            history.append(
                f"{message.role}: {message.content}"
            )

        conversation_history = "\n".join(
            history
        )

        answer = RAGService.ask(
            question=question,
            collection_name=session.collection_name,
            conversation_history=conversation_history
        )

        ChatMessage.objects.create(
            session=session,
            role="assistant",
            content=answer
        )

        return Response(
            {
                "session_id": session_id,
                "question": question,
                "answer": answer
            }
        )