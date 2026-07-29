# Release Guide

ForgingBlocks follows a **local-preparation + automated-publishing model**: contributors prepare releases locally, create PRs for review, and GitHub Actions handles publishing automatically after merge.

## Quick Release

```bash
# 1. Validate
git checkout main && git pull origin main

# 2. Simulate first (always safe)
poetry run poe release patch

# 3. Execute when ready
poetry run poe release patch --execute

# 4. Review and merge the created PR
```

## Full Documentation

- [Release Guide](https://forging-blocks-org.github.io/forging-blocks/dev/contributing/release-guide/) — complete reference: mental model, commit conventions, release flow diagram, command reference, maintainer checklist, and versioned docs.
