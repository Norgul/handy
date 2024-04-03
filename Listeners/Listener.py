from abc import ABC, abstractmethod
from Events import Event

class Listener(ABC):
    events = {}
    
    def __init__(self, mode, *args) -> None:
        self.mode = mode
        self.args = args
    
    @abstractmethod
    def handle(self, **kwargs):
        pass
    
    def execute(self, event: Event, **kwargs):
        self.init_events_dict(event)

        if self.mode == 'stream':
            self.stream(event, **kwargs)
        elif self.mode == 'flip_flop':
            self.flip_flop(event)

    def init_events_dict(self, event):
        if not event in self.events:
            self.events[event] = False

        inverse_event = event.inverse_event

        if inverse_event and (not inverse_event in self.events):
            self.events[inverse_event] = False
    
    def flip_flop(self, event: Event):
        """
        Flip-flop mechanism to ensure that event and inverse event are in opposite states.
        """
        if self.events[event]:
            return
    
        self.handle()
        self.events[event] = True

        inverse_event = event.inverse_event
        if inverse_event and self.events[inverse_event]:
            self.events[inverse_event] = False
        
    
    def stream(self, event: Event, **kwargs):
        self.handle(**kwargs)
        self.events[event] = True
    
        inverse_event = event.inverse_event
        if inverse_event and self.events[inverse_event]:
            self.events[inverse_event] = False
    