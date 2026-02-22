#!/usr/bin/env python3
"""
Fix internal links in content files.

Strategy:
  1. Build a URL map (old_url -> new_url) from the aliases in every .md file.
  2. For each content file, scan the BODY only (not front matter) and:
     - If a dankleiman.com URL is in the alias map -> replace with new section URL.
     - Otherwise -> strip the domain prefix, leaving a root-relative path.
       Pages kept their `url:` field so they still serve at the same path.

Run with --dry-run first to preview changes.
"""

import re
import sys
from pathlib import Path

DRY_RUN = "--dry-run" in sys.argv

BASE = Path(__file__).parent.parent
TAICHI_DIR = BASE / "content" / "taichi"
CODE_DIR = BASE / "content" / "code"

# Matches http://dankleiman.com/... or https://www.dankleiman.com/...
DOMAIN_RE = re.compile(
    r'https?://(?:www\.)?dankleiman\.com(/[^\s"\')\]>]*)',
    re.IGNORECASE,
)


def parse_yaml_aliases(content):
    """Extract aliases list from YAML front matter using regex (no yaml dep)."""
    if not content.startswith("---\n"):
        return []
    end = content.find("\n---\n", 4)
    if end == -1:
        return []
    fm_text = content[4:end]
    # Match the aliases block: aliases:\n- /url1/\n- /url2/
    m = re.search(r'^aliases:\n((?:- [^\n]+\n?)+)', fm_text, re.MULTILINE)
    if not m:
        return []
    return re.findall(r'^- (.+)$', m.group(1), re.MULTILINE)


def parse_toml_aliases(content):
    """Extract aliases list from TOML front matter using regex."""
    if not content.startswith("+++\n"):
        return []
    end = content.find("\n+++\n", 4)
    if end == -1:
        return []
    fm_text = content[4:end]
    m = re.search(r'^aliases\s*=\s*\[([^\]]*)\]', fm_text, re.MULTILINE)
    if m:
        return re.findall(r'"([^"]+)"', m.group(1))
    return []


def build_url_map():
    """Return dict mapping old_path -> new_url for all content files."""
    url_map = {}

    def register(aliases, new_url):
        for alias in aliases:
            path = alias.rstrip("/")
            url_map[path + "/"] = new_url
            url_map[path] = new_url

    for md_file in sorted(TAICHI_DIR.glob("*.md")):
        if md_file.name == "_index.md":
            continue
        content = md_file.read_text(encoding="utf-8")
        new_url = f"/taichi/{md_file.stem}/"
        register(parse_yaml_aliases(content), new_url)

    for md_file in sorted(CODE_DIR.glob("*.md")):
        if md_file.name == "_index.md":
            continue
        content = md_file.read_text(encoding="utf-8")
        new_url = f"/code/{md_file.stem}/"
        register(parse_yaml_aliases(content) or parse_toml_aliases(content), new_url)

    return url_map


def split_front_matter(content):
    """Return (front_matter_str, body_str) tuple."""
    if content.startswith("---\n"):
        end = content.find("\n---\n", 4)
        if end != -1:
            return content[: end + 5], content[end + 5:]
    elif content.startswith("+++\n"):
        end = content.find("\n+++\n", 4)
        if end != -1:
            return content[: end + 5], content[end + 5:]
    return "", content


def fix_body(body, url_map):
    """Replace dankleiman.com links in body text."""

    def replacer(m):
        path = m.group(1)
        # Normalise: ensure trailing slash for lookup
        lookup = path.rstrip("/") + "/"
        if lookup in url_map:
            return url_map[lookup]
        if path in url_map:
            return url_map[path]
        # Not a post URL — strip domain, keep root-relative path
        return path if path else "/"

    return DOMAIN_RE.sub(replacer, body)


def main():
    print(f"Mode: {'DRY RUN' if DRY_RUN else 'LIVE'}")

    url_map = build_url_map()
    print(f"Built URL map with {len(url_map)} entries")

    all_files = (
        [f for f in TAICHI_DIR.glob("*.md") if f.name != "_index.md"]
        + [f for f in CODE_DIR.glob("*.md") if f.name != "_index.md"]
    )

    changed = 0
    total_replacements = 0

    for md_file in sorted(all_files):
        content = md_file.read_text(encoding="utf-8")
        fm, body = split_front_matter(content)

        new_body = fix_body(body, url_map)
        if new_body == body:
            continue

        # Count how many links changed
        n = len(DOMAIN_RE.findall(body)) - len(DOMAIN_RE.findall(new_body))
        # (all matches in body were replaced, so count original matches)
        n_orig = len(DOMAIN_RE.findall(body))

        print(f"  {md_file.name}: {n_orig} link(s) updated")
        total_replacements += n_orig
        changed += 1

        if not DRY_RUN:
            md_file.write_text(fm + new_body, encoding="utf-8")

    print(f"\n{'Would update' if DRY_RUN else 'Updated'} {changed} files, "
          f"{total_replacements} links total.")
    if DRY_RUN:
        print("Run without --dry-run to apply.")


if __name__ == "__main__":
    main()
