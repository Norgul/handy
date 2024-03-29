from hand import Hand

class ThumbMiddleTouch:
    @staticmethod
    def execute(frame, hand: Hand):
        return hand.touching(frame, hand.fingers.thumb_tip, hand.fingers.middle_tip)
