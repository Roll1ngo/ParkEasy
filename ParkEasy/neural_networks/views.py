from django.shortcuts import render
from .implement_model_ocr import get_number_in_text
from .forms import ImageUploadForm


def upload_car_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()  # Зберігаємо зображення
            image_path = uploaded_image.image.path  # Отримуємо шлях до зображення
            path_to_number_plate = get_number_in_text(image_path)

            return render(request, 'neural_networks/upload_image.html', {'text': path_to_number_plate})
    else:
        form = ImageUploadForm()
    return render(request, 'neural_networks/upload_image.html', {'form': form})

