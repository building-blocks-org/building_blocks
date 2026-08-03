# Errors

Foundation provides a **structured error model** — every failure carries a message, metadata, and a typed identity.

## Core types

- **Error** — Base class. Carries an `ErrorMessage` and `ErrorMetadata`.
- **ErrorMessage** — A value object representing the human-readable description.
- **ErrorMetadata** — Context dict for extra fields (field name, detail, codes).
- **FieldReference** — A value object referencing a field by name (`value: str`).

## Concrete error types

### Validation
- **ValidationError** — Abstract base for validation failures. Not meant to be thrown directly.
- **ValidationFailedError** — Concrete validation error. The type to raise when input validation fails.
- **FieldErrors** — Groups errors by field. Carries a `FieldReference` and child errors.
- **CombinedErrors** — Groups multiple errors from different sources.
- **ValidationFieldErrors** — Groups validation errors for a specific field. Carries a `FieldReference` and child errors.
- **CombinedValidationErrors** — Groups multiple validation errors that share the `ValueErrorMixin` taxonomy.

### Rule violations
- **RuleViolationError** — Abstract base for business rule failures. Not meant to be thrown directly.
- **RuleViolatedError** — Concrete rule violation error. The type to raise when a business rule is violated.
- **CombinedRuleViolationErrors** — Groups multiple rule violation errors that share the `RuntimeErrorMixin` taxonomy.

### Structural errors
- **ArchitectureError** — Raised when a structural invariant of the architecture is violated.
- **CantModifyImmutableAttributeError** — Raised when a frozen attribute is reassigned.
- **ConfigurationError** — Raised when configuration is invalid.
- **NoneNotAllowedError** — Raised when `None` is provided where disallowed.
- **NonHashableValueError** — Raised when a non-hashable value is provided where hashability is required.
- **NotCallablePredicateError** — Raised when a specification predicate is not callable.
- **ResultAccessError** — Raised when accessing `value` on `Err` or `error` on `Ok`.


## Built-in taxonomy

Concrete errors include mixins that make them catchable as Python built-in types:

- **`ValueError`** — Input and precondition errors inherit `ValueErrorMixin`:
    `ValidationFailedError`, `ConfigurationError`, `NoneNotAllowedError`,
    `NonHashableValueError`, `NotCallablePredicateError`,
    `ValidationFieldErrors`, `CombinedValidationErrors`

    ```python
    except ValueError:  # catches all of the above
    ```

- **`RuntimeError`** — State and invariant errors inherit `RuntimeErrorMixin`:
    `RuleViolatedError`, `ArchitectureError`,
    `CantModifyImmutableAttributeError`, `ResultAccessError`,
    `CombinedRuleViolationErrors`

    ```python
    except RuntimeError:  # catches all of the above
    ```

The root `Error` class does **not** include either mixin. Domain and application
errors inherit the mixin from the appropriate base class — see their reference
pages for details.

## When to use

Subclass `Error` for your own error types. Raise `ValidationFailedError` for input failures, `RuleViolatedError` for business rule violations. Use `FieldErrors` and `CombinedErrors` to group multiple failures. Every error carries an `ErrorMessage` and `ErrorMetadata` for structured handling.

!!! note "Related"
    See [Domain Errors](../domain/errors.md) and [Application Errors](../application/errors.md) for block-specific error types.
