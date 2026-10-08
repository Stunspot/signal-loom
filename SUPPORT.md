# Support

Signal Loom Infographics is community-supported through [GitHub Issues](https://github.com/Stunspot/signal-loom/issues).

Before opening an issue:

1. identify the exact commit or package version;
2. run `python scripts/self_check.py`;
3. reproduce with the smallest non-sensitive source or Loomfile possible;
4. state the host, operating system, Python version, command, exact output, and which evidence layer failed;
5. check the [customer guide](docs/CUSTOMER-GUIDE.md#troubleshooting-and-recovery).

For a legacy-format or stale-review message, preserve the original and use the [copy-first correction procedure](docs/STATE-AND-REVIEW.md#correct-or-migrate-a-project-safely). Include the declared Loomfile version and the exact validator error in a support report. Do not clear a review condition or incomplete-copy marker merely to obtain a pass.

If a copy was interrupted, retain the original and partial destination; record whether `.migration-incomplete.json` exists. If archive commit was interrupted, leave any surviving output untouched until its custody and contents are known. A new destination lets you continue without overwriting evidence.

Use one of these classifications:

- package construction or installation;
- host discovery or invocation;
- Loomfile initialization or validation;
- HTML inspection or packaging;
- documentation or Pages defect;
- accessibility issue;
- security issue (follow [SECURITY.md](SECURITY.md), do not disclose exploit details publicly).

Do not attach private sources, credentials, proprietary Loomfiles, or personal data. A public issue is public. There is no guaranteed response time, service-level agreement, private consulting entitlement, factual-review service, or emergency channel.