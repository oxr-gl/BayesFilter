# P8d Gate 2 Implementation Review Subplan

Date: 2026-06-14

Status: `CODEX_REVIEWED_READY_FOR_BOUNDED_READONLY_REVIEW_AFTER_GATE1_RERUN`

## Question

Can P8d proceed from focused local validation to the CPU-only full benchmark run without unresolved implementation, artifact, or boundary-safety blockers?

## Boundary Contract

Claude may be used only as a read-only reviewer. Claude is not an execution authority and cannot authorize crossing human, runtime, model-file, funding, product-capability, or scientific-claim boundaries. Codex remains responsible for local checks, visible patches, final go/no-go decisions, and stopping if a boundary is reached.

The review prompt must not paste whole files. It may name file paths, line ranges, symbols, and the prior findings. Claude may inspect only the targeted local files:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-visible-repair-execution-plan-2026-06-13.md`
- `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`
- this Gate 2 subplan

## Review Scope

Claude should check only for blocking issues in:

- consistency with the P8d reset memo and visible repair plan;
- correctness of P8d metadata, command manifest, and artifact paths;
- preservation of true not-applicable cells versus real route gaps;
- DPF value-only five-seed contract and no DPF score/Hessian promotion;
- exact Kalman scope limited to LGSSM/KSC surrogate policy;
- spatial SIR score/Hessian staying `not_applicable_no_free_theta`;
- CPU-only full-run readiness after local checks;
- sufficient artifact coverage for the final result note.

Previous Claude implementation findings already patched:

- stale P8c summary title;
- true not-applicable cells counted as real gaps;
- tests did not guard that accounting.

## Stop And Loop Rules

If Claude returns `VERDICT: AGREE`, Codex will independently verify that the local focused checks still pass and then proceed to Gate 3 evidence-contract recording.

If Claude returns `VERDICT: REVISE` with a fixable blocker, Codex will patch the same P8d lane visibly, rerun focused local checks, and then rerun bounded review. High or max effort is reserved for material unresolved issues. Stop after five rounds for the same blocker.

If review does not converge or a blocker requires package installation, network fetch, credentials, GPU use, detached execution, destructive git action, new algorithmic implementation, product-capability claims, or a scientific-claim boundary crossing, write a blocker result and stop for human direction.

## Planned Local Checks Before And After Any Patch

```bash
env CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py
```

```bash
env CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py
```

```bash
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-visible-repair-execution-plan-2026-06-13.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-gap-closure-plan-2026-06-13.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-gate1-focused-validation-result-2026-06-14.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-gate2-implementation-review-subplan-2026-06-14.md scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py
```

## Planned Claude Command Shape

Use the trusted worker wrapper with a bounded prompt and no pasted whole-file content:

```bash
timeout 90s bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name p8d-implementation-review-r2 --model sonnet --effort low "<bounded prompt>"
```

## Codex Subplan Review

Status: `PASS`.

The subplan has a narrow baseline, explicit stop conditions, no proxy promotion criterion, no full-run execution authority for Claude, no GPU requirement, and concrete artifacts for the next gate. It preserves the reset memo's order: local checks, read-only implementation review, evidence contract, full CPU-only run only if review converges, and post-run audit.

