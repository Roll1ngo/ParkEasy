import requests
from django import forms
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.views import View
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from .forms import NewRegisterForm
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from admin_panel.forms import UserProfileForm, PlateFormSet, PlatesFormUser, PlateFormSetUser
from parkings.models import Plates, UserProfile


def profile(request):
    return render(request, 'users/profile.html')


# class RegisterView(View):
#     template_name = 'users/register.html'
#     form_class = RegisterForm
#
#     def dispatch(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return redirect(to='/')
#         return super().dispatch(request, *args, **kwargs)
#
#     def get(self, request):
#         return render(request, self.template_name, context={'form': self.form_class})
#
#     def post(self, request):
#         form = self.form_class(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data['username']
#             messages.success(request, f'Greetings {username}, your account has been successfully registered')
#             return redirect(to='users:login')
#         return render(request, self.template_name, context={'form': form})


class RegisterView(View):
    template_name = 'users/register.html'
    form_class = NewRegisterForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to='/')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, context={'form': self.form_class})

    def post(self, request):
        print(request.POST)
        form = self.form_class(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            # Створення користувача
            user = form.save()

            # Створення UserProfile
            user_profile = UserProfile.objects.create(
                user=user,
                name=form.cleaned_data['name'],
                phone_number=form.cleaned_data['phone_number'],
                email=form.cleaned_data['email']
            )

            # Створення Plates
            plate = Plates.objects.create(
                user=user_profile,
                plate_number=form.cleaned_data['plate_number'],
                is_banned=False  # за замовчуванням не забанений
            )



            username = form.cleaned_data['username']
            messages.success(request, f'Greetings {username}, your account has been successfully registered')
            return redirect(to='users:login')
        return render(request, self.template_name, context={'form': form})


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    error_messages = {
        'invalid_login': "Invalid username or password. Please try again.",
        'inactive': "This account is inactive.",
    }

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(self.error_messages['invalid_login'], code='invalid_login')
            elif not self.user_cache.is_active:
                raise forms.ValidationError(self.error_messages['inactive'], code='inactive')

        return self.cleaned_data, redirect('/accounts/profile/')
        

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('/accounts/profile/')


def change_password(request):
    template_name = 'users/change_password.html'
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been successfully changed!')
            return redirect('/accounts/profile/')
        else:
            messages.error(request, 'The old or new password is not valid.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, template_name, {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')


class CustomPasswordResetView(PasswordResetView):
    template_name = 'users/reset_password.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    success_url = 'reset_password_sent'


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'


def index(request):
    return render(request, 'users/index.html')


def edit_user(request):
    user = request.user.userprofile

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=user)
        plates_formset = PlateFormSetUser(request.POST, instance=user)

        if profile_form.is_valid() and plates_formset.is_valid():
            profile_form.save()

            # Зберігаємо або видаляємо форми
            for form in plates_formset:
                if form.cleaned_data and form.cleaned_data.get('DELETE', False):
                    if form.instance.pk:
                        form.instance.delete()
                elif form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    form.save()

            return redirect('users:profile')  # Перенаправлення після успішного збереження
    else:
        profile_form = UserProfileForm(instance=user)
        plates_formset = PlateFormSetUser(instance=user)

    return render(request, 'users/edit_user.html', {
        'profile_form': profile_form,
        'plates_formset': plates_formset
    })