# Examples Overview

This table documents the planned and suggested examples to showcase how to use the library/toolbox for building clean/hexagonal architecture applications with SOLID and DDD principles.

| Example Name      | Theme/Idea                           | Concept Focus                                  | Stack / Frameworks                | Layers Used                        | Notes / Features                                   |
|-------------------|--------------------------------------|------------------------------------------------|-----------------------------------|-------------------------------------|----------------------------------------------------|
| **taskflow**      | Task Manager                         | Aggregates, CQRS, Event Sourcing               | Simple script, CLI, FastAPI, Flask| Application, Domain, Infra, Present.| Start simple, then scale up to web example          |
| **orderly**       | Order Management (E-commerce)        | Domain events, business rules, DDD patterns    | FastAPI, Django                   | All                                 | CRUD, order state, payments, notifications         |
| **gatekeeper**    | User Auth (registration/login)       | Boundaries, security, user entity, value objs  | FastAPI, Django                   | All                                 | Auth flows, RBAC, password reset, JWT, etc.        |
| **datastreamer**  | Data Pipeline / ETL                  | Ports/adapters, hexagonal, streaming           | Script, FastAPI                   | All                                 | Ingest, transform, store data, metrics             |
| **blogcraft**     | Blogging Platform                    | UGC, moderation, read/write separation         | FastAPI, Django, Flask            | All                                 | Posts, comments, tags, moderation                  |
| **evently**       | Event Booking                        | Concurrency, value objects, process managers   | FastAPI, Flask                    | All                                 | Book/cancel seats, event status, notifications     |
| **stockroom**     | Inventory Management                 | Aggregates, domain services, reporting         | FastAPI, Django, CLI              | All                                 | Stock in/out, suppliers, inventory queries         |
| **notifier**      | Messaging/Notification System        | Event-driven, external integration, adapters   | FastAPI, Kafka, Celery            | All                                 | Send notifications via email, SMS, push, etc.      |
| **ledger**        | Bank Account / Wallet                | Transactions, security, business rules         | FastAPI, Flask                    | All                                 | Accounts, transfers, transaction log, balances     |
| **catalogue**     | Product Catalog                      | Aggregates, value objects, repository pattern  | FastAPI, Django, CLI              | All                                 | Manage products, categories, pricing               |

---

## Columns

- **Example Name:** Short, memorable project name for the example.
- **Theme/Idea:** Real-world domain modeled in the example.
- **Concept Focus:** Key software architecture or DDD concepts emphasized.
- **Stack / Frameworks:** Frameworks/libraries used in the example (e.g., FastAPI, Django, Flask, CLI).
- **Layers Used:** Application, Domain, Infrastructure, Presentation (all examples aim to use all four).
- **Notes / Features:** Features, flows, or aspects that make the example educational and relevant.

---

> This table can be expanded as new examples are added or refined. Each example should include a README.md and, if applicable, a docker-compose.yml for external services.
