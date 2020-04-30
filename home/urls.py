from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login', views.login, name="login"),
    path('chat', views.chat, name="chat"),
    path('chat/<id>', views.chat, name="chat"),
    path('send-message', views.send_messages, name='send-message'),
    path('logout', views.logout, name="logout"),

]
