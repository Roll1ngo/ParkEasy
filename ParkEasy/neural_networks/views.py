from django.shortcuts import render
from django.utils import timezone
from .implement_model_ocr import get_number_in_text
from .forms import ImageUploadForm
from math import ceil
from parkings.models import Plates, History, UserProfile


def upload_car_image_and_start(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()  # Зберігаємо зображення
            image_path = uploaded_image.image.path  # Отримуємо шлях до зображення
            path_to_number_plate = get_number_in_text(image_path)

            if path_to_number_plate == 'Не визначено знаходження номерного знаку':
                return render(request, 'neural_networks/upload_image.html', {'form': form, 'error': 'Car plate hasn\'t been recognized'})

            try:
                plate = Plates.objects.get(plate_number=path_to_number_plate)
            except Plates.DoesNotExist:
                return render(request, 'neural_networks/upload_image.html', {'form': form, 'error': f'Car plate {path_to_number_plate} hasn\'t found in database'})

            if plate.is_banned:
                return render(request, 'neural_networks/upload_image.html',
                              {'form': form, 'error': f'Car plate {path_to_number_plate} is banned'})

            if plate.user != UserProfile.objects.get(user=request.user):
                return render(request, 'neural_networks/upload_image.html', {'form': form, 'error': f'Car plate {path_to_number_plate} doesn\'t belong to you'})

            # Додавання нового запису до таблиці History
            History.objects.create(
                plate=plate,
                parking_start=timezone.now(),
                is_completed=False
            )

            return render(request, 'neural_networks/upload_image.html', {'form': form, 'text': 'Your parking session has just been started!'})

    else:
        form = ImageUploadForm()

    return render(request, 'neural_networks/upload_image.html', {'form': form})


def upload_car_image_and_finish(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()  # Зберігаємо зображення
            image_path = uploaded_image.image.path  # Отримуємо шлях до зображення
            path_to_number_plate = get_number_in_text(image_path)

            # Якщо номерний знак не розпізнаний
            if path_to_number_plate == 'Не визначено знаходження номерного знаку':
                return render(request, 'neural_networks/upload_image.html', {'form': form, 'error': 'Car plate hasn\'t been recognized'})

            # Перевірка наявності номерного знаку в БД
            try:
                plate = Plates.objects.get(plate_number=path_to_number_plate)
            except Plates.DoesNotExist:
                return render(request, 'neural_networks/upload_image.html', {'form': form, 'error': f'Car plate {path_to_number_plate} hasn\'t found in database'})

            # Перевірка власника номерного знаку
            if plate.user != UserProfile.objects.get(user=request.user):
                return render(request, 'neural_networks/upload_image.html', {'form': form, 'error': f'Car plate {path_to_number_plate} doesn\'t belong to you'})

            # Перевірка наявності активного паркування
            try:
                parking_history = History.objects.get(plate=plate, is_completed=False)
            except History.DoesNotExist:
                return render(request, 'neural_networks/upload_image.html', {'form': form, 'error': f'No ongoing parking session found for car plate {path_to_number_plate}'})

            # Завершення паркування
            parking_end_time = timezone.now()
            parking_start_time = parking_history.parking_start

            # Розрахунок тривалості в годинах (округляємо до більшої години)
            duration_seconds = (parking_end_time - parking_start_time).total_seconds()
            duration_hours = ceil(duration_seconds / 3600)  # Завжди округляємо до більшої години

            # Оновлення запису в історії
            parking_history.parking_end = parking_end_time
            parking_history.is_completed = True
            parking_history.duration = duration_hours  # Зберігаємо тривалість в годинах
            parking_history.save()

            return render(request, 'neural_networks/upload_image.html', {'text': 'Your parking session has just been finished!'})

    else:
        form = ImageUploadForm()

    return render(request, 'neural_networks/upload_image.html', {'form': form})