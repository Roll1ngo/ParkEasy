import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def detect_text(image_path):
    # Завантаження зображення
    img = cv2.imread(image_path)

    # Перетворення на відтінки сірого
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Використання Tesseract для розпізнавання тексту
    text = pytesseract.image_to_string(gray)
    return text


if __name__ == '__main__':
    print(detect_text(
        "neural_networks/test_images/plate_number_images/license-plate_5f912e8a-230d-4033-bfda-b71878cfb944_0.92.jpg"))
