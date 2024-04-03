import cv2
from EventManager import EventManager
from mp_hands import MpHands
from input_controller import InputController
from cursor_controller import CursorController
from Gestures import Gestures

event_manager = EventManager()
event_manager.register().register_inverse_events()

mp_hands = MpHands()
cap = cv2.VideoCapture(0)
input_controller = InputController()
cursor_controller = CursorController()

left_hand_size = None

while True:
    success, frame = cap.read()
    if not success:
        continue
    
    # Flip the image horizontally for a selfie-view display.
    frame = cv2.flip(frame, 1)    
    
    left_hand, right_hand = mp_hands.extract_hands(frame)
    
    Gestures(frame, left_hand, right_hand, input_controller, cursor_controller).load()
    
    cv2.imshow('MediaPipe Hands', frame)
    # Use Esc to exit
    if cv2.waitKey(5) & 0xFF == 27:
        break
    
cap.release()
