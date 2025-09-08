from django import forms
from .models import Call, Message
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
class CallForm(forms.ModelForm):
    class Meta:
        model = Call
        fields = [ "building","lab","description"]
        

User = get_user_model()
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = [ "description"]
