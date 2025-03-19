from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path("api/", views.chatbot_api, name="chatbot_api"),
    path("clear/", views.clear_chat, name="clear_chat")
]
