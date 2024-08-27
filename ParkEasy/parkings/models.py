from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(blank=True, null=True, max_length=20)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    parking_limit = models.IntegerField(default=0)
    last_limit_notification_sent = models.CharField(max_length=6, null=True, blank=True)

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


class History(models.Model):
    plate = models.ForeignKey(Plates, on_delete=models.CASCADE, related_name='parkings_history')
    parking_start = models.DateTimeField(auto_now_add=True)
    parking_end = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    duration = models.IntegerField(null=True, blank=True)

    def __str__(self):
        plate_number = self.plate.plate_number if self.plate else 'Unknown'
        return f"Parking {self.id} for plate {plate_number}, Started at {self.parking_start}, Ended at {self.parking_end if self.parking_end else 'Ongoing'}, Completed: {'Yes' if self.is_completed else 'No'}, Duration: {self.duration} hour"
