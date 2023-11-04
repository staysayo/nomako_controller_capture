import socket
import time

# Remote Control (RC) car's network details
RC_UDP_IP = "192.168.0.1"
RC_UDP_PORT = 8234

# Set up a UDP socket for communication
socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Define command values for center, left, and right steering
CENTER_STEERING_COMMAND = "80"    # Center position for steering command
LEFT_STEERING_COMMAND = "2e"      # Full left
RIGHT_STEERING_COMMAND = "d2"     # Full right

def send_command_to_rc(command_hex):
    # Send a command to the RC car over UDP.
    socket_udp.sendto(bytes.fromhex(command_hex), (RC_UDP_IP, RC_UDP_PORT))
    print(f"Sent command: {command_hex}")

# Function to create a command string for steering
def create_steering_command(steering_position):
    # Constructs the command string with the steering command
    return f"C0 A8 00 01 00 00 04 21 00 00 {steering_position}"

# Try steering left, center, and right
try:
    # Left steering
    send_command_to_rc(create_steering_command(LEFT_STEERING_COMMAND))
    time.sleep(2)  # wait for 2 seconds

    # Center steering
    send_command_to_rc(create_steering_command(CENTER_STEERING_COMMAND))
    time.sleep(2)  # wait for 2 seconds

    # Right steering
    send_command_to_rc(create_steering_command(RIGHT_STEERING_COMMAND))
    time.sleep(2)  # wait for 2 seconds

except KeyboardInterrupt:
    print("\nExiting.")
finally:
    socket_udp.close()
