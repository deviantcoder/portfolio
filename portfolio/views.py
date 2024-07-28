import requests
from django.shortcuts import render, redirect, get_object_or_404
from .models import Portfolio, Message, Project
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

    github_repos = get_github_repos()
    print()

    context = {
        'portfolio': portfolio,
        'skills': skills,
        'form': form,
        'github_repos': github_repos,
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


def get_github_repos():
    url = 'https://api.github.com/users/deviantcoder/repos'

    try:
        response = requests.get(url)
        response.raise_for_status()
        github_repos = response.json()

    except requests.RequestException as e:
        print(f'Error fetching GitHub repos: {e}')
        return []

    repos = []

    for repo in github_repos:
        project, status = Project.objects.get_or_create(
            name=repo['name'],
            defaults={
                'url': repo['url'],
                'description': repo['description'],
            }
        )

        existing_project = {
            'name': project.name,
            'url': project.url,
            'description': project.description,
        }

        repos.append(existing_project)

    return repos
    
