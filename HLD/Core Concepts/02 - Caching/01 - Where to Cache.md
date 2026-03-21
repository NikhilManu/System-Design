# Caching

Caches are essential for scalable systems. The reduce load on the database and cut latency. They also create new challenges around invalidation and failure handling.

## Where to Cache

Caching can show up in multiple layers of a system.

### External Cache

A standalone cache service that application talks to over the network. We store frequently accessed data in something like Redis.

Note: In most cases this should be the default answer.

![External Cache](https://github.com/NikhilManu/System-Design/blob/main/images/HLD/Core%20Concepts/02%20-%20Caching/External%20Cache.png)

### CDN (Content Delivery Network)

A CDN is geographically distributed network of servers that caches content close to users. Instead of every request travelling to origin server, a CDN stores copies of the content around the world.

#### Note: Modern CDN can cache much more than static files. The can cache API responses, HTML Pages etc

How it works:
1. A user requests an image from your app.
2. The request goes to the nearest CDN edge server.
3. If image exist, return immediately.
4. If not, CDN fetches it from origin server and stores it.

### Client Side Cache

Client-side caching stores data close to the requester to avoid unnecessary network calls. 

Ex: browser

But it can also mean caching within a client library.

Ex: Redis clients cache cluster metadata like which nodes are in the cluster. So that client can route request directly to right node.

![Client-Side Cache](https://github.com/NikhilManu/System-Design/blob/main/images/HLD/Core%20Concepts/02%20-%20Caching/Client%20Side%20Cache.png)

### In-Process Caching

In-Process cache simply means storing them inside a local cache. Reads from local memory are faster than reads from Redis.

![In-Process Cache](https://github.com/NikhilManu/System-Design/blob/main/images/HLD/Core%20Concepts/02%20-%20Caching/In-Process%20Cache.png)

They are very fast, but main issue is cached data will not be shared across servers. So data getting updated or invalidation, the other server will not know.

User In-Process caching for small frequently accessed values that rarely change. Mention this as an optimization layer after we already introduced an external cache.