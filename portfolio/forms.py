from django import forms
from .models import Message, Portfolio, Skill, Socials


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


class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input', 'placeholder': 'Name', 'name': 'name'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'textarea', 'placeholder': 'Bio', 'name': 'Bio'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'input', 'placeholder': 'Email', 'type': 'email', 'name': 'Email'
            }),
            'github': forms.TextInput(attrs={
                'class': 'input', 'placeholder': 'GitHub Link', 'name': 'github'
            }),
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input', 'placeholder': 'Title'
            }),
            'progress': forms.NumberInput(attrs={
                'class': 'input', 'placeholder': 'Progress'
            }),
        }


class SocialsForm(forms.ModelForm):
    class Meta:
        model = Socials
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input', 'placeholder': 'Name'
            }),
            'url': forms.TextInput(attrs={
                'class': 'input', 'placeholder': 'URL'
            }),
        }
