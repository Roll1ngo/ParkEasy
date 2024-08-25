from django.db import models

class ImageUploadCar(models.Model):
    image = models.ImageField(upload_to='uploads/temp')

    def __str__(self):
        return self.image.name

class CarNumberPlate(models.Model):
    image = models.ImageField(upload_to='uploads/temp')
    number_plate_text = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.number_plate_text