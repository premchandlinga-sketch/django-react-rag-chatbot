from django.urls import path

from chatbot.views import (
    ChatSessionAPIView,
    ChatMessageAPIView
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
]