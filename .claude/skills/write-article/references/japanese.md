# Writing the Japanese pages (`/ja/`)

Read this before writing or editing anything in `ja/`. The structural rules (paths, hreflang, fonts, Play links) are in CLAUDE.md under "Japanese version"; this file is about the reader and the writing.

## The reader

A local hobby angler, Lake Biwa first. They fish several times a season, know what a 遊漁券 is and what a crankbait does, and read Japanese fishing media and blogs. They don't need the lake explained to them. What they need is one dependable place to **check before the next trip**: what the rules are this season, when each fish is in, which times and conditions to aim for, and what has changed. They read on a phone, often the night before or at the launch ramp.

So a Japanese page is not the English page translated. It's shorter on background and tourist logistics, and longer on:
- rules and the reason for them, with the official source (滋賀県の琵琶湖レジャー利用適正化条例, 外来魚のリリース禁止, 回収ボックスの場所, ボートの航行規制区域, 漁協の遊漁規則)
- seasonal timing by month and by area (北湖・南湖, 東岸・西岸, 内湖)
- conditions that move the bite (水温, 風向き, 濁り, 気圧, 時合, 月齢) as rules of thumb, not promises
- a short "釣行前チェック" list readers can run through before leaving home

Leave out what only a foreign visitor needs: the phrase boxes, how to ask for a permit in Japanese, station-by-station travel from Tokyo, explanations of Japanese etiquette that every local knows.

## Voice

- です・ます調. Plain, friendly and confident, like an experienced angler at the tackle shop, not a press release or keigo-heavy customer service.
- Factual and hedged in the same way as the English site. The bite window and the app's score are 目安 to check 「天気と合わせて」, never guarantees. Avoid hype words (爆釣, 必釣, 絶対釣れる, 最強) and clickbait headings.
- Give the source in the sentence when it matters: 「滋賀県によると」, 「〇〇漁協の2026年の案内では」. Readers trust a page that shows where a rule comes from.
- Natural Japanese first. If a sentence reads like a translation (long subject chains, 「〜することができます」 everywhere, too many 「あなた」), rewrite it. Read the paragraph back as a local reader would.
- Say plainly when something can't be confirmed: 「2026年の日程はまだ発表されていません（10月時点）」.

## Terms (use the words locals search for)

| Use | Notes |
|---|---|
| 琵琶湖・霞ヶ浦・サロマ湖・小川原湖・猪苗代湖・諏訪湖 | lake names as written locally |
| 北湖・南湖, 内湖 | Biwa's basins and side lakes |
| ブラックバス (オオクチバス), スモールマウス (コクチバス), ブルーギル, ワカサギ, ビワマス, ニジマス, シジミ | the everyday name first; the official name in brackets where rules use it |
| 外来魚, リリース禁止, 外来魚回収ボックス・回収いけす | Shiga's release rules |
| 遊漁券, 遊漁料, 漁協, 解禁, 禁漁期間, 体長制限 | permits and seasons |
| オカッパリ, レンタルボート, ガイド船, ドーム船, 氷上ワカサギ釣り | ways to fish |
| 時合, 朝マズメ・夕マズメ, 月齢, ソルナー, 潮汐, 潮見表, 大潮・小潮 | timing. The store listing writes 時合 and the app screen 時合い; the pages use 時合 |
| 水温, 風向き, 濁り, 気圧 | conditions |

The app is called 『釣れるかな？』 in Japanese copy. Its feature names come from the Japanese store listing (`~/AndroidStudioProjects/FishingApp/store/listing.md`, section "Japanese (ja-JP)"): スコア, 狙い目の魚, おすすめルアー, フィーディングタイム, 潮見表, ホーム画面ウィジェット, 釣果記録, 釣り場のルール確認. Use those exact names so the site and the app feel like one product. The JSON-LD `publisher.name` stays "TsureruKana".

## Formatting

- Half-width digits and Latin letters, full-width Japanese punctuation 「、。（）」. Quotes 「」, titles of works 『』.
- Money as 300円, ranges with 〜 (6:30〜15:00, 1月中旬〜2月下旬), dates as 2026年1月15日, 24-hour times.
- Units as in the English pages (km², m, cm). No space between Japanese text and numbers.
- Headings can be the question a local would type: 「琵琶湖で釣ったバスはリリースしていい？」 — they match search queries and make the TOC useful.
- Keep `<title>` to about 35 characters and the description to about 120, front-loading the lake and the topic (「琵琶湖 バス釣りのルールと季節 | My Japan Fishing」).

## Reasons to come back (build these in)

- A **釣行前チェック** `.info-box` near the top: rules, the season's dates, where to check closures or the weather, with links to the official pages.
- A **month-by-month** `.season-box` or table (北湖 / 南湖 if they differ) that readers check as the season turns.
- A visible **更新日** line and, after a seasonal update, one sentence on what changed (「2027年シーズンの日程に更新しました」).
- A **出典** `.info-box` listing every official source, noting that dates and fees change.
- An app note about what the reader checks again and again: 時合, the score, 潮見表 at Saroma and Ogawara, the widget. Use the Japanese screenshots (`images/app/ja/app-*.webp`, made from the app repo's `store/out/ja/*.png` the same way as the English ones), and check that the image isn't blank before using it.

## Sources to start from

Search in Japanese, and prefer the primary source: 滋賀県 (琵琶湖レジャー利用適正化条例, 外来魚対策), the fishing cooperatives (漁協) for each lake, the city or prefecture tourism site, and the operators themselves. Japanese fishing media and blogs are useful for seasonal patterns and local practice, but check any rule or fee against an official page before stating it.
