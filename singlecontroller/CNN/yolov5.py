import numpy as np
import torch
import cv2
import random


def random_int():
    return random.randint(0, 255)


model = torch.hub.load("ultralytics/yolov5", "yolov5s")
model.conf = 0.5

class_names = [
    "aeroplane",
    "bicycle",
    "bird",
    "boat",
    "bottle",
    "bus",
    "car",
    "cat",
    "chair",
    "cow",
    "diningtable",
    "dog",
    "horse",
    "motorbike",
    "person",
    "pottedplant",
    "sheep",
    "sofa",
    "train",
    "tvmonitor",
]

num_classes = len(class_names)
class_colors = []
for i in range(0, num_classes):
    hue = 255 * i / num_classes
    col = np.zeros((1, 1, 3)).astype("uint8")
    col[0][0][0] = hue
    col[0][0][1] = 128
    col[0][0][2] = 255
    cvcol = cv2.cvtColor(col, cv2.COLOR_HSV2BGR)
    col = (int(cvcol[0][0][0]), int(cvcol[0][0][1]), int(cvcol[0][0][2]))
    class_colors.append(col)


def main_n(frame, cv_image):
    result = model(frame)

    datas = []

    ndresult = result.xyxy[0]
    for v in ndresult:
        if v[5] == 0:
            datas.append(
                [
                    int(v[0]),  # left
                    int(v[1]),  # top
                    int(v[2]),  # right
                    int(v[3]),  # bottom
                    float(v[4]),  # confidence
                ]
            )
    for data in datas:
        if data[4] > 50 / 100:
            left, top, right, bottom = data[:4]
            cv_image = cv2.rectangle(
                cv_image, (left, top), (right, bottom), (0, 255, 0), 3
            )

    return cv_image


def main_p(frame, cv_image):
    result = model(frame)
    datas = []
    ndresult = result.pandas().xyxy[0]
    for i in range(len(ndresult)):
        name = ndresult.name[i]
        conf = ndresult.confidence[i]
        xmin = ndresult.xmin[i]
        ymin = ndresult.ymin[i]
        xmax = ndresult.xmax[i]
        ymax = ndresult.ymax[i]

        datas.append(
            [
                int(xmin),  # left
                int(ymax),  # top
                int(xmax),  # right
                int(ymin),  # bottom
                float(conf),
                str(name),  # name
            ]
        )
    for data in datas:
        if data[5] == "person":
            if data[4] > 50 / 100:
                left, top, right, bottom = data[:4]
                conf = round(data[4] * 100)
                text = data[5] + " - " + str(conf) + "%"
                cv2.rectangle(
                    cv_image,
                    (left, top),
                    (right, bottom),
                    class_colors[class_names.index(data[5])],
                    2,
                )
                cv2.putText(
                    cv_image,
                    text,
                    (left, top),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    class_colors[class_names.index(data[5])],
                    2,
                )
    return cv_image


def main_m(frame, cv_image):
    result = model(frame)
    datas = []
    ndresult = result.pandas().xyxy[0]
    for i in range(len(ndresult)):
        name = ndresult.name[i]
        conf = ndresult.confidence[i]
        xmin = ndresult.xmin[i]
        ymin = ndresult.ymin[i]
        xmax = ndresult.xmax[i]
        ymax = ndresult.ymax[i]

        datas.append(
            [
                int(xmin),  # left
                int(ymax),  # top
                int(xmax),  # right
                int(ymin),  # bottom
                float(conf),
                str(name),  # name
            ]
        )
    for data in datas:
        if data[5] in class_names:
            if data[4] > 50 / 100:
                left, top, right, bottom = data[:4]
                conf = round(data[4] * 100)
                text = data[5] + " - " + str(conf) + "%"
                cv2.rectangle(
                    cv_image,
                    (left, top),
                    (right, bottom),
                    class_colors[class_names.index(data[5])],
                    2,
                )
                cv2.putText(
                    cv_image,
                    text,
                    (left, top),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    class_colors[class_names.index(data[5])],
                    2,
                )
    return cv_image
