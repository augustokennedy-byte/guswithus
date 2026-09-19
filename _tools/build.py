#!/usr/bin/env python3
"""Rebuild the Resource Center card listings in all seven pages from resources.json.

Only the <main> block is rewritten. The head, CSS, nav, search script and footer
of each page are hand-tuned and are left exactly as they are.

  python3 build.py <site-root> <resources.json>
"""
import json, re, sys, pathlib, html, datetime

ARROW = ('<svg width="15" height="15" viewBox="0 0 24 24" fill="none" '
         'stroke="currentColor" stroke-width="2.6" aria-hidden="true">'
         '<path d="M5 12h13M13 6l6 6-6 6"/></svg>')
PHONE = ('<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" '
         'aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 006.6 6.6l2.2-2.2a1 '
         '1 0 011-.24 11.4 11.4 0 003.6.58 1 1 0 011 1V20a1 1 0 01-1 1A17 17 0 '
         '013 4a1 1 0 011-1h3.5a1 1 0 011 1c0 1.25.2 2.46.58 3.6a1 1 0 01-.25 '
         '1l-2.2 2.2z"/></svg>')

# page directory -> the data-boro token it filters on (None = every card)
PAGES = {
    "": None, "jamaica": "jamaica", "queens": "queens", "brooklyn": "brooklyn",
    "manhattan": "manhattan", "bronx": "bronx", "staten-island": "statenisland",
}


def search_blob(c, section_title):
    """Rebuild the data-s attribute the on-page search reads."""
    prefix = " ".join([c["name"], c["what"], c.get("note") or "",
                       c.get("addr") or "", section_title.replace("&amp;", "and"),
                       " ".join(c["boro"])])
    return html.escape(prefix, quote=True).lower() + c["keywords"]


def render_card(c, section_title):
    L = ['        <article class="card%s" data-cat="%s" data-boro="%s" data-s="%s">'
         % (" urgent" if c.get("urgent") else "", c["cat"],
            " ".join(c["boro"]), search_blob(c, section_title))]
    if c.get("badge"):
        L.append('          <span class="badge">%s</span>' % c["badge"])
    L.append('          <h3>%s</h3>' % c["name"])
    L.append('          <p class="what">%s</p>' % c["what"])
    if c.get("addr"):
        L.append('          <p class="addr">%s</p>' % c["addr"])
    if c.get("note"):
        L.append('          <p class="note">%s</p>' % c["note"])
    L.append('          <div class="acts">')
    for a in c["acts"]:
        if a["kind"] == "go":
            rel = ' target="_blank" rel="noopener noreferrer"' if a["external"] else ""
            L.append('            <a class="go" href="%s"%s>%s %s</a>'
                     % (a["href"], rel, a["label"], ARROW))
        else:
            L.append('            <a class="tel" href="%s">%s %s</a>'
                     % (a["href"], PHONE, a["label"]))
    L.append('          </div>')
    L.append('        </article>')
    return "\n".join(L)


def render_main(data, boro):
    L = ['<main id="main">', '  <div class="wrap">']
    for s in data["sections"]:
        cards = [c for c in data["cards"] if c["cat"] == s["cat"]
                 and (boro is None or boro in c["boro"])]
        if not cards:
            continue
        L.append('    <section class="cat" id="cat-%s" data-cat="%s">'
                 % (s["slug"], s["cat"]))
        L.append('      <h2>%s <span class="n">%d resources</span></h2>'
                 % (s["title"], len(cards)))
        L.append('      <div class="grid">')
        L.extend(render_card(c, s["title"]) for c in cards)
        L.append('      </div>')
        L.append('    </section>')
    return "\n".join(L) + data["tail"]


CHECKED_RE = re.compile(r'\n *<p class="checked">.*?</p>', re.S)
ANCHOR = '    <p><strong>The G Method, developed with our team.</strong>'


def stamp_checked(src, iso):
    """Show readers when these links were last verified, and keep it honest."""
    d = datetime.date.fromisoformat(iso)
    pretty = "%d %s %d" % (d.day, d.strftime("%B"), d.year)
    line = ('\n    <p class="checked">Every link on this page was checked on '
            '<time datetime="%s">%s</time>. We check them on the 1st and the '
            '15th of every month.</p>' % (iso, pretty))
    if CHECKED_RE.search(src):
        return CHECKED_RE.sub(lambda _: line, src, count=1)
    i = src.index(ANCHOR)
    j = src.index("</p>", i) + len("</p>")
    return src[:j] + line + src[j:]


def main():
    site = pathlib.Path(sys.argv[1])
    data = json.loads(pathlib.Path(sys.argv[2]).read_text(encoding="utf-8"))
    for slug, boro in PAGES.items():
        path = site / "resources" / slug / "index.html"
        src = path.read_text(encoding="utf-8")
        start, end = src.index('<main id="main">'), src.index('</main>')
        new = src[:start] + render_main(data, boro) + src[end:]
        new = stamp_checked(new, data["checked"])
        if new != src:
            path.write_text(new, encoding="utf-8")
            print("updated %s" % path.relative_to(site))
        else:
            print("unchanged %s" % path.relative_to(site))


if __name__ == "__main__":
    main()
