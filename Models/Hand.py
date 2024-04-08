from abc import ABC, abstractmethod
from typing import Tuple
from Models.Fingers import Fingers
import math
from Screen import Screen


class Hand(ABC):
    def __init__(self, screen: Screen, mp_hands, landmarks) -> None:
        self.screen = screen

        self.mp_hands = mp_hands
        self.fingers = Fingers(landmarks)

    @abstractmethod
    def facing_forward(self) -> bool:
        """
        Check if hand is directed towards the camera by comparing
        pinky and index finger tip position on x axis
        """
        pass

    @abstractmethod
    def thumb_facing_inwards(self) -> bool:
        pass

    @abstractmethod
    def thumb_facing_outwards(self) -> bool:
        pass

    def bounding_box(self) -> Tuple[int, int, int, int]:
        """
        Hand bounding box dimensions
        """
        top_left_x, top_left_y, bottom_right_x, bottom_right_y = self.fingers.landmark_coordinates()

        top_left_x, top_left_y = self.screen.coordinates_to_frame_pixels(top_left_x, top_left_y)
        bottom_right_x, bottom_right_y = self.screen.coordinates_to_frame_pixels(bottom_right_x, bottom_right_y)

        return top_left_x, top_left_y, bottom_right_x, bottom_right_y

    def center(self) -> Tuple[int, int]:

        top_left_x, top_left_y, bottom_right_x, bottom_right_y = self.bounding_box()

        center_x = (top_left_x + bottom_right_x) / 2
        center_y = (top_left_y + bottom_right_y) / 2

        return int(center_x), int(center_y)

    def bottom_knuckle_center(self) -> Tuple[int, int]:
        center_x = (self.fingers.index_bottom.x + self.fingers.pinky_bottom.x) / 2
        center_y = (self.fingers.index_bottom.y + self.fingers.pinky_bottom.y) / 2

        return self.screen.coordinates_to_frame_pixels(center_x, center_y)

    def size(self) -> float:

        top_left_x, top_left_y, bottom_right_x, bottom_right_y = self.bounding_box()

        width = abs(bottom_right_x - top_left_x)
        height = abs(bottom_right_y - top_left_y)
        size = width * height

        return size

    def up(self) -> bool:
        return (
            self.thumb_facing_outwards()
            and self.fingers.index_up()
            and self.fingers.middle_up()
            and self.fingers.ring_up()
            and self.fingers.pinky_up()
        )

    def grab(self) -> bool:
        return (
            self.thumb_facing_inwards()
            and self.fingers.index_down()
            and self.fingers.middle_down()
            and self.fingers.ring_down()
            and self.fingers.pinky_down()
        )

    def one(self) -> bool:
        return (
            self.thumb_facing_inwards()
            and self.fingers.index_up()
            and self.fingers.middle_down()
            and self.fingers.ring_down()
            and self.fingers.pinky_down()
        )

    def two(self) -> bool:
        return (
            self.thumb_facing_inwards()
            and self.fingers.index_up()
            and self.fingers.middle_up()
            and self.fingers.ring_down()
            and self.fingers.pinky_down()
        )

    def three(self) -> bool:
        return (
            self.thumb_facing_outwards()
            and self.fingers.index_up()
            and self.fingers.middle_up()
            and self.fingers.ring_down()
            and self.fingers.pinky_down()
        )

    def touching(self, finger_landmark1, finger_landmark2, radius=30) -> bool:
        """
        Check if two landmark points are touching with a given radius
        """
        # Scale the landmark points to match the frame dimensions
        x1, y1 = self.screen.coordinates_to_frame_pixels(finger_landmark1.x, finger_landmark1.y)
        x2, y2 = self.screen.coordinates_to_frame_pixels(finger_landmark2.x, finger_landmark2.y)

        # Calculate the distance between the two points
        dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

        # If the distance is less than or equal to the sum of their radii, they are touching
        return dist <= (2 * radius) and not self.grab() and self.uprightish() and self.facing_forward()

    def uprightish(self) -> bool:
        """
        Check if at least 4 fingers are up at any given moment
        """
        count = sum(
            [
                self.fingers.thumb_up(),
                self.fingers.index_up(),
                self.fingers.middle_up(),
                self.fingers.ring_up(),
                self.fingers.pinky_up(),
            ]
        )

        return count >= 4


class LeftHand(Hand):
    was_recently_up: bool = False
    up_counter: int = 0
    cursor_activated: bool = False

    def __init__(self, screen: Screen, mp_hands, landmarks) -> None:
        super().__init__(screen, mp_hands, landmarks)

        self.up_count()
        self.should_activate_cursor()

    def facing_forward(self) -> bool:
        return self.fingers.pinky_tip.x < self.fingers.index_tip.x

    def thumb_facing_inwards(self) -> bool:
        return self.fingers.thumb_pointing_left()

    def thumb_facing_outwards(self) -> bool:
        return not self.thumb_facing_inwards()

    def up_count(self) -> None:
        if self.up():
            if not LeftHand.was_recently_up:
                LeftHand.was_recently_up = True
                LeftHand.up_counter += 1
        elif self.grab():
            if LeftHand.was_recently_up:
                LeftHand.was_recently_up = False

    def should_activate_cursor(self) -> None:
        if LeftHand.up_counter % 2 == 0:
            LeftHand.cursor_activated = not LeftHand.cursor_activated
            LeftHand.up_counter -= 1


class RightHand(Hand):

    def __init__(self, screen: Screen, mp_hands, landmarks) -> None:
        super().__init__(screen, mp_hands, landmarks)

    def facing_forward(self) -> bool:
        return self.fingers.pinky_tip.x > self.fingers.index_tip.x

    def thumb_facing_inwards(self) -> bool:
        return self.fingers.thumb_pointing_right()

    def thumb_facing_outwards(self) -> bool:
        return not self.thumb_facing_inwards()
