# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A static, hand-written HTML/CSS content site (English) about lake fishing in Japan, served at `myjapanfishing.com` via GitHub Pages (`CNAME`; repo `tomat-coding/fishing-web`, deployed from `main`). It is also the web companion and SEO funnel for the Android app "Tsurerukana?" (`com.tomat.fishingapp`); pages link to its Google Play listing.

There is no build system, package manager, JavaScript, linter or test suite. Every page is a standalone `.html` file at the repo root that shares a single `styles.css`. To preview, serve the root directory (e.g. `python3 -m http.server`) instead of opening files directly, because some links are root-relative (`/`, `/favicon.ico`).

`favicon.ico`, `favicon-16x16.png`, `favicon-32x32.png` and `logo.png` (the JSON-LD publisher logo) are resized copies of the app's Google Play icon. If the app icon changes, regenerate them.

`google99ec3fbe524bd037.html` is the Google Search Console verification file. Don't edit or remove it.

## Page structure

- **`index.html`** is the home page. It has a `.hero`, `.intro`, one `.post-card` per article, a `.deep-dive` summary section and an `.app-note`. It is the only page with JSON-LD (`WebSite` schema) and the `android-app://` alternate link.
- **Article pages** (`*-japan.html`, `*-fishing.html`, etc.) all use the same skeleton. When adding one, copy an existing article instead of starting from scratch:
  - A `<head>` with `title` (`<Article Title> | My Japan Fishing`), `description`, `keywords`, `canonical`, Open Graph tags (`og:type` = `article`) and Twitter card tags. The OG/Twitter images reuse the hero's Unsplash URL at `w=1200`.
  - `header` (logo links to `index.html`), then `.page-hero` with `.back-link`, `h1` and a subtitle.
  - `.container > article` holding `.intro`, then a `.toc` whose anchors match the `id`s on each `.content-section`, then the content sections, then `.app-note`, then `.related` ("Keep reading" links to the other articles).
  - The same `footer` on every page.
- Reusable content components defined in `styles.css`: `.info-box` (plus the `.info-box--teal` variant) with `.info-label`, `.tip`, `.season-box`, `.lake-section`/`.lake-rank`/`.lake-meta`, `.phrase-box`/`.phrase-item` (`.phrase-jp`, `.phrase-romaji`, `.phrase-meaning`), and `.group-box`/`.group-item` (`.item-name`, `.item-tag`, `.item-desc`, `.item-image`).

## Adding or renaming an article touches several files

There are no templates or includes, so shared content is duplicated by hand:
1. Create the page, and make its `canonical`/`og:url` match the actual filename.
2. Add a `.post-card` for it in `index.html`.
3. Add it to the `.related` list on every other article page.
4. Header, footer and `.app-note` changes must be repeated on every page.

## Styling

- All styles live in `styles.css`. Colors are CSS custom properties on `:root` (`--deep-sea`, `--tide-teal`, `--dawn-amber`, `--foam`, `--ink`, `--ink-soft`, `--line`, …), so use those variables rather than hard-coded hex values.
- Fonts come from a Google Fonts `@import` at the top of `styles.css`: Zilla Slab for display/headings, Inter for body text, and JetBrains Mono for small labels and eyebrows.
- There is one responsive breakpoint: `@media (max-width: 650px)`.

## Content conventions

- The site covers exactly six lakes: Biwa, Kasumigaura, Saroma, Ogawara, Inawashiro and Suwa. The copy is deliberately factual and hedged. For example, solunar/moon-phase theory is presented as a heuristic to check "alongside the weather, not instead of it", not as a guarantee. Keep that tone and don't overclaim.
- Hero and thumbnail photos are hotlinked from Unsplash with `?auto=format&fit=crop&q=80&w=<size>` (1600 for the home hero, 1400 for article heroes, 400 for card thumbnails, 1200 for social images). Local images go in `images/`.
- Escape `&` as `&amp;` in HTML text and attributes.
