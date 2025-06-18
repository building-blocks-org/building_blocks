#!/bin/bash

# Building Blocks Example Project Creator
# Creates properly structured example projects with correct Poetry configuration
# Author: Glauber Brennon <glauberbrennon@gmail.com>
# Usage: ./scripts/create-example-project.sh <project-name> [options]

set -e

# Script metadata
SCRIPT_VERSION="1.1.0"
SCRIPT_AUTHOR="Glauber Brennon"
SCRIPT_EMAIL="glauberbrennon@gmail.com"

# ... (previous color definitions and config)

# Enhanced help with comprehensive examples
show_help() {
    cat << EOF
🚀 Building Blocks Example Project Creator v${SCRIPT_VERSION}

DESCRIPTION:
    Creates fully-structured example projects showcasing the building-blocks library
    with different architectural patterns and complexity levels.

USAGE:
    $(basename "$0") <project-name> [options]

ARGUMENTS:
    project-name    Name of the project to create (required)
                   Must start with letter, contain only letters, numbers, _, -

OPTIONS:
    -t, --type TYPE         Project type (default: clean-ddd)
    -f, --force            Force overwrite if project exists
    -v, --verbose          Enable verbose output for debugging
    -d, --dry-run          Show what would be created without creating
    -l, --list-types       List all available project types with descriptions
    -e, --examples         Show comprehensive usage examples
    -h, --help             Show this help message

PROJECT TYPES:
EOF

    for type in "${!PROJECT_TYPES[@]}"; do
        printf "    %-20s %s\n" "$type" "${PROJECT_TYPES[$type]}"
    done

    cat << EOF

QUICK EXAMPLES:
    # Create a clean DDD example (most common)
    $(basename "$0") taskflow

    # Create anti-pattern comparison
    $(basename "$0") taskflow_bad --type primitive-obsession

    # Preview what would be created
    $(basename "$0") my_service --type microservice --dry-run

    # Force recreate existing project
    $(basename "$0") existing_project --force

MORE EXAMPLES:
    Use --examples flag for comprehensive usage scenarios

DOCUMENTATION:
    Local docs:  ./docs/tooling/project-creator.md
    Online:      https://github.com/gbrennon/building-blocks#tooling

AUTHOR:
    ${SCRIPT_AUTHOR} <${SCRIPT_EMAIL}>

TIP: Use 'make help' from repository root for all available commands
EOF
}

# Show comprehensive examples
show_examples() {
    cat << EOF
🎯 Comprehensive Usage Examples

BASIC USAGE:
    # Create your first example (recommended starting point)
    $(basename "$0") my_first_example

    # This creates a clean-ddd project with:
    # ✅ Complete domain layer (entities, value objects, events)
    # ✅ Application services with proper use cases
    # ✅ Infrastructure adapters
    # ✅ CLI interface with Typer
    # ✅ Comprehensive test suite

COMPARISON PROJECTS:
    # Create clean implementation
    $(basename "$0") user_management --type clean-ddd

    # Create anti-pattern version for comparison
    $(basename "$0") user_management_bad --type primitive-obsession

    # Now you have side-by-side comparison!

ARCHITECTURE EXPLORATION:
    # Event-driven with CQRS
    $(basename "$0") event_store --type event-driven

    # Microservice with API focus
    $(basename "$0") user_api --type microservice

    # Modular monolith
    $(basename "$0") ecommerce_platform --type monolith

DEVELOPMENT WORKFLOW:
    # Preview before creating
    $(basename "$0") prototype --dry-run --verbose

    # Create and immediately start developing
    $(basename "$0") quick_poc && cd examples/quick_poc && poetry shell

TEAM SCENARIOS:
    # Onboarding new developer
    $(basename "$0") onboarding_example --type clean-ddd

    # Architecture review session
    $(basename "$0") architecture_review --type clean-ddd
    $(basename "$0") architecture_review_antipattern --type primitive-obsession

    # Workshop materials
    $(basename "$0") workshop_part1 --type clean-ddd
    $(basename "$0") workshop_part2 --type event-driven

NAMING CONVENTIONS:
    Good names:
    ✅ taskflow, user_service, order_management
    ✅ ecommerce_api, inventory_system
    ✅ workshop_example, demo_project

    Avoid:
    ❌ test (too generic)
    ❌ 123example (starts with number)
    ❌ my-project-with-very-long-name (too verbose)

POST-CREATION WORKFLOW:
    1. cd examples/your_project
    2. poetry shell
    3. ./scripts/dev-setup.sh      # Complete environment setup
    4. poetry run pytest           # Verify everything works
    5. Start implementing domain layer

TROUBLESHOOTING:
    # Clean slate (remove and recreate)
    $(basename "$0") project_name --force

    # Debug mode
    $(basename "$0") project_name --verbose --dry-run

    # Check what types are available
    $(basename "$0") --list-types

INTEGRATION WITH BUILDING-BLOCKS:
    # All projects automatically get:
    # 📦 Local building-blocks dependency
    # 🔧 Shared quality tooling (black, ruff, mypy)
    # 🧪 Test infrastructure
    # 📚 Architecture documentation
    # 🚀 Development scripts

Need more help? Check ./docs/tooling/ or open an issue!
EOF
}

# List project types with detailed descriptions
show_project_types() {
    cat << EOF
📋 Available Project Types

clean-ddd (default):
    🎯 Purpose: Comprehensive clean architecture showcase
    📚 Demonstrates: DDD, Hexagonal Architecture, SOLID, Events
    🏗️ Includes: Full layer structure, CLI, API, tests
    👥 Best for: Learning, onboarding, reference implementation
    ⏱️ Setup time: ~2 minutes

primitive-obsession:
    🎯 Purpose: Anti-pattern demonstration
    📚 Demonstrates: What NOT to do, code smells, technical debt
    🏗️ Includes: Anemic models, scattered logic, primitive types
    👥 Best for: Training, code reviews, refactoring workshops
    ⏱️ Setup time: ~1 minute

event-driven:
    🎯 Purpose: Event-driven architecture with CQRS
    📚 Demonstrates: Events, CQRS, async processing, sagas
    🏗️ Includes: Event store, projections, handlers
    👥 Best for: Distributed systems, microservices training
    ⏱️ Setup time: ~3 minutes

microservice:
    🎯 Purpose: Single-purpose service with clean boundaries
    📚 Demonstrates: API design, service boundaries, resilience
    🏗️ Includes: FastAPI, health checks, monitoring
    👥 Best for: Microservices architecture, API design
    ⏱️ Setup time: ~2 minutes

monolith:
    🎯 Purpose: Modular monolith with bounded contexts
    📚 Demonstrates: Module boundaries, shared kernel, evolution
    🏗️ Includes: Multiple bounded contexts, module communication
    👥 Best for: Legacy modernization, monolith → microservices
    ⏱️ Setup time: ~4 minutes

RECOMMENDATION MATRIX:
    New to DDD/Clean Arch:     clean-ddd
    Teaching/Training:         clean-ddd + primitive-obsession
    Event-driven systems:      event-driven
    API development:           microservice
    Large system design:       monolith
EOF
}

# Add these functions to the argument parsing
parse_arguments() {
    if [[ $# -eq 0 ]]; then
        log_error "Project name is required. Use --help for usage information."
    fi

    while [[ $# -gt 0 ]]; do
        case $1 in
            -l|--list-types)
                show_project_types
                exit 0
                ;;
            -e|--examples)
                show_examples
                exit 0
                ;;
            # ... rest of existing parsing
        esac
    done
}
