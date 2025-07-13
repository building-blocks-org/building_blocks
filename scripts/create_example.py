#!/usr/bin/env python3
import argparse
import os
import sys

EXAMPLES_DIR = "examples"


def create_init_file(path: str) -> None:
    """
    Creates an empty __init__.py file in the specified directory.

    Args:
        path: The path to the directory where the __init__.py file should be
        created.
    """
    with open(os.path.join(path, "__init__.py"), "a") as _:
        pass


def create_package_directory(path: str):
    """
    Creates a directory and places an empty __init__.py file inside it,
    making it a Python package.

    Args:
        path: The path to the directory to create.
    """
    os.makedirs(path, exist_ok=True)
    create_init_file(path)
    print(f"Created Python package directory: {path}")


def create_ports_directory(layer_path: str) -> None:
    """
    Create the ports directory structure (ports, inbound, outbound)
    as Python packages within the specified layer path.

    Args:
        layer_path (str): The base path of the layer (e.g., application_dir,
        domain_dir).
    """
    ports_package = os.path.join(layer_path, "ports")
    create_package_directory(ports_package)
    create_package_directory(os.path.join(ports_package, "inbound"))
    create_package_directory(os.path.join(ports_package, "outbound"))


def create_layer_sub_structure(
    layer_path: str,
    create_ports: bool = False,
    create_services: bool = False,  # Changed default to False
    create_entities: bool = False,
    create_value_objects: bool = False,
) -> None:
    """
    Creates common sub-structure (e.g., services, ports, entities,
    value_objects) for a given layer.

    Args:
        layer_path (str): The base path of the layer (e.g., application_dir,
        domain_dir).
        create_ports (bool): If True, creates the 'ports' directory structure.
        create_services (bool): If True, creates the 'services' directory.
        create_entities (bool): If True, creates the 'entities' directory.
        create_value_objects (bool): If True, creates the 'value_objects'
        directory.
    """
    try:
        if create_services:
            services_package = os.path.join(layer_path, "services")
            create_package_directory(services_package)

        if create_ports:
            create_ports_directory(layer_path)

        if create_entities:
            entities_package = os.path.join(layer_path, "entities")
            create_package_directory(entities_package)

        if create_value_objects:
            value_objects_package = os.path.join(layer_path, "value_objects")
            create_package_directory(value_objects_package)

    except IOError as e:
        print(
            f"Error creating layer sub-structure in {layer_path}: {e}", file=sys.stderr
        )
        sys.exit(1)


def create_specific_layer(
    example_name: str,
    layer_name: str,
    create_ports: bool = False,
    create_services: bool = False,
    create_entities: bool = False,
    create_value_objects: bool = False,
) -> None:
    """
    Creates a specific architectural layer for an example project,
    including its base directory and optional sub-structures.

    Args:
        example_name (str): The name of the example.
        layer_name (str): The name of the layer (e.g., "application", "domain").
        create_ports (bool): If True, creates the 'ports' directory structure.
        create_services (bool): If True, creates the 'services' directory.
        create_entities (bool): If True, creates the 'entities' directory (for
        domain).
        create_value_objects (bool): If True, creates the 'value_objects'
        directory (for domain).
    """
    layer_dir = os.path.join(EXAMPLES_DIR, example_name, "src", layer_name)
    create_package_directory(layer_dir)

    create_layer_sub_structure(
        layer_dir,
        create_ports=create_ports,
        create_services=create_services,
        create_entities=create_entities,
        create_value_objects=create_value_objects,
    )


def main():
    parser = argparse.ArgumentParser(
        description="Creates a new example project structure."
    )
    parser.add_argument(
        "example_name", help="The name of the example project (e.g., my_service)."
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="The host port to map to the container (default: 8000).",
    )

    args = parser.parse_args()

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    examples_dir_path = os.path.join(project_root, "examples")

    print(f"Project root identified: {project_root}")
    print(f"Examples directory: {examples_dir_path}")

    os.makedirs(examples_dir_path, exist_ok=True)

    example_base_path = os.path.join(examples_dir_path, args.example_name)
    src_path = os.path.join(example_base_path, "src")
    os.makedirs(src_path, exist_ok=True)
    print(f"Created base example directory: {example_base_path}")
    print(f"Created src directory: {src_path}")

    # Application Layer
    create_specific_layer(
        args.example_name, "application", create_ports=True, create_services=True
    )

    # Domain Layer
    create_specific_layer(
        args.example_name,
        "domain",
        create_ports=True,
        create_services=False,
        create_entities=True,
        create_value_objects=True,
    )

    # Infrastructure Layer
    create_specific_layer(
        args.example_name, "infrastructure", create_ports=False, create_services=False
    )

    # Presentation Layer
    create_specific_layer(
        args.example_name, "presentation", create_ports=False, create_services=False
    )

    print("Done creating example structure.")


if __name__ == "__main__":
    main()
