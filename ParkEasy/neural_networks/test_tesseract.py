from additional_functions import show_image

import cv2
import pytesseract
import numpy as np
from PIL import Image


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
custom_config = r'--oem 3 --psm 7 --tessdata-dir "C:\Program Files\Tesseract-OCR\tessdata" -l \
ukr -c tessedit_char_whitelist=0123456789АБВГҐДЕЄЖЗИІЇКЛМНОПРСТУФХЦЧШЩЬЮЯ'

save_path = 'neural_networks/test_images/plate_number_images/ppc_images/preprocess_img'

# Розпізнавання тексту


def detect_text(image_path):
    img = cv2.imread(image_path)

    text = pytesseract.image_to_string(img, config=custom_config)
    return text


def preprocess_image(img_path):
    """
    Функція для підготовки зображення номерного знаку до розпізнавання.

    Args:
        img_path (str): Шлях до зображення.

    Returns:
        PIL.Image: Оброблене зображення.
    """

    # Завантаження зображення
    img = cv2.imread(img_path)

    # Перетворення в сірий колір
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Пошук контурів
    contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Вибір найбільшого контуру (припускаємо, що це номерний знак)
    c = max(contours, key=cv2.contourArea)

    # Обчислення обертаючого прямокутника
    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)
    box = box.astype(np.intp)

    # Випрямлення зображення
    width = int(rect[1][0])
    height = int(rect[1][1])
    dst = np.zeros((height, width, 3), dtype="uint8")
    m = cv2.getPerspectiveTransform(box, np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]]))
    warped = cv2.warpPerspective(gray, m, (width, height))

    # Покращення контрасту
    alpha = 1.5  # Контраст
    beta = 0  # Яскравість
    adjusted = cv2.convertScaleAbs(warped, alpha=alpha, beta=beta)

    # Бінаризація
    thresh = cv2.threshold(adjusted, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Перетворення в формат PIL для Tesseract
    pil_image = Image.fromarray(thresh)
    cv2.imwrite(save_path, pil_image)

    return pil_image


if __name__ == '__main__':
    # print(detect_text(
    #     "neural_networks/test_images/ocr/output_img.jpg"))
    # show_image("neural_networks/test_images/ocr/output_img.jpg")
    img_path = 'test_images/plate_number_images/license-plate_2b865d1d-c040-4cfe-9ceb-2d0f0c5f5b76_0.85.jpg'
    ppc_img = preprocess_image(img_path)

