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
        
        
    key_states = {}

    key_pressed = False
    mouse_clicked = False
    

    @staticmethod
    def press(case, key):
        keyboard = KeyboardController()

        if key not in InputController.key_states:
            InputController.key_states[key] = False

        if case:
            if not InputController.key_states[key]:
                print("Pressed", key)
                keyboard.press(key)
                InputController.key_states[key] = True
        else:
            if InputController.key_states[key]:
                print("Released", key)
                keyboard.release(key)
                InputController.key_states[key] = False
                
                
    @staticmethod
    def click(case, button):
        
        mouse = MouseController()
        
        if case:
            if not InputController.mouse_clicked:
                print("Mouse click", button)
                mouse.click(button)
                InputController.mouse_clicked = True
        else:
            if InputController.mouse_clicked:
                print("Released click", button)
                InputController.mouse_clicked = False