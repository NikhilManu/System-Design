## Delivery Framework 

Here is a image of the delivery Framework

![Delivery Framework](https://github.com/NikhilManu/System-Design/blob/main/images/HLD/Delivery%20Framework.png)

- Requirements
  - Functional Requirements
  - Non-Functional Requirements
  - Capacity Esitmation
- Core Entities
- API or System Interface
- Data Flow [Optional]
- High Level Design
- Deep Dives

### Requirements

#### Funtional Requirements

These are the core features of your system.

Ex: Users should be able to post tweets

#### Non-Functional Requirements

These are the statements about the system qualities that are important to users.

Ex: The system should be able to scale to support 100M+ DAU (Daily Active Users)

#### Capacity Estimation

In most cases we can tell them we are skipping on estimations and we will do math while designing when/if necessary. 

TopK system for trending topics in FB post, we would want to estimate the number fo topics as this will influence the design.


### Core Entities

We should provide a foundation to build on. These are the core entities that our API will exchange and that our system will persist in a Data Model.

Note: We dont want to list the entire data model, because we simply cannot anticipate every relationships and entities.

For example of twitter, our core entities would be
* User
* Tweet
* Follow

### API or System Interface

Main decision to make here is - which API protocol should I use?

* REST - Mostly the default choice for most interviews
* GraphQL - Choose this when you have diverse clients with different data needs
* RPC - User for internal APIs when performance is crictical

### Data Flow

If your system doesnt involve a long sequence of actions, skip this.

For a webcrawler, this might look like:
* Fetch seed URLs
* Parse HTML
* Extract URLs
* Store data
* Repeat

### High Level Design

Here we are drawing boxes and arrows to represent different components of the system and how they interact. Components are building blocks like server, databases, caches, etc.

Primary goal is to design an architecture that satisfies API that we designed.


### Deep Dives

Since now we got a high-level design, we will make it better by
* Ensuring it meets all of you Non-Funtional Requirements
* Addressing edge cases
* Identifying and addressing issues and bottlenecks
* Improving the design based on probes from you interviewer