# P46-M4 Result: Resume Governance

metadata_date: 2026-06-08
phase: P46-M4
Status: `PASS_P46_RESUME_GOVERNANCE`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | P46-M4 passed Claude resume-governance review after P46 code governance passed and focused P45/P46 gates passed locally. |
| Primary criterion status | The adapter repair is locally green and cross-agent reviewed; focused P45 historical blocker tests plus P46 positive adapter tests pass together. |
| Veto diagnostic status | No local regression was observed in P45 blocker classification, P45 closeout tests, or P46 multistate adapter tests. |
| Main uncertainty | The repair does not by itself create same-target CUT4--Zhao--Cui equality evidence for generalized SV, spatial SIR, or predator-prey. |
| Next justified action | Resume only the amended follow-up lane allowed by the P46 plan; keep P45 equality rows blocked until separate same-target gates exist. |
| Not concluded | No P45 equality promotion, no HMC readiness, no production score API, no adaptive TT-cross/SIRT reproduction, no paper-scale Zhao--Cui reproduction. |

## Evidence Contract

Question:

- After P46-M3 code governance pass, can the P45/P46 execution be resumed as an
  amended follow-up without overwriting P45 historical blocker results or
  promoting unsupported equality claims?

Baseline/comparator:

- P45 closeout result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p45-overnight-gated-self-recovery-execution-result-2026-06-08.md`
- P46 plan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p46-multistate-zhaocui-adapter-plan-2026-06-08.md`
- P46 code-governance result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p46-multistate-zhaocui-adapter-result-2026-06-08.md`

Primary pass criterion:

- P45 historical blocker tests and P46 adapter tests pass together.
- P46 is recorded as an amended follow-up, not a rewrite of P45 result claims.
- Resume claims are limited to the bounded multistate fixed-design TT adapter.

Veto diagnostics:

- Any attempt to reclassify P45 generalized-SV/SIR/predator-prey comparison
  rows as passed without same-target CUT4 and dense/refined reference gates.
- Any claim of HMC readiness, production score API, adaptive TT-cross/SIRT, or
  paper-scale Zhao--Cui reproduction.
- Any local regression in P45 blocker tests or P46 adapter tests.

## Skeptical Plan Audit

Status: `PASS_TO_CLAUDE_RESUME_REVIEW`.

- Wrong-baseline risk: P46 dense tensor-product fixtures validate a tiny
  adapter, not CUT4 equality for the P45 nonlinear targets.  Resume claims keep
  that distinction.
- Proxy-metric risk: finite TT values and branch hashes are not used as
  equality evidence; focused tests include dense tieout for the P46 adapter and
  blocker preservation for P45.
- Hidden-assumption risk: all axes are retained on a tensor-product grid, so
  the result does not imply high-dimensional scalability.
- Stale-context risk: P45 closeout remains `PASS_P45_OVERNIGHT_PROGRAM_COMPLETE`
  with promoted comparison rows equal to none.  P46 is a follow-up repair.

## Local Evidence

Focused P45/P46 resume gate:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p45_target_registry.py \
  tests/highdim/test_p45_multistate_zhaocui_route.py \
  tests/highdim/test_p45_generalized_sv_comparison_blocker.py \
  tests/highdim/test_p45_spatial_sir_comparison_blocker.py \
  tests/highdim/test_p45_predator_prey_comparison_blocker.py \
  tests/highdim/test_p45_cross_model_error_calibration.py \
  tests/highdim/test_p45_integration_closeout.py \
  tests/highdim/test_p46_multistate_zhaocui_adapter.py
```

Result:

```text
28 passed, 2 TensorFlow Probability deprecation warnings in 6.09s
```

Previously rerun P46 focused gates:

```text
tests/highdim/test_p46_multistate_zhaocui_adapter.py: 5 passed
tests/highdim/test_p45_multistate_zhaocui_route.py tests/highdim/test_p46_multistate_zhaocui_adapter.py: 8 passed
compileall bayesfilter/highdim and P46 tests: passed
git diff --check for P46 scoped files: passed
```

## Claude Review Evidence

P46-M3 bounded line-range code/governance review returned:

```text
PASS_P46_CODE_GOVERNANCE
```

The preceding packet-only probe returned `BLOCK_PACKET_SELF_CONTAINED`, which
was treated as a valid finding that implementation review required primary
line-range inspection, not as a Claude operational failure.

## Resume Classification

Allowed after Claude agreement:

- resume the execution as an amended P46 follow-up;
- use the multistate adapter as a new bounded implementation capability;
- plan future same-target comparison phases for generalized SV, spatial SIR,
  and predator-prey if they include separate CUT4/dense-reference gates.

Still blocked:

- P45 generalized-SV equality comparison;
- P45 spatial-SIR equality comparison;
- P45 predator-prey equality comparison;
- score/gradient/HMC promotion for P45 targets;
- adaptive TT-cross/SIRT or paper-scale Zhao--Cui reproduction.

## Requested Claude Verdict

Return exactly one of:

```text
PASS_P46_RESUME_GOVERNANCE
```

or

```text
BLOCK_P46_RESUME_GOVERNANCE
```

## Claude Verdict

Claude read-only resume-governance review returned:

```text
PASS_P46_RESUME_GOVERNANCE
```

Summary:

- P46 follow-up resume is correctly bounded.
- P45 generalized-SV, spatial-SIR, and predator-prey equality remain blocked.
- HMC, production score API, adaptive TT-cross/SIRT, and paper-scale
  reproduction remain nonclaims.
