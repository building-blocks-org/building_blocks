#!/bin/bash

# Building Blocks Example Project Creator - Enterprise Edition
# Robust error handling, comprehensive logging, bulletproof execution
# Author: Glauber Brennon <glauberbrennon@gmail.com>

set -euo pipefail  # Strict error handling: exit on error, undefined vars, pipe failures

# Script metadata
readonly SCRIPT_VERSION="1.2.0"
readonly SCRIPT_AUTHOR="Glauber Brennon"
readonly SCRIPT_EMAIL="glauberbrennon@gmail.com"
readonly SCRIPT_NAME="$(basename "$0")"

# Colors for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly PURPLE='\033[0;35m'
readonly CYAN='\033[0;36m'
readonly NC='\033[0m' # No Color

# Logging configuration
readonly LOG_FILE="/tmp/building-blocks-creator-$(date +%Y%m%d-%H%M%S).log"
VERBOSE=false
DEBUG=false

# Path resolution - CRITICAL for reliability
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
readonly EXAMPLES_DIR="$ROOT_DIR/examples"

# Verify critical paths exist
if [[ ! -d "$ROOT_DIR" ]] || [[ ! -f "$ROOT_DIR/pyproject.toml" ]]; then
    echo -e "${RED}[FATAL]${NC} Script path resolution failed!"
    echo "SCRIPT_DIR: $SCRIPT_DIR"
    echo "ROOT_DIR: $ROOT_DIR"
    echo "Current PWD: $(pwd)"
    exit 1
fi

# Enhanced logging system
log_to_file() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

log_info() {
    local msg="[INFO] $1"
    echo -e "${BLUE}${msg}${NC}"
    log_to_file "$msg"
}

log_success() {
    local msg="[SUCCESS] $1"
    echo -e "${GREEN}${msg}${NC}"
    log_to_file "$msg"
}

log_warning() {
    local msg="[WARNING] $1"
    echo -e "${YELLOW}${msg}${NC}"
    log_to_file "$msg"
}

log_error() {
    local msg="[ERROR] $1"
    echo -e "${RED}${msg}${NC}" >&2
    log_to_file "$msg"
}

log_fatal() {
    local msg="[FATAL] $1"
    echo -e "${RED}${msg}${NC}" >&2
    log_to_file "$msg"
    echo ""
    echo "💻 Debug information:"
    echo "  Script: $SCRIPT_NAME"
    echo "  Version: $SCRIPT_VERSION"
    echo "  PWD: $(pwd)"
    echo "  User: $(whoami)"
    echo "  Log: $LOG_FILE"
    echo ""
    echo "🔧 Troubleshooting:"
    echo "  1. Check permissions: ls -la $ROOT_DIR"
    echo "  2. Verify Poetry: poetry --version"
    echo "  3. Check log: cat $LOG_FILE"
    exit 1
}

log_debug() {
    if [[ "$DEBUG" == true ]]; then
        local msg="[DEBUG] $1"
        echo -e "${PURPLE}${msg}${NC}"
        log_to_file "$msg"
    fi
}

log_step() {
    local msg="[STEP] $1"
    echo -e "${CYAN}${msg}${NC}"
    log_to_file "$msg"
}

# Project configuration
PROJECT_NAME=""
PROJECT_TYPE="clean-ddd"
FORCE_OVERWRITE=false
DRY_RUN=false

# Project type definitions with validation
declare -A PROJECT_TYPES=(
    ["clean-ddd"]="Clean Architecture with DDD"
    ["primitive-obsession"]="Anti-pattern example showing primitive obsession"
    ["event-driven"]="Event-driven architecture example"
    ["microservice"]="Microservice with clean architecture"
    ["monolith"]="Modular monolith with DDD"
)

