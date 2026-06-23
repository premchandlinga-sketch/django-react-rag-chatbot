from django.contrib import admin
from .models import (ChatSession,ChatMessage,Document,Reminder)

admin.site.register(ChatSession)
admin.site.register(ChatMessage)
admin.site.register(Document)
admin.site.register(Reminder)