#!/usr/bin/env python3
"""Consistency audit for the myjapanfishing.com static site.

Checks the rules in CLAUDE.md that are easy to break by hand: title and
description length, canonical/og:url/JSON-LD URLs, dateModified vs. the
visible "Updated" line vs. sitemap lastmod, TOC anchors, image attributes,
local links, Google Play referrers, index cards, "Keep reading" lists, the
app page's FAQ JSON-LD, and for the Japanese pages in ja/: lang, og:locale,
hreflang pairs, the language switch and the Japanese font.

Usage:
    python3 audit.py [repo_root] [--page file.html ja/file.html ...]

Prints ERROR / WARN lines grouped by file and exits 1 if any ERROR was found.
Standard library only.
"""

import difflib
import json
import os
import re
import sys
from html.parser import HTMLParser

SITE = "https://myjapanfishing.com/"
SKIP = {"404.html"}
LANGS = ("en", "ja")
TITLE_MAX = {"en": 60, "ja": 35}   # Google shows fewer Japanese characters
DESC_MAX = {"en": 160, "ja": 125}
PLAY_PREFIX = "https://play.google.com/store/apps/details?id=com.tomat.fishingapp"
UTM_SOURCE = {"en": "utm_source%3Dmyjapanfishing%26", "ja": "utm_source%3Dmyjapanfishing-ja%26"}
APP_PAGE = "japan-fishing-forecast-app.html"
VOID = ("img", "meta", "link", "br", "hr", "input", "source")


