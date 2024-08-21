from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from users.models import UserCreate


class RegisterForm(UserCreationForm):
    email = forms.CharField(max_length=100, required=True, widget=forms.TextInput())
    license_plate = forms.CharField(max_length=10)
    license_plate_image = forms.ImageField()
   
    class Meta:
        model = User
        fields = ['username', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            UserCreate.objects.create(
                user=user,
                license_plate=self.cleaned_data['license_plate'],
                license_plate_image=self.cleaned_data['license_plate_image']
            )
        return user

class LoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ['username', 'password']

class SearchForm(forms.Form):
    keyword = forms.CharField(label='Keyword', max_length=100)  