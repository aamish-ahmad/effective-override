# Reproducibility

This repository is intended to function as a public research artifact with committed inputs and committed derived outputs.

## Included

- synthetic source datasets
- model response ledgers used in the public release
- integrated result tables
- metrics JSON files
- audit files
- baseline ladder outputs
- robustness outputs

## Local Reproduction Surface

The release can be re-run locally for integration and analysis without API calls by using the scripts under `repro/`, the integration entry points, and the analysis scripts under `scripts/`.

## Scope

The final analysis layer is deterministic over the committed local files. API runner scripts remain in the repository for completeness, but the public release does not require API execution to inspect the reported outputs.

## Environment Notes

Optional local environment loading is documented in [local_env_setup.md](/C:/Users/chuwi/Desktop/Artifacts_all/agency-trajectory-benchmark/docs/local_env_setup.md).
