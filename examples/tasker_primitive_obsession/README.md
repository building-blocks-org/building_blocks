# Tasker: Primitive Obsession Example

## What is Primitive Obsession?

**Primitive Obsession** is an anti-pattern where you use primitive types (like `str`, `int`, `float`, etc.) to represent domain concepts that deserve their own types. This leads to code that is harder to understand, maintain, and extend.
It’s a common smell in codebases that haven’t adopted Domain-Driven Design (DDD), strong typing, or clean architecture principles.

**Symptoms of Primitive Obsession:**
- Using `str` for things like email, user ID, role, etc.
- Passing around raw `int` or `str` values in functions, instead of explicit value objects or domain entities
- Lack of validation encapsulated in types (e.g. any string can be used as an email address or user ID)

**Why is it a problem?**
- Harder to spot bugs (you might swap parameters or pass the wrong value)
- Validation and rules are scattered, not enforced at the boundary
- Harder to refactor or change domain rules
- Code is less readable (what does this `str` actually represent?)

---

## About This Example

This `Tasker Primitive Obsession` example is a simple task management application that allows you to:

- Register a user
- Sign in as a user
- Change a user's role
- Create a task

**BUT:**
This implementation intentionally uses primitive types (`str`, `int`, etc.) everywhere—even for things like user IDs, emails, roles, and task descriptions—to highlight the drawbacks of this approach.

---

## How to Read This Example

### What to Look For

- **Function signatures** using generic types (`str`, `int`) for domain concepts
- **Lack of validation** or encapsulation—any value can be passed, no protection against invalid data
- **Business rules** (like role validation or email structure) are not enforced by the type system
- **Bug-prone code**: It’s easy to swap parameters or introduce subtle bugs

---

## Why Is This Bad?

- **No compile-time safety:** You can pass an email where a role is expected, and the code won’t complain until runtime (if at all).
- **No centralized validation:** Validation is scattered or missing; bugs can creep in easily.
- **Harder to refactor:** If you want to change how roles or emails are handled, you have to find every place they’re used as `str`.
- **Domain logic is leaky:** Business concepts are not explicit in the code, leading to confusion and bugs.

---

## What’s the Alternative?

In a strongly-typed, DDD-inspired or "clean" design, you would use **Value Objects** (or Enums, or custom types) for core domain concepts:

- `UserId`
- `EmailAddress`
- `UserRole` (as an Enum or Value Object)
- `TaskDescription`

This encapsulates validation, clarifies intent, and makes your code easier to maintain and extend.

*Check out the `tasker_strongly_typed` example for a better approach!*

---

## Running the Example

> **This example is intentionally “bad” to demonstrate the anti-pattern.
> See the strongly typed version for best practices!**

To run this example:

```shell
docker compose up --build
```

---

## Further Reading

- [Martin Fowler: Primitive Obsession](https://martinfowler.com/bliki/PrimitiveObsession.html)
- [Domain-Driven Design Reference](https://www.domainlanguage.com/ddd/reference/)
- [Refactoring.Guru: Primitive Obsession](https://refactoring.guru/smells/primitive-obsession)

---

**Explore, learn, and see how strong typing and Value Objects can make your code safer and more expressive!**
