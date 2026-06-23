from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from chatbot.models import ChatSession
from chatbot.serializers import ChatSessionSerializer


class ChatSessionAPIView(APIView):

    def get(self, request):

        sessions = ChatSession.objects.all().order_by('-created_at')

        serializer = ChatSessionSerializer(
            sessions,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = ChatSessionSerializer(
            data=request.data
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