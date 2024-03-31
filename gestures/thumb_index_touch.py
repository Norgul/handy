from hand import Hand

class ThumbIndexTouch:
    @staticmethod
    def execute(frame, hand: Hand):
        # Need to ensure other fingers are up so it doesn't confuse fist with 
        return hand.touching(frame, hand.fingers.thumb_tip, hand.fingers.index_tip) \
            and not hand.fist()