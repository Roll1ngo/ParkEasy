from django.urls import path
from . import views

urlpatterns = [
    path('upload_image/', views.upload_car_image, name='upload_car_image'),
]