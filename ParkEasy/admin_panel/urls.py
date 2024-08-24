from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.home, name='home'),
    path('users/', views.users, name='users'),
    path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('rate/', views.rate, name='rate'),
    path('parking_history/', views.parking_history, name='parking_history'),
    path('reports/', views.reports, name='reports'),
    path('reports/parking-report/', views.generate_parking_report, name='download_parking_report'),
]
