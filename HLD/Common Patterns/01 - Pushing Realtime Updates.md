# Pushing Realtime Updates

## Problem

Consider Google Docs. When one user types a character, all other users viewing the document need to see change suddenly. Here we cant have the users polling the server for updates every few ms without crushing the infrastructure

## Solution

When system requires real-time updates, push notification etc, the solution requires two distinct pieces:

* how do we get updates from server to the client?
* how do we get updates from the source to the server?

### Client-Server Connection Protocols

Real-time systems frequently need persistent connections or clever polling strategies to enable servers to push updates to clients.

#### Networking Layers

The most important layers are
* Network Layer (Layer 3)
* Transport Layer (Layer 4)
* Application Layer (Layer 7)

##### Network Layer

* At this layer is IP, the protocol that handles routing and addressing.
* It is responsible for 
  * breaking data into packets
  * handling packet forwarding between networks
  * providing best effort delivery to any destination IP address
* There are no guarantees
  * packets can get lost
  * duplicated
  * or reordered along the way

##### Transport Layer

* At this layer is TCP and UDP, which provide the end-to-end communication service
  * *TCP is a connection-oriented protocol*: 
    * Before you can send data, you need to establish a connection with other side
    * It ensures that the data is delivered correctly and in order.
    * Gives guarantee but means connections
      * takes time to establish
      * resources to maintain
      * bandwidth to use
  * *UDP is a connectionless protocol*:
    * You can send data to any other IP address on n/w without any prior setup.
    * It doesn't ensures that the data is delivered correctly or in order.

##### Application Layer

At the final layer are the application protocols like DNS, HTTP, WebSockets, WebRTC.

#### Request LifeCycle

![Request Lifecycle](https://github.com/NikhilManu/System-Design/blob/main/images/HLD/Common%20Patterns/01%20-%20Pushing%20Realtime%20Updates/Request%20LifeCycle.png)

A series of steps happens when we type a URL into browser

* *DNS Resolution*: The client starts by resolving the domain name of website to an IP address using DNS (Domain Name System)
* *TCP Handshake*: The client initiates a TCP connection with server using a three-way handshake
  * SYN: The client sends SYN(synchronize) packet to server to request a connection
  * SYN-ACK: The server responds with a SYN-ACK packet to acknowledge the request
  * ACK: The client sends ACK packet to establish the connection
* *HTTP Request*: Once TCP conn is established, the client sends HTTP GET request to the server to request the web page.
* *Server Processing*: The server processes the request, retrieves the requested web page and prepares an HTTP response.
* *HTTP Response*: The server sends the HTTP response back to the client, which includes the requested web page content.
* *TCP Teardown*: After the data transfer is complete, the client and server close the TCP connection using four-way handshake
  * FIN: The client sends a FIN(Finish) packet to the server to terminate the connection.
  * ACK: The server acknowledges the FIN packet with an ACK.
  * FIN: The server sends a FIN packet to the client to terminate it side of the connection
  * ACK: The client acknowledges the server's FIN packet with an ACK.

<br>

Here the main two points to note are
* Each round trip between client and server adds latency to our request, including those to establish connections before we send out application data.
* Second, the TCP connection itself represents state that both the client and server must maintain
  * Unless we use features like HTTP keep-alive, we need to repeat this connection setup which a significant overhead.

##### With Load Balancers

Load balancers distribute incoming requests across these servers to ensure even load distribution and high availability.

Two main types of load balancers
* *Layer 4 Load Balancer*
* *Layer 7 Load Balancer*

###### L4 Load Balancer

* They operate on the *transport layer(TCP/UDP)*
* They make routing decisions based on network information like IP addresses and port, without looking at actual contents of packet
* The effect is as-if we randomly select backend server and assumed TCP connections were established directly between client and server

Key characteristics of L4 Load Balancers:
* Maintain persistent TCP connections between client and server
* Fast and efficient due to minimal packet inspection
* Cannot make routing decision based on application data
* Mostly used when raw perf is the priority

###### L7 Load Balancer

* They operate on the *application layer(HTTP)*
* They can examine actual content of each request and make intelligent routing decision

Key characteristics of L7 Load Balancers:
* Terminate incoming connectinos and create new ones to backend servers
* Can route based on request content (URL, header, cookies etc)
* More CPU-intensive due to packet inspection
* Provide more flexibility and features
* Better suited for HTTP-based traffic