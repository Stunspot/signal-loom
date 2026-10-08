# Release maintenance

This topic is for the product maintainer. Customers should begin with [the customer guide](CUSTOMER-GUIDE.md) or [the completed example](../examples/counts-and-rates/README.md).

## Select and finish the candidate

Version 0.2.0 expands the record and return workflow from the accepted 0.1.1 promise: current material/output review binding, coherent record relationships, and copy-first migration. Keep `signal-loom` as the invocation/technical identity and Signal Loom Infographics as the display name. Preserve the canonical faculty toolkit and existing artwork.

Finish source, docs, current sidecars and examples before freezing. Use the existing TestForge process for a bounded readiness claim with independent documentation and technical challenge. A product defect ends that candidate cycle. Actual release archives and custody digests belong after acceptance, explicit release intent and confirmation that source is unchanged.

## Build the accepted release once

Choose a new output path outside the source repository:

```bash
python scripts/build_release.py PRODUCT_SOURCE NEW_OUTPUT.zip
```

The builder selects the named root files plus agents, assets, docs, examples, fallbacks, knowledge, schemas, scripts, tests and current delivery sidecars. It omits Git data, caches, historical verification, earlier releases and superseded sidecars. Empty example directories are included so the complete example survives extraction. Source files are not changed.

The archive has one `signal-loom-v0.2.0` root, supported by both Codex and Claude Code when installed as `signal-loom`. It includes `product-release.json`, an exact payload manifest. No host-specific dependency or runtime service is required. Installation/discovery/invocation still need their own observation.

Extract into a fresh directory with the host's ordinary archive tool, then run:

```bash
python -B EXTRACTED_ROOT/scripts/verify_release.py EXTRACTED_ROOT
python -B EXTRACTED_ROOT/scripts/self_check.py
python -B EXTRACTED_ROOT/scripts/validate_loomfile.py EXTRACTED_ROOT/examples/counts-and-rates/corrected
```

Verify before allowing tools to add caches: the release verifier expects the exact extracted payload and directories. `-B` avoids Python bytecode directories. If other tools have already changed that extraction, use a new extraction rather than deleting unknown files to make a checksum pass.

## Deliver the complete current product

Carry accepted source through the existing repository/release/Pages channel, applicable current installations and Nova consumers. Keep the complete ZIP, unchanged appropriate artwork, current install prompt and current Extra together on the governed shelf, and reconcile its catalog and existing Library card. Shelf state does not prove Discord upload or live publication. Final Nova parent releases follow their coordinated edition acceptance.

If an output already exists, the builder refuses it. A hard-link error may leave a completed output; inspect it and its custody without overwriting. A material source change invalidates the prior seal and requires a new accepted candidate. Historical archives stay preserved outside current installable cargo.
