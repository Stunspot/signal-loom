# Signal Loom site source

The static project site is published from this `docs/` directory.

## Source and evidence boundary

The site describes the public contest edition in this repository. Its product claims are derived from:

- `SKILL.md`;
- `knowledge/operating-doctrine.md`;
- `knowledge/claim-and-currentness-doctrine.md`;
- `knowledge/representation-and-chart-integrity.md`;
- the included Loomfile initialization, validation, HTML inspection, and packaging tools.

The page does not claim that static inspection proves security or accessibility conformance, that a built artifact is reviewed or approved, that approved export means publication, that the product invents missing evidence, or that every host can install the standalone source independently.

## Files

- `index.html` — semantic single-page project overview;
- `style.css` — responsive presentation and accessibility treatment;
- `assets/signal-loom-hero.png` — generated 1600×900 raster hero artwork;
- `.nojekyll` — direct static-file serving marker.

## Deployment

`.github/workflows/deploy-pages.yml` uploads this directory with GitHub's official Pages Actions. Repository Pages must be configured to use **GitHub Actions** before the first deployment can publish.

## Review notes

The page uses one H1, semantic landmarks, a skip link, visible keyboard focus, descriptive links, meaningful alternative text, responsive layout, and reduced-motion handling. These checks support structural accessibility only; they are not a claim of formal accessibility conformance, browser coverage, security, professional fitness, or representative-user success.
