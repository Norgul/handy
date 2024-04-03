from abc import ABC
from typing import Type
from typing import List
from Listeners.Listener import Listener

class Event(ABC):
    @classmethod
    def __init__(self) -> None:
        self.inverse_event: self = None
        self.listeners: List[Listener] = []
        self.executed = False

    @classmethod
    def dispatch(self, case: bool, **kwargs) -> None:
        """
        Flip-flop mechanism for dispatching events. As long as case is true, it will execute
        listeners. Inverse event will only trigger if original event was once triggered
        to prevent continuous triggering of inverse events when nothing is happening.
        """
        if case:
            for listener in self.listeners:
                listener.execute(self, **kwargs)
                    
            self.executed = True

        elif self.executed:
            self.executed = False
            
            if self.inverse_event:
                self.inverse_event.dispatch(True)

    @classmethod
    def register_inverse(self, event: Type['Event']) -> None:
        """
        Set inverse event which would be triggered as opposite in flip-flop mechanism.
        Make sure that inverse event has this event as its inverse as well.

        I.e. if original event is PressSomething, inverse might be ReleaseSomething.
        """
        self.inverse_event = event
        event.inverse_event = self

    @classmethod
    def listen(self, listener: Listener) -> None:
        self.listeners.append(listener)
    