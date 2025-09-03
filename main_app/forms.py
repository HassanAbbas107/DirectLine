from django import forms
from .models import Call, Message

class CallForm(forms.ModelForm):
    class Meta:
        model = Call
        fields = [ "building","lab","description"]
        


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = [ "description"]
