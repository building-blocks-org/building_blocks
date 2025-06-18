# Examples Overview & Backlog

Welcome to the **Examples Overview & Backlog** for the Building Blocks library!
This document is both a catalog of existing examples and a living backlog of planned or proposed examples.

---

## Examples Backlog Table

| Example Name   | Status      | Domain/Theme        | Stack / Frameworks         | Owner/Lead   | Notes / Learning Goals                              |
|----------------|-------------|---------------------|----------------------------|--------------|-----------------------------------------------------|
| taskflow       | In Progress | Task Manager        | Script, FastAPI            | gbrennon     | End-to-end: CLI then web; shows evolution from script to API; deep dive on aggregates, CQRS, event handling, and layering decisions. |
| orderly        | Planned     | Order Management    | FastAPI, Django            |              | E-commerce domain; covers order lifecycles, payments, and notifications; demonstrates business rules, domain events, extensibility, and integration with adapters. |
| gatekeeper     | Planned     | Auth System         | FastAPI, Django            |              | Full auth lifecycle: registration, login, RBAC, password reset; explicit boundary between domain and infra; security best practices and pluggable adapters for auth strategies. |
| datastreamer   | Planned     | Data Pipeline / ETL | Script, FastAPI            |              | Clean architecture for data ingestion/analytics; ports/adapters for sources/sinks and transform steps; testable business logic; plug-and-play adapters for external systems. |
| blogcraft      | Idea        | Blogging Platform   | FastAPI, Django            |              | CQRS/read-write separation; moderation workflows; aggregates for posts/comments; real-world UGC and content moderation patterns. |
| evently        | Idea        | Event Booking       | FastAPI, Flask             |              | To be defined: candidate for demonstrating process managers, seat reservation concurrency, and event-driven workflows. |
| stockroom      | Idea        | Inventory Mgmt      | FastAPI, CLI               |              | To be defined: inventory, suppliers, stock movements, domain services, and reporting. |
| notifier       | Idea        | Notification Svc    | FastAPI, Kafka, Celery     |              | To be improved: event-driven, outbound ports, multiple notification channels (email, SMS, push), and integration patterns. |
| ledger         | Idea        | Bank Account        | FastAPI, Flask             |              | To be improved: rich domain, transactional boundaries, security, balance tracking, and auditability. |
| catalogue      | Idea        | Product Catalog     | FastAPI, Django, CLI       |              | To be improved: product aggregates, categories, pricing logic, extensibility, and advanced querying. |

---

## Example Details and Notes

### taskflow

- **Status:** In Progress
- **Theme:** Task management (To-do list)
- **Stack:** Simple script (CLI), then FastAPI
- **Goals:**
  - Start with a CLI/simple-script for core domain modeling.
  - Evolve to a FastAPI-based web version to demonstrate adaptation.
  - Show: Entities, Value Objects, Aggregates, Use Cases, Repositories, Adapters.
  - Demonstrate CQRS and basic event handling.
  - Explicit documentation on layering and architectural trade-offs.
- **Learning Points:**
  - How a simple domain grows from script to API.
  - Clean layering in real-world evolution.
  - Testing business logic in isolation.

---

### orderly

- **Status:** Planned
- **Theme:** E-commerce order management
- **Stack:** FastAPI, Django
- **Goals:**
  - Full DDD: aggregates, repositories, domain events, business invariants.
  - Integrate with payment, inventory, notification (as ports/adapters).
  - Extensible for new payment types, events, and notification channels.
- **Learning Points:**
  - Real-world business rules and event-driven design.
  - Infrastructure adaptation (DBs, external services).
  - API evolution and modularity.

---

### gatekeeper

- **Status:** Planned
- **Theme:** User registration, authentication, authorization
- **Stack:** FastAPI, Django
- **Goals:**
  - Clear boundary between domain logic and infrastructure for authentication.
  - Use value objects for email/password.
  - Demonstrate RBAC and flexible role strategies.
  - Pluggable adapters for JWT and session auth.
- **Learning Points:**
  - Security and clean boundaries in DDD.
  - Interface segregation and pluggability.
  - Handling sensitive data (passwords, tokens).

---

### datastreamer

- **Status:** Planned
- **Theme:** Data ingestion, ETL, analytics
- **Stack:** Script, FastAPI
- **Goals:**
  - Hexagonal architecture for data pipelines (ports: source, sink, transform).
  - Easily extendable with new data sources/sinks (CSV, DB, Kafka).
  - Demonstrate testable business logic and clear separation of concerns.
- **Learning Points:**
  - Clean separation in data-heavy/analytics contexts.
  - Building testable ETL pipelines with hexagonal patterns.

---

### blogcraft

- **Status:** Idea
- **Theme:** Blogging platform (posts, comments)
- **Stack:** FastAPI, Django
- **Goals:**
  - CQRS: separate write/read models.
  - UGC moderation workflows and process managers.
  - Aggregates for posts and comments, tagging, and extensibility.
- **Learning Points:**
  - Modularity via CQRS and process managers.
  - Real-world content moderation and UGC patterns.

---

### evently

- **Status:** Idea
- **Theme:** Event ticket booking
- **Stack:** FastAPI, Flask
- **Goals/Notes:** To be defined: candidate for process managers, seat reservation concurrency, and event-driven workflows.

---

### stockroom

- **Status:** Idea
- **Theme:** Inventory management
- **Stack:** FastAPI, CLI
- **Goals/Notes:** To be defined: inventory, suppliers, stock movements, domain services, and reporting.

---

### notifier

- **Status:** Idea
- **Theme:** Notification/messaging system
- **Stack:** FastAPI, Kafka, Celery
- **Goals/Notes:** To be improved: event-driven, outbound ports, multiple notification channels, and integration patterns.

---

### ledger

- **Status:** Idea
- **Theme:** Simple bank account/wallet
- **Stack:** FastAPI, Flask
- **Goals/Notes:** To be improved: rich domain, business invariants, transactional boundaries, and auditability.

---

### catalogue

- **Status:** Idea
- **Theme:** Product catalog
- **Stack:** FastAPI, Django, CLI
- **Goals/Notes:** To be improved: product aggregates, categories, pricing, extensibility.

---

## Contribution Guidelines

- To pick up an example, comment your intent in the [Discussions](https://github.com/gbrennon/building-blocks/discussions) or open an issue.
- When working on an example, update this file with status, notes, and learning goals.
- Each example should have its own `README.md` with its architecture, design notes, and instructions.
- Focus on clear, educational code and explanations.

---
