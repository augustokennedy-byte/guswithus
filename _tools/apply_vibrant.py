#!/usr/bin/env python3
"""Apply _tools/vibrant.css and the hero quick-jump tiles to all seven Resource Center pages.

Idempotent: replaces its own block if already present. Run after editing vibrant.css.
  python3 _tools/apply_vibrant.py .
"""
import re, sys, pathlib

START, END = "/* ==== VIBRANT REFRESH", "/* ==== END VIBRANT REFRESH ==== */"
QUICK = [("food","\U0001F34E","Food","#F58426"),("housing","\U0001F3E0","Rent &amp; shelter","#0848A2"),
         ("jobs","\U0001F4BC","Jobs","#0E7490"),("legal","⚖️","Legal help","#4338CA"),
         ("kids","\U0001F9D2","Kids &amp; teens","#DB2777"),("health","⚕️","Health","#0F766E")]
QRE = re.compile(r'\n *<nav class="quick".*?</nav>(\n *<p class="winter">.*?</p>)?', re.S)

def quick_html(src):
    items = []
    for slug, icon, label, color in QUICK:
        if 'id="cat-%s"' % slug in src:
            items.append('      <a href="#cat-%s" style="--accent:%s"><span class="ic" aria-hidden="true">%s</span>%s</a>'
                         % (slug, color, icon, label))
    winter = ('\n    <p class="winter"><strong>Winter help:</strong> '
              '<a href="#cat-money">heating bills and free tax prep</a>, '
              '<a href="#cat-housing">shelter and rent help</a>. Call to confirm what is open now.</p>')
    return '\n    <nav class="quick" aria-label="Jump to a topic">\n%s\n    </nav>%s' % ("\n".join(items), winter)

def main():
    root = pathlib.Path(sys.argv[1])
    css = (root / "_tools" / "vibrant.css").read_text(encoding="utf-8").strip()
    for d in ["", "jamaica", "queens", "brooklyn", "manhattan", "bronx", "staten-island"]:
        p = root / "resources" / d / "index.html"
        src = p.read_text(encoding="utf-8")
        if START in src:
            a = src.index(START); b = src.index(END) + len(END)
            src = src[:a] + css + src[b:]
        else:
            src = src.replace("</style>", css + "\n</style>", 1)
        tiles = quick_html(src)
        src = QRE.sub("", src)
        marker = '<div class="g-method">'
        i = src.index(marker); j = src.index("</div>", i) + len("</div>")
        src = src[:j] + tiles + src[j:]
        p.write_text(src, encoding="utf-8")
        print("styled", p.relative_to(root))

if __name__ == "__main__":
    main()
