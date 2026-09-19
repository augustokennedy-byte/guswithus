#!/usr/bin/env python3
"""One-time extractor: pull the Resource Center card data out of the built HTML
into resources.json, so the list becomes editable data instead of 950KB of HTML."""
import json, re, sys, pathlib, html

SITE = pathlib.Path(sys.argv[1])
INDEX = SITE / "resources" / "index.html"
src = INDEX.read_text(encoding="utf-8")

main = src[src.index('<main id="main">'):src.index('</main>')]

SECTION_RE = re.compile(
    r'<section class="cat" id="cat-(?P<slug>[a-z-]+)" data-cat="(?P<cat>[a-z-]+)">\s*'
    r'<h2>(?P<title>.*?) <span class="n">.*?</span></h2>', re.S)
CARD_RE = re.compile(
    r'<article class="card(?P<urgent> urgent)?" data-cat="(?P<cat>[^"]*)" data-boro="(?P<boro>[^"]*)" '
    r'data-s="(?P<s>[^"]*)">(?P<body>.*?)</article>', re.S)

def one(pat, body):
    m = re.search(pat, body, re.S)
    return m.group(1).strip() if m else None

# anchors: <a class="go" href=".." (target..)?>LABEL <svg...></a>
ANCHOR_RE = re.compile(
    r'<a class="(?P<kind>go|tel)" href="(?P<href>[^"]*)"(?P<attrs>[^>]*)>(?P<inner>.*?)</a>', re.S)

def anchor_label(inner):
    # strip the inline svg, keep the visible text
    txt = re.sub(r'<svg.*?</svg>', '', inner, flags=re.S)
    return re.sub(r'\s+', ' ', txt).strip()

sections, cards = [], []
bounds = [(m.start(), m) for m in SECTION_RE.finditer(main)]
for i, (pos, m) in enumerate(bounds):
    end = bounds[i + 1][0] if i + 1 < len(bounds) else len(main)
    sections.append({"slug": m.group("slug"), "cat": m.group("cat"),
                     "title": m.group("title")})
    for c in CARD_RE.finditer(main[pos:end]):
        body = c.group("body")
        acts = []
        for a in ANCHOR_RE.finditer(body):
            acts.append({"kind": a.group("kind"), "href": a.group("href"),
                         "label": anchor_label(a.group("inner")),
                         "external": 'target="_blank"' in a.group("attrs")})
        cards.append({
            "cat": c.group("cat"),
            "urgent": bool(c.group("urgent")),
            "boro": c.group("boro").split(),
            "badge": one(r'<span class="badge">(.*?)</span>', body),
            "name": one(r'<h3>(.*?)</h3>', body),
            "what": one(r'<p class="what">(.*?)</p>', body),
            "addr": one(r'<p class="addr">(.*?)</p>', body),
            "note": one(r'<p class="note">(.*?)</p>', body),
            "acts": acts,
            "search": c.group("s"),
        })

# The data-s search blob is derived from the card's own text plus a tail of
# hand-picked keywords. Split that tail off so the derived part can be rebuilt
# whenever the wording changes -- otherwise editing a description silently
# breaks on-page search.
_sect = {s["cat"]: s["title"].replace("&amp;", "and") for s in sections}
for c in cards:
    prefix = " ".join([c["name"], c["what"], c.get("note") or "",
                       c.get("addr") or "", _sect[c["cat"]], " ".join(c["boro"])])
    derived = html.escape(prefix, quote=True).lower()
    assert c["search"].startswith(derived), "search blob does not decompose: " + c["name"]
    c["keywords"] = c["search"][len(derived):]
    del c["search"]

# everything after the final card section (no-results block + closer + wrap close)
_la = main.rindex('</article>')
_sc = main.index('    </section>', _la) + len('    </section>')
tail = main[_sc:]

dest_path = pathlib.Path(sys.argv[2])
prev = {}
if dest_path.exists():
    prev = json.loads(dest_path.read_text(encoding="utf-8"))

out = {"checked": prev.get("checked", "1970-01-01"),
       "sections": sections, "cards": cards, "tail": tail}
dest = dest_path
dest.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"sections={len(sections)} cards={len(cards)} -> {dest}")
