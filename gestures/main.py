from abc import ABC, abstractmethod
from hand import Hand
from input_controller import InputController
from gestures.thumb_index_touch import LeftThumbIndexTouch, RightThumbIndexTouch
from gestures.thumb_middle_touch import LeftThumbMiddleTouch, RightThumbMiddleTouch
from gestures.thumb_pinky_touch import LeftThumbPinkyTouch, RightThumbPinkyTouch
from gestures.thumb_ring_touch import LeftThumbRingTouch, RightThumbRingTouch

class Gestures(ABC):
    def __init__(self, frame, hand: Hand, input_controller: InputController) -> None:
        self.frame = frame
        self.hand = hand
        self.input_controller = input_controller

        self.execute_gestures()
    
    @abstractmethod
    def execute_gestures(self):
        pass

class LeftGestures(Gestures):
    def execute_gestures(self):
        LeftThumbIndexTouch.execute(self.frame, self.hand, self.input_controller)
        LeftThumbMiddleTouch.execute(self.frame, self.hand, self.input_controller)
        LeftThumbPinkyTouch.execute(self.frame, self.hand, self.input_controller)
        LeftThumbRingTouch.execute(self.frame, self.hand, self.input_controller)

class RightGestures(Gestures):
    def execute_gestures(self):
        RightThumbIndexTouch.execute(self.frame, self.hand, self.input_controller)
        RightThumbMiddleTouch.execute(self.frame, self.hand, self.input_controller)
        RightThumbPinkyTouch.execute(self.frame, self.hand, self.input_controller)
        RightThumbRingTouch.execute(self.frame, self.hand, self.input_controller)