#!/usr/bin/env python3
"""Stage a clean, review-safe copy of the site for uploading to a static host.

Excludes build tooling and notes, and adds a blanket robots.txt so a shared
review link is not crawled or indexed while the content is still in draft.

    python3 tools-build-preview.py

Output: ../assemble-capital-preview/   (drag this folder onto the host)
"""
import os
import shutil

SRC = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(SRC), "assemble-capital-preview")

# never ship build tooling, notes, or OS cruft
EXCLUDE_FILES = {"README.md", ".DS_Store"}
EXCLUDE_PREFIX = ("tools-",)
EXCLUDE_SUFFIX = (".py", ".md")
EXCLUDE_DIRS = {".git", "__pycache__", "node_modules"}

ROBOTS = """# Private review build — not for indexing.
User-agent: *
Disallow: /
"""

def keep(name):
    if name in EXCLUDE_FILES:
        return False
    if name.startswith(EXCLUDE_PREFIX):
        return False
    if name.endswith(EXCLUDE_SUFFIX):
        return False
    return True

# Rebuild the output dir, but preserve the Vercel/Git link dirs so re-deploys
# keep hitting the same project + URL instead of minting a new one each time.
PRESERVE = (".vercel", ".git")
if os.path.isdir(OUT):
    for entry in os.listdir(OUT):
        if entry in PRESERVE:
            continue
        p = os.path.join(OUT, entry)
        shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
else:
    os.makedirs(OUT, exist_ok=True)

copied = skipped = 0
for root, dirs, files in os.walk(SRC):
    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
    rel = os.path.relpath(root, SRC)
    dest_dir = OUT if rel == "." else os.path.join(OUT, rel)
    os.makedirs(dest_dir, exist_ok=True)
    for f in files:
        if keep(f):
            shutil.copy2(os.path.join(root, f), os.path.join(dest_dir, f))
            copied += 1
        else:
            skipped += 1

with open(os.path.join(OUT, "robots.txt"), "w") as fh:
    fh.write(ROBOTS)

size = sum(os.path.getsize(os.path.join(r, f))
           for r, _, fs in os.walk(OUT) for f in fs)
print(f"staged  : {OUT}")
print(f"copied  : {copied} files ({size / 1024 / 1024:.1f} MB)")
print(f"excluded: {skipped} tooling/notes files")
print("robots.txt: Disallow: /  (blocks crawling of the review link)")
