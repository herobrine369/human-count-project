"""

"""
# TODO: deploy it on django and reactjs
########################################################
# horizontal = np.hstack([img, img])
# vertical = np.vstack([img, img])
# grid = np.vstack([horizontal, horizontal])

# print(type(vertical))

# img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
########################################################
from time import sleep

import requests
import torchvision
import torch
import numpy as np
import cv2

import threading

# various functions and fields here
persons_count_ = 0
has_exited = False

COCO_INSTANCE_CATEGORY_NAMES = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
    'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
    'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
    'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
    'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]


def upload_count():
    # TODO: MAKE IT FASTER
    try:
        curr_count = persons_count_
        requests.post('http://localhost:8103/persons-count/', data={'count': str(curr_count)})
        print(f"uploaded count {curr_count}")
    except Exception:
        pass


def keep_uploading_count():
    while not has_exited:
        t = threading.Thread(target=upload_count)
        t.daemon = True
        t.start()
        sleep(10)


def process_rects_labels(img, pred):
    """
    Manipulate the prediction data for counting persons

    Args:
        img (np.ndarray): A image of the detection
        pred (dict): detection predictions for img

    Returns:
        (tuple):
            img_rects_labels (np.ndarray): image which is annotated with rectangles, labels and persons count for the prediction
            persons_count (int): count of persons
    """
    persons_count = 0
    img_rects_labels = img.copy()
    for (rect, label, score) in zip(pred[0]["boxes"], pred[0]["labels"], pred[0]["scores"]):
        if score <= 0.6:
            continue
        if label == 1:
            persons_count += 1
        # put label at the top-left of rectangle
        cv2.putText(img_rects_labels,
                    f"{COCO_INSTANCE_CATEGORY_NAMES[label]}, {score:.3f}",
                    (int(rect[0]), int(rect[1]) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),  # white
                    2,
                    cv2.LINE_AA
                    )
        # rectangles around objects
        cv2.rectangle(img_rects_labels,
                      (int(rect[0]), int(rect[1])),
                      (int(rect[2]), int(rect[3])),
                      (255, 0, 0),  # blue
                      2,
                      cv2.LINE_AA)

    # put person count at the top-left of the image
    cv2.putText(img_rects_labels,
                f"number of persons, {persons_count}",
                (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),  # white
                2,
                cv2.LINE_AA
                )
    return img_rects_labels, persons_count


# def draw_rects_labels(img, pred):
#     """
#     Annotate an image with its prediction of object detection
#
#     Args:
#         img (np.ndarray): A image of the detection
#         pred (dict): detection predictions for img
#
#     Returns:
#         A image which is annotated with rectangles and labels for the prediction
#     """
#     img_rects_labels = img.copy()
#     for (rect, label, score) in zip(pred[0]["boxes"], pred[0]["labels"], pred[0]["scores"]):
#         if score <= 0.6:
#             continue
#         cv2.putText(img_rects_labels,
#                     f"{COCO_INSTANCE_CATEGORY_NAMES[label]}, {score:.3f}",
#                     (int(rect[0]), int(rect[1]) - 10),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     1,
#                     (255, 255, 255),  # white
#                     2,
#                     cv2.LINE_AA
#                     )
#         cv2.rectangle(img_rects_labels,
#                       (int(rect[0]), int(rect[1])),
#                       (int(rect[2]), int(rect[3])),
#                       (255, 0, 0),  # blue
#                       2,
#                       cv2.LINE_AA)
#     return img_rects_labels


def main():
    global has_exited, persons_count_

    # execute thread for uploading the persons count
    t = threading.Thread(target=keep_uploading_count)
    t.daemon = True
    t.start()

    # prepare cuda device if available
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    # prepare model
    model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
    model.eval().to(device)

    cap = cv2.VideoCapture(0)

    while True:
        ret, raw_img = cap.read()

        # recognition
        # and then count the people
        # store the data

        # convert bgr to rgb and feed it into model
        img_rgb = cv2.cvtColor(raw_img, cv2.COLOR_BGR2RGB)
        with torch.no_grad():
            x = torchvision.transforms.ToTensor()(img_rgb).to(device)
            results = model([x])

        img_rects_label, persons_count = process_rects_labels(raw_img, results)

        cv2.imshow('frame', img_rects_label)

        persons_count_ = persons_count

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    has_exited = True


if __name__ == '__main__':
    main()
