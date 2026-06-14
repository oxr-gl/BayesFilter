# P46 Result: Multistate Zhao-Cui Fixed-Design TT Adapter

metadata_date: 2026-06-08
phase: P46
Status: `PASS_P46_RESUME_GOVERNANCE`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | P46 implementation reached local evidence pass for the bounded multistate adapter; Claude line-range code review returned `PASS_P46_CODE_GOVERNANCE`; Claude resume-governance review returned `PASS_P46_RESUME_GOVERNANCE`. |
| Primary criterion status | Local P46 value/replay/shape tests passed for tiny dim-2 and dim-3 fixtures against dense tensor-product references. |
| Veto diagnostic status | No local target-mismatch, scalar fallback, TensorFlow-backend, whitespace/compile, or Claude code-governance veto was observed. |
| Main uncertainty | P46 validates only a tiny fixed-design multistate adapter, not P45 generalized-SV/SIR/predator-prey equality or production score/HMC readiness. |
| Next justified action | Resume only the amended follow-up lane allowed by the P46 plan; keep P45 equality rows blocked until separate same-target gates exist. |
| Not concluded | No overnight resume, no P45 generalized-SV/SIR/predator-prey equality promotion, no HMC readiness, no production score API, no adaptive TT-cross/SIRT reproduction. |

## What Was Implemented

- Added `multistate_nonlinear_fixed_design_tt_value_path` in
  `bayesfilter/highdim/filtering.py`.
- Added multistate adjacent target builders, all-axes retained-grid helpers,
  multistate predictive propagation, and multistate retained moment helpers.
- Kept `scalar_nonlinear_fixed_design_tt_value_path` unchanged so historical
  scalar-only blocker tests remain valid.
- Exported new symbols from the highdim subpackage only.
- Added `tests/highdim/test_p46_multistate_zhaocui_adapter.py`.

## Evidence Contract Outcome

The P46 evidence contract allowed only a bounded adapter repair.  It did not
allow promotion of P45 generalized SV, spatial SIR, or predator-prey equality
without separate same-target reference and CUT4 gates.

Local implementation evidence supports the bounded adapter repair:

- dim 2: order-7 dense tensor-product tieout;
- dim 3: order-5 dense tensor-product tieout, because order 7 hit the fitter
  condition-number veto under current tiny-fixture caps;
- deterministic branch replay;
- retained all-axes grid shape and density-hash checks;
- scalar route rejection remains covered by P45 tests.

## Local Commands

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p46_multistate_zhaocui_adapter.py
```

Result: 5 passed, 2 TensorFlow Probability deprecation warnings.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p45_multistate_zhaocui_route.py tests/highdim/test_p46_multistate_zhaocui_adapter.py
```

Result: 8 passed, 2 TensorFlow Probability deprecation warnings.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim tests/highdim/test_p46_multistate_zhaocui_adapter.py
```

Result: passed.

```bash
git diff --check -- bayesfilter/highdim/filtering.py bayesfilter/highdim/__init__.py tests/highdim/test_p46_multistate_zhaocui_adapter.py docs/plans/bayesfilter-highdim-zhao-cui-p46-multistate-zhaocui-adapter-plan-2026-06-08.md
```

Result: passed.

## Claude Review Loop

Plan review:

- Iteration 1 returned `PASS_P46_PLAN_GOVERNANCE`.

Code/governance review:

- Attempt 1: direct `claude -p` full implementation review; no output after
  repeated polls, stopped as operational hang.
- Attempt 2: direct `claude -p` narrower exact-path review; no output after
  repeated polls, stopped as operational hang.
- Attempt 3: direct `claude -p` review over compact code-review packet; no
  output after repeated polls, stopped as operational hang.
- Attempt 4: `claudecodex` `claude_worker.sh` review over compact
  code-review packet; no output after repeated polls, stopped as operational
  hang.

Because the user requested Claude code review before resuming the overnight
execution, Codex did not launch the P45/P46 resumed overnight run.

Recovery after claudecodex review-probe repair:

- The generic Claude read-only probe skill was added to `claudecodex` and
  committed as `d5cddf3`.
- The P46 code-review packet was patched from a packet-only summary to a
  bounded line-range review request with exact files/ranges, current local
  evidence, pass/block criteria, and nonclaims.
- Probe ladder:

```text
CLAUDE_PROBE_OK
CLAUDE_PACKET_READ_OK
BLOCK_PACKET_SELF_CONTAINED
```

Interpretation: Claude was operational, and the packet-only block correctly
identified that implementation correctness required primary code/test range
inspection.

Bounded line-range review:

```text
PASS_P46_CODE_GOVERNANCE
```

Claude findings:

- scalar route preservation passed;
- reviewed P46 implementation path is TensorFlow/TensorFlow Probability only;
- reference-measure, coordinate-Jacobian, and uniform-reference-density factors
  are internally consistent in the reviewed path;
- retained axes, shape checks, density hashes, and branch identities are
  explicit enough for the tiny adapter;
- dim-2/order-7 and dim-3/order-5 evidence remains bounded and non-promotional;
- no adaptive TT-cross/SIRT, paper-scale Zhao--Cui, score API, HMC, GPU, or
  high-dimensional scalability claim is made.

## Artifacts

- Plan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p46-multistate-zhaocui-adapter-plan-2026-06-08.md`
- Code-review packet:
  `docs/plans/bayesfilter-highdim-zhao-cui-p46-code-review-packet-2026-06-08.md`
- Resume-governance result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p46-resume-governance-result-2026-06-08.md`
- Result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p46-multistate-zhaocui-adapter-result-2026-06-08.md`

Status: `PASS_P46_RESUME_GOVERNANCE`.
