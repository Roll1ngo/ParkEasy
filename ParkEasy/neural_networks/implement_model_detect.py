from inference_sdk import InferenceHTTPClient
import matplotlib.pyplot as plt
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
    try:
        image = cv2.imread(image_path)
        model_predict = CLIENT.infer(image_path, model_id="license-plates-us-eu-1tufg/2")
        predictions = model_predict['predictions']

        for predict in predictions:
            number_plate_uuid = uuid.uuid4()
            if predict['class'] == 'license-plate' and predict['confidence'] > 0.3:
                x, y, width, height = predict['x'], predict['y'], predict['width'], predict['height']
                confidence = round(predict['confidence'], 2)

                x1, y1 = int(x - width / 2), int(y - height / 2)
                x2, y2 = int(x + width / 2), int(y + height / 2)

                # Ensure coordinates are within image bounds
                if image is not None:
                    x1 = max(0, x1)
                    y1 = max(0, y1)
                    x2 = min(image.shape[1], x2)
                    y2 = min(image.shape[0], y2)

                    cropped_image = image[y1:y2, x1:x2]

                    if cropped_image.size > 0:
                        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        text = f"{predict['class']} ({confidence:.2f})"
                        cv2.putText(image, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                        # Ensure SAVE_DIR exists before saving the file
                        os.makedirs(SAVE_DIR, exist_ok=True)
                        save_path = os.path.join(SAVE_DIR, f"{predict['class']}_{number_plate_uuid}_{confidence}.jpg")
                        cv2.imwrite(save_path, cropped_image)
                        return save_path
                    else:
                        print("Вирізане зображення порожнє.")
                else:
                    print("Зображення є None, перевірте завантаження зображення.")
                    return "12"

        # If no license plate is detected
        print("Не вдалося виявити номерний знак на зображені")
        return "12"

    except UnboundLocalError:
        print("Помилка: save_path не визначений.")
        return "12"

    except Exception as e:
        print(f"Невідома помилка: {e}")
        return "12"




if __name__ == '__main__':

    source_image_path = 'neural_networks/test_images/car_image/1484814.jpg'
    path_number_plate_image = get_plate_number_image(source_image_path)
