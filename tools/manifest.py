"""Print `sha256  project/<path>` for every file under design-system/.

The Design System artifact keeps the same files under project/. Compare this output
with the artifact's file list after a sync: every line must match.

Usage:  python3 tools/manifest.py
"""
import hashlib, os

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "design-system")

rows = []
for d, _, files in os.walk(ROOT):
    for f in files:
        p = os.path.join(d, f)
        rel = os.path.relpath(p, ROOT).replace(os.sep, "/")
        rows.append(("project/" + rel, hashlib.sha256(open(p, "rb").read()).hexdigest()))
for path, digest in sorted(rows):
    print(digest, path)
print(f"{len(rows)} files")
