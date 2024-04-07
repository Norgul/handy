from Events.LeftHandEvents import CursorActivated, LeftThumbTouchedIndex, LeftThumbTouchedMiddle, LeftThumbTouchedPinky, LeftThumbTouchedRing
from Events.RightHandEvents import RightHandGrab, RightHandPointingOne, RightHandPointingThree, RightHandPointingTwo, RightThumbTouchedIndex, RightThumbTouchedMiddle, RightThumbTouchedPinky, RightThumbTouchedRing
from Hand import Hand

class Gestures():
    def __init__(self, frame) -> None:
        self.frame = frame

    def load(self, left_hand, right_hand):
        if left_hand:
            self.load_left_hand(left_hand)
    
        if right_hand:
            self.load_right_hand(right_hand)
            
        return self

    def load_left_hand(self, hand: Hand) -> None:
        fingers = hand.fingers

        LeftThumbTouchedIndex.when(hand.touching(fingers.thumb_tip, fingers.index_tip)).dispatch()
        LeftThumbTouchedMiddle.when(hand.touching(fingers.thumb_tip, fingers.middle_tip)).dispatch(frame=self.frame, hand=hand)
        LeftThumbTouchedRing.when(hand.touching(fingers.thumb_tip, fingers.ring_tip)).dispatch()
        LeftThumbTouchedPinky.when(hand.touching(fingers.thumb_tip, fingers.pinky_tip)).dispatch()

        CursorActivated.when(Hand.cursor_activated).dispatch(frame=self.frame, hand=hand)    

    def load_right_hand(self, hand: Hand) -> None:
        self.right_hand_up = hand.up()

        fingers = hand.fingers
        RightThumbTouchedIndex.when(hand.touching(fingers.thumb_tip, fingers.index_tip)).dispatch()
        RightThumbTouchedMiddle.when(hand.touching(fingers.thumb_tip, fingers.middle_tip)).dispatch()
        RightThumbTouchedPinky.when(hand.touching(fingers.thumb_tip, fingers.pinky_tip)).dispatch()
        RightThumbTouchedRing.when(hand.touching(fingers.thumb_tip, fingers.ring_tip)).dispatch()

        RightHandPointingOne.when(hand.one()).dispatch()
        RightHandPointingTwo.when(hand.two()).dispatch()
        RightHandPointingThree.when(hand.three()).dispatch()

        RightHandGrab.when(hand.grab()).dispatch()

