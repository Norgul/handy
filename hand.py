from fingers import Fingers
import numpy as np
import cv2
import math

class Hand:
    def __init__(self, mp_hands, landmarks, is_left = True):
        
        self.is_left = is_left
        self.is_right = not is_left
        
        self.mp_hands = mp_hands
        self.fingers = Fingers(landmarks)
        
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

    def touching(self, frame, finger1, finger2, radius=30):
        """
        Check if two landmark points are touching with a given radius
        """
        # Scale the landmark points to match the frame dimensions
        x1, y1 = finger1.x * frame.shape[1], finger1.y * frame.shape[0]
        x2, y2 = finger2.x * frame.shape[1], finger2.y * frame.shape[0]

        # Calculate the distance between the two points
        dist = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
        # If the distance is less than or equal to the sum of their radii, they are touching
        return dist <= (2 * radius)