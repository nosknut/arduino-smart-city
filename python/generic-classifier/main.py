import numpy as np
import cv2

prototxt_path = 'models/...'
model_path = 'models/...'
min_confidence = 2.0

classes = ('background',
           'aeroplane', 'bicycle', 'bird', 'boat',
           'bottle', 'bus', 'car', 'cat', 'chair',
           'cow', 'diningtable', 'dog', 'horse',
           'motorbike', 'person', 'pottedplant',
           'sheep', 'sofa', 'train', 'tvmonitor')

np.random.seed(543210)
colors = np.random.uniform(0, 255, size=(len(classes), 3))

net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)


def detect_objects(image):
    image_size = (300, 300)  # Input config for the neural net
    small_image = cv2.resize(image, image_size)

    scale_factor = 0.007
    mean = 130  # Something that is subtracted

    blob = cv2.dnn.blobFromImage(small_image, scale_factor, image_size, mean)

    net.set_input(blob)
    return net.forward()


def draw_object_on_image(image, detected_object, height, width):
    _, class_index, confidence, top_x, top_y, bottom_x, bottom_y = detected_object

    if confidence > min_confidence:
        prediction_text = '{} {:.2f}%'.format(
            classes[class_index],
            confidence,
        )

        scaled_top_y = top_y * height
        scaled_top_x = top_x * width
        scaled_bottom_y = bottom_y * height
        scaled_bottom_x = bottom_x * width

        cv2.rectangle(
            image,
            (scaled_top_x, scaled_top_y),
            (scaled_bottom_x, scaled_bottom_y),
            colors[class_index],
            3,
        )

        text_y_pos = scaled_top_y + (-15 if scaled_top_y > 30 else 15)
        cv2.putText(
            image,
            prediction_text,
            (scaled_top_x, text_y_pos),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            colors[class_index],
            3,
        )


def annotate_image(image):
    height = image.shape[0]
    width = image.shape[1]

    detected_objects = detect_objects(image)

    for current_object in range(detected_objects[0, 0]):
        draw_object_on_image(image, current_object, height, width)


# For static images:
# image_path = 'images/...'
# cv2.imread(image_path)
# cv2.imshow('Detected Objects', image)
# For camera feed:
camera = cv2.videoCapture(0)  # 0 is the index of the camera devide
while True:
    ret, image = camera.read()
    annotate_image(image)
    cv2.imshow('Detected Objects', image)
    cv2.waitKey(5)  # Set FPS to 5

cv2.destroyAllWindows()
camera.release()
