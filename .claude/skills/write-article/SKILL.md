---
name: write-article
description: Plan, research, write and publish a new article on myjapanfishing.com end to end — search intent and outline, fact research from official Japanese sources, the HTML page in the site's article skeleton, and every file a new page touches (index card, "Keep reading" lists, sitemap, lake hub, hreflang pairs). Works for both the English site and the Japanese pages in /ja/ for local anglers. Use this whenever the user wants a new page, guide, post or article on the site in either language, or a Japanese version of an existing page (e.g. "write a page about fishing near Tokyo", "add a month-by-month calendar", "a guide for tourists"), or wants to turn an idea or notes into an article, even if they only give a topic.
---

# Write a new article

A new page only helps if it answers a real question better than what's already ranking, and if it's wired into the rest of the site so readers and Google can find it. Work through these stages and check in with the user at the two marked points; everything else you can decide from CLAUDE.md and the existing pages.

## 0. Which language?

English pages are for foreign visitors and residents; Japanese pages (`ja/`) are for local hobby anglers who come back to check rules, seasons and timing before each trip. For a Japanese page, read `references/japanese.md` now and follow it throughout, together with the "Japanese version" section of CLAUDE.md. A Japanese page about a topic that already exists in English is written fresh for the local reader, not translated, and it reuses the English filename so the two pair up.

## 1. Pin down the reader and the query

- Who searches for this and what do they need to walk away with? Write it as one sentence: *"A visitor staying in Kyoto who wants a half-day of lake fishing and needs to know where, how to get there, and whether they need a license."*
- What's the main search query and two or three variants (in Japanese for `ja/` pages, e.g. 琵琶湖 バス リリース禁止, 琵琶湖 冬 バス 釣り方)? Check what currently ranks (WebSearch) and note what those pages miss: outdated prices, no English, no practical access info, no rules. That gap is the article's reason to exist.
- Does an existing page already cover it? If so, propose expanding that page instead (use the reader-review skill) — two thin pages on one topic compete with each other.
- Remember the site's scope: exactly six lakes (Biwa, Kasumigaura, Saroma, Ogawara, Inawashiro, Suwa) plus topics around them. A new article should connect back to those lakes; don't quietly add a seventh lake without asking.

## 2. Outline → **check in with the user**

Propose: filename (`<keyword-led-slug>.html`, lowercase, hyphens), `<title>` (~60 chars, `… | My Japan Fishing`), meta description (~155 chars), `h1` in the site's voice, and the TOC sections with one line each on what they answer. Mark which facts still need research. Wait for the user's OK or edits before writing.

## 3. Research the facts

- Prefer primary sources: the fisheries cooperative (漁協), prefecture or city pages, the tourism board, the operator's own site. Search in Japanese as well as English (e.g. `琵琶湖 遊漁券 料金`, `ワカサギ 解禁 2026`); the Japanese pages are usually more current.
- Write down each fact with its source URL and the year it applies to. Prices, seasons, hours and rules change yearly, so say which season a fact is for ("the 2026 details").
- If two sources disagree, or the only source is old, say so in the copy or leave it out. Never fill a gap with a plausible guess.
- App facts come from `~/AndroidStudioProjects/FishingApp/store/listing.md`, not memory.
- Facts that already appear on another page (a lake's permit price, say) must agree with that page; if your research shows the other page is out of date, tell the user and fix both.

## 4. Write the page

For a Japanese page, copy the closest existing `ja/` article if there is one; otherwise start from the English article and convert it (`lang="ja"`, root-absolute paths, `og:locale`, `inLanguage`, Noto Sans JP, Japanese breadcrumbs, `hl=ja` and the `-ja` referrer, Japanese footer and app note). For an English page, copy the closest existing article as the starting file (a lake guide for lake topics, `lake-fishing-license-japan.html` or `moon-phase-fishing-japan.html` for cross-lake topics) and replace its content. Keep the skeleton exactly as CLAUDE.md describes: head meta + OG/Twitter + fonts + JSON-LD `@graph` (Article + BreadcrumbList), header, `.page-hero` with `fetchpriority="high"` hero, subtitle and `page-updated` line, `.intro`, `.toc`, `.content-section`s with matching `id`s, a closing `.tip`, `.app-note`, `.related`, footer.

Writing guidance:
- Lead with the answer. The intro should tell the reader what this page will let them do and the single most important thing to know.
- Use the site's components where they fit the content, not for decoration: `.lake-meta` for numbers, `.info-box` for "check before you go" and the "Sources" box, `.tip` for one-line advice, `.season-box` for timing, `.phrase-box` for the Japanese the reader will need in that situation, `.group-box` for species or gear lists.
- Every page gets a **Sources** `.info-box` linking the official pages used, with a note that dates and fees change.
- Voice: factual, warm, hedged; never promise fish; moon phase and the app are checked "alongside the weather, not instead of it". Short paragraphs that read well on a phone.
- The `.app-note` text is specific to the page's topic, uses the matching screenshot from `images/app/app-*.webp`, and the Play link's referrer uses `utm_campaign%3D<filename-without-.html>`.
- Hero image: a real Unsplash photo that actually shows what the alt text says (open the photo page to confirm). Hotlink with `?auto=format&fit=crop&q=80&w=1400`, and `w=1200` for `og:image`/`twitter:image`. If no fitting photo exists, say so and ask whether to use a stand-in or wait for the user's own photo.
- Dates: `datePublished` = `dateModified` = today; the visible "Updated" line shows the same date. Escape `&` as `&amp;`.

## 5. Wire it into the site

1. `index.html`: add a `.post-card` (thumbnail at `w=400`) in a sensible position, and update the `.deep-dive` if the topic belongs there.
2. `.related` lists: add the new page to the "Keep reading" list of the pages where it's genuinely one of the ~5 most relevant next reads (replace a weaker link rather than growing the list), and give the new page its own curated list of about five.
3. `sitemap.xml`: add the URL with today's `lastmod`, and bump `lastmod` on every page you touched.
4. Lake guides only: add the lake to the hub (`japans-lakes-for-fishing.html`), its section in `lake-fishing-license-japan.html`, and use the Home → The Six Lakes We Cover → guide breadcrumb.
5. Link to the new page from the body copy of one or two related articles where a reader would naturally want it — contextual links help more than the "Keep reading" list.

### Japanese pages also need

1. The first `ja/` page also brings `ja/index.html` (a Japanese home page with its own hero, intro and cards), the `:lang(ja)` font rules in `styles.css`, the `.lang-switch` style, and the Japanese app screenshots in `images/app/ja/`. Once `ja/` exists, every English page gets a `.lang-switch` in its header too.
2. `ja/index.html` gets the `.post-card`, and the `.related` lists stay within `ja/`.
3. If an English counterpart exists, add the `hreflang` alternates (`en`, `ja`, `x-default` → English) to **both** pages and point both `.lang-switch` links at each other.
4. Facts shared with the English page must agree. If your research finds the English page is out of date, fix it too (see the refresh-page skill).

## 6. Check → **hand back to the user**

- Run `python3 .claude/skills/site-audit/scripts/audit.py .` and fix everything it reports.
- Do a reader-review pass on the new page (`.claude/skills/reader-review/SKILL.md`) and apply the improvements that need no new facts.
- Preview with `python3 -m http.server` from the repo root and look at the page at desktop and phone width. For Japanese pages, check that line breaks look natural and nothing overflows on a phone.
- Summarise for the user: the page, the files touched, any facts you couldn't confirm, and the photo situation. Leave everything uncommitted; the user commits and pushes.
