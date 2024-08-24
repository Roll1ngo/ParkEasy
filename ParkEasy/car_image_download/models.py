from django.db import models

class ImageUploadCar(models.Model):
    image = models.ImageField(upload_to='uploads/temp')

