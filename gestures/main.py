from hand import Hand
from input_controller import InputController
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController

from gestures.thumb_index_touch import ThumbIndexTouch
from gestures.thumb_middle_touch import ThumbMiddleTouch
from gestures.thumb_pinky_touch import ThumbPinkyTouch
from gestures.thumb_ring_touch import ThumbRingTouch

class Gestures():
    key_states = {}
    key_pressed = False
    mouse_clicked = False
    mouse_click_hold = False

    hand_up_counter = 0
    left_hand_up = False
    activate = False

    def __init__(self, frame, left_hand: Hand, right_hand: Hand, input_controller: InputController) -> None:
        self.frame = frame
        self.left_hand = left_hand
        self.right_hand = right_hand
        self.input_controller = input_controller

        self.left_hand_up = False
        self.right_hand_up = False

        # region two finger touch
        self.left_thumb_index_touch = False
        self.left_thumb_middle_touch = False
        self.left_thumb_pinky_touch = False
        self.left_thumb_ring_touch = False

        self.right_thumb_index_touch = False
        self.right_thumb_middle_touch = False
        self.right_thumb_pinky_touch = False
        self.right_thumb_ring_touch = False
        # endregion two finger touch

    def load(self):
        if self.left_hand:
            self.left_hand_up = self.left_hand.up()

            self.left_thumb_index_touch = ThumbIndexTouch.execute(self.frame, self.left_hand)
            self.left_thumb_middle_touch = ThumbMiddleTouch.execute(self.frame, self.left_hand)
            self.left_thumb_pinky_touch = ThumbPinkyTouch.execute(self.frame, self.left_hand)
            self.left_thumb_ring_touch = ThumbRingTouch.execute(self.frame, self.left_hand)

        if self.right_hand:
            self.right_hand_up = self.right_hand.up()

            self.right_thumb_index_touch = ThumbIndexTouch.execute(self.frame, self.right_hand)
            self.right_thumb_middle_touch = ThumbMiddleTouch.execute(self.frame, self.right_hand)
            self.right_thumb_pinky_touch = ThumbPinkyTouch.execute(self.frame, self.right_hand)
            self.right_thumb_ring_touch = ThumbRingTouch.execute(self.frame, self.right_hand)

        return self

    @staticmethod
    def press(case, key):
        keyboard = KeyboardController()

        if key not in Gestures.key_states:
            Gestures.key_states[key] = False

        if case:
            if not Gestures.key_states[key]:
                print("Pressed", key)
                keyboard.press(key)
                Gestures.key_states[key] = True
        else:
            if Gestures.key_states[key]:
                print("Released", key)
                keyboard.release(key)
                Gestures.key_states[key] = False

    @staticmethod
    def click(case, button):

        mouse = MouseController()

        if case:
            if not Gestures.mouse_clicked:
                print("Mouse click", button)
                mouse.click(button)
                Gestures.mouse_clicked = True
        else:
            if Gestures.mouse_clicked:
                print("Released click", button)
                Gestures.mouse_clicked = False

    @staticmethod
    def click_hold(case, button):

        mouse = MouseController()

        if case:
            if not Gestures.mouse_click_hold:
                print("Mouse click", button)
                mouse.press(button)
                Gestures.mouse_click_hold = True
        else:
            if Gestures.mouse_click_hold:
                print("Released click", button)
                mouse.release(button)
                Gestures.mouse_click_hold = False


    @staticmethod
    def is_up(hand: Hand):
        if not hand:
            return

        if hand.up():
            if not Gestures.left_hand_up:
                print("Hand up")
                Gestures.left_hand_up = True
                Gestures.hand_up_counter += 1

            if Gestures.hand_up_counter % 2 == 0:
                Gestures.activate = not Gestures.activate
                Gestures.hand_up_counter -= 1
                print("Activate", Gestures.activate)
        elif hand.fist():
            if Gestures.left_hand_up:
                print("Hand down")
                Gestures.left_hand_up = False

