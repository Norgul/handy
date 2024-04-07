from typing import Tuple, Union
import mediapipe as mp
from Models.Fingers import Fingers
from Models.Hand import *
import cv2

from Screen import Screen

class MpHands:
    def __init__(self) -> None:
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands
        
        static_image_mode = False
        num_hands = 2
        self.hands = self.mp_hands.Hands(static_image_mode, num_hands)


    def extract_hands(self, screen: Screen) -> Tuple[LeftHand, RightHand]:
        results = self.hands.process(cv2.cvtColor(screen.frame, cv2.COLOR_BGR2RGB))
        
        if results.multi_hand_landmarks is None:
            return None, None
        
        left_landmarks, right_landmarks = self.split_landmarks_by_hand(results)
        
        left_hand = self.init_hand(screen, left_landmarks, (0,0,255), True)
        right_hand = self.init_hand(screen, right_landmarks, (255,0,0), False)
        
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


    def init_hand(self, screen: Screen, landmarks, color, is_left: bool) -> Union[Hand, None]:
        if not landmarks:
            return None

        if is_left:
            hand = LeftHand(screen, self.hands, landmarks)
        else:
            hand = RightHand(screen, self.hands, landmarks)

        top_left_x, _, bottom_right_x, _ = hand.bounding_box()
        
        # Prevent registering small random objects as hands
        if bottom_right_x - top_left_x < 100:
            return None
        
        # Hand indicator at wrist position
        hand.fingers.circle_tip(screen, hand.fingers.wrist, color)

        self.draw_finger_points(screen, hand.fingers)
        self.draw_landmarks(screen.frame, landmarks)
        
        return hand

    def draw_finger_points(self, screen: Screen, fingers: Fingers) -> None:
        fingers.circle_tip(screen, fingers.thumb_tip, (204, 204, 0))
        fingers.circle_tip(screen, fingers.index_tip, (147, 20, 255))
        fingers.circle_tip(screen, fingers.middle_tip, (0, 255, 255))
        fingers.circle_tip(screen, fingers.ring_tip, (0, 255, 0))
        fingers.circle_tip(screen, fingers.pinky_tip, (255, 0, 0))
    

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

