from typing import Tuple
from Fingers import Fingers
import numpy as np
import math

class Hand:
    def __init__(self, frame, mp_hands, landmarks, is_left = True) -> None:
        self.frame = frame
        
        self.mp_hands = mp_hands
        self.fingers = Fingers(landmarks)
        
        self.is_left = is_left
        self.is_right = not is_left
        
    def bounding_box(self) -> Tuple[int, int, int, int]:
        # Get the x and y coordinates of the hand landmarks
        x = []
        y = []
        for id, landmark in enumerate(self.fingers.hand_landmarks.landmark):
            x.append(landmark.x)
            y.append(landmark.y)

        # Calculate the bounding box of the hand
        top_left_x = np.min(x)
        top_left_y = np.min(y)
        bottom_right_x = np.max(x)
        bottom_right_y = np.max(y)

        bounding_box = (top_left_x, top_left_y, bottom_right_x - top_left_x, bottom_right_y - top_left_y)

        top_left_x, top_left_y, width, height = bounding_box
        bottom_right_x = top_left_x + width
        bottom_right_y = top_left_y + height

        # Adapt 0-1 from mediapipe to actual frame dimension
        frame_height, frame_width, _ = self.frame.shape
        top_left_x, top_left_y, bottom_right_x, bottom_right_y = [top_left_x * frame_width, top_left_y *
                                  frame_height, bottom_right_x * frame_width, bottom_right_y * frame_height]
        top_left_x, top_left_y, bottom_right_x, bottom_right_y = map(int, [top_left_x, top_left_y, bottom_right_x, bottom_right_y])

        # cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
        
        return top_left_x, top_left_y, bottom_right_x, bottom_right_y

    def center(self) -> Tuple[float, float]:
        
        top_left_x, top_left_y, bottom_right_x, bottom_right_y = self.bounding_box()
        
        center_x = (top_left_x + bottom_right_x) / 2
        center_y = (top_left_y + bottom_right_y) / 2
        
        return center_x, center_y

    def size(self) -> float:
        
        top_left_x, top_left_y, bottom_right_x, bottom_right_y = self.bounding_box()
        
        width = abs(bottom_right_x - top_left_x)
        height = abs(bottom_right_y - top_left_y)
        size = width * height
        
        return size

    def up(self) -> bool:
        return self.fingers.thumb_up() \
            and self.fingers.index_up() \
            and self.fingers.middle_up() \
            and self.fingers.ring_up() \
            and self.fingers.pinky_up()

    def grab(self) -> bool:
        return self.fingers.thumb_up() \
            and self.fingers.index_down() \
            and self.fingers.middle_down() \
            and self.fingers.ring_down() \
            and self.fingers.pinky_down()
            
    def one(self) -> bool:
        return self.fingers.thumb_up() \
            and self.fingers.index_up() \
            and self.fingers.middle_down() \
            and self.fingers.ring_down() \
            and self.fingers.pinky_down()
    
    def two(self) -> bool:
        return self.fingers.thumb_up() \
            and self.fingers.index_up() \
            and self.fingers.middle_up() \
            and self.fingers.ring_down() \
            and self.fingers.pinky_down()
    
    def three(self) -> bool:
        return self.fingers.thumb_up() \
            and self.fingers.index_up() \
            and self.fingers.middle_up() \
            and self.fingers.ring_up() \
            and self.fingers.pinky_down()
    

    def touching(self, finger1, finger2, radius=30) -> bool:
        """
        Check if two landmark points are touching with a given radius
        """
        # Scale the landmark points to match the frame dimensions
        x1, y1 = finger1.x * self.frame.shape[1], finger1.y * self.frame.shape[0]
        x2, y2 = finger2.x * self.frame.shape[1], finger2.y * self.frame.shape[0]

        # Calculate the distance between the two points
        dist = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
        
        # If the distance is less than or equal to the sum of their radii, they are touching
        # Also, need to ensure other fingers are up so it doesn't confuse fist with it
        return dist <= (2 * radius) and not self.grab()