# Polling

## Simple Polling: The Baseline

The simplest approach is to have client regularly poll the server for updates. This could be done with a HTTP request that client makes at a regular interval.

Note: If low frequency update (2-5 sec) works, then propose a simple polling based appraoch

The advantages are
* Simple to implement
* Stateless
* No special infrastructure needed
* Works with any standard networking infrastructure
* Easy to understand

The disadvantages are
* Higher latency
* Limited update frequency
* More bandwidth usage
* Can be resource intensive

#### When to use simple polling ?

Simple polling is a great baseline, unless you require very low latency and real-time updates. Also it is good when the window where we need updates is short.

*NOTE*: To reduce overhead one way is to use HTTP keep-alive connections, so that we only need to establish TCP connections once which minimizes setup and teardown overhead

## Long Polling: The Easy Solution

The client makes a request to the server and the server holds the request open until new data is available. The server responds with the data, and the client immediately makes a new HTTP request. 

If no data has come through in a long while, we might return empty response so that client can make another request

Ex of Chatbot
* Client makes HTTP request to server
* Server holds request open until new data is available
* Server responds with data
* Client immediately makes a new request
* Process repeats

The important trade-off is that since client needs to "call back" to server after each receipt, the approach can introduce extra latency

![Long Polling Latency](https://github.com/NikhilManu/System-Design/blob/main/images/HLD/Common%20Patterns/01%20-%20Pushing%20Realtime%20Updates/Long%20Polling.png)

Assume the latency between server and client is 100ms.

If we have 2 updates 10ms apart, with long polling we'll receive the first update after 100ms and we'll receive second update after 290ms
(90ms for first response to finish + 100ms latency)

The advantages are:
* Builds and works on standard HTTP
* Easy to implement
* Stateless server-side
* No special infrastructure needed

The disadvantages are:
* Higher latency than alternatives
* More HTTP overhead
* can be resource intensive with clients
* Not suitable for frequent updates due to above mentioned issue
* Requests can hang around for a long time.
* Browsers limit the number of concurrent connections per domain, means you can only have a few long-polling connections per domain.

### When to use Long Polling?

Long polling is a great solution for near real-time updates with a simple implementation. Its a good choice when updates are infrequent.

If latency trade-off of a simple polling solution is at all an issue, long polling is an obvious upgrade.

