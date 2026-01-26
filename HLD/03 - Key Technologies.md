## Key Technologies

Key technologies that are relevant are

* Core Database
  * Relational Databases
  * NoSQL Databases
* Blob Storage
* Search Optimized Database
* API Gateway
* Load Balancer
* Queue
* Streams / Event Sourcing
* Distributed Lock
* Distributed Cache
* CDN

### Core Database

* For product design interview, general recommendation will be a relational database
* For infrastructure design interviews, general recommentation will be a NoSQL database

Note: Dont try to compare NoSQL and SQL databases as these technologies are highly overlapping. (Both can work great for scaling (SQL) and also relationships (NoSQL))

*If asked to compare "Postgres is used here because its ACID properties will allow data integrity" is great point*

#### - Relational Databases

Often used for transactional data (eg: user record)

Important features are
* SQL Joins
* Indexes (B-Tree or Hash Table)
* Transactions: Grouping multiple operations into a single atomic operation

#### - NoSQL Databases

These databases do not use traditional table-based structure and are often schema-less.

Allows to handle large volumes of unstructured, semi or structured data and to scale horizontally with ease

They are best in situations where
* *Flexible Data Models*: Data model is evolving or need to store different types of data
* *Scalability*: Application needs to scale horizontally (across many servers) or high user load
* *Handling Big Data and Real-Time Web Apps*: Application with large volumes of data or application requiring real-time data processing

Things to know about NoSQL databases
* *Data Models*
  * Key-value stores
  * Document stores
  * column-family stores 
  * graph databases
* *Consistency Model*: offers various consistency model ranging from strong to eventual consistency
* *Indexes* (B-Tree or Hash Table)
* *Scalability*: NoSQL databases scale horizontally by using consistent hashing or sharding to distribute data across many servers
  
### Blob Storage

For storing large, unstructured blobs of data. This could be images, videos or other files. These are cost effective that traditional databases

They work in conjuction with CDNs, so to get fast downloads from anywhere in the world

Things to konw about blob
* Durability: Highly Durable even if disk or server fails
* Scalability: They are highly scalable
* Cost: Cost effective
* Security: Built-in security features and access control features
* Upload and download directly from Client
* Chunking: When uploading large files, it common to use chunking to upload the file in smaller pieces.

### Search Optimized Database

Designed to handle full-text search using techniques like indexing, tokenization and stemming. They work by building inverted Indexes. 


Things to know about Search Optimized Databases
* *Invereted Indexes*: These are data structure that map from words to document that contain them.

```
{
    "word1": [doc1, doc2, doc3],
    "word2": [doc2, doc3, doc4]
}
```
* Tokenization: Process of breaking a piece of text into individual words. This allows to map for inverted indexes
* Stemming: Process of reducing words to their root form.
  * Ex: running and runs would be reduced to run
* Fuzzy Search: Ability to find results that are similar to given search term.
* Scaling: These databases scale by adding more nodes to a cluster and sharding data across those nodes.

### API Gateway

API gateway sits in front of the system and is responsible for routing incoming requests to appropriate backend service.

### Load Balancer

When having large amount of traffic, we will need to distribute that traffic across multiple machines to avoid overloading single machine

Sometime we will need to have specific features from load balancer
* Sticky Sessions
* Persistent Connections

The most common decision is to make is whether to use and L4 (layer4) or L7 (layer 7) load balancer
* Persistent Connections like Websockets, then mostly L4 load balancer
* L7 offers great flexibility in routing traffic to different services while minimizing the connection downstream

### Queue

Couple of common use cases for queues:
* *Buffer for Bursty Traffic*: A queue buffers incoming request during peak hours, allowing them to process at manageable rate without overloading the server
* *Distribute Work Across a System*: Queues can be used to distribute expensive image processing tasks. 

Things to know about queues:
* Message Ordering (FIFO and complex ordering guarantees)
* Retry Mechanisms
* Dead Letter Queues: These queues are used to store messages that cannot be processed. Usefull for debugging and auditing.
* Scaling with Partitions: Queues can be partitioned across multiple servers so that they scale to handle more messages.
* Backpressure: Way of slowing down the production of messages when the queue is overwhelmed. (Potentially returning an error to user)

### Streams / Event Sourcing

Technique where changes in application state are stored as sequence of events.

*Note*: Unlike Message Queues, streams can retain data for a configurable period of time, allowing users to read and re-read messages.

* *When you need to process large amount of data in real-time*
* *When you need to support complex processing scenarios like event sourcing*
* *When you need to support multiple consumers reading from same stream*
  
Things to know abuot streams:
* Scaling with Partitioning
* Multiple Consumer Groups: Streams can support multiple consumer groups, allowing consumer to read from the same stream independently.
* Replication: In order to support fault tolerance.
* Windowing: Way of grouping events together based on time or count

### Distributed Lock

Traditional Databases with ACID properties use transaction locks to keep data consistent, but they're not designed for longer term locking. This is where distributed locks come in handy (Ex: Concert ticket)

Common examples of when to use a distributed lock
* *E-commerce Checkout System*: Locking high demand item during checkout
* *Ride-Sharing Matchmaking*: Locking nearby driver, which prevents them from being matched with multiple riders
* *Distributed Cron jobs*: Lock ensures that a task is executed by only one server at a time.
* *Online Auction Bidding System*: lock can be used during the final moments of bidding to ensure that when a bid is placed in last second, the system locks the item briefly to process the bid and update the current highest bid.

Things to know abuot distributed locks
* *Locking Mechanisms*: Most common implementation of this uses Redis and is called Redlock. Redlock uses multiple Redis instances to ensure that a lock is acquired and released in a safe consistent manner
* *Lock Expiry*: These locks can be set to expire after a certain amount of time.
* *Locking Granularity*: These locks can be used to lock a single or group of resources.
* *Deadlock*


### Distributed Cache

Distributed cache is just a server or cluster of servers, that stores data in memory. They are great for storing data thats expensive to compute.

We want to use a cache when:
* *Save Aggregated Metrics*
* *Reduce Number of DB Queries*
* *Speed up Expensive Queries*

Things to know about distributed caches:
* *Eviction Policy*: Some common eviction policies are
  * LRU
  * FIFO
  * Least Frequently Used (LFU)
* *Cache Invalidation Strategy*
* *Cache Write Strategy*: Makes sure data is writtent to cache in a consistent manner. Some strategies are
  * Write-Through Cache: Write data to both the cache and datastore simultaneously. Ensure consistency but slower for write operations.
  * Write-Around Cache: Write data directly to datastore, bypassing the cache. Minimizes cache pollution but might increase data fetch time on subsequent reads.
  * Write-Back Cache: Writes data to the cache and then asynchronously writes the data to the datastore. This is faster for write operations but can lead to data loss if cache fails before the data is written to datastore.

### CDN

A content delivery network(CDN) is a type of cache that uses distributed servers to deliver content to user based on their location. Often used to deliver static content like images, videos and HTML files. But they can be also used for dynamic content like API Response.

They work by caching content on servers that are close to users. If the content is not cached, the CDN will fetch from server, cache it on server and then give the content to user.

Things to know about CDNs:
* *CDNs are not just for static assets*: They are especially useful for dynamic content which is accessed frequently but changes infrequently
* *CDNs can be used to cache API responses*
* *Eviction Policies*