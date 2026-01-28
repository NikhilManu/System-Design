## Server-Sent Events: The Efficient One-Way Street

SSE is an extension of long polling that allows the server to send a stream of data to the client.

SSE uses a special header "<b>Transfer-Encoding: chunked</b>" which tell the client that the response is a series of chunks. This allows us to move from single atomic request/response to stream of data.

With SSE instead of sending full response once data becomes availble, the server sends a chunk of data and then keeps request open to send more data. SSE is perfect for senarios where server needs to push data to client, but client doesn't need send data back frequently.

#### How SSE Works?

* Client establishes SSE connection
* Server keeps connection open
* Sever sends messages when data changes or update happens
* Client receives updates in real-time

<b>NOTE</b>: Modern browsers have built-in support through EventSource object


The advantages are
* Built into browsers
* Automatic reconnection
* Works over HTTP
* More efficient than long polling
* Simple to implement

The disadvantages are
* One-way communication only
* Some networking equipment don't support streaming.
* Browsers limit the number of concurrent connections per domain
* Monitoring is hard since request can hang around for a long time.

#### When to use SSE?

SSE is a great upgrade to long-polling because it eliminates the issue around high-frequency updates while still building on top of HTTP.

Popular use cases for SSE is AI chat apps which frequently involve the need to stream new tokens to the user.

#### Things to discuss

Most SSE connections wont be long (30s - 60s), so for sending longer messages we might need to talk about how client re-establish connection and how they deal with gaps in between.

* SSE standard includes a "last event ID" which is intended to cover the gap
* EventSource object in browsers explictly handles this reconnection logic.
