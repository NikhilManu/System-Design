# Bit.ly

Design a URL Shortener like Bit.ly

## Functional Requirements

In some interviews, they will provide us with a core functional requirement upfront. In other cases, we'll need to determine these ourselves.

Most important thing is that we zero in on the top 3-4 features of system.

#### Core Requirements

1. Users should be able to submit a long URL and receive a shortened version.
2. Users can optionally provide a custom alias and expiration for shortened URL.
3. Users should be able to access Original Url by using the shortened URL
4. System Scale: 1B shortened URLs and 100M DAU

#### Out of Scope 

* User authentication and account management
* Analytics on link clicks

We are consider thme out of scope as they add complexity without being core to basic functionality. But it is best to discuss with the interviewer, if we should include them in our design


## Non-Functional Requirements

These requirement refers to specifications about how a system operates, rather than what task it peforms.

#### Core Requirements

1. System should ensure uniqueness for short URL
2. Low latency redirections (< 200ms)
3. The system should be reliable and available
4. The system should scale 1B shortened URLs and 100M DAU

#### Out of Scope

* Data consistency in real-time analytics
* Advanced security features like spam detection and malicious URL filtering.

## Core Entities

Here the core entities are very straight forward:
1. Original URL: Original long URL that user wants to shorten
2. Short URL: The shortened URL that user wants to share
3. User: The user who created the shortened URL

## API

Usually, these are 1:1 mapping of funtional requirements, but there can be exceptions. Most of the time REST API will be used.

```
// Shorten a URL
POST  /urls
{
    originalUrls,
    customAlias?,
    expirationTime?
}
-->
{
    shortUrl
}
```

```
// Redirect to Original URL
GET  /{short_url} --> HTTP 302 redirect to the original URL
```

## High Level Design

#### User should be able to submit a long URL and receive a shortened URL

The core components at a high-level are
1. Client: User interacts with system through any device
2. Primary Server: The primary server receives requests from the client and handles all business logic.
3. Database: Stores the mapping of short codes to long urls

<br>

![Create Short URL](https://github.com/NikhilManu/System-Design/blob/main/images/HLD/Questions%20Breakdown/001%20-%20Bitly/Create%20Short%20Url.png)

When user submits long url, the client sends a POST request to "/urls", then:
1. Primary Server receives the request and validates URL. Also we can check if this URL was already shortened
2. If URL is valid, we generate a short code
3. We can insert the short code (or custom alias), long URL, and expiration date into our database
4. Finally return the short URL to client

#### User should be able to access the original URL by using shortened URL

![Redirect to Original URL](https://github.com/NikhilManu/System-Design/blob/main/images/HLD/Questions%20Breakdown/001%20-%20Bitly/Redirect%20to%20Long%20URL.png)

When user accesses a shortened URL, then

1. Browser sends a GET request to our servers
2. Our Primary Server receives the request and looks up for the short code in db
3. If short code is found and not expired, the server returns the corresponding URL
4. Then server sends a HTTP redirect response to users browser

<br>

There are two type of HTTP redirects

* 301 (Permament Redirect): Browser cache this response, meaning the subsequent request to short URL might go directly to Long URL
* 302 (Temporary Redirect): This suggest that resource is temporarily located at a different URL. So browser doesnt cache this response.

For URL shortener, 302 redirect is often preferred as

* Prevents browser from caching the redirect, which could cause issues if we need to update or delete the short URL in future.
* Allows us to track click statistics for each short URL
* Allows us to update or expire links as required

## Potential Deep Dives

#### How can we ensure short urls are unique?

<b>1. Hash Function </b>

We will hash the long URL. This will always point to same short code. If we want multiple codes per URL, we could add a secret salt of nonce (HMAC). We can then take the output and encode it with base62 and take first N character as short code.

Challenges:
* Despite the randomness, there's still a chance of generating duplicate short codes as number of stored URL increases. 
* To reduce collision probability, we need higher randomness, which means generating longer short codes, which negates the whole purpose
* To handle collisions, implement UNIQUE constraint on Short Code column. In our case, since we made it the PK, we dont need to do that.

<b>2. Unique Counter with Base62 Encoding</b>

One way we could simply eliminate collision is to implement a counter and increment the value for each new url. We can then take output of counter and encode it using base62 to ensure its compact (encoding it will be usefull when counter value is large)

Challenges:
* In distributed environment, maintaining a single global counter can be challenging due to synchronizaiton issues.
* We dont need to concern ourselves with length of short code
  
  1,00,00,00,000 in base62 is '15ftG', which is quite short

#### How can we ensure that redirects are fast?

Since we make short URL as PK, we are not doing any full table scans. So that itself is pretty good optimization.

Note: Making non-incremental columns as PK can affect performance of the DB according to the database that you use.

We can introduce in-memory cache like Redis b/w application server and database. 
* Read through cache. (Cache Miss means, cache fetches data stores it)
* we can reduce the number of hits to the DB. 
* For eviction remove the LRU nodes.

Challenges:
* Cache Invalidation can be complex, especially when updates or deletions occur. In our case URLs are mostly read-heavy, so rarely changes
* Memory limitations require careful decisions about cache size, eviction policies

#### How can we scale to support 1B shortened URLs and 100M DAU?

Lets quickly calculate size of the database. Each row contains
* Short Code (8 Bytes)
* Original URL (100 Bytes)
* creationTime (8 Bytes)
* Optional Custom Alias (100 Bytes)
* Expiration Date (8 Bytes)

This totals to 200 Bytes per row. We can round to 500 Bytes for additional metadata. 

If we store 1B mappings, we are looking at 500 Vytes * 1B rows = 500GB. This is well within the capabilities of modern SSDs

But what if DB goes down?
* Database Replication: If one goes down, we can redirect to another. This adds complexity to our system as we need to ensure our Primary Server can interact with replica without any issues
* Database Backup: Implement a backup system that periodically takes snapshot of our database and stores it in seperate location. This also adds complexity as we need to ensures our Primary Server can interact with the backup without any issues.

#### Lets look at our Primary Server

We know that the reads are much more frequent that writes. We can scale our Primary Server by separating the read and write operations. This introduces a microservice architecture. Where the Read service handles the redirect and Write Service handles the creation of new short URLs. This seperation allows us to scale ecah service independently based on their specific demands

Now when Write service is scaled, we need a single source of truth for Counter. We could use Redis to make it global. To ensure high availability of our counter service, we can use Redis's built in replication features.

<br>

![Final Design](https://github.com/NikhilManu/System-Design/blob/main/images/HLD/Questions%20Breakdown/001%20-%20Bitly/Final%20Design.png)