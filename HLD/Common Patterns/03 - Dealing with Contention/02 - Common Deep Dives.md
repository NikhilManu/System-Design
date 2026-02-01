### Choosing Right Approach

General Guide line on when to use which approach

![All Approaches](https://github.com/NikhilManu/System-Design/blob/main/images/HLD/Common%20Patterns/03%20-%20Dealing%20with%20Contention/All%20Approaches.png)

Here is a flow chart for more simplified version

![Flow Chart](https://github.com/NikhilManu/System-Design/blob/main/images/HLD/Common%20Patterns/03%20-%20Dealing%20with%20Contention/Right%20Approach%20Flow%20Chart.png)

### When to use in Interviews

#### Recognition Signals

* Multiple users competing for limited resources
* Prevent double-booking
* Ensure data consistency under high concurrency
* Handle race condition in distributed systems

#### When not to overcomplicate

* Low contention scenarios
* Single user operations
* Read-heavy workloads

### Common Deepdives

#### How do you prevent deadlocks with pessimistic locking?

A wants to transfer 100 to B, while B wants to transfer 50 to A. So first transaction locks A's account and then tries to lock B's account. The second transaction lock B's account and then tries to lock A'account. Both transaction will wait forever.

The standard is ordered locking, which means always acquiring locks in a consistent order regardless of the buisness logic. In practice, this means sorting all resource you need to lock by a deterministic key before acquiring locks.

As a fallback, DB timeout configurations serve as a safety net when ordered locking isn't practical or when edge cases are missed.


#### What if your coordinator service crashes during a distributed transactions?

This is the classic 2PC failure scenario.

Production systems handle this with coordinator failover and transaction recovery. When a new coordinator starts up, it reads persistent logs to determine which transactions where in-flight and completes them.

Sagas are more resilient as they don't hold locks across network calls.

#### How do you handle the ABA problem with optimistic concurrency?

This problem occurs when a value changes from A to B and back to A between our read and write. Optimistic check sees the same value and assumes nothing changed, but important state transitions happened.

The solution is using a column that will always change. We could add a column like version or count which would always change.

#### What about performance when everyone wants the same resource?

Sharding doesn't help. Load balancing doesn't help as the compete for same database now. Even read replicas dont work as bottleneck is on the writes.

First strategy is questioning whether we can change the problem itself
* Instead on auction item, we have 10 identical items and can run separate auctions for each.
* We can make the likes and follows eventually consistent - users wont notice this.

For cases where we need strong consistency on a hot resource, implement queue-based serialization. 
* Put all requests for a specific resource into a dedicated queue that gets processed by a single worker thread. 
* This eliminites contention by making operations sequential
* The queue acts as buffer that can absorb traffic spikes while works processes in sustainable rate.

The tradeoff is latency. Users might wait longer for their requests to be processed.


