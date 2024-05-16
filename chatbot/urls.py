from django.urls import path
from . import views

urlpatterns = [
    path("chatbot", views.chatbot, name="chatbot"),
    path(
        "get_feedbackai_demo_purpose/",
        views.get_feedbackai_demo_purpose,
        name="get_feedbackai_demo_purpose",
    ),
    path("scenariocreator/", views.scenariocreator, name="scenariocreator"),
    path("get_feedbackai/", views.get_feedbackai, name="getfeedbackai"),
    path("", views.simulationlab, name="simulationlab"),
    # path("logout", views.logout, name="logout"),
]
