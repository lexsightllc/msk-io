<!-- SPDX-License-Identifier: MPL-2.0 -->
# Contributing Guide

## Getting Started

1. Clone the repository.
2. Run `scripts/bootstrap` to create a virtual environment, install dependencies, and configure pre-commit hooks.
3. Use `scripts/dev` to launch a live-reload API server during development.

## Development Workflow

- Create feature branches from `main`.
- Follow Conventional Commit messages (`type(scope): description`).
- Use the scripts in `scripts/` or `make <target>` to run checks locally before pushing.
- Ensure new features include unit tests and, where appropriate, integration or end-to-end coverage.
- Update documentation in `docs/` and `project.yaml` when behavior changes.

## Pull Requests

- Describe changes clearly and reference relevant issues.
- Update `CHANGELOG.md` under the `Unreleased` section.
- Verify `scripts/check` passes locally.
- Expect automated CI to run linting, type checking, security scans, tests, and SBOM generation.

## Code Review

- Reviewers should focus on correctness, maintainability, and security.
- Suggested improvements can be requested; blocking issues must include clear reasoning.
- Maintainers merge once quality bars are met and CI is green.

## Licensing of Contributions

By submitting a contribution you agree that it will be licensed under the [MPL-2.0](LICENSE), matching the outbound license of the project. Please ensure new files include an "SPDX-License-Identifier: MPL-2.0" header so that inbound and outbound terms remain aligned.