class Page(HTMLParser):
    """Collects the bits of a page the audit cares about."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.html_lang = None
        self.title = ""
        self.meta = {}
        self.hreflang = {}       # lang -> href
        self.lang_switch = []
        self.links = []          # (tag, attr, value)
        self.ids = set()
        self.imgs = []           # attrs dicts
        self.jsonld = []
        self.toc_anchors = []
        self.section_ids = []
        self.related = []
        self.post_cards = []
        self.updated = None
        self.faq_summaries = []
        self.classes = set()
        self._stack = []         # open element class lists
        self._in = None          # "title" | "jsonld" | "summary"
        self._buf = ""

    def _inside(self, cls):
        return any(cls in c for c in self._stack)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = (a.get("class") or "").split()
        self.classes.update(cls)
        if tag not in VOID:
            self._stack.append(cls)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "html":
            self.html_lang = a.get("lang")
        elif tag == "title":
            self._in, self._buf = "title", ""
        elif tag == "meta":
            key = a.get("name") or a.get("property")
            if key:
                self.meta[key] = a.get("content", "")
        elif tag == "link" and a.get("rel") == "canonical":
            self.meta["canonical"] = a.get("href", "")
        elif tag == "link" and a.get("rel") == "alternate" and a.get("hreflang"):
            self.hreflang[a["hreflang"]] = a.get("href", "")
        elif tag == "script" and a.get("type") == "application/ld+json":
            self._in, self._buf = "jsonld", ""
        elif tag == "summary" and self._inside("lp-faq"):
            self._in, self._buf = "summary", ""
        elif tag == "time" and self._inside("page-updated"):
            self.updated = a.get("datetime")
        elif tag == "img":
            self.imgs.append(a)
        if tag == "section" and "content-section" in cls and "id" in a:
            self.section_ids.append(a["id"])
        if tag == "a":
            href = a.get("href", "")
            if self._inside("toc") and href.startswith("#"):
                self.toc_anchors.append(href[1:])
            if self._inside("related"):
                self.related.append(href)
            if "post-card" in cls:
                self.post_cards.append(href)
            if "lang-switch" in cls:
                self.lang_switch.append(href)
        for attr in ("href", "src"):
            if attr in a and tag in ("a", "link", "img", "script", "source"):
                self.links.append((tag, attr, a[attr]))

    def handle_endtag(self, tag):
        if tag in ("title", "script", "summary") and self._in:
            text = self._buf.strip()
            if self._in == "title":
                self.title = text
            elif self._in == "jsonld":
                self.jsonld.append(text)
            elif self._in == "summary":
                self.faq_summaries.append(" ".join(text.split()))
            self._in = None
        if tag not in VOID and self._stack:
            self._stack.pop()

    def handle_data(self, data):
        if self._in:
            self._buf += data


def graph_nodes(blobs, problems):
    nodes = []
    for raw in blobs:
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            problems.append(("ERROR", f"JSON-LD does not parse: {e}"))
            continue
        nodes.extend(data.get("@graph", [data]))
    return nodes


def node(nodes, typ):
    return next((n for n in nodes if n.get("@type") == typ), None)


def read_sitemap(root):
    path = os.path.join(root, "sitemap.xml")
    if not os.path.exists(path):
        return {}
    text = open(path, encoding="utf-8").read()
    return dict(re.findall(r"<loc>(.*?)</loc>\s*<lastmod>(.*?)</lastmod>", text))


def lang_of(rel):
    return "ja" if rel.startswith("ja/") else "en"


def slug(rel):
    name = os.path.basename(rel)
    return {"index.html": "home", APP_PAGE: "app-page"}.get(name, name[:-5])


def url_for(rel):
    return SITE + (rel[:-len("index.html")] if rel.endswith("index.html") else rel)


def rel_for(url):
    rel = url.replace(SITE, "", 1)
    return rel + "index.html" if rel == "" or rel.endswith("/") else rel


def counterpart(rel):
    return rel[3:] if rel.startswith("ja/") else "ja/" + rel


def resolve(root, rel, val):
    """Local file a link points at, or None for external/anchor links."""
    if re.match(r"^(https?:|mailto:|tel:|#|data:)", val) or val.startswith("//"):
        return None
    path = val.split("#")[0].split("?")[0]
    if not path:
        return None
    if path.startswith("/"):
        target = os.path.join(root, path.lstrip("/"))
    else:
        target = os.path.normpath(os.path.join(root, os.path.dirname(rel), path))
    if path.endswith("/"):
        target = os.path.join(target, "index.html")
    return target


def audit_page(root, rel, sitemap, all_pages):
    p = Page()
    raw = open(os.path.join(root, rel), encoding="utf-8").read()
    p.feed(raw)
    out = []
    err = lambda m: out.append(("ERROR", m))
    warn = lambda m: out.append(("WARN", m))
    name = os.path.basename(rel)
    lang = lang_of(rel)
    is_article = "page-hero" in p.classes
    is_app = name == APP_PAGE
    is_home = name == "index.html"

    # Language
    if p.html_lang != lang:
        err(f'<html lang="{p.html_lang}">, expected "{lang}"')
    if lang == "ja":
        if p.meta.get("og:locale") != "ja_JP":
            err("og:locale should be ja_JP")
        if "Noto+Sans+JP" not in raw:
            warn("Google Fonts link doesn't load Noto Sans JP")
        if "phrase-box" in p.classes:
            warn("phrase box on a Japanese page (that's content for foreigners)")
        for tag, attr, val in p.links:
            if tag in ("a", "link", "img") and resolve(root, rel, val) and not val.startswith("/"):
                err(f"/ja/ pages use root-absolute paths: {val}")
        to_en_home = sum(t == "a" and v == "/" for t, _, v in p.links) - p.lang_switch.count("/")
        if to_en_home > 0:
            warn(f'{to_en_home} link(s) to "/" (the English home page); link home with "/ja/"')

    # Title and description
    if not p.title:
        err("missing <title>")
    else:
        n, cap = len(p.title), TITLE_MAX[lang]
        if n > cap + 5:
            err(f"title is {n} chars (aim for ~{cap}): {p.title!r}")
        elif n > cap:
            warn(f"title is {n} chars (aim for ~{cap})")
        if not is_home and not p.title.endswith("| My Japan Fishing"):
            warn("title doesn't end with '| My Japan Fishing'")
    desc = p.meta.get("description", "")
    if not desc:
        err("missing meta description")
    elif len(desc) > DESC_MAX[lang]:
        warn(f"meta description is {len(desc)} chars (aim for ~{DESC_MAX[lang] - 5})")

    # URLs
    expected = url_for(rel)
    for key in ("canonical", "og:url"):
        if p.meta.get(key) != expected:
            err(f"{key} is {p.meta.get(key)!r}, expected {expected!r}")
    if "www.myjapanfishing.com" in raw:
        err("uses www.myjapanfishing.com (use the apex domain)")
    for key in ("og:title", "og:description", "og:image", "twitter:card", "twitter:image"):
        if key not in p.meta:
            warn(f"missing {key}")
    if is_article and p.meta.get("og:type") != "article":
        warn(f"og:type is {p.meta.get('og:type')!r}, expected 'article'")

    # hreflang and the language switch
    other = counterpart(rel)
    has_pair = other in all_pages
    if has_pair:
        en_url, ja_url = (expected, url_for(other)) if lang == "en" else (url_for(other), expected)
        want = {"en": en_url, "ja": ja_url, "x-default": en_url}
        for hl, url in want.items():
            if p.hreflang.get(hl) != url:
                err(f'hreflang="{hl}" is {p.hreflang.get(hl)!r}, expected {url!r}')
    elif p.hreflang:
        err(f"has hreflang links but no {other} counterpart exists")
    if any(r.startswith("ja/") for r in all_pages):
        if not p.lang_switch:
            warn("no .lang-switch link in the header")
        else:
            target = resolve(root, rel, p.lang_switch[0])
            home = os.path.join(root, "index.html" if lang == "ja" else "ja/index.html")
            want_t = os.path.join(root, other) if has_pair else home
            if target and os.path.normpath(target) != os.path.normpath(want_t):
                err(f".lang-switch points at {p.lang_switch[0]}, expected the "
                    f"{'counterpart' if has_pair else 'other language home page'}")

    # JSON-LD
    nodes = graph_nodes(p.jsonld, out)
    if not nodes:
        err("no JSON-LD")
    for n in nodes:
        pub = n.get("publisher")
        if isinstance(pub, dict) and pub.get("name") != "TsureruKana":
            err(f"{n.get('@type')} publisher.name is {pub.get('name')!r}, expected 'TsureruKana'")
    art = node(nodes, "Article")
    if is_article:
        if not art:
            err("article page without an Article JSON-LD node")
        else:
            if art.get("description") != desc:
                err("Article JSON-LD description doesn't match the meta description")
            if art.get("mainEntityOfPage") != expected:
                err(f"Article mainEntityOfPage is {art.get('mainEntityOfPage')!r}")
            if lang == "ja" and art.get("inLanguage") != "ja":
                err('Article JSON-LD needs "inLanguage": "ja"')
            mod = art.get("dateModified")
            if p.updated != mod:
                err(f"visible 'Updated' date {p.updated!r} != JSON-LD dateModified {mod!r}")
            if (art.get("datePublished") or "") > (mod or ""):
                err("datePublished is after dateModified")
        crumbs = node(nodes, "BreadcrumbList")
        if not crumbs:
            err("no BreadcrumbList JSON-LD")
        else:
            items = crumbs.get("itemListElement", [])
            if items and items[-1].get("item") != expected:
                err("last breadcrumb item doesn't point at this page")
            if items and items[0].get("item") != url_for("ja/index.html" if lang == "ja" else "index.html"):
                err("first breadcrumb item should be this language's home page")
            hub = ("ja/" if lang == "ja" else "") + "japans-lakes-for-fishing.html"
            if name.startswith("lake-") and name.endswith("-fishing.html") and hub in all_pages \
                    and len(items) != 3:
                warn("lake guide breadcrumb should be Home → the six-lakes hub → guide")

    # Updated date vs sitemap
    if expected not in sitemap:
        err("not listed in sitemap.xml")
    else:
        page_date = (art or {}).get("dateModified") or p.updated
        if page_date and sitemap[expected] < page_date:
            err(f"sitemap lastmod {sitemap[expected]} is older than the page's date {page_date}")

    # TOC anchors
    if p.toc_anchors:
        for a in p.toc_anchors:
            if a not in p.ids:
                err(f"TOC links to #{a}, but no element has that id")
        for s in p.section_ids:
            if s not in p.toc_anchors:
                warn(f"content-section #{s} isn't in the TOC")
    elif is_article:
        warn("no .toc found")

    # Images
    for img in p.imgs:
        src = img.get("src", "")
        if "alt" not in img:
            err(f"<img> without alt: {src}")
        if img.get("fetchpriority") == "high":
            if "unsplash.com" in src and is_article and "w=1400" not in src:
                warn(f"article hero isn't w=1400: {src}")
            continue
        if not img.get("width") or not img.get("height"):
            warn(f"<img> without width/height: {src}")
        if img.get("loading") != "lazy" and not is_app:
            warn(f"<img> without loading=\"lazy\": {src}")

    # Local links and assets
    for tag, attr, val in p.links:
        target = resolve(root, rel, val)
        if not target:
            continue
        if not os.path.exists(target):
            err(f"broken local {attr}: {val}")
        elif target.endswith(".html") and "#" in val:
            anchor = val.split("#", 1)[1]
            if f'id="{anchor}"' not in open(target, encoding="utf-8").read():
                err(f"link {val} points at a missing anchor")

    # Google Play referrer
    campaign = f"utm_campaign%3D{slug(rel)}"
    for tag, attr, val in p.links:
        if val.startswith(PLAY_PREFIX):
            if "referrer=" not in val:
                err(f"Google Play link without referrer: {val[:80]}…")
                continue
            if UTM_SOURCE[lang] not in val:
                err(f"Google Play referrer should use {UTM_SOURCE[lang][:-3]}")
            if campaign not in val:
                err(f"Google Play referrer campaign should be {slug(rel)!r}")
            if lang == "ja" and "hl=ja" not in val:
                err("Google Play link on a Japanese page needs &amp;hl=ja")
    if is_article and "app-note" not in p.classes:
        warn("no .app-note CTA")

    # Keep reading
    if is_article:
        rel_links = [h for h in p.related if h.endswith(".html")]
        if not rel_links:
            warn("no .related 'Keep reading' list")
        elif not 3 <= len(rel_links) <= 7:
            warn(f".related lists {len(rel_links)} pages (aim for about five)")
        for h in rel_links:
            t = resolve(root, rel, h)
            if t and os.path.normpath(t) == os.path.normpath(os.path.join(root, rel)):
                err(".related links to the page itself")
            elif t and lang_of(os.path.relpath(t, root)) != lang:
                err(f".related links to a page in the other language: {h}")

    # Bare ampersands in text (outside scripts)
    body = re.sub(r"<script.*?</script>", "", raw, flags=re.S)
    for m in re.finditer(r"&(?=\s)", body):
        line = body.count("\n", 0, m.start()) + 1
        err(f"unescaped '&' at line ~{line} (use &amp;)")

    # App page FAQ in step with JSON-LD
    if is_app:
        faq = node(nodes, "FAQPage")
        if not faq:
            err("app page without FAQPage JSON-LD")
        else:
            # JSON-LD questions may be worded a little more fully than the
            # visible <summary>, so match them loosely.
            q_ld = [" ".join(q.get("name", "").split()) for q in faq.get("mainEntity", [])]
            if len(q_ld) != len(p.faq_summaries):
                err(f"FAQPage JSON-LD has {len(q_ld)} questions, the visible FAQ has "
                    f"{len(p.faq_summaries)}")
            for q in p.faq_summaries:
                if not difflib.get_close_matches(q, q_ld, n=1, cutoff=0.6):
                    err(f"visible FAQ question has no JSON-LD match: {q!r}")
        if not node(nodes, "MobileApplication"):
            err("app page without MobileApplication JSON-LD")

    # Index cards (each language's home lists that language's pages)
    if is_home:
        cards = set()
        for c in p.post_cards:
            t = resolve(root, rel, c)
            if t:
                cards.add(os.path.relpath(t, root))
        for other_rel in all_pages:
            if lang_of(other_rel) == lang and os.path.basename(other_rel) != "index.html" \
                    and other_rel not in cards:
                warn(f"{rel} has no .post-card for {other_rel}")

    return out


def find_pages(root):
    pages = [f for f in os.listdir(root)
             if f.endswith(".html") and f not in SKIP and not f.startswith("google")]
    ja = os.path.join(root, "ja")
    if os.path.isdir(ja):
        pages += ["ja/" + f for f in os.listdir(ja) if f.endswith(".html")]
    return sorted(pages)


def main():
    args = sys.argv[1:]
    pages_only = []
    if "--page" in args:
        i = args.index("--page")
        pages_only = args[i + 1:]
        args = args[:i]
    root = os.path.abspath(args[0] if args else ".")
    all_pages = find_pages(root)
    sitemap = read_sitemap(root)
    for loc in sitemap:
        if rel_for(loc) not in all_pages:
            print(f"sitemap.xml\n  ERROR lists {loc}, but there's no such page\n")

    errors = warnings = 0
    targets = [os.path.relpath(os.path.join(root, f), root) for f in pages_only] or all_pages
    for rel in targets:
        results = audit_page(root, rel, sitemap, all_pages)
        if not results:
            continue
        print(rel)
        for level, msg in results:
            print(f"  {level} {msg}")
            errors += level == "ERROR"
            warnings += level == "WARN"
        print()
    print(f"Checked {len(targets)} page(s): {errors} error(s), {warnings} warning(s).")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
