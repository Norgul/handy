import cv2
from mp_hands import MpHands
from input_controller import InputController

mp_hands = MpHands()
cap = cv2.VideoCapture(0)
input_controller = InputController()

while True:
    success, frame = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue
    
    # Flip the image horizontally for a selfie-view display.
    frame = cv2.flip(frame, 1)    
    
    mp_hands.process(frame, input_controller)
       
    cv2.imshow('MediaPipe Hands', frame)
    # Use Esc to exit
    if cv2.waitKey(5) & 0xFF == 27:
        break
    
cap.release()
