# Index Optimization Patterns

We should identify performance bottlenecks by examining query plans and database metrics. This is about understanding access patterns and crafintg and indexing approach that supports them.

## Composite Indexes

Most common optimization pattern. Instead of creating separate indexes for each column, we create a single index that combines multiple columns in a specific order.

### The Order Matters

The order of columns in composite index is crucial.

Basically "Order columns from most selective to least selective". But there's more to it. If we sort frequently a particular column, including it in the composite index (even if it's not highly selective) can eliminate expensive sort.

## Covering Indexes

A covering index is one that includes all the columns needed by your query.

Think about showing a social media feed post timestamp and like counts. With regular index on (user_id, created_at), the database first finds matching post in the index and needs to fetch the full page data to get like count. 

We could include the like column directly in our index, so that we can skip expensive lookups.

The trade-off is size as they are larger because they store extra columns.

#### Note

The reality of 2026 is that covering indexes are more of niche optimization that go-to solution. Modern database query optimizers have become quite smart at executing queries efficiently with regular indexes.

## Conclusion

![Indexing FlowChart](https://github.com/NikhilManu/System-Design/blob/main/images/HLD/Core%20Concepts/01%20-%20Database%20Indexing/Index%20FlowChart.png)