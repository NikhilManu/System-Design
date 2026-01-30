# Scaling Reads

Scaling Read addresses the challenge of serving high-volume read requests when your application grow fron hundreds to millions of users.

## Solution

Read scaling follow a natural progression from simple to complex distributed system.
1. Optimize read performance within database
2. Scale database horizontally
3. Add external caching layers

### Optimize within Database

#### Indexing

* Index is a sorted lookup table that points to rows in your actual data.
* When index is not present, the database performs a full table scan which is very expensive.
* Index turns O(n) operation into O(log n) operation
* Most common types of indexes are
  * B-tree being most common for general queries
  * Hash Indexes work well for exact matches
  * Specialized Indexes handle full-text or geographic queries

*Note*: You'll read outdata resources warning about "too many indexes" slowing down writes. While Index overhead is real, the fear is overblown.

#### Hardware Upgrades

Sometimes the answer is just better hardware. This won't solve every problem, but it's often the fastest way to buy yourself some breathing room.

#### Denormalization Strategies

Normalization is process of structuring data to reduce redundancy by splitting information across multiple tables to avoid storing duplicate data. It makes queries more complex because we need joins to bring related data back together.

For read-heavy systems, denormalization trades storage for speed. 

Denormalization is classic ex of optimizing reads at the expense of writes. Always consider read/write ratio before denormalizing. If writes are frequent, the complexity may not be worth it.

#### Scale Database Horizontally

* When a single DB server hits its limits, add more server. 
* General rule of thumb is DB will need to scale horizontally when we exceed 50k - 100k requests per second (Assuming we already have index)

##### Read Replicas

* Read Replicas copy data from primary db to additional severs. All writes go to the primary but reads can go to any replica. This distributes read load.
* They also provide redundancy as nice benifit. If primary fails, you can promote replica to become new primary
* Leader-follower replication is standard approach. Replication can be synchronous (slower but consisten) or asynchrounous (faster but potential stale data)

##### Database Sharding

If well-indexed queries are slow, sharding can help by splitting data across multiple databases

Sharding helps in two main ways
* Smaller dataset means faster individual queries
* Distribution of read load across multiple databases

Functional Sharding splits data by buisness domain or feature rather than by records.

Geographic Sharding is effective for global read scaling. 

However sharding adds significant operational complexity and is primarily a write scaling technique.


#### Add External Caching Layers

Most application exhibit highly skewed access patterns. Caches exploit this pattern by storing frequently accessed data in memory.

##### Application-Level Caching

In-memory cache like Redis sit between our application and database. When app needs data, it check the cache first. On a hit, you get fast response. On a miss, we query the database and populate the cache.

This pattern works because frequently used data stays in cache while less frequently accessed data falls back to database

Cache invalidation remains primary challenge. Common Strategies are
* Time based expiration(TTL): Set a fixed life for cached entries.
* Write through invalidation: Updates or delete cache immediately when writing to the database. Ensures consistency but adds latency to write operations and requires careful error handling
* Write behind invalidation: Queue invalidation events to process asynchronosly.
* Tagged Invalidation: Associate cache entries with tags. Invalidate all entries with specific tag when related data changes.
* Versioned Keys: Include version number in cache keys. Simple and reliable but requires version tracking

##### CDN and Edge Caching

Content Delivery Networks extend caching beyond data center to global edge locations. Modern CNDs cache dynamic content including API responses and database query results.

Geographic distribution provides dramatic latency improvements. This reduces times from 200ms to under 10ms while completely eliminating load on our origin servers.

Trade-off is managing cache invalidation across scores of edge locations. The performance gains, usually justify the extra work.