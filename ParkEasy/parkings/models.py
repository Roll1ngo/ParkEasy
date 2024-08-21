from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(blank=True, null=True, max_length=20)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"Username: {self.user}, Phone: {self.phone_number}, Email: {self.email}"


class Plates(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='plates')
    plate_number = models.CharField(max_length=20)
    is_banned = models.BooleanField(default=False)

    def __str__(self):
        return self.plate_number


class Rates(models.Model):
    rate = models.IntegerField()