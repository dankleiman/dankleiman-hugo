#!/usr/bin/env python3
"""
Phase 3: Restructure Hugo content directories.

For each post:
  1. Strip YYYY-MM-DD- date prefix from filename to get new slug
  2. Compute old URL (from front matter `url` field or permalink pattern)
  3. Compute new URL (/taichi/slug/ or /code/slug/)
  4. Add `aliases` to front matter pointing to old URL
  5. Move file to content/taichi/ or content/code/
  6. Delete .html originals for converted posts
  7. Delete dropped .html files

For content/page/:
  - Move entire directory to content/taichi/ as a subdirectory tree
  - Pages keep their existing URL slugs (no date prefix to strip)
  - Add aliases only if the page URL would change

Run with --dry-run first to preview all moves.
"""

import re
import sys
import shutil
from pathlib import Path

DRY_RUN = "--dry-run" in sys.argv

BASE = Path(__file__).parent.parent
POST_DIR = BASE / "content" / "post"
TAICHI_DIR = BASE / "content" / "taichi"
CODE_DIR = BASE / "content" / "code"

DATE_PREFIX = re.compile(r'^\d{4}-\d{2}-\d{2}-(.+)$')

CODE_SLUGS = {
    "2014-03-18-whoa-octopress",
    "2014-03-19-learning-more-about-octopress",
    "2014-03-20-getting-a-feel-for-it",
    "2014-05-12-reflections-on-pre-work-launch-academy",
    "2014-05-17-launch-academy-week-1-reflections",
    "2014-05-21-day-10-the-dreams-continue",
    "2014-05-25-building-a-learning-tool-for-compound-data-structures",
    "2014-05-30-buying-a-mongolian-website",
    "2014-06-08-asking-questions-the-holy-grail-of-oop",
    "2014-06-15-launch-academy-5-weeks-in-or-5-weeks-left",
    "2014-06-23-the-race-to-hello-world-rails-vs-sinatra",
    "2014-07-02-launching-datastroyer",
    "2014-08-03-burlington-ruby-conference-2014",
    "2014-08-11-coding-bootcamp-roi-3-weeks-later",
    "2015-01-11-parachuting-into-unfamilar-code",
    "2015-04-29-10-of-my-favorite-talks-from-railsconf-2015",
    "2015-08-13-sms-to-do-list-with-twilio",
    "2015-08-29-text-me-when-youre-done-twilio-for-notifications-of-long-running-dev-tasks",
    "2015-09-15-i-hate-voicemail-straight-to-sms-with-twilio",
    "2016-03-09-migrating-from-wordpress-to-jekyll",
    "2016-03-11-migrating-posts-and-pages-from-wordpress-to-jekyll",
    "2016-04-10-nice-try-nilclass",
    "2016-09-24-rails-security-exercises-from-bearclaw",
    "2016-12-29-my-5-strategies-for-learning-go-in-2017",
    "2017-02-12-gobridge-with-bill-kennedy",
    "2017-10-06-dont-blow-your-bigquery-budget",
    "2017-10-30-top-n-per-group-in-bigquery",
    # No-date code files (stem only)
    "3-ways-to-level-up-your-sql-as-a-software-engineer",
    "deduping-data-with-row-number",
    "find-missing-data",
    "find-the-latest-record",
    "generating-a-40000-page-site-with-bigquery-hugo-and-github-pages",
    "guarantee-rows",
    "keeping-an-engineering-notebook",
    "more-efficient-top-n-solutions-for-bigquery",
    "order-by-case",
    "roll-your-own-database-part-1",
    "seed-data-for-your-wip-sql-queries",
    "showing-data-change",
    "stop-writing-sql-backwards",
}

DROP_STEMS = {
    "2010-11-08-trainerfly-backstory-the-practice-problem",
    "2010-11-14-trainerfly-backstory-the-moodle-project",
    "2010-11-20-trainerfly-characters",
    "2010-11-29-trainerfly-pre-launch-in-the-works",
    "2011-01-23-new-trainerfly-video-series",
    "2011-02-20-user-feedback-from-trainerfly-beta",
    "2011-04-21-cross-posted-from-trainerfly-launching-an-online-course",
    "2010-11-09-your-spectrum-of-services",
    "2010-12-06-your-marketing-universe",
    "2010-12-10-no-systems-no-raise-for-you-this-year",
    "2010-12-13-make-the-most-of-phase-based-activities",
    "2010-12-21-find-your-true-fans",
    "2010-12-29-become-an-enterprise-of-one",
    "2010-12-29-hybrid-business-thought-experiment",
    "2010-12-31-out-with-the-old-business-model",
    "2011-01-03-epic-meaning-sheep-knuckles-and-the-institute-for-the-future",
    "2011-01-04-crossfits-brilliant-use-of-game-mechanics",
    "2011-01-08-work-speed-mistakes",
    "2011-01-20-simplicity-persuasion-and-technology",
    "2011-01-31-teaching-cycles",
    "2011-02-02-highlights-from-how-great-entrepreneurs-think",
    "2011-02-05-buried-psychological-nuggets",
    "2011-02-21-march-is-going-to-be-health-month",
    "2011-02-23-xkcd-let-go",
    "2011-03-01-the-pros-and-cons-of-automation",
    "2011-03-04-signing-the-contract",
    "2011-03-07-my-rules-are-lame",
    "2011-03-24-take-home-one-new-thing",
    "2011-03-29-health-month-wrap-up",
    "2011-12-29-new-look-for-2012-and-a-special-announcement",
    "2010-12-03-technology-and-all-that-heavenly-glory",
    "2010-11-23-youtube-audioswap",
    "2010-11-15-going-mobile",
    "2010-11-15-mobile-izing-wordpress-and-moodle",
}


