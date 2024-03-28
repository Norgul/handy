import mediapipe as mp
from hand import Hand
from cv_helpers import *
import cv2
import pyautogui

class MpHands:
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands
        
        static_image_mode = False
        num_hands = 2
        
        self.hands = self.mp_hands.Hands(static_image_mode, num_hands)

    def draw(self, frame, hand_landmarks):
        """
        Draw points on a found hand
        """
        self.mp_drawing.draw_landmarks(
            frame,
            hand_landmarks,
            self.mp_hands.HAND_CONNECTIONS,
            self.mp_drawing_styles.get_default_hand_landmarks_style(),
            self.mp_drawing_styles.get_default_hand_connections_style())

    def extract_left_right_landmarks(self, frame, results):
        """
        Split landmarks by detected hand
        """
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

    def init_hand(self, frame, landmarks, color):
                   
        if not landmarks:
            return None
                         
        # Draw left/right hand indicator circles
        # Additional points...5, 6, 7, 8
        for ind in [0]:
            landmark = landmarks.landmark[ind]
            center = (int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0]))
            cv2.circle(frame, center, 15, color, 5)

        hand = Hand(self.hands, landmarks)
        hand.bounding_box(frame)
        
        fingers = hand.fingers
        # Draw finger points
        fingers.circle_tip(frame, fingers.thumb_tip, (204, 204, 0))
        fingers.circle_tip(frame, fingers.index_tip, (147, 20, 255))
        fingers.circle_tip(frame, fingers.middle_tip, (0, 255, 255))
        fingers.circle_tip(frame, fingers.ring_tip, (0, 255, 0))
        fingers.circle_tip(frame, fingers.pinky_tip, (255, 0, 0))
        
        return hand
        
    def process(self, frame):
        results = self.hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        if results.multi_hand_landmarks is None:
            return
        
        left_landmarks, right_landmarks = self.extract_left_right_landmarks(frame, results)
        
        # if left_landmarks:
        self.draw(frame, left_landmarks)
        self.draw(frame, right_landmarks)
        
        left_hand = self.init_hand(frame, left_landmarks, (0,0,255))
        right_hand = self.init_hand(frame, right_landmarks, (255,0,0))
        
        
        if left_hand:
            left_fingers = left_hand.fingers
            
            if left_hand.three_fingers_up():
                print_on_frame(frame, "3 left FINGERS UP")
                pyautogui.hotkey('...')

            if left_hand.touching(frame, left_fingers.index_tip, left_fingers.thumb_tip):
                print_on_frame(frame, "Index and thumb touching")
                pyautogui.hotkey('...')
                
                
            if left_hand.touching(frame, left_fingers.middle_tip, left_fingers.thumb_tip):
                print_on_frame(frame, "Middle and thumb touching")
                pyautogui.hotkey('...')
                
                

        if right_hand:
            right_fingers = right_hand.fingers

            if right_hand.three_fingers_up():
                print_on_frame(frame, "3 right FINGERS UP", True)
                
                
            if right_hand.touching(frame, right_fingers.index_tip, right_fingers.thumb_tip):
                print_on_frame(frame, "Index and thumb touching", True)
                
                
            if right_hand.touching(frame, right_fingers.middle_tip, right_fingers.thumb_tip):
                print_on_frame(frame, "Middle and thumb touching", True)
                
                
        

