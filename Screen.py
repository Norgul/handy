from typing import Tuple
import pyautogui
import numpy as np

class Screen:

    frame_width: float = None
    frame_height: float = None
    monitor_width: int = None
    monitor_height: int = None

    def __init__(self, frame: np.array) -> None:
        self.frame = frame

        # Make sure to calculate just once upon instantiation
        if not Screen.frame_width or not Screen.frame_height:
            Screen.frame_height, Screen.frame_width, _ = frame.shape

        # Make sure to calculate just once upon instantiation
        if not Screen.monitor_width or not Screen.monitor_height:
            Screen.monitor_width, Screen.monitor_height = pyautogui.size()


    def double_coordinates_to_pixels(self, width: int, height: int, top_left_x: float, top_left_y: float, bottom_right_x: float, bottom_right_y: float) -> Tuple[int, int, int, int]:
        top_left_x, top_left_y = self.coordinates_to_pixels(top_left_x, top_left_y, width, height)
        bottom_right_x, bottom_right_y = self.coordinates_to_pixels(bottom_right_x, bottom_right_y, width, height)

        return (top_left_x, top_left_y, bottom_right_x, bottom_right_y)


    def coordinates_to_pixels(self, x: float, y: float, width: int, height: int) -> Tuple[int, int]:
        """
        Take coordinates in 0-1 range and scale them up to 
        dimension in pixels for a given width/height 
        """
        return int(x * width), int(y * height)


    def coordinates_to_frame_pixels(self, x: float, y: float) -> Tuple[int, int]:
        return self.coordinates_to_pixels(x, y, Screen.frame_width, Screen.frame_height)
    

    def scale_monitor_to_frame(self, percentage: int) -> Tuple[int, int, float]:
        """
        Return monitor dimensions scaled to fit in x% of the frame
        """
        scaled_width = int(Screen.frame_width * (percentage / 100))
        scale_factor = scaled_width / Screen.monitor_width
        scaled_height = int(Screen.monitor_height * scale_factor)
        
        return scaled_width, scaled_height, scale_factor