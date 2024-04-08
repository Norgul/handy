from typing import List
from Events.Event import Event
from Listeners.Listener import Listener


class EventManager:

    def __init__(self, map: dict[Event, List[Listener]], inverse_map: dict[Event, Listener]) -> None:
        self.map = map
        self.inverse_map = inverse_map

        self.register_events()
        self.register_inverse_events()

    def register_events(self) -> None:
        for event in self.map:
            for listener in self.map[event]:
                event.listen(listener)

    def register_inverse_events(self) -> None:
        for event in self.inverse_map:
            event.register_inverse(self.inverse_map[event])
