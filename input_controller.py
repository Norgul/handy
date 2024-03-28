from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController, Key

from pynput.mouse import Button
from pynput.keyboard import Key

class InputController:
    def __init__(self):
        self.mouse = MouseController()
        self.button = Button
        
        self.keyboard = KeyboardController()
        self.key = Key
