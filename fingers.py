from typing import Tuple
import cv2
import numpy as np

from Screen import Screen

class Fingers:
    def __init__(self, hand_landmarks):
        if not hand_landmarks:
            print("WARNING: No hand landmarks present")
            return
        
        self.hand_landmarks = hand_landmarks

        self.thumb_tip = hand_landmarks.landmark[4]
        self.thumb_knuckle = hand_landmarks.landmark[3]
        self.thumb_bottom = hand_landmarks.landmark[2]

        self.index_tip = hand_landmarks.landmark[8]
        self.index_knuckle = hand_landmarks.landmark[6]
        self.index_bottom = hand_landmarks.landmark[5]

        self.middle_tip = hand_landmarks.landmark[12]
        self.middle_knuckle = hand_landmarks.landmark[10]

        self.ring_tip = hand_landmarks.landmark[16]
        self.ring_knuckle = hand_landmarks.landmark[14]

        self.pinky_tip = hand_landmarks.landmark[20]
        self.pinky_knuckle = hand_landmarks.landmark[18]

        self.wrist = hand_landmarks.landmark[0]

    # region fingers
    def thumb_up(self) -> bool:
        return self.thumb_tip.y < self.thumb_knuckle.y

    def thumb_pointing_left(self) -> bool:
        return self.thumb_tip.x < self.thumb_knuckle.x
        
    def thumb_pointing_right(self) -> bool:
        return self.thumb_tip.x > self.thumb_knuckle.x

    def index_up(self) -> bool:
        return self.index_tip.y < self.index_knuckle.y

    def middle_up(self) -> bool:
        return self.middle_tip.y < self.middle_knuckle.y

    def ring_up(self) -> bool:
        return self.ring_tip.y < self.ring_knuckle.y

    def pinky_up(self) -> bool:
        return self.pinky_tip.y < self.pinky_knuckle.y

    def thumb_down(self) -> bool:
        return self.thumb_tip.y > self.thumb_knuckle.y

    def index_down(self) -> bool:
        return self.index_tip.y > self.index_knuckle.y

    def middle_down(self) -> bool:
        return self.middle_tip.y > self.middle_knuckle.y

    def ring_down(self) -> bool:
        return self.ring_tip.y > self.ring_knuckle.y

    def pinky_down(self) -> bool:
        return self.pinky_tip.y > self.pinky_knuckle.y
    # endregion fingers

    def circle_tip(self, screen: Screen, landmark, color) -> None:
        """
        Draw a circle around a particular landmark point
        """
        center = (int(landmark.x * screen.frame_width), int(landmark.y * screen.frame_height))
        cv2.circle(screen.frame, center, 25, color, cv2.FILLED)
        
    def landmark_coordinates(self) -> Tuple[float, float, float, float]:
        """
        Traverse all landmark coordinates to find top-left and bottom-right ones
        to be able to draw a bounding box. Coordinates are in 0-1 range.
        """
        x = []
        y = []
        for _, landmark in enumerate(self.hand_landmarks.landmark):
            x.append(landmark.x)
            y.append(landmark.y)

        top_left_x = np.min(x)
        top_left_y = np.min(y)
        bottom_right_x = np.max(x)
        bottom_right_y = np.max(y)

        return (top_left_x, top_left_y, bottom_right_x, bottom_right_y)
