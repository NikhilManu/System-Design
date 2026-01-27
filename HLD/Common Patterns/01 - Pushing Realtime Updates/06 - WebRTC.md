## WebRTC: The Peer-to-Peer Solution

WebRTC enables direct peer-to-peer communication between browsers. Perfect for video/audio calls and data sharing like document editors.

Client talk to a central "Signaling Server" which keeps track of which peers are available together with their connection information. Once a client has information they can try to establish direct connection without any intermediary servers.

The WebRTC standard includes two methods
* *STUN*: "Session Traversal Utilities for NAT" is a protocol and techniques which allows peers to establish publically routable addresses and ports
* *TURN*: "Traversal Using Relay around NAT" is a relay service, a way to bounce requests through a central server which can then be routed to the appropriate peer.   

![WebRTC setup](https://github.com/NikhilManu/System-Design/blob/main/images/HLD/Common%20Patterns/01%20-%20Pushing%20Realtime%20Updates/WebRTC%20setup.png)

### How WebRTC works?

1. Peers discover each other through signaling server
2. Exchange connection information
3. Establish direct peero connection, using STUN/TURN if needed.
4. Stream audio/video or send data directly

### When to use WebRTC?

Its a overkill for most real-time update use cases, but its a great tool for scenarios like video/audio call, screen sharing and gaming.

#### Advantages

* Direct peer communication
* Lower latency
* Reduced server costs
* Native audio/video support

#### Disadvantages

* Complex setup
* Requires signaling server
* NAT/Firewall issues
* Connection setup delay