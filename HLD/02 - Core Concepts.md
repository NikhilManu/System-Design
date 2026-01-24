## Core Concepts

Core concepts are the fundamental principles and techniques that form the foundation of every system design.

* Networking Essential
* API Design
* Data Modelling
* Database Indexing
* Caching
* Sharding
* Consistent Hashing
* CAP Theorem
* Numbers to Know

### Networking Essentials

At basic level we need to understand how services talk to each other and what happens when those connections fail or get slow.

* Most systems, default will be HTTP over TCP unless we have a specific reason to use something else
* WebSockets and Server Sent Events(SSE) come up when real-time updates are needed. Key difference 
  * SSE is for server-to-client push (live scores or notification)
  * WebSockets handle bidirectional communication (Chat)
  * SSE are simpler to implement and works better with standard HTTP infra.
  * WebSockets are necessary when clients need to push data back to server frequently.
  * Both are stateful connections. So we will need to think about connection persistence and what happens when a server goes down.
* gRPC is worth mentioning for internal service-to-service communication when performance is critical.
* Load balancing is another important topic
  * Layer 7 load balancers operate at the application level and can route based on actual HTTP request content
  * Layer 4 load balancers work at TCP level and are faster but dumber. They just distribute connections without looking at the content.
  * WebSockets typically need Layer 4 balancing because we're maintaining a persistent TCP connection.

### API Design

* For most questions, REST will be the way.
* When returning large result, pagination must be done. Cursor-based works better for real-time data where new items get added frequently
* For authentication, use JWT tokes for user sessions and API keys for service-to-service calls.
* Rate-limiting if tried to DDOS.

### Data Modelling

* SQL vs NoSQL
  * SQL works great when we have structured data with clear relationships and need *strong consistency*
  * NoSQL works great when we need flexible schemas or you need to scale horizontally across many servers without complex joins
* Normalization and denormalization
  * Normalization means splitting data across table to avoid duplication. This keeps the data consistent but means we need to join to get complete data.
  * Denormalization means we duplicate data to avoid joins and make reads faster. The downside is updates. For read-heavy systems where data changes rarely, the tradeoff is often worth it
* NoSQL requires you to design your partition key and sort key based on your access patterns. So you have to know your queries upfront and design around them.

### Database Indexing

* Indexes are used to make db queries fast
* The most common index is B-tree.
  * It keeps data sorted in tree structure that supports both exact lookups and range queries.
* Hash Indexes are faster for exact matches but can't do range queries so they are less common.
* Propose indexes on the fields which will be queried frequently.
* ElasticSearch for full-text Search
* PostGIS extension for geospatial queries
  
### Caching

* Store frequently accesssed data in fast memory so that we can skip the db reads
* Reduce the load on the db, letting it handle more write traffic and avoiding the need to scale it prematurely
* Cache invalidation is hardest part. Some strategies are
  * Invalidate cache entry immediately after writes
  * Use short TTLs and accept some staleness
  * Or combine both approaches
* What happens when cache failures (Cache Stampede), now every request suddenly hits the database and take down the whole system. Some approaches are  
  * Keeping small in-process cache as a fallback
  * Using circuit breakers to prevent overwhemling the database
  * accepting degraded performance until Redis comes back up
* CDN caching is different, its for static assets like images, videos and JS files served from edge locations close to users

In process caching works for small values that change rarely, but for core application data, external caching with Redis is the default

### Sharding

* Sharding comes up when we need to split data across multiple independent servers. This happens when we hit
  * Storage limits
  * write throughput limits
  * read throughput limits that even replicas can't handle

* Most important decision is the shard key. This determines how data gets distributed
  * For instagram, if you shard by user_id, all the user-scoped queries will be fast as the hit one shard. But the global queries will become expensive as we have to hit multiple shards. That's the tradeoff
  * Most systems use hash-based sharding where you hash the shard key and use modulo to pick a shard. This distributes data evenly and avoids hot spots.
  * Range based sharding can work if access patterns naturally paritition.
  * Directory based sharding uses a lookup table to decide where data lives. It is flexible addes dependecy and latency, so its rarely worth it in interviews
* Cross-shard transactions becomes nearly impossible, so design your shard boundaries to avoid them. Resharding is painful

### Consistent Hashing

  When using simple hash-based distrubution ( hash(key) % N ) to pick server, adding or removing a server change the N. This means almost every key now maps to a different server, so we would have to move the data around

* Consistent hashing fixes this by arranging both servers and key on a virtual ring. We hash each key and place it on a ring, then the key belongs to next server encounter when going clockwise
  * When a server is added, only the keys between the new server and the previous server need to move
  * When a server is removed, only its key relocate to the next server on the ring.

### CAP Theorem

* It states you can have only two of three properties at once
  * Consistency :- All nodes see the same data
  * Availability :- Every request gets a response
  * Partition Tolerance :- System works even when network connections fail between nodes
* Since network partitions are unavoidable in distributed systems, we are really choosing between consistency and availability
* For most systems, availability is the right default. Users can tolerate seeing slightly stale data. Ex: Instagram
* Strong consistency matters when stale data causes buisness isssues. Ex Banks
* In interviews, when asked about consistency. The safe answer is eventual consistency unless problem involves money or booking limited resource

### Numbers to know

![Numbers to Know](https://github.com/NikhilManu/System-Design/blob/main/images/HLD/Numbers%20To%20Know.png)