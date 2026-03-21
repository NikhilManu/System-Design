# CAP Theorem

CAP Theorem states that in a distributed system, we can only have two out of three of following properties

* <b>Consistency</b>: All nodes see the same data at the same time.
* <b>Availbility</b>: Every request to non-failing node receives a response, without guarantee that it contains the most recent version of the data
* <b>Partition Tolerance</b>: The system continues to operate despite failure between two nodes of the system.

In any distributed system, partition tolerance is a must. Network failures will happen and our system needs to handle them. 

So CAP theorem really boils down to a single choice. Consistency or Availability.

### When to Choose Consistency

1. Ticket Booking System: Users trying to book same seat on a flight
2. E-commerce Inventory: Users trying to buy the last item in an inventory
3. Financial Systems

If we prioritize consistency, our design might include:
* Distributed Transactions
* Single-Node Solutions

### When to Choose Availability

Majority of the system can tolerate some inconsistency and should prioritize availability.

1. Social Media
2. Content Platform (Netflix)
3. Review Sites

if we prioritize availability, our design might include:
* Multiple Replicas
* Change Data Capture (CDC): CDC to track changes in primary database and propogate they async to replicas.

### Considerations

As system grows, the choice between availability and consistency is not always binary. A feature of the system may be available and other might be consistent.

#### Different Level of Consistency

1. Strong Consistency: All reads reflect the most recent write.
2. Causal Consistency: Related event appear in the same order to all users.
3. Rear-your-own-writes Consistency: Users always see their own updates immediately.
4. Eventual Consistency: System will become consistent over time.