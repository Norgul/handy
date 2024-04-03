from typing import Tuple
from Events.LeftHandEvents import HandSpawnedCursor, LeftThumbTouchedIndex, LeftThumbTouchedMiddle, LeftThumbTouchedPinky, LeftThumbTouchedRing
from Events.RightHandEvents import RightHandGrab, RightHandPointingOne, RightHandPointingThree, RightHandPointingTwo, RightThumbTouchedIndex, RightThumbTouchedMiddle, RightThumbTouchedPinky, RightThumbTouchedRing
from Hand import Hand
from cursor_controller import CursorController
from input_controller import InputController

import math
import cv2

class Gestures():
    key_states = {}
    key_pressed = False
    mouse_clicked = False
    mouse_click_hold = False

    hand_up_counter = 0
    left_hand_up = False
    activate = False
    
    left_midpoint = None


    def __init__(self, frame, left_hand: Hand, right_hand: Hand, input_controller: InputController, cursor_controller: CursorController) -> None:
        self.frame = frame
        self.left_hand = left_hand
        self.right_hand = right_hand

        self.input_controller = input_controller
        self.cursor_controller = cursor_controller

    def load(self):
        self.load_left_hand()
        self.load_right_hand()
            
        return self

    def load_left_hand(self) -> None:
        if not self.left_hand:
            return

        fingers = self.left_hand.fingers

        #region cursor
        self.left_hand_up_counter()

        if Gestures.hand_up_counter % 2 == 0:
            Gestures.activate = not Gestures.activate
            Gestures.hand_up_counter -= 1

        self.cursor_controller.draw_when_true(self.frame, Gestures.activate, self.left_hand)
        
        if self.left_hand and self.cursor_controller.drawn:
            (mouse_x, mouse_y) = self.cursor_controller.move_mouse_within_rectangle(self.frame, fingers.index_bottom.x, fingers.index_bottom.y)
    
            HandSpawnedCursor.dispatch(Gestures.activate, x=mouse_x, y=mouse_y)
        #endregion cursor
    
        dx, dy = self.calculate_distance_from_point(fingers)    
        LeftThumbTouchedMiddle.dispatch(self.left_hand.touching(fingers.thumb_tip, fingers.middle_tip), x=dx, y=dy)

        LeftThumbTouchedIndex.dispatch(self.left_hand.touching(fingers.thumb_tip, fingers.index_tip))
        LeftThumbTouchedRing.dispatch(self.left_hand.touching(fingers.thumb_tip, fingers.ring_tip))
        LeftThumbTouchedPinky.dispatch(self.left_hand.touching(fingers.thumb_tip, fingers.pinky_tip))

    def left_hand_up_counter(self) -> None:
        if self.left_hand.up():
            if not Gestures.left_hand_up:
                Gestures.left_hand_up = True
                Gestures.hand_up_counter += 1
        elif self.left_hand.grab():
            if Gestures.left_hand_up:
                Gestures.left_hand_up = False

    def load_right_hand(self) -> None:
        if not self.right_hand:
            return
    
        self.right_hand_up = self.right_hand.up()

        fingers = self.right_hand.fingers
        RightThumbTouchedIndex.dispatch(self.right_hand.touching(fingers.thumb_tip, fingers.index_tip))
        RightThumbTouchedMiddle.dispatch(self.right_hand.touching(fingers.thumb_tip, fingers.middle_tip))
        RightThumbTouchedPinky.dispatch(self.right_hand.touching(fingers.thumb_tip, fingers.pinky_tip))
        RightThumbTouchedRing.dispatch(self.right_hand.touching(fingers.thumb_tip, fingers.ring_tip))

        RightHandPointingOne.dispatch(self.right_hand.one())
        RightHandPointingTwo.dispatch(self.right_hand.two())
        RightHandPointingThree.dispatch(self.right_hand.three())

        RightHandGrab.dispatch(self.right_hand.grab())


    def calculate_distance_from_point(self, fingers) -> Tuple[float, float]:
        if not self.left_hand.touching(fingers.thumb_tip, fingers.middle_tip):
            Gestures.left_midpoint = None
            return None, None

        h,w,c = self.frame.shape
        cx, cy = int(self.left_hand.fingers.middle_tip.x*w), int(self.left_hand.fingers.middle_tip.y*h)
        
        middle_tip_pixel = (cx, cy)
        
        if not Gestures.left_midpoint:
            Gestures.left_midpoint = (cx, cy)

        cv2.line(self.frame, Gestures.left_midpoint, middle_tip_pixel, (255,255,0), 3)

        # Calculate distance between points
        x_diff_squared = (middle_tip_pixel[0] - Gestures.left_midpoint[0])**2
        y_diff_squared = (middle_tip_pixel[1] - Gestures.left_midpoint[1])**2
        distance = math.sqrt(x_diff_squared + y_diff_squared)
        
        direction_vector = (middle_tip_pixel[0] - Gestures.left_midpoint[0], middle_tip_pixel[1] - Gestures.left_midpoint[1])
    
        # Calculate speed based on distance
        # You can adjust the scaling factor as needed
        speed = (distance/100) * 0.1  # Adjust as needed
        dx = direction_vector[0] * speed
        dy = direction_vector[1] * speed

        return dx, dy
        # HandSpawnedCursor.dispatch(Gestures.activate, x=dx, y=dy)

        # if left_hand and input_controller:
        #     # Convert normalized coordinates to screen coordinates
        #     image_width, image_height = frame.shape[1], frame.shape[0]
        #     x = int(left_hand.fingers.index_tip.x * image_width)
        #     y = int(left_hand.fingers.index_tip.y * image_height)

        #     # Move mouse cursor
        #     self.move_mouse(input_controller, x, y)
