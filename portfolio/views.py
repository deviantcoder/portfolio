import requests
from django.shortcuts import render, redirect, get_object_or_404
from .models import Portfolio, Message
from .forms import MessageForm
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings


def index(request):
    portfolio = Portfolio.objects.first()
    skills = portfolio.skill_set.all()

    form = MessageForm()
    if request.method == 'POST':
        send_message(request)
        

    github_url = 'https://api.github.com/users/deviantcoder/repos'

    # repos = requests.get(github_url).json()

    print(settings.EMAIL_HOST_USER)
    print(settings.EMAIL_HOST_PASSWORD)

    context = {
        'portfolio': portfolio,
        'skills': skills,
        'form': form,
    }

    return render(request, 'portfolio/portfolio.html', context)


def send_message(request):
    form = MessageForm(request.POST)
    if form.is_valid():
        message = form.save()

        send_mail(
            f'New message from: {message.name}',
            f'Name: {message.name}\nEmail: {message.email}\n{message.message}',
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],
            fail_silently=False
        )

        return redirect('/')
