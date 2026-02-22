#!/usr/bin/env python3
"""
Inject Hugo youtube shortcodes into converted .md files.
Reads video IDs from the original .html files and inserts
{{< youtube VIDEO_ID >}} at the correct position in the .md.

For Viddler embeds (dead platform): inserts a placeholder comment.
"""

import re
from pathlib import Path

POST_DIR = Path(__file__).parent.parent / "content" / "post"

YOUTUBE_ID = re.compile(
    r'youtube\.com/(?:v|embed)/([a-zA-Z0-9_-]{11})'
    r'|youtu\.be/([a-zA-Z0-9_-]{11})'
    r'|youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})',
    re.IGNORECASE
)
VIDDLER_ID = re.compile(r'viddler\.com/player/([a-zA-Z0-9]+)/', re.IGNORECASE)

# Files with flash embeds (from conversion report)
FLASH_FILES = [
    "2010-11-05-brookline-tai-chis-collaboration-with-the-department-of-public-health",
    "2010-12-17-new-video-for-tai-chi-group",
    "2011-01-23-updating-your-energy-arts-instructor-profile",
    "2011-03-30-the-strange-link-between-eyes-and-movement",
    "2011-04-02-tai-chi-in-telluride",
    "2011-04-07-running-rhythm",
    "2011-05-21-follow-the-20-20-20-rule-for-better-breathing",
    "2011-05-26-disrupt-the-stress-cycle-with-better-breathing",
    "2011-06-02-standing-single-whip",
    "2011-06-20-gods-playing-in-the-clouds-at-brookline-tai-chi",
    "2011-07-06-how-to-treat-lower-back-pain",
    "2011-07-14-how-xingyi-saved-my-butt",
    "2011-07-25-how-does-qigong-work",
    "2011-07-26-what-im-learning-at-the-wu-tai-chi-instructor-training-2",
    "2011-07-30-week-2-of-the-short-form-instructor-training",
    "2011-08-01-how-do-i-sequence-my-practice-sets-for-qigong-and-tai-chi",
    "2011-08-05-week-3-update-from-the-beach",
    "2011-08-12-short-form-training-final-update",
    "2011-08-15-how-to-achieve-whole-body-relaxation",
    "2011-08-23-how-to-balance-practicing-multiple-qigong-sets",
    "2011-08-30-what-is-real-tai-chi",
    "2011-09-01-practice-twice-a-day",
    "2011-09-06-jack-white-on-the-value-of-a-form",
    "2011-09-08-learning-tai-chi-for-the-first-time",
    "2011-09-12-is-your-practice-all-in-your-head-2",
    "2011-10-17-4-practice-partners-you-should-avoid",
    "2011-10-24-why-circular-breathing-is-only-the-beginning",
    "2011-10-31-opening-the-energy-gates-by-bruce-frantzis-is-the-most-important-qigong-book-to-have-in-your-library",
    "2011-11-07-robert-tangora-on-the-importance-of-integration-in-tai-chi",
    "2011-11-14-a-doctor-a-runner-and-a-meditator-walk-into-a-bar",
    "2011-11-16-the-challenge-of-the-three-swings",
    "2011-11-28-youtube-qigong-videos",
    "2011-12-05-stress-reduction-techniques-that-work-in-5-minutes-or-less",
    "2011-12-06-whats-the-best-way-to-practice-sinking-the-chest-2",
    "2011-12-08-how-active-should-i-be-when-standing",
    "2011-12-19-z-health-exercises-for-stiff-joints-in-the-morning",
    "2011-12-21-case-study-energy-gates-tune-up",
    "2011-12-26-what-is-a-frozen-shoulder-anyway",
    "2012-01-04-guided-practice-aides",
    "2012-01-04-how-to-learn-absolutely-anything-in-2012",
    "2012-01-09-how-do-i-keep-my-awareness-for-jumping-around",
    "2012-01-23-learning-to-use-your-kwa-in-tai-chi",
    "2012-01-25-how-dr-mark-cheng-is-bringing-tai-chi-to-the-fitness-community-part-2",
    "2012-01-30-my-favorite-breathing-hack",
    "2012-02-04-2-subtle-causes-of-neck-pain-and-how-to-avoid-them",
    "2012-02-06-how-to-get-more-flexible-without-adding-stretching-to-your-practice",
    "2012-02-08-read-faster-move-better",
    "2012-02-13-twisting-through-the-legs",
    "2012-02-15-the-marriage-of-heaven-and-earth-qigong",
    "2012-02-20-turn-the-legs-to-turn-the-body",
    "2012-02-22-arm-swing-and-the-force-transmission-problem",
    "2012-03-05-making-more-space-inside-your-body",
    "2012-03-09-10000-views-on-youtube",
    "2012-03-14-what-i-learned-from-robert-tangora-about-spinal-qigong",
    "2012-03-19-why-you-should-not-worry-about-breathing-in-tai-chi",
    "2012-03-21-the-difference-between-breathing-in-yoga-and-tai-chi",
    "2012-03-28-push-hands-and-the-tai-chi-mastery-program",
    "2012-04-09-more-of-the-best-qigong-on-youtube",
    "2012-04-11-straight-lines-circles-and-spheres",
    "2012-06-01-bruce-frantzis",
    "2012-06-04-relaxing-your-eyes-in-tai-chi",
]


