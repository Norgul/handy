from abc import ABC, abstractmethod
from Events import Event


class Listener(ABC):
    events = {}

    def __init__(self, *args, flip_flop: bool = False) -> None:
        self.args = args
        self.flip_flop = flip_flop

    @abstractmethod
    def handle(self, **kwargs) -> None:
        pass

    def execute(self, event: Event, **kwargs) -> None:
        self.init_events_dict(event)

        # Break only if flip flop is enabled and event has already been executed
        if self.flip_flop and self.events[event]:
            return

        self.handle(**kwargs)

        self.events[event] = True

        inverse_event = event.inverse_event
        if inverse_event and self.events[inverse_event]:
            self.events[inverse_event] = False

    def init_events_dict(self, event) -> None:
        """
        Sets events dictionary to indicate which events were executed and which were not
        """
        if not event in self.events:
            self.events[event] = False

        inverse_event = event.inverse_event

        if inverse_event and (not inverse_event in self.events):
            self.events[inverse_event] = False
