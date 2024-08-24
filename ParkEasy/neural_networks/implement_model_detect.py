from inference_sdk import InferenceHTTPClient
import cv2
import os
import uuid


# initialize the client
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="9cBmz9pmN1YhVsvyH05Z"
)
SAVE_DIR = 'neural_networks/test_images/plate_number_images'


def get_plate_number_image(image_path: str):
    resize_image_path = image_path
    image = cv2.imread(resize_image_path)
    model_predict = CLIENT.infer(resize_image_path, model_id="license-plates-us-eu-1tufg/2")
    predictions = model_predict['predictions']

    for predict in predictions:
        number_plate_uuid = uuid.uuid4()
        if predict['class'] == 'license-plate' and predict['confidence'] > 0.7:

            x, y, width, height = predict['x'], predict['y'], predict['width'], predict['height']
            confidence = round(predict['confidence'], 2)
            print(x, y, width, height, "______", confidence)

            # Обчислення координат верхнього лівого і нижнього правого кутів
            x1, y1, x2, y2 = int(x - width / 2), int(y - height / 2), int(x + width / 2), int(y + height / 2)

            # Вирізаємо область з зображення
            cropped_image = image[y1:y2, x1:x2]
            # Adjust coordinates for OpenCV (top-left corner)
            x1, y1, x2, y2 = int(x - width / 2), int(y - height / 2), int(x + width / 2), int(y + height / 2)

            # Draw bounding box
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green color for bounding boxes

            # Add label and confidence (optional)
            text = f"{predict['class']} ({confidence:.2f})"
            cv2.putText(image, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Збереження вирізаного зображення
            save_path = os.path.join(SAVE_DIR, f"{predict['class']}_{number_plate_uuid}_{confidence}.jpg")
            cv2.imwrite(save_path, cropped_image)
    return save_path


if __name__ == '__main__':

    source_image_path = 'neural_networks/test_images/car_image/1484814.jpg'
    path_number_plate_image = get_plate_number_image(source_image_path)
