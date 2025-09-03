from django.urls import path, include
from . import views


urlpatterns = [
path("Calls",views.CallsListView.as_view(),name="call_list")

]
