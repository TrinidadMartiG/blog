#!/usr/bin/env python3
"""Static site builder for blog-v3."""

import re
import os
import sys
import json
import shutil
import argparse
from datetime import datetime
from pathlib import Path

import frontmatter
import markdown
from jinja2 import Environment, FileSystemLoader


ROOT         = Path(__file__).parent
POSTS_DIR    = ROOT / "posts"
TEMPLATES_DIR= ROOT / "templates"
STATIC_DIR   = ROOT / "static"
DATA_DIR     = ROOT / "data"
OUTPUT_DIR   = ROOT / "_site"

_md = markdown.Markdown(
    extensions=["fenced_code", "codehilite", "tables", "toc"],
    extension_configs={
        "codehilite": {"css_class": "highlight", "guess_lang": False},
        "toc": {"permalink": False},
    },
)


# ── Core ──────────────────────────────────────────────────────

def derive_slug(filename: str) -> str:
    """'2026-05-12-memory-pointers.md' → 'memory-pointers'"""
    name = Path(filename).stem
    return re.sub(r"^\d{4}-\d{2}-\d{2}-", "", name)


def parse_post(filepath: str) -> dict:
    post = frontmatter.load(filepath)
    _md.reset()
    content = _md.convert(post.content)
    date_str = str(post.metadata["date"])
    date_fmt = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y.%m.%d")
    return {
        "title":    post.metadata["title"],
        "date":     date_str,
        "date_fmt": date_fmt,
        "course":   post.metadata["course"],
        "week":     post.metadata.get("week"),
        "tags":     post.metadata.get("tags", []),
        "excerpt":  post.metadata["excerpt"],
        "slug":     derive_slug(Path(filepath).name),
        "content":  content,
    }


def extract_toc(html: str) -> list:
    matches = re.findall(r'<h2[^>]*id=["\']([^"\']+)["\'][^>]*>(.*?)</h2>', html, re.IGNORECASE)
    if len(matches) < 3:
        return []
    return [{"anchor": a, "text": re.sub(r"<[^>]+>", "", t)} for a, t in matches]


# ── Pipeline ──────────────────────────────────────────────────

def load_curriculum() -> list:
    with open(DATA_DIR / "curriculum.json") as f:
        return json.load(f)["courses"]


def compute_stats(courses: list) -> dict:
    total     = len(courses)
    completed = sum(1 for c in courses if c["status"] == "complete")
    overall   = round(sum(c["progress"] for c in courses) / total) if total else 0
    return {"overall_pct": overall, "completed_courses": completed, "total_courses": total}


def _jinja_env() -> Environment:
    return Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))


def _get_current_course(courses: list) -> dict:
    for c in courses:
        if c["status"] == "in_progress":
            return c
    return courses[0]


def _latest_week(posts: list, course_name: str) -> int:
    weeks = [p["week"] for p in posts if p["course"] == course_name and p["week"]]
    return max(weeks) if weeks else 1


def build_all():
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)
    (OUTPUT_DIR / "posts").mkdir()

    if STATIC_DIR.exists():
        shutil.copytree(STATIC_DIR, OUTPUT_DIR / "static")

    # copy about.html if present
    about_src = ROOT / "about.html"
    if about_src.exists():
        shutil.copy(about_src, OUTPUT_DIR / "about.html")

    md_files = sorted(POSTS_DIR.glob("*.md"), reverse=True)
    posts = [parse_post(str(f)) for f in md_files if not f.name.startswith(".")]

    courses = load_curriculum()
    stats   = compute_stats(courses)
    current = _get_current_course(courses)

    post_counts: dict = {}
    for p in posts:
        post_counts[p["course"]] = post_counts.get(p["course"], 0) + 1
    for c in courses:
        c["post_count"] = post_counts.get(c["name"], 0)

    categories: dict = {}
    for c in courses:
        categories.setdefault(c["category"], []).append(c)

    env = _jinja_env()

    post_tmpl = env.get_template("post.html")
    for i, post in enumerate(posts):
        toc       = extract_toc(post["content"])
        prev_post = posts[i + 1] if i + 1 < len(posts) else None
        next_post = posts[i - 1] if i > 0 else None
        html = post_tmpl.render(
            post=post, toc=toc,
            prev_post=prev_post, next_post=next_post,
            root="../", static_root="../static/",
        )
        (OUTPUT_DIR / "posts" / f"{post['slug']}.html").write_text(html)

    index_tmpl = env.get_template("index.html")
    html = index_tmpl.render(
        posts=posts,
        sidebar_courses=courses,
        current_course=current["name"],
        current_week=_latest_week(posts, current["name"]),
        root="", static_root="static/",
        **stats,
    )
    (OUTPUT_DIR / "index.html").write_text(html)

    curr_tmpl = env.get_template("curriculum.html")
    html = curr_tmpl.render(
        categories=categories, root="", static_root="static/", **stats,
    )
    (OUTPUT_DIR / "curriculum.html").write_text(html)

    print(f"Built {len(posts)} post(s) → {OUTPUT_DIR}")


# ── Watch + Serve ─────────────────────────────────────────────

def watch_and_serve(port: int = 8000):
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    import http.server

    build_all()

    class RebuildHandler(FileSystemEventHandler):
        def on_any_event(self, event):
            if event.is_directory:
                return
            if any(event.src_path.endswith(ext) for ext in (".md", ".html", ".css", ".json")):
                print(f"Changed: {Path(event.src_path).name} — rebuilding…")
                try:
                    build_all()
                except Exception as e:
                    print(f"Build error: {e}")

    observer = Observer()
    for watch_dir in [POSTS_DIR, TEMPLATES_DIR, STATIC_DIR, DATA_DIR]:
        if watch_dir.exists():
            observer.schedule(RebuildHandler(), str(watch_dir), recursive=True)
    observer.start()
    print(f"Watching for changes. Serving at http://localhost:{port}")

    os.chdir(OUTPUT_DIR)
    handler = http.server.SimpleHTTPRequestHandler
    handler.log_message = lambda *a: None
    httpd = http.server.HTTPServer(("", port), handler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


# ── Publish ───────────────────────────────────────────────────

def publish():
    build_all()
    docs_dir = ROOT / "docs"

    if docs_dir.exists():
        for item in docs_dir.iterdir():
            if item.name == "superpowers":
                continue
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
    docs_dir.mkdir(exist_ok=True)

    for item in OUTPUT_DIR.iterdir():
        dest = docs_dir / item.name
        if item.is_dir():
            shutil.copytree(str(item), str(dest))
        else:
            shutil.copy2(str(item), str(dest))

    (docs_dir / ".nojekyll").touch()
    print(f"Published → {docs_dir}")


# ── CLI ───────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="blog-v3 builder")
    parser.add_argument("--watch",   action="store_true", help="watch + serve locally")
    parser.add_argument("--publish", action="store_true", help="build + copy to docs/ for GitHub Pages")
    parser.add_argument("--port",    type=int, default=8000)
    args = parser.parse_args()

    if args.publish:
        publish()
        sys.exit(0)
    elif args.watch:
        watch_and_serve(args.port)
    else:
        build_all()
