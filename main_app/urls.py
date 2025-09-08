from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    # Calls
    path("calls/", views.CallsListView.as_view(), name="call_list"),
    path("calls/new/", views.CallCreateView.as_view(), name="call_create"),
    path("calls/<int:pk>/delete/", views.CallDelete.as_view(), name="call_delete"),
    path("calls/<int:call_id>/", views.CallDetailView.as_view(), name="call_detail"),

    # Messages
    path("messages/new/", views.MessageCreateView.as_view(), name="message_create"),
    path("messages/", views.MessageListView.as_view(), name="messages_list"),
    path("messages/<int:message_id>/update/", views.MessageUpdateView.as_view(), name="message_update"),
    path("messages/<int:pk>/delete/", views.MessageDeleteView.as_view(), name="message_delete"),

    # Auth
    path("auth/signup/", views.SignUpView.as_view(), name="signup"),
    path("auth/login/", LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("auth/logout/", LogoutView.as_view(next_page="login"), name="logout"),
]