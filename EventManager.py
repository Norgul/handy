from typing import Type
from Events.Event import Event

class EventManager:
    
    def __init__(self, map: dict, inverse_map: dict) -> None:
        self.map = map
        self.inverse_map = inverse_map


    def register(self) -> 'EventManager':
        # Register map events
        for event in self.map:
            event: Type[Event] = event

            for listener in self.map[event]:
                event.listen(listener)

        # Register inverse events
        for event in self.inverse_map:
            event: Type[Event] = event

            event.register_inverse(self.inverse_map[event])

        return self
