# Concurrency

Concurrency is what happens when multiple things try to happen at the same time.

## Concurrency Fundamentals

* When threads in the same process share memory.
* When multiple threads can make progress indpendently and their execution can overlap.

## The Toolbox

Concurrency problem are solve with small set of primitive that every language provides.
- Atomics
- Locks (Mutexes)
- Semaphores
- Condition Variables
- Blocking Queues

### Atomics

Atomics provide thread-safe operations on single variables without locks.

```
using System.Threading;

int counter = 0
Interlocked.Increment(ref counter); // Thread safe increment
```

### Locks (Mutexes)

When a thread holds a lock, other thread trying to acquire it is blocked until the first thread releases it.

```
private reaodnly object _lock = new object()

lock(_lock) {
    // Only one thread can be here at a time.
    counter++;
}
```

Note: Locks are our default tool for protecting shared state.

### Semaphores

Semaphores are counting locks. Instead of binary locked/unlock, a semaphore has N permits.

```
using System.Threading;

var permits = new SemaphoreSlim(5); // Allow 5 concurrent operations
await permits.WaitAsync(); // Block if no permit available

try {
    doWork();
} finally {
    permits.Release();
}
```

### Condition Variables

Condition variables let threads wait efficiently for condition to become true. A thread acquires a lock, checks a condition, and if not satisfied, waits.

```
using System.Threading;

private readonly object _lock = new object();

lock (_lock) {
    while (!condition) {
        Monitor.Wait(_lock);
    }

    // Condition is now true
}
```

### Blocking Queues

* Producers call ```Add() or Put()``` to add Items; if full, they block.
* Consumers call ```Take() or Get()``` to remove items; if empty, the block.

```
using System.Collections.Concurrent;

var queue = new BlockingCollection<Task>(boundedCapacity: 100);
queue.Add(task); // Blocks if queue is full
queue.Take(); // Blocks if queue is empty
```

This queue handles all synchronization internally making it our go-to tool for handling work between threads.

### Language Reference

[Concurrency primitives for Different Languages](https://www.hellointerview.com/learn/low-level-design/concurrency/intro#language-reference)

## Three Problem Types

* Correctness
* Coordination
* Scarcity

![Three Problem](https://github.com/NikhilManu/System-Design/blob/main/images/LLD/Three%20Problem.png)
