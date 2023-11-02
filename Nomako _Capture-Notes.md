# Packet Breakdown between App and RC

## UDP Connection Between Android App and RC

### UDP Details:
- **Port:** 8234
- **Flags:** Do not fragment
- **TTL:** 64
- **Connection Method:** Connected via Wi-Fi Direct (P2P)

## Plain Text Commands in UDP Payload

### MAKO_CONNECT (12B)
- **Hex:** `4d 41 4b 4f 5f 43 4f 4e 4e 45 43 54`
- **Behavior:** 
  - Sent after the Android device has connected to the WiFi AP of the RC named "NOMAD ND1_XXXXXX". 
  - The SSID is found on a sticker on the RC. 
  - Continuously sent every 45ms until a packet from the RC is received.
- **Response:** The RC does not respond to this message directly.
- **Purpose:** Serves as an initial standby packet to the RC.

### MAKO_READ_BATT (14B)
- **Hex:** `4d 41 4b 4f 5f 52 45 41 44 5f 42 41 54 54`
- **Behavior:** 
  - Does not elicit a direct response from the RC.
  - Sent in 6000ms intervals, acting as a heartbeat.
- **App Functionality:** 
  - The Android app has a battery meter, presumably for reading the toy's battery status.
- **Programming Note:** 
  - This command is sent 500ms after the last message received from the RC or 6000ms after the last command sent from the app.

### MAKO_DISCONNECT (15B)
- **Hex:** `4d 41 4b 4f 5f 44 49 53 43 4f 4e 4e 45 43 54`
- **Behavior:** 
  - Disconnect command sent from the app in triplets.

## Remaining Bytes (in hex)

### Sent from App to RC (11B)
- **Hex:** `c0 a8 01 01  00 00  04 21  00 00 80`
- **Behavior:** 
  - Part of a handshake after establishing the UDP connection.
  - TODO: Determine the average send rate in ms.
- **Byte Analysis:** 
  - Bytes 1-4: Constant, resembling IP address `192.168.1.1`.
  - Bytes 5-6: Zeroes, likely padding, constant.
  - Bytes 7-8: Constant `04 21`.
  - Byte 9: Forward command variable, default `00`, with a min value of `2d` and a max of `e6`.
  - Byte 10: Reverse command variable, default `00`, with a min value of `2a` and a max of `e6`.
  - Byte 11: Turn command variable, ranges from `2e` (full left) to `80` (center) to `D2` (full right).

### Sent from RC to App (16B)
- **Hex:** `c0 a8 01 01  00 00 09 f8 00 00  64 65  00 00  00 00`
- **Behavior:** 
  - Acknowledges the forward and reverse command variables but not the turn variable.
  - TODO: Determine the average send rate in ms.
  - TODO: Capture more packets at different battery levels to understand battery status communication.
- **Byte Analysis:** 
  - Bytes 1-4: Constant, resembling IP address `192.168.1.1`.
  - Bytes 5-10: Appear to be constant; need confirmation.
  - Bytes 11-12: Variable, meaning currently unknown; complete range needs determining.
  - Bytes 13-14: Mimic the forward and reverse commands from the app, acting as acks.
  - Byte 15: Expected to ack the turn command but is always `00`.
  - Byte 16: Appears to be a constant `00`.

## Tasks and TODOs

- [ ] Determine the average send rate for both the App to RC and RC to App messages.
- [ ] Capture additional packets to confirm if Bytes 5-10 and 15-16 are constant.
- [ ] Capture packets at different battery levels to analyze how battery status is communicated.
- [ ] Complete the analysis of the variable bytes to determine their function and range.
