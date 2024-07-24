from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input', 'placeholder': 'Ex. Jane Smith', 'type': 'text', 'name': 'Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'input', 'placeholder': 'Ex. janesmith@email.com', 'type': 'email', 'name': 'Email'
            }),
            'message': forms.Textarea(attrs={
                'class': 'textarea', 'placeholder': 'Your message', 'name': 'Message'
            }),
        }