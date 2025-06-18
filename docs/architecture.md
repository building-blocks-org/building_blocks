# Architecture Guide

`building_blocks` is designed around the principles of Clean Architecture and Hexagonal Architecture (Ports and Adapters). This guide provides a deep dive into the structure and philosophy of the library.

## Core Principles

- **Separation of Concerns**: The library enforces a strict separation between the domain, application, and infrastructure layers.
- **Dependency Rule**: Dependencies flow inwards. The domain layer has no knowledge of the application layer, and the application layer has no knowledge of the infrastructure or presentation layers.
- **Framework Agnostic**: The core logic of your application should not depend on any specific framework (like FastAPI, Django, or Flask).

## Layers

The architecture is divided into the following layers:

### 1. Domain Layer

This is the core of your application. It contains the business logic, entities, and rules.

- **Entities**: Objects representing core business concepts (e.g., `Order`, `Product`).
- **Value Objects**: Immutable objects representing descriptive aspects of the domain (e.g., `Address`, `Money`).
- **Aggregates**: Clusters of domain objects that can be treated as a single unit.
- **Domain Services**: Operations that don't naturally fit within an entity.
- **Domain Events**: Represent significant events that occurred in the domain.

### 2. Application Layer

This layer orchestrates the use cases of your application. It contains the application logic and defines the ports for interacting with the outside world.

- **Application Services**: Implement the application's use cases. They coordinate the domain layer to perform tasks.
- **Inbound Ports**: Define how the application can be driven by external actors (e.g., a web controller, a CLI command). These are typically implemented as abstract base classes or interfaces.
- **Outbound Ports**: Define the interfaces for services that the application needs to communicate with the outside world (e.g., a database, a message broker).

### ASCII Diagram

```
      +----------------------------------------------------------------+
      |                        Presentation Layer                      |
      |        (Controllers, Views, CLI Commands, etc.)                |
      +----------------------------------------------------------------+
                                      |
                                      v
+-------------------------------------+--------------------------------------+
|             Application Layer (Ports)                                      |
|                                                                            |
|   +-------------------+       +-----------------------+                    |
|   |  Inbound Ports    |------>|  Application Services |                    |
|   | (Use Case ABCs)   |       |   (Orchestration)     |                    |
|   +-------------------+       +-----------------------+                    |
|                                      |                                     |
|                                      v (drives)                            |
|   +-------------------+       +-----------------------+                    |
|   |  Outbound Ports   |<------|                       |                    |
|   | (Repository ABCs) |       |                       |                    |
|   +-------------------+       +-----------------------+                    |
|                                                                            |
+-------------------------------------+--------------------------------------+
                                      |
                                      v
+-------------------------------------+--------------------------------------+
|                     Domain Layer                                           |
|                                                                            |
|   +-------------------+       +-----------------------+                    |
|   |      Entities     |       |    Domain Services    |                    |
|   +-------------------+       +-----------------------+                    |
|                                                                            |
+----------------------------------------------------------------------------+
```

## Port Architecture

The "ports" in hexagonal architecture are the boundaries of your application.

- **Inbound Ports**: Define the API of the application layer. In `building_blocks`, these are abstract classes that your presentation layer will call.
- **Outbound Ports**: Define the interfaces needed by your application to get data from or send data to external systems. Your infrastructure layer will provide concrete implementations (adapters) for these ports.

This separation ensures that your core application and domain logic remain pure and isolated from the details of external technologies.
