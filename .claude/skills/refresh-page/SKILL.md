---
name: refresh-page
description: Bring an existing myjapanfishing.com page up to date for the current or coming season — re-check prices, permits, opening dates, ice and event information against the official sources in its "Sources" box, update the copy, and keep every page that repeats the same lake facts in sync, with dates bumped everywhere. Use this whenever the user says a page is outdated, a season is starting (ice fishing, bass, shijimi, wakasagi), asks to "update", "refresh" or "re-verify" a lake guide or article, or mentions a rule, price or date change at one of the six lakes.
---

# Refresh a page

Fishing seasons, fees and rules change every year, and a page that confidently states last year's ice-fishing dates loses a reader for good. A refresh is mainly fact-checking, and the hard part is that the same facts live on several pages.

## 1. Find what can go stale

Read the page and list every time-sensitive fact: fees, permit types and where to buy them, opening and closing dates, hours, size/bag limits, banned methods, event dates, transport details, phone/URL of operators, and anything phrased with a year ("for the 2026 season"). Note the "Sources" box links.

Then find every other place the same fact appears. For a lake that's at least:
- the lake guide (`lake-<name>-fishing.html`, or `lake-suwa-wakasagi-fishing.html`)
- its section in `japans-lakes-for-fishing.html`
- its section in `lake-fishing-license-japan.html`
- the `index.html` `.deep-dive` and post card
- possibly `fishing-lures.html` (lure rules) and `lake-fishing-manners-phrases.html`

`grep -n` for the price or date (e.g. `grep -n '¥300' *.html`) catches the copies you'd otherwise miss.

## 2. Re-verify

Open each source (WebFetch) and search for newer notices, in Japanese too (`<lake> 漁協 お知らせ`, `<lake> ワカサギ 2026`, `<lake> 遊漁料`). Cooperatives often post the new season as a PDF or a news item rather than updating the main page. For each fact, record: still correct / changed (old → new, with source) / can't confirm.

If something can't be confirmed for the coming season, don't keep stating last year's value as current. Say which year it's from and tell readers to check, or ask the user if they have local knowledge.

## 3. Report before editing

Show the user a short table: fact, old value, new value, source, and which pages contain it. Point out anything worth adding while you're there (a new closure, a reader question the page doesn't answer). Get a go-ahead if anything is surprising or uncertain; straightforward confirmed updates can proceed.

## 4. Update everywhere, together

- Change the fact on every page that repeats it, in each page's own wording.
- Update year references ("2026 details" → "2027 details") only where the fact really was re-confirmed.
- Add a new source to the "Sources" box if you used one.
- On each page whose content changed, bump the Article JSON-LD `dateModified`, the visible `<p class="page-updated">` (`datetime` attribute and the text), and `<lastmod>` in `sitemap.xml`, all to today. If the visible change is meaningful to readers, a short sentence like "Updated for the 2027 season" in the intro or info box tells returning readers what's new.
- If the meta description quotes a changed fact, update it and the identical Article JSON-LD `description`.
- If an app feature is mentioned, check it against `~/AndroidStudioProjects/FishingApp/store/listing.md`.

## 5. Check

Run the checker on everything you touched and fix what it reports:

```bash
python3 .claude/skills/site-audit/scripts/audit.py . --page <file1>.html <file2>.html
```

Summarise what changed, on which pages, and anything left unconfirmed. Leave the work uncommitted; the user commits and pushes.
