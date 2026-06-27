from rest_framework import serializers

from .models import (
    ChatSession,
    ChatMessage,
    UploadedDocument
)


class UploadedDocumentSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = UploadedDocument

        fields = "__all__"


class ChatSessionSerializer(
    serializers.ModelSerializer
):

    documents = UploadedDocumentSerializer(
        many=True,
        read_only=True
    )

    class Meta:

        model = ChatSession

        fields = "__all__"


class ChatMessageSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = ChatMessage

        fields = "__all__"