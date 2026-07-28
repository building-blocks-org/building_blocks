# Architectural Styles

## How to read these pages

This section explores **well-known architectural styles** as they appear in the software architecture literature.

These pages are not a source of definitions.
They are intended to help you **relate ForgingBlocks concepts** to architectural styles you may already know.

---

## Quick summary

This section explores **well-known architectural styles** (Clean Architecture, Hexagonal, Layered, CQRS, Event-Driven, MVC) as they appear in software architecture literature. It helps you **relate ForgingBlocks concepts** to styles you may already know.

- **Clean Architecture** — Dependency inversion with entities at the center; ForgingBlocks types define the core
- **Hexagonal Architecture** — Ports and adapters isolating domain logic; ForgingBlocks ports define the boundaries
- **Layered Architecture** — Hierarchical separation of concerns; ForgingBlocks types populate each layer
- **CQRS** — Separate read and write models; ForgingBlocks types define commands, queries, and projections
- **Event-Driven** — Loose coupling through events; ForgingBlocks types define messages and handlers
- **MVC** — Separates presentation into Model, View, and Controller; ForgingBlocks types define the Model

Key points:
- Pages are **explanatory, not prescriptive** — no definitions, no imposed architecture, no recommendations
- Each page describes one style, uses neutral terminology, shows how ForgingBlocks concepts *project* onto it
- **Reference** section remains the source of truth for responsibilities/boundaries
- You can read any page in isolation or skip this section entirely

Useful if: you know a style and want to map it to ForgingBlocks, want to compare styles, or are exploring trade-offs.

---

## What these pages are

Each page in this section:

- Describes a single architectural style.
- Uses neutral, literature-aligned terminology.
- Shows how ForgingBlocks concepts can be *projected* onto that style.

The intent is explanatory, not prescriptive.

---

## What these pages are not

These pages do **not**:

- Define the meaning of Domain, Application, or Infrastructure.
- Impose a preferred architecture.
- Recommend one style over another.

The **Reference** section remains the source of truth for responsibilities and boundaries.

---

## When this section is useful

You may find this section helpful if you:

- Are familiar with an architectural style and want to map it to ForgingBlocks.
- Want to compare styles using a shared vocabulary.
- Are exploring design trade-offs.

If none of those apply, you can safely skip this section.
