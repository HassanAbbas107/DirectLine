from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from .models import Call, Message
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import requests
from .forms import CallForm,MessageForm
from django.contrib.auth import logout


class SignUpView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = 'registration/sign-up.html'
    

#Calls Views
class CallCreateView(CreateView):
    model=Call
    form_class=CallForm
    template_name = "Calls/call_form.html"
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    
    
    def get_success_url(self):
        return reverse('call_detail',kwargs={'call_id':self.object.pk})
    
    
class CallsListView(ListView):
    model=Call
    template_name = "Calls/call_list.html"
    context_object_name = "Call"    
    def get_queryset(self):
        return super().get_queryset()

class CallDetailView(DetailView):
    model = Call
    template_name = "Calls/call_detail.html"
    context_object_name = "Call"
    pk_url_kwarg = 'call_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["messages"] = Message.objects.filter(call= self.object)
        return context
    
    
class CallDelete(DeleteView):
    model = Call 
    template_name= "Calls/call_delete.html"    
    success_url = reverse_lazy("call_list")
    
    


class MessageCreateView(CreateView):
    
    model = Message
    template_name="Messages/message_form.html"
    form_class=MessageForm
    success_url = reverse_lazy("call_list")
    
    def form_valid(self, form):
        call = Call.objects.get(pk=self.kwargs['pk'])
        form.instance.call = call
        form.instance.user = self.request.user
        
        return super().form_valid(form)
    


class MessageListView(ListView):
    model=Message
    template_name="Messages/message_list.html"
    context_object_name='message'
    
class MessageDetailView(DetailView):
    model = Message
    template_name="Messages/message_details.html"
    context_object_name='message'
    pk_url_kwarg = 'message_id'
    
    
class MessageDeleteView(DeleteView):
    model=Message
    template_name = "Messages/message_delete.html"
    success_url = reverse_lazy("call_list")


class MessageUpdateView(UpdateView):
    model = Message
    template_name='Messages/message-form.html'
    form_class = MessageForm
    success_url=reverse_lazy("call_list")
    pk_url_kwarg = 'message_id'
    
    
