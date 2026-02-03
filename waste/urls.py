from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='waste/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('submit/', views.submit_waste, name='submit_waste'),
    path('history/', views.history, name='history'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]
