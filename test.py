"""
@description Main script for controlling a Remote-Controlled (RC) car via UDP using a joystick.
             This script captures joystick inputs and translates them into commands
             sent to the RC car over a Wi-Fi Direct (P2P) UDP connection.
@version 1.1.0 - Added structured comments for documentation generation
@author Neal Wallace
@date 11/04/2023
"""

import pygame
import socket
import time
import select

# Version number for the script updated to reflect the integration of notes as comments
__version__ = "1.1.0"

# Initialize the pygame library and the joystick module
pygame.init()
pygame.joystick.init()

# Check if there is at least one joystick connected
if pygame.joystick.get_count() < 1:
    print("No joystick detected! Please connect a joystick to continue.")
    pygame.quit()
    exit()

# Initialize the first joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()

"""
@description Network configuration for the RC car's communication.
@details Establishes a non-blocking UDP socket to communicate with the RC car.
         The IP and port should match the RC car's network settings.
@network_details IP: 192.168.0.1, Port: 8234, Connection: Wi-Fi Direct (P2P), TTL: 64, Flags: Do not fragment
"""
RC_UDP_IP = "192.168.0.1"
RC_UDP_PORT = 8234
socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socket_udp.bind(('', RC_UDP_PORT))
socket_udp.setblocking(0)

"""
@description Defines the dead zones for joystick sensitivity.
             This helps to prevent unintended movements when the joystick is near its center position.
@dead_zones Forward/Reverse: 0.05, Steering: 0.15
"""
DEAD_ZONE_FORWARD_REVERSE = 0.05
DEAD_ZONE_STEERING = 0.15

"""
@description Default command values for the RC car when the joystick is in the neutral position.
@defaults Idle throttle command: "00", Center steering command: "80"
"""
IDLE_THROTTLE_COMMAND = "00"
CENTER_STEERING_COMMAND = "80"

"""
@description Function to apply dead zone adjustments to joystick input.
@behavior Ignores any input_value that falls within the specified dead_zone_threshold.
@insight By adjusting the dead_zone_threshold, we can fine-tune the responsiveness of the joystick input.
@todo Fine-tune dead zone values based on user feedback or empirical testing.
"""
def apply_dead_zone(input_value, dead_zone_threshold):
    if -dead_zone_threshold < input_value < dead_zone_threshold:
        return 0
    return (input_value - dead_zone_threshold) / (1 - dead_zone_threshold) if input_value > 0 else (input_value + dead_zone_threshold) / (1 - dead_zone_threshold)

"""
@description Function to map joystick input to command values with steering adjustment.
@behavior Handles negative values for left steering and positive for right steering.
          Zero input centers the steering.
@insight The mapping accounts for the dead zones and scales the input to the expected command range.
@todo Consider implementing a non-linear mapping for more intuitive control.
"""
def map_value_to_command(input_value, input_min, input_max, output_min, output_max):
    if input_value < 0:
        return format(int(((input_value - input_min) / (0 - input_min)) * (0x2e - output_min) + output_min), '02x')
    elif input_value > 0:
        return format(int(((input_value - 0) / (input_max - 0)) * (output_max - 0x80) + 0x80), '02x')
    else:
        return format(0x80, '02x')

"""
@description Function to create command strings based on joystick positions.
@behavior Constructs a command string with separate forward and reverse commands, as well as steering.
@insight Commands are formed by concatenating hex values representing different control signals.
@todo Implement additional commands for other functionalities such as lights and horn.
"""
def create_command_string(throttle_position, steering_position):
    throttle_position = apply_dead_zone(throttle_position, DEAD_ZONE_FORWARD_REVERSE)
    steering_position = apply_dead_zone(steering_position, DEAD_ZONE_STEERING)
    forward_command = map_value_to_command(throttle_position, 0, 1, 45, 230) if throttle_position > 0 else IDLE_THROTTLE_COMMAND
    reverse_command = map_value_to_command(-throttle_position, 0, 1, 42, 230) if throttle_position < 0 else IDLE_THROTTLE_COMMAND
    steering_command = map_value_to_command(steering_position, -1, 1, 46, 210)
    return f"C0 A8 01 01 00 00 04 21 {forward_command} {reverse_command} {steering_command}"

"""
@description Function to send the command to the RC car.
@behavior Converts the hex string into bytes and transmits the command via the UDP socket.
@insight This is the direct interface with the RC car, where commands are executed.
@todo Implement error handling for network errors or failed transmissions.
"""
def send_command_to_rc(command_hex):
    socket_udp.sendto(bytes.fromhex(command_hex), (RC_UDP_IP, RC_UDP_PORT))

"""
@description Starts the communication handshake with the RC car.
@handshake_process Sends the MAKO_CONNECT command and listens for any acknowledgment.
                   If no response is received within 2 seconds, it proceeds to send the handshake sequence.
"""
def initiate_handshake_with_rc():
    connect_command_hex = "4D 41 4B 4F 5F 43 4F 4E 4E 45 43 54"
    send_command_to_rc(connect_command_hex)
    print("Sent MAKO_CONNECT command to initiate handshake.")
    socket_udp.settimeout(2)
    try:
        data, addr = socket_udp.recvfrom(1024)
        print(f"Received response from RC: {data.hex()}")
    except socket.timeout:
        print("No response to MAKO_CONNECT; proceeding with handshake.")
    handshake_command_hex = "C0 A8 00 01 00 00 04 21 00 00 80"
    send_command_to_rc(handshake_command_hex)
    send_command_to_rc(handshake_command_hex)
    print("Sent initial handshake sequence.")

def send_idle_command():
    idle_command_hex = f"C0 A8 00 01 00 00 04 21 {IDLE_THROTTLE_COMMAND} {IDLE_THROTTLE_COMMAND} {CENTER_STEERING_COMMAND}"
    send_command_to_rc(idle_command_hex)
    print("Sent idle command to reset RC car.")

# Start the handshake process
initiate_handshake_with_rc()

try:
    while True:
        pygame.event.pump()
        throttle_axis = joystick.get_axis(3)
        steering_axis = joystick.get_axis(0)
        rc_command_hex = create_command_string(throttle_axis, steering_axis)
        send_command_to_rc(rc_command_hex)
        print(f"Sent command: {rc_command_hex}")
        ready_to_read, _, _ = select.select([socket_udp], [], [], 0.1)
        if ready_to_read:
            packet_data, packet_addr = socket_udp.recvfrom(1024)
            print(f"Received packet from {packet_addr}: {packet_data.hex()}")
        time.sleep(0.1)

except KeyboardInterrupt:
    send_idle_command()
    print("\nExiting.")
    pygame.quit()
    socket_udp.close()