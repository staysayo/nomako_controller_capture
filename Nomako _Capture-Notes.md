# Packet Breakdown between App and RC

## UDP connection between Android app and RC
- Port: 8234
- Flags: Do not fragment
- TTL: 
- Connected via Wi-Fi Direct (P2P)

## Plain Text Commands in UDP Payload

### MAKO_CONNECT (12B)
- Hex: `4d 41 4b 4f 5f 43 4f 4e 4e 45 43 54`
- Description:
  - Seen after the Android device has connected to the WiFi AP of the RC named "NOMAD ND1_XXXXXX," which is also found on a sticker on the RC.
  - This message is also sent every 45ms until it receives a packet from the RC.
  - RC does not seem to respond to this message directly.
  - Seems to serve as an initial standby packet communication to the RC.

### MAKO_READ_BATT (14B)
- Hex: `4d 41 4b 4f 5f 52 45 41 44 5f 42 41 54 54`
- Description:
  - Does not directly elicit a response from the RC.
  - The Android app has a battery meter and presumably reads the toy battery. This command does not seem to return a battery level.
  - Sent in 6000ms intervals that act as a heartbeat.
  - Programming Note: This command is sent 500ms after the last message received from the RC or 6000ms after the last command sent from the app.

### MAKO_DISCONNECT (15B)
- Hex: `4d 41 4b 4f 5f 44 49 53 43 4f 4e 4e 45 43 54`
- Description:
  - Disconnect command.
  - Seems to be sent from the app in triplet.

### Remaining Bytes (in hex)
- `c0 a8 01 01  00 00  04 21  00 00 80`
- Description:
  - Sent from App to RC (11B).
  - TODO: Add send rate in ms (what's the avg time this message is sent?).
  - This exact payload is sent as part of a handshake between the app and RC after the UDP connection is established.
  - Bytes 1-4 resemble IP address 192.168.1.1 in decimal format. Uncertain where the IP came from as the WiFi P2P handshake is not yet understood.
  - Bytes 5-6 are always 0's, likely padding (constant).
  - Bytes 7-8 are always `04 21` (constant).
  - Byte 9 is the forward command variable, defaults to `00`.
  - Byte 10 is the reverse command variable, defaults to `00`.
  - Byte 11 is the turn left and right command variable, defaults to `80` (likely the center of the range). This default can likely be changed with the "TRIM" function in the app, which is used to center the steering.

- `c0 a8 01 01  00 00 09 f8 00 00  64 65  00 00  00 00`
- Description:
  - Sent from RC to app (16B).
  - TODO: Add send rate in ms (what's the avg time this message is sent?).
  - The RC acknowledges the forward and reverse command variables received but not the turn variable.
  - TODO: Capture more packets at a different battery level to figure out how the RC communicates battery status.
  - Bytes 1-4 resemble IP address 192.168.1.1 in decimal format. Uncertain where the IP came from as the WiFi P2P handshake is not yet understood.
  - Bytes 5-10: TODO (appear to be constant in all packet captures so far).
  - Bytes 11-12: TODO (not constant, values appear random at times).
  - Bytes 13-14 mimic the forward and reverse commands sent from the app. Byte 13 is the ack for the last Forward command received, and Byte 14 is the ack for the last Reverse command received. Follows the same limitations in the programming notes of the Forward and Reverse commands sent from the app.
  - Byte 15: Expected to be the ack byte for the Turn command sent from the app but is always `00` (appears constant).
  - Byte 16: Appears constant `00`.
```