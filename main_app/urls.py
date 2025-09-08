from django.urls import path, include
from . import views


urlpatterns = [
path("calls/",views.CallsListView.as_view(),name="call_list"),
path("calls/new/",views.CallCreateView.as_view(),name="call_create"),
path("calls/<int:pk>/delete/",views.CallDelete.as_view(),name='call_delete'),
path("calls/<int:call_id>/",views.CallDetailView.as_view(),name="call_detail"),


# Messages url  
path("messages/new/",views.MessageCreateView.as_view(),name="message_create"),
path("messages/",views.MessageListView.as_view(),name="messages_list"),
path("messages/<int:message_id>/",views.MessageDetailView.as_view(),name="message_details"),
path("messages/<int:message_id>/update/",views.MessageUpdateView.as_view(),name="message_create"),
path("messages/<int:pk>/delete/",views.MessageDeleteView.as_view(),name="message_delete"),
path("auth/signup",views.SignUpView.as_view(), name="signup"),
 
]
