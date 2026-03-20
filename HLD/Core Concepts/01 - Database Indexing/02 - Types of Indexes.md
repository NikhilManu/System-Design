# Types of Indexes

There are many types of indexes, some are mostly used for specialized use cases.

1. B-Tree
2. LSM Trees (Log-Structured Merge Trees)
3. Hash Indexes
4. Geospatial Indexes
5. Inverted Indexes

## B-Tree Indexes

These are the most common type of database indexes, providing an efficient way to organize data for fast searches and updates.

### Structure of B-Tree

A B-tree is a self-balancing tree that maintains sorted data and allows for efficient insertion, deletion and searches. Each node contains ordered array of keys and pointers, structured to minimize disk reads.

### Why B-Tree are the Default Choice

1. They maintain sorted order, making RANGE queries and ORDER BY operations efficient.
2. They are self balancing, ensuring predictable performance.
3. Handle both equality searches and range searches equally well.
4. They remain balanced even with random inserts and deletes, avoiding the performance cliffs you might see with simpler tree structures.

## LSM Trees (Log Structured Merge Trees)

LSM Tree is the storage format for your entire table, sorted by the PK. PK lookups are extremely fast, but secondary indexes require additional structures.

Instead of updating data in-place like B-Tree, LSM Tree uses an append-only approach that is used for Write-heavy workloads.

### How LSM Trees Work ?

Solves write problem by batching writes in memory and flushing them to disk sequentially. LSM trees buffer changes in memory and write them out in large chunks.

This is what happens when we write to database that uses LSM

1. Memtable (Memory Component): New writes go into in-memory structure called a memtable. Typically implemented as Red-Black or Skip list. This is fast since it's all in RAM
2. Write-Ahead log (WAL): To ensure durability, every write is appended to a write-ahead log on disk.
3. Flush to SSTable: Once the memtable reaches certain size, it's frozen and flushed to disk as an immutable Sorted String Table (SSTable). This is single sequential write operation that can write MB of data at once.
4. Compaction: Over time, we accumulate many SSTables on disk. A background process called compaction periodically merges these files, removing duplicates and deleted entries.

This makes writes incredibly fast, we're just appending to memory and a log file. Even when flushing to disk, we're writing large sequential chunks rather that seeking to random locations.

### Negative Impacts on Reads 

When we query for a specific key, the database must check multiple places
1. First, the memtable: is the data in the in-memory buffer ?
2. Then, immutable memtables: Any memtables waiting to be flushed ?
3. Finally, all SSTables on disk: Starting from newest and working backwards

To mitigate the performance issues, the employ several optimizations
1. Bloom Filters: A Data Structure that can tell if a key is not in the file.
2. Sparse Indexes: Since SSTables are sorted, they maintain sparse indexes that tell the range of keys in each block.
3. Compaction Strategies: Different compaction strategies optimize different workloads.
    * Size-Tiered compaction minimize write amplification but can lead to more files to check.
    * Leveled compaction maintains fewer files but requires more frequent rewrites.

## Hash Indexes

At the core they just hashmap that maps indexed values to row locations. Hash collisions are handled by allowing multiple entries per bucket, many systems use chaining with overflow storage when a bucket fills.

Hash Indexes shine in specific scenarios, particularly for in-memory databases like Redis.

### When to choose Hash Indexes ?

* We need absolute fastest possible exact-match lookups
* We never need Range queries or sorting
* We have plenty of Memory

But in most cases B-Trees will be a better choice.
