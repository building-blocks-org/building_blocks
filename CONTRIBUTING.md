# Contributing to Building Blocks

We welcome contributions from the community! Whether you're fixing a bug, adding a feature, or improving documentation, your help is appreciated.

## How to Contribute

1.  **Fork the repository** on GitHub.
2.  **Clone your fork** to your local machine.
3.  **Set up the development environment**:
    ```bash
    poetry install
    ```
4.  **Create a new branch** for your changes:
    ```bash
    git checkout -b my-feature-branch
    ```
5.  **Make your changes**.
6.  **Run the tests**:
    ```bash
    poetry run pytest
    ```
7.  **Commit your changes** with a clear commit message.
8.  **Push your changes** to your fork.
9.  **Create a pull request** to the `main` branch of the original repository.

## Code Style

We use `black` for code formatting and `isort` for import sorting. Please run these tools before committing your changes.

```bash
poetry run black .
poetry run isort .
```

## Reporting Bugs

If you find a bug, please open an issue on our [GitHub issue tracker](https://github.com/gbrennon/building-blocks/issues). Include as much detail as possible, such as:

- A clear description of the bug.
- Steps to reproduce the bug.
- The expected behavior.
- The actual behavior.
- Your Python version and the version of `building_blocks`.

Thank you for contributing!
