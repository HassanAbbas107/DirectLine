from django.urls import path, include
from . import views


urlpatterns = [
path("Calls/",views.CallsListView.as_view(),name="call_list"),
path("Calls/new/",views.CallCreateView.as_view(),name="call_create"),
path("Calls/<int:call_pk>/delete/",views.CallDelete.as_view(),name='call_delete'),
path("Calls/<int:call_id>/",views.CallDetailView.as_view(),name="call_detail"),



path("Messages/new/",views.MessageCreateView.as_view(),name="message_create"),
path("Messages/",views.MessageListView.as_view(),name="messages_list"),
path("Messages/<int:>")
]
