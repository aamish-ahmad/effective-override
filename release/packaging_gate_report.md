# Packaging Gate Report

## Scope

Repository: `effective-override`  
Release target: `v1.0.0`

## Public Safety

Status: `PASS`

Committed files were checked for forbidden public wording, real API key patterns, and excluded local files. The release surface was kept free of `.env` files, `CODEX_TASK` files, and older excluded pilot materials.

## README and Metadata

Status: `PASS`

The release-facing metadata now uses:

- project name: `Agency Trajectory Benchmark`
- stable version: `v1.0.0`
- relative markdown links suitable for GitHub
- paper-in-preparation wording without a public PDF placeholder

## Reproduction

Status: `WARN`

The repository includes no-API reproduction scripts and committed derived outputs. A prior local Bash/WSL run reported a shell-path issue for `python`, which is an environment warning rather than a data-integrity problem.

## Results Consistency

Status: `PASS`

Release-facing wording was kept aligned with the committed metrics and summaries. No JSON or CSV metrics were changed for this metadata pass.
