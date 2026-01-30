### When to use?

Look at each of our external API requests, and for the high-volume ones. Start with query optimization, then move to caching and read replicas.

### When not to use?

* Write-heavy systems
* Small scale applications
* Strongly consistent systems
* Real-time collaborative systems

## Common Deep Dives

### What happens when your queries start taking longer as dataset grows?

The issue in most cases is without proper indexing, the database performs a full table scan. This problem compound with joins. Just add indexes on columns you query frequently.

### How do you handle millions of concurrent reads for the same cached data?

The first solution is <b>Request Coalescing</b> - basically combining multiple requests for the same key into a single request. This helps when backend can't handle the load of everyone asking for the same thing at once.

When coalescing isn't enough for extreme loads, we need to distribute the load itself.

Cache key fanout spreads a single hot key across multiple cache entries. Clients randomly pick one. We can do this by appending a random number to the key. The trade-off with fanout is memory usage and cache consistency. 

But for read-heavy scenarios where hot-key problem threatens availbility, this redundancy is small price for staying online.

### What happens when multiple requests try to rebuild an expired cache entry simultaneously?

Cache stampede happens because cache expiration is binary - one moment the data exist and the next it doesn't.

One approach uses distributed locks to serialize rebuilds. Only the first request to notice the missing cache entry gets to rebuild it, while everyone else waits for the rebuild to complete. This has serious downsides
* If rebuild fails or takes too long, thousands of request timeout waiting
* We need complex timeout handling and fallback logic

A smarter approach uses probabilistic early refresh - serving cached data while refreshing it in the background. This refreshes cache entries before they expire, but not all at once. 

If your cache entry expires in 60mins, a request at minute 50 might have 1% chance of refreshing. At minute 59 it might have 20%.

For our most critical cached data, neither approach might be acceptable. But for our most popular content, this insurance is worthwhile.

### How do you handle cache invalidadtion when data updates need to immediately visible?

A common naive approach is delete the cache entry after a write. It introduces problems
* Which caches do we delete from - application cache, CDN, browser?
* What if an invalidation request fails?
* What if a req comes right after you delete the old value but before the new value is written?

A btter approach for entity-level data is cache versioning also called cache key versioning. Instead of deleting old key, we make them irrelevant

Why this works?

* There are no race conditions because a "late writer" cant overwrite new data - the databases forces a new version number
* There's no partial invalidation to worry about because we're not deleting caches, we're routing around them
* It is safe under concurrency because version changes are atomic in database.

When this isn't pratical?

* For global systems with CDN caching, invalidation becomes more complex.