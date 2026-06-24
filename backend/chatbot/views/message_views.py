from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from chatbot.models import (
    ChatSession,
    ChatMessage
)

from chatbot.serializers import (
    ChatMessageSerializer
)


class ChatMessageAPIView(APIView):

    def get(
        self,
        request,
        session_id
    ):

        messages = ChatMessage.objects.filter(
            session_id=session_id
        ).order_by(
            "created_at"
        )

        serializer = ChatMessageSerializer(
            messages,
            many=True
        )

        return Response(
            serializer.data
        )

    def post(
        self,
        request,
        session_id
    ):

        data = request.data.copy()

        data["session"] = session_id

        serializer = ChatMessageSerializer(
            data=data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def put(
        self,
        request,
        session_id,
        message_id
    ):

        try:

            message = ChatMessage.objects.get(
                id=message_id,
                session_id=session_id
            )

        except ChatMessage.DoesNotExist:

            return Response(
                {
                    "error":
                    "Message not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ChatMessageSerializer(
            message,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(
        self,
        request,
        session_id,
        message_id
    ):

        try:

            message = ChatMessage.objects.get(
                id=message_id,
                session_id=session_id
            )

        except ChatMessage.DoesNotExist:

            return Response(
                {
                    "error":
                    "Message not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if message.role == "user":

            next_message = (
                ChatMessage.objects.filter(
                    session_id=session_id,
                    created_at__gt=
                    message.created_at
                )
                .order_by(
                    "created_at"
                )
                .first()
            )

            if (
                next_message
                and
                next_message.role
                == "assistant"
            ):

                next_message.delete()

        message.delete()

        return Response(
            {
                "message":
                "Message deleted successfully"
            }
        )