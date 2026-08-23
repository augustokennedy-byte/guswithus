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

Skip link, semantic landmarks, one `h1` per page, labeled nav with
`aria-expanded`, visible focus rings, AA contrast, alt text, reduced-motion
support, and 44px minimum tap targets on mobile.
