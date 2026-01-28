## Pushing via Pub/Sub

We have a single service that collects update from source and then broadcast them to all the interested clients.

Popular options are Kafka and Redis

![Pub/Sub Message sending](https://github.com/NikhilManu/System-Design/blob/main/images/HLD/Common%20Patterns/01%20-%20Pushing%20Realtime%20Updates/Pub-Sub.png)

When client connects we dont need them to connect to a specific endpoint server and instead can connect to any of them. Once connected, the endpoint server will register client with the pub/sub server.

On connection side, the following happens
1. The client establishes a connection with an endpoint server
2. The endpoint server registers the client with the Pub/Sub service
   1. often they create a topic and subscribe to it.
   2. They also keep a mapping from topics to the connections associated with them

On the update broadcasting side, the following happens
1. Updates are pushed to the Pub/Sub service to the relevant topic
2. The Pub/Sub service broadcast the update to all the client subscribed to the topic
3. The endpoint server receives the update, looks up which client is subscribed to that topic and forwards the update to the client over existing connection

#### Advantages

* Managing load on endpoint server is easy, we can use simple load balancer with "least connection" strategy
* We can broadcast updates to a large numbe of clients efficiently
* We minimize the proliferation of state through our system

#### Disadvantages

* We don't know whether subscribers are connected to the endpoint server, or when they disconnect
* The Pub/Sub service becomes a single point of failure and bottleneck.
* We introduce an additional layer which can add latency
* There exist many-to-many connections between Pub/Sub service hosts and the endpoint servers

### When to use Pub/Sub?

* When we need to broadcast updates to large number of clients. 
* When we dont need to respond to connect/disconnect events 
* When we dont maintain a lot of state associated with a given client

### Things to discuss

* Single point of failure and bottleneck of Pub/Sub Service.
  * Redis cluster is a popular way to scale pub/sub service which involves sharding the subscriptions by the key across multiple hosts.
* Pub/sub clusters create many-to-many links between brokers and endpoint servers. 
  * Keep the cluster small or partition topics so each endpoint only connects to shard it needs.
* For inbound connections we can use a load-balancer with "least connection" strategy