# Design Principles

## General Software Design Principles

* KISS - Keep It Simple, Stupid
* DRY - Dont Repeat Yourself
* YAGNI - You Aren't Gonna Need It
* Separation of Concerns
* Law of Demeter - Principle of least knowledge. A method should only talk to its immediate friend

## Object-Oriented Desing Principles (SOLID)

<b>Note: Moder lang favors simpler approaches - composition over class hierarchies, functions over interfaces.</b>

### Single Responsibility Principle (SRP)

A class should have only one reason to change.

### Open/Closed Principle (OCP)

A class should be open for extension but closed for modifications. We should be able to add new behavior without changing existing code.

### Liskov Substitution Principle (LSP)

Subclasses must work wherever the base class works. In simpler terms, extending a class should not narrow the functionality.

### Interface Segregation Principle (ISP)

Prefer small, focused interfaces over large, general purpose ones. Dont force classes to implement methods they don't need.

### Dependency Inversion Principle (DIP)

DIP states that our code should depend on abstractions, not concrete implementation.



