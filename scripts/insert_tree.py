"""
Automatically insert project directory tree into README.md
Usage:
python scripts/tree.py > TREE.md
python scripts/insert_tree.py
"""

from pathlib import Path

readme = Path("README.md").read_text(encoding="utf-8")
tree = Path("TREE.md").read_text(encoding="utf-16")

start = "<!-- TREE_START -->"
end = "<!-- TREE_END -->"

before = readme.split(start)[0]
after = readme.split(end)[1]

new_readme = before + start + "\n\n```text\n" + tree.rstrip() + "\n```\n" + end + after

Path("README.md").write_text(new_readme, encoding="utf-8")
