#!/usr/bin/env python3
"""
Convert Hugo HTML posts to Markdown.
- Strips WordPress legacy front matter fields
- Converts HTML body to Markdown via html2text
- Flags broken/legacy content (Flash embeds, missing images, internal links)
- Writes a report of issues found
"""

import os
import re
import sys
import json
import html2text
from pathlib import Path

POST_DIR = Path(__file__).parent.parent / "content" / "post"
REPORT_PATH = Path(__file__).parent.parent / "scripts" / "conversion_report.json"

# Front matter fields to drop entirely
DROP_FIELDS = {
    "comments", "wordpress_id", "wordpress_url", "date_gmt",
    "status", "published", "excerpt"
}

# Patterns that flag content issues
FLASH_PATTERN = re.compile(r'<object|<embed|classid="clsid:', re.IGNORECASE)
IMG_PATTERN = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']', re.IGNORECASE)
INTERNAL_LINK_PATTERN = re.compile(r'href=["\'](?:https?://dankleiman\.com)?(/[^"\']+)["\']', re.IGNORECASE)
WP_SHORTCODE_PATTERN = re.compile(r'\[caption[^\]]*\]|\[/caption\]|\[gallery[^\]]*\]', re.IGNORECASE)
MORE_TAG_PATTERN = re.compile(r'<a id="more[^"]*"[^>]*></a>', re.IGNORECASE)

# Files to convert: only .html files
# Code list — skip these (already .md or will be handled separately)
CODE_FILES = {
    "2014-03-18-whoa-octopress.md",
    "2014-03-19-learning-more-about-octopress.md",
    "2014-03-20-getting-a-feel-for-it.md",
    "2014-05-12-reflections-on-pre-work-launch-academy.md",
    "2014-05-17-launch-academy-week-1-reflections.md",
    "2014-05-21-day-10-the-dreams-continue.md",
    "2014-05-25-building-a-learning-tool-for-compound-data-structures.md",
    "2014-05-30-buying-a-mongolian-website.md",
    "2014-06-08-asking-questions-the-holy-grail-of-oop.md",
    "2014-06-15-launch-academy-5-weeks-in-or-5-weeks-left.md",
    "2014-06-23-the-race-to-hello-world-rails-vs-sinatra.md",
    "2014-07-02-launching-datastroyer.md",
    "2014-08-03-burlington-ruby-conference-2014.md",
    "2014-08-11-coding-bootcamp-roi-3-weeks-later.md",
    "2015-01-11-parachuting-into-unfamilar-code.md",
    "2015-04-29-10-of-my-favorite-talks-from-railsconf-2015.md",
    "2015-08-13-sms-to-do-list-with-twilio.md",
    "2015-08-29-text-me-when-youre-done-twilio-for-notifications-of-long-running-dev-tasks.md",
    "2015-09-15-i-hate-voicemail-straight-to-sms-with-twilio.md",
    "2016-03-09-migrating-from-wordpress-to-jekyll.md",
    "2016-03-11-migrating-posts-and-pages-from-wordpress-to-jekyll.md",
    "2016-04-10-nice-try-nilclass.md",
    "2016-09-24-rails-security-exercises-from-bearclaw.md",
    "2016-12-29-my-5-strategies-for-learning-go-in-2017.md",
    "2017-02-12-gobridge-with-bill-kennedy.md",
    "2017-10-06-dont-blow-your-bigquery-budget.md",
    "2017-10-30-top-n-per-group-in-bigquery.md",
    "3-ways-to-level-up-your-sql-as-a-software-engineer.md",
    "deduping-data-with-row-number.md",
    "find-missing-data.md",
    "find-the-latest-record.md",
    "generating-a-40000-page-site-with-bigquery-hugo-and-github-pages.md",
    "guarantee-rows.md",
    "keeping-an-engineering-notebook.md",
    "more-efficient-top-n-solutions-for-bigquery.md",
    "order-by-case.md",
    "roll-your-own-database-part-1.md",
    "seed-data-for-your-wip-sql-queries.md",
    "showing-data-change.md",
    "stop-writing-sql-backwards.md",
}

