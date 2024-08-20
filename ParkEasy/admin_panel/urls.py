from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.home, name='home'),
    path('users/', views.users, name='users'),
]
