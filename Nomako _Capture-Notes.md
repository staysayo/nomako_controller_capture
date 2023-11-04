# Packet Breakdown between App and RC

## UDP Connection Between Android App and RC

### UDP Details:
- **Port:** 8234
- **Flags:** Do not fragment
- **TTL:** 64
- **Connection Method:** Connected via Wi-Fi Direct (P2P)

## Plain Text Commands in UDP Payload

### MAKO_CONNECT (12B)
- **Hex:** `4D 41 4B 4F 5F 43 4F 4E 4E 45 43 54`
- **Behavior:** 
  - Sent after the Android device has connected to the WiFi AP of the RC named "NOMAD ND1_XXXXXX". 
  - The SSID is found on a sticker on the RC. 
  - Continuously sent every 1.264 ms (average observed send rate) until a packet from the RC is received.
- **Response:** The RC does not respond to this message directly.
- **Purpose:** Serves as an initial standby packet to the RC.
- **Insight:** Testing has shown that the first four bytes of the command (`C0 A8 00 01`), which resemble an IP address, can remain unchanged or match the sender's IP address without affecting the command's execution by the RC.

### MAKO_READ_BATT (14B)
- **Hex:** `4D 41 4B 4F 5F 52 45 41 44 5F 42 41 54 54`
- **Behavior:** 
  - Does not elicit a direct response from the RC.
  - Sent in 6000ms intervals, acting as a heartbeat.
- **App Functionality:** 
  - The Android app has a battery meter, presumably for reading the toy's battery status.
- **Programming Note:** 
  - This command is sent 500ms after the last message received from the RC or 6000ms after the last command sent from the app.

### MAKO_DISCONNECT (15B)
- **Hex:** `4D 41 4B 4F 5F 44 49 53 43 4F 4E 4E 45 43 54`
- **Behavior:** 
  - Disconnect command sent from the app in triplets.

### MAKO_LED1_ON (12B)
- **Hex:** `4D 41 4B 4F 5F 4C 45 44 31 5F 4F 4E`
- **Behavior:** 
  - Turn on accessory LED1 lights.

### MAKO_LED1_OFF (13B)
- **Hex:** `4D 41 4B 4F 5F 4C 45 44 31 5F 4F 46 46`
- **Behavior:** 
  - Turn off accessory LED1 lights.

### MAKO_LED2_ON (12B)
- **Hex:** `4D 41 4B 4F 5F 4C 45 44 32 5F 4F 4E`
- **Behavior:** 
  - Turn on accessory LED2 lights.

### MAKO_LED2_OFF (13B)
- **Hex:** `4D 41 4B 4F 5F 4C 45 44 32 5F 4F 46 46`
- **Behavior:** 
  - Turn off accessory LED2 lights.

## Remaining Bytes (in hex)

### Sent from App to RC (11B)
- **Hex:** `C0 A8 00 01  00 00  04 21  00 00 80`
- **Behavior:** 
  - Appears to be the initial part of a handshake sequence after establishing the UDP connection. 
  - The client sends two commands of `00 00 80` following the `MAKO_CONNECT`. 
  - It then goes into idle with `MAKO_READ_BATT` commands, acting as a heartbeat, until new movement commands are sent.
  - Average send rate: approximately 117.51 ms (748,883 bps).
- **Byte Analysis:** 
  - Bytes 1-4: Initially thought to be a constant resembling the IP address `192.168.1.1`. Updated analysis and testing reveal that these bytes can be variable and the RC will still process the command.
  - Bytes 5-6: Zeroes, likely padding, constant.
  - Bytes 7-8: Constant `04 21`.
  - Byte 9: Forward command variable, default `00`, with a min value of `2d` (45d) and a max of `e6` (230d).
  - Byte 10: Reverse command variable, default `00`, with a min value of `2a` (42d) and a max of `e6` (230d).
  - Byte 11: Turn command variable, ranges from `2e` (46d) (full left) to `80` (128d) (center) to `D2` (210d) (full right).

### Sent from RC to App (16B)
- **Hex:** `C0 A8 01 01  00 00 09 F8 00 00  64 65  00 00  00 00`
- **Behavior:** 
  - The RC appears to echo the commands sent by the app in the formats observed for other commands, acknowledging the forward and reverse command variables but not the turn variable. This echoing may serve as an acknowledgement during the initial handshake process.
  - Average send rate: approximately 13.83 ms (9,253,958 bps).
- **Byte Analysis:** 
  - Bytes 1-4: Constant, resembling IP address `192.168.1.1`.
  - Bytes 5-10: Appear to be constant; need confirmation.
  - Bytes 11-12: Variable, meaning currently unknown; complete range needs determining.
  - Bytes 13-14: Mimic the forward and reverse commands from the app, acting as acks.
  - Byte 15: Expected to ack the turn command but is always `00`.
  - Byte 16: Appears to be a constant `00`.

## Tasks and TODOs

- [x] Determine the average send rate for both the App to RC and RC to App messages.
- [x] Capture additional packets to confirm if Bytes 5-10 and 15-16 are constant.
- [x] Capture packets at different battery levels to analyze how battery status is communicated.
- [x] Complete the analysis of the variable bytes to determine their function and range.
- [x] Investigate the purpose of the `00 00 80` sequence in the handshake process.
- [x] Analyze the RC's echoing mechanism to determine if it is a standard acknowledgment or if it serves additional purposes.
- [x] Examine if there are any variations in the echoed commands under different operational conditions (e.g., low battery, signal loss).
- [ ] Determine the full sequence of commands and responses during the initial connection to establish a comprehensive view of the handshake protocol.
- [ ] Test the hypothesis that the `MAKO_READ_BATT` command functions solely as a heartbeat or if it carries additional synchronization or status information.
