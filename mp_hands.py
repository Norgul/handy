from typing import Tuple, Union
import mediapipe as mp
from Hand import Hand
import numpy as np
import cv2

class MpHands:
    def __init__(self) -> None:
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands
        
        static_image_mode = False
        num_hands = 2
        self.hands = self.mp_hands.Hands(static_image_mode, num_hands)


    def extract_hands(self, frame: np.array) -> Tuple[Hand, Hand]:
        
        results = self.hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        if results.multi_hand_landmarks is None:
            return None, None
        
        left_landmarks, right_landmarks = self.split_landmarks_by_hand(results)
        
        left_hand = self.init_hand(frame, left_landmarks, (0,0,255), True)
        right_hand = self.init_hand(frame, right_landmarks, (255,0,0), False)
        
        return left_hand, right_hand
    

    def split_landmarks_by_hand(self, results) -> Tuple[list, list]:
        if results.multi_hand_landmarks is None:
            return [], []

        left_landmarks = []
        right_landmarks = []
    
        for hand, landmark in zip(results.multi_handedness, results.multi_hand_landmarks):
            hand_type = hand.classification[0].label

            if hand_type == "Left":
                left_landmarks = landmark
            elif hand_type == "Right":
                right_landmarks = landmark

        return left_landmarks, right_landmarks


    def init_hand(self, frame, landmarks, color, is_left) -> Union[Hand, None]:
        if not landmarks:
            return None

        hand = Hand(frame, self.hands, landmarks, is_left)
        top_left_x, _, bottom_right_x, _ = hand.bounding_box()
        
        # Prevent registering small random objects as hands
        if bottom_right_x - top_left_x < 100:
            return None
        
        self.draw_hand_indicator_circle(frame, landmarks, color)
        self.draw_finger_points(frame, hand.fingers)
        self.draw_landmarks(frame, landmarks)
        
        return hand
    

    def draw_hand_indicator_circle(self, frame, landmarks, color) -> None:
        landmark = landmarks.landmark[0]
        center = (int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0]))
        cv2.circle(frame, center, 15, color, 5)
    

    def draw_finger_points(self, frame, fingers) -> None:
        fingers.circle_tip(frame, fingers.thumb_tip, (204, 204, 0))
        fingers.circle_tip(frame, fingers.index_tip, (147, 20, 255))
        fingers.circle_tip(frame, fingers.middle_tip, (0, 255, 255))
        fingers.circle_tip(frame, fingers.ring_tip, (0, 255, 0))
        fingers.circle_tip(frame, fingers.pinky_tip, (255, 0, 0))
    

    def draw_landmarks(self, frame, hand_landmarks) -> None:
        """
        Draw points on a found hand
        """
        self.mp_drawing.draw_landmarks(
            frame,
            hand_landmarks,
            self.mp_hands.HAND_CONNECTIONS,
            self.mp_drawing_styles.get_default_hand_landmarks_style(),
            self.mp_drawing_styles.get_default_hand_connections_style())

