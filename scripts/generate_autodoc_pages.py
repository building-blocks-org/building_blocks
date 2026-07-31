"""API Reference generator for ForgingBlocks.

This script generates API-level documentation from docstrings.
It is intended for contributors and advanced users, not as a replacement
for curated Guide or Reference documentation.
"""

from __future__ import annotations

import ast
import re
import shutil
import sys
import textwrap
from pathlib import Path

SRC_DIR = Path("src/forging_blocks")
OUT_DIR = Path("docs/reference/autodoc")
MKDOCS_YML = Path("mkdocs.yml")


def module_title(path: Path) -> str:
    """Convert a module path to a readable title."""
    return path.stem.replace("_", " ").title()


def import_path(path: Path) -> str:
    """Convert a file path to a Python import path."""
    rel = path.relative_to(SRC_DIR)
    return f"forging_blocks.{'.'.join(rel.with_suffix('').parts)}"


def ensure_dir(path: Path) -> None:
    """Ensure the parent directory of a path exists."""
    path.parent.mkdir(parents=True, exist_ok=True)


def find_source_files(base: Path) -> list[Path]:
    """Find all Python source files, excluding __init__.py and internal modules.

    Internal modules are those under directories named ``helpers`` — these
    are implementation details, not part of the public API surface.
    """
    return [
        p
        for p in base.rglob("*.py")
        if p.name != "__init__.py" and "helpers" not in p.relative_to(base).parts
    ]


def generate_markdown(src: Path) -> Path:
    """Generate a markdown file for a given Python source file."""
    title = module_title(src)
    out = OUT_DIR / src.relative_to(SRC_DIR).with_suffix(".md")
    ensure_dir(out)

    content = [
        f"# {title}",
        "",
        f"::: {import_path(src)}",
        "    options:",
        "      show_source: true",
        "      show_root_heading: true",
    ]
    out.write_text("\n".join(content), encoding="utf-8")

    print(f"[OK] Generated: {out}")
    return out


def _group_autodoc_files(
    files: list[Path], out_dir: Path
) -> dict[str, tuple[list[tuple[str, str]], dict[str, object]]]:
    """Group autodoc markdown files into a recursive tree by layer.

    Returns ``{layer_name: (page_entries, subdirectories)}`` where each node is a
    tuple of *(title, relative_path) pages* at that level and a dict of
    *subdirectory-name → nested_node*.
    """
    tree: dict[str, tuple[list[tuple[str, str]], dict[str, object]]] = {}

    for file in files:
        parts = list(file.relative_to(out_dir).parts)
        if not parts:
            continue

        layer = parts[0].replace("_", " ").title()
        title = parts[-1].removesuffix(".md").replace("_", " ").title()
        path = "/".join(parts)

        if layer not in tree:
            tree[layer] = ([], {})

        current: tuple[list[tuple[str, str]], dict[str, object]] = tree[layer]
        for part in parts[1:-1]:
            name = part.replace("_", " ").title()
            if name not in current[1]:
                current[1][name] = ([], {})
            current = current[1][name]  # type: ignore[assignment]

        current[0].append((title, path))

    return tree


def _render_nav_tree(
    node: tuple[list[tuple[str, str]], dict[str, object]],
    indent: str,
    level: int,
) -> list[str]:
    """Render a tree node recursively as MkDocs nav YAML lines.

    Section headers (directories with no page path) become
    expandable/collapsible containers in MkDocs.
    """
    pages, subdirs = node
    lines: list[str] = []
    for name, link in sorted(pages):
        lines.append(f"{indent * level}- {name}: reference/autodoc/{link}")
    for dirname in sorted(subdirs):
        lines.append(f"{indent * level}- {dirname}:")
        sub_node = subdirs[dirname]
        lines.extend(
            _render_nav_tree(
                sub_node,  # type: ignore[arg-type]
                indent,
                level + 1,
            )
        )
    return lines


def build_autodoc_section(files: list[Path], indent: str = "  ") -> str:
    """Build the MkDocs navigation section for autodoc pages.

    The first entry is always a link to the autodoc index page,
    followed by pages grouped by architectural layer with
    recursive nesting for subdirectories.
    """
    grouped = _group_autodoc_files(files, OUT_DIR)

    lines = [f"{indent}- API Reference:", f"{indent}  - Overview: reference/autodoc/index.md"]
    for layer in sorted(grouped):
        lines.append(f"{indent}  - {layer}:")
        lines.extend(_render_nav_tree(grouped[layer], indent, 3))

    return "\n".join(lines)


def update_nav(mkdocs: str, section: str) -> str:
    """Update the MkDocs navigation section with the autodoc section."""
    api_ref_pattern = r"(?ms)^  - API Reference:.*?(?=^  - [A-Z]|^[a-z_]+:|\Z)"
    if re.search(api_ref_pattern, mkdocs):
        return re.sub(api_ref_pattern, section + "\n", mkdocs)

    ref_pattern = r"(?ms)^  - Reference:.*?(?=^  - [A-Z]|^[a-z_]+:|\Z)"
    match = re.search(ref_pattern, mkdocs)
    if match:
        insert_pos = match.end()
        return mkdocs[:insert_pos] + section + "\n" + mkdocs[insert_pos:]

    return mkdocs.rstrip() + "\n" + section + "\n"


