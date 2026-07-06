# GUS Website — guswithus.org redesign

Premium, mobile-first, accessible homepage for **GUS — Growth, Unity & Success, Inc.**
Everything lives in one file: `index.html` (plus `assets/gus-logo.jpg`). No build step needed.

## Preview it
Double-click `index.html`, or serve the folder:
```
python3 -m http.server 8000 --directory "/Users/gus/Documents/GUS Growth Unity & Success/Website"
```
then open http://localhost:8000

## Connect Zeffy (free donations — 3 steps)
1. Create a free account at https://www.zeffy.com and build a **Donation form**
   (Fundraising → Donation forms → Create). Zeffy charges nonprofits $0 — no platform
   or transaction fees, so 100% of each gift reaches GUS.
2. **Quick option (works immediately):** copy your form's public link
   (Share → Copy link) and paste it into the `href` of the
   "Donate securely on Zeffy" button in `index.html` (search for `zeffy.com`).
3. **Embedded option (donors never leave the page):** in Zeffy go to
   Share → Embed and copy the URL that looks like
   `https://www.zeffy.com/embed/donation-form/XXXXXXXX`.
   In `index.html`, find the comment block labeled `ZEFFY SETUP`, delete the
   `.zeffy-cta` div, and uncomment the `<iframe>`, pasting your embed URL as its `src`.

## Publish
- **Replace the Wix site:** most direct path is to host this file on Netlify / Vercel /
  GitHub Pages (all free) and point the guswithus.org domain at it, or
- **Keep Wix:** recreate the sections in Wix using this page as the spec (copy, colors,
  order, and CTAs are all final).

## Brand system used
- Green `#22A95A` (accents, energy) · darkened to `#15803D` when used as text for WCAG AA contrast
- Blue `#0848A2` (trust, headings, primary buttons) · ink navy `#0B2447`
- Fonts: Sora (headlines) + Inter (body), via Google Fonts
- Tagline: "Where Potential Meets Purpose"

## Accessibility included
Skip link, semantic landmarks, one `h1`, labeled nav/menu button with `aria-expanded`,
visible focus rings, AA color contrast, alt text, reduced-motion support, keyboard-friendly.
