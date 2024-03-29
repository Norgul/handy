import cv2
from mp_hands import MpHands
from input_controller import InputController
from gestures.main import Gestures

mp_hands = MpHands()
cap = cv2.VideoCapture(0)
input_controller = InputController()

def find_and_draw_midpoints(frame):
    # Get frame dimensions
    height, width, _ = frame.shape
    
    # Draw a vertical line across the frame
    cv2.line(frame, (width // 2, 0), (width // 2, height), (255, 255, 255), 1)
    
    # Find middle points of each half of the screen
    midpoint_left = (width // 4, height // 2)
    midpoint_right = (width // 4 * 3, height // 2)
    
    # Draw filled red circles at the middle points
    radius = 10
    thickness = -1  # Negative thickness to fill the circle
    color = (0, 0, 255)  # Red color
    cv2.circle(frame, midpoint_left, radius, color, thickness)
    cv2.circle(frame, midpoint_right, radius, color, thickness)
    
    # Store coordinates of the circles
    midpoint_left_coordinates = (midpoint_left[0], midpoint_left[1])
    midpoint_right_coordinates = (midpoint_right[0], midpoint_right[1])
    
    return midpoint_left_coordinates, midpoint_right_coordinates

while True:
    success, frame = cap.read()
    if not success:
        continue
    
    # Flip the image horizontally for a selfie-view display.
    frame = cv2.flip(frame, 1)    
    
    # Split screen in half and find centers
    left_midpoint, right_midpoint = find_and_draw_midpoints(frame)
    
    left_hand, right_hand = mp_hands.extract_hands(frame)
    
    gestures = Gestures(frame, left_hand, right_hand, input_controller).load()
    
    # Left
    InputController.click(gestures.left_thumb_index_touch, input_controller.button.left)

    # Right
    InputController.press(gestures.right_thumb_index_touch, input_controller.key.shift)
    
    
    cv2.imshow('MediaPipe Hands', frame)
    # Use Esc to exit
    if cv2.waitKey(5) & 0xFF == 27:
        break
    
cap.release()






     
        
    #     if left_hand:
    #         h,w,c = frame.shape
    #         cx, cy = int(left_hand.fingers.index_bottom.x*w), int(left_hand.fingers.index_bottom.y*h)
            
    #         index_bottom = (cx, cy)
            
    #         print("------")

    #         cv2.line(frame, left_midpoint, index_bottom, (255,255,0 ), 3)

            
    
    #         # Calculate distance between points
    #         x_diff_squared = (index_bottom[0] - left_midpoint[0])**2
    #         y_diff_squared = (index_bottom[1] - left_midpoint[1])**2
    #         distance = math.sqrt(x_diff_squared + y_diff_squared)

            
    #         direction_vector = (index_bottom[0] - left_midpoint[0], index_bottom[1] - left_midpoint[1])


    #         # Move mouse cursor based on direction and distance
    #         self.move_mouse_direction_distance(input_controller, direction_vector, distance)
        
    #     # if left_hand and input_controller:
    #     #     # Convert normalized coordinates to screen coordinates
    #     #     image_width, image_height = frame.shape[1], frame.shape[0]
    #     #     x = int(left_hand.fingers.index_tip.x * image_width)
    #     #     y = int(left_hand.fingers.index_tip.y * image_height)

    #     #     # Move mouse cursor
    #     #     self.move_mouse(input_controller, x, y)
        
    
    # def move_mouse_direction_distance(self, input_controller: InputController, direction, distance):

    #     pygame.mixer.init()
        
    #     # Calculate speed based on distance
    #     # You can adjust the scaling factor as needed
    #     speed = (distance/100) * 0.1  # Adjust as needed
    #     dx = direction[0] * speed
    #     dy = direction[1] * speed
    #     input_controller.mouse.move(dx, dy)

        
    # def clamp_between(self, value, in_min, in_max, out_min, out_max):
    #     """
    #     Take a numeric value, give it original min-max values it 
    #     can span from, then give it output min-max value it 
    #     should be spread at
    #     """

    #     ratio = (value - in_min) / (in_max - in_min)
        
    #     # Scale and shift the ratio to fit within the output range
    #     mapped_value = out_min + (ratio * (out_max - out_min))
        
    #     return mapped_value
    
