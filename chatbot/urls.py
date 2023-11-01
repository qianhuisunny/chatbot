from django.urls import path
from . import views

urlpatterns = [
    path("", views.chatbot, name="chatbot"),
    path("clear_chat/", views.clear_chat, name="clear_chat"),
    path(
        "get_feedbackai_demo_purpose/",
        views.get_feedbackai_demo_purpose,
        name="get_feedbackai_demo_purpose",
    ),
    path("scenariocreator/", views.scenariocreator, name="scenariocreator"),
    # path("login", views.login, name="login"),
    # path("register", views.register, name="register"),
    # path("logout", views.logout, name="logout"),
]
