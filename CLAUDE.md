# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A static, hand-written HTML/CSS content site (English) about lake fishing in Japan, served at `myjapanfishing.com` via GitHub Pages (`CNAME`; repo `tomat-coding/fishing-web`, deployed from `main`). It is also the web companion and SEO funnel for the Android app "TsureruKana" (釣れるかな？, `com.tomat.fishingapp`); pages link to its Google Play listing. Use the name "TsureruKana" (as on the Play Store), including in the JSON-LD `publisher.name`.

There is no build system, package manager, JavaScript, linter or test suite. Every page is a standalone `.html` file at the repo root that shares a single `styles.css`. To preview, serve the root directory (e.g. `python3 -m http.server`) instead of opening files directly, because some links are root-relative (`/`, `/favicon.ico`).

`favicon.ico`, `favicon-16x16.png`, `favicon-32x32.png` and `logo.png` (the JSON-LD publisher logo) are resized copies of the app's Google Play icon. If the app icon changes, regenerate them.

GitHub Pages builds the site with its default Jekyll step. Any file that belongs only in the repo, like this one, must be listed under `exclude` in `_config.yml`, or it gets published.

`404.html` is served by GitHub Pages for any missing URL, so every link and asset in it uses a root-absolute path (`/styles.css`, `/lake-biwa-fishing.html`). It's `noindex` and isn't in the sitemap.

`google99ec3fbe524bd037.html` is the Google Search Console verification file. Don't edit or remove it.

## Project skills

`.claude/skills/` holds the content workflows: `plan-content` (what to write next), `write-article` (a new page end to end), `refresh-page` (re-verify seasonal facts and keep repeated lake facts in sync), `reader-review` (editorial pass from the reader's side) and `site-audit` (consistency checks). `python3 .claude/skills/site-audit/scripts/audit.py .` mechanically checks most rules in this file; run it after editing pages. Jekyll skips dot-folders, so `.claude/` isn't published.

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
- **`japan-fishing-forecast-app.html`** is the app's landing page, modeled on the Sugu Toire page of our toilet site (`toiletinjapan.com/sugu-toire.html`). It doesn't use the article skeleton: `body.lp-page`, a full-width `.lp-hero` with `.phone` mockups, then `.lp` sections (`.lp-stats`, `.ways`, `.features`, `.split`, `.lp-steps`, an `.lp-faq` accordion, the `.lp-cta` download card and `.lp-related` chips). Its JSON-LD `@graph` has `MobileApplication` (free, `offers.price` 0), `FAQPage` and `BreadcrumbList`, so keep the FAQ JSON-LD in step with the visible FAQ. The visible "Updated" line sits under the FAQ. App feature facts come from the app repo's `store/listing.md` (`~/AndroidStudioProjects/FishingApp/store/`), so check there before describing a feature.
- **`.app-note`** (the app CTA near the end of each page) is a two-column grid: an `.app-note-shot` screenshot, then `.app-note-body` with the page-specific text, the official Google Play badge (`.app-badge`, `images/google-play-badge.png`) and an `.app-note-more` line, "iPhone version coming soon · See everything the app does". Each page uses the screenshot that fits its topic (lures → `app-lures.webp`, moon phase → `app-feeding-windows.webp`, Saroma → `app-tide-table.webp`, and so on).
- Every Google Play link carries a referrer for install attribution: `&amp;referrer=utm_source%3Dmyjapanfishing%26utm_medium%3Dwebsite%26utm_campaign%3D<page slug>` (`home` for `index.html`, `app-page` for the app page).
- App images live in `images/app/`. `app-*.webp` are the store screenshots (with headlines) from the app repo's `store/out/en/*.png`, made with `cwebp -q 80 -resize 540 960`, and are used in the `.app-note` boxes. `screen-*.webp` are the plain screens from `store/raw/en/*.png`, made with `cwebp -q 80 -resize 600 1333`, and are used in the app page's phone mockups. The `catch_log` screenshot is blank in both folders, so it isn't used. When the store screenshots change, regenerate them.
- `.related` ("Keep reading") lists are curated to about five of the most relevant pages. They don't list every article.
- Reusable content components defined in `styles.css`: `.info-box` (plus the `.info-box--teal` variant) with `.info-label`, `.tip`, `.season-box`, `.lake-section`/`.lake-rank`/`.lake-meta`, `.phrase-box`/`.phrase-item` (`.phrase-jp`, `.phrase-romaji`, `.phrase-meaning`), and `.group-box`/`.group-item` (`.item-name`, `.item-tag`, `.item-desc`, `.item-image`).

## Japanese version (`/ja/`)

The Japanese pages are for local hobby anglers (Lake Biwa first), not tourists. They're reference guides that readers come back to before each trip (rules, seasons, timing, conditions), and they lead on to the app. They're written in Japanese for that reader, not translated, so content that only makes sense for foreigners (phrase boxes, the manners and phrases page, getting a permit without speaking Japanese) is left out. Writing guidance is in `.claude/skills/write-article/references/japanese.md`.

- Files live in `ja/` and keep the English filename when there's an English counterpart (`ja/lake-biwa-fishing.html`). A page may exist in only one language.
- `<html lang="ja">`, `og:locale` = `ja_JP`, and `"inLanguage": "ja"` on the JSON-LD `Article`. URLs are `https://myjapanfishing.com/ja/<file>`, and `ja/index.html` is `https://myjapanfishing.com/ja/`. Breadcrumb names are in Japanese, and the author and publisher are unchanged.
- Every link and asset in a `/ja/` page uses a root-absolute path (`/styles.css`, `/images/app/…`, `/ja/lake-biwa-fishing.html`), like `404.html`.
- **hreflang:** a page with a counterpart has `<link rel="alternate" hreflang="en|ja|x-default" href="…">` in both languages' `<head>`, with `x-default` pointing to the English URL. A page without a counterpart has none.
- **Language switch:** the header has `<a class="lang-switch">` linking to the counterpart ("日本語" on English pages, "English" on Japanese ones), or to the other language's home page when there's no counterpart.
- **Fonts:** the Google Fonts `<link>` on `/ja/` pages adds `Noto+Sans+JP:wght@400;500;700`, and `:lang(ja)` rules in `styles.css` switch text to it. Add those rules along with the first `/ja/` page.
- **Lengths:** the `<title>` (`… | My Japan Fishing`) is about 35 characters, and the meta description about 120, because Google shows fewer Japanese characters.
- **Google Play links** add `&amp;hl=ja` and use `utm_source%3Dmyjapanfishing-ja` with the usual campaign slugs.
- **The app** is 『釣れるかな？』 in Japanese copy, with feature names taken from the "Japanese (ja-JP)" section of the app repo's `store/listing.md`. The JSON-LD publisher stays "TsureruKana". App screenshots go in `images/app/ja/`, made from `store/out/ja/` and `store/raw/ja/` with the same `cwebp` settings as the English ones.
- `/ja/` pages go in `sitemap.xml`, get their own `.post-card` in `ja/index.html` and have their own `.related` lists of Japanese pages.
- When a fact appears in both languages, change it in both.

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
