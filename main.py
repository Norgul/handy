import cv2
import mediapipe as mp
import pyautogui
import time
from mp_hands import MpHands

mp_hands = MpHands()
cap = cv2.VideoCapture(0)

while True:
    
    success, frame = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue
    
    # Flip the image horizontally for a selfie-view display.
    frame = cv2.flip(frame, 1)    
    
    mp_hands.process(frame)
       
    cv2.imshow('MediaPipe Hands', frame)
    # Use Esc to exit
    if cv2.waitKey(5) & 0xFF == 27:
        break
    
cap.release()
