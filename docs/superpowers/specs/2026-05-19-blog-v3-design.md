# blog-v3 Design Spec

**Date:** 2026-05-19  
**Author:** Trinidad Martí  
**Purpose:** Static academic journal documenting an OSSU CS degree self-study (à la Scott Young's MIT Challenge)

---

## Overview

A hand-rolled static blog hosted on GitHub Pages. Posts authored in Markdown locally, built to HTML via a Python script, previewed locally, pushed to GitHub. No framework dependencies. Nothing-company-inspired monochrome dot-grid aesthetic.

---

## Stack

| Concern | Choice |
|---|---|
| Hosting | GitHub Pages (`/docs` folder or `gh-pages` branch) |
| Build | `build.py` — Python 3 |
| Markdown parsing | `markdown` lib + `python-frontmatter` |
| Syntax highlighting | `Pygments` (fenced code blocks) |
| Dev server | `python -m http.server` |
| File watching | `build.py --watch` (uses `watchdog`) |
| Styling | Hand-written CSS, no framework |

**Install:** `pip install markdown python-frontmatter pygments watchdog`

---

## Project Structure

```
blog-v3/
├── build.py               # build script
├── requirements.txt
├── templates/
│   ├── base.html          # shared shell (nav, dot-grid bg, CSS vars)
│   ├── index.html         # homepage template
│   ├── post.html          # post page template
│   └── curriculum.html    # curriculum map template
├── posts/
│   └── YYYY-MM-DD-slug.md # markdown source files
├── static/
│   ├── style.css
│   └── media/             # images, videos referenced in posts
├── data/
│   └── curriculum.json    # OSSU course list + completion % per course
├── _site/                 # build output (gitignored locally, pushed to Pages)
└── docs/
    └── superpowers/specs/
```

---

## Post Frontmatter

```yaml
---
title: "Memory & Pointers"
date: "2026-05-12"
course: "CS50x"
week: 4
tags: ["c", "memory"]
excerpt: "Stack vs heap. malloc returns a pointer to heap memory — caller owns it."
---
```

All fields required except `week` (optional for non-course posts).

**Slug**: derived from filename — `2026-05-12-memory-pointers.md` → `/posts/memory-pointers.html`

---

## Visual System

### Palette (monochrome only)

| Token | Value | Use |
|---|---|---|
| `--bg` | `#f5f5f0` | page background |
| `--dot` | `#cccccc` | dot grid color |
| `--ink` | `#111111` | primary text, borders |
| `--meta` | `#888888` | dates, labels, secondary text |
| `--muted` | `#dddddd` | dividers, progress bar bg |
| `--code-bg` | `#1a1a1a` | code block background |
| `--code-fg` | `#e0e0e0` | code block text |

### Typography

- **Font**: `'Courier New', Courier, monospace` — everything
- **Headings**: `font-weight: 900`, `letter-spacing: -0.01em`
- **Meta labels**: `font-size: 0.7rem`, `letter-spacing: 0.3em`, `text-transform: uppercase`
- **Body**: `font-size: 0.9rem`, `line-height: 1.8`

### Dot Grid

```css
background-color: var(--bg);
background-image: radial-gradient(circle, var(--dot) 1px, transparent 1px);
background-size: 16px 16px;
```

Content sits on a semi-transparent overlay (`rgba(245,245,240,0.93)`) so dots show through but readability is maintained.

### Rules

- No `border-radius` anywhere — sharp edges only
- No color other than monochrome
- All borders `1px solid` or `2px solid`, never thicker
- Tags: `border: 1px solid #333`, no background fill

---

## Pages

### Homepage (`/index.html`)

**Structure (top to bottom):**

1. **Nav** — `TRINIDAD.LOG` left, `FEED / CURRICULUM / ABOUT` right. `border-bottom: 2px solid #111`
2. **Status strip** — `border: 1px solid #222` box containing:
   - Left: "NOW STUDYING" label + current course + week
   - Center: "OVERALL PROGRESS" label + progress bar
   - Right: completion percentage (large, `font-weight: 900`)
3. **Two-column body** — `grid-template-columns: 200px 1fr`
   - **Left (curriculum sidebar)**: "CURRICULUM MAP" label, list of OSSU courses with mini progress bars. Active course bold, future courses muted
   - **Right (feed)**: "RECENT ENTRIES" label, chronological list of posts — date+course meta, title, excerpt

Progress % and course list driven by `data/curriculum.json`.

---

### Post Page (`/posts/slug.html`)

**Structure:**

1. **Nav** — same as homepage, with `← BACK TO FEED` right-aligned
2. **Post header**:
   - Meta line: `YYYY.MM.DD · COURSE · WEEK N`
   - Title: largest text on page, `font-weight: 900`
   - Tags: bordered pills
3. **Reading column**: `max-width: 680px`, centered, `margin: 0 auto`
   - Body text rendered from Markdown
   - Code blocks: dark background (`#1a1a1a`), Pygments syntax highlighting, language label top-right
   - Images: `max-width: 100%`, `border: 1px solid #ccc`
   - Videos: pass-through `<video>` tag, `max-width: 100%`
   - Auto-generated TOC for posts with 3+ `##` headings, rendered above body
4. **Footer nav**: `← prev post` / `next post →`

---

### Curriculum Page (`/curriculum.html`)

Full OSSU course list grouped by category (Intro CS, Core CS, Advanced CS). Each course shows:
- Course name + link to OSSU source
- Progress bar
- Count of posts tagged to that course
- Status badge: `NOT STARTED` / `IN PROGRESS` / `COMPLETE`

Data source: `data/curriculum.json`. Updated manually when completing courses.

**`curriculum.json` schema:**
```json
{
  "courses": [
    {
      "id": "cs50x",
      "name": "CS50x",
      "category": "Intro CS",
      "url": "https://cs50.harvard.edu/x/",
      "status": "in_progress",
      "progress": 70
    }
  ]
}
```
`status`: `"not_started"` | `"in_progress"` | `"complete"`. `progress`: 0–100 integer.

---

## Build Script (`build.py`)

**Normal build:**
```bash
python build.py
# reads posts/, templates/, data/ → writes _site/
```

**Watch + serve (dev):**
```bash
python build.py --watch
# watches source files, rebuilds on change
# starts http.server on localhost:8000
```

**Build steps:**
1. Clean `_site/`
2. Copy `static/` → `_site/static/`
3. Parse all `.md` in `posts/` via `python-frontmatter` + `markdown`
4. Render each post through `templates/post.html` → `_site/posts/slug.html`
5. Build post index (sorted by date desc) → render `templates/index.html` → `_site/index.html`
6. Load `data/curriculum.json` → render `templates/curriculum.html` → `_site/curriculum.html`

---

## GitHub Pages Deploy

Two options (pick at setup):

**Option 1 — `/docs` folder** (simpler): build outputs to `docs/` instead of `_site/`, committed alongside source. Pages serves from `main:/docs`.

**Option 2 — `gh-pages` branch** (cleaner): source on `main`, built output pushed to `gh-pages` branch. Keeps source and output separate.

Recommendation: **Option 1** to start — zero extra tooling, one branch, push and done.

---

## Content Authoring Workflow

```bash
# 1. Write post
touch posts/2026-05-19-slug.md   # add frontmatter + markdown

# 2. Preview
python build.py --watch          # open localhost:8000

# 3. Publish
python build.py
git add .
git commit -m "post: title here"
git push
```

---

## Out of Scope

- Comments system
- Search
- RSS feed (can add later)
- Dark mode toggle
- Math notation / LaTeX (can add later via KaTeX)
- About page (nav link present; static `about.html` written by hand, not generated — out of build scope)
