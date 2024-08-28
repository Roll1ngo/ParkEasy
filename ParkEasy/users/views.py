from django.shortcuts import get_object_or_404
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
from django.core.paginator import Paginator
from admin_panel.forms import UserProfileForm, PlateFormSet, PlatesFormUser, PlateFormSetUser
from parkings.models import Plates, UserProfile, Rates, History
import pandas as pd
from io import BytesIO
from openpyxl import load_workbook
from django.http import HttpResponse



def profile(request):
    current_rate = Rates.objects.last()
    return render(request, 'users/profile.html', {'current_rate': current_rate.rate})


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
                email=form.cleaned_data['email'],
                parking_limit=0,
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


def parking_history(request):
    # Перевірте, чи є поточний користувач автентифікованим
    if not request.user.is_authenticated:
        return redirect('login')  # Змініть на реальний маршрут для логіну

    # Отримання профілю користувача
    user_profile = get_object_or_404(UserProfile, user=request.user)

    # Отримання історії паркування для поточного користувача
    parking_history = History.objects.filter(
        plate__user=user_profile
    ).select_related('plate__user').all()

    current_rate = Rates.objects.last().rate

    # Додаємо розрахунок вартості
    for parking in parking_history:
        if parking.parking_end:
            parking.rate = current_rate
            parking.cost = parking.duration * current_rate
        else:
            parking.rate = None
            parking.cost = None

    # Пагінація
    paginator = Paginator(parking_history, 50)  # 50 записів на сторінку
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'users/parking_history.html', {'page_obj': page_obj})



def generate_user_parking_report(request):
    user_id = request.user.id
    user = get_object_or_404(UserProfile, user_id=user_id)

    parking_history = History.objects.filter(plate__user=user).select_related('plate__user')
    current_rate = Rates.objects.last().rate if Rates.objects.last() else 0

    data = []
    for parking in parking_history:
        parking_start = parking.parking_start.replace(tzinfo=None)
        parking_end = parking.parking_end.replace(tzinfo=None) if parking.parking_end else None
        parking_completed = 'Yes' if parking.is_completed else 'No'

        if parking.parking_end and parking.duration:
            parking.cost = parking.duration * current_rate
        else:
            parking.cost = None

        data.append({
            'Parking ID': parking.id,
            'User Name': user.name,
            'Plate Number': parking.plate.plate_number,
            'Parking Start': parking_start,
            'Parking End': parking_end,
            'Completed': parking_completed,
            'Duration (hours)': parking.duration,
            'Cost (UAH)': parking.cost
        })

    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='User Parking History')

    output.seek(0)
    output = autosize_columns(output)

    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=user_{user_id}_parking_report.xlsx'

    return response

def autosize_columns(file_in_memory):
    wb = load_workbook(file_in_memory)
    ws = wb.active

    for col in ws.columns:
        max_length = max(len(str(cell.value)) for cell in col)
        ws.column_dimensions[col[0].column_letter].width = max_length + 2

    updated_memory_file = BytesIO()
    wb.save(updated_memory_file)
    updated_memory_file.seek(0)

    return updated_memory_file