_PYTHON_BLOCK_RE = re.compile(r"```python\n(.*?)```", re.DOTALL)


def _find_python_blocks(docstring: str) -> list[str]:
    """Extract ```python code blocks from a docstring."""
    return _PYTHON_BLOCK_RE.findall(docstring)


def validate_docstring_imports(src_path: Path) -> list[str]:
    """Verify that imports in docstring code examples are actually used.

    Parses every ```python block in every module/class/function docstring,
    collects imported names, then checks whether each imported name appears
    as a ``Load``-context reference (including as the root of an attribute
    chain like ``mod.Thing``).

    Returns a list of warning messages, one per unused import.
    """
    warnings: list[str] = []
    source = src_path.read_text(encoding="utf-8")

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return warnings

    for node in ast.walk(tree):
        if not isinstance(node, ast.Module | ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
            continue
        docstring = ast.get_docstring(node)
        if not docstring:
            continue
        for block in _find_python_blocks(docstring):
            try:
                block_tree = ast.parse(textwrap.dedent(block))
            except SyntaxError:
                continue

            imported: dict[str, int] = {}  # name -> line in block
            for n in ast.walk(block_tree):
                match n:
                    case ast.Import(names=names):
                        for alias in names:
                            imported[alias.asname or alias.name] = n.lineno
                    case ast.ImportFrom(names=names):
                        for alias in names:
                            if alias.name == "*":
                                continue
                            imported[alias.asname or alias.name] = n.lineno

            used: set[str] = set()
            for n in ast.walk(block_tree):
                if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load):
                    used.add(n.id)
                elif isinstance(n, ast.Attribute) and isinstance(n.ctx, ast.Load):
                    root = n
                    while isinstance(root, ast.Attribute):
                        root = root.value
                    if isinstance(root, ast.Name):
                        used.add(root.id)

            for name, line_no in imported.items():
                if name not in used:
                    warnings.append(
                        f"{src_path}: unused import '{name}' "
                        f"in docstring code example (block line {line_no})"
                    )

    return warnings


def _render_index_tree(
    node: tuple[list[tuple[str, str]], dict[str, object]],
    level: int = 0,
) -> list[str]:
    """Render a tree node recursively as markdown index links.

    Subdirectories become nested headings (``###``, ``####``, …),
    preserving the directory hierarchy in the generated index.
    """
    pages, subdirs = node
    lines: list[str] = []
    for name, link in sorted(pages):
        lines.append(f"- [{name}]({link})")
    if pages and subdirs:
        lines.append("")
    for dirname in sorted(subdirs):
        heading = "#" * (level + 3)
        lines.append(f"{heading} {dirname}")
        lines.append("")
        sub_node = subdirs[dirname]
        lines.extend(
            _render_index_tree(
                sub_node,  # type: ignore[arg-type]
                level + 1,
            )
        )
        lines.append("")
    return lines


def generate_autodoc_index(files: list[Path], out_dir: Path) -> Path:
    """Generate a teachable index page linking to every autodoc page.

    Groups pages by architectural layer and writes a markdown file
    with an introductory paragraph followed by per-layer link lists
    that mirror the directory hierarchy.
    Always regenerates so the index stays in sync with the source tree.
    """
    index_file = out_dir / "index.md"
    grouped = _group_autodoc_files(files, out_dir)

    lines: list[str] = [
        "# API Reference",
        "",
        "Welcome to the ForgingBlocks API reference! This section is",
        "generated automatically from the library docstrings and gives you",
        "the full public API surface — every class, function, and module",
        "that makes up the toolkit.",
        "",
        "Use it as a companion to the hand-written **Guide** (which walks",
        "you through concepts and workflows) and **Reference** (which covers",
        "architectural intent and design rationale). Think of this page as",
        "your map: pick a layer below, dive into the module you need, and",
        "explore the signatures, docstrings, and source code directly.",
        "",
    ]

    for layer, node in sorted(grouped.items()):
        lines.append(f"## {layer}")
        lines.append("")
        lines.extend(_render_index_tree(node))
        lines.append("")

    index_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[OK] Generated: {index_file}")
    return index_file


def main() -> None:
    """Main function to generate autodoc pages and update mkdocs.yml."""
    if not SRC_DIR.exists():
        print(f"[ERROR] Source directory not found: {SRC_DIR}")
        sys.exit(1)

    source_files = find_source_files(SRC_DIR)

    all_warnings: list[str] = []
    for src_path in source_files:
        all_warnings.extend(validate_docstring_imports(src_path))

    if all_warnings:
        print("\n[DOCSTRING IMPORT WARNINGS]")
        for w in all_warnings:
            print(f"  {w}")
        print()
        sys.exit(1)

    # Clean stale autodoc pages from renamed/deleted modules
    shutil.rmtree(OUT_DIR, ignore_errors=True)

    files = [generate_markdown(p) for p in source_files]
    generate_autodoc_index(files, OUT_DIR)

    mkdocs_text = MKDOCS_YML.read_text(encoding="utf-8")
    section = build_autodoc_section(files)
    updated_mkdocs = update_nav(mkdocs_text, section)
    MKDOCS_YML.write_text(updated_mkdocs, encoding="utf-8")

    print("\n[DOCS] Autodoc generation complete.\n")


if __name__ == "__main__":
    main()
