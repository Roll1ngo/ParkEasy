import time

from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt



def resize_image(image_path, new_width=800):
    """Змінює розмір зображення, зберігаючи пропорції.

    Args:
      image_path (str): Шлях до зображення.
      new_width (int): Бажана ширина зображення.

    Returns:
      PIL.Image: Зображення з новим розміром.
    """
    resized_image_path = "./test_images/resized/resize.jpg"
    # Відкриваємо зображення
    image = Image.open(image_path)

    # Обчислюємо нову висоту, зберігаючи пропорції
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio)

    # Змінюємо розмір зображення
    resized_image = image.resize((new_width, new_height))

    resized_image.save(resized_image_path)
    time.sleep(1)

    return resized_image_path


def show_image(image_path: str):

    image = cv2.imread(image_path)
    # Перетворюємо зображення з BGR (формат OpenCV) на RGB (формат matplotlib)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Відображаємо зображення за допомогою matplotlib
    plt.imshow(image_rgb)
    plt.axis('off')  # Вимикаємо осі
    plt.show()
