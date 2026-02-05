# Coordination 

Coordination is about threads communicating and handing off work.

## The Problem

We need a safe way for producers and consumers to hand off work without wasting CPU or crashing under load

Three things need solving:

1. Efficient Waiting - consumers should sleep when there's no work, waking immediately when work arrives.
2. Backpressure - producers should slow down when consumers can't keep up, preventing memory exhaustion.
3. Thread safety - the coordination mechanism itself must handle concurrent access without corruption.

## Solution

### Shared State Coordination

Most common approach uses shared data structures.

#### Wait/Notify (Condition Variables)

We have a lock protecting some shared state and a condition variable attached to that lock. When a thread needs to wait for a condition to become true, it calls "Wait" on the condition variable. Two things happen atomically

1. The thread releases the lock and goes to sleep.
2. The thread stops consuming CPU entirely. It's completely parked until explicitly woken.

```
lock (lockObj) {
    while (!conditionIsMet()) {
        Monitor.Wait(lockObj); // Releases lock, sleeps until notified
    }

    DoWork();
    Monitor.PulseAll(lockObj); // Wakes all waiting Threads
}
```

##### Challenges

The trickies part about condition variables is deciding whether to wake one thread or all threads

Lets say we have queue with both producers and consumers waiting on the same condition. Which thread wakes up? The runtime picks one arbitrarily. It might pick another consumer, even though consumer need items, not space. The safe fix is wake all threads instead of just one. But waking all threads has a cost, as they all compete for the lock.

The better solution is to use separate condition variables. One for "queue not empty" that consumers wait on and another for "queue not full" that producers wait on. Now when consumers frees up space, it triggers "not full" condition, waking the producers.

#### Blocking Queues

A blocking queue is a thread-safe queue with special behavior it's empty or full. 
* When we try to remove item from empty queue, the call blocks instead of returning immeidiately.
* When thread tries to add item, it wakes you up and get the item.
* When queue is full, trying to ad item blocks until space frees up.
  
```
using System.Collections.Concurrent;

public class TaskScheduler {
    private readonly BlockingCollection<Action> _queue = new BlockingCollection<Action>(boundedCapacity: 1000);

    public void SubmitTask(Action task) {
        _queue.Add(task);
    }

    public void WorkerLoop() {
        while (true) {
            var task = _queue.Take();
            task();
        }
    }
}
```

Note: BlockingQueue is your default answer for producer-consumer problems.

##### Challenges

* Biggest mistake is creating an unbounded queue. This brings memory exhaustion problem.
  * A common approach to choose capcity is based on burst tolerance.
  * If workers can handle 100 tasks/sec and we want to absorb 10 sec traffic spike without blocking producer. We need a buffer of 1000 tasks.

<br>

What happens when the queue fills up. We have three options
1. Block producers with put() - Use this where slowing down is acceptable
2. Timeout and reject with offer(timeout) - Use this on request paths where we can't stall.
3. Drop and log with offer() - Use this where dropping under load is acceptable.

<br>

Graceful shutdown is another common follow-up.

1. Interrupt the worker threads - When we interrupt a thread blocked in take(), it wakes up and throws InterruptedException. Worker cactes this and exits cleanly.
2. Use poll with a timeout - The worker waits up to the timout period for a task. If nothing shows up, poll returns null. When shutdown is requested, set the flag and workers will notice without one timeout period and exit
3. Use the poison pill pattern - Create a special sentinel task that means "shut down". Whne shutdown is requested, submit one poison pill per worker to the queue. When the thread sees the poision pill, it exits its loop and shuts down.

### Message Passing Coordination

Instead of multiple thread accessing shared data structures, what if each thread had its own private state and communicated only by sending messages.

#### The Actor Model
Its an object with mailbox and a message handler. When you send a message to an actor, the messages goes into its mailbox. The actor pulls messages from the mailbox one at a time and processes them. Since one message is processed at a time, the actor's internal state never faces concurrent access.

```
public abstract class Actor<T> {
    private readonly BlockingCollection<T> _mailbox = new();
    private readonly CancellationTokeSource _cts = new();

    protected Actor() {
        Task.Run(() => Run(_cts.Token));
    }

    public void Send(T message) {
        _mailbox.Add(message);
    }

    protected abstract void OnReceive(T message);

    public void Stop() {
        _cts.Cancel();
        _mailbox.CompleteAdding();
    }

    public void Run(CancellationToken token) {
        try {
            foreach (var message in _mailbox.GetConsumingEnumerable(token)) {
                OnReceive(message);
            }
        } catch (OperationCanceledException) { }
    }
}
```

##### When to use Actors

When we have many independent entities that occasionally need to communicate.

Note: Rule of thumb is "process these task in the background", use a blocking queue. If our problem is "coordinate many independent entites with their own state" consider actors.


##### Challenges

* Mailbox Overflow - Most framework allow to configure mailbox size and overflow behavior - drop messages, block senders, or apply backpressure.
* Message ordering - Messages from actor A to actor B arrive in order Buf if Actor A and C both send to B, the interleaving is undefined.
* Debugging
* Request Response patterns - Actors communicate async, if we need send a message and wait for reply, we need to build that pattern ourself.

### Common Problems

Producer-consumer doesn't appear in interview as an abstract data structure problem. It shows up disguised as practical systems where some work need to happen asynchronously.

### Process Requests Asynchronously

Users make request that need work done, but some that work is slow and doesn't need to happen on the request path. We need respond immediately to use while handling the heavy lifting in the background.

```
public record EmailTask(string Recipient, string Template, string Data);

public class EmailService {
    private readonly BlockingCollection<EmailTask> _emailQueue = new BlockingCollection<EmailTask>(boundedCapacity: 10000);

    public void SignUp(string email, string name) {
        _userRepo.Save(email, name);
        _emailQueue.Add(new EmailTask(email, "welcome", name));
    }

    public void EmailWorker() {
        while (true) {
            var task = _emailQueue.Take();
            _emailClient.Send(task.Recipient, task.Template, task.Data)
        }
    }
}
```

##### Examples
* Image Upload Service
* Payment Processing
* Report Generation

### Handle Bursty Traffic

Bursty traffic is when load comes in waves instead of steadily.

Coordination solves this with a buffer. We size workers for normal load, say 100 workers. When burst hits, the queue absorbs the spike. Requests pile up in the queue while workers churn through them at their normal rate.

##### Examples

* News Sites
* Email Campaign
* Batch Job completion
* Webhooks

## Conclusion

Coordination is about how threads communicate and hand off work.

Shared State Coordination uses data structures that multiple thread access. This is the right default for producer-consumer problem in interviews

Message passing Coordination avoids shared state entirely. Actors own thier data and communicate through messages. This shines for systems with many independent stateful entites

![Coordination Decision Tree](https://github.com/NikhilManu/System-Design/blob/main/images/LLD/Coordination%20Decision%20Tree.png)