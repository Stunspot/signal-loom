# Validation and evidence boundaries

Signal Loom Infographics 0.2.0 supports a source-to-infographic workflow and recoverable corrections. The commands in Run local checks establish bounded local behavior. An executed result applies only to the candidate and environment recorded with it; this file is not a claim that every command ran for every installation.

## Run local checks

From the installed product root with Python 3.10+:

```bash
python scripts/self_check.py
python -m unittest discover -s tests -v
python scripts/inspect_infographic_html.py docs/index.html
python scripts/validate_loomfile.py examples/counts-and-rates/original
python scripts/validate_loomfile.py examples/counts-and-rates/corrected
```

The native suite exercises legitimate intake and completed state against empty advanced stages, unsupported or malformed records, broken claim/story links, changed output resources, stale review, approval conditions, copy preservation and interruption, and packaging preservation. Synthetic release tests exercise namespace and payload behavior without standing in for the actual final release.

## What the checks establish

The self-check checks named product resources, display/invocation identity, declared hosts and schema JSON. The Loomfile validator checks its implemented fields and relationships, source checksums and whole-project review consistency. Schema files are reference shapes; the validator does not execute a general JSON Schema engine.

The HTML inspector parses source without running scripts. A static pass does not prove rendering or accessibility. The teaching example retains its actual assessment and limitations under each Loomfile's `review/` directory. The example was authored by the builder, not produced by a representative-user trial.

The Loomfile packager preflights portable names, rejects linked paths and named secret-like files, hashes exact streamed file bytes, validates its extracted archive, preserves required empty directories and the original project, and refuses existing or concurrent outputs. A final-link interruption leaves any surviving destination for custody inspection. Supplied source ZIPs stay opaque; a filename denylist does not scan contents for secrets.

The complete product builder packages its intentional source list into one installable root for both supported hosts. After an accepted release, `verify_release.py EXTRACTED_ROOT` compares exact file and directory inventory and file bytes to the embedded manifest. That manifest establishes consistency, not an authenticated signature or working host integration.

## Keep the remaining claims separate

Factual accuracy, present-day currentness, domain judgment, representative-user success, fresh-host discovery/invocation, rendered layout, keyboard and screen-reader use, formal accessibility conformance, security, professional fitness, authenticated approval, publication and platform performance each need their own evidence. A structural pass proves none of them.

If a check fails, retain its actual error and the affected work. Classify whether the deliverable, test, tool or environment failed before repairing it. Follow [State, review, and correction](docs/STATE-AND-REVIEW.md) for a stale review or legacy format, and [the customer guide](docs/CUSTOMER-GUIDE.md#troubleshooting-and-recovery) for installation or packaging recovery.

Historical verification remains repository history; it is not current evidence for the new review/migration contract. Current readiness and actual final release verification are recorded separately after the candidate is frozen and independently challenged. A package or source check alone is never a release-readiness claim.
