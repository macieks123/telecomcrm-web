# Telecom CRM website

Landing page for **[www.telecomcrm.com](https://www.telecomcrm.com)** — Telecom CRM, the AI-native CRM, CPQ and Order Management platform built by TriarIT. TriarIT brand colours and logo; copy as on the live site (29 Sep 2026).

## Structure

```
index.html            # The page. Self-contained: CSS inline, TriarIT logos inline as SVG. Deploy this.
favicon.svg           # Favicons, linked from index.html as /favicon.svg etc.
favicon-32.png
apple-touch-icon.png
assets/               # TriarIT logo files for other uses (not referenced by the page)
  triarit-mark.svg, triarit-mark-512.png
  triarit-logo-horizontal-light-bg.svg, triarit-logo-horizontal-dark-bg.svg
src/                  # Source for index.html
  page.template.html  # Markup and CSS; edit this, not index.html
  build.py            # Generates index.html (logo sprite, TM Forum API cards, <head> meta)
  logo-*.inline.txt   # Logo SVG bodies extracted from TriarIT_logo_master.pdf
```

## Editing

1. Change `src/page.template.html` (or the TM Forum API list and `<head>` meta in `src/build.py`).
2. Run `python3 src/build.py` (Python 3, no dependencies).
3. Commit both the template and the regenerated `index.html`.

## Deploying

Static site, no build step at deploy time: serve the repository root from any static host (GitHub Pages, Netlify, Cloudflare Pages, a bucket). `src/` and `assets/` can be served or excluded; the page does not need them.

## Before go-live

1. **Legal footer (art. 206 KSH).** A sp. z o.o. website must show registry court, KRS number and share capital. Add them to the footer line marked with a `TODO` comment in `src/page.template.html`, then rebuild.
2. **Social preview image.** `og:image` still points to the existing `https://www.telecomcrm.com/og.png`, which is in the old teal style. Replace it with a TriarIT-branded 1200×630 image.
3. **Fonts.** Montserrat, IBM Plex Sans and IBM Plex Mono load from Google Fonts. For an EU site, self-hosting the font files is the safer choice (German courts have ruled against loading Google Fonts without consent).

## Brand rules used

- Colours: grey `#838787`, blue `#34A5DA`, magenta `#D22DF6`; charcoal `#232526` panels match the TriarIT presentation template.
- The three brand colours fail WCAG AA as small text on white, so blue is used for fills, rules and icons, with dark text on blue buttons. Text-safe shades for coloured text: blue `#1A74A3`, magenta `#9A1CC0`, grey `#626768`.
- The violet-to-magenta logo gradient is used once, in the hero headline.
- Header lockup: TriarIT mark + "Telecom CRM" + "by TriarIT". Full TriarIT logo in the "Built by" section and the footer.
- Light and dark mode follow the visitor's system setting.

---

TriarIT Sp. z o.o. · ul. Grzybowska 87, 00-844 Warsaw, Poland · office@triarit.com · [www.triarit.com](https://www.triarit.com)
