from hand import Hand
from input_controller import InputController
from gestures.thumb_index_touch import ThumbIndexTouch
from gestures.thumb_middle_touch import ThumbMiddleTouch
from gestures.thumb_pinky_touch import ThumbPinkyTouch
from gestures.thumb_ring_touch import ThumbRingTouch

class Gestures():
    def __init__(self, frame, left_hand: Hand, right_hand: Hand, input_controller: InputController) -> None:
        self.frame = frame
        self.left_hand = left_hand
        self.right_hand = right_hand
        self.input_controller = input_controller
        
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
            self.left_thumb_index_touch = ThumbIndexTouch.execute(self.frame, self.left_hand)
            self.left_thumb_middle_touch = ThumbMiddleTouch.execute(self.frame, self.left_hand)
            self.left_thumb_pinky_touch = ThumbPinkyTouch.execute(self.frame, self.left_hand)
            self.left_thumb_ring_touch = ThumbRingTouch.execute(self.frame, self.left_hand)
            
        if self.right_hand:
            self.right_thumb_index_touch = ThumbIndexTouch.execute(self.frame, self.right_hand)
            self.right_thumb_middle_touch = ThumbMiddleTouch.execute(self.frame, self.right_hand)
            self.right_thumb_pinky_touch = ThumbPinkyTouch.execute(self.frame, self.right_hand)
            self.right_thumb_ring_touch = ThumbRingTouch.execute(self.frame, self.right_hand)
            
        return self