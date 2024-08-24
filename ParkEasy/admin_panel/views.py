from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.utils.timezone import make_naive
from django.utils import timezone
from .forms import UserProfileForm, PlateFormSet, RateForm
from parkings.models import UserProfile, Plates, Rates, History
import pandas as pd
from math import ceil
from datetime import datetime, timedelta
from openpyxl import load_workbook
from io import BytesIO


def is_superuser(user):
    return user.is_superuser


def superuser_required(function=None, redirect_field_name=None, login_url=None):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not is_superuser(request.user):
                messages.error(request, "You don't have sufficient rights to access this page")
                return redirect('/login/')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    if function:
        return decorator(function)
    return decorator


@superuser_required(login_url='/login/')
def home(request):
    return render(request, 'admin_panel/home.html')


@superuser_required(login_url='/login/')
def users(request):
    users = UserProfile.objects.prefetch_related('plates').all()
    return render(request, 'admin_panel/users.html', {'users': users})


@superuser_required(login_url='/login/')
def edit_user(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=user)
        plates_formset = PlateFormSet(request.POST, instance=user)

        if profile_form.is_valid() and plates_formset.is_valid():
            profile_form.save()
            plates_formset.save()

            for form in plates_formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    form.save()

            return redirect('admin_panel:users')  # Перенаправляємо після збереження
    else:
        profile_form = UserProfileForm(instance=user)
        plates_formset = PlateFormSet(instance=user)

    return render(request, 'admin_panel/edit_user.html', {
        'profile_form': profile_form,
        'plates_formset': plates_formset
    })


@superuser_required(login_url='/login/')
def rate(request):
    current_rate = Rates.objects.last()

    if request.method == 'POST':
        form = RateForm(request.POST, instance=current_rate)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rate has been successfully updated')
            return redirect('admin_panel:rate')
    else:
        form = RateForm(instance=current_rate)

    return render(request, 'admin_panel/rate.html', {
        'rate': current_rate.rate,
        'form': form
    })


@superuser_required(login_url='/login/')
def parking_history(request):
    parking_history = History.objects.select_related('plate').all()
    current_rate = Rates.objects.last().rate

    # Додаємо розрахунок вартості
    for parking in parking_history:
        if parking.parking_end:
            # duration = parking.parking_end - parking.parking_start
            # hours = ceil(duration.total_seconds() / 3600)
            parking.cost = parking.duration * current_rate
        else:
            parking.cost = None

    # Пагінація
    paginator = Paginator(parking_history, 50)  # 50 записів на сторінку
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_panel/parking_history.html', {'page_obj': page_obj})


@superuser_required(login_url='/login/')
def reports(request):
    return render(request, 'admin_panel/reports.html')


@superuser_required(login_url='/login/')
def generate_parking_report(request):
    # Отримуємо дані за останні 30 днів
    now = timezone.now()
    thirty_days_ago = now - timezone.timedelta(days=30)

    parking_history = History.objects.filter(parking_start__gte=thirty_days_ago).select_related('plate')
    current_rate = Rates.objects.last().rate

    # Формуємо дані для експорту в Excel
    data = []
    for parking in parking_history:

        parking_start = parking.parking_start.replace(tzinfo=None)
        parking_end = parking.parking_end.replace(tzinfo=None) if parking.parking_end else None
        parking_completed = 'Yes' if parking.is_completed else 'No'

        if parking.parking_end:
            parking.cost = parking.duration * current_rate
        else:
            parking.cost = None
        data.append({
            'ID': parking.id,
            'Plate Number': parking.plate.plate_number,
            'Parking Start': parking_start,
            'Parking End': parking_end,
            'Completed': parking_completed,
            'Duration (hours)': parking.duration,
            'Cost (UAH)': parking.cost
        })

    # Створюємо DataFrame для зручного експорту
    df = pd.DataFrame(data)

    # Записуємо DataFrame у формат Excel в пам'ять
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Parking History')

    output.seek(0)

    # Змінюємо ширину колонок
    output = autosize_columns(output)

    # Формуємо HTTP-відповідь для скачування Excel файлу
    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=parking_report.xlsx'

    return response


def autosize_columns(file_in_memory):
    # Завантажуємо Excel файл з пам'яті за допомогою openpyxl
    wb = load_workbook(file_in_memory)
    ws = wb.active

    # Налаштовуємо ширину колонок
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter  # Отримуємо літеру колонки
        for cell in col:
            try:
                # Визначаємо довжину тексту в кожній комірці колонки
                max_length = max(max_length, len(str(cell.value)))
            except:
                pass
        # Встановлюємо ширину колонки відповідно до максимального значення
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column].width = adjusted_width

    # Створюємо новий BytesIO об'єкт для збереження оновленого файлу
    updated_memory_file = BytesIO()
    wb.save(updated_memory_file)
    updated_memory_file.seek(0)  # Повертаємося до початку файлу в пам'яті

    return updated_memory_file  # Повертаємо оновлений файл у пам'яті