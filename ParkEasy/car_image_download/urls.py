from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_car_image, name='car_image_upload'),
]
