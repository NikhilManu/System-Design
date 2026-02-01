## Delivery Framework

![Delivery Framework](https://github.com/NikhilManu/System-Design/blob/main/images/LLD/Delivery%20Framework.png)

### 1. Requirements (~5 minutes)

* Primary Capabilities - What operations must this system support?
* Rules and completion - What conditions define success, failure, or when the system stops or transistions state?
* Error handling - How should the system respond when inputs or actions are invalid?
* Scope boundaries - What areas are in scope (core & buisness logic) and what areas are explicitly out?

### 2. Entities and Relationships (~3 minutes)

#### Identify Entities

* If something maintains state or enforces rules, it likely deserves to be its own entity
* If it's just information attached to something else, it's probably just a field on another class

#### Define Relationships

* Which entity is driving the main workflow (orchestrator)?
* Which entities own durable state?
* How do they depend on each other? (has-a, uses, contains)
* Where should specific rules logically live?

#### Representing on a Whiteboard

For Tic-Tac-Toe,

```
Entities:
- Game
- Board
- Player

Relationships:
- Game -> Board
- Game -> Player (2x)
```

### 3. Class Design (~10-15 minutes)

Start with the orchestrator class, then move down to supporting entities.

For each entity, we'll answer two questions:
1. State - What does this class need to remember to enforce the requirements?
2. Behavior - What does this class need to do, in terms of operation or queries?

#### Deriving State From Requirements

From requirement list and for each entity ask:
* Which parts of requirement does this entity own?
* What information does it need to keep in memory to satisfy those responsibilities?

#### Deriving Behavior From Requirements

For each class, ask:
* what operations the outside world needs
* Which requirements thos operations satisfy

### 4. Implementation (~10 minutes)

1. Happy Path - Walk through the method in a linear way.
2. Edge Cases - Invalid inputs, illegal operations, out-of-range values, calls that violate the current system state.

At last verify and walk through a specific non-trivial scenario. Find bugs and fix it on the spot.


### 5. Extensibility (~5 minutes, if time and level allow)

Interviewers may ask what if questions, and check whether our design can evolve cleanly