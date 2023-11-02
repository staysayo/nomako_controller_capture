# UDP Communication Analysis Tasks

## Overview
The following tasks are based on the initial packet breakdown between an Android app and a Remote Controller (RC) over UDP. Each task is aimed at addressing gaps in the current understanding of the communication protocol and data packets.

## Analysis Tasks

### Documentation Tasks
- [ ] **Determine TTL Value:** Document the TTL value for the UDP packets.

### Research & Development Tasks
- [ ] **UDP Send Rate:**
  - [ ] Determine and document the average send rate in ms for packets sent from App to RC.
  - [ ] Determine and document the average send rate in ms for packets sent from RC to App.
- [ ] **Understanding the Handshake:**
  - [ ] Investigate and document the source of the IP address used in the handshake.
- [ ] **Battery Status Communication:**
  - [ ] Capture and analyze packets at different battery levels to determine the RC's battery status communication method.

### Analysis & Testing Tasks
- [ ] **Byte Analysis:**
  - [ ] Analyze the purpose and possible range of values for Bytes 5-10 in the message from RC to App.
  - [ ] Analyze the purpose and complete range of values for Bytes 11-12 in messages from App to RC and RC to App.
- [ ] **Command Variable Ranges:**
  - [ ] Document the observed min-max values for the command variables in Bytes 9 and 10 (forward and reverse commands).
  - [ ] Investigate how the TRIM function might alter Byte 11 (turn command) and document the findings.
- [ ] **Acknowledge Commands:**
  - [ ] Investigate why Byte 15 does not acknowledge the turn command as expected and document the findings.

### Validation Tasks
- [ ] **Constant Values Confirmation:**
  - [ ] Confirm through multiple packet captures whether Bytes 5-6 and Bytes 15-16 in the message from RC to App are indeed constants.

## Notes
- Ensure packet captures are taken in varied operational scenarios to confirm constants and variable ranges.
- Keep track of changes in the battery level and corresponding packet variations for accurate documentation.
```