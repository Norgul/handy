from input_controller import InputController
from hand import Hand

class ThumbRingTouch:
    shift_pressed = False
    left_clicked = False
    
    @staticmethod
    def execute(frame, hand: Hand, input_controller: InputController):
        raise NotImplementedError("Subclasses must implement interact method")

class LeftThumbRingTouch(ThumbRingTouch):
    @staticmethod
    def execute(frame, hand: Hand, input_controller: InputController):
        if not hand:
            return

        fingers = hand.fingers
        
        if hand.touching(frame, fingers.ring_tip, fingers.thumb_tip):
            if not ThumbRingTouch.left_clicked:
                print("Left ring touch")
                # input_controller.mouse.click(input_controller.button.left)
                # ThumbMiddleTouch.left_clicked = True
        else:
            if ThumbRingTouch.left_clicked:
                print("Left ring release")
                # ThumbMiddleTouch.left_clicked = False

class RightThumbRingTouch(ThumbRingTouch):
    @staticmethod
    def execute(frame, hand: Hand, input_controller: InputController):
        if not hand:
            return

        fingers = hand.fingers
        
        if hand.touching(frame, fingers.ring_tip, fingers.thumb_tip):
            if not ThumbRingTouch.shift_pressed:
                print("Right ring touch")
                # input_controller.keyboard.press(input_controller.key.shift)
                # ThumbMiddleTouch.shift_pressed = True
        else:
            if ThumbRingTouch.shift_pressed:
                print("Right ring release")
                # input_controller.keyboard.release(input_controller.key.shift)
                # ThumbMiddleTouch.shift_pressed = False
