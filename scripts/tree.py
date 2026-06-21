from pathlib import Path
import sys
sys.stdout.reconfigure(encoding="utf-8")

IGNORE_DIRS = {
    ".venv",
    "__pycache__",
    ".git",
    ".pytest_cache",
    ".mypy_cache",
}

SHOW_EXTENSIONS = {".py", ".toml", ".md"}  # adjust as needed


def should_skip_dir(name: str) -> bool:
    return name in IGNORE_DIRS


def should_show_file(path: Path) -> bool:
    return path.suffix in SHOW_EXTENSIONS


def print_tree(path: Path, prefix: str = ""):
    entries = sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))

    entries = [
        e for e in entries
        if not (e.is_dir() and should_skip_dir(e.name)) and (e.name != "__init__.py")
    ]

    for i, entry in enumerate(entries):
        connector = "└── " if i == len(entries) - 1 else "├── "

        print(prefix + connector + entry.name)

        if entry.is_dir():
            extension = "    " if i == len(entries) - 1 else "│   "
            print_tree(entry, prefix + extension)


if __name__ == "__main__":
    root = Path("src/app")
    print(root.name)

    print_tree(root)