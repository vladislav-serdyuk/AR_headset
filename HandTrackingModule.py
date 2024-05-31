"""
Copyright (C) 2024  Vladislav Serdyuk

Этот файл — часть AR_headset.
AR_headset — свободная программа: вы можете перераспространять ее и/или
изменять ее на условиях Стандартной общественной лицензии GNU в том виде,
в каком она была опубликована Фондом свободного программного обеспечения;
либо версии 3 лицензии, либо любой более поздней версии.
AR_headset распространяется в надежде, что она будет полезной, но БЕЗО ВСЯКИХ ГАРАНТИЙ;
даже без неявной гарантии ТОВАРНОГО ВИДА или ПРИГОДНОСТИ ДЛЯ ОПРЕДЕЛЕННЫХ ЦЕЛЕЙ.
Подробнее см. в Стандартной общественной лицензии GNU.
Вы должны были получить копию Стандартной общественной лицензии GNU вместе с этой программой.
Если это не так, см. <https://www.gnu.org/licenses/>.
"""

import cv2
import mediapipe as mp


def fingers_up(my_hand):
    """
    Finds how many fingers are open and returns in a list.
    Considers left and right hands separately
    :return: List of which fingers are up
    """
    fingers = []
    my_hand_type = my_hand["type"]
    my_lm_list = my_hand["lmList"]
    # Thumb
    if my_hand_type == "Right":
        if my_lm_list[4][0] > my_lm_list[3][0]:
            fingers.append(1)
        else:
            fingers.append(0)
    else:
        if my_lm_list[4][0] < my_lm_list[3][0]:
            fingers.append(1)
        else:
            fingers.append(0)

    # 4 Fingers
    for _id in range(1, 5):
        if my_lm_list[[4, 8, 12, 16, 20][_id]][1] < my_lm_list[[4, 8, 12, 16, 20][_id] - 2][1]:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers


class HandDetector:
    """
    Finds Hands using the mediapipe library. Exports the landmarks
    in pixel format. Adds extra functionalities like finding how
    many fingers are up or the distance between two fingers. Also
    provides bounding box info of the hand found.
    """

    def __init__(self, static_mode=False, max_hands=2, model_complexity=1, detection_con=0.5, min_track_con=0.5):

        """
        :param static_mode: In static mode, detection is done on each image: slower
        :param max_hands: Maximum number of hands to detect
        :param model_complexity: Complexity of the hand landmark model: 0 or 1.
        :param detection_con: Minimum Detection Confidence Threshold
        :param min_track_con: Minimum Tracking Confidence Threshold
        """
        self.hands = mp.solutions.hands.Hands(static_image_mode=static_mode,
                                              max_num_hands=max_hands,
                                              model_complexity=model_complexity,
                                              min_detection_confidence=detection_con,
                                              min_tracking_confidence=min_track_con)

    def find_hands(self, img):
        """
        Finds hands in a BGR image.
        :param img: Image to find the hands in.
        :return: Hands info
        """
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)
        all_hands = []
        h, w, c = img.shape

        if results.multi_hand_landmarks:
            for handType, handLms in zip(results.multi_handedness, results.multi_hand_landmarks):
                my_hand = {}
                # lmList
                my_lm_list = []
                x_list = []
                y_list = []
                for lm in handLms.landmark:
                    px, py, pz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                    my_lm_list.append([px, py, pz])
                    x_list.append(px)
                    y_list.append(py)

                my_hand["lmList"] = my_lm_list

                # bbox
                xmin, xmax = min(x_list), max(x_list)
                ymin, ymax = min(y_list), max(y_list)
                box_w, box_h = xmax - xmin, ymax - ymin
                my_hand["bbox"] = xmin, ymin, box_w, box_h

                if handType.classification[0].label == "Right":
                    my_hand["type"] = "Left"
                else:
                    my_hand["type"] = "Right"

                my_hand["fingersUp"] = fingers_up(my_hand)

                all_hands.append(my_hand)

        return all_hands
