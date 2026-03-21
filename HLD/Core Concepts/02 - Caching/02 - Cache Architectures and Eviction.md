# Cache Architectures

There are four cache patterns 

* Cache Aside (Lazy Loading)
* Write-Through Caching
* Write-Behind (Write Back) Caching
* Read-Through Caching

## Cache Aside (Lazy Loading)

Most Common caching pattern

1. Application checks the cache
2. If the data is there, return it.
3. If not, fetch the data from db, store it in cache and return it.

## Write-Through Caching

Application writes only to the Cache. The cache then synchronously writes to the database before returning to the application. The write operation doesnt complete until both cache and database are updated.

Some Problems are

* Slower writes, as application must wait for both cache and database write to complete.
* Dual-write problem, the cache updates but the db update fails then the system can become inconsistent.

Note: This architecture is less common as it requires special infra. Use this when reads must always return fresh data.

## Write-Behind (Write-Back) Caching

Application writes only to the Cache. The cache batches and writes the data to database asynchronously in the background.

This makes writes very fast, but introduces risk. If cache crashes before flushing, we can lose data. 

This is best when 
* occasional data loss is acceptable.
* We need high write throughput and eventual consistency is acceptable.

## Read-Through Caching

In Read-Through caching, the cache acts as a smart proxy. Our application never talks to the database directly. On a cache miss, the cache itself fetches from the database, stores the data and returns it

Ex: CDN

<br>

# Cache Eviction Policies

Strategy for removing entries from cache when full is called Eviction Policies.

## LRU (Least Recently Used)

* LRU evitcs the item that has not been accessed for the longest time.
* Default in many systems

## LFU (Least Frequently Used)

* LFU evicts the item that has been accessed the least.
* It maintains a counter for each key and removes the one with lowest frequency.

## FIFO (First in First Out)

* FIFO evicts the oldest item in the cache based on insertion time. 
* It can be implemented with simple queue, but it ignores usage pattern.

## TTL (Time to Live)

* TTL is not eviction policy by itself. 
* It sets an expiration time for each key and removes the entries that are too old. Often combined with LRU to balance freshness.