def extract_video_ids(html_content):
    """
    Return ordered list of (type, id) tuples from the HTML.
    type is 'youtube' or 'viddler'.
    Deduplicates while preserving order.
    """
    results = []
    seen = set()

    # Walk through the HTML finding embeds in document order
    # by scanning for object/embed tags
    # We find all youtube IDs in order
    for m in YOUTUBE_ID.finditer(html_content):
        vid_id = m.group(1) or m.group(2) or m.group(3)
        if vid_id and vid_id not in seen:
            seen.add(vid_id)
            results.append(('youtube', vid_id))

    for m in VIDDLER_ID.finditer(html_content):
        vid_id = m.group(1)
        key = f'viddler:{vid_id}'
        if key not in seen:
            seen.add(key)
            results.append(('viddler', vid_id))

    return results


def build_shortcode_block(videos):
    """Build the markdown block to append for all videos in a post."""
    lines = []
    for vtype, vid_id in videos:
        if vtype == 'youtube':
            lines.append(f'{{{{< youtube {vid_id} >}}}}')
        else:
            lines.append(
                f'<!-- VIDEO UNAVAILABLE: This video was hosted on Viddler '
                f'(player ID: {vid_id}), which is no longer active. '
                f'The video content has been lost. -->'
            )
    return '\n\n'.join(lines)


def process_file(slug):
    html_path = POST_DIR / f"{slug}.html"
    md_path = POST_DIR / f"{slug}.md"

    if not html_path.exists():
        return f"SKIP (no html): {slug}"
    if not md_path.exists():
        return f"SKIP (no md): {slug}"

    html_content = html_path.read_text(encoding="utf-8", errors="replace")
    md_content = md_path.read_text(encoding="utf-8")

    videos = extract_video_ids(html_content)
    if not videos:
        return f"NO_VIDEOS: {slug}"

    shortcode_block = build_shortcode_block(videos)

    # Append shortcodes at the end of the file
    new_content = md_content.rstrip() + '\n\n' + shortcode_block + '\n'
    md_path.write_text(new_content, encoding="utf-8")

    yt_count = sum(1 for t, _ in videos if t == 'youtube')
    vd_count = sum(1 for t, _ in videos if t == 'viddler')
    return f"OK ({yt_count} youtube, {vd_count} viddler): {slug}"


def main():
    results = {'ok': [], 'viddler': [], 'no_videos': [], 'skip': []}

    for slug in FLASH_FILES:
        result = process_file(slug)
        print(result)
        if result.startswith("OK"):
            if 'viddler' in result and '0 viddler' not in result:
                results['viddler'].append(slug)
            else:
                results['ok'].append(slug)
        elif result.startswith("NO_VIDEOS"):
            results['no_videos'].append(slug)
        else:
            results['skip'].append(slug)

    print(f"\nSummary:")
    print(f"  YouTube shortcodes injected: {len(results['ok'])}")
    print(f"  Viddler placeholders added:  {len(results['viddler'])}")
    print(f"  No video IDs found:          {len(results['no_videos'])}")
    print(f"  Skipped (missing files):     {len(results['skip'])}")

    if results['no_videos']:
        print(f"\nPosts with flash embed but no extractable video ID:")
        for s in results['no_videos']:
            print(f"  {s}")


if __name__ == "__main__":
    main()
