from hand import Hand

class ThumbRingTouch:
    @staticmethod
    def execute(frame, hand: Hand):
        return hand.touching(frame, hand.fingers.thumb_tip, hand.fingers.ring_tip)
