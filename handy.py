import cv2
import mediapipe as mp
import pyautogui
import time
from fingers import Fingers

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

swipe_left = False
swipe_right = False

going_left = 0;
going_right = 0;

previous_point = 0;

cap = cv2.VideoCapture(0)
with mp_hands.Hands(model_complexity=0,min_detection_confidence=0.5,min_tracking_confidence=0.5) as hands:

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

                fingers = Fingers(hand_landmarks)
                fingers.bounding_box(frame)


                if fingers.left():
                    if fingers.three_fingers_up():
                        cv2.putText(frame, "3 left FINGERS UP", (10, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                        if not swipe_left:
                            swipe_left = True
                            #pyautogui.hotkey('ctrl', 'left')

                        continue

                    swipe_left = False

                if fingers.right():
                    if fingers.three_fingers_up():
                        cv2.putText(frame, "3 right FINGERS UP", (10, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                        if not swipe_right:
                            swipe_right = True
                            #pyautogui.hotkey('ctrl', 'right')

                        continue

                    swipe_right = False




        # Flip the image horizontally for a selfie-view display.
        cv2.imshow('MediaPipe Hands', frame)
        #cv2.imshow('MediaPipe Hands', cv2.flip(frame, 1))

        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
