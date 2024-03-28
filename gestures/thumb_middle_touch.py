from input_controller import InputController
from hand import Hand

class ThumbMiddleTouch:
    shift_pressed = False
    left_clicked = False
    
    @staticmethod
    def execute(frame, hand: Hand, input_controller: InputController):
        raise NotImplementedError("Subclasses must implement interact method")

class LeftThumbMiddleTouch(ThumbMiddleTouch):
    @staticmethod
    def execute(frame, hand: Hand, input_controller: InputController):
        if not hand:
            return

        fingers = hand.fingers
        
        if hand.touching(frame, fingers.middle_tip, fingers.thumb_tip):
            if not ThumbMiddleTouch.left_clicked:
                print("Left middle touch")
                # input_controller.mouse.click(input_controller.button.left)
                # ThumbMiddleTouch.left_clicked = True
        else:
            if ThumbMiddleTouch.left_clicked:
                print("Left middle release")
                # ThumbMiddleTouch.left_clicked = False

class RightThumbMiddleTouch(ThumbMiddleTouch):
    @staticmethod
    def execute(frame, hand: Hand, input_controller: InputController):
        if not hand:
            return

        fingers = hand.fingers
        
        if hand.touching(frame, fingers.middle_tip, fingers.thumb_tip):
            if not ThumbMiddleTouch.shift_pressed:
                print("Right middle touch")
                # input_controller.keyboard.press(input_controller.key.shift)
                # ThumbMiddleTouch.shift_pressed = True
        else:
            if ThumbMiddleTouch.shift_pressed:
                print("Right middle release")
                # input_controller.keyboard.release(input_controller.key.shift)
                # ThumbMiddleTouch.shift_pressed = False
