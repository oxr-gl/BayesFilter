# DPF V2 Algorithm Full BF/FilterFlow Live Gated Execution Launch Compatibility Amendment

metadata_date: 2026-06-08
status: LAUNCH_COMPATIBILITY_REPAIR_READY

## Context

Initial live run:

- run_id: `dpf-v2-algorithm-full-comparison-live-20260608-012548`
- run_dir: `docs/plans/logs/dpf-v2-algorithm-full-comparison-live-20260608-012548`

The supervisor stopped during P0 worker launch before any phase execution or
Claude phase review. Every P0 worker iteration failed with the installed Codex
CLI rejecting:

```bash
codex exec --ask-for-approval never
```

Observed error:

```text
error: unexpected argument '--ask-for-approval' found
```

## Repair

The installed `codex exec --help` exposes `--full-auto` for non-interactive
low-friction sandboxed execution. The live supervisor now invokes phase workers
with:

```bash
codex exec --cd "$ROOT" --sandbox workspace-write --full-auto ...
```

## Evidence Scope

This repair changes only the Codex worker launcher syntax. It does not weaken
the human-risk override, phase gates, Claude read-only review, CPU-only
TensorFlow rule, `.localsource/filterflow` no-mutation policy, no-student rule,
or no-oracle rule.

## Decision

Relaunch should use a fresh run id. The failed run remains a launcher
compatibility artifact, not a P0 scientific or governance result.
