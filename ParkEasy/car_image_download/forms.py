
# forms.py
from django import forms
from .models import ImageUploadCar

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUploadCar
        fields = ['image']