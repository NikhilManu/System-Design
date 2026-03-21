# Caching Problems

The most common problems that arises are
* Cache Stampede (Thundering Herd)
* Cache Consistency
* Hot Keys

## Cache Stampede

* A cache stampede happens when a cache entry expires and many requests try to rebuild it at the same time.
* A brief window, where every request misses the cache and goes straight to the database.

![Cache Stampede](https://github.com/NikhilManu/System-Design/blob/main/images/HLD/Core%20Concepts/02%20-%20Caching/Cache%20Stampede.png)

#### How to Handle it ?

* <b>Request Coalescing (Single Flight)</b>: Allows only one request to rebuild the cache while others wait for the result. Most effective solution.
* <b>Cache Warming</b>: Refresh popular keys proactively before they expire. This only helps when using TTL-based expiration. If we invalidate cache on writes, warming does not prevent stampede

## Cache Consistency

These happen when the cache and database return different values for the same request. This is common because most read from cache and write to database first. That creates a window where the cache still holds stale data.

#### How to Handle it ?

* <b>Cache Invalidation on Writes</b>
* <b>Short TTLs for stale tolerance</b>: Let slightly stale data live temporarily if eventual consistency is acceptable.
* <b>Accept Eventual Consistency</b>

## Hot Keys

A Hot key is a cache entry that receives a huge amount of traffic compared to everything else. Even if Cache hit rate is high, a single hot key can overload one cache node

#### How to Handle it ?

* <b>Replicate Hot Keys</b>: Store the same value on multiple cache nodes and load balance reads across them.
* <b>Add a local fallback cache</b>: Keep extremly hot values in process to avoid pounding Redis
* <b>Apply Rate Limiting</b>: Slow down abusive traffic patterns on specific keys.