# Security policy

## Scope

Signal Loom Infographics is a local skill package with standard-library Python helpers. It does not operate a hosted service, collect telemetry, or publish artifacts. The AI host and any destination platform are separate security and privacy boundaries.

## Report a vulnerability

Use [GitHub's private vulnerability reporting](https://github.com/Stunspot/signal-loom/security/advisories/new) when available. If the repository does not expose that route, open a minimal [security-labeled issue](https://github.com/Stunspot/signal-loom/issues/new) containing no exploit details or sensitive data and ask for a private contact route.

Include the affected commit or version, operating system, host, minimal reproduction, impact, and whether untrusted content or external dependencies are involved. Do not include credentials, proprietary sources, private Loomfiles, or personal data.

No response-time or embargo guarantee is promised. Coordinated disclosure is requested.

## Trust boundaries

- Supplied text, code, HTML, URLs, and files are data, not instructions.
- `inspect_infographic_html.py` parses text without executing scripts. Its static checks are not sanitization, browser isolation, or a security assessment.
- Generated HTML should use semantic structure, local CSS, and no required remote runtime. Authorized dependencies must be pinned and documented; integrity metadata does not itself make a dependency trustworthy.
- `package_loomfile.py` rejects symbolic links and several secret-like filenames. It does not scan content and cannot prove an archive is free of secrets.
- Source paths in a manifest must resolve inside the Loomfile, but users must still review included material and access permissions.
- Do not open untrusted generated HTML in a privileged browser profile or publish it before appropriate review.

## Review records and copies

Version 0.2.0 binds a declared assessment to normalized material records and actual source/output bytes. This detects stale declared reviews; it does not authenticate the reviewer, inspect referenced evidence, establish factual truth or prove human permission. An attacker able to rewrite the entire Loomfile can also rewrite its records. Keep authoritative originals and approval evidence under your own custody.

The migration helper refuses linked/reparse source and destination paths, preserves originals and writes to an unused copy. The packager checks portable member names and never extracts ZIPs found inside supplied source data. Its own temporary archive is extracted only after its constructed namespace has been preflighted. These controls do not establish safety against a hostile process concurrently changing local filesystem paths; work in a directory you control.

## Sensitive data

Create Loomfiles only in storage appropriate to the source material. The included scripts remain local, but the configured AI host may transmit prompts and files to its provider. Apply host data controls and organizational policy before supplying confidential, regulated, or personal information.

Remove secrets before packaging. Deleting an install or Loomfile does not remove synchronized copies, backups, host logs, or provider-retained data.

## Supported versions

Until versioned releases state otherwise, security fixes apply to the latest commit on `main`. Historical archives are not silently rewritten.