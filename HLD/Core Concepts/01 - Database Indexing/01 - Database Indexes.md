# Database Indexes

Indexes are separate data structures which are optimized for searching. They allow databases to quickly locate records without scanning the whole table.

### Physical Storage and Access Patterns

* Without index we need to scan through every page of data one by one. As the pages in the application increases, reading becomes slower
* With indexes, instead of reading through every page, indexes provide a path to reach directly to data we need.

Note: Modern databases have optimization like prefetching and caching to make random access faster.

### Cost

* Every index created requires additional disk space.
* Write performance takes a hit. Classic case is table with frequent writes but infrequent reads.

#### Note

In reality, the impact of indexes on memory is often overblown. Modern databases have smart buffer pool management that reduces the performance hit of having multiple indexes.

However, its still a good idea to monitor the index usage and avoid creating unnecessary indexes that don't provide significant benefits.

