import requests
from .models import Portfolio, Message, Project, Skill
from .forms import MessageForm, PortfolioForm
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, Http404


def index(request):
    portfolio = Portfolio.objects.first()
    skills = Skill.objects.all()

    form = MessageForm()
    if request.method == 'POST':
        send_message(request)
        return redirect('/')

    github_repos = get_github_repos()

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

        messages.success(request, 'Message was sent')


def get_github_repos():
    url = settings.GITHUB_URL

    try:
        response = requests.get(url)
        response.raise_for_status()
        github_repos = response.json()

    except requests.RequestException as e:
        print(f'Error fetching GitHub repos: {e}')
        return []

    for repo in github_repos:
        project, status = Project.objects.get_or_create(
            name=repo['name'],
            defaults={
                'url': repo['svn_url'],
                'description': repo['description'],
            }
        )

    repos = Project.objects.filter(visible=True)

    return repos
    

def logout_user(request):
    logout(request)
    return redirect('/')


@login_required(login_url='/')
def edit_portfolio(request):
    portfolio = Portfolio.objects.first()
    form = PortfolioForm(instance=portfolio)

    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES, instance=portfolio)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'form': form,
    }

    return render(request, 'portfolio/portfolio_form.html', context)


def login_admin(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.warning(request, 'User does not exist')
            return redirect('login_admin')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Welcome back!')
            return redirect('/')
        messages.warning(request, 'Username or password is incorrect')
        return redirect('login_admin')

    return render(request, 'portfolio/login.html')


def download_resume(request):
    portfolio = Portfolio.objects.first()

    if not portfolio or not portfolio.resume:
        raise Http404('Resume is not available at the moment :(')
    
    file_name = portfolio.resume

    response = FileResponse(portfolio.resume.open('rb'))
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    
    return response


def hide_project(request, pk):
    project = get_object_or_404(Project, id=pk)
    
    project.visible = False
    project.save()

    return redirect('/')
    