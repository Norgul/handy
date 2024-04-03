from Listeners.Listener import Listener
from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import Controller as KeyboardController, Key

class MousePress(Listener):
    def handle(self):
        button = self.args[0]
        
        mouse = MouseController()
        mouse.press(button)
        
        print("Mouse press", button)

class MouseRelease(Listener):
    def handle(self):
        button = self.args[0]
        
        mouse = MouseController()
        mouse.release(button)
        
        print("Mouse release", button)
        
class MouseTap(Listener):
    def handle(self):

        button = self.args[0]
        
        mouse = MouseController()
        mouse.press(button)
        print("Mouse tap", button)
        mouse.release(button)

class MousePosition(Listener):
    def handle(self, **kwargs):
        
        x = kwargs.get('x')
        y = kwargs.get('y')
        
        mouse = MouseController()
        mouse.position = (x, y)

class MouseMove(Listener):
    def handle(self, **kwargs):
        
        x = kwargs.get('x')
        y = kwargs.get('y')
        
        mouse = MouseController()
        mouse.move(x, y)

class MouseScroll(Listener):
    def handle(self, **kwargs):
        
        x = kwargs.get('distance')
        y = 0 #args[1]
        
        mouse = MouseController()
        mouse.scroll(x, y)
        
        print("Mouse scroll", x, y)
        
class KeyPress(Listener):
    def handle(self):
        key = self.args[0]
        
        keyboard = KeyboardController()
        keyboard.press(key)
        
        print("Key press", key)
        
class KeyRelease(Listener):
    def handle(self):
        key = self.args[0]
        
        keyboard = KeyboardController()
        keyboard.release(key)
        
        print("Key release", key)

class KeyTap(Listener):
    def handle(self):
        key = self.args[0]
        
        keyboard = KeyboardController()
        keyboard.press(key)
        print("Key tapped", key)
        keyboard.release(key)
