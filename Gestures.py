from typing import Tuple
from Events.LeftHandEvents import HandSpawnedCursor, LeftThumbTouchedIndex, LeftThumbTouchedMiddle, LeftThumbTouchedPinky, LeftThumbTouchedRing
from Events.RightHandEvents import RightHandGrab, RightHandPointingOne, RightHandPointingThree, RightHandPointingTwo, RightThumbTouchedIndex, RightThumbTouchedMiddle, RightThumbTouchedPinky, RightThumbTouchedRing
from Hand import Hand
from cursor_controller import CursorController
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

    def __init__(self, frame, cursor_controller: CursorController) -> None:
        self.frame = frame
        self.cursor_controller = cursor_controller

        self.smoothen = SmoothPoints()


    def load(self, left_hand, right_hand):
        if left_hand:
            self.load_left_hand(left_hand)
    
        if right_hand:
            self.load_right_hand(right_hand)
            
        return self

    def load_left_hand(self, hand: Hand) -> None:
        fingers = hand.fingers

        #region cursor
        self.left_hand_up_counter(hand)

        if Gestures.hand_up_counter % 2 == 0:
            Gestures.activate = not Gestures.activate
            Gestures.hand_up_counter -= 1

        self.cursor_controller.draw_when_true(self.frame, Gestures.activate, hand)
        
        if hand and self.cursor_controller.drawn:
            (mouse_x, mouse_y) = self.cursor_controller.move_mouse_within_rectangle(self.frame, fingers.index_bottom.x, fingers.index_bottom.y)
    
            self.smoothen.update(mouse_x, mouse_y)
            smooth_x, smooth_y = self.smoothen.smooth()

            HandSpawnedCursor.dispatch(Gestures.activate, x=smooth_x, y=smooth_y)
        #endregion cursor
    
        dx, dy = self.calculate_distance_from_point(hand)    
        LeftThumbTouchedMiddle.dispatch(hand.touching(fingers.thumb_tip, fingers.middle_tip), x=dx, y=dy)

        LeftThumbTouchedIndex.dispatch(hand.touching(fingers.thumb_tip, fingers.index_tip))
        LeftThumbTouchedRing.dispatch(hand.touching(fingers.thumb_tip, fingers.ring_tip))
        LeftThumbTouchedPinky.dispatch(hand.touching(fingers.thumb_tip, fingers.pinky_tip))

    def left_hand_up_counter(self, hand: Hand) -> None:
        if hand.up():
            if not Gestures.left_hand_up:
                Gestures.left_hand_up = True
                Gestures.hand_up_counter += 1
        elif hand.grab():
            if Gestures.left_hand_up:
                Gestures.left_hand_up = False

    def load_right_hand(self, hand: Hand) -> None:
        self.right_hand_up = hand.up()

        fingers = hand.fingers
        RightThumbTouchedIndex.dispatch(hand.touching(fingers.thumb_tip, fingers.index_tip))
        RightThumbTouchedMiddle.dispatch(hand.touching(fingers.thumb_tip, fingers.middle_tip))
        RightThumbTouchedPinky.dispatch(hand.touching(fingers.thumb_tip, fingers.pinky_tip))
        RightThumbTouchedRing.dispatch(hand.touching(fingers.thumb_tip, fingers.ring_tip))

        RightHandPointingOne.dispatch(hand.one())
        RightHandPointingTwo.dispatch(hand.two())
        RightHandPointingThree.dispatch(hand.three())

        RightHandGrab.dispatch(hand.grab())


    def calculate_distance_from_point(self, hand: Hand) -> Tuple[float, float]:
        fingers = hand.fingers

        if not hand.touching(fingers.thumb_tip, fingers.middle_tip):
            Gestures.left_midpoint = None
            return None, None

        height, width, _ = self.frame.shape
        cx, cy = int(fingers.middle_tip.x * width), int(fingers.middle_tip.y * height)
        
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



class SmoothPoints:

    max_points = 5
    buffer = []
    total_x = 0
    total_y = 0

    def update(self, x, y):
        for index, value in enumerate(SmoothPoints.buffer):
            print(f"Index: {index}, Value: {value}")

        SmoothPoints.buffer.append((x, y))
        SmoothPoints.total_x += x
        SmoothPoints.total_y += y

        if len(self.buffer) >= SmoothPoints.max_points:
            old_x, old_y = SmoothPoints.buffer[0]
            SmoothPoints.total_x -= old_x
            SmoothPoints.total_y -= old_y

            del SmoothPoints.buffer[0]



    def smooth(self):
        smooth_x = SmoothPoints.total_x / min(len(SmoothPoints.buffer), SmoothPoints.max_points)
        smooth_y = SmoothPoints.total_y / min(len(SmoothPoints.buffer), SmoothPoints.max_points)

        return smooth_x, smooth_y
