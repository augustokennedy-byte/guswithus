# guswithus.org

The public website for **GUS — Growth, Unity & Success, Inc.**
Static HTML, no build step. Hosted on GitHub Pages, served over HTTPS at
https://www.guswithus.org.

## Structure

```
index.html          Homepage (all sections, inline CSS + JS)
about/index.html    About page, legal identity, EIN, determination date
contact/index.html  Contact details and social accounts
404.html            Branded not-found page (GitHub Pages serves this automatically)
robots.txt          Points crawlers at the sitemap
sitemap.xml         The three real pages
favicon.ico         Browser tab icon
assets/             Logos, founder photo, social share card
CNAME               www.guswithus.org
.nojekyll           Tells GitHub Pages to serve files as-is
```

Eight single-file redirect folders (`gus-with-us/`, `about-us/`, `donate/`,
`programs/`, `contact-us/`, `terms-and-conditions/`, `privacy-policy/`,
`accessibility-statement/`) catch URLs from the old Wix site that Google still
has indexed and send visitors to the right page. Leave them in place until
Search Console shows no traffic on them.

## Preview locally

```
python3 -m http.server 8000
```

Then open http://localhost:8000. Run it from this folder.

## Publish

Commit to `main` and push. GitHub Pages redeploys in about a minute.
Repo: https://github.com/augustokennedy-byte/guswithus

## Brand system

- Green `#22A95A` for accents, darkened to `#15803D` when used as text (WCAG AA)
- Blue `#0848A2` for headings and primary buttons, ink navy `#0B2447`
- Fonts: Sora for headlines, Inter for body, loaded from Google Fonts
- Tagline: "Where Potential Meets Purpose"

Colors are CSS variables at the top of each file (`--green`, `--blue`). Never
hard-code a new color.

## Images

Source logo is `assets/gus-logo.jpg` (1201px). The sized PNGs used by the site
(`logo-32`, `logo-180`, `logo-192`, `logo-512`) are generated from it with the
white background knocked out, so the mark sits flush on any background.
`assets/og-image.png` is the 1200x630 card that appears when someone shares a
link. Regenerate these if the logo ever changes.

## Donations

Donations run through Zeffy, which charges nonprofits nothing. The homepage
embeds the live form as an iframe and falls back to a direct link if the embed
fails to load. PayPal and Venmo are offered as secondary options.

## Search and social

Each page carries a canonical URL, Open Graph and Twitter card tags, and a
share image. The homepage also carries `NGO` structured data (JSON-LD) with the
EIN, address, phone, founder, service area, and the four programs. About and
contact carry breadcrumb data. Validate changes at
https://validator.schema.org and https://search.google.com/test/rich-results.

## Accessibility

Target is **WCAG 2.2 Level AA**, which is the yardstick used for ADA and
Section 508 claims. The public statement lives at `/accessibility/` and is
linked from every footer. `accessibility-statement/` redirects to it.

Skip link on every page, semantic landmarks, one `h1` per page, labeled nav
with `aria-expanded`, alt text, reduced-motion support, and 44px minimum tap
targets on mobile.

Two rules that are easy to break by accident:

- **Focus indicator** is `outline:3px solid #0B2447` plus a
  `box-shadow:0 0 0 6px rgba(245,179,1,.95)` halo. The dark ring carries the
  contrast on light backgrounds, the gold halo carries it on dark ones. The
  old gold-only ring was 1.88:1 against white and failed. Do not swap it back,
  and do not add `outline:none` to any focusable element.
- **`--green` (#22A95A) is not a text background.** White on it is 3.05:1.
  Use `--green-dark` (#15803D, 5.02:1 against white) for anything with text
  on it. `--green` is fine for bars, ticks, and decoration.

In the Resource Center: borough chips are links and carry `aria-current`,
category chips are buttons and carry `aria-pressed`. Do not use `aria-pressed`
on a link, it is not a valid attribute for that role. The result count
(`#tally`) is `role="status"` so filtering is announced.

## Preferred source badge

Every footer carries a link to
`https://www.google.com/preferences/source?q=www.guswithus.org`, which lets a
reader mark GUS as a preferred source in Google Search. This is the deeplink
form on purpose. Google also ships a JavaScript button
(`news.google.com/swg/js/v1/publisher.js`), and we do not use it, because the
Resource Center must not load a third-party script that could observe someone
looking up a domestic violence hotline.
