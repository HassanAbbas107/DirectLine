from django.urls import path, include
from . import views


urlpatterns = [
path("Calls/",views.CallsListView.as_view(),name="call_list"),
path("Calls/new/",views.CallCreateView.as_view(),name="call_create"),
path("Calls/<int:pk>/delete/",views.CallDelete.as_view(),name='call_delete'),
path("Calls/<int:call_id>/",views.CallDetailView.as_view(),name="call_detail"),


# Messages url  
path("Messages/new/",views.MessageCreateView.as_view(),name="message_create"),
path("Messages/",views.MessageListView.as_view(),name="messages_list"),
path("Messages/<int:message_id>/",views.MessageDetailView.as_view(),name="message_details"),
path("Messages/<int:message_id>/update/",views.MessageUpdateView.as_view(),name="message_create"),
path("Messages/<int:pk>/delete/",views.MessageDeleteView.as_view(),name="message_delete"),
path("auth/signup",views.SignUpView.as_view(), name="signup"),

]
