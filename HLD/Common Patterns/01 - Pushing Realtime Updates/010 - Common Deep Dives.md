## Common Deep Dives

### How do you handle connection failures and reconnection?

Our real time systems need graceful degradation and recovery.

* Key challenge is detecting disconnections quickly and resuming without data loss. Websockets connections dont always signal when they break - a client might think its connected while server has already cleaned up. 
  * Implementing heartbeat mechanism helps detect these *Zombie Connections*
  
* For recovery, we need to track what update client has received. When client reconnects they should get everything they missed. 
  * This means maintaining a per-user message queue OR 
  * implementing sequence numbers that clients can reference during reconnections

### What happens when a single user has millions of followers who all need the same update?

The solution involves strategic caching and hierarchical distribution. Instead of writing the update to millions of individual user feeds, cache the update once and distribute through multiple layers. Regional servers can pull the update and push to local client, reducing load on any single component

![Hierarchical Aggregation](https://github.com/NikhilManu/System-Design/blob/main/images/HLD/Common%20Patterns/01%20-%20Pushing%20Realtime%20Updates/Hierarchical%20Aggregation.png)

### How do you maintain message ordering across distributed servers?

* Vector clocks or logical timestamp help establish ordering relationships between messages. Each server maintain its own clock, and the messages include timestamp information that helps recipients determine the order
* For critical ordering requirements, we might need to funnel all related message through a single server or partition. This trades some scalability for consistency guarantee, but simplifies the ordering problem