# Architecture Guide

`building_blocks` is designed around the principles of Clean Architecture and Hexagonal Architecture (Ports and Adapters). This guide provides a deep dive into the structure and philosophy of the library.

## Core Principles

- **Separation of Concerns**: The library enforces a strict separation between the domain, application, and infrastructure layers.
- **Dependency Rule**: Dependencies flow inwards. The domain layer has no knowledge of the application layer, and the application layer has no knowledge of the infrastructure or presentation layers.
- **Framework Agnostic**: The core logic of your application should not depend on any specific framework (like FastAPI, Django, or Flask).

## Layers

The architecture is divided into the following layers.

### 1. Domain Layer

This is the heart of your application, containing the business logic, entities, and rules, completely independent of any technical implementation details.

- **What it is**: It contains `Entities`, `Value Objects`, `Aggregates`, `Domain Services`, and `Domain Events`.
- **How `building_blocks` helps**: The library provides base classes and helpers to model your domain effectively. For example, you might have `building_blocks.domain.Entity` or `building_blocks.domain.AggregateRoot` that provide common functionality like identity management and domain event tracking.

### 2. Application Layer

This layer orchestrates the use cases of your application. It contains the application logic and defines the "ports" for interacting with the outside world.

- **What it is**: It contains `Application Services` (Use Cases) that execute business workflows, and the `Inbound` and `Outbound Ports` that define the application's boundaries.
- **How `building_blocks` helps**: The library gives you structures to define these boundaries cleanly. You might use a `building_blocks.application.UseCase` base class to structure your services or `building_blocks.application.Port` as a marker interface for your repository contracts.

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

The "ports" in hexagonal architecture are the boundaries of your application, defined within the Application Layer.

- **Inbound Ports**: Define the API of the application layer. In `building_blocks`, these are abstract classes that your presentation layer will call. They represent the "use cases" of the system.
- **Outbound Ports**: Define the interfaces needed by your application to get data from or send data to external systems (e.g., a database). Your infrastructure layer will provide concrete implementations (adapters) for these ports.

This separation ensures that your core application and domain logic remain pure and isolated from the details of external technologies.
