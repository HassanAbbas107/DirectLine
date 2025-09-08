from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Call, Message
from .forms import CallForm, MessageForm

class SignUpView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/sign-up.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("call_list")
        return super().dispatch(request, *args, **kwargs)

# Calls Views (your existing ones)
class CallCreateView(UserPassesTestMixin, CreateView):
    model = Call
    form_class = CallForm
    template_name = "Calls/call_form.html"

    def get_success_url(self):
        return reverse('call_detail', kwargs={'call_id': self.object.pk})

    def test_func(self):
        user = self.request.user
        return user.is_authenticated

class CallsListView(ListView):
    model = Call
    template_name = "Calls/call_list.html"
    context_object_name = "Call"

class CallDetailView(DetailView):
    model = Call
    template_name = "Calls/call_detail.html"
    context_object_name = "Call"
    pk_url_kwarg = 'call_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["messages"] = Message.objects.filter(call=self.object)
        return context

class CallDelete(DeleteView):
    model = Call
    template_name = "Calls/call_delete.html"
    success_url = reverse_lazy("call_list")

# Message Views (your existing ones, with minor corrections)
class MessageCreateView(CreateView):
    model = Message
    template_name = "Messages/message_form.html"
    form_class = MessageForm
    success_url = reverse_lazy("call_list")

class MessageListView(ListView):
    model = Message
    template_name = "Messages/message_list.html"
    context_object_name = 'message'

class MessageDetailView(DetailView):
    model = Message
    template_name = "Messages/message_details.html"
    context_object_name = 'message'
    pk_url_kwarg = 'message_id'

class MessageDeleteView(DeleteView):
    model = Message
    template_name = "Messages/message_confirm_delete.html"  
    success_url = reverse_lazy("call_list")

class MessageUpdateView(UpdateView):
    model = Message
    template_name = ["Messages/message_form.html"  ]
    form_class = MessageForm
    success_url = reverse_lazy("call_list")
    pk_url_kwarg = 'message_id'