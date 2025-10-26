<!-- SPDX-License-Identifier: MPL-2.0 -->
# MSK-IO

MSK-IO is an offline-first medical imaging pipeline that combines DICOM ingestion, segmentation, multimodal retrieval, and LLM-based reasoning. The project now follows a standardized repository layout so teams can bootstrap, test, and deploy consistently across environments.

## Repository Layout

```
.
├── apps/                     # Prototype Flutter/PWA/browser-extension clients
├── assets/                   # Offline Chromium bundle and other large assets
├── configs/                  # Tooling configuration (lockfiles, commitlint, templates)
├── data/                     # Workspace for local datasets (gitignored)
├── docs/                     # Whitepaper, ADRs, and system maps
├── infra/                    # Helm charts and infrastructure manifests
├── scripts/                  # Task shims wrapping Make targets and CI flows
├── src/                      # Python package (src-layout)
├── tests/                    # Unit, integration, and e2e suites
├── Dockerfile                # Container image for running the API
├── Makefile                  # Canonical task runner
└── project.yaml              # Machine-readable metadata
```

Legacy tooling (e.g., `bootstrap_chromium.py`, `full_setup.sh`) is still available for air-gapped deployments but the new scripts under `scripts/` should be preferred.

## Quickstart

```bash
# Clone and enter the repository
git clone https://example.org/msk-io.git
cd msk-io

# Bootstrap toolchain and install hooks
scripts/bootstrap

# Run the full local quality gate
scripts/check

# Launch the development API server (http://localhost:8000)
scripts/dev
```

When operating offline place a Chromium archive at `assets/resources/chromium/chromium.tar.xz` and run `bootstrap_pipeline.py` to extract the binary before invoking the main pipeline.

## Developer Tasks

| Task | Description |
| --- | --- |
| `scripts/bootstrap` | Create a virtual environment, install dependencies, and configure pre-commit hooks. |
| `scripts/dev` | Start the FastAPI service with hot reload. |
| `scripts/lint` | Run Ruff, Black, and isort; pass `--fix` to auto-correct lint issues. |
| `scripts/fmt` | Format code with Black, isort, and Ruff formatter. |
| `scripts/typecheck` | Execute mypy in strict mode. |
| `scripts/test` | Run unit and integration tests with coverage. |
| `scripts/e2e` | Execute end-to-end scenarios under `tests/e2e`. |
| `scripts/coverage` | Generate coverage reports in the terminal and XML. |
| `scripts/build` | Build Python artifacts via `python -m build`. |
| `scripts/package` | Confirm build artifacts exist (wheel/sdist). |
| `scripts/release` | Build artifacts and run `twine check` for release validation. |
| `scripts/update-deps` | Regenerate `configs/python/requirements-lock.txt` using pip-tools. |
| `scripts/security-scan` | Run Bandit, pip-audit, and detect-secrets scans. |
| `scripts/sbom` | Produce a CycloneDX SBOM with pip-audit. |
| `scripts/gen-docs` | Generate API documentation into `docs/api/` using pdoc. |
| `scripts/migrate` | Run database migrations when a `migrations/` directory is present. |
| `scripts/clean` | Remove build artifacts, caches, and generated reports. |
| `scripts/check` | Execute linting, type checking, tests, coverage, and security scan sequentially. |

Every script has a PowerShell counterpart (e.g., `scripts/lint.ps1`) so Windows developers can participate without WSL.

## Observability and Compliance

- Logging configuration lives in `src/msk_io/utils/log_config.py` and enables structured output.
- Metrics are exposed via the FastAPI application and can be scraped by Prometheus.
- Security scanning is automated via GitHub Actions (`.github/workflows/ci.yml`) and locally with `scripts/security-scan`.
- SBOM artifacts are generated into `sbom/` and uploaded during CI.

## Documentation

Additional architecture notes live under `docs/`:

- `docs/WHITEPAPER.md` – pipeline deep dive
- `docs/adr/` – decision records (starting with ADR 0001 for the normalization work)
- `docs/system-map.md` – high-level system topology diagram

## Support

Questions, bug reports, and feature requests can be filed via GitHub issues or directed to the owners listed in `project.yaml`.

## License

MSK-IO is distributed under the [Mozilla Public License 2.0](LICENSE). Any modifications to MPL-covered files must be shared under the same license, while larger aggregations can remain under separate terms when the MPL files are left unmodified. For details, review the LICENSE file.

## Credits

Please retain this project's [NOTICE](NOTICE) file when redistributing MSK-IO. The project acknowledges all contributors listed via Git history and documents third-party components in NOTICE.

