#!/bin/bash

# Interactive Help System for Building Blocks
# Provides contextual help and discovery

set -e

# Colors
readonly GREEN='\033[0;32m'
readonly BLUE='\033[0;34m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m'

show_main_menu() {
    cat << EOF
🚀 Building Blocks Help System

What would you like to do?

1) Create a new example project
2) Learn about project types
3) See usage examples
4) Troubleshoot issues
5) View development workflow
6) Check quality standards
7) Browse documentation

q) Quit

EOF
    read -p "Enter your choice (1-7, q): " choice

    case $choice in
        1) create_project_wizard ;;
        2) ./scripts/create-example-project.sh --list-types ;;
        3) ./scripts/create-example-project.sh --examples ;;
        4) show_troubleshooting ;;
        5) show_workflow ;;
        6) show_quality ;;
        7) show_docs ;;
        q|Q) exit 0 ;;
        *) echo "Invalid choice. Try again." && show_main_menu ;;
    esac
}

create_project_wizard() {
    echo -e "${BLUE}📋 Project Creation Wizard${NC}"
    echo ""

    # Get project name
    read -p "Project name (e.g., taskflow): " project_name
    if [[ -z "$project_name" ]]; then
        echo "Project name required!"
        return
    fi

    # Get project type
    echo ""
    echo "Available project types:"
    echo "1) clean-ddd (recommended for learning)"
    echo "2) primitive-obsession (anti-pattern example)"
    echo "3) event-driven (CQRS + Event Sourcing)"
    echo "4) microservice (API-focused service)"
    echo "5) monolith (modular monolith)"

    read -p "Choose type (1-5): " type_choice

    case $type_choice in
        1) project_type="clean-ddd" ;;
        2) project_type="primitive-obsession" ;;
        3) project_type="event-driven" ;;
        4) project_type="microservice" ;;
        5) project_type="monolith" ;;
        *) project_type="clean-ddd" ;;
    esac

    # Confirm and create
    echo ""
    echo -e "${YELLOW}Creating project:${NC}"
    echo "  Name: $project_name"
    echo "  Type: $project_type"
    echo ""
    read -p "Proceed? (y/N): " confirm

    if [[ "$confirm" =~ ^[Yy]$ ]]; then
        ./scripts/create-example-project.sh "$project_name" --type "$project_type"

        echo ""
        echo -e "${GREEN}✅ Project created!${NC}"
        echo ""
        echo "Next steps:"
        echo "  cd examples/$project_name"
        echo "  poetry shell"
        echo "  ./scripts/dev-setup.sh"
    fi
}

show_troubleshooting() {
    cat << EOF
🔧 Common Issues & Solutions

Issue: "Poetry not found"
Solution: Install Poetry from https://python-poetry.org/docs/#installation

Issue: "Project already exists"
Solution: Use --force flag or choose different name

Issue: "Building-blocks import failed"
Solution: Ensure you're in building-blocks repository root

Issue: "Permission denied"
Solution: Make script executable: chmod +x scripts/create-example-project.sh

Issue: "Tests failing"
Solution: Run from project directory: cd examples/project && poetry run pytest

Need more help? Check docs/tooling/troubleshooting.md
EOF

    read -p "Press Enter to continue..."
    show_main_menu
}

show_workflow() {
    cat << EOF
🔄 Development Workflow

1. Create Project:
   ./scripts/create-example-project.sh my_project

2. Setup Environment:
   cd examples/my_project
   poetry shell
   ./scripts/dev-setup.sh

3. Implement Features:
   - Start with domain layer (entities, value objects)
   - Add application services (use cases)
   - Create infrastructure adapters
   - Build presentation layer

4. Quality Checks:
   ./scripts/quality-check.sh
   ./scripts/test.sh

5. Repository-wide Checks:
   cd ../../
   make check  # or poetry run quality-check.sh

More details: docs/tooling/development-workflow.md
EOF

    read -p "Press Enter to continue..."
    show_main_menu
}

show_quality() {
    cat << EOF
📊 Quality Standards

Code Formatting:
  ✅ Black (line length: 88)
  ✅ Ruff (linting + import sorting)

Type Checking:
  ✅ MyPy (strict mode)

Security:
  ✅ Bandit (security linting)

Testing:
  ✅ Pytest (with coverage reporting)
  ✅ Minimum 80% coverage

Quality Commands:
  poetry run black --check .
  poetry run ruff check .
  poetry run mypy src/
  poetry run bandit -r src/
  poetry run pytest --cov=src

More details: docs/tooling/quality-gates.md
EOF

    read -p "Press Enter to continue..."
    show_main_menu
}

show_docs() {
    cat << EOF
📚 Documentation

Local Documentation:
  docs/tooling/                  - Tool documentation
  docs/architecture/             - Architecture guides
  docs/examples/                 - Example walkthroughs
  docs/api/                      - API reference

Online Resources:
  README.md                      - Getting started
  CONTRIBUTING.md                - Contribution guide
  examples/*/README.md           - Example-specific docs

Quick Access:
  make docs                      - Build documentation
  make help                      - Show all make targets
  ./scripts/help.sh              - This help system

EOF

    read -p "Press Enter to continue..."
    show_main_menu
}

# Start the help system
echo "Welcome to Building Blocks Help System!"
echo "======================================"
echo ""
show_main_menu
