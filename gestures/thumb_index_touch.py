from input_controller import InputController
from hand import Hand

class ThumbIndexTouch:
    shift_pressed = False
    left_clicked = False
    
    @staticmethod
    def execute(frame, hand: Hand, input_controller: InputController):
        raise NotImplementedError("Subclasses must implement interact method")

class LeftThumbIndexTouch(ThumbIndexTouch):
    @staticmethod
    def execute(frame, hand: Hand, input_controller: InputController):
        if not hand:
            return

        fingers = hand.fingers
        
        if hand.touching(frame, fingers.index_tip, fingers.thumb_tip):
            if not ThumbIndexTouch.left_clicked:
                print("Left clicked")
                input_controller.mouse.click(input_controller.button.left)
                ThumbIndexTouch.left_clicked = True
        else:
            if ThumbIndexTouch.left_clicked:
                print("Released click")
                ThumbIndexTouch.left_clicked = False

class RightThumbIndexTouch(ThumbIndexTouch):
    @staticmethod
    def execute(frame, hand: Hand, input_controller: InputController):
        if not hand:
            return

        fingers = hand.fingers
        
        if hand.touching(frame, fingers.index_tip, fingers.thumb_tip):
            if not ThumbIndexTouch.shift_pressed:
                print("Pressed shift")
                input_controller.keyboard.press(input_controller.key.shift)
                ThumbIndexTouch.shift_pressed = True
        else:
            if ThumbIndexTouch.shift_pressed:
                print("Released shift")
                input_controller.keyboard.release(input_controller.key.shift)
                ThumbIndexTouch.shift_pressed = False
