from django import forms
from .models import Call, Message
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
class CallForm(forms.ModelForm):
    class Meta:
        model = Call
        fields = ["building", "lab", "description"]
        widgets = {
            'building': forms.TextInput(attrs={'placeholder': 'e.g. Building 5', 'class': 'form-input'}),
            'lab': forms.TextInput(attrs={'placeholder': 'e.g. Lab 4B', 'class': 'form-input'}),
            'description': forms.Textarea(attrs={'placeholder': 'Please detail the technical issue or support request...', 'class': 'form-textarea', 'rows': 4}),
        }

User = get_user_model()
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("role",) # Optionally let them select a role or just keep default

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["description"]
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Type your comment or update here...', 'class': 'form-textarea', 'rows': 3}),
        }

