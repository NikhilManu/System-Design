# Dealing with Contention

Contention occurs when multiple processes compete for the same resource simultaneously. 

Ex: Booking the last concert ticket.


## Solution

Solution follows a natural progression of complexity. We will start with single database solution using atomicity and transactions, then add coordination mechanism when concurrent access creats conflicts, and finally move to distributed coordination when multiple databases are involved

### Single Node Solutions

When all the data exists in a single database, the solutions are more straight forward
1. Atomicity
2. Pessimistic Locking
3. Isolation Levels
4. Optimistic Concurrency Locking

#### Atomicity

Atomicity means that a group of operations either all succeed or all fails. Transactions are how database provide atomicity

```
BEGIN TRANSACTION;

UPDATE accounts SET balance = balance - 100 WHERE user_id = 'alice';

UPDATE accounts SET balance = balance + 100 WHERE user_id = 'bob';

COMMIT; -- Both operation succeed together
```

But even with atomic transaction, the problem doesnt solve. Because now Two people can still book the same seat. (When Bob and Alice start transaction simultaneously)

#### Pessimistic Locking

Prevents conflicts by acquiring locks upfront.

```
BEGIN TRANSACTION;

SELECT available_seats FROM concerts
WHERE concert_id = 1
FOR UPDATE;

UPDATE concerts
SET available_seats = availble_seats - 1
WHERE concert_id = 1

INSERT INTO Tickets(userId, concert_id, seat_number, puchase_time)
VALUES (1, 1, 24, NOW())

COMMIT;
```

FOR UPDATE clause acquires an exclusive lock on the concert row before reading. A lock in this context is a mechanism that prevents other connections from accessing the same data untill lock is released.

Performance considerations are really important when using locks. We want lock as few rows as possible.
* Lock entire table and we kill concurrency
* Hold lock for seconds instead of ms and we create bottlenecks.

#### Isolation Levels

Instead of locking rows with FOR UPDATE, we can let db automatically handle conflicts using Isolation Levels.

Isolation levels control how much concurrent transactions can see each others change. Most db supported four standard Isolation level
* READ UNCOMMITED: Can see uncommitted changes from other transaction (Rarely Used)
* READ COMMITTED: Can see only committed changes (default in PostgreSQL)
* REPEATABLE READ: Same data read multiple times within a transaction stays consistent (default in MySQL)
* SERIALIZABLE: Strongest isolation, transaction appear to run one after another.

The default of either still allows for ticket race condition. The SERIALIZABLE level solves this by making transaction appear to run one at a time. They are much more expensive than locks.

#### Optimistic Concurrency Control

Pessimistic locking assumes conflict will happen and prevents them upfront. Here the opposite approach is taken.

Pattern is simple, we include a version number with our data. Every time we update a record, increment the version. When updating, specify both the new value and the expected current version.

```
BEGIN TRANSACTION;
UPDATE concerts
SET available_seats = availble_seats - 1
WHERE concert_id = 1
AND availble_seat = 1 -- Expected current value

INSERT INTO tickets (user_id, concert_id, seat_number, purchase_time)
VALUES (1, 1, 22, NOW())
COMMIT;

BEGIN TRANSACTION;
UPDATE concerts 
SET availble_seats = available_seats - 1
WHERE concert_id = 1
AND availble_seat = 1 -- Stale value
```

This approach makes sense when conflicts are uncommon. For most e-commerce scenarios the change of two people buying the exact same item at exact same moment is low. The occasional retry is worth it.

### Mulitple Nodes

Consider a bank transfer, Alice lives in db A and Bob lives in db B. Now we cant use a single database transaction to handle the transfer.

#### Two-Phase Commit (2PC)

We have a coordinator managing the transcation across multiple database participants. The coordinator asks all participants to prepare the transaction in the first phase, then tells them to commit or abort in the second phase based on whether everyone successfully prepared.

This guarantees atomicity, but its expensive and fragile. If service crashes between prepare and commit, both databases are left with open transactions in an uncertain state.

#### Distributed Locks

We just ensure only one process can work on a particular resource at a time across our entire system.

For bank transfer, we could acquire locks on both Alice's and Bob's account ID before starting any operations. This prevents concurrent transfers from interfering with each other.

Distributed Locks can be implemented with several technologies
* Redis with TTL
* Database columns
* Zookeeper
  
When we select a seat, it doesn't immediately go from availble to sold. Instead it goes to reserved state that gives us time to complete payment while preventing others from selecting the same seat.

Disdvantage is that they can become bottlenecks under high contention, and we need to handle lock timeouts and failure scenarios

#### Saga Pattern

Instead of trying to coordinate everything atomically like 2PC, it breaks the opeartion into a sequence of independent steps that can each be undone if something goes wrong

Ex:
1. Step 1: Debit 100 from alice account in DB A, commit immeidately
2. Step 2: Credit 100 from Bob accoutn in DB B, commit immediately
3. Step 3: Send confirmation notifications

If any step fails we just undo the other changes

Since each step is commited transaction, there will be no long-running open transactions and no co-ordinator crashes. Each db operations succeed or fails independently.

This eventual consistency is what makes saga practical.