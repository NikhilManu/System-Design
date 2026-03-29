### Partioning

Partioning means splitting large table into smaller tables inside a single database.

Two types of common partioning
* Horizontal Partitioning: Split Rows across partitions
* Vertical Partitioning: Split columns across partitions

# Sharding

Sharding is horizontal partitioning across multiple machines. Each shards hold a subset of the data and together the shards make up the full dataset.

Each shard is standalone database with its own CPU, memory, storage and connection pool.

## How to Shard Data ?

We got to make two decisions

1. What to shard by: The field or column we use to split the data.
2. How to distribute it: The rule for assigning those groups to shards.

### Choosing Shard Key

Bad shard keys leads to 
* Uneven data distributions
* Hot spots
* Queries that have to hit every shard

Below are the things that make a good shard key:

* <b>High Cardinality</b>: The key should have many unique values. (Sharding by boolean field means we can have only two shards at max.)
* <b>Even Distribution</b>: Values should spread evenly across shards. (If Sharding by country and 90% users are in US)
* <b>Aligns with queries</b>: Most common queries should ideally hit just one shard. Queries that span all shards become expensive.

### Sharding Strategies

#### Range Based Sharding

Range sharding is the most straight-forward. It just groups by continuous range of values.

```
Shard 1 → User IDs 1–1M
Shard 2 → User IDs 1M–2M
Shard 3 → User IDs 2M–3M
```

The main advantage is simplicity and support for efficient range scans. Works best when different users naturally query different ranges.

#### Hash-Based Sharding

Hash sharding uses a hash function to evenly distribute records across shards.

```
shard = hash(user_id) % 4

User 42  → hash(42) % 4 = Shard 2
User 99  → hash(99) % 4 = Shard 3
User 123 → hash(123) % 4 = Shard 1
```

* The big advantage of hash-based sharding is even distribution.
* With Consistent Hashing, removing or adding shards also minimizes data movement.

#### Directory-Based Sharding

Directory Sharding uses a lookup table to decide where each record lives.

```
user_to_shard
---------------
User 15   → Shard 1
User 87   → Shard 4
User 204  → Shard 2
```

* The advantage is flexibility. For Rebalancing load, just update the mapping table.
* The downside is every single request needs a lookup.
* Makes sense when we need maximum flexibility and afford the extra lookup cost.