def get_new_slug(stem):
    """Strip date prefix YYYY-MM-DD- from stem if present."""
    m = DATE_PREFIX.match(stem)
    return m.group(1) if m else stem


def get_old_url(stem):
    """
    Reconstruct old URL from stem.
    Dated posts: /YYYY/MM/DD/slug/
    Undated posts: /post/slug/ (they were served from /post/ section)
    """
    date_match = re.match(r'^(\d{4})-(\d{2})-(\d{2})-(.+)$', stem)
    if date_match:
        y, mo, d, slug = date_match.groups()
        return f"/{y}/{mo}/{d}/{slug}/"
    else:
        return f"/post/{stem}/"


def inject_aliases(content, old_url):
    """Add aliases field to YAML front matter if not already present."""
    if not content.startswith("---"):
        return content

    end = content.find("\n---\n", 4)
    if end == -1:
        return content

    fm = content[4:end]
    body = content[end + 5:]

    # Don't add if already has aliases
    if re.search(r'^aliases:', fm, re.MULTILINE):
        return content

    alias_block = f'aliases:\n- {old_url}'
    new_fm = fm.rstrip() + '\n' + alias_block
    return f"---\n{new_fm}\n---\n{body}"


def process_posts(dry_run):
    moves = []
    deletes = []

    # Collect all .md files (the converted ones)
    md_files = sorted(POST_DIR.glob("*.md"))

    for md_path in md_files:
        stem = md_path.stem  # filename without extension

        if stem in DROP_STEMS:
            deletes.append(('drop_md', md_path))
            continue

        new_slug = get_new_slug(stem)
        old_url = get_old_url(stem)

        if stem in CODE_SLUGS:
            dest_dir = CODE_DIR
            new_url = f"/code/{new_slug}/"
        else:
            dest_dir = TAICHI_DIR
            new_url = f"/taichi/{new_slug}/"

        dest_path = dest_dir / f"{new_slug}.md"
        moves.append((md_path, dest_path, old_url, new_url))

    # Also collect .html files to delete (originals + drops)
    html_files = sorted(POST_DIR.glob("*.html"))
    for html_path in html_files:
        deletes.append(('delete_html', html_path))

    print(f"\n{'[DRY RUN] ' if dry_run else ''}POST MOVES ({len(moves)} files):")
    for src, dst, old_url, new_url in moves[:10]:
        print(f"  {src.name} -> {dst.relative_to(BASE)}  [{old_url} -> {new_url}]")
    if len(moves) > 10:
        print(f"  ... and {len(moves) - 10} more")

    print(f"\n{'[DRY RUN] ' if dry_run else ''}HTML DELETES ({len(deletes)} files):")
    for action, path in deletes[:5]:
        print(f"  {action}: {path.name}")
    if len(deletes) > 5:
        print(f"  ... and {len(deletes) - 5} more")

    if not dry_run:
        TAICHI_DIR.mkdir(parents=True, exist_ok=True)
        CODE_DIR.mkdir(parents=True, exist_ok=True)

        for src, dst, old_url, new_url in moves:
            content = src.read_text(encoding="utf-8")
            content = inject_aliases(content, old_url)
            dst.write_text(content, encoding="utf-8")

        for action, path in deletes:
            if path.exists():
                path.unlink()

        print(f"\nMoved {len(moves)} posts.")
        print(f"Deleted {len(deletes)} files.")

    return moves, deletes


def process_pages(dry_run):
    """
    Move content/page/ -> content/taichi/pages/
    Pages keep their slug-based URLs (/:title) so most won't change.
    The section changes from 'page' to 'taichi' but URL stays the same
    because we'll configure taichi section with /:slug permalinks.
    No aliases needed since the URL path itself doesn't change.
    """
    page_dir = BASE / "content" / "page"
    dest_dir = TAICHI_DIR / "pages"

    if not page_dir.exists():
        print("\nNo content/page/ directory found, skipping.")
        return

    subdirs = [d for d in page_dir.iterdir() if d.is_dir()]
    files = [f for f in page_dir.iterdir() if f.is_file()]

    print(f"\n{'[DRY RUN] ' if dry_run else ''}PAGE MOVE:")
    print(f"  content/page/ -> content/taichi/pages/")
    print(f"  ({len(subdirs)} subdirectories, {len(files)} top-level files)")

    if not dry_run:
        dest_dir.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(str(page_dir), str(dest_dir))
        shutil.rmtree(str(page_dir))
        print(f"  Moved content/page/ to content/taichi/pages/")


def main():
    print(f"Mode: {'DRY RUN (no changes will be made)' if DRY_RUN else 'LIVE (files will be moved)'}")

    moves, deletes = process_posts(DRY_RUN)
    process_pages(DRY_RUN)

    taichi_count = sum(1 for src, dst, _, _ in moves if dst.parent.name == 'taichi')
    code_count = sum(1 for src, dst, _, _ in moves if dst.parent.name == 'code')

    print(f"\nSummary:")
    print(f"  Tai chi posts -> content/taichi/: {taichi_count}")
    print(f"  Code posts    -> content/code/:   {code_count}")
    print(f"  HTML deletes:                     {len(deletes)}")
    if DRY_RUN:
        print(f"\nRun without --dry-run to execute.")


if __name__ == "__main__":
    main()
