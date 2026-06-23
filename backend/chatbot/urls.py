from django.urls import path

from chatbot.views import (
    ChatSessionAPIView,
    ChatMessageAPIView,
    UploadPDFAPIView,
    ChatAPIView
)

urlpatterns = [

    path(
        "sessions/",
        ChatSessionAPIView.as_view(),
        name="sessions"
    ),

    path(
        "sessions/<int:session_id>/messages/",
        ChatMessageAPIView.as_view(),
        name="messages"
    ),

    path(
        "upload/",
        UploadPDFAPIView.as_view(),
        name="upload"
    ),
    path(
        "chat/",
        ChatAPIView.as_view(),
        name="chat"
    ),
    path(
    "sessions/<int:session_id>/",
    ChatSessionAPIView.as_view()
    ),
]