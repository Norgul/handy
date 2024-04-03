from Events.LeftHandEvents import HandSpawnedCursor, LeftThumbReleasedIndex, LeftThumbReleasedMiddle, LeftThumbReleasedPinky, LeftThumbReleasedRing, LeftThumbTouchedIndex, LeftThumbTouchedMiddle, LeftThumbTouchedPinky, LeftThumbTouchedRing
from Events.RightHandEvents import RightHandGrab, RightHandPointingOne, RightHandPointingThree, RightHandPointingTwo, RightThumbReleasedIndex, RightThumbReleasedMiddle, RightThumbReleasedPinky, RightThumbReleasedRing, RightThumbTouchedIndex, RightThumbTouchedMiddle, RightThumbTouchedPinky, RightThumbTouchedRing
from Listeners.Listeners import KeyPress, KeyRelease, KeyTap, MouseMove, MousePosition, MousePress, MouseRelease, MouseScroll, MouseTap
from pynput.mouse import Button
from pynput.keyboard import Key

class EventManager:
    
    map = {
        LeftThumbTouchedIndex(): [MousePress('flip_flop', Button.left)],
        LeftThumbReleasedIndex(): [MouseRelease('flip_flop', Button.left)],
        LeftThumbTouchedMiddle(): [
            MousePress('flip_flop', Button.middle),
            MouseMove('stream')
        ],
        LeftThumbReleasedMiddle(): [
            MouseRelease('flip_flop', Button.middle),
        ],
        LeftThumbTouchedPinky(): [],
        LeftThumbReleasedPinky(): [],
        LeftThumbTouchedRing(): [],
        LeftThumbReleasedRing(): [],

        HandSpawnedCursor(): [
            MousePosition('stream')
        ],
        
        RightThumbTouchedIndex(): [KeyPress('flip_flop', 'G')],
        RightThumbReleasedIndex(): [KeyRelease('flip_flop', 'G')],
        RightThumbTouchedMiddle(): [KeyPress('flip_flop', 'R')],
        RightThumbReleasedMiddle(): [KeyRelease('flip_flop', 'R')],
        RightThumbTouchedRing(): [KeyPress('flip_flop', 'S')],
        RightThumbReleasedRing(): [KeyRelease('flip_flop', 'S')],
        RightThumbTouchedPinky(): [KeyPress('flip_flop', 'E')],
        RightThumbReleasedPinky(): [KeyRelease('flip_flop', 'E')],

        RightHandPointingOne(): [KeyTap('flip_flop', 'X')],
        RightHandPointingTwo(): [KeyTap('flip_flop', 'Y')],
        RightHandPointingThree(): [KeyTap('flip_flop', 'Z')],

        RightHandGrab(): [KeyTap('flip_flop', Key.shift)]
    }

    def __init__(self) -> None:
        pass
    
    def register(self) -> 'EventManager':

        for event in EventManager.map:
            for listener in EventManager.map[event]:
                event.listen(listener)

        return self
                
    def register_inverse_events(self) -> 'EventManager':

        LeftThumbTouchedIndex.register_inverse(LeftThumbReleasedIndex)
        LeftThumbTouchedMiddle.register_inverse(LeftThumbReleasedMiddle)
        LeftThumbTouchedPinky.register_inverse(LeftThumbReleasedPinky)
        LeftThumbTouchedRing.register_inverse(LeftThumbReleasedRing)

        RightThumbTouchedIndex.register_inverse(RightThumbReleasedIndex)
        RightThumbTouchedMiddle.register_inverse(RightThumbReleasedMiddle)
        RightThumbTouchedPinky.register_inverse(RightThumbReleasedPinky)
        RightThumbTouchedRing.register_inverse(RightThumbReleasedRing)

        return self