from django import forms
from django.core.validators import FileExtensionValidator

from .models import ImageUpload


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*'})
        }
        validators = [
            FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])
        ]