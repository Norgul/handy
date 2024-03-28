from fingers import Fingers
import numpy as np
import cv2

class Hand:
    def __init__(self, mp_hands, fingers: Fingers):
        self.mp_hands = mp_hands
        self.fingers = fingers
        
    def bounding_box(self, frame):

        # Get the x and y coordinates of the hand landmarks
        x = []
        y = []
        for id, landmark in enumerate(self.fingers.hand_landmarks.landmark):
            x.append(landmark.x)
            y.append(landmark.y)

        # Calculate the bounding box of the hand
        xmin = np.min(x)
        ymin = np.min(y)
        xmax = np.max(x)
        ymax = np.max(y)

        bounding_box = (xmin, ymin, xmax - xmin, ymax - ymin)

        xmin, ymin, width, height = bounding_box
        xmax = xmin + width
        ymax = ymin + height

        # Adapt 0-1 from mediapipe to actual frame dimension
        frame_height, frame_width, _ = frame.shape
        xmin, ymin, xmax, ymax = [xmin * frame_width, ymin *
                                  frame_height, xmax * frame_width, ymax * frame_height]
        xmin, ymin, xmax, ymax = map(int, [xmin, ymin, xmax, ymax])

        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)


    def three_fingers_up(self) -> bool:
        return self.fingers.thumb_up() and self.fingers.index_up() and self.fingers.middle_up() and self.fingers.ring_down() and self.fingers.pinky_down()
