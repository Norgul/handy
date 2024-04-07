import time
from typing import Union
from Models.Hand import Hand

class SpawnTimeCounter:

    hand_shown = None

    def __init__(self, spawn_timeout) -> None:
        self.spawn_timeout = spawn_timeout

    def check(self, hand: Hand) -> Union[Hand, None]:
        # Reset value for frames when hand is not visible
        if not hand:
            self.hand_shown = None
            return
    
        # Initialize counter
        if not self.hand_shown:
            self.hand_shown = time.time()

        # Not yet available, unset hand
        if time.time() - self.hand_shown < self.spawn_timeout:
            return None
        
        return hand