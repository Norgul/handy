class Fingers:
    def __init__(self, hand_landmarks):
        self.hand_landmarks = hand_landmarks

        self.thumb_tip = hand_landmarks.landmark[4]
        self.thumb_knuckle = hand_landmarks.landmark[2]

        self.index_tip = hand_landmarks.landmark[8]
        self.index_knuckle = hand_landmarks.landmark[6]

        self.middle_tip = hand_landmarks.landmark[12]
        self.middle_knuckle = hand_landmarks.landmark[10]

        self.ring_tip = hand_landmarks.landmark[16]
        self.ring_knuckle = hand_landmarks.landmark[14]

        self.pinky_tip = hand_landmarks.landmark[20]
        self.pinky_knuckle = hand_landmarks.landmark[18]

        self.wrist = hand_landmarks.landmark[0]

    # region fingers
    def thumb_up(self) -> bool:
        return self.thumb_tip.y < self.thumb_knuckle.y

    def index_up(self) -> bool:
        return self.index_tip.y < self.index_knuckle.y

    def middle_up(self) -> bool:
        return self.middle_tip.y < self.middle_knuckle.y

    def ring_up(self) -> bool:
        return self.ring_tip.y < self.ring_knuckle.y

    def pinky_up(self) -> bool:
        return self.pinky_tip.y < self.pinky_knuckle.y

    def thumb_down(self) -> bool:
        return self.thumb_tip.y > self.thumb_knuckle.y

    def index_down(self) -> bool:
        return self.index_tip.y > self.index_knuckle.y

    def middle_down(self) -> bool:
        return self.middle_tip.y > self.middle_knuckle.y

    def ring_down(self) -> bool:
        return self.ring_tip.y > self.ring_knuckle.y

    def pinky_down(self) -> bool:
        return self.pinky_tip.y > self.pinky_knuckle.y
    # endregion fingers
