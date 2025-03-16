from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('get-messages/', views.get_messages, name='get_messages'),
    path('start-session/', views.start_session, name='start_session'),
    path('end-session/', views.end_session, name='end_session'),
    path('clear/', views.clear_chat, name='clear_chat'),
] 