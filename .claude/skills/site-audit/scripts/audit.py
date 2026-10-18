#!/usr/bin/env python3
"""Consistency audit for the myjapanfishing.com static site.

Checks the rules in CLAUDE.md that are easy to break by hand: title and
description length, canonical/og:url/JSON-LD URLs, dateModified vs. the
visible "Updated" line vs. sitemap lastmod, TOC anchors, image attributes,
local links, Google Play referrers, index cards, "Keep reading" lists and the
app page's FAQ JSON-LD.

Usage:
    python3 audit.py [repo_root] [--page file.html ...]

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
TITLE_MAX = 60
DESC_MAX = 160
PLAY_PREFIX = "https://play.google.com/store/apps/details?id=com.tomat.fishingapp"
APP_PAGE = "japan-fishing-forecast-app.html"


class Page(HTMLParser):
    """Collects the bits of a page the audit cares about."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.meta = {}
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
        if tag not in ("img", "meta", "link", "br", "hr", "input", "source"):
            self._stack.append(cls)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "title":
            self._in, self._buf = "title", ""
        elif tag == "meta":
            key = a.get("name") or a.get("property")
            if key:
                self.meta[key] = a.get("content", "")
        elif tag == "link" and a.get("rel") == "canonical":
            self.meta["canonical"] = a.get("href", "")
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
        if tag not in ("img", "meta", "link", "br", "hr", "input", "source") and self._stack:
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


def slug(fname):
    return {"index.html": "home", APP_PAGE: "app-page"}.get(fname, fname[:-5])


def url_for(fname):
    return SITE if fname == "index.html" else SITE + fname


def audit_page(root, fname, sitemap, all_pages):
    p = Page()
    raw = open(os.path.join(root, fname), encoding="utf-8").read()
    p.feed(raw)
    out = []
    err = lambda m: out.append(("ERROR", m))
    warn = lambda m: out.append(("WARN", m))
    is_article = "page-hero" in p.classes
    is_app = fname == APP_PAGE

    # Title and description
    if not p.title:
        err("missing <title>")
    else:
        if len(p.title) > TITLE_MAX + 5:
            err(f"title is {len(p.title)} chars (aim for ~{TITLE_MAX}): {p.title!r}")
        elif len(p.title) > TITLE_MAX:
            warn(f"title is {len(p.title)} chars (aim for ~{TITLE_MAX})")
        if fname != "index.html" and not p.title.endswith("| My Japan Fishing"):
            warn("title doesn't end with '| My Japan Fishing'")
    desc = p.meta.get("description", "")
    if not desc:
        err("missing meta description")
    elif len(desc) > DESC_MAX:
        warn(f"meta description is {len(desc)} chars (aim for ~155)")

    # URLs
    expected = url_for(fname)
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
            if fname.startswith("lake-") and fname.endswith("-fishing.html") and len(items) != 3:
                warn("lake guide breadcrumb should be Home → The Six Lakes We Cover → guide")

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
        if not img.get("alt") and img.get("alt") != "":
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
        if re.match(r"^(https?:|mailto:|tel:|#|data:)", val) or val.startswith("//"):
            continue
        path = val.split("#")[0].split("?")[0]
        if not path or path == "/":
            continue
        target = os.path.join(root, path.lstrip("/"))
        if not os.path.exists(target):
            err(f"broken local {attr}: {val}")
        elif path.endswith(".html") and "#" in val:
            anchor = val.split("#", 1)[1]
            if f'id="{anchor}"' not in open(target, encoding="utf-8").read():
                err(f"link {val} points at a missing anchor")

    # Google Play referrer
    want = f"utm_campaign%3D{slug(fname)}"
    for tag, attr, val in p.links:
        if val.startswith(PLAY_PREFIX):
            if "referrer=" not in val:
                err(f"Google Play link without referrer: {val[:80]}…")
            elif want not in val:
                err(f"Google Play referrer campaign should be {slug(fname)!r}")
    if is_article and "app-note" not in p.classes:
        warn("no .app-note CTA")

    # Keep reading
    if is_article:
        rel = [h for h in p.related if h.endswith(".html")]
        if not rel:
            warn("no .related 'Keep reading' list")
        elif not 3 <= len(rel) <= 7:
            warn(f".related lists {len(rel)} pages (aim for about five)")
        if fname in rel:
            err(".related links to the page itself")

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

    # Index cards
    if fname == "index.html":
        cards = {c.lstrip("/") for c in p.post_cards}
        for other in all_pages:
            if other not in ("index.html",) and other not in cards:
                warn(f"index.html has no .post-card for {other}")

    return out


def main():
    args = sys.argv[1:]
    pages_only = []
    if "--page" in args:
        i = args.index("--page")
        pages_only = args[i + 1:]
        args = args[:i]
    root = os.path.abspath(args[0] if args else ".")
    all_pages = sorted(
        f for f in os.listdir(root)
        if f.endswith(".html") and f not in SKIP and not f.startswith("google")
    )
    sitemap = read_sitemap(root)
    for loc in sitemap:
        f = "index.html" if loc == SITE else loc.replace(SITE, "")
        if f not in all_pages:
            print(f"sitemap.xml\n  ERROR lists {loc}, but there's no such page\n")

    errors = warnings = 0
    for fname in pages_only or all_pages:
        results = audit_page(root, os.path.basename(fname), sitemap, all_pages)
        if not results:
            continue
        print(fname)
        for level, msg in results:
            print(f"  {level} {msg}")
            errors += level == "ERROR"
            warnings += level == "WARN"
        print()
    checked = len(pages_only or all_pages)
    print(f"Checked {checked} page(s): {errors} error(s), {warnings} warning(s).")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
