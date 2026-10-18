---
name: reader-review
description: Review a myjapanfishing.com page the way a real visitor would — a foreign angler planning a trip to a Japanese lake — and suggest concrete edits that make it more useful, more enjoyable to read, and worth bookmarking and coming back to. Use this whenever the user asks to improve, polish, critique or "make better" an article, asks why a page isn't performing or keeping readers, wants more engagement, return visits or time on page, or has just drafted a new article (the write-article skill calls this as its final pass).
---

# Reader review

Search brings people to this site once. Whether they stay, trust it, and come back before their next trip depends on whether the page solves their actual problem better than the other results. Judge every page from the seat of its reader, not from an SEO checklist.

## Who the reader is

Mostly an English-speaking angler (resident foreigner or visitor) who has a lake or a trip in mind and limited Japanese. They want to know: *Is this worth it? When should I go? What's biting? What does it cost, what are the rules, how do I get there, and what will catch me out?* Many read on a phone, often with the trip days away. Some are non-anglers (a partner, a family) deciding whether the trip works for them.

## Read the page, then score it on these

Read the whole page first, as the reader would. Then go through each point and note what's missing or weak. Quote the exact passage you're commenting on.

1. **The answer is up top.** Within the intro and first section, could someone who skims leave with the key answer (best season, main fish, cost, the one big catch)? If the essentials are buried in paragraph six, suggest a short "At a glance" `.info-box` or tightening the intro.
2. **Specific beats general.** Prices in yen, opening hours, months, station names, walking times, permit names, sizes and limits. Every vague phrase ("fairly cheap", "in winter", "nearby") is a chance to be concrete. Flag facts with no source or date; the site's credibility rests on the "Sources" box and the hedged tone.
3. **It answers the next question.** After each section, what would the reader ask next? ("Can I rent gear?", "Is it OK for kids?", "What if the ice is closed?", "Do I need to speak Japanese?") Unanswered next-questions are the best source of new paragraphs, `.tip` lines and FAQ-style subheads.
4. **What will go wrong.** Readers remember the page that warned them: closures, cash-only, reservation needed, lures banned, ice cancelled, last bus times, what wardens confiscate. Each lake page should have at least one honest "check before you go" warning.
5. **Scannable on a phone.** Short paragraphs, descriptive `h2`/`h3` (not clever ones only), lists for steps and rules, the `.lake-meta` line for numbers, a TOC that matches. Flag walls of text and paragraphs over ~5 lines on mobile.
6. **Voice.** Factual, warm, plainly hedged; the site never promises fish. Moon phase and the app are a heuristic "alongside the weather, not instead of it". Cut hype, filler intros ("Japan is a beautiful country…"), and anything that sounds like AI boilerplate. Keep lake-local colour (nicknames, history, food) that makes the page enjoyable, as long as it's short and true.
7. **Reasons to come back.** This is what turns a one-time visit into a bookmark. Look for, or suggest:
   - a **season box** (`.season-box`) or month-by-month line the reader returns to as the season changes;
   - a "**check before you go**" list with the official links that change every year;
   - a visible **Updated** date that's recent, plus a sentence on what changed when it matters ("2026 season dates confirmed");
   - **Japanese phrases** for the exact situations on that page (`.phrase-box`), which people screenshot;
   - **links onward** that match the reader's next step (the license page from a lake guide, the lake guide from the lures page), not just "Keep reading";
   - the **app note** framed around something the reader will check repeatedly (feeding windows, tides, the widget), with the screenshot that matches the topic.
8. **Images earn their place.** Alt text describes what's shown; generic stock photos are flagged as candidates for the user's own trip photos (see the SEO roadmap memory).

## Output

Lead with a two-sentence verdict: who the page serves well now and the single biggest improvement. Then a table, most valuable first:

| # | What to change | Why it helps the reader | Where (section / line) | Effort |
|---|---|---|---|---|

Keep it to the 5–10 changes that matter; don't pad. For the top three, include draft copy in the site's voice using the existing components (`.info-box`, `.tip`, `.season-box`, `.phrase-box`, `.group-box`) so the user can see exactly what you mean.

Never invent facts to fill a gap. If a suggestion needs a fact you don't have (a price, a date, a rule), say so and offer to research it from the official sources, or mark it for the user to confirm.

Then offer to apply the changes. When applying: follow CLAUDE.md (update `dateModified`, the visible "Updated" line and the sitemap `lastmod` together; keep the meta description and Article JSON-LD description identical; sync lake facts across the guide, the hub, the license page and the `index.html` deep-dive), and run the site-audit checker on the page afterwards:

```bash
python3 .claude/skills/site-audit/scripts/audit.py . --page <file>.html
```
