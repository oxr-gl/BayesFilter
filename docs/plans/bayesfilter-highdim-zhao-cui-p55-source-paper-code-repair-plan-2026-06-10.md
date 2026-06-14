# P55 Repair Plan: Source/Paper/Code Conformance

metadata_date: 2026-06-10
program: P55-zhao-cui-paper-source-code-conformance
status: REVIEWED_AFTER_CLAUDE_LOOP
supervisor: Codex
reviewer: Claude Code read-only

## Task Decomposition

This artifact covers task 2 of the requested workflow:

1. use the reviewed P55 discrepancy audit;
2. create an implementation repair plan;
3. review the plan with Claude Code read-only until convergence or max five
   rounds;
4. only then execute the reviewed plan.

The fixed/fixed-gradient branch remains legitimate.  This plan does not remove
or penalize that branch.  It only prevents fixed-variant necessity from being
used as a substitute for source-route implementation.

## Binding Source-Anchor Policy

Before any Zhao--Cui lane implementation can be called source-faithful, the
phase must cite both:

1. the Zhao--Cui paper section/equation or reviewed paper note; and
2. the author source file and line-level operation under
   `third_party/audit/zhao_cui_tensor_ssm_p10/source`.

Each implementation choice must be classified as:

- `source_faithful`: matches the cited paper/source operation;
- `fixed_hmc_adaptation`: preserves the author's algorithmic route while
  freezing randomness, ranks, bases, schedules, or samples for HMC
  differentiability;
- `extension_or_invention`: not present in the author paper/source and not
  allowed to close source-faithfulness gaps without explicit user approval.

Missing anchors or a reviewer approval based only on internal coherence must
block with `BLOCK_SOURCE_UNGROUNDED`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What executable implementation work can close the highest-priority non-fixed-variant discrepancies without drifting from the Zhao--Cui paper/source route? |
| Baseline/comparator | P55 discrepancy audit; P48/P49/P54 source contracts; `full_sol.m`, `pre_sol.m`, `ssmodel.m`, `computeL.m`, and TT/SIRT source behavior. |
| Primary pass criterion | Add real source-route implementation substrate for target construction, finite-pruned recentering, transport-object protocol, retained sampling, proposal correction, and one-step result accounting, with tests. |
| Veto diagnostics | Any implementation copies MATLAB; any source-faithfulness claim lacks paper and author-source anchors; any fixed branch is relabeled as author-adaptive source reproduction; any local-neighborhood/all-grid route is used as the P55 repair; any helper-only patch is claimed to complete full sequential fixed/source-contract filtering. |
| Explanatory diagnostics | Focused pytest, compile check, diff check, and Claude execution review. |
| Not concluded | Complete sequential fixed/source-contract filtering, paper-scale SIR, predator-prey preconditioned production, generalized-SV source route, smoothing, and HMC readiness. |

## Skeptical Plan Audit

Status: PASS_FOR_REVIEW.

- Wrong baseline risk: the plan follows `full_sol` / `pre_sol` operation order,
  not P53 local-neighborhood rank scaling or all-grid retained propagation.
- Source-anchor risk: any future implementation phase must re-open the cited
  author source and paper anchors before adding new source-route behavior.
  Otherwise it must emit `BLOCK_SOURCE_UNGROUNDED`.
- Dependency risk: retained sampling and proposal correction depend on a fitted
  transport object; therefore the first implementation target is a transport
  object protocol and analytic test transport, not fake retained samples.
- Fixed-variant carveout risk: fixed-design/HMC code is left intact and
  separately labeled.  It cannot satisfy the P55 source-route pass criteria.
- Proxy metric risk: protocol tests certify only the one-step source substrate;
  they do not certify production fixed-transport fit quality or paper-scale model
  readiness.
- Artifact adequacy risk: every executed phase must write a result note.

## Phase Plan

