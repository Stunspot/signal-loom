# State, review, and correction

Use this reference when a project is ready for assessment or needs a correction. Commands run from the installed Signal Loom directory with Python 3.10+. Replace `my-story` with the path to your Loomfile; quote paths containing spaces.

## What the labels mean

| Stage | Required work |
|---|---|
| intake | Supported, parseable records; unresolved work may remain |
| spined | Nonempty story with unique beat and claim ids and known links |
| planned | Every beat has an earned representation or an explicit omission |
| built | Nonempty web index and a produced file for every requested output |
| reviewed | An actual current assessment with its material/output basis and evidence |
| approved_for_export | A passing current review and explicit matching approval; no blocking open issue |

`authority_status` records draft, reviewed or approved authority separately. A reviewed assessment may say `REVISE` or `BLOCKED`; the existence of a review never means the work passed. `publication_status` remains `manual_only`. Packing a draft is a backup operation, not an approval.

`project.yaml` contains JSON despite its filename. The current `loomfile_version` is `0.2.0`. A source manifest retains its separate `manifest_version: 0.1.0`; these version fields describe different records.

## Assess the work that exists

Start with a built Loomfile. Validate it and inspect the HTML. Perform the domain, rendered and accessibility reviews appropriate to its intended use; retain the actual observations and any missing evidence.

```bash
python scripts/validate_loomfile.py my-story
python scripts/inspect_infographic_html.py my-story/output/web/index.html
python scripts/capture_review_basis.py my-story my-story/review/basis-current.json
```

Capture writes a new file exclusively and changes no verdict or authority. Use a new filename if that file exists. Do not put a capture under `sources/`, `state/` or `output/`: those areas form the assessed material. If material changes during assessment, capture the final material again and assess that changed work.

Copy the entire captured object into `basis` in `review/diagnostics.json`. Fill the following fields from the assessment, not from a desired outcome:

| Field | Meaning |
|---|---|
| status | `PASS`, `PASS_WITH_CONDITIONS`, `REVISE` or `BLOCKED`; `not_run` before assessment |
| reviewer | The actual person or model conducting the stated review |
| intended_use | The exact use the assessment covers |
| evidence | Nonempty references to actual assessment records |
| top_three / secondary | Genuine finding objects; up to three in top_three |
| conditions | Conditions on the assessment, including missing evidence that changes use |
| unproved_layers | Specific evidence not established |

A finding or condition needs `id`, `statement`, `status` and boolean `blocking`. `status` is `open`, `met` or `accepted_residual`. A met item needs `resolution_evidence`. An accepted residual needs an `acceptance` object with actual `owner`, `intended_use` and `evidence`. High/critical open findings block approval even if marked nonblocking. `PASS_WITH_CONDITIONS` requires declared conditions or findings. Preserve earlier diagnostics with a new name or in history before recording a replacement assessment.

For example, an honest open condition is:

```json
{"id":"keyboard-review","statement":"Keyboard operation has not been exercised for the intended interactive use.","status":"open","blocking":true}
```

After recording a current assessment, set stage and authority to `reviewed` and run validation again. A pass checks the declared records and their consistency. It does not authenticate the reviewer, inspect the content of evidence references, establish factual truth, or confer permission.

## Record actual approval

Only after an accountable owner actually approves the stated use, set `approval` in `project.yaml` to their `owner`, `intended_use`, authority `evidence` and the captured `basis_sha256`. The use must exactly match the current review. Set `authority_status` to `approved` and, for export, `stage` to `approved_for_export`; validate again.

A passing review, current basis and absence of open blocking issues are required. An accepted residual must name the same accountable owner and use as the approval. No helper obtains consent for you. The teaching examples deliberately contain no human approval.

## Correct or migrate a project safely

For an old `0.1.0` Loomfile or a current reviewed project, choose a new destination outside the original:

```bash
python scripts/migrate_loomfile.py my-story my-story-corrected
```

The helper copies and verifies the original files, preserves the copied old project and review under `checkpoints/snapshots/prior-review-*`, then resets the new copy to intake/draft with a not-run review. The original folder is unchanged. Existing content, outputs and user notes remain available in the copy. Keep the original: the history folder holds the prior project/review, not a second complete copy of every old output.

Inspect `validation_errors` in the result; a completed copy can still need record corrections. Legacy files may lack source metadata, coherent ids, supported statuses or current review fields. Repair only the new copy. Unsupported versions are refused. Existing destinations, linked paths and destinations inside the source are refused.

Update source records, claims, narrative, representations and outputs together. Once inspected, advance to the stage the retained work actually earns, then perform a new assessment and obtain any required approval. The [worked correction](../examples/counts-and-rates/README.md) shows the entire path.

If copying fails, preserve the original and partial destination. A `.migration-incomplete.json` marker makes incomplete copies fail validation. Inspect that copy; choose a new destination for another attempt. Do not delete the marker to pretend an interrupted copy completed.

## What invalidates review

The basis includes project meaning (excluding workflow labels, approval and timestamps), all declared material JSON, the claim ledger, actual registered source files and every file under `output/`. It is a whole-project binding, not selective dependency tracking. Changing an output stylesheet or image invalidates it just as changing the HTML does.

Review records, decisions and checkpoint history are excluded so recording an assessment or a journal note does not invalidate it. JSON whitespace alone does not change normalized material records; source/output byte changes do. A manifest source checksum checks declared source consistency; neither that checksum nor an `as_of` label proves currentness or truth. `--skip-hashes` is diagnostic only and cannot qualify current review or approval.
