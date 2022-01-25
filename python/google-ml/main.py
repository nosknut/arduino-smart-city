import numpy as np
import cv2
import json
import base64
import io
import os
from google.cloud import vision
from google.oauth2 import service_account


def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

# https://cloud.google.com/vision/docs/base64#python


def encode_image(image):
    image_content = image.read()
    return base64.b64encode(image_content)


def getRect(vertecies, height, width):
    xs, ys = set(), set()
    for vertex in vertecies:
        xs.add(vertex['x'] * width)
        ys.add(vertex['y'] * height)

    return [
        (int(min(xs)), int(max(ys))),  # top_left
        (int(max(xs)), int(min(ys))),  # bottom_right
    ]


work_folder = 'python/google-ml/'
credentials = service_account.Credentials.from_service_account_file(
    work_folder+'service_account.json')
client = vision.ImageAnnotatorClient(credentials=credentials)

file_name = os.path.abspath(work_folder+'images/bins.jpg')

with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

# https://cloud.google.com/python/docs/reference/vision/latest/google.cloud.vision_v1.types.AnnotateImageResponse
response = load_json(work_folder + 'response.json')
# client.label_detection(image=vision.Image(content=content))
print(response)

image = cv2.imread(file_name)
for obj in response['responses'][0]['localizedObjectAnnotations']:
    mid, name, score = list(obj.values())[:3]
    if name == "Waste container":
        height, width = image.shape[:2]
        top_left, bottom_right = getRect(
            obj['boundingPoly']['normalizedVertices'], height, width)
        cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 3)

cv2.imshow('Detected Objects', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
