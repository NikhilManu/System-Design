## Pushing Via Consistent Hashes

In many of the client update mechanism (polling, SSE, Websockets) the client has a persistent connection with a server and the server is responsible for sending updates.

Ideally when a message needs to be sent to X, we need to
1. Figure out which server X is connected to
2. Send the message to that server
3. That server will lookup which request is associated with X
4. The server will then write the message via appropriate connection.

There are two ways to handle this situation
* Simple Hashing
* Consistent Hashing

### Simple Hashing

This approach is to use simple modulo function to determine which server is responsible for a given user. So we have 1 server who owns the connection for a User.

We will have a central service who knows the number of servers and can assign them each a number 0 to N-1. Apache Zookeeper does this.

When client initally connects, we can either
* Directly connect them to the appropriate server
* Have them randomly connect to a server and have the server redirect them to the appropriate server based on the internal data.

<br>

When client connects, the following happens
* The client connects to random server
* The server looks up the clients hash in Zookeeper to figure out which server is responsible for them
* The server redirects client to appropriate server
* The client connects to correct server
* The server adds that client to map of connections.

This approach works because we always know that a single server is responsible for a given User. 

This works great when N is fixed, but becomes a issue when we need to scale up, as changing the number servers will require almost all the users to reconnect to different servers.

### Consistent Hashing

This approach maps both server and users onto a hash ring, and each users connects to the next server they encounter while moving clockwise around the ring.

#### Advantages

* Predictable Server assignment
* Minimal connection disruption during scaling
* Works well with stateful connections
* Easy to add or remove servers

#### Disadvantages

* Complex to implement correctly
* Requires coordination service (like Zookeeper)
* All servers need to maintain routing information
* Connection state is lost if server fails

#### When to use Consistent Hashing?

Ideal when you need to maintain persistent connections and your system needs to scale dynamically.

Its valuable when each connection requires significant server-side state that would be expensive to transfer between servers.


#### Things to discuss

When using this method you should also talk about the orchestration logic necessary to make it work. 
* Signaling the beginning of a scaling event. Recording both old and new server assignments
* Slowly disconnecting clients from old server and having them reconnect to their new assigned server
* Signaling the end of scaling event and updating the coordination server with new server assignments
* In the interim, having messages which are sent to both the old and new server until they're fully transitioned