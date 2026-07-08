# Manual Adjoint Phase 7 Result: Return-To-P82 Validation Handoff

Date: 2026-06-22

Status: P82_RETURN_BLOCKED_BY_BENCHMARK_WIRING_PASSED_AFTER_CLAUDE_R2_AGREE

## Evidence Contract

| Field | Result |
|---|---|
| Question | Is there enough reviewed evidence to hand P82 a bounded streaming actual-gradient route candidate and preserve the 13-point FD comparator protocol? |
| Baseline/comparator | M2-M6 parity/memory evidence, P82 FD-only correction, P82 full-AD route correction, and the current P82 benchmark wiring. |
| Primary criterion | Blocked: the M6 manual streaming route is reviewed locally, but the P82 SIR d18 benchmark path does not expose or forward `transport_gradient_mode`, so exact executable P82 commands cannot honestly be stated. |
| Veto diagnostics | Raw full-AD N10000 route not reintroduced; P82 FD protocol preserved; tiny M6 memory-shape evidence not treated as N10000 feasibility; M6 not described as Zhao-Cui source-faithful evidence. |
| Explanatory diagnostics | Handoff records route metadata, supported/unsupported modes, current wiring gap, and non-executable candidate command shape after a future wiring patch. |
| Not concluded | P82 has not resumed; no P82 FD agreement, N10000 feasibility, GPU/TF32 evidence, HMC/default/posterior/scientific-superiority readiness, or Zhao-Cui source-faithfulness. |

## Skeptical Plan Audit

- Wrong baseline: controlled.  P82 remains FD-only same-scalar LEDH consistency;
  Zhao-Cui is not used as comparator evidence.
- Proxy promotion: controlled.  M6 tiny parity and empty returned transport
  matrix are not promoted to N10000 feasibility.
- Missing stop condition: resolved by writing `P82_RETURN_BLOCKED_BY_BENCHMARK_WIRING`.
- Unfair comparison: no comparison run is launched in M7.
- Hidden assumption: surfaced.  The P82 benchmark path cannot currently select
  the manual streaming transport gradient mode.
- Environment mismatch: no GPU command is run in M7.
- Artifact adequacy: the handoff records exact candidate command shape only as
  non-executable until wiring exists.

Audit result: M7 must block P82 return rather than claiming readiness.

## Findings

The M6 route is available in:

- `batched_annealed_transport_core_tf`, via
  `transport_gradient_mode="manual_streaming_finite_sinkhorn_stopped_scale_keys"`.

The current P82 benchmark path goes through:

- `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py`;
- `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py`;
- `streaming_batched_ledh_pfpf_ot_value_core_tf`.

That path exposes `transport_plan_mode` and `transport_ad_mode`, but it does
not expose `transport_gradient_mode`.  The streaming value core calls the
batched transport core with:

```text
transport_gradient_mode="raw"
```

Therefore a governed P82 actual-gradient command for the M6 manual streaming
route cannot yet be executed.

## Artifacts

Wrote the handoff:

- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-p82-validation-handoff-2026-06-22.md`

Refreshed the M8 subplan:

- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase8-closeout-code-doc-audit-subplan-2026-06-22.md`

## Checks

Command:

```bash
git diff --check -- docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-*.md
```

Status:

- passed before M7 R1 review.

Claude M7 R1 one-path review then returned `VERDICT: REVISE` only because this
section still said the check was pending.  No other material blocker was
identified in that review.

Claude M7 R2 one-path review returned `VERDICT: AGREE`, finding no material
blocker to closing M7 as `P82_RETURN_BLOCKED_BY_BENCHMARK_WIRING` and advancing
to M8 closeout.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
|---|---|---|---|---|---|
| Block P82 return at M7 | Failed readiness: benchmark wiring missing | No forbidden P82 run launched; raw full AD remains forbidden | Whether the manual streaming route remains feasible once wired into the full SIR d18 benchmark path | Write a narrow P82 wiring subplan before any validation | No P82 FD agreement, N10000 feasibility, GPU evidence, or production readiness |

## Handoff

M8 may proceed to close out the manual-adjoint program as a partial success with
a concrete downstream blocker:

```text
P82_RETURN_BLOCKED_BY_BENCHMARK_WIRING
```

The next active work should be a separate P82 wiring phase that adds and tests
`transport_gradient_mode` propagation through the benchmark path.  Do not run
P82 validation before that wiring phase passes local checks and review.
