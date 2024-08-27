import cv2
import numpy as np
from paddleocr import PaddleOCR
import re

from .implement_model_detect import get_plate_number_image
from .additional_functions import en_uk_replace

# Initialize PaddleOCR with English language model
ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)


# Validate Ukrainian plate format
def validate_ukraine_plate(text):
    if len(text) > 8 and sum(char.isdigit() for char in text) < 4:
        return text
    text = en_uk_replace(text)
    if len(text) >= 8:
        text = text[-8:].upper()

        print(f"Detected License Plate: {text}")
        return text
    else:
        return text.upper()


def extract_license_plate_text(image_path):
    image = cv2.imread(image_path)

    # Check if the image is loaded correctly
    if image is None:
        print(f"Error: Image at path {image_path} could not be loaded.")
        return None

    # OCR
    result = ocr.ocr(image)
    print("output ocr___", result)
    if result and result != [None]:
        plate_text = ""
        for line in result:
            for word_info in line:
                # Extract the text information
                text = word_info[1][0]
                if text != 'UA':
                    plate_text += text

        if plate_text:
            return validate_ukraine_plate(plate_text)
        else:
            return "Не визначено знаходження номерного знаку"
    else:
        return "Не визначено знаходження номерного знаку"


def segment_characters(image):
    # Preprocess cropped license plate image
    img_lp = cv2.resize(image, (333, 75))
    img_gray_lp = cv2.cvtColor(img_lp, cv2.COLOR_BGR2GRAY)
    _, img_binary_lp = cv2.threshold(img_gray_lp, 200, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    img_binary_lp = cv2.erode(img_binary_lp, (3, 3))
    img_binary_lp = cv2.dilate(img_binary_lp, (3, 3))

    LP_WIDTH = img_binary_lp.shape[0]
    LP_HEIGHT = img_binary_lp.shape[1]

    # Make borders white
    img_binary_lp[0:3, :] = 255
    img_binary_lp[:, 0:3] = 255
    img_binary_lp[72:75, :] = 255
    img_binary_lp[:, 330:333] = 255

    # Estimations of character contours sizes of cropped license plates
    dimensions = [LP_WIDTH / 6,
                  LP_WIDTH / 2,
                  LP_HEIGHT / 10,
                  2 * LP_HEIGHT / 3]

    cv2.imwrite('neural_networks/test_images/ocr/output_img.jpg', img_binary_lp)

    # Get contours within cropped license plate
    char_list = find_contours(dimensions, img_binary_lp)

    return char_list


# Match contours to license plate or character template
def find_contours(dimensions, img):
    # Find all contours in the image
    cntrs, _ = cv2.findContours(img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Retrieve potential dimensions
    lower_width = dimensions[0]
    upper_width = dimensions[1]
    lower_height = dimensions[2]
    upper_height = dimensions[3]

    # Check largest 5 or  15 contours for license plate or character respectively
    cntrs = sorted(cntrs, key=cv2.contourArea, reverse=True)[:15]

    ii = cv2.imread('neural_networks/test_images/ocr/output_img.jpg')

    x_cntr_list = []
    target_contours = []
    img_res = []
    for cntr in cntrs:
        # detects contour in binary image and returns the coordinates of rectangle enclosing it
        intX, intY, intWidth, intHeight = cv2.boundingRect(cntr)

        # checking the dimensions of the contour to filter out the characters by contour's size
        if intWidth > lower_width and intWidth < upper_width and intHeight > lower_height and intHeight < upper_height:
            x_cntr_list.append(
                intX)  # stores the x coordinate of the character's contour, to used later for indexing the contours

            char_copy = np.zeros((44, 24))
            # extracting each character using the enclosing rectangle's coordinates.
            char = img[intY:intY + intHeight, intX:intX + intWidth]
            char = cv2.resize(char, (20, 40))

            cv2.rectangle(ii, (intX, intY), (intWidth + intX, intY + intHeight), (76, 202, 102), 2)

            # Make result formatted for classification: invert colors
            char = cv2.subtract(255, char)

            # Resize the image to 24x44 with black border
            char_copy[2:42, 2:22] = char
            char_copy[0:2, :] = 0
            char_copy[:, 0:2] = 0
            char_copy[42:44, :] = 0
            char_copy[:, 22:24] = 0

            img_res.append(char_copy)  # List that stores the character's binary image (unsorted)

    # arbitrary function that stores sorted list of character indeces
    indices = sorted(range(len(x_cntr_list)), key=lambda k: x_cntr_list[k])
    img_res_copy = []
    for idx in indices:
        img_res_copy.append(img_res[idx])  # stores character images according to their index
    img_res = np.array(img_res_copy)

    return img_res


def get_number_in_text(source_image_path):
    plate_path = get_plate_number_image(source_image_path)
    plate = cv2.imread(plate_path)

    char = segment_characters(plate)

    return extract_license_plate_text(plate_path)


if __name__ == '__main__':
    get_number_in_text('neural_networks/test_images/car_image/193636285orig.jpeg')
