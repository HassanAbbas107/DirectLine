from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import connection
from .models import Call, Message
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from .forms import CallForm, MessageForm, CustomUserCreationForm

User = get_user_model()

class SignUpView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = 'registration/sign-up.html'

# Calls Views
class CallCreateView(LoginRequiredMixin, CreateView):
    model = Call
    form_class = CallForm
    template_name = "Calls/call_form.html"
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('call_detail', kwargs={'call_id': self.object.pk})

class CallsListView(LoginRequiredMixin, ListView):
    model = Call
    template_name = "Calls/call_list.html"
    context_object_name = "Call"    
    
    def get_queryset(self):
        user = self.request.user
        if user.role == user.Role.ADMIN:
            return Call.objects.all().order_by('-id')
        return Call.objects.filter(user=user).order_by('-id')

class CallDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Call
    template_name = "Calls/call_detail.html"
    context_object_name = "Call"
    pk_url_kwarg = 'call_id'
    
    def test_func(self):
        call = self.get_object()
        user = self.request.user
        return user.role == user.Role.ADMIN or call.user == user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["messages"] = Message.objects.filter(call=self.object).order_by('id')
        return context

class CallDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Call 
    template_name = "Calls/call_delete.html"    
    success_url = reverse_lazy("call_list")
    
    def test_func(self):
        call = self.get_object()
        user = self.request.user
        return user.role == user.Role.ADMIN or call.user == user

# Messages Views
class MessageCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Message
    template_name = "Messages/message-form.html"  # Map to existing message-form.html
    form_class = MessageForm
    
    def test_func(self):
        call = Call.objects.get(pk=self.kwargs['pk'])
        user = self.request.user
        return user.role == user.Role.ADMIN or call.user == user
        
    def form_valid(self, form):
        call = Call.objects.get(pk=self.kwargs['pk'])
        form.instance.call = call
        form.instance.user = self.request.user
        
        # If user is admin and updates status, apply changes to Call status
        if self.request.user.role == self.request.user.Role.ADMIN:
            status = self.request.POST.get('status')
            if status in Call.Status.values:
                call.status = status
                call.save()
                
        return super().form_valid(form)
        
    def get_success_url(self):
        return reverse('call_detail', kwargs={'call_id': self.kwargs['pk']})

class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "Messages/message_list.html"
    context_object_name = 'messages'  # Changed from 'message' to match template looping
    
    def get_queryset(self):
        user = self.request.user
        if user.role == user.Role.ADMIN:
            return Message.objects.all().order_by('-id')
        return Message.objects.filter(call__user=user).order_by('-id')

class MessageDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Message
    template_name = "Messages/message_details.html"
    context_object_name = 'message'
    pk_url_kwarg = 'message_id'
    
    def test_func(self):
        message = self.get_object()
        user = self.request.user
        return user.role == user.Role.ADMIN or message.call.user == user

class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message
    template_name = "Messages/message_delete.html"
    
    def test_func(self):
        message = self.get_object()
        user = self.request.user
        return user.role == user.Role.ADMIN or message.user == user
        
    def get_success_url(self):
        return reverse('call_detail', kwargs={'call_id': self.object.call.id})

class MessageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Message
    template_name = 'Messages/message-form.html'
    form_class = MessageForm
    pk_url_kwarg = 'message_id'
    
    def test_func(self):
        message = self.get_object()
        user = self.request.user
        return user.role == user.Role.ADMIN or message.user == user
        
    def get_success_url(self):
        return reverse('call_detail', kwargs={'call_id': self.object.call.id})

@require_http_methods(["GET"])
def healthcheck(request):
    """Healthcheck endpoint for monitoring. Returns 200 if DB is connected."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return JsonResponse({
            "status": "healthy",
            "service": "directline-api",
            "database": "connected"
        })
    except Exception as e:
        return JsonResponse({
            "status": "unhealthy",
            "service": "directline-api",
            "error": str(e)
        }, status=503)