DROP_FILES = {
    "2010-11-08-trainerfly-backstory-the-practice-problem.html",
    "2010-11-14-trainerfly-backstory-the-moodle-project.html",
    "2010-11-20-trainerfly-characters.html",
    "2010-11-29-trainerfly-pre-launch-in-the-works.html",
    "2011-01-23-new-trainerfly-video-series.html",
    "2011-02-20-user-feedback-from-trainerfly-beta.html",
    "2011-04-21-cross-posted-from-trainerfly-launching-an-online-course.html",
    "2010-11-09-your-spectrum-of-services.html",
    "2010-12-06-your-marketing-universe.html",
    "2010-12-10-no-systems-no-raise-for-you-this-year.html",
    "2010-12-13-make-the-most-of-phase-based-activities.html",
    "2010-12-21-find-your-true-fans.html",
    "2010-12-29-become-an-enterprise-of-one.html",
    "2010-12-29-hybrid-business-thought-experiment.html",
    "2010-12-31-out-with-the-old-business-model.html",
    "2011-01-03-epic-meaning-sheep-knuckles-and-the-institute-for-the-future.html",
    "2011-01-04-crossfits-brilliant-use-of-game-mechanics.html",
    "2011-01-08-work-speed-mistakes.html",
    "2011-01-20-simplicity-persuasion-and-technology.html",
    "2011-01-31-teaching-cycles.html",
    "2011-02-02-highlights-from-how-great-entrepreneurs-think.html",
    "2011-02-05-buried-psychological-nuggets.html",
    "2011-02-21-march-is-going-to-be-health-month.html",
    "2011-02-23-xkcd-let-go.html",
    "2011-03-01-the-pros-and-cons-of-automation.html",
    "2011-03-04-signing-the-contract.html",
    "2011-03-07-my-rules-are-lame.html",
    "2011-03-24-take-home-one-new-thing.html",
    "2011-03-29-health-month-wrap-up.html",
    "2011-12-29-new-look-for-2012-and-a-special-announcement.html",
    "2010-12-03-technology-and-all-that-heavenly-glory.html",
    "2010-11-23-youtube-audioswap.html",
    "2010-11-15-going-mobile.html",
    "2010-11-15-mobile-izing-wordpress-and-moodle.html",
}


def parse_front_matter(content):
    """Split YAML front matter from HTML body. Returns (fm_text, body_text)."""
    if not content.startswith("---"):
        return None, content
    # Find the closing ---
    end = content.find("\n---\n", 4)
    if end == -1:
        return None, content
    fm_text = content[4:end]
    body_text = content[end + 5:]
    return fm_text, body_text


def clean_front_matter(fm_text):
    """
    Remove DROP_FIELDS from YAML front matter using line-level parsing.
    Returns cleaned YAML string and a dict of kept fields for reference.
    """
    lines = fm_text.split("\n")
    cleaned = []
    skip_block = False
    kept = {}
    current_key = None

    for line in lines:
        # Detect top-level key (not indented)
        top_key_match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*):', line)
        if top_key_match:
            current_key = top_key_match.group(1)
            skip_block = current_key in DROP_FIELDS
            if not skip_block:
                cleaned.append(line)
                kept[current_key] = []
        elif skip_block:
            # This line belongs to a dropped block — skip it
            continue
        else:
            cleaned.append(line)
            if current_key and current_key in kept:
                kept[current_key].append(line.strip())

    return "\n".join(cleaned), kept


def convert_body(html_body):
    """Convert HTML body to Markdown using html2text."""
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.body_width = 0  # Don't wrap lines
    h.protect_links = False
    h.unicode_snob = True
    h.wrap_links = False
    h.mark_code = True
    return h.handle(html_body)