# Validation functions
validate_project_name() {
    local name="$1"

    if [[ -z "$name" ]]; then
        log_fatal "Project name cannot be empty"
    fi

    if [[ ! "$name" =~ ^[a-zA-Z][a-zA-Z0-9_-]*$ ]]; then
        log_fatal "Invalid project name: '$name'. Must start with letter and contain only letters, numbers, underscores, and hyphens."
    fi

    if [[ ${#name} -gt 50 ]]; then
        log_fatal "Project name too long: '$name'. Maximum 50 characters."
    fi

    log_debug "Project name validation passed: $name"
}

validate_project_type() {
    local type="$1"

    if [[ ! "${PROJECT_TYPES[$type]+_}" ]]; then
        log_error "Invalid project type: '$type'"
        echo ""
        echo "Available types:"
        for t in "${!PROJECT_TYPES[@]}"; do
            printf "  %-20s %s\n" "$t" "${PROJECT_TYPES[$t]}"
        done
        exit 1
    fi

    log_debug "Project type validation passed: $type"
}

validate_environment() {
    log_step "Environment Validation"

    # Check Poetry
    if ! command -v poetry &> /dev/null; then
        log_fatal "Poetry not found. Install from https://python-poetry.org/docs/#installation"
    fi
    local poetry_version
    poetry_version=$(poetry --version 2>&1 || echo "unknown")
    log_debug "Poetry version: $poetry_version"

    # Check Python
    if ! command -v python3 &> /dev/null; then
        log_fatal "Python 3 not found"
    fi
    local python_version
    python_version=$(python3 --version 2>&1)
    log_debug "Python version: $python_version"

    # Verify building-blocks structure
    if [[ ! -f "$ROOT_DIR/src/building_blocks/__init__.py" ]]; then
        log_fatal "building-blocks library structure not found at: $ROOT_DIR/src/building_blocks/"
    fi

    # Check write permissions
    if [[ ! -w "$ROOT_DIR" ]]; then
        log_fatal "No write permission to repository root: $ROOT_DIR"
    fi

    log_success "Environment validation passed"
}

check_existing_project() {
    local project_dir="$EXAMPLES_DIR/$PROJECT_NAME"

    if [[ -d "$project_dir" ]]; then
        if [[ "$FORCE_OVERWRITE" != true ]]; then
            log_error "Project already exists: $project_dir"
            echo ""
            echo "Options:"
            echo "  1. Use --force to overwrite"
            echo "  2. Choose a different name"
            echo "  3. Remove manually: rm -rf $project_dir"
            exit 1
        else
            log_warning "Will overwrite existing project: $project_dir"
        fi
    fi
}

# Enhanced argument parsing with better error messages
show_help() {
    cat << EOF
🚀 Building Blocks Example Project Creator v${SCRIPT_VERSION}

DESCRIPTION:
    Creates fully-structured example projects showcasing the building-blocks library
    with different architectural patterns and complexity levels.

USAGE:
    $SCRIPT_NAME <project-name> [options]

ARGUMENTS:
    project-name    Name of the project to create (required)
                   Must start with letter, contain only letters, numbers, _, -

OPTIONS:
    -t, --type TYPE         Project type (default: clean-ddd)
    -f, --force            Force overwrite if project exists
    -v, --verbose          Enable verbose output
    -d, --debug            Enable debug output
    --dry-run              Show what would be created without creating
    -l, --list-types       List all available project types
    -h, --help             Show this help message

PROJECT TYPES:
EOF

    for type in "${!PROJECT_TYPES[@]}"; do
        printf "    %-20s %s\n" "$type" "${PROJECT_TYPES[$type]}"
    done

    cat << EOF

EXAMPLES:
    # Create a clean DDD example
    $SCRIPT_NAME taskflow

    # Create anti-pattern example
    $SCRIPT_NAME taskflow_bad --type primitive-obsession

    # Debug mode
    $SCRIPT_NAME test_project --debug --dry-run

TROUBLESHOOTING:
    # Enable debug logging
    $SCRIPT_NAME project --debug --verbose

    # Check log file
    cat $LOG_FILE

AUTHOR:
    $SCRIPT_AUTHOR <$SCRIPT_EMAIL>
EOF
}

parse_arguments() {
    if [[ $# -eq 0 ]]; then
        log_error "Project name is required"
        echo ""
        show_help
        exit 1
    fi

    while [[ $# -gt 0 ]]; do
        case $1 in
            -t|--type)
                if [[ -z "${2:-}" ]]; then
                    log_fatal "Project type argument missing"
                fi
                PROJECT_TYPE="$2"
                shift 2
                ;;
            -f|--force)
                FORCE_OVERWRITE=true
                shift
                ;;
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            -d|--debug)
                DEBUG=true
                VERBOSE=true
                set -x  # Enable bash debugging
                shift
                ;;
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            -l|--list-types)
                echo "Available project types:"
                for type in "${!PROJECT_TYPES[@]}"; do
                    printf "  %-20s %s\n" "$type" "${PROJECT_TYPES[$type]}"
                done
                exit 0
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            -*)
                log_fatal "Unknown option: $1. Use --help for usage information."
                ;;
            *)
                if [[ -z "$PROJECT_NAME" ]]; then
                    PROJECT_NAME="$1"
                else
                    log_fatal "Multiple project names provided: '$PROJECT_NAME' and '$1'"
                fi
                shift
                ;;
        esac
    done

    # Validate required arguments
    if [[ -z "$PROJECT_NAME" ]]; then
        log_fatal "Project name is required. Use --help for usage information."
    fi

    log_debug "Arguments parsed successfully"
    log_debug "PROJECT_NAME: $PROJECT_NAME"
    log_debug "PROJECT_TYPE: $PROJECT_TYPE"
    log_debug "FORCE_OVERWRITE: $FORCE_OVERWRITE"
    log_debug "DRY_RUN: $DRY_RUN"
}

show_configuration() {
    log_step "Configuration Summary"
    echo "  Project Name: $PROJECT_NAME"
    echo "  Project Type: $PROJECT_TYPE (${PROJECT_TYPES[$PROJECT_TYPE]})"
    echo "  Target Directory: $EXAMPLES_DIR/$PROJECT_NAME"
    echo "  Force Overwrite: $FORCE_OVERWRITE"
    echo "  Dry Run: $DRY_RUN"
    echo "  Debug Mode: $DEBUG"
    echo "  Log File: $LOG_FILE"
    echo ""
}

# Create directory structure with detailed error handling
create_directory_structure() {
    local project_dir="$EXAMPLES_DIR/$PROJECT_NAME"

    log_step "Creating Directory Structure"
    log_debug "Target directory: $project_dir"

    if [[ "$DRY_RUN" == true ]]; then
        log_info "DRY RUN: Would create directory structure at $project_dir"
        return 0
    fi

    # Ensure examples directory exists
    if [[ ! -d "$EXAMPLES_DIR" ]]; then
        log_debug "Creating examples directory: $EXAMPLES_DIR"
        mkdir -p "$EXAMPLES_DIR" || log_fatal "Failed to create examples directory: $EXAMPLES_DIR"
    fi

    # Remove existing if force overwrite
    if [[ -d "$project_dir" ]] && [[ "$FORCE_OVERWRITE" == true ]]; then
        log_warning "Removing existing project directory: $project_dir"
        rm -rf "$project_dir" || log_fatal "Failed to remove existing directory: $project_dir"
    fi

    # Create main project directory
    log_debug "Creating project directory: $project_dir"
    mkdir -p "$project_dir" || log_fatal "Failed to create project directory: $project_dir"

    # Create complete directory structure
    local dirs=(
        "src"
        "tests"
        "docs"
        "scripts"
        "src/$PROJECT_NAME"
        "src/$PROJECT_NAME/domain"
        "src/$PROJECT_NAME/domain/entities"
        "src/$PROJECT_NAME/domain/value_objects"
        "src/$PROJECT_NAME/domain/messages"
        "src/$PROJECT_NAME/domain/messages/events"
        "src/$PROJECT_NAME/domain/messages/commands"
        "src/$PROJECT_NAME/domain/ports"
        "src/$PROJECT_NAME/domain/ports/inbound"
        "src/$PROJECT_NAME/domain/ports/outbound"
        "src/$PROJECT_NAME/application"
        "src/$PROJECT_NAME/application/ports"
        "src/$PROJECT_NAME/application/ports/inbound"
        "src/$PROJECT_NAME/application/ports/outbound"
        "src/$PROJECT_NAME/application/services"
        "src/$PROJECT_NAME/application/requests"
        "src/$PROJECT_NAME/application/responses"
        "src/$PROJECT_NAME/infrastructure"
        "src/$PROJECT_NAME/infrastructure/persistence"
        "src/$PROJECT_NAME/infrastructure/messaging"
        "src/$PROJECT_NAME/infrastructure/services"
        "src/$PROJECT_NAME/presentation"
        "tests/unit"
        "tests/integration"
        "tests/e2e"
        "tests/unit/domain"
        "tests/unit/application"
        "tests/unit/infrastructure"
        "tests/unit/presentation"
    )

    # Add project-type specific directories
    case "$PROJECT_TYPE" in
        "clean-ddd"|"event-driven"|"monolith")
            dirs+=(
                "src/$PROJECT_NAME/domain/services"
                "src/$PROJECT_NAME/application/handlers"
                "src/$PROJECT_NAME/presentation/cli"
                "src/$PROJECT_NAME/presentation/api"
            )
            ;;
        "primitive-obsession")
            dirs+=(
                "src/$PROJECT_NAME/presentation/cli"
            )
            ;;
        "microservice")
            dirs+=(
                "src/$PROJECT_NAME/domain/services"
                "src/$PROJECT_NAME/application/handlers"
                "src/$PROJECT_NAME/presentation/api"
            )
            ;;
    esac

    # Create all directories
    for dir in "${dirs[@]}"; do
        local full_path="$project_dir/$dir"
        log_debug "Creating directory: $full_path"
        mkdir -p "$full_path" || log_fatal "Failed to create directory: $full_path"
    done

    # Verify creation
    if [[ ! -d "$project_dir/src/$PROJECT_NAME" ]]; then
        log_fatal "Directory creation verification failed: $project_dir/src/$PROJECT_NAME"
    fi

    log_success "Directory structure created successfully"
}

# Create __init__.py files with error checking
create_init_files() {
    local project_dir="$EXAMPLES_DIR/$PROJECT_NAME"

    log_step "Creating Package Files"

    if [[ "$DRY_RUN" == true ]]; then
        log_info "DRY RUN: Would create __init__.py files"
        return 0
    fi

    # Create __init__.py files for all Python packages
    log_debug "Creating __init__.py files in src/"
    while IFS= read -r -d '' dir; do
        local init_file="$dir/__init__.py"
        log_debug "Creating: $init_file"
        touch "$init_file" || log_fatal "Failed to create: $init_file"
    done < <(find "$project_dir/src" -type d -print0)

    log_debug "Creating __init__.py files in tests/"
    while IFS= read -r -d '' dir; do
        local init_file="$dir/__init__.py"
        log_debug "Creating: $init_file"
        touch "$init_file" || log_fatal "Failed to create: $init_file"
    done < <(find "$project_dir/tests" -type d -print0)

    # Verify critical files exist
    local critical_files=(
        "$project_dir/src/$PROJECT_NAME/__init__.py"
        "$project_dir/src/$PROJECT_NAME/domain/__init__.py"
        "$project_dir/tests/__init__.py"
    )

    for file in "${critical_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            log_fatal "Critical file missing: $file"
        fi
    done

    log_success "Package files created successfully"
}

# Enhanced pyproject.toml creation with validation
create_pyproject_toml() {
    local project_dir="$EXAMPLES_DIR/$PROJECT_NAME"
    local pyproject_file="$project_dir/pyproject.toml"

    log_step "Creating pyproject.toml"
    log_debug "Target file: $pyproject_file"

    if [[ "$DRY_RUN" == true ]]; then
        log_info "DRY RUN: Would create pyproject.toml"
        return 0
    fi

    # Get project-specific configuration
    get_project_config "$PROJECT_TYPE"

    # Build keywords string
    local keywords_str=""
    for keyword in "${PROJECT_KEYWORDS[@]}"; do
        keywords_str+="    \"$keyword\",\n"
    done
    keywords_str=${keywords_str%,\\n}  # Remove trailing comma and newline

    # Create pyproject.toml with error handling
    cat > "$pyproject_file" << EOF || log_fatal "Failed to create pyproject.toml"
[tool.poetry]
name = "$PROJECT_NAME"
version = "0.1.0"
description = "$PROJECT_DESCRIPTION"
authors = ["$SCRIPT_AUTHOR <$SCRIPT_EMAIL>"]
license = "MIT"
readme = "README.md"
packages = [{include = "$PROJECT_NAME", from = "src"}]
keywords = [
$(echo -e "$keywords_str")
]

[tool.poetry.dependencies]
python = "^3.9"
building-blocks = {path = "../../", develop = true}
EOF

    # Add conditional dependencies based on project type
    if [[ "$INCLUDE_CLI" == true ]]; then
        cat >> "$pyproject_file" << EOF || log_fatal "Failed to add CLI dependencies"
typer = "^0.9.0"
rich = "^13.0.0"
EOF
    fi

    if [[ "$INCLUDE_API" == true ]]; then
        cat >> "$pyproject_file" << EOF || log_fatal "Failed to add API dependencies"
fastapi = "^0.104.0"
uvicorn = "^0.24.0"
EOF
    fi

    # Add scripts section if CLI is included
    if [[ "$INCLUDE_CLI" == true ]]; then
        cat >> "$pyproject_file" << EOF || log_fatal "Failed to add scripts section"

[tool.poetry.scripts]
$PROJECT_NAME = "$PROJECT_NAME.presentation.cli.main:app"
EOF
    fi

    # Add build system
    cat >> "$pyproject_file" << EOF || log_fatal "Failed to add build system"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

# Tool configurations inherited from root pyproject.toml
# Run quality checks from repository root to use shared configuration
EOF

    # Verify file was created and has content
    if [[ ! -f "$pyproject_file" ]]; then
        log_fatal "pyproject.toml was not created: $pyproject_file"
    fi

    if [[ ! -s "$pyproject_file" ]]; then
        log_fatal "pyproject.toml is empty: $pyproject_file"
    fi

    log_debug "pyproject.toml size: $(wc -l < "$pyproject_file") lines"
    log_success "pyproject.toml created successfully"
}

# Get project-specific configuration with enhanced validation
get_project_config() {
    local type="$1"

    log_debug "Loading configuration for project type: $type"

    case "$type" in
        "clean-ddd")
            PROJECT_DESCRIPTION="Clean Architecture with DDD Example showcasing building-blocks library"
            PROJECT_KEYWORDS=(
                "clean architecture example"
                "hexagonal architecture example"
                "domain-driven design example"
                "ddd example"
                "building-blocks showcase"
                "software architecture"
                "clean code example"
            )
            INCLUDE_CLI=true
            INCLUDE_API=true
            INCLUDE_DOMAIN_SERVICES=true
            INCLUDE_EVENT_HANDLERS=true
            ;;
        "primitive-obsession")
            PROJECT_DESCRIPTION="Anti-pattern example demonstrating primitive obsession and anemic domain model"
            PROJECT_KEYWORDS=(
                "anti-pattern example"
                "primitive obsession"
                "anemic domain model"
                "code smell example"
                "what not to do"
                "refactoring example"
            )
            INCLUDE_CLI=true
            INCLUDE_API=false
            INCLUDE_DOMAIN_SERVICES=false
            INCLUDE_EVENT_HANDLERS=false
            ;;
        "event-driven")
            PROJECT_DESCRIPTION="Event-driven architecture example with CQRS and Event Sourcing"
            PROJECT_KEYWORDS=(
                "event-driven architecture"
                "cqrs example"
                "event sourcing"
                "building-blocks showcase"
                "microservices"
                "distributed systems"
            )
            INCLUDE_CLI=true
            INCLUDE_API=true
            INCLUDE_DOMAIN_SERVICES=true
            INCLUDE_EVENT_HANDLERS=true
            ;;
        "microservice")
            PROJECT_DESCRIPTION="Microservice implementation with clean architecture principles"
            PROJECT_KEYWORDS=(
                "microservice example"
                "clean architecture"
                "building-blocks showcase"
                "api design"
                "service architecture"
            )
            INCLUDE_CLI=false
            INCLUDE_API=true
            INCLUDE_DOMAIN_SERVICES=true
            INCLUDE_EVENT_HANDLERS=true
            ;;
        "monolith")
            PROJECT_DESCRIPTION="Modular monolith with DDD bounded contexts"
            PROJECT_KEYWORDS=(
                "modular monolith"
                "bounded contexts"
                "ddd example"
                "building-blocks showcase"
                "monolithic architecture"
            )
            INCLUDE_CLI=true
            INCLUDE_API=true
            INCLUDE_DOMAIN_SERVICES=true
            INCLUDE_EVENT_HANDLERS=true
            ;;
        *)
            log_fatal "Unknown project type in get_project_config: $type"
            ;;
    esac

    log_debug "Project configuration loaded successfully"
}

