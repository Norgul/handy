from Events.Event import Event
from Listeners.Listener import Listener

class EventManager:
    
    def __init__(self, map: dict, inverse_map: dict) -> None:
        self.map = map
        self.inverse_map = inverse_map

        self.register_events()
        self.register_inverse_events()


    def register_events(self) -> None:
        for event in self.map:
            event: Event = event

            for listener in self.map[event]:
                listener: Listener = event

                event.listen(listener)


    def register_inverse_events(self) -> None:
        for event in self.inverse_map:
            event: Event = event
            listener: Listener = self.inverse_map[event]

            event.register_inverse(listener)

