# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A static, hand-written HTML/CSS content site (English) about lake fishing in Japan, served at `myjapanfishing.com` via GitHub Pages (`CNAME`; repo `tomat-coding/fishing-web`, deployed from `main`). It is also the web companion and SEO funnel for the Android app "Tsurerukana?" (`com.tomat.fishingapp`); pages link to its Google Play listing.

There is no build system, package manager, JavaScript, linter or test suite. Every page is a standalone `.html` file at the repo root that shares a single `styles.css`. To preview, serve the root directory (e.g. `python3 -m http.server`) instead of opening files directly, because some links are root-relative (`/`, `/favicon.ico`).

`favicon.ico`, `favicon-16x16.png`, `favicon-32x32.png` and `logo.png` (the JSON-LD publisher logo) are resized copies of the app's Google Play icon. If the app icon changes, regenerate them.

GitHub Pages builds the site with its default Jekyll step. Any file that belongs only in the repo, like this one, must be listed under `exclude` in `_config.yml`, or it gets published.

`404.html` is served by GitHub Pages for any missing URL, so every link and asset in it uses a root-absolute path (`/styles.css`, `/lake-biwa-fishing.html`). It's `noindex` and isn't in the sitemap.

`google99ec3fbe524bd037.html` is the Google Search Console verification file. Don't edit or remove it.

## Page structure

- **`index.html`** is the home page. It has a `.hero`, `.intro`, one `.post-card` per article, a `.deep-dive` summary section and an `.app-note`. Its JSON-LD uses the `WebSite` schema.
- **Article pages** (`*-japan.html`, `*-fishing.html`, etc.) all use the same skeleton. When adding one, copy an existing article instead of starting from scratch:
  - A `<head>` with `title`, `description`, `canonical`, Open Graph tags (`og:type` = `article`), Twitter card tags, the Google Fonts `<link>`, and a JSON-LD `@graph` containing an `Article` and a `BreadcrumbList`. The `Article` has `datePublished` and `dateModified`, so bump `dateModified` whenever you edit the content. The OG/Twitter images reuse the hero's Unsplash URL at `w=1200`.
  - The `<title>` targets search queries (`<Keyword-led title> | My Japan Fishing`) and is kept to about 60 characters, since Google truncates anything longer. The meta description is kept to about 155 characters, and the Article JSON-LD `description` matches it. The `h1`, `og:title` and card titles can keep the site's voice instead.
  - Under the hero subtitle, a `<p class="page-updated">Updated <time datetime="…">…</time></p>` line shows the same date as the JSON-LD `dateModified`. Update both together.
  - `header` (the logo links to `/`), then `.page-hero` with `.back-link`, `h1` and a subtitle. The hero `<img>` has `fetchpriority="high"`. Other images get `loading="lazy"` plus `width`/`height` attributes.
  - `.container > article` holding `.intro`, then a `.toc` whose anchors match the `id`s on each `.content-section`, then the content sections, then `.app-note`, then `.related` ("Keep reading" links to the other articles).
  - The same `footer` on every page.
- **Lake guides** (`lake-<name>-fishing.html`, and `lake-suwa-wakasagi-fishing.html`) each cover one lake. `japans-lakes-for-fishing.html` is the hub that summarizes all six and links to each guide. Their breadcrumb JSON-LD goes Home → The Six Lakes We Cover → the lake guide. When a fact about a lake changes, update the guide, the hub section, the lake's section in `lake-fishing-license-japan.html`, and the `index.html` deep-dive together, because they repeat each other.
- `.related` ("Keep reading") lists are curated to about five of the most relevant pages. They don't list every article.
- Reusable content components defined in `styles.css`: `.info-box` (plus the `.info-box--teal` variant) with `.info-label`, `.tip`, `.season-box`, `.lake-section`/`.lake-rank`/`.lake-meta`, `.phrase-box`/`.phrase-item` (`.phrase-jp`, `.phrase-romaji`, `.phrase-meaning`), and `.group-box`/`.group-item` (`.item-name`, `.item-tag`, `.item-desc`, `.item-image`).

## Adding or renaming an article touches several files

There are no templates or includes, so shared content is duplicated by hand:
1. Create the page. Its `canonical`, `og:url` and JSON-LD URLs must match the filename on the apex domain `https://myjapanfishing.com/`. `www.` 301-redirects there, so never use it in URLs.
2. Add a `.post-card` for it in `index.html`.
3. Add it to the `.related` list on every other article page.
4. Add it to `sitemap.xml`, and update `<lastmod>` there whenever a page changes.
5. Header, footer and `.app-note` changes must be repeated on every page.

## Styling

- All styles live in `styles.css`. Colors are CSS custom properties on `:root` (`--deep-sea`, `--tide-teal`, `--dawn-amber`, `--foam`, `--ink`, `--ink-soft`, `--line`, …), so use those variables rather than hard-coded hex values.
- Fonts come from a Google Fonts `<link>` in each page's `<head>`. Don't use `@import` in the CSS, because it delays loading. The fonts are Zilla Slab for display/headings, Inter for body text, and JetBrains Mono for small labels and eyebrows.
- There is one responsive breakpoint: `@media (max-width: 650px)`.

## Content conventions

- The site covers exactly six lakes: Biwa, Kasumigaura, Saroma, Ogawara, Inawashiro and Suwa. The copy is deliberately factual and hedged. For example, solunar/moon-phase theory is presented as a heuristic to check "alongside the weather, not instead of it", not as a guarantee. Keep that tone and don't overclaim.
- Hero and thumbnail photos are hotlinked from Unsplash with `?auto=format&fit=crop&q=80&w=<size>` (1600 for the home hero, 1400 for article heroes, 400 for card thumbnails, 1200 for social images). Local images go in `images/` as WebP, resized to what's displayed (for example with `cwebp -q 80 -resize`), with their real `width`/`height` in the `<img>`.
- Escape `&` as `&amp;` in HTML text and attributes.
