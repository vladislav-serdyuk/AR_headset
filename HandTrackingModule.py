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


def fingersUp(myHand):
    """
    Finds how many fingers are open and returns in a list.
    Considers left and right hands separately
    :return: List of which fingers are up
    """
    fingers = []
    myHandType = myHand["type"]
    myLmList = myHand["lmList"]
    # Thumb
    if myHandType == "Right":
        if myLmList[4][0] > myLmList[3][0]:
            fingers.append(1)
        else:
            fingers.append(0)
    else:
        if myLmList[4][0] < myLmList[3][0]:
            fingers.append(1)
        else:
            fingers.append(0)

    # 4 Fingers
    for _id in range(1, 5):
        if myLmList[[4, 8, 12, 16, 20][_id]][1] < myLmList[[4, 8, 12, 16, 20][_id] - 2][1]:
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

    def __init__(self, staticMode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5):

        """
        :param mode: In static mode, detection is done on each image: slower
        :param maxHands: Maximum number of hands to detect
        :param modelComplexity: Complexity of the hand landmark model: 0 or 1.
        :param detectionCon: Minimum Detection Confidence Threshold
        :param minTrackCon: Minimum Tracking Confidence Threshold
        """
        self.hands = mp.solutions.hands.Hands(static_image_mode=staticMode,
                                              max_num_hands=maxHands,
                                              model_complexity=modelComplexity,
                                              min_detection_confidence=detectionCon,
                                              min_tracking_confidence=minTrackCon)

    def findHands(self, img):
        """
        Finds hands in a BGR image.
        :param img: Image to find the hands in.
        :return: Hands info
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)
        allHands = []
        h, w, c = img.shape
        if results.multi_hand_landmarks:
            for handType, handLms in zip(results.multi_handedness, results.multi_hand_landmarks):
                myHand = {}
                # lmList
                mylmList = []
                xList = []
                yList = []
                for lm in handLms.landmark:
                    px, py, pz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                    mylmList.append([px, py, pz])
                    xList.append(px)
                    yList.append(py)

                myHand["lmList"] = mylmList

                # bbox
                xmin, xmax = min(xList), max(xList)
                ymin, ymax = min(yList), max(yList)
                boxW, boxH = xmax - xmin, ymax - ymin
                myHand["bbox"] = xmin, ymin, boxW, boxH

                if handType.classification[0].label == "Right":
                    myHand["type"] = "Left"
                else:
                    myHand["type"] = "Right"

                myHand["fingersUp"] = fingersUp(myHand)

                allHands.append(myHand)

        return allHands
