from django.urls import path
from . import views

urlpatterns = [
    path('upload_image_start/', views.upload_car_image_and_start, name='upload_image_start'),
    path('upload_image_finish/', views.upload_car_image_and_finish, name='upload_image_finish'),
]