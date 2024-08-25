from django.shortcuts import render
from neural_networks.implement_model_ocr import get_number_in_text
from .models import CarNumberPlate, ImageUploadCar
from .forms import ImageUploadForm  # Додаємо імпорт форми

# Ваш код для upload_car_image
def upload_car_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()  # Зберігаємо завантажене зображення
            image_path = uploaded_image.image.path  # Отримуємо шлях до збереженого зображення

            try:
                # Спроба витягти текст із зображення за допомогою OCR
                number_plate_text = get_number_in_text(image_path)

                # Зберігаємо розпізнаний текст номерного знака в базу даних
                CarNumberPlate.objects.create(number_plate_text=number_plate_text, user=request.user)

            except Exception as e:
                # Обробка помилок під час OCR
                return render(request, 'neural_networks/upload_image.html', {
                    'form': form,
                    'error': 'Failed to process image: ' + str(e)
                })

            # Повертаємо результат, якщо все успішно
            return render(request, 'neural_networks/upload_image.html', {
                'text': number_plate_text
            })
    else:
        form = ImageUploadForm()  # Створюємо пусту форму для GET-запитів
    return render(request, 'neural_networks/upload_image.html', {'form': form})
