import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
import textwrap
from build import derive_slug, parse_post, extract_toc


def test_derive_slug_strips_date():
    assert derive_slug("2026-05-12-memory-pointers.md") == "memory-pointers"

def test_derive_slug_no_date():
    assert derive_slug("hello-world.md") == "hello-world"

def test_derive_slug_strips_extension():
    assert derive_slug("2026-01-01-foo.md") == "foo"


def test_parse_post_returns_required_fields(tmp_path):
    p = tmp_path / "2026-05-12-test-post.md"
    p.write_text(textwrap.dedent("""\
        ---
        title: "Test Post"
        date: "2026-05-12"
        course: "CS50x"
        week: 4
        tags: ["c", "memory"]
        excerpt: "A test post."
        ---
        ## Hello

        World.
    """))
    post = parse_post(str(p))
    assert post["title"] == "Test Post"
    assert post["date"] == "2026-05-12"
    assert post["course"] == "CS50x"
    assert post["week"] == 4
    assert post["tags"] == ["c", "memory"]
    assert post["excerpt"] == "A test post."
    assert post["slug"] == "test-post"
    assert "<h2" in post["content"]
    assert post["date_fmt"] == "2026.05.12"


def test_parse_post_week_optional(tmp_path):
    p = tmp_path / "2026-05-12-no-week.md"
    p.write_text(textwrap.dedent("""\
        ---
        title: "No Week"
        date: "2026-05-12"
        course: "General"
        tags: []
        excerpt: "No week field."
        ---
        Content here.
    """))
    post = parse_post(str(p))
    assert post["week"] is None


def test_extract_toc_returns_empty_for_few_headings():
    html = "<p>Hello</p><h2 id='a'>One</h2>"
    assert extract_toc(html) == []


def test_extract_toc_returns_items_for_three_or_more():
    html = (
        '<h2 id="intro">Intro</h2>'
        '<h2 id="body">Body</h2>'
        '<h2 id="conclusion">Conclusion</h2>'
    )
    toc = extract_toc(html)
    assert len(toc) == 3
    assert toc[0] == {"anchor": "intro", "text": "Intro"}
    assert toc[2] == {"anchor": "conclusion", "text": "Conclusion"}


# ── Pipeline tests (added in Task 6) ────────────────────────
from build import load_curriculum, compute_stats, build_all


def test_load_curriculum_returns_list():
    courses = load_curriculum()
    assert isinstance(courses, list)
    assert len(courses) > 0
    assert "id" in courses[0]
    assert "name" in courses[0]
    assert "category" in courses[0]
    assert "status" in courses[0]
    assert "progress" in courses[0]


def test_compute_stats_overall_pct():
    courses = [
        {"progress": 100, "status": "complete"},
        {"progress": 0, "status": "not_started"},
        {"progress": 0, "status": "not_started"},
        {"progress": 0, "status": "not_started"},
    ]
    stats = compute_stats(courses)
    assert stats["overall_pct"] == 25
    assert stats["completed_courses"] == 1
    assert stats["total_courses"] == 4


def test_build_all_creates_output_files(tmp_path, monkeypatch):
    import build as b
    monkeypatch.setattr(b, "OUTPUT_DIR", tmp_path / "_site")
    monkeypatch.setattr(b, "POSTS_DIR", tmp_path / "posts")

    posts_dir = tmp_path / "posts"
    posts_dir.mkdir()
    (posts_dir / "2026-05-19-hello-world.md").write_text(
        "---\ntitle: Hello World\ndate: '2026-05-19'\ncourse: CS50x\nweek: 1\ntags: []\nexcerpt: First post.\n---\nHello!"
    )
    build_all()
    assert (tmp_path / "_site" / "index.html").exists()
    assert (tmp_path / "_site" / "posts" / "hello-world.html").exists()
    assert (tmp_path / "_site" / "curriculum.html").exists()
