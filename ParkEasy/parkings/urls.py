from django.urls import path
from . import views

app_name = 'parkings'

urlpatterns = [
    path('', views.index, name='index'),
]
