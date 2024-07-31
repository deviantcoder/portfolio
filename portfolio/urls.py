from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout_user, name='logout'),
    path('edit-portfolio/', views.edit_portfolio, name='edit_portfolio'),
    path('login-admin/', views.login_admin, name='login_admin'),
    path('download-resume/', views.download_resume, name='download_resume'),
    path('hide-project/<str:pk>/', views.hide_project, name='hide_project'),
]