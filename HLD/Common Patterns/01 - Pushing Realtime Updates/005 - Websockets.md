## WebSockets: The Full-Duplex Champion

Websockets are go-to choice for bi-directional communication between client and the server. Especially if we have high freq writes and reads.

### How websockets works?

* Websockets build on HTTP through "<b>upgrade</b>" protocol, which allows TCP connection to change L7 protocol.
* Since it changes L7 protocol, we can use some session information like cookies, header

Once connection is established both clients and server can send "messages" to each other.
1. Client initiates Websockets handshake over HTTP
2. Connection upgrades to Websocket protocol
3. Both client and server can send messages
4. Connection stays open till explicitly closed

### Extra Challenges

Websocket connections are persistent connection, so out infra needs to support it
* Some L7 Load balancers do support it but generally not that good. (L7  LB doesnt guarantee same TCP connection for each incoming request)
* L4 Load Balancers will support websockets natively since same TCP connection is used for each request

<br>

When we have long running-connections, deployments are an issue. There two ways to deal with this
* Sever all old connection and have them reconnect
* Let the new servers take over and keep the connection alive.

First one is more simpler, but does have some effect on the persistence. Also we should handle situations where client may have missed updates due to being disconnected

Due to many issues with stateful connection, it is generally better to create a Websocket service which handle the connection management and scaling. This allows rest of system to remain stateless.

![Websocket architecture](https://github.com/NikhilManu/System-Design/blob/main/images/HLD/Common%20Patterns/01%20-%20Pushing%20Realtime%20Updates/WebSocket%20Architecture.png)


#### Advantages

* Full duplex (read and write) communication
* Lower latency than HTTP due to reduced overhead
* Efficient for frequent messages
* Wide browser support

#### Disadvantages

* More complex to implement
* Requires infrastructure
* Statefull connection, can make load balancing and scaling more complex
* Need to handle reconnection.

### When to use WebSockets?

Generally, if we need high-frequency bi-directional communication. It is better to use Websockets.

Note: <b>Another common pattern is to have SSE subcriptions for updates and do writes over simple HTTP whenever they occur</b>