# get_database.py
import os
import sys
import django

# Додаємо шлях до кореневого каталогу проекту
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Встановлюємо змінну середовища для налаштування Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParkEasy.settings')

# Ініціалізуємо Django
django.setup()

# Тепер можна імпортувати моделі
from car_image_download.models import CarNumberPlate

# Ваш код для отримання даних з бази
all_entries = CarNumberPlate.objects.all()

for entry in all_entries:
    print(entry.number_plate_text, entry.image, entry.uploaded_at)

