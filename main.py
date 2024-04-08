import cv2
from EventManager import EventManager
from Events.LeftHandEvents import *
from Events.RightHandEvents import *
from Listeners.Listeners import *
from pynput.mouse import Button
from pynput.keyboard import Key
from Screen import Screen
from Models.MpHands import MpHands
from CursorController import CursorController
from Gestures import Gestures
from HandSpawnTimeCounter import SpawnTimeCounter

cursor_controller = CursorController()

EventManager(
    map={
        # region simple left gestures
        LeftThumbTouchedIndex(): [MousePress(Button.left)],
        LeftThumbReleasedIndex(): [MouseRelease(Button.left)],
        LeftThumbTouchedMiddle(): [MousePress(Button.middle)],
        LeftThumbReleasedMiddle(): [MouseRelease(Button.middle)],
        LeftThumbTouchedRing(): [MousePress(Button.right)],
        LeftThumbReleasedRing(): [MousePress(Button.right)],
        LeftThumbTouchedPinky(): [],
        LeftThumbReleasedPinky(): [],
        # endregion simple left gestures
        # region simple right gestures
        RightThumbTouchedIndex(): [KeyPress("G")],
        RightThumbReleasedIndex(): [KeyRelease("G")],
        RightThumbTouchedMiddle(): [KeyPress("R")],
        RightThumbReleasedMiddle(): [KeyRelease("R")],
        RightThumbTouchedRing(): [KeyPress("S")],
        RightThumbReleasedRing(): [KeyRelease("S")],
        RightThumbTouchedPinky(): [KeyPress("E")],
        RightThumbReleasedPinky(): [KeyRelease("E")],
        RightHandPointingOne(): [KeyTap("X")],
        RightHandPointingTwo(): [KeyTap("Y")],
        RightHandPointingThree(): [KeyTap("Z")],
        RightHandGrab(): [KeyTap(Key.shift)],
        # region simple right gestures
        CursorActivated(): [DrawCursorGrid(cursor_controller), ControlCursor(cursor_controller)],
        CursorDeactivated(): [ResetCursorGrid(cursor_controller)],
        FineModeActivated(): [TurnOnFineMode(cursor_controller)],
        FineModeDeactivated(): [TurnOffFineMode(cursor_controller)],
    },
    inverse_map={
        LeftThumbTouchedIndex: LeftThumbReleasedIndex,
        LeftThumbTouchedMiddle: LeftThumbReleasedMiddle,
        LeftThumbTouchedPinky: LeftThumbReleasedPinky,
        LeftThumbTouchedRing: LeftThumbReleasedRing,
        RightThumbTouchedIndex: RightThumbReleasedIndex,
        RightThumbTouchedMiddle: RightThumbReleasedMiddle,
        RightThumbTouchedPinky: RightThumbReleasedPinky,
        RightThumbTouchedRing: RightThumbReleasedRing,
        CursorActivated: CursorDeactivated,
        FineModeActivated: FineModeDeactivated,
    },
)

mp_hands = MpHands()
cap = cv2.VideoCapture(0)

left_timer = SpawnTimeCounter(spawn_timeout=0.3)
right_timer = SpawnTimeCounter(spawn_timeout=0.3)

while True:
    success, frame = cap.read()
    if not success:
        continue

    # Flip the image horizontally for a selfie-view display.
    frame = cv2.flip(frame, 1)

    screen = Screen(frame)
    # TODO: is there a better way to do this?
    cursor_controller.inject_screen(screen)

    left_hand, right_hand = mp_hands.extract_hands(screen)

    # Make sure to start monitoring gestures after certain
    # amount of time hands have been present on the screen
    left_hand = left_timer.check(left_hand)
    right_hand = right_timer.check(right_hand)

    # Draw bounding boxes
    # if left_hand:
    #     top_left_x, top_left_y, bottom_right_x, bottom_right_y = left_hand.bounding_box()
    #     cv2.rectangle(frame, (top_left_x, top_left_y), (bottom_right_x, bottom_right_y), (0, 255, 0), 2)
    # if right_hand:
    #     top_left_x, top_left_y, bottom_right_x, bottom_right_y = right_hand.bounding_box()
    #     cv2.rectangle(frame, (top_left_x, top_left_y), (bottom_right_x, bottom_right_y), (0, 255, 0), 2)

    Gestures(frame).load(left_hand, right_hand)

    cv2.imshow("MediaPipe Hands", frame)
    # Use Esc to exit
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
