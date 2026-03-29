# Challenges of Sharding

* Hot spots and Load Imbalance
* Cross-Shard Operations
* Maintaining Consistency

### Hot Spots and Load Imbalance

Even with good shard key, some shard can end up handling way more traffic than others. This is called hot spot.

Most common causes are 
* Celebrity Problem
* Time Based sharding

Handling hot spots
* Isolate hot keys to dedicated shards
* Use compound shard keys: Sharding by hash(user_id + date). This helps spread across multiple shards
* Dynamic Shard Splitting

### Cross-Shard Operations

We can't eliminate the cross-shard queries entirely, but we can minimize them
* Cache the results
* Denormalize to keep related data together: if we frequently need to query post along with user data, store some post information directly on user's shard. Yes this duplicates data, which is often worth the trade-off.
* Accept the hit for rare queries

Note: Cross-shard operations are signal that something in our design need rethinking. Interviewers expect us to minimize cross-shard queries, not just accept them as inevitable.

### Maintain Consistency

When data lives on single database, transactions are straight-forward. The database handles the consistency guarantee.

Sharding breaks this. The textbook solution is to
* Two-Phase Commit (2PC)
* Saga Series

How to Handling consistency issues ?

* Design to avoid cross-shard transactions
* Use Sagas for multi-shard operations
* Accept eventual consistency

## Sharding in Modern Databases

Most modern distributed databases handle sharding automatically.

For SQL Databses
* Vitess and Citus are popular open-source sharding layers that we use for Postgres or MySQL
* They handle query routing, cross-shard operations and resharding
* Cloud Providers like AWS Aurora and Google Cloud Spanner offers distributed SQL with built in sharding.

<br>

Common NoSQL databases also lets us specify a partition key and handle the rest. They automatically rebalance when we add capacity and route queries to right shards
* Cassandra uses a partitioner with virtual nodes, which is a form of consistent hashing to map partition keys to token ranges on nodes.
* DynamoDB hashes the partition key to route items to internal partitions and splits/merges partitions as they grow.
* MongoDB shards data into range based chunks on the shard key.

## When to Mention Sharding

We need to establish why a single database won't work first.

* Storage: We have 500M users with 5KB of data each, that's 2.5TB. A single postgres instance can handle that, but if we grow 10x we'll need to shard.
* Write throughput: "We're expecting 50k writes per second during peak. A single database will struggle with that write load, so we should shard
* Read throughput: Even with read replicas, if we're servin 100M DAU making multiple queries each, we'll need to distribute the read load across shards.