| Phase | Discrepancy relationship | Implementation scope | Files | Pass criterion | Non-claims |
| --- | --- | --- | --- | --- | --- |
| P55-M1 | Partially repairs D06 and creates a protocol prerequisite for fixed transport integration.  Does not attempt author-adaptive TT/SIRT parity. | Add first-class `SourceRouteTarget` and `SourceRouteTransportProtocol` contracts.  Provide a tiny analytic Gaussian test transport used only as a lower-rung reference. | `source_route.py`, new tests | Target object combines unshifted negative log target, shift, frame, determinant policy, source terms, and fitted-transport protocol validates manifest/inverse/log-density/log-normalizer methods. | No author-adaptive TT/SIRT parity claim |
| P55-M2 | Partially repairs D05. | Repair `source_route_recenter` to match `computeL` finite pruning semantics before weights are normalized. | `source_route.py`, recenter tests | NaN/Inf sample columns and matching weights are removed; all-invalid or zero-mass cases fail clearly; clean batches keep previous behavior. | No source filter loop |
| P55-M3 | Partially repairs D07 and D08 only for protocol-backed analytic/reference transports. | Integrate retained sample generation and proposal correction around the transport protocol. | `source_route.py`, sample/proposal tests | A one-step result object samples reference points, maps by inverse transport and affine frame, evaluates proposal log density, applies true target correction, records ESS, and returns normalizer contribution. | No production fixed-transport fitting; no full source filter |
| P55-M4 | Adds a one-step boundary that exercises part of D01 at `t=1`; explicitly does not repair D01 sequential loop or D02 retained-object marginalization. | Add a one-step source reapproximation boundary for `t=1` only.  It must refuse `t>1` until retained-object marginalization is implemented. | `source_route.py`, new tests | One-step boundary wires target, transport, retained samples, correction, and normalizer.  Two-step/sequential claims are blocked with an explicit missing-marginalization error. | D01 and D02 remain open for sequential filtering |
| P55-M5 | Claim-control and drift-guard work for D10, D11, D16. | Strengthen execution result claims and drift guards. | docs/tests | Result artifact records fixed-variant carveout, local-neighborhood/all-grid quarantine, clean-room no-copy status. | No substantive source-route repair or paper-scale claims |

## Deferred Follow-On Phases

These are real discrepancies but are not honest to claim as fixed by this P55
implementation pass:

| Deferred item | Discrepancies | Next required plan |
| --- | --- | --- |
| Sequential source filter and previous retained-object marginalization for `t>1` | D01, D02 | P55 only adds a `t=1` boundary. P56 or P57 must implement retained-density marginalization and multi-step filtering tests. |
| Production fixed-transport integration | fixed-gradient requirement, D06-D08 substrate | P55 only adds the protocol prerequisite. P56 or P57 must integrate the fixed/HMC-compatible transport path with dense/analytic references and fit diagnostics. |
| Source preconditioned route | D09, D14 | Later plan after unpreconditioned one-step and sequential route pass. |
| Spatial SIR source route | D13 | Later ladder after sequential route exists. |
| Generalized-SV source transforms | D12 | Separate target-equality audit/test plan. |
| Smoothing | D15 | Separate smoothing plan only if requested. |

## Excluded Non-Goals

| Excluded item | Reason |
| --- | --- |
| Author-adaptive TTIRT/TTSIRT fit parity | Excluded from future missing-gap lists because BayesFilter requires a fixed/fixed-gradient HMC-compatible branch.  The implementation may preserve the author route as a comparator or historical anchor, but it is not a required repair target. |
| Adaptive Zhao--Cui filtering requirements | Excluded unless the user explicitly requests a separate non-HMC historical reproduction study. |

## Implementation Rules

- Use TensorFlow/TFP for BayesFilter-owned differentiable code.
- Do not copy MATLAB source code.
- Keep source-route code separate from the fixed-gradient branch.
- Preserve unrelated dirty worktree changes.
- New tests must fail if source-route retained sampling is attempted without a
  transport object exposing the required methods.
- New tests must fail if `t>1` source reapproximation is claimed without a
  previous retained-object marginalization implementation.

## Planned Validation

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p55_source_route_target_transport.py \
  tests/highdim/test_p55_source_route_one_step.py \
  tests/highdim/test_p49_source_route_sample_proposal.py \
  tests/highdim/test_p49_source_route_recenter_normalizer.py \
  tests/highdim/test_p54_source_route_drift_audit.py \
  tests/highdim/test_public_api_highdim.py
```

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q \
  bayesfilter/highdim/source_route.py \
  bayesfilter/highdim/__init__.py \
  tests/highdim/test_p55_source_route_target_transport.py \
  tests/highdim/test_p55_source_route_one_step.py
```

```bash
git diff --check -- \
  bayesfilter/highdim/source_route.py \
  bayesfilter/highdim/__init__.py \
  tests/highdim/test_p55_source_route_target_transport.py \
  tests/highdim/test_p55_source_route_one_step.py \
  docs/plans/bayesfilter-highdim-zhao-cui-p55-source-paper-code-discrepancy-audit-2026-06-10.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p55-source-paper-code-repair-plan-2026-06-10.md
```

## Claude Review Request

Claude should review this plan read-only and return:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```

Review for dependency errors, source drift, fixed-variant carveout mistakes,
overclaims, and whether the execution scope is real implementation rather than
governance-only.
