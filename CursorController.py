from Hand import Hand
import cv2
import pyautogui
import pygame
from typing import Tuple
import math

from Screen import Screen

class CursorController:
        
    # Where to start measuring distance from. 
    # TODO: This should be refactored to support many of these.
    spawned_point = None
    
    # Coordinates for a cursor grid within the mouse will move
    coordinates = None

    def __init__(self, scale_percentage: int = 50) -> None:
        self.scale_percentage = scale_percentage
        self.monitor_width, self.monitor_height = pyautogui.size()
        
        pygame.init()

    def inject_screen(self, screen: Screen) -> None:
        self.screen = screen


    def draw_bounds(self, frame, hand: Hand) -> None:
        """
        Draw a rectangle on the screen around finger landmark
        """
        hand_center_x, hand_center_y = hand.center()

        if not CursorController.coordinates:
            CursorController.coordinates = self.screen.scaled_monitor_coordinates_around(hand_center_x, hand_center_y)

            pygame.mixer.music.load("Effects/cursor_on.mp3")
            pygame.mixer.music.play()

        # Draw the rectangle on the frame
        cv2.rectangle(frame, (CursorController.coordinates[0], CursorController.coordinates[1]), (CursorController.coordinates[2], CursorController.coordinates[3]), (255, 255, 255), 3)
        # Draw the circle representing a cursor indicator
        cv2.circle(frame, (hand_center_x, hand_center_y), 25, (0, 0, 0), cv2.FILLED)


    def normalize_mouse(self, x, y) -> Tuple[float, float]:
        """
        Take x/y coordinates as pixel value of frame pixels
        move origin so that 0 starts on rectangle beginning instead of frame beginning
        normalize them to monitor dimensions
        """
        top_left_x, top_left_y = (CursorController.coordinates[0], CursorController.coordinates[1])

        x_moved_origin = x - top_left_x
        y_moved_origin = y - top_left_y

        normalized_x = int(x_moved_origin / Screen.scale_factor)
        normalized_y = int(y_moved_origin / Screen.scale_factor)

        mouse_x = max(0, min(normalized_x, self.screen.monitor_width))
        mouse_y = max(0, min(normalized_y, self.screen.monitor_height))

        return (mouse_x, mouse_y)


    def calculate_distance_from_point(self, frame, hand: Hand) -> Tuple[float, float]:
        fingers = hand.fingers

        if not hand.touching(fingers.thumb_tip, fingers.middle_tip):
            CursorController.spawned_point = None
            return None, None

        frame_height, frame_width, _ = frame.shape
        cx, cy = int(fingers.middle_tip.x * frame_width), int(fingers.middle_tip.y * frame_height)
        
        middle_tip_pixel = (cx, cy)
        
        if not CursorController.spawned_point:
            CursorController.spawned_point = (cx, cy)

        cv2.line(frame, CursorController.spawned_point, middle_tip_pixel, (255,255,0), 3)

        # Calculate distance between points
        x_diff_squared = (middle_tip_pixel[0] - CursorController.spawned_point[0])**2
        y_diff_squared = (middle_tip_pixel[1] - CursorController.spawned_point[1])**2
        distance = math.sqrt(x_diff_squared + y_diff_squared)
        
        direction_vector = (middle_tip_pixel[0] - CursorController.spawned_point[0], middle_tip_pixel[1] - CursorController.spawned_point[1])
    
        # Calculate speed based on distance
        # You can adjust the scaling factor as needed
        speed = (distance/100) * 0.1  # Adjust as needed
        dx = direction_vector[0] * speed
        dy = direction_vector[1] * speed

        return dx, dy
