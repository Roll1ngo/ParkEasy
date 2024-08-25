from django.db import models
from django.contrib.auth.models import User  # Імпортуємо модель користувача

class ImageUploadCar(models.Model):
    image = models.ImageField(upload_to='uploads/temp')

class CarNumberPlate(models.Model):
    number_plate_text = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Тимчасово дозволяємо null

    def __str__(self):
        return self.number_plate_text
