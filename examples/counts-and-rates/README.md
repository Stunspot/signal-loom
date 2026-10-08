# Make a count comparison, then correct it

This worked example is for a first-time Signal Loom user with Python 3.10+ and a browser. It teaches how supplied evidence becomes a story, a visual, a bounded review, and a later correction. Every survey value is fictional.

## Start with the result

Open [the original infographic](original/output/web/index.html) in a browser from this extracted package. On GitHub, download the package or HTML first; GitHub's source viewer does not render the infographic. Read the count chart and the missing-denominator explanation. Then open [the corrected infographic](corrected/output/web/index.html): North changes from 120 to 108 after twelve duplicate responses are removed. South remains 90 and West 60. The participation-rate conclusion stays unknown.

The key judgment is useful restraint: the count chart is earned, while a participation-rate ranking is not. Refusing the entire infographic would discard a valid comparison. Inventing populations would manufacture the answer.

## Follow the evidence into the picture

| Open | What to look for |
|---|---|
| [Original CSV](original/sources/originals/responses.csv) and [scope note](original/sources/originals/source-note.md) | Common survey window, fictional values and absent denominators |
| [Claim ledger](original/state/claims.jsonl) | Distinct illustrative measurements, an inferred comparison and the limit |
| [Story](original/state/spine.json) | Observation → tempting inference → missing denominator → bounded conclusion → next evidence |
| [Visual plan](original/state/visual-plan.json) | Zero-based count chart plus prose; rate chart and map rejected for specific reasons |
| [Infographic](original/output/web/index.html) | Visible fictional label, common scale, exact table and no invented rate |
| [Review](original/review/diagnostics.json) | Actual scope, captured basis, conditions and unproved layers; no human approval |

From the installed product root, run:

```bash
python scripts/validate_loomfile.py examples/counts-and-rates/original
python scripts/inspect_infographic_html.py examples/counts-and-rates/original/output/web/index.html
```

Expected: declared-state and static HTML checks pass. Missing social metadata may produce warnings because this local teaching artifact has no supplied publication URL or thumbnail. Those warnings are not permission to invent URLs.

## Make your own correction copy

Use an unused path outside the original. Do not edit the shipped examples in place.

```bash
python scripts/migrate_loomfile.py examples/counts-and-rates/original ./my-count-correction
```

Expected: `source_unchanged` is true, the new copy is intake/draft, and `validation_errors` is empty for this supplied example. Open its `user-notes.md`: the reader's note remains. Open the reported history path: the prior review and project remain historical, not current approval.

Read the supplied [correction note](corrected/sources/originals/correction.md) and [corrected CSV](corrected/sources/originals/responses-corrected.csv). In your copy, add those source files, register their actual bytes, and revise the count claim, total, chart, caption and table together. Retain the original CSV and denominator warning. Compare your result with the supplied corrected copy; do not blindly replace your work with it.

Once the revised artifact is built, follow [State, review, and correction](../../docs/STATE-AND-REVIEW.md#assess-the-work-that-exists) to capture its current basis and record your actual assessment. A source edit or output edit makes the earlier basis stale. A new journal note alone does not.

## Know when you are done

Your original is intact, your note and prior review survive, the current visible count and source agree, the missing rate evidence stays visible, and validation matches the stage actually reached. Package a draft or reviewed copy to a new ZIP if you need a backup; the ZIP preserves that state. Human export approval and public publication remain separate.

This is an authored teaching example, not a record of representative-user success. Its review files state the checks actually performed. The four changed values are North's count, its bar length, the total and the correction notice; the supported conclusion does not become a rate ranking.
