from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.home, name='home'),
    path('users/', views.users, name='users'),
    path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('rate/', views.rate, name='rate'),
]
