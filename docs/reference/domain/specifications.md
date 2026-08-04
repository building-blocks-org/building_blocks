# Specifications

The **Specification** pattern expresses composable business rules as predicates over candidate objects.

A `Specification` encapsulates a rule evaluated with `is_satisfied_by(candidate)`. Compositions (`&`, `|`, `~`) allow rules to be combined into richer predicates.

## When to use

Subclass `Specification` and implement `is_satisfied_by(candidate) → bool`. Compose with `&`, `|`, `~` instead of nesting if-statements. Each specification is a single, testable unit of logic.

## ComposableSpecification

`ComposableSpecification` combines multiple specifications into a single rule using logical operators
(`&`, `|`, `~`) and short-circuits:

- `AndSpecification` — Both specifications must be satisfied.
- `OrSpecification` — At least one specification must be satisfied.
- `NotSpecification` — The specification must not be satisfied.

Each operator returns a new `ComposableSpecification` instance, so chains are immutable and
composable without side effects.

!!! note "Where the implementation lives"

    The specification pattern is defined in the Domain block alongside Entity and AggregateRoot. It is imported from `forging_blocks.domain.specification`.
