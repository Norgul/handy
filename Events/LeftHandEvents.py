from Events.Event import Event

# region finger-to-finger touch


class LeftThumbTouchedIndex(Event):
    pass


class LeftThumbReleasedIndex(Event):
    pass


class LeftThumbTouchedMiddle(Event):
    pass


class LeftThumbReleasedMiddle(Event):
    pass


class LeftThumbTouchedPinky(Event):
    pass


class LeftThumbReleasedPinky(Event):
    pass


class LeftThumbTouchedRing(Event):
    pass


class LeftThumbReleasedRing(Event):
    pass


# endregion finger-to-finger touch


class CursorActivated(Event):
    pass


class CursorDeactivated(Event):
    pass


class FineModeActivated(Event):
    pass


class FineModeDeactivated(Event):
    pass
