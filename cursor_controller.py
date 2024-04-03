from Hand import Hand
import cv2
import pyautogui
import pygame
from typing import Tuple

class CursorController:
        
    def __init__(self, scale_percentage: int = 30) -> None:
        self.scale_percentage = scale_percentage
        # Is rectangle drawn
        self.drawn = False
        # Are dimensions calculated
        self.calculated = False
        
        self.monitor_width, self.monitor_height = pyautogui.size()
        
        self.scale_factor = None
        self.top_left_x = None
        self.top_left_y = None
        self.bottom_right_x = None
        self.bottom_right_y = None
        
        pygame.init()
        

    def draw_when_true(self, frame, case: bool, hand: Hand) -> None:
        """
        Given some case, draw a rectangle on the screen around finger landmark
        """
        # Case is false, so just reset the variables
        if not case:
            self.drawn = False
            self.calculated = True
            return
            
        # Rectangle is not yet drawn, but we can see the hand on the screen, so we'll extrapolate the coordinates
        if not self.drawn and hand:
            
            scaled_width, scaled_height, self.scale_factor = self.scaled_monitor_dimensions(frame, self.scale_percentage)
            hand_center_x, hand_center_y = hand.center()
            self.calculate_rectangle_coordinates(frame, scaled_width, scaled_height, hand_center_x, hand_center_y)

            self.calculated = True
            
            pygame.mixer.music.load("Effects/cursor_on.mp3")
            pygame.mixer.music.play()

        # We calculated the coordinates, we can continue drawing this on the screen as long as you don't reset it
        if self.calculated:
            # Draw the rectangle on the frame
            cv2.rectangle(frame, (self.top_left_x, self.top_left_y), (self.bottom_right_x, self.bottom_right_y), (255, 255, 255), 3)
            self.drawn = True
            
    def scaled_monitor_dimensions(self, frame, percentage: int) -> Tuple[int, int, float]:
        """
        Return monitor dimensions scaled to fit in x% of the frame
        """
        frame_height, frame_width, _ = frame.shape
            
        scaled_width = int(frame_width * (percentage / 100))
        scale_factor = scaled_width / self.monitor_width
        scaled_height = int(self.monitor_height * scale_factor)
        
        return scaled_width, scaled_height, scale_factor
        
    def calculate_rectangle_coordinates(self, frame, scaled_width, scaled_height, center_x, center_y) -> None:
        """
        Calculate rectangle coordinates to position it around center coordinates,
        but keep it within frame bounds if it was to be drawn outside a frame.
        """
        frame_height, frame_width, _ = frame.shape

        # Calculate half of the rectangle width and height
        half_width = scaled_width / 2
        half_height = scaled_height / 2

        # Calculate the coordinates of the top-left corner and bottom-right corner
        self.top_left_x = int(center_x - half_width)
        self.top_left_y = int(center_y - half_height)

        # Adjust coordinates to keep the rectangle within the screen bounds
        if self.top_left_x < 0:
            self.top_left_x = 0
        elif self.top_left_x + scaled_width > frame_width:
            self.top_left_x = frame_width - scaled_width

        if self.top_left_y < 0:
            self.top_left_y = 0
        elif self.top_left_y + scaled_height > frame_height:
            self.top_left_y = frame_height - scaled_height

        # Calculate bottom-right coordinates based on adjusted top-left coordinates
        self.bottom_right_x = self.top_left_x + scaled_width
        self.bottom_right_y = self.top_left_y + scaled_height

    def move_mouse_within_rectangle(self, frame, x, y) -> Tuple[float, float]:
        """
        Move the mouse within a specified rectangle based on finger coordinates.
        """
        frame_height, frame_width, _ = frame.shape
        
        # Put borders in 0-1 range
        left_border = self.top_left_x / frame_width
        right_border = self.bottom_right_x / frame_width
        top_border = self.top_left_y / frame_height
        bottom_border = self.bottom_right_y / frame_height
        
        # Reset X so that 0 is right at the left border
        x_moved_origin = x - left_border
        # Reset Y so that 0 is right at the top border
        y_moved_origin = y - top_border
        
        # Scale down the range to fit 0-1 in smaller rectangle range
        normalized_x = x_moved_origin / (right_border - left_border)
        normalized_y = y_moved_origin / (bottom_border - top_border)

        # Clamp between 0-1 range
        normalized_x = max(0.0, min(normalized_x, 1.0))
        normalized_y = max(0.0, min(normalized_y, 1.0))
        
        # X goes from 0-1, normalizing to actual pixels
        mouse_x = normalized_x * self.monitor_width
        mouse_y = normalized_y * self.monitor_width
        
        return (mouse_x, mouse_y)
