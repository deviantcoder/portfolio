import requests
from .models import Portfolio, Message, Project, Skill
from .forms import MessageForm, PortfolioForm, SkillForm
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, Http404
from django.utils import timezone


def index(request):
    portfolio = Portfolio.objects.first()
    skills = Skill.objects.all()

    form = MessageForm()
    if request.method == 'POST':
        send_message(request)
        return redirect('/')

    visible_github_repos = get_github_repos().filter(visible=True)
    invisible_github_repos = get_github_repos().filter(visible=False)

    context = {
        'portfolio': portfolio,
        'skills': skills,
        'form': form,
        'visible_github_repos': visible_github_repos,
        'invisible_github_repos': invisible_github_repos,
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
    if Project.objects.exists() and time_delta():
        url = settings.GITHUB_URL
        headers = {
            'Authorization': f'token {settings.GITHUB_TOKEN}'
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            github_repos = response.json()
        except requests.RequestException as e:
            print(f'Error fetching GitHub repos: {e}')
            return Project.objects.none()

        for repo in github_repos:
            project, status = Project.objects.get_or_create(
                name=repo['name'],
                defaults={
                    'url': repo['svn_url'],
                    'description': repo['description'],
                }
            )

    return Project.objects.all()


def time_delta():
    project = Project.objects.last()
    delta = timezone.now() - project.created

    return delta >= timezone.timedelta(days=1)
    

def logout_user(request):
    logout(request)
    return redirect('/')


@login_required(login_url='/')
def edit_portfolio(request):
    page_title = 'Edit portfolio info'
    portfolio = Portfolio.objects.first()
    form = PortfolioForm(instance=portfolio)

    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES, instance=portfolio)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'form': form,
        'page_title': page_title,
    }

    return render(request, 'portfolio/object_form.html', context)


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


@login_required(login_url='/')
def hide_unhide_project(request, pk):
    project = get_object_or_404(Project, id=pk)
    
    if project.visible:
        project.visible = False
    else:    
        project.visible = True
    project.save()

    return redirect('/')


@login_required(login_url='/')
def add_skill(request):
    page_title = 'Add Skill'
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save()
            messages.success(request, f'Skill was added: {skill.name}')
            return redirect('/')

    context = {
        'page_title': page_title,
        'form': form,
    }

    return render(request, 'portfolio/object_form.html', context)


@login_required(login_url='/')
def edit_skill(request, pk):
    skill = get_object_or_404(Skill, id=pk)
    page_title = f'Edit Skill: {skill.name}'
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.info(request, 'Skill was saved')
            return redirect('/')
    
    context = {
        'page_title': page_title,
        'form': form,
    }

    return render(request, 'portfolio/object_form.html', context)


@login_required(login_url='/')
def delete_skill(request, pk):
    skill = get_object_or_404(Skill, id=pk)
    skill_name = skill.name
    skill.delete()
    messages.info(request, f'Skill was deleted: {skill_name}')
    return redirect('/')
    