# Adversarial verification

Date: 2026-08-12
Candidate fingerprint: 1187defe54242e7e705868ebea1ba71ece6e8dde877c98eecd801867c5b5540a
Documentation fingerprint: e81e5ee4c62ec44be7767e5ff7c1a2319f0699e8d6b609dcc0f37ca9077db59a
Presentation fingerprint: 7ad424dc3649cd144fc610800a013cff0cc5a8a225e128d3068a47de455af4a3
Verdict: PASS_LOCAL with post-deployment rendered verification required.

Challenges and results:

- Product buried: repaired. The README opens with **Signal Loom makes infographics** and immediately names inputs and output.
- README exists but does not orient: repaired. A visitor can now identify fit, install, prove discovery/invocation/health, make a first infographic, recover, and find deeper guidance without reading an internal verification narrative first.
- Wide viewport or browser zoom collapses content: repaired in source. The outer content width no longer combines a fixed cap with viewport-growing internal padding. The focused regression rejects the exact failed rule.
- Narrow viewport: source geometry retains a 1rem gutter and mobile grid breakpoints; the computed content width is 288 pixels at a 320-pixel viewport.
- Unsupported capability inflation: rejected. The README preserves manual publication, evidence authority, static-check, security, accessibility, and factual limits.
- Broken navigation: rejected. Local file and same-page fragment checks pass; both HTML files pass bounded inspection.
- Unrelated work: preserved. The untracked docs/assets/signal-loom-social-card.jpg is not staged or modified.

Thirteen unit tests, package self-check, both HTML inspections, eight Hesperos lint passes, local link/fragment checks, exact TestForge line-ending verification, and diff hygiene pass. The remaining decisive check is the corrected live render in the browser state that produced the screenshot.