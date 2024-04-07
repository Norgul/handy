from typing import Tuple
import pyautogui
import numpy as np
import math 

class Screen:

    frame_width: float = None
    frame_height: float = None
    monitor_width: int = None
    monitor_height: int = None
    scale_factor = 0

    def __init__(self, frame: np.array, scale_percentage: int = 50) -> None:
        self.frame = frame
        self.scale_percentage = scale_percentage

        # Make sure to calculate just once upon instantiation
        if not Screen.frame_width or not Screen.frame_height:
            Screen.frame_height, Screen.frame_width, _ = frame.shape

        # Make sure to calculate just once upon instantiation
        if not Screen.monitor_width or not Screen.monitor_height:
            Screen.monitor_width, Screen.monitor_height = pyautogui.size()
        

    def coordinates_to_frame_pixels(self, x: float, y: float) -> Tuple[int, int]:
        return self.coordinates_to_pixels(x, y, Screen.frame_width, Screen.frame_height)
    

    def coordinates_to_pixels(self, x: float, y: float, width: int, height: int) -> Tuple[int, int]:
        """
        Take coordinates in 0-1 range and scale them up to 
        dimension in pixels for a given width/height 
        """
        return int(x * width), int(y * height)
    

    def pixels_to_frame_coordinates(self, x: float, y: float) -> Tuple[int, int]:
        return self.pixels_to_coordinates(x, y, Screen.frame_width, Screen.frame_height)
    

    def pixels_to_coordinates(self, x: float, y: float, width: int, height: int) -> Tuple[float, float]:
        """
        Take coordinates in pixel range and scale them down to 
        0-1 dimension for a given width/height 
        """
        return x / width, y / height


    def scaled_monitor_coordinates_around(self, x: int, y: int):
        """
        Draw a scaled monitor rectangle around a given point
        """
        scaled_monitor_width, scaled_monitor_height, Screen.scale_factor = self.scale_monitor_to_frame(self.scale_percentage)
        
        return self.calculate_rectangle_coordinates(scaled_monitor_width, scaled_monitor_height, x, y)


    def scale_monitor_to_frame(self, percentage: int) -> Tuple[int, int, float]:
        """
        Return monitor dimensions scaled to fit in x% of the frame
        """
        scaled_width = int(Screen.frame_width * (percentage / 100))
        scale_factor = scaled_width / Screen.monitor_width
        # Probably doesn't matter much, but this will round up to higher pixel
        scaled_height = math.ceil(Screen.monitor_height * scale_factor)

        return scaled_width, scaled_height, scale_factor
    

    def calculate_rectangle_coordinates(self, scaled_width, scaled_height, center_x, center_y) -> Tuple[int, int, int, int]:
        """
        Calculate rectangle coordinates to position it around center coordinates,
        but keep it within frame bounds if it was to be drawn outside a frame.
        """
        # Calculate half of the rectangle width and height
        half_width = scaled_width / 2
        half_height = scaled_height / 2

        # Calculate the coordinates of the top-left corner and bottom-right corner
        top_left_x = int(center_x - half_width)
        top_left_y = int(center_y - half_height)

        # Adjust coordinates to keep the rectangle within the screen bounds
        if top_left_x < 0:
            top_left_x = 0
        elif top_left_x + scaled_width > Screen.frame_width:
            top_left_x = Screen.frame_width - scaled_width

        if top_left_y < 0:
            top_left_y = 0
        elif top_left_y + scaled_height > Screen.frame_height:
            top_left_y = Screen.frame_height - scaled_height

        # Calculate bottom-right coordinates based on adjusted top-left coordinates
        bottom_right_x = top_left_x + scaled_width
        bottom_right_y = top_left_y + scaled_height

        return (top_left_x, top_left_y, bottom_right_x, bottom_right_y)