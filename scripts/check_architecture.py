#!/usr/bin/env python3
"""
Clean Architecture dependency validation script.
Ensures proper layered architecture following hexagonal/clean architecture principles.
"""

import ast
import sys
from pathlib import Path


class ArchitectureValidator:
    """Validates clean architecture layer dependencies."""

    LAYERS = {
        "domain": 0,  # Core business logic - no external dependencies
        "application": 1,  # Use cases - can depend on domain
        "infrastructure": 2,  # External concerns - can depend on domain/application
        "presentation": 2,  # UI/API layer - can depend on domain/application
    }

    FORBIDDEN_IMPORTS = {
        "domain": [
            "flask",
            "fastapi",
            "django",
            "sqlalchemy",
            "requests",
            "http",
            "redis",
            "boto3",
            "kafka",
            "celery",
        ],
        "application": ["flask", "fastapi", "django", "sqlalchemy", "requests", "http"],
    }

    def __init__(self, src_path: Path):
        self.src_path = src_path
        self.violations: list[str] = []

    def validate(self) -> bool:
        """Run all architecture validations."""
        self._check_forbidden_imports()

        if self.violations:
            print("🏗️  Architecture Violations Found:")
            for violation in self.violations:
                print(f"   ❌ {violation}")
            return False

        print("✅ Clean Architecture validated successfully!")
        return True

    def _check_forbidden_imports(self):
        """Check for forbidden external dependencies in specific layers."""
        for layer, forbidden in self.FORBIDDEN_IMPORTS.items():
            layer_files = list(self.src_path.rglob(f"*/{layer}/**/*.py"))

            for py_file in layer_files:
                if py_file.name == "__init__.py":
                    continue

                imports = self._extract_imports(py_file)
                for import_path in imports:
                    if any(forbidden_lib in import_path for forbidden_lib in forbidden):
                        self.violations.append(
                            f"{py_file.relative_to(self.src_path)}: "
                            f"{layer} layer contains forbidden import: {import_path}"
                        )

    def _extract_imports(self, file_path: Path) -> set[str]:
        """Extract all import statements from a Python file."""
        try:
            with open(file_path, encoding="utf-8") as f:
                tree = ast.parse(f.read())
        except Exception:
            return set()

        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module)

        return imports


def main():
    """Main validation entry point."""
    src_path = Path("src")
    if not src_path.exists():
        print("❌ src/ directory not found")
        sys.exit(1)

    validator = ArchitectureValidator(src_path)
    if not validator.validate():
        sys.exit(1)


if __name__ == "__main__":
    main()
