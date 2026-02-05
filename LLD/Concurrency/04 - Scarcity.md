# Scarcity 

Scarcity is about managing limited resource when demand exceeds supply.

## The Problem

What happens when there arent enough resources for everyone?

Them main solutions are 
* Semaphores - limit how many thread can hold a resources simultaneously
* Resource pooling - gives you actual resource objects, not just permission

The four patterns where scarcity appears most and how to apply the solutions
* Limit concurrent opeartions
* Limit aggregate consumption
* Reuse expensive objects
* Maximize utilization

## The Solution

### Semaphores

A semaphore is a counter that limits how many threads can do something at once. We create a permit with a count, which is the maximum number of threads that can run concurrently.

```
using System.Threading;

public class APIClient {
    private readonly SemaphoreSlim _requestPermits = new SemaphoreSlim(5);

    public async Task<Remove> MakeRequestAsync(string endpoint) {
        await _requestPermits.WaitAsync();

        try {
            return await _httpClient.GetAsync(endpoint);
        } finally {
            _requestPermits.Release();
        }
    }
}
```

Note: In interviews Semaphores are your go-to answer for limiting concurrent operations.

##### Challenges

Semaphores work when we need to limit how many operations run concurrently, but they cant help when we need to hand out specific objects.

### Resource Pooling (With Blocking Queues)

Connection pools have a different problem than simple concurrency limiting. We need to hand out the actual connection object themselves.

That's where blocking Queues comes in. When a thread needs a connection, it pulls from the queue. If the queue is empty, the thread blocks.

```
using System.Collections.Concurrent;

public class ConnectionPool {
    private readonly BlockingColleciton<Connection> = _availableConnections;

    public ConnectionPool(int poolSize) {
        _availableConnections = new BlockingCollection<Connection>(poolSize);
        for (int i = 0; i < poolSize; i++) {
            _availableConnections.Add(CreateNewConnections());
        }
    }

    public Connection Acquire() {
        return _availableConnections.Take(); // Blocks if empty
    }

    public void Release(Connection conn) {
        _availableConnections.Add(conn);
    }

    public void ExecuteQuery(string query) {
        var conn = Acquire();
        try {
            conn.Execute(query);
        } finally {
            Release(conn);
        }
    }
}
```

##### Challenges

* The pool creates all connections upfront during construction. This means startup is slow but subsequent requests are fast.
* Another way is to create connection on demand up to max pool Size. This makes first few requests slow

Note: Upfront creation is better in almost all cases unless startup time matters

* Always check if connection is valid, as it can be stale.
* Creating a unbounded queue will have problem with memory
* Blocking forever on request paths.
  * The solution is to use timeout variants. Instead of take, use Poll with timeout.

## Common Problems

Scarcity problem show in interviews in one of three ways, each directly handled by semaphores or blocking queues
1. Limit concurrent operations (semaphores with N permits)
2. Limit aggregate consumption (semaphores with permit = resource units)
3. Reuse expensive object (blocking queues of actual objects)

### Limit concurrent operations

```
using System.Threading;
using System.IO;

public class DownloadManager {
    private readonly SemaphoreSlim _downloadSlots = new SemaphoreSlim(3);

    public async Task DownloadAsync(string url, string destination) {
        await _downloadSlots.WaitAsync();
        try {
            var data = await _httpClient.DownloadAsync(url);
            await File.WriteAllBytesAsync(destination, data);
        } finally {
            _downloadSlots.Release();
        }
    }
}
```

If 3 downloads are running, the thread blocks untill one finishes.

### Limit Aggregate Consumption

```
public class DiskWriter {
    private const int MB = 1024 * 1024;
    private reaonly object _lock = new object();
    private int _available = 100;

    public async Task WriteFileAsync(byte[] data, string path) {
        int permits = Math.max(1, (data.length + MB - 1) / MB);

        lock (_lock) {
            while (availble < permits) {
                Monitor.Wait(_lock);
            }

            _availble -= permits;
        }

        try {
            await File.WriteAllBytesAsync(path, data);
        } finally {
            lock (_lock) {
                _available += permits;
                Monitor.PulseAll(_lock);
            }
        }
    }

}
```

Each write acquires permits equal to its size, rounded up to nearest MB. If not enough permits are available, the thread blocks until ongoing writes complete.

### Reuse Expensive Objects

This exactly the blocking queue pattern which is said above - thread takes object from the queue and use it, and return it in a finally block.

### Maximum Utilization

What if the want to make the resources maximally busy?

There are three main concepts to this

* Work stealing - handles uneven task distribution. Instead of single queue feeding all workers, each worker maintains its own queue. When a worker queue empties, it steals tasks from another worker queue.
* Batching - amortizes coordination overhead. If making 1000 small database writes, acquiring and releasing a conneciton 1000 times wastes cycles. Instead batch writes together.
* Adaptive sizing - adjusts pool capacity based on demand. A fixed pool of 10 connection might be too small during peak traffic and wasteful during quiet periods.

Note: For most they only check only semaphores and bounded pools. Buf if the interviewer pushes on throughput, then pivot to these answers


## Conclusion

![Scarcity Decision Tree](https://github.com/NikhilManu/System-Design/blob/main/images/LLD/Scarcity%20Decision%20Tree.png)