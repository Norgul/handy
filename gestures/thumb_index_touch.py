from hand import Hand

class ThumbIndexTouch:
    @staticmethod
    def execute(frame, hand: Hand):
        return hand.touching(frame, hand.fingers.thumb_tip, hand.fingers.index_tip)