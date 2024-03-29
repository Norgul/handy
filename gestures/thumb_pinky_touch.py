from hand import Hand

class ThumbPinkyTouch:
    @staticmethod
    def execute(frame, hand: Hand):
        return hand.touching(frame, hand.fingers.thumb_tip, hand.fingers.pinky_tip)
