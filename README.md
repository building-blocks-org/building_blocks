# ForgingBlocks

Composable **abstractions and interfaces** for writing clean, testable, and maintainable Python code.

[![Python](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![Poetry](https://img.shields.io/badge/packaging-poetry-blue.svg)](https://python-poetry.org/)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](https://mypy-lang.org/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![CI](https://github.com/forging-blocks-org/forging-blocks/workflows/CI/badge.svg)](https://github.com/forging-blocks-org/forging-blocks/actions/workflows/ci.yml)

---

## Overview

> Not a framework — a **toolkit** of composable contracts and abstractions.

**ForgingBlocks** provides layer-agnostic foundations for clean architecture in Python: `Result` for explicit error handling, `ValueObject` for domain modeling, ports and adapters for dependency inversion, and more. Use what you need; ignore the rest. It doesn't dictate your architecture — it gives you the language to define one.

---

## Installation

```bash
pip install forging-blocks          # pip
poetry add forging-blocks           # Poetry
uv add forging-blocks               # uv
```

**Requires Python 3.14+**

---

## Quick Example

```python
from forging_blocks.foundation import Result, Ok, Err

def divide(a: float, b: float) -> Result[float, str]:
    if b == 0:
        return Err("Don't divide by zero")
    return Ok(a / b)

result = divide(10, 2).map(lambda n: f"Result: {n}")
print(result.value)  # "Result: 5.0"
```

---

## Documentation

- [Full Documentation](https://forging-blocks-org.github.io/forging-blocks/dev/)
- [Getting Started](https://forging-blocks-org.github.io/forging-blocks/dev/guide/getting-started/)
- [Blocks Overview](https://forging-blocks-org.github.io/forging-blocks/dev/guide/recommended_blocks_structure/)
- [Architecture Overview](https://forging-blocks-org.github.io/forging-blocks/dev/guide/architecture-overview/)
- [Testing Guide](https://forging-blocks-org.github.io/forging-blocks/dev/guide/testing/)
- [API Reference](https://forging-blocks-org.github.io/forging-blocks/dev/reference/)
- [Contributing Guide](https://forging-blocks-org.github.io/forging-blocks/dev/contributing/)
- [Release Guide](https://forging-blocks-org.github.io/forging-blocks/dev/contributing/release-guide/)

---

## License

MIT — see [LICENSE](LICENSE)

---

_**ForgingBlocks** — foundations for clean, testable, and maintainable Python architectures._
