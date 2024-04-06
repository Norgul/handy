import cv2
from EventManager import EventManager
from mp_hands import MpHands
from cursor_controller import CursorController
from Gestures import Gestures
from HandSpawnTimeCounter import SpawnTimeCounter

event_manager = EventManager()
event_manager.register().register_inverse_events()

mp_hands = MpHands()
cap = cv2.VideoCapture(0)
cursor_controller = CursorController()

left_timer = SpawnTimeCounter(spawn_timeout=0.3)
right_timer = SpawnTimeCounter(spawn_timeout=0.3)

while True:
    success, frame = cap.read()
    if not success:
        continue
    
    # Flip the image horizontally for a selfie-view display.
    frame = cv2.flip(frame, 1)    

    left_hand, right_hand = mp_hands.extract_hands(frame=frame)

    # Make sure to start monitoring gestures after certain 
    # amount of time hands being present on the screen
    left_hand = left_timer.check(left_hand)
    right_hand = right_timer.check(right_hand)
    
    Gestures(frame, cursor_controller).load(left_hand, right_hand)
    
    cv2.imshow('MediaPipe Hands', frame)
    # Use Esc to exit
    if cv2.waitKey(5) & 0xFF == 27:
        break
    
cap.release()
