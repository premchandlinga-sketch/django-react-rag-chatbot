from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from chatbot.models import ChatSession, ChatMessage
from chatbot.serializers import ChatMessageSerializer


class ChatMessageAPIView(APIView):

    def get(self, request, session_id):

        messages = ChatMessage.objects.filter(
            session_id=session_id
        ).order_by("created_at")

        serializer = ChatMessageSerializer(
            messages,
            many=True
        )

        return Response(serializer.data)

    def post(self, request, session_id):

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