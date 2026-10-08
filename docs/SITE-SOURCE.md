# Site source and boundaries

This directory is the complete static source for `https://stunspot.github.io/signal-loom/`.

## Runtime

- `index.html` is the customer journey.
- `404.html` is the repository-specific recovery page.
- `style.css` contains the local responsive visual system.
- `assets/signal-loom-pages-hero.png` is the 1200×800 Pages hero.
- `assets/signal-loom-social-card.jpg` is the deployable 1731×909 Open Graph/social card (308,051 bytes).
- `assets/signal-loom-social-card.png` is the lossless source master and is not wired to social metadata because it exceeds the social upload limit; the current master is 1731×909 and 2,635,725 bytes.
- The README uses the separate 1600×720 `assets/signal-loom-readme-hero.png`.
- There is no JavaScript, remote font, analytics, telemetry, form, iframe, or required third-party runtime.

## Visual provenance

The README hero, Pages hero, and social card are separately generated raster artworks created for Signal Loom Infographics, then sized for their specific surfaces. They are not produced by repository code. The social card visibly contains the exact product title and the line "Makes source-bound infographics from research and data." The 2026-10-03 display-name edit replaced the social-card lettering with the exact title **Signal Loom Infographics**, retained the descriptive line, and regenerated the JPG from the reviewed PNG master. The earlier visual-approval hashes describe historical bytes, not these current assets.

## Content boundary

The site explains product purpose, audience, capabilities, limits, Codex and Claude Code installation, verification, first use, workflow, outputs, configuration, troubleshooting, recovery, update, removal, data cleanup, privacy, network behavior, security, accessibility limits, provenance, support, contribution, license, and evidence status. The repository customer guide remains the detailed operational reference.

The live repository and live site must be checked after deployment. A source file, successful local check, workflow transcript, or HTTP 200 does not by itself establish rendered quality, navigation behavior, correct live assets, accessibility conformance, or publication success.

## Correction and example navigation

The 0.2.0 page adds a literal Corrections navigation target with the copy command and links to the completed example and review reference. The actual teaching Loomfiles live in the complete product under `examples/`; this Pages source links to their repository lesson instead of pretending the repository source viewer renders local HTML. Download/extract the package to open those infographics with their attached source links.

## Accessibility boundary

The source includes semantic regions, one `h1`, ordered headings, alt text, a skip link, visible keyboard focus, reflow layouts, horizontally scrollable stage content, and reduced-motion treatment. These are source-level properties. Formal accessibility conformance requires separate rendered keyboard, zoom/reflow, contrast, screen-reader, and assistive-technology testing.