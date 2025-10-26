<!-- SPDX-License-Identifier: MPL-2.0 -->
# ADR 0001: Repository Normalization

## Status
Accepted

## Context
The project contained ad-hoc tooling, multiple language runtimes, and missing governance files. Developers lacked a consistent way to bootstrap, lint, or test changes locally, leading to divergent practices and fragile automation.

## Decision
Adopt a standardized repository layout with:
- `src/` for Python packages following the src-layout
- `tests/` split into `unit`, `integration`, and `e2e`
- Tooling wrappers under `scripts/` with make targets mirroring CI
- Canonical documentation (README, CHANGELOG, CONTRIBUTING, CODE_OF_CONDUCT)
- Automation via GitHub Actions running `make check`, building container images, and publishing SBOM artifacts
- Metadata tracked in `project.yaml`

## Consequences
- Local developer experience aligns with CI expectations
- Security scanning and SBOM generation are automated
- Future services can reuse the same scripts/Makefile without bespoke changes
- Non-standard components (Flutter, PWA, browser extension) remain in `apps/` with documentation about their divergence
