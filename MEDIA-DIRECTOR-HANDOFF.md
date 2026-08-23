# GUS Website & Donations — Media Director Handoff

**For:** Arnau Sagrera-Barnet (info@velorfilms.com)

Welcome aboard, Arnau. Here is everything you need to manage the GUS web presence.

## What you have access to

**1. The website (GitHub)**
- Repo: https://github.com/augustokennedy-byte/guswithus
- You will get an invite by email. Accept it, then you can edit from the repo
  page in any browser. No software needed.
- The homepage is `index.html`. To edit text: open the file on github.com,
  click the pencil icon, make your changes, then "Commit changes". The live
  site updates within about a minute.
- There are two other pages, `about/index.html` and `contact/index.html`, plus
  a `404.html` for broken links.
- Every change is saved in history and reversible, so you cannot break anything
  permanently. Images live in `assets/` (Add file, then Upload files).

**2. Donations (Zeffy)**
- You will get a member invite to our Zeffy account by email.
- Zeffy is where donation forms, event ticketing, and donor receipts live. You
  can create campaign forms, export donor lists, and see totals.
- Bank and payout settings stay admin-only (Gus).

## House rules
- Brand colors: green #22A95A and blue #0848A2. They are set as variables at
  the top of each HTML file (`--green`, `--blue`), so never hard-code new colors.
- Tagline stays: "Where Potential Meets Purpose."
- Donation messaging always leads with: 100% of donations reach our programs
  (Zeffy charges us nothing).
- Big changes (new sections, redesigns): talk to Gus first.

## Things that are easy to break

- **Social links appear in three places** (homepage footer icons, homepage
  contact list, and the about and contact pages). If a handle changes, update
  all of them, and update the `sameAs` list in the JSON-LD block at the top of
  `index.html`. Google reads that block to connect the accounts to the org.
- **The share image** is `assets/og-image.png`, sized 1200x630. It is what
  people see when they post a GUS link. If you replace it, keep those exact
  dimensions and keep the filename the same.
- **The redirect folders** (`gus-with-us/`, `donate/`, `privacy-policy/` and
  five others) exist to catch links from the old Wix site that are still in
  Google. They are not real pages. Leave them alone.
- **`sitemap.xml`** lists the three real pages. If you add a page, add it there
  too.

## Still open

- The site has no privacy policy or terms page. The old Wix URLs for them are
  currently redirected to the about page. Worth writing real ones.
- A YouTube channel has been planned but not created. Setup steps are in the
  Content folder.

## Quick reference
- Website repo: https://github.com/augustokennedy-byte/guswithus
- Live site: https://www.guswithus.org
- Donations: zeffy.com (log in with your invited email)
- Questions: info@guswithus.org
