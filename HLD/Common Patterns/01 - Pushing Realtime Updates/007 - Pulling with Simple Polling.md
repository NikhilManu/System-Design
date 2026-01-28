## Pulling with Simple Polling

![Pulling with Simple Polling](https://github.com/NikhilManu/System-Design/blob/main/images/HLD/Common%20Patterns/01%20-%20Pushing%20Realtime%20Updates/Pulling%20with%20Simple%20Polling.png)

Our client is constantly asking the server for updates and the server needs to maintain a state necessary to respond to those requests.

Most common way is to have DB where we store the updates, from the DB our clients can pull the updates they need.

*Note*: With polling we are tolerating delay. We use the poll itself as trigger, even though actual update may have occured at some other point of time.

#### Advantages

* Simple to implement
* State is contrained in DB
* No special infra
* Easy to understand

#### Disadvantages

* High latency
* Excess DB load when updates are infrequent and polling is frequent

### When to use Pull-based Polling?

This is great when user experience should be somewhat responsive, but quickly responding is not the main thing.

### Things to discuss

* Talk about how we store updates if we are using a database
* How can we query and how that can change given your load.