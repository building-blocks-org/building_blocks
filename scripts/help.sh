#!/bin/bash

# Interactive Help System for Building Blocks - Enterprise Edition
# Comprehensive help with error diagnosis and troubleshooting

set -e

# Colors
readonly GREEN='\033[0;32m'
readonly BLUE='\033[0;34m'
readonly YELLOW='\033[1;33m'
readonly RED='\033[0;31m'
readonly NC='\033[0m'

# Get script directory for reliable path resolution
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Verify we're in the right place
if [[ ! -f "$ROOT_DIR/pyproject.toml" ]]; then
    echo -e "${RED}[ERROR]${NC} Not in building-blocks repository!"
    echo "Current directory: $(pwd)"
    echo "Expected to find: $ROOT_DIR/pyproject.toml"
    exit 1
fi

create_project_wizard() {
    echo -e "${BLUE}📋 Project Creation Wizard${NC}"
    echo "========================================="
    echo ""

    # Get project name with validation
    while true; do
        read -p "Project name (e.g., taskflow): " project_name
        if [[ -z "$project_name" ]]; then
            echo -e "${RED}❌ Project name required!${NC}"
            continue
        fi

        if [[ ! "$project_name" =~ ^[a-zA-Z][a-zA-Z0-9_-]*$ ]]; then
            echo -e "${RED}❌ Invalid name! Must start with letter, use only letters, numbers, _, -${NC}"
            continue
        fi

        break
    done

    # Get project type with descriptions
    echo ""
    echo "Available project types:"
    echo "1) clean-ddd (🎯 Best for learning - full clean architecture)"
    echo "2) primitive-obsession (⚠️ Anti-pattern example - what NOT to do)"
    echo "3) event-driven (🚀 CQRS + Event Sourcing - advanced patterns)"
    echo "4) microservice (🔌 API-focused service - production ready)"
    echo "5) monolith (🏗️ Modular monolith - large system design)"
    echo ""

    while true; do
        read -p "Choose type (1-5): " type_choice

        case $type_choice in
            1) project_type="clean-ddd"; break ;;
            2) project_type="primitive-obsession"; break ;;
            3) project_type="event-driven"; break ;;
            4) project_type="microservice"; break ;;
            5) project_type="monolith"; break ;;
            *) echo -e "${RED}❌ Invalid choice! Please enter 1-5.${NC}" ;;
        esac
    done

    # Show what will be created
    echo ""
    echo -e "${YELLOW}📋 Project Summary:${NC}"
    echo "  Name: $project_name"
    echo "  Type: $project_type"
    echo "  Location: $ROOT_DIR/examples/$project_name"

    # Additional info based on type
    case $project_type in
        "clean-ddd")
            echo "  Features: Full DDD, CLI, API, Events, Tests"
            echo "  Perfect for: Learning, reference, onboarding"
            ;;
        "primitive-obsession")
            echo "  Features: Anti-patterns, code smells, anemic model"
            echo "  Perfect for: Training, showing what NOT to do"
            ;;
        "event-driven")
            echo "  Features: CQRS, Event Sourcing, Async processing"
            echo "  Perfect for: Distributed systems, microservices"
            ;;
        "microservice")
            echo "  Features: FastAPI, health checks, monitoring"
            echo "  Perfect for: Production APIs, service architecture"
            ;;
        "monolith")
            echo "  Features: Bounded contexts, module communication"
            echo "  Perfect for: Large systems, legacy modernization"
            ;;
    esac

    echo ""
    echo "Estimated setup time: 2-3 minutes"
    echo ""

    # Confirm creation
    while true; do
        read -p "Proceed with creation? (y/N): " confirm
        case $confirm in
            [Yy]|[Yy][Ee][Ss])
                break
                ;;
            [Nn]|[Nn][Oo]|"")
                echo "Cancelled."
                return
                ;;
            *)
                echo "Please answer yes or no."
                ;;
        esac
    done

    # Create the project with enhanced error handling
    echo ""
    echo -e "${BLUE}🔧 Creating project...${NC}"

    local creation_script="$SCRIPT_DIR/create-example-project.sh"

    if [[ ! -f "$creation_script" ]]; then
        echo -e "${RED}❌ Creation script not found: $creation_script${NC}"
        return 1
    fi

    # Make sure script is executable
    chmod +x "$creation_script"

    # Run with verbose output
    if "$creation_script" "$project_name" --type "$project_type" --verbose; then
        echo ""
        echo -e "${GREEN}✅ Project created successfully!${NC}"
        echo ""
        echo "🚀 Quick start:"
        echo "  cd examples/$project_name"
        echo "  poetry shell"
        echo "  ./scripts/dev-setup.sh"
        echo ""
        echo "📚 Next steps:"
        echo "  1. Explore the generated code structure"
        echo "  2. Run the tests: poetry run pytest"
        echo "  3. Start implementing your domain logic"
        echo "  4. Check README.md for detailed guidance"
    else
        echo ""
        echo -e "${RED}❌ Project creation failed!${NC}"
        echo ""
        echo "🔧 Troubleshooting:"
        echo "  1. Check Poetry is installed: poetry --version"
        echo "  2. Verify permissions: ls -la $ROOT_DIR"
        echo "  3. Try with debug: $creation_script $project_name --type $project_type --debug"
        echo "  4. Check logs for detailed error information"
    fi
}

# Add other functions (show_troubleshooting, show_workflow, etc.) here...
# ... (keeping the rest of the help.sh as before but with enhanced error handling)

show_main_menu() {
    cat << EOF
🚀 Building Blocks Help System - Enhanced Edition

What would you like to do?

1) Create a new example project (🎯 Most popular)
2) Learn about project types
3) See usage examples
4) Troubleshoot issues
5) View development workflow
6) Check quality standards
7) Browse documentation
8) Diagnose environment

q) Quit

EOF
    read -p "Enter your choice (1-8, q): " choice

    case $choice in
        1) create_project_wizard ;;
        2) "$SCRIPT_DIR/create-example-project.sh" --list-types ;;
        3) "$SCRIPT_DIR/create-example-project.sh" --examples ;;
        4) show_troubleshooting ;;
        5) show_workflow ;;
        6) show_quality ;;
        7) show_docs ;;
        8) diagnose_environment ;;
        q|Q) exit 0 ;;
        *)
            echo -e "${RED}❌ Invalid choice. Please try again.${NC}"
            echo ""
            show_main_menu
            ;;
    esac
}

# New diagnostic function
diagnose_environment() {
    echo -e "${BLUE}🔍 Environment Diagnosis${NC}"
    echo "=========================="
    echo ""

    # Check Poetry
    if command -v poetry &> /dev/null; then
        local poetry_version
        poetry_version=$(poetry --version 2>&1)
        echo -e "${GREEN}✅ Poetry:${NC} $poetry_version"
    else
        echo -e "${RED}❌ Poetry:${NC} Not installed"
        echo "   Install from: https://python-poetry.org/docs/#installation"
    fi

    # Check Python
    if command -v python3 &> /dev/null; then
        local python_version
        python_version=$(python3 --version 2>&1)
        echo -e "${GREEN}✅ Python:${NC} $python_version"
    else
        echo -e "${RED}❌ Python 3:${NC} Not found"
    fi

    # Check building-blocks structure
    if [[ -f "$ROOT_DIR/src/building_blocks/__init__.py" ]]; then
        echo -e "${GREEN}✅ Building Blocks:${NC} Library structure found"
    else
        echo -e "${RED}❌ Building Blocks:${NC} Library structure missing"
    fi

    # Check permissions
    if [[ -w "$ROOT_DIR" ]]; then
        echo -e "${GREEN}✅ Permissions:${NC} Write access to repository"
    else
        echo -e "${RED}❌ Permissions:${NC} No write access to $ROOT_DIR"
    fi

    # Check examples directory
    if [[ -d "$ROOT_DIR/examples" ]]; then
        local example_count
        example_count=$(find "$ROOT_DIR/examples" -maxdepth 1 -type d | wc -l)
        echo -e "${GREEN}✅ Examples:${NC} Directory exists ($((example_count - 1)) projects)"
    else
        echo -e "${YELLOW}⚠️ Examples:${NC} Directory will be created"
    fi

    echo ""
    echo "📊 Summary:"
    echo "  Repository: $ROOT_DIR"
    echo "  User: $(whoami)"
    echo "  Date: $(date)"

    echo ""
    read -p "Press Enter to continue..."
    show_main_menu
}

# Start the enhanced help system
echo "Welcome to Building Blocks Help System - Enhanced Edition!"
echo "=========================================================="
echo ""
show_main_menu
