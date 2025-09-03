from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from .models import Call, Message
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.
class CallsListView(LoginRequiredMixin,ListView):
    model=Call
    LoginRequiredMixin = "Calls/Call_list.html"
    context_object_name = "Call"    
    def get_queryset(self):
        return super().get_queryset()