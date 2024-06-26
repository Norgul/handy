from Models.Hand import Hand
from Listeners.Listener import Listener
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController
from CursorController import CursorController


class MousePress(Listener):
    def __init__(self, *args) -> None:
        super().__init__(*args, flip_flop=True)

    def handle(self, **kwargs) -> None:
        button = self.args[0]

        mouse = MouseController()
        mouse.press(button)

        print("Mouse press", button)


class MouseRelease(Listener):
    def __init__(self, *args) -> None:
        super().__init__(*args, flip_flop=True)

    def handle(self, **kwargs) -> None:
        button = self.args[0]

        mouse = MouseController()
        mouse.release(button)

        print("Mouse release", button)


class MouseTap(Listener):
    def handle(self, **kwargs) -> None:

        button = self.args[0]

        mouse = MouseController()
        mouse.press(button)
        print("Mouse tap", button)
        mouse.release(button)


class MousePosition(Listener):
    def handle(self, **kwargs) -> None:

        x = kwargs.get("x")
        y = kwargs.get("y")

        mouse = MouseController()
        mouse.position = (x, y)


class MouseMove(Listener):
    def handle(self, **kwargs) -> None:

        x = kwargs.get("x")
        y = kwargs.get("y")

        mouse = MouseController()
        mouse.move(x, y)


class MouseScroll(Listener):
    def handle(self, **kwargs) -> None:

        x = kwargs.get("distance")
        y = 0  # args[1]

        mouse = MouseController()
        mouse.scroll(x, y)

        print("Mouse scroll", x, y)


class KeyPress(Listener):
    def __init__(self, *args) -> None:
        super().__init__(*args, flip_flop=True)

    def handle(self, **kwargs) -> None:
        key = self.args[0]

        keyboard = KeyboardController()
        keyboard.press(key)

        print("Key press", key)


class KeyRelease(Listener):
    def __init__(self, *args) -> None:
        super().__init__(*args, flip_flop=True)

    def handle(self, **kwargs) -> None:
        key = self.args[0]

        keyboard = KeyboardController()
        keyboard.release(key)

        print("Key release", key)


class KeyTap(Listener):
    def __init__(self, *args) -> None:
        super().__init__(*args, flip_flop=True)

    def handle(self, **kwargs) -> None:
        key = self.args[0]

        keyboard = KeyboardController()
        keyboard.press(key)
        print("Key tapped", key)
        keyboard.release(key)


class DrawCursorGrid(Listener):
    def handle(self, **kwargs) -> None:

        cursor_controller: CursorController = self.args[0]
        frame = kwargs.get("frame")
        hand = kwargs.get("hand")

        cursor_controller.draw_bounds(frame, hand)


class ControlCursor(Listener):
    def handle(self, **kwargs) -> None:

        cursor_controller: CursorController = self.args[0]
        frame = kwargs.get("frame")
        hand: Hand = kwargs.get("hand")

        mouse = MouseController()

        if CursorController.fine_mode:
            (mouse_x, mouse_y) = cursor_controller.calculate_distance_from_point(frame, *hand.bottom_knuckle_center())
            mouse.move(mouse_x, mouse_y)
            return

        if not CursorController.coordinates:
            return

        mouse.position = cursor_controller.interpolate_mouse(*hand.bottom_knuckle_center())


class TurnOnFineMode(Listener):
    def __init__(self, *args) -> None:
        super().__init__(*args, flip_flop=True)

    def handle(self, **kwargs) -> None:
        CursorController.fine_mode = True


class TurnOffFineMode(Listener):
    def __init__(self, *args) -> None:
        super().__init__(*args, flip_flop=True)

    def handle(self, **kwargs) -> None:
        CursorController.fine_mode = False
        CursorController.spawned_point = None


class ResetCursorGrid(Listener):
    def __init__(self, *args) -> None:
        super().__init__(*args, flip_flop=True)

    def handle(self, **kwargs) -> None:
        CursorController.coordinates = None
