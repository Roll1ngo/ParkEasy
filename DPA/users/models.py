from django.contrib.auth.models import User
from django.db import models

class UserCreate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    license_plate = models.CharField(max_length=10, unique=True)
    license_plate_image = models.ImageField(upload_to='license_plates/')
    car_model = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.license_plate}'
