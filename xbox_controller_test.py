import pygame
import time

# Initialize pygame and the joystick
pygame.init()
pygame.joystick.init()

# Check for joystick presence
if pygame.joystick.get_count() < 1:
    print("No joystick connected!")
    pygame.quit()
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

try:
    while True:
        pygame.event.pump()
        # Xbox controllers usually use axes 3 for the right Y stick and 0 for the left X stick
        # These numbers may vary based on your controller and how pygame interprets it
        right_stick_y = joystick.get_axis(3)  # Right Stick Y-Axis
        left_stick_x = joystick.get_axis(0)   # Left Stick X-Axis
        print(f"Right Stick Y-Axis: {right_stick_y}, Left Stick X-Axis: {left_stick_x}")
        time.sleep(0.1)  # Add a small delay to make the output readable

except KeyboardInterrupt:
    # Handle Ctrl-C to terminate the script
    print("\nExiting.")
    pygame.quit()
