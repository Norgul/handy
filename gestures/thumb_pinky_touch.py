from input_controller import InputController
from hand import Hand

class ThumbPinkyTouch:
    shift_pressed = False
    left_clicked = False
    
    @staticmethod
    def execute(frame, hand: Hand, input_controller: InputController):
        raise NotImplementedError("Subclasses must implement interact method")

class LeftThumbPinkyTouch(ThumbPinkyTouch):
    @staticmethod
    def execute(frame, hand: Hand, input_controller: InputController):
        if not hand:
            return

        fingers = hand.fingers
        
        if hand.touching(frame, fingers.pinky_tip, fingers.thumb_tip):
            if not ThumbPinkyTouch.left_clicked:
                print("Left pinky touch")
                # input_controller.mouse.click(input_controller.button.left)
                # ThumbMiddleTouch.left_clicked = True
        else:
            if ThumbPinkyTouch.left_clicked:
                print("Left pinky release")
                # ThumbMiddleTouch.left_clicked = False

class RightThumbPinkyTouch(ThumbPinkyTouch):
    @staticmethod
    def execute(frame, hand: Hand, input_controller: InputController):
        if not hand:
            return

        fingers = hand.fingers
        
        if hand.touching(frame, fingers.pinky_tip, fingers.thumb_tip):
            if not ThumbPinkyTouch.shift_pressed:
                print("Right pinky touch")
                # input_controller.keyboard.press(input_controller.key.shift)
                # ThumbMiddleTouch.shift_pressed = True
        else:
            if ThumbPinkyTouch.shift_pressed:
                print("Right pinky release")
                # input_controller.keyboard.release(input_controller.key.shift)
                # ThumbMiddleTouch.shift_pressed = False