def audit_body(html_body, filename):
    """Return a list of issues found in the HTML body."""
    issues = []

    if FLASH_PATTERN.search(html_body):
        issues.append({"type": "flash_embed", "detail": "Contains Flash <object>/<embed> tag — needs YouTube iframe replacement"})

    for img_match in IMG_PATTERN.finditer(html_body):
        src = img_match.group(1)
        if src.startswith("/uploads/") or src.startswith("http://dankleiman.com/uploads/"):
            # Normalize to local path
            local = src.replace("http://dankleiman.com", "")
            static_path = Path(__file__).parent.parent / "static" / local.lstrip("/")
            if not static_path.exists():
                issues.append({"type": "missing_image", "detail": f"Image not found in static/: {local}"})
            else:
                issues.append({"type": "image_ref", "detail": f"Image ref (exists): {local}"})
        elif src.startswith("http://") or src.startswith("https://"):
            issues.append({"type": "external_image", "detail": f"External image: {src}"})

    for link_match in INTERNAL_LINK_PATTERN.finditer(html_body):
        path = link_match.group(1)
        issues.append({"type": "internal_link", "detail": f"Internal link: {path}"})

    if WP_SHORTCODE_PATTERN.search(html_body):
        issues.append({"type": "wp_shortcode", "detail": "Contains WordPress [caption] or [gallery] shortcode"})

    return issues


def process_file(filepath):
    """Process a single HTML file. Returns result dict."""
    filename = filepath.name
    result = {"file": filename, "issues": [], "status": "ok"}

    content = filepath.read_text(encoding="utf-8", errors="replace")

    fm_text, body = parse_front_matter(content)
    if fm_text is None:
        result["status"] = "no_front_matter"
        result["issues"].append({"type": "parse_error", "detail": "No front matter found"})
        return result

    # Audit before conversion
    issues = audit_body(body, filename)
    result["issues"] = issues

    # Clean front matter
    clean_fm, kept_fields = clean_front_matter(fm_text)

    # Remove WordPress <a id="more"> tags from body
    body = MORE_TAG_PATTERN.sub("", body)

    # Convert body to markdown
    md_body = convert_body(body)

    # Build output
    output = f"---\n{clean_fm.strip()}\n---\n\n{md_body.strip()}\n"

    # Write .md file (same name, .md extension)
    out_path = filepath.with_suffix(".md")
    out_path.write_text(output, encoding="utf-8")

    result["status"] = "converted"
    result["output_file"] = str(out_path.name)
    return result


def main():
    html_files = sorted(f for f in POST_DIR.glob("*.html") if f.name not in DROP_FILES)

    print(f"Found {len(html_files)} HTML files to convert (excluding dropped files)")

    report = {
        "total": len(html_files),
        "converted": 0,
        "errors": 0,
        "flash_embeds": [],
        "missing_images": [],
        "existing_images": [],
        "external_images": [],
        "internal_links": [],
        "wp_shortcodes": [],
        "parse_errors": [],
        "all_results": [],
    }

    for i, filepath in enumerate(html_files):
        result = process_file(filepath)
        report["all_results"].append(result)

        if result["status"] == "converted":
            report["converted"] += 1
        else:
            report["errors"] += 1

        for issue in result["issues"]:
            t = issue["type"]
            entry = {"file": result["file"], "detail": issue["detail"]}
            if t == "flash_embed":
                report["flash_embeds"].append(entry)
            elif t == "missing_image":
                report["missing_images"].append(entry)
            elif t == "image_ref":
                report["existing_images"].append(entry)
            elif t == "external_image":
                report["external_images"].append(entry)
            elif t == "internal_link":
                report["internal_links"].append(entry)
            elif t == "wp_shortcode":
                report["wp_shortcodes"].append(entry)
            elif t == "parse_error":
                report["parse_errors"].append(entry)

        if (i + 1) % 25 == 0:
            print(f"  {i + 1}/{len(html_files)} processed...")

    # Write report
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"\nDone.")
    print(f"  Converted:      {report['converted']}")
    print(f"  Errors:         {report['errors']}")
    print(f"  Flash embeds:   {len(report['flash_embeds'])}")
    print(f"  Missing images: {len(report['missing_images'])}")
    print(f"  Existing imgs:  {len(report['existing_images'])}")
    print(f"  External imgs:  {len(report['external_images'])}")
    print(f"  Internal links: {len(report['internal_links'])}")
    print(f"  WP shortcodes:  {len(report['wp_shortcodes'])}")
    print(f"\nFull report: scripts/conversion_report.json")


if __name__ == "__main__":
    main()
