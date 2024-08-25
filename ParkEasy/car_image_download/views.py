from django.shortcuts import render
from neural_networks.implement_model_ocr import get_number_in_text
from .forms import ImageUploadForm


def upload_car_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()  # Save the uploaded image
            image_path = uploaded_image.image.path  # Get the path to the saved image

            try:
                # Try to extract text from the image using OCR
                path_to_number_plate = get_number_in_text(image_path)
            except Exception as e:
                # Handle any errors during OCR processing
                return render(request, 'neural_networks/upload_image.html', {
                    'form': form,
                    'error': 'Failed to process image: ' + str(e)
                })

            # Render the result if everything is successful
            return render(request, 'neural_networks/upload_image.html', {
                'text': path_to_number_plate
            })
    else:
        form = ImageUploadForm()  # Create a blank form for GET requests
    return render(request, 'neural_networks/upload_image.html', {'form': form})


