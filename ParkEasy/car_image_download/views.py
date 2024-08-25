from django.shortcuts import render
from neural_networks.implement_model_ocr import get_number_in_text
from .forms import ImageUploadForm
from .models import CarNumberPlate


def upload_car_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()  # Зберігаємо зображення
            image_path = uploaded_image.image.path  # Отримуємо шлях до зображення

            try:
                # Спроба розпізнати текст з зображення за допомогою OCR
                number_plate_text = get_number_in_text(image_path)

                # Збереження розпізнаного тексту у базу даних
                CarNumberPlate.objects.create(number_plate_text=number_plate_text)

            except Exception as e:
                # Обробка помилок під час розпізнавання
                return render(request, 'neural_networks/upload_image.html', {
                    'form': form,
                    'error': 'Failed to process image: ' + str(e)
                })

            # Відображення результату, якщо все успішно
            return render(request, 'neural_networks/upload_image.html', {
                'text': number_plate_text
            })
    else:
        form = ImageUploadForm()  # Створення пустої форми для GET запитів
    return render(request, 'neural_networks/upload_image.html', {'form': form})



