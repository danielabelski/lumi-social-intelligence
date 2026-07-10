# Documentation

This directory contains the public-facing documentation for **Lumi Social Intelligence**.

## Start here

- [Product brief](product-brief.md) — concise product framing.
- [Architecture](architecture.md) — how **Lumi Layered Memory**, **Nuances**, and **Presence** work together.
- [Release boundary](release-boundary.md) — what may and may not enter the release repository.
- [Host compatibility](host-compatibility.md) — host-neutral contract and current adapter status.
- [Licensing](licensing.md) — code, documentation, and branding license model.
- [Release checklist](release-checklist.md) — pre-publication gate.
- [Module release gates](module-release-gates.json) — package names and fail-closed module promotion rules.

## Module export audit

Before promoting a private module candidate into `core/`, run the audit command in
read-only mode and review the JSON report:

```bash
python3 scripts/audit_module_export.py \
  --module "Presence" \
  --source /path/to/private/candidate \
  --report /tmp/presence-export-audit.json
```

The command does **not** copy files. It only compares the candidate tree against
`docs/module-release-gates.json` and blocks raw runs, private runtime state,
logs, secrets, and files outside the public export allowlist.

## Naming rule

Public-facing docs should use the product names:

- **Lumi Layered Memory**
- **Nuances**
- **Presence**

Use folder names only when discussing repository paths.
