# README

## Description

Main script for controlling a Remote-Controlled (RC) car via UDP using a joystick.

## Comments and Tags

### `version`

1.1.0 - Added structured comments for documentation generation

### `author`

Neal Wallace

### `date`

11/04/2023

### `details`

Establishes a non-blocking UDP socket to communicate with the RC car.

### `network_details`

IP: 192.168.0.1, Port: 8234, Connection: Wi-Fi Direct (P2P), TTL: 64, Flags: Do not fragment

### `dead_zones`

Forward/Reverse: 0.05, Steering: 0.15

### `defaults`

Idle throttle command: "00", Center steering command: "80"

### `behavior`

Ignores any input_value that falls within the specified dead_zone_threshold.

### `insight`

By adjusting the dead_zone_threshold, we can fine-tune the responsiveness of the joystick input.

### `todo`

Fine-tune dead zone values based on user feedback or empirical testing.

### `behavior`

Handles negative values for left steering and positive for right steering.

### `insight`

The mapping accounts for the dead zones and scales the input to the expected command range.

### `todo`

Consider implementing a non-linear mapping for more intuitive control.

### `behavior`

Constructs a command string with separate forward and reverse commands, as well as steering.

### `insight`

Commands are formed by concatenating hex values representing different control signals.

### `todo`

Implement additional commands for other functionalities such as lights and horn.

### `behavior`

Converts the hex string into bytes and transmits the command via the UDP socket.

### `insight`

This is the direct interface with the RC car, where commands are executed.

### `todo`

Implement error handling for network errors or failed transmissions.

### `handshake_process`

Sends the MAKO_CONNECT command and listens for any acknowledgment.

