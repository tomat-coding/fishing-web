---
name: site-audit
description: Audit myjapanfishing.com for broken consistency between pages — title/description length, canonical and og:url, JSON-LD vs. visible dates, sitemap lastmod, TOC anchors, image attributes, broken local links, Google Play referrers, index cards, "Keep reading" lists, the app page FAQ, and the Japanese pages in /ja/ (hreflang pairs, language switch, lang/locale, Play hl=ja). Use this whenever the user asks to check, audit, validate, lint or "make sure everything is right" on the site, before they commit or push a batch of edits, after adding/renaming/editing any page, or when Search Console reports indexing or structured-data problems — even if they don't say "audit".
---

# Site audit

The site has no build step, so every rule in CLAUDE.md is kept by hand and drifts easily: a date bumped in the JSON-LD but not in the visible "Updated" line, a new page missing from `sitemap.xml`, a TOC link to a renamed section. This skill catches that drift mechanically first, then looks at the things a script can't judge.

## 1. Run the checker

```bash
python3 .claude/skills/site-audit/scripts/audit.py .
```

Add `--page lake-biwa-fishing.html` (one or more files) to check only what was just edited. It exits 1 when there are errors.

What it checks, so you know what it does *not* cover:
- `<title>` about 60 chars and ending `| My Japan Fishing`; meta description about 155.
- `canonical` and `og:url` equal the apex URL for the filename; no `www.` anywhere.
- JSON-LD parses; `publisher.name` is `TsureruKana`; the Article `description` equals the meta description; `mainEntityOfPage` and the last breadcrumb point at the page; lake guides have the 3-step breadcrumb.
- Visible `Updated <time datetime>` equals `dateModified`; `sitemap.xml` lists the page with a `lastmod` no older than it; the sitemap lists no missing pages.
- Every `.toc` anchor has a matching `id`; every `.content-section` is in the TOC.
- Non-hero images have `width`, `height` and `loading="lazy"`; article heroes use `w=1400`.
- Local `href`/`src` targets (and `page.html#anchor` links) exist.
- Google Play links carry the referrer with the right `utm_campaign` slug (`home`, `app-page`, or the filename without `.html`).
- Articles have an `.app-note` and a `.related` list of about five pages that doesn't link to itself.
- `&` followed by a space anywhere outside scripts (should be `&amp;`).
- Every article has its own hero photo (only its English/Japanese counterpart may share it), and the cards on each home page all use different thumbnails.
- `index.html` and `ja/index.html` each have a `.post-card` for every page in their language; the app page's FAQPage JSON-LD matches the visible `<details>` FAQ.
- **Japanese pages (`ja/`)**: `lang="ja"`, `og:locale` `ja_JP`, `"inLanguage": "ja"`, Noto Sans JP loaded, root-absolute paths only, home links to `/ja/` not `/`, shorter title (~35) and description (~120) limits, Play links with `hl=ja` and `utm_source=myjapanfishing-ja`, breadcrumbs starting at `/ja/`, and `.related` lists staying in one language.
- **hreflang pairs**: when `X.html` and `ja/X.html` both exist, both carry `en`, `ja` and `x-default` (English) alternates, and their `.lang-switch` links point at each other. A page with no counterpart has no hreflang and its switch goes to the other language's home page. Once `ja/` exists, every page is expected to have a `.lang-switch`.

## 2. Look at what the script can't judge

Read the flagged pages, and also check by eye:
- **Lake facts in sync.** If a lake guide changed, compare its prices, seasons and rules with the hub section in `japans-lakes-for-fishing.html`, the lake's section in `lake-fishing-license-japan.html`, the `index.html` deep-dive, and the same facts in `ja/` (`grep -rn '<price or date>' *.html ja/`). Contradictions between pages, or between the English and Japanese version of a page, hurt reader trust more than any SEO slip.
- **Japanese copy quality** on `ja/` pages: natural Japanese, the terms and app feature names in `.claude/skills/write-article/references/japanese.md`, and no content meant only for foreign visitors.
- **Social images** reuse the hero photo at `w=1200`.
- **Header, footer and `.app-note` wording** match the other pages (CLAUDE.md step 5). A quick `grep -c` of a footer sentence across `*.html` shows strays.
- **The `.app-note` screenshot fits the topic** (lures → `app-lures.webp`, moon phase → `app-feeding-windows.webp`, tides → `app-tide-table.webp`).
- **Hard-coded hex colours** in `styles.css` outside `:root` (`grep -n '#[0-9a-fA-F]\{3,6\}' styles.css`), which should be custom properties.
- **Files that shouldn't be published**: anything repo-only must be in `_config.yml` `exclude` (dot-folders like `.claude/` are skipped by Jekyll already).

## 3. Report

Group findings as **Must fix** (errors, broken links, contradictory facts), **Should fix** (warnings, SEO length issues) and **Nice to have**. For each, give the file and line and the concrete fix. Then offer to apply the fixes. When you fix, bump `dateModified`, the visible "Updated" line and the sitemap `lastmod` only if page *content* changed, not for markup-only fixes; then rerun the script until it's clean.

Leave changes uncommitted; the user commits and pushes themselves.
