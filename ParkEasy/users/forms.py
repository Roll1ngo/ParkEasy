from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from users.models import UserCreate
from parkings.models import Plates


# class RegisterForm(UserCreationForm):
#     email = forms.CharField(max_length=100, required=True, widget=forms.TextInput())
#     license_plate = forms.CharField(max_length=10)
#     license_plate_image = forms.ImageField()
#
#     class Meta:
#         model = User
#         fields = ['name', 'username', 'email', 'password1', 'password2', 'license_plate', 'license_plate_image']
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         if commit:
#             user.save()
#             UserCreate.objects.create(
#                 user=user,
#                 license_plate=self.cleaned_data['license_plate'],
#                 license_plate_image=self.cleaned_data.get('license_plate_image')
#             )
#         return user


class LoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ['username', 'password']


class SearchForm(forms.Form):
    keyword = forms.CharField(label='Keyword', max_length=100)


class NewRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    name = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=20)
    plate_number = forms.CharField(max_length=10)
    license_plate_image = forms.ImageField()

    class Meta:
        model = User
        fields = ['username', 'name', 'phone_number', 'email', 'plate_number', 'license_plate_image', 'password1', 'password2']

    def clean_plate_number(self):
        plate_number = self.cleaned_data.get('plate_number')
        if Plates.objects.filter(plate_number=plate_number).exists():
            raise forms.ValidationError("This license plate is already in use.")
        return plate_number
