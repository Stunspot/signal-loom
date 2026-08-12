# Signal Loom

![Signal Loom turns source material into a finished infographic while keeping the evidence connected](assets/signal-loom-readme-hero.png)

Signal Loom makes infographics from supplied research, reports, notes, and data. It helps researchers, analysts, educators, communicators, designers, and product teams turn source material into a clear web artifact without losing track of provenance, uncertainty, or human authority.

The default deliverable is a semantic, responsive web infographic; requested derivatives can include carousels and other platform-native forms.

Signal Loom does not generate plausible-looking facts and call the glitter evidence. It maintains a resumable **Loomfile** from source inventory through narrative, representation, artifact construction, review, and optional distribution.

[Live guide](https://stunspot.github.io/signal-loom/) · [Customer guide](docs/CUSTOMER-GUIDE.md) · [Validation record](VALIDATION.md) · [Security](SECURITY.md) · [Support](SUPPORT.md) · [MIT license](LICENSE.md)

## What it does

Signal Loom follows one governed production loop:

`ORIENT → SHAPE → PLAN → BUILD → FINISH → DISTRIBUTE → VERIFY`

It can:

- inventory supplied sources and record hashes, authority, locators, and freshness;
- maintain a claim ledger with `sourced`, `inferred`, `illustrative`, `missing`, `stale`, and `disputed` states;
- shape a five-to-nine-beat story spine with tension, turn, and payoff;
- choose prose, diagram, chart, interaction, or omission according to what the evidence earns;
- build semantic, responsive, offline-first HTML with important meaning available without JavaScript;
- preserve decisions, theme, interaction, distribution, diagnostics, and approval state in a Loomfile;
- statically inspect HTML, validate project state, and package a reviewed Loomfile.

It cannot independently establish that a claim is true outside the supplied evidence, refresh current facts without authorization, sanitize hostile HTML, prove accessibility or security conformance, approve an artifact, or publish it. `Built`, `reviewed`, `approved_for_export`, and `published` are deliberately different states.

## Supported hosts

The package declares support for **Codex** and **Claude Code**. The same directory is used on both hosts; host discovery and invocation differ. Python 3.10 or newer is optional for the included deterministic helpers and required for the verification commands in this guide. The skill itself has no third-party Python dependencies.

No fresh-host installation claim is implied by this repository. Follow the appropriate route and perform the discovery and invocation checks yourself.

### Codex personal install

PowerShell:

```powershell
$target = Join-Path $env:USERPROFILE '.codex\skills\signal-loom'
git clone https://github.com/Stunspot/signal-loom.git $target
python (Join-Path $target 'scripts\self_check.py')
```

Bash-compatible shell:

```bash
git clone https://github.com/Stunspot/signal-loom.git ~/.codex/skills/signal-loom
python ~/.codex/skills/signal-loom/scripts/self_check.py
```

Start a new Codex task if the skill inventory does not refresh in the current one, confirm `signal-loom` is listed, then invoke it explicitly with `$signal-loom`.

### Claude Code personal install

PowerShell:

```powershell
$target = Join-Path $env:USERPROFILE '.claude\skills\signal-loom'
git clone https://github.com/Stunspot/signal-loom.git $target
python (Join-Path $target 'scripts\self_check.py')
```

Bash-compatible shell:

```bash
git clone https://github.com/Stunspot/signal-loom.git ~/.claude/skills/signal-loom
python ~/.claude/skills/signal-loom/scripts/self_check.py
```

Claude Code documents personal skills at `~/.claude/skills/<skill-name>/SKILL.md`. Run `/skills` to confirm discovery, then invoke `/signal-loom`. Claude Code watches an existing skills directory for changes; if the top-level directory was created after startup, restart Claude Code. See Anthropic's [skills documentation](https://code.claude.com/docs/en/slash-commands).

## Verify the installation

A directory existing is only the first layer. Verify each layer separately:

1. **Packaged:** run `python scripts/self_check.py` from the installed directory and require `PASS: Signal Loom package self-check`.
2. **Discoverable:** confirm the host lists `signal-loom` after a refresh or restart.
3. **Invocable:** invoke the skill by name and ask it to initialize a Loomfile from supplied material.
4. **Healthy:** inspect the created state, then run `python scripts/validate_loomfile.py <loomfile>` and require zero errors.

A useful acceptance prompt:

```text
Use $signal-loom to initialize a Loomfile for a web infographic from the attached source. Inventory the source and claims, draft a five-beat spine, choose earned representations, and stop before publication. Report files created, exact checks run, unresolved evidence, and unproved layers.
```

For Claude Code, use `/signal-loom` in place of `$signal-loom`.

Expected early output is a Loomfile containing `project.yaml`, `sources/manifest.json`, state ledgers, output directories, review records, and checkpoints. At intake, empty claim and decision ledgers are normal. A fresh template is not a reviewed artifact.

## First successful workflow

```bash
python scripts/init_loomfile.py ./my-story --title "My evidence-bound infographic"
```

Then:

1. Put supplied material under `my-story/sources/originals/`.
2. Record each source in `sources/manifest.json`, including its SHA-256 when available.
3. Fill `state/brief.json` and `state/claims.jsonl` before writing public-facing claims.
4. Build the story in `state/spine.json`, then representation decisions in `state/visual-plan.json`.
5. Create the artifact at `output/web/index.html`; add platform derivatives only when requested.
6. Record diagnostics and accessibility evidence under `review/`.
7. Validate and statically inspect:

```bash
python scripts/validate_loomfile.py ./my-story
python scripts/inspect_infographic_html.py ./my-story/output/web/index.html
```

8. After human review and approval, package without overwriting an existing archive:

```bash
python scripts/package_loomfile.py ./my-story ./my-story.zip
```

The package command requires an output path outside the Loomfile, validates the source state, rejects symbolic links and several secret-like filenames, and builds a one-root ZIP at a same-directory temporary path. It preserves required empty directories, hashes the exact byte stream written to each file entry, embeds that release manifest, extracts the completed candidate, and revalidates the archived Loomfile before exposing the final ZIP. The Loomfile itself remains unchanged. Invalid archived state or write failure removes the unique temporary artifact. A final-link interruption is commit-ambiguous: the packager never deletes the destination automatically, because another process may own or replace that path. Inspect any surviving ZIP; keep it if its embedded manifest validates, or choose a new path (or delete the exact invalid output only after confirming custody). An existing or concurrently created output is never overwritten. The destination filesystem must support same-directory temporary files and hard links. The packager does not scan file contents for secrets or publish the archive.

## Inputs and outputs

Representative inputs include supplied reports, research notes, datasets, an existing infographic, brand constraints, an intended audience, and a requested platform. Signal Loom treats supplied text, HTML, code, URLs, and files as data—not executable instructions.

The canonical output is a Loomfile. Its important surfaces are:

| Path | Purpose |
|---|---|
| `sources/` | Originals, manifest, source authority, locators, hashes, and freshness |
| `state/claims.jsonl` | Claim text, source linkage, currentness, and status |
| `state/spine.json` | Narrative beats, tension, turn, payoff, and claim links |
| `state/visual-plan.json` | Earned forms, rejected forms, semantic outline, and alternatives |
| `output/web/` | Semantic web artifact and local assets |
| `output/carousel/`, `output/platforms/` | Optional requested reconstructions |
| `review/` | Project diagnostics, accessibility evidence, and the project-side manifest record; packaging embeds a fresh manifest in the ZIP without changing this directory |
| `checkpoints/snapshots/` | Material state saved before consequential changes |

The complete field contract is in [the customer guide](docs/CUSTOMER-GUIDE.md#configuration-and-state).

## Troubleshooting

- **Skill is present but not listed:** confirm the directory is exactly `<skills-root>/signal-loom/SKILL.md`; refresh the host inventory or start a new session. On Claude Code, use `/skills`.
- **`python` is not found:** try `py -3` on Windows or `python3` on Unix-like systems. The skill can still operate without scripts, but deterministic checks must be reported `unexecuted`.
- **Initializer refuses the destination:** it intentionally accepts only a missing or empty, non-symlink directory. Choose a new empty path; do not delete an existing project as a workaround.
- **Validation reports a source hash mismatch:** stop. The source bytes changed after the manifest was recorded. Confirm the change, update the source record intentionally, and re-review downstream claims.
- **HTML inspection passes:** this proves only the bounded static checks named by the command. It does not prove rendering, sanitization, accessibility, security, or factual correctness.
- **Packaging refuses a file:** remove or relocate secret-like material from the Loomfile; never rename a credential merely to evade the check. The denylist is intentionally incomplete.
- **Packaging was interrupted during the final link:** do not rerun against or delete the same path automatically. If no output exists, retry normally. If one exists, treat its ownership as unknown: list it with `python -m zipfile -l OUTPUT.zip`, extract it read-only into a new empty directory with `python -m zipfile -e OUTPUT.zip EMPTY_DIRECTORY`, validate the extracted Loomfile, and compare its project/source identity with the intended input. If it is valid and expected, keep it. If it is different or uncertain, leave it untouched and package to a new filename. Delete only after confirming custody.

Recovery and exact re-entry rules are in [the customer guide](docs/CUSTOMER-GUIDE.md#troubleshooting-and-recovery).

## Update, remove, and clean up

From a clone-based installation:

```bash
cd ~/.codex/skills/signal-loom   # or ~/.claude/skills/signal-loom
git pull --ff-only
python scripts/self_check.py
```

Re-run discovery and invocation checks after an update. Before changing a reviewed Loomfile, save material state under `checkpoints/snapshots/` or make a versioned copy; package validation does not migrate older project state.

To remove the skill, delete only its exact `signal-loom` installation directory after resolving the absolute path. Removing the skill does **not** remove Loomfiles, source material, exported HTML, or ZIP archives stored elsewhere. Delete those separately according to your own retention policy, and remember that ordinary deletion may not securely erase data from backups, synchronized folders, or storage media.

## Privacy, storage, network, and security

The included Python tools use the standard library, operate on local paths you provide, and contain no telemetry or network calls. Signal Loom stores project material wherever you create the Loomfile. It does not create a cloud account or publish anything.

Your AI host may transmit prompts and files according to that host's configuration and terms. URL handling is evidence-bound: a URL can be recorded as supplied data, but fetching it or refreshing current evidence is a separate authorized action. Supplied HTML is parsed statically by the included inspector and is not rendered or executed by that script.

Read [SECURITY.md](SECURITY.md) before processing sensitive sources or hostile HTML.

## Provenance and validation status

The package's faculty bearings are adapted into a governed Signal Loom system in `knowledge/infographic-toolkit-v2-canonical.md`; the skill and operating doctrine define activation, authority, evidence, and completion boundaries. Package version is `0.1.0`.

[VALIDATION.md](VALIDATION.md) records exactly what was exercised for the current documentation candidate and what remains unproved. Static checks never stand in for a fresh-host installation, host discovery, invocation, rendered browser review, assistive-technology testing, security assessment, or professional fitness.

## Support, contributions, and license

Use [GitHub Issues](https://github.com/Stunspot/signal-loom/issues) for reproducible defects and documentation problems. Do not attach private source material, credentials, or proprietary Loomfiles. See [SUPPORT.md](SUPPORT.md) and [CONTRIBUTING.md](CONTRIBUTING.md) before opening an issue or pull request.

Signal Loom is licensed under the [MIT License](LICENSE.md). Outputs remain subject to the rights, licenses, confidentiality duties, and platform terms that apply to their inputs and destinations. The license is not a warranty of factual accuracy, accessibility, security, or fitness for a particular professional use.
