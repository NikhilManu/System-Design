# Correctness

Correcness is about preventing data corruption when multiple thread access shared state. The danger isn't deadlock, but producing wrong results.

## The Problem

What happens when two users try to book the same seat at the same time?

Alice wants 7A, Bob also wants 7A

In concurrent environment, Both saw the seat as available. Both proceed to book it. This is a common issue. This is a correctness problem.

There are four solutions to correctness problem, from simplest to complex

* Coarse-grained locking
* Fine-grained locking
* Atomic variables
* Thread confinement

Then we have two patterns where correctness bugs appear most
* Check-then-act
* Read-modify-write

## The Solution

### Coarse-Grained locking (One Lock)

When a thread acquires a lock, every other thread trying to acquire that same lock has to wait until the first thread releases it.

Coarse-grained locking means using one lock to guard all booking operations.

```
using System.Collections.Generic;

public class TicketBooking {
    private readonly object _bookingLock = new object();
    private Dictionary<string, string> _seatOwners = new Dictionary<string, string>();

    public bool BookSeat(string seatId, string visitorId) {
        lock (_bookingLock) {
            if (_seatOwners.ContainsKey(seatId)) {
                return false;
            }

            _seatOwners[seatId] = visitorId;
            return true;
        }
    }
}
```

Note: This should be default choice for shared state.

##### Challenges

* Biggest mistake with coarse-grained locking is releasing the lock too early.
* Another mistake is using different lock objects for different operations that need to be atomic together.

The tradeoff is throughput. With single lock guarding all booking operations.

#### Read-Write Locks

Sometimes the workload is heavily skewed towards reads. In these cases, coarse-grained locking is wasteful because readers block each other even though they're not modifying anything.

A read-write lock (shared-exclusing lock) solves this. It has two modes
1. Read Mode (Shared)
2. Write Mode (Exclusive)

```
using System.Collections.Generic;
using System.Threading;

public class Cache {
    private readonly ReaderWriterLockSlim _rwLock = new();
    private readonly Dictionary<string, string> _data = new();

    public string Get(string key) {
        _rwLock.EnterReadLock();
        try {
            return _data.TryGetValue(key, out var value) ? value : null;
        }
        finally {
            _rwLock.ExitReadLock();
        }
    }

    public void Put(string key, string value) {
        _rwLock.EnterWriteLock();
        try {
            _data[key] = value;
        }
        finally {
            _rwLock.ExitWriteLock();
        }
    }
}
```

C# ReaderWriteLockSlim is the modern choice. Slim Version is better, the older have performance issues.


### Fine-Grained Locking

Threads only block each other when they're competing for the same resources.

```
using System.Collections.Concurrent;

public class TicketBookingFineGrained {
    private readonly ConcurrentDictionary<string, object> _seatLocks = new();
    private readonly ConcurrentDictionary<string, string> _seatOwners = new();

    private object GetLock(string seatId) {
        return _seatLocks.GetorAdd(seatId, _ => new object());
    }

    public bool BookSeat(string seatId, string visitorId) {
        lock (GetLock(seatId)) {
            if (_seatOwners.ContainsKey(seatId)) {
                return false;
            }

            _seatOwners[seatId] = visitorId;
            return true;
        }
    }
}
```

This pattern scales much better under load. Fine-grained is worth mentioning when the interviewer asks about scalability.

#### Challenges

The extra throughput comes at a cost as it can introduce lot of complexity.

Ex: Consider when user wants to swap seats with another user. We need to lock both seats to make it atomic. If A tries to swap 7A for 12B while B tries to do that for 12B and 7A. This is deadlock. 

The fix is to always acquire locks in a consistent order. We could lock from smaller to larger.

There is also pratical overhead for unbounded resources, we might need to cleanup locks that are no longer in use.


Note: If a human is triggering the operation, coarse-grained locking is almost always fine. Fine-grained locking matters when we are processing machine generated traffic at scale.

### Atomic Variables

Locks work, but they're not free. When lock is contented, threads waiting on it can't do anything useful. For simple operations on a single variable, lighter weight alternative is atomic variable.

Consider tracking how many seats have been booked. Incrementing normally is unsage as increment has three steps (read, add, write) that can interleave.

```
using System.Threading;

public class BookingStats {
    private int _bookingCount = 0;

    public void OnSeatBooked() {
        Interlocked.Increment(ref _bookingCount);
    }

    public int GetBookedCount() {
        return Interlocked.CompareExchange(ref _bookingCount, 0, 0);
    }
}
```

For complex updates, we'll use CAS loop

```
using System.Threading;

public class ConcurrencyTracker {
    private int _maxConcurrent = 0;
    
    public void UpdateMaxConcurrent(int current) {
        int observed;
        do {
            observed = _maxConcurrent;
            if (current <= observed) {
                return;
            }
        } while (Interlocked.CompareExchange(ref _maxConcurrent, current, observed) != observed)
    }
}
```

Note: Reach for atomics when we have a single Counter or flag that multiple thread update.


### Thread Confinement (Shared Nothing)

The simplest way is avoid sharing data between threads in the first place. This is called shared nothgin or Thread Confinement.


This patterns shows up more often. Dragonfly, high performance Redis alternative, partitions keyspace across threads.

Operations that span multiple partitions still require coordination. Load imbalance can become an Issue if some partitions are hotter than others.

Note: For most interviews, thread confinement is overkill. But its worth mentioning if the interviewer pushes hard on scalability.

## Common Bugs

Synchronization bugs dont appear randomly. They cluster around specific patterns that show up again and again.

### Check-Then-Act

You check a condition, make a decision based on that check, then act on it. The bug happens when another thread invalidates the check between when you read it and when you act on it.

#### Examples
* Connection Pool
* LRU Cache with Max Size
* File Download Manager
* Parking Lot
* Singleton (Lazy Initialization)

### Read-Modify-Write

You read a value, compute something from it and write the result back. The bug happens when two thread read the same value, both compute from it, and both write back, causing one update to get lost.

#### Examples
* Hit Counter
* Bank Account
* Metrics Aggregator
* Inventory System

## Conclusion

![Correctness Decision Tree](https://github.com/NikhilManu/System-Design/blob/main/images/LLD/Correctness%20Decision%20Tree.png)