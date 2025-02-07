import random

import cv2
import numpy as np
import requests
import torch
from PIL import Image
from flask import Flask, jsonify, Response

app = Flask(__name__, template_folder='.')

model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

detected_fruits = []


def check_spoilage(cropped_image):
    img = np.array(cropped_image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    yellow_pixels = cv2.countNonZero(mask)
    total_pixels = img.shape[0] * img.shape[1]
    yellow_percentage = (yellow_pixels / total_pixels) * 100

    spoilage_threshold = 10
    if yellow_percentage > spoilage_threshold:
        return True
    else:
        return False


def detect_freshness(cropped_image, class_name):
    img = np.array(cropped_image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    avg_hue = cv2.mean(img[:, :, 0])[0]
    global freshness
    freshness_values = {
        0: 'Very Fresh',
        1: 'Fresh',
        2: 'Slightly Stale',
        3: 'Stale',
        4: 'Rotten'
    }

    if class_name == 'apple':
        if avg_hue < 30:
            freshness = freshness_values[0]
        elif avg_hue < 60:
            freshness = freshness_values[1]
        elif avg_hue < 90:
            freshness = freshness_values[2]
        elif avg_hue < 120:
            freshness = freshness_values[3]
        else:
            freshness = freshness_values[4]
    elif class_name == 'banana':
        if avg_hue < 20:
            freshness = freshness_values[0]
        elif avg_hue < 80:
            freshness = freshness_values[1]
        elif avg_hue < 140:
            freshness = freshness_values[2]
        elif avg_hue < 180:
            freshness = freshness_values[3]
        else:
            freshness = freshness_values[4]
    elif class_name == 'orange':
        if avg_hue < 20:
            freshness = freshness_values[0]
        elif avg_hue < 80:
            freshness = freshness_values[1]
        elif avg_hue < 140:
            freshness = freshness_values[2]
        elif avg_hue < 180:
            freshness = freshness_values[3]
        else:
            freshness = freshness_values[4]
    elif class_name == 'broccoli':
        if avg_hue < 20:
            freshness = freshness_values[0]
        elif avg_hue < 80:
            freshness = freshness_values[1]
        elif avg_hue < 140:
            freshness = freshness_values[2]
        elif avg_hue < 180:
            freshness = freshness_values[3]
        else:
            freshness = freshness_values[4]
    elif class_name == 'sandwich':
        if avg_hue < 20:
            freshness = freshness_values[0]
        elif avg_hue < 80:
            freshness = freshness_values[1]
        elif avg_hue < 140:
            freshness = freshness_values[2]
        elif avg_hue < 180:
            freshness = freshness_values[3]
        else:
            freshness = freshness_values[4]
    elif class_name == 'donut':
        if avg_hue < 20:
            freshness = freshness_values[0]
        elif avg_hue < 80:
            freshness = freshness_values[1]
        elif avg_hue < 140:
            freshness = freshness_values[2]
        elif avg_hue < 180:
            freshness = freshness_values[3]
        else:
            freshness = freshness_values[4]
    elif class_name == 'cake':
        if avg_hue < 20:
            freshness = freshness_values[0]
        elif avg_hue < 80:
            freshness = freshness_values[1]
        elif avg_hue < 140:
            freshness = freshness_values[2]
        elif avg_hue < 180:
            freshness = freshness_values[3]
        else:
            freshness = freshness_values[4]
    elif class_name == 'hot dog':
        if avg_hue < 20:
            freshness = freshness_values[0]
        elif avg_hue < 80:
            freshness = freshness_values[1]
        elif avg_hue < 140:
            freshness = freshness_values[2]
        elif avg_hue < 180:
            freshness = freshness_values[3]
        else:
            freshness = freshness_values[4]
    elif class_name == 'pizza':
        if avg_hue < 20:
            freshness = freshness_values[0]
        elif avg_hue < 80:
            freshness = freshness_values[1]
        elif avg_hue < 140:
            freshness = freshness_values[2]
        elif avg_hue < 180:
            freshness = freshness_values[3]
        else:
            freshness = freshness_values[4]
    elif class_name == 'carrot':
        if avg_hue < 20:
            freshness = freshness_values[0]
        elif avg_hue < 80:
            freshness = freshness_values[1]
        elif avg_hue < 140:
            freshness = freshness_values[2]
        elif avg_hue < 180:
            freshness = freshness_values[3]
        else:
            freshness = freshness_values[4]
    return freshness


@app.route('/detect_freshness', methods=['GET'])
def detect_freshness_webcam():
    global detected_fruits
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        results = model(Image.fromarray(frame))
        labels = results.names
        pred_boxes = results.xyxy[0][:, :4]
        detections = []

        detected_fruits = []
        for label, bbox in zip(results.xyxy[0][:, -1].int(), pred_boxes):
            label = int(label)
            class_name = labels[label]
            if class_name in ['apple',
                              'banana',
                              'orange',
                              'sandwich',
                              'broccoli',
                              'carrot',
                              'hot dog',
                              'pizza',
                              'donut',
                              'cake']:
                bbox = bbox.tolist()
                cropped_image = frame[int(bbox[1]):int(bbox[3]), int(bbox[0]):int(bbox[2])]
                freshness_score = detect_freshness(cropped_image, class_name)
                is_spoiled = check_spoilage(cropped_image)

                detection = {
                    'label': class_name,
                    'freshness': freshness_score,
                    'is_spoiled': is_spoiled}
                detections.append(detection)

                detected_fruits.append(class_name)

        city = 'Delhi'
        country = 'India'
        api_key = "f596234f7b2eb18b4a28194da7d158a4"
        weather_url = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?appid={api_key}&q={city},{country}&units=imperial')
        weather_data = weather_url.json()
        temp = round(weather_data['main']['temp'])
        temp = int((temp - 32) * 5 / 9)
        humidity = weather_data['main']['humidity']
        gas_sensor_reading = random.randint(0, 100)

        if detections:
            response = jsonify(
                {'detections': detections, 'temperature': temp, 'humidity': humidity, 'gas_sensor': gas_sensor_reading})
            return Response(response.data, mimetype='application/json')

    cap.release()
    cv2.destroyAllWindows()
    return Response('No detections found', mimetype='text/plain')


@app.route('/detected_fruits', methods=['GET'])
def get_detected_fruits():
    global detected_fruits
    return jsonify({'detected_fruits': detected_fruits})


if __name__ == "__main__":
    app.run(debug=False, host='192.168.137.1', port=5001)

get_detected_fruits()
