# Contributing to ForgingBlocks

Thank you for your interest in contributing to ForgingBlocks.

This document is a quick orientation. For the full guide covering development setup, testing, code standards, and automation hooks, see the docs.

## What You Can Contribute

- Bug fixes and improvements
- Documentation clarifications and examples
- New abstractions that align with the existing design
- Tooling, automation, and developer experience improvements

## Quick Setup

```bash
# Fork, clone, install
git clone https://github.com/<username>/forging-blocks.git
cd forging-blocks
poetry install

# Install automation hooks
pre-commit install
pre-commit install --hook-type pre-push
```

## Full Documentation

- [Contributing Guide](https://forging-blocks-org.github.io/forging-blocks/dev/contributing/) — development setup, testing guidelines, code standards, PR process
- [Testing Guide](https://forging-blocks-org.github.io/forging-blocks/dev/guide/testing/) — detailed testing examples
- [Release Guide](https://forging-blocks-org.github.io/forging-blocks/dev/contributing/release-guide/) — release process for maintainers
