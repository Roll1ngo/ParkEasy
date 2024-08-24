from additional_functions import show_image

import cv2
import os
import pytesseract
import numpy as np
from PIL import Image

import matplotlib.pyplot as plt

os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
custom_config = r'--oem 3 --psm 7 -l ukr '

save_path = 'ppc.jpg'

# Розпізнавання тексту


def detect_text(image_path):
    img = cv2.imread(image_path)

    text = pytesseract.image_to_string(img, config=custom_config)
    return text


def preprocess_image(img_path, save_path=None):
    """
    Функція для підготовки зображення номерного знаку до розпізнавання.

    Args:
        img_path (str): Шлях до зображення.
        save_path (str, optional): Шлях для збереження обробленого зображення.

    Returns:
        PIL.Image: Оброблене зображення.
    """

    # Завантаження зображення
    img = cv2.imread(img_path)
    if img is None:
        raise ValueError(f"Image not found at {img_path}")

    # Перетворення в сірий колір
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Пошук контурів
    contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        raise ValueError("No contours found")

    # Вибір найбільшого контуру (припускаємо, що це номерний знак)
    c = max(contours, key=cv2.contourArea)

    # Обчислення обертаючого прямокутника
    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)
    box = np.array(box, dtype=np.float32)

    # Випрямлення зображення
    width = int(rect[1][0])
    height = int(rect[1][1])
    dst = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]], dtype=np.float32)
    m = cv2.getPerspectiveTransform(box, dst)
    warped = cv2.warpPerspective(gray, m, (width, height))

    # Покращення контрасту
    alpha = 1.5  # Контраст
    beta = 0  # Яскравість
    adjusted = cv2.convertScaleAbs(warped, alpha=alpha, beta=beta)

    # Бінаризація
    thresh = cv2.threshold(adjusted, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Перетворення в формат PIL для Tesseract
    pil_image = Image.fromarray(thresh)

    if save_path:
        cv2.imwrite(save_path, cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR))

    return pil_image


if __name__ == '__main__':
    print(detect_text(
        "test_images/ocr/output_img.jpg"))
    # show_image("neural_networks/test_images/ocr/output_img.jpg")
    # img_path = 'test_images/plate_number_images/license-plate_413fc2dd-db25-439d-b218-f9d7efe620fb_0.81.jpg'
    # ppc_img = preprocess_image(img_path)
    # # show_image(img_path)
    # plt.imshow(ppc_img)
    # plt.axis('off')  # Вимикаємо осі
    # plt.show()