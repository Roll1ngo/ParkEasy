from django.shortcuts import render
from neural_networks.implement_model_ocr import get_number_in_text
from .forms import ImageUploadForm
from .models import CarNumberPlate  # Імпортуємо модель

def upload_car_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()  # Зберігаємо зображення
            image_path = uploaded_image.image.path  # Отримуємо шлях до збереженого зображення

            try:
                # Спроба витягнути текст з номерного знака за допомогою OCR
                number_plate_text = get_number_in_text(image_path)

                # Зберігаємо зображення та текст номерного знака у базі даних
                CarNumberPlate.objects.create(
                    image=uploaded_image.image,
                    number_plate_text=number_plate_text
                )

            except Exception as e:
                # Обробка будь-яких помилок під час OCR
                return render(request, 'neural_networks/upload_image.html', {
                    'form': form,
                    'error': 'Помилка обробки зображення: ' + str(e)
                })

            # Відображаємо результат успішного виконання
            return render(request, 'neural_networks/upload_image.html', {
                'text': number_plate_text
            })
    else:
        form = ImageUploadForm()  # Створюємо пусту форму для GET-запитів
    return render(request, 'neural_networks/upload_image.html', {'form': form})