# Create development scripts with enhanced error handling
create_dev_scripts() {
    local project_dir="$EXAMPLES_DIR/$PROJECT_NAME"
    local scripts_dir="$project_dir/scripts"

    log_step "Creating Development Scripts"

    if [[ "$DRY_RUN" == true ]]; then
        log_info "DRY RUN: Would create development scripts"
        return 0
    fi

    # Ensure scripts directory exists
    mkdir -p "$scripts_dir" || log_fatal "Failed to create scripts directory: $scripts_dir"

    # Quality check script
    local quality_script="$scripts_dir/quality-check.sh"
    cat > "$quality_script" << 'EOF' || log_fatal "Failed to create quality-check.sh"
#!/bin/bash
# Quality check for project
# Run from project directory

set -e

PROJECT_NAME=$(basename "$(pwd)")
echo "🔍 Running quality checks for $PROJECT_NAME..."

# Run from repository root to use shared configuration
cd ../../

echo "  → Black formatting check..."
poetry run black --check "examples/$PROJECT_NAME/src/" "examples/$PROJECT_NAME/tests/"

echo "  → Ruff linting..."
poetry run ruff check "examples/$PROJECT_NAME/src/" "examples/$PROJECT_NAME/tests/"

echo "  → MyPy type checking..."
poetry run mypy "examples/$PROJECT_NAME/src/"

echo "  → Bandit security check..."
poetry run bandit -r "examples/$PROJECT_NAME/src/"

echo "✅ All quality checks passed!"
EOF

    # Test script
    local test_script="$scripts_dir/test.sh"
    cat > "$test_script" << 'EOF' || log_fatal "Failed to create test.sh"
#!/bin/bash
# Test script for project
# Run from project directory

set -e

PROJECT_NAME=$(basename "$(pwd)")
echo "🧪 Running tests for $PROJECT_NAME..."

poetry run pytest tests/ -v --cov="src/$PROJECT_NAME" --cov-report=term-missing

echo "✅ All tests passed!"
EOF

    # Development setup script
    local setup_script="$scripts_dir/dev-setup.sh"
    cat > "$setup_script" << 'EOF' || log_fatal "Failed to create dev-setup.sh"
#!/bin/bash
# Development setup for project

set -e

PROJECT_NAME=$(basename "$(pwd)")
echo "🔧 Setting up development environment for $PROJECT_NAME..."

# Install dependencies
echo "Installing dependencies..."
poetry install

# Verify setup
echo "Verifying setup..."
poetry run python -c "from building_blocks.domain import Entity; print('✅ Dependencies verified')"

# Run initial tests
echo "Running initial tests..."
poetry run pytest tests/ -v

echo "✅ Development environment ready!"
echo ""
echo "Next steps:"
echo "  1. Implement domain layer"
echo "  2. Add application services"
echo "  3. Create infrastructure adapters"
echo "  4. Build presentation layer"
EOF

    # Make scripts executable
    chmod +x "$scripts_dir"/*.sh || log_warning "Failed to make scripts executable"

    # Verify scripts were created
    local scripts=("quality-check.sh" "test.sh" "dev-setup.sh")
    for script in "${scripts[@]}"; do
        local script_path="$scripts_dir/$script"
        if [[ ! -f "$script_path" ]]; then
            log_fatal "Script not created: $script_path"
        fi
        log_debug "Created script: $script_path"
    done

    log_success "Development scripts created successfully"
}

# Create main package __init__.py with enhanced content
create_main_init() {
    local project_dir="$EXAMPLES_DIR/$PROJECT_NAME"
    local init_file="$project_dir/src/$PROJECT_NAME/__init__.py"

    log_step "Creating Main Package"

    if [[ "$DRY_RUN" == true ]]; then
        log_info "DRY RUN: Would create main package __init__.py"
        return 0
    fi

    cat > "$init_file" << EOF || log_fatal "Failed to create main __init__.py"
"""
$PROJECT_NAME - $PROJECT_DESCRIPTION

This project demonstrates the practical application of the building-blocks
library in a real-world scenario.

Architecture Layers:
- Domain: Pure business logic and rules
- Application: Use cases and orchestration
- Infrastructure: External system adapters
- Presentation: User interfaces

Generated by: Building Blocks Project Creator v$SCRIPT_VERSION
Author: $SCRIPT_AUTHOR
Created: $(date -u '+%Y-%m-%d %H:%M:%S UTC')
"""

__version__ = "0.1.0"
__author__ = "$SCRIPT_AUTHOR"
__email__ = "$SCRIPT_EMAIL"

# Package exports will be added as components are implemented
__all__ = []
EOF

    # Verify file was created
    if [[ ! -f "$init_file" ]]; then
        log_fatal "Main __init__.py was not created: $init_file"
    fi

    log_debug "Main __init__.py size: $(wc -l < "$init_file") lines"
    log_success "Main package created successfully"
}

# Create comprehensive README with project-specific content
create_readme() {
    local project_dir="$EXAMPLES_DIR/$PROJECT_NAME"
    local readme_file="$project_dir/README.md"

    log_step "Creating README.md"

    if [[ "$DRY_RUN" == true ]]; then
        log_info "DRY RUN: Would create README.md"
        return 0
    fi

    cat > "$readme_file" << EOF || log_fatal "Failed to create README.md"
# $PROJECT_NAME

> $PROJECT_DESCRIPTION

## 🎯 Purpose

This example demonstrates:

EOF

    # Add project-specific purpose based on type
    case "$PROJECT_TYPE" in
        "clean-ddd")
            cat >> "$readme_file" << EOF
- **Clean Architecture** (Hexagonal Architecture)
- **Domain-Driven Design (DDD)**
- **SOLID Principles**
- **Event-Driven Architecture**
- **CQRS Pattern**
- **Building Blocks Library Usage**
EOF
            ;;
        "primitive-obsession")
            cat >> "$readme_file" << EOF
- **Primitive Obsession Anti-Pattern**
- **Anemic Domain Model Problems**
- **Why Value Objects Matter**
- **Scattered Business Logic Issues**
- **Comparison with Clean Implementation**

⚠️ **WARNING: This is an example of what NOT to do!**
EOF
            ;;
        "event-driven")
            cat >> "$readme_file" << EOF
- **Event-Driven Architecture**
- **CQRS (Command Query Responsibility Segregation)**
- **Event Sourcing Patterns**
- **Asynchronous Processing**
- **Event Bus Implementation**
EOF
            ;;
        "microservice")
            cat >> "$readme_file" << EOF
- **Microservice Architecture**
- **API Design Best Practices**
- **Service Boundaries**
- **Inter-Service Communication**
- **Resilience Patterns**
EOF
            ;;
        "monolith")
            cat >> "$readme_file" << EOF
- **Modular Monolith Architecture**
- **Bounded Context Implementation**
- **Module Communication**
- **Shared Kernel Patterns**
- **Evolution to Microservices**
EOF
            ;;
    esac

    cat >> "$readme_file" << EOF

## 🏗️ Architecture

\`\`\`
src/$PROJECT_NAME/
├── domain/           # Pure business logic
│   ├── entities/     # Aggregates and entities
│   ├── value_objects/ # Immutable value types
│   ├── messages/     # Domain events and commands
EOF

    if [[ "$INCLUDE_DOMAIN_SERVICES" == true ]]; then
        cat >> "$readme_file" << EOF
│   ├── services/     # Domain services
EOF
    fi

    cat >> "$readme_file" << EOF
│   └── ports/        # Domain contracts
├── application/      # Use cases and orchestration
│   ├── services/     # Use case implementations
│   ├── ports/        # Application contracts
│   ├── requests/     # Input DTOs
EOF

    if [[ "$INCLUDE_EVENT_HANDLERS" == true ]]; then
        cat >> "$readme_file" << EOF
│   ├── handlers/     # Event and command handlers
EOF
    fi

    cat >> "$readme_file" << EOF
│   └── responses/    # Output DTOs
├── infrastructure/   # External concerns
│   ├── persistence/  # Database adapters
│   ├── messaging/    # Event bus implementations
│   └── services/     # External service adapters
└── presentation/     # User interfaces
EOF

    if [[ "$INCLUDE_API" == true ]]; then
        cat >> "$readme_file" << EOF
    ├── api/          # REST API
EOF
    fi

    if [[ "$INCLUDE_CLI" == true ]]; then
        cat >> "$readme_file" << EOF
    └── cli/          # Command line interface
EOF
    fi

    cat >> "$readme_file" << EOF
\`\`\`

## 🚀 Getting Started

\`\`\`bash
# Install dependencies
poetry install

EOF

    if [[ "$INCLUDE_CLI" == true ]]; then
        cat >> "$readme_file" << EOF
# Run CLI
poetry run $PROJECT_NAME --help

EOF
    fi

    if [[ "$INCLUDE_API" == true ]]; then
        cat >> "$readme_file" << EOF
# Run API server
poetry run uvicorn $PROJECT_NAME.presentation.api.main:app --reload

EOF
    fi

    cat >> "$readme_file" << EOF
# Run tests
poetry run pytest

# Quality checks (from repository root)
cd ../../
poetry run black --check examples/$PROJECT_NAME/
poetry run ruff check examples/$PROJECT_NAME/
poetry run mypy examples/$PROJECT_NAME/src/
\`\`\`

## 📚 Learning Path

1. **Domain Layer** - Start with entities and value objects
2. **Application Layer** - Understand use cases and ports
3. **Infrastructure** - See how external concerns are handled
4. **Presentation** - Learn about clean interfaces

## 🔗 Related

- Main library: \`../../src/building_blocks/\`
- Other examples: \`../\`

## 📖 Documentation

Generated on: $(date -u '+%Y-%m-%d %H:%M:%S UTC')
Created by: Building Blocks Example Creator v$SCRIPT_VERSION
Author: $SCRIPT_AUTHOR <$SCRIPT_EMAIL>
EOF

    # Verify README was created
    if [[ ! -f "$readme_file" ]]; then
        log_fatal "README.md was not created: $readme_file"
    fi

    log_debug "README.md size: $(wc -l < "$readme_file") lines"
    log_success "README.md created successfully"
}

# Create basic test files with validation
create_basic_tests() {
    local project_dir="$EXAMPLES_DIR/$PROJECT_NAME"
    local test_file="$project_dir/tests/test_setup.py"

    log_step "Creating Basic Tests"

    if [[ "$DRY_RUN" == true ]]; then
        log_info "DRY RUN: Would create basic tests"
        return 0
    fi

    cat > "$test_file" << EOF || log_fatal "Failed to create test_setup.py"
"""Test that the $PROJECT_NAME example is properly set up."""

import pytest


def test_building_blocks_import():
    """Test that we can import building-blocks components."""
    from building_blocks.domain import Entity, ValueObject, Event

    assert Entity is not None
    assert ValueObject is not None
    assert Event is not None


def test_project_import():
    """Test that we can import $PROJECT_NAME."""
    import $PROJECT_NAME

    assert $PROJECT_NAME.__version__ == "0.1.0"
    assert $PROJECT_NAME.__author__ == "$SCRIPT_AUTHOR"


class TestProjectStructure:
    """Test that the project structure is correct."""

    def test_can_import_domain_layer(self):
        """Test domain layer package structure."""
        import $PROJECT_NAME.domain
        import $PROJECT_NAME.domain.entities
        import $PROJECT_NAME.domain.value_objects
        import $PROJECT_NAME.domain.messages
        import $PROJECT_NAME.domain.ports
EOF

    if [[ "$INCLUDE_DOMAIN_SERVICES" == true ]]; then
        cat >> "$test_file" << EOF
        import $PROJECT_NAME.domain.services
EOF
    fi

    cat >> "$test_file" << EOF

    def test_can_import_application_layer(self):
        """Test application layer package structure."""
        import $PROJECT_NAME.application
        import $PROJECT_NAME.application.ports
        import $PROJECT_NAME.application.services
        import $PROJECT_NAME.application.requests
        import $PROJECT_NAME.application.responses
EOF

    if [[ "$INCLUDE_EVENT_HANDLERS" == true ]]; then
        cat >> "$test_file" << EOF
        import $PROJECT_NAME.application.handlers
EOF
    fi

    cat >> "$test_file" << EOF

    def test_can_import_infrastructure_layer(self):
        """Test infrastructure layer package structure."""
        import $PROJECT_NAME.infrastructure
        import $PROJECT_NAME.infrastructure.persistence
        import $PROJECT_NAME.infrastructure.messaging
        import $PROJECT_NAME.infrastructure.services

    def test_can_import_presentation_layer(self):
        """Test presentation layer package structure."""
        import $PROJECT_NAME.presentation
EOF

    if [[ "$INCLUDE_API" == true ]]; then
        cat >> "$test_file" << EOF
        import $PROJECT_NAME.presentation.api
EOF
    fi

    if [[ "$INCLUDE_CLI" == true ]]; then
        cat >> "$test_file" << EOF
        import $PROJECT_NAME.presentation.cli
EOF
    fi

    # Verify test file was created
    if [[ ! -f "$test_file" ]]; then
        log_fatal "test_setup.py was not created: $test_file"
    fi

    log_debug "test_setup.py size: $(wc -l < "$test_file") lines"
    log_success "Basic tests created successfully"
}

# Setup Poetry environment with comprehensive validation
setup_poetry_environment() {
    local project_dir="$EXAMPLES_DIR/$PROJECT_NAME"

    log_step "Setting up Poetry Environment"

    if [[ "$DRY_RUN" == true ]]; then
        log_info "DRY RUN: Would set up Poetry environment"
        return 0
    fi

    # Change to project directory
    log_debug "Changing to project directory: $project_dir"
    cd "$project_dir" || log_fatal "Failed to change to project directory: $project_dir"

    # Install dependencies with timeout
    log_info "Installing dependencies (this may take a few minutes)..."

    # Use timeout to prevent hanging
    if command -v timeout &> /dev/null; then
        timeout 300 poetry install || log_fatal "Poetry install failed or timed out after 5 minutes"
    else
        poetry install || log_fatal "Poetry install failed"
    fi

    # Verify building-blocks import
    log_info "Verifying building-blocks import..."
    poetry run python -c "
from building_blocks.domain import Entity, ValueObject, Event
print('✅ building-blocks imported successfully')
print(f'  Entity: {Entity}')
print(f'  ValueObject: {ValueObject}')
print(f'  Event: {Event}')
" || log_fatal "building-blocks import verification failed"

    # Run basic setup tests
    log_info "Running setup verification tests..."
    poetry run pytest tests/test_setup.py -v || log_fatal "Setup tests failed"

    # Return to original directory
    cd - > /dev/null || log_warning "Failed to return to original directory"

    log_success "Poetry environment configured successfully"
}

# Enhanced summary with next steps
show_summary() {
    local project_dir="$EXAMPLES_DIR/$PROJECT_NAME"

    echo ""
    echo "🎉 Project '$PROJECT_NAME' created successfully!"
    echo "=================================================="
    echo ""
    echo "📁 Location: $project_dir"
    echo "📋 Type: $PROJECT_TYPE (${PROJECT_TYPES[$PROJECT_TYPE]})"
    echo "📊 Files created: $(find "$project_dir" -type f | wc -l)"
    echo "📂 Directories created: $(find "$project_dir" -type d | wc -l)"
    echo ""
    echo "🚀 Next steps:"
    echo "   cd examples/$PROJECT_NAME"
    echo "   poetry shell"
    echo "   poetry run pytest tests/ -v"
    echo ""
    echo "🛠️ Development workflow:"
    echo "   ./scripts/dev-setup.sh      # Complete environment setup"
    echo "   ./scripts/test.sh           # Run tests"
    echo "   ./scripts/quality-check.sh  # Code quality checks"
    echo ""
    echo "📚 Implementation order:"
    echo "   1. Domain layer (entities, value objects, events)"
    echo "   2. Application layer (use cases, ports)"
    echo "   3. Infrastructure layer (persistence, messaging)"

    if [[ "$INCLUDE_CLI" == true ]] || [[ "$INCLUDE_API" == true ]]; then
        echo "   4. Presentation layer"
        if [[ "$INCLUDE_CLI" == true ]]; then
            echo "      - CLI interface (Typer + Rich)"
        fi
        if [[ "$INCLUDE_API" == true ]]; then
            echo "      - REST API (FastAPI)"
        fi
    fi

    echo ""
    echo "🔗 Resources:"
    echo "   📖 Project docs: examples/$PROJECT_NAME/README.md"
    echo "   🏛️ Architecture: src/$PROJECT_NAME/ (clean layers)"
    echo "   🧪 Tests: tests/ (comprehensive test suite)"
    echo "   📝 Log file: $LOG_FILE"
    echo ""

    if [[ "$PROJECT_TYPE" == "primitive-obsession" ]]; then
        echo "⚠️  ANTI-PATTERN PROJECT:"
        echo "   This project shows what NOT to do!"
        echo "   Compare with a clean-ddd project to see the difference."
        echo ""
    fi
}

# Main execution function with comprehensive error handling
main() {
    # Initialize logging
    log_to_file "=== Building Blocks Project Creator v$SCRIPT_VERSION Started ==="
    log_to_file "Command: $0 $*"
    log_to_file "PWD: $(pwd)"
    log_to_file "User: $(whoami)"
    log_to_file "Date: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"

    echo "🚀 Building Blocks Example Project Creator v$SCRIPT_VERSION"
    echo "============================================================"
    echo ""

    # Parse and validate arguments
    parse_arguments "$@"
    validate_project_name "$PROJECT_NAME"
    validate_project_type "$PROJECT_TYPE"

    # Show configuration
    show_configuration

    # Environment validation
    validate_environment
    check_existing_project

    # Project creation pipeline
    get_project_config "$PROJECT_TYPE"
    create_directory_structure
    create_init_files
    create_pyproject_toml
    create_readme
    create_main_init
    create_dev_scripts
    create_basic_tests
    setup_poetry_environment

    # Success summary
    show_summary

    log_to_file "=== Project creation completed successfully ==="
}

# Trap errors and provide helpful debugging information
trap 'log_fatal "Script failed at line $LINENO. Check log: $LOG_FILE"' ERR

# Execute main function with all arguments
main "$@"
