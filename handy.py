import cv2
import mediapipe as mp
import pyautogui
from finger import Finger

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

prev_frame = None
swipe_direction = None

# Define the threshold for detecting a swipe gesture
swipe_threshold = 50


cap = cv2.VideoCapture(0)
with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        frame.flags.writeable = False
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame)

        # Draw the hand annotations on the image.
        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

                fingers = Finger(hand_landmarks)
                fingers.bounding_box(frame)
                
                if fingers.three_fingers_up():
                    cv2.putText(frame, "3 FINGERS UP", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                    # pyautogui.hotkey('ctrl', 'left')
                    

        # Flip the image horizontally for a selfie-view display.
        #cv2.imshow('MediaPipe Hands', image)
        cv2.imshow('MediaPipe Hands', cv2.flip(frame, 1))

        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
