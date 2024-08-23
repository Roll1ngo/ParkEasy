from django.db import models


class ImageUpload(models.Model):
    image = models.ImageField(upload_to='uploads/', max_length=1024*1024*5)
