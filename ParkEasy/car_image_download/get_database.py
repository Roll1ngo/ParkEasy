from car_image_download.models import CarNumberPlate

# Витягуємо всі записи з таблиці CarNumberPlate
all_entries = CarNumberPlate.objects.all()

# Переглядаємо кожен запис
for entry in all_entries:
    print(entry.number_plate_text, entry.image, entry.uploaded_at)
