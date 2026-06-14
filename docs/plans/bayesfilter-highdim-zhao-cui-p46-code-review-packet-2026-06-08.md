# P46 Code Review Packet

metadata_date: 2026-06-08
phase: P46-M3
status: `PASSED_BOUNDED_CLAUDE_LINE_RANGE_CODE_REVIEW`

## Purpose

Compact packet for read-only Claude review of the P46 multistate
Zhao--Cui/fixed-design TT adapter.  The full files are still the governing
implementation artifacts; this packet points to the relevant slices so review
does not stall on full-file scans.

Codex is supervisor and executor. Claude is read-only reviewer only. Claude
must not edit files, run experiments, launch agents, or change state.

This packet is not intended to be a packet-only proof of implementation
correctness.  It is a bounded line-range review request: Claude must inspect
the named files/ranges below.  A packet-only self-containment probe on
2026-06-08 correctly returned `BLOCK_PACKET_SELF_CONTAINED` because
implementation correctness, TensorFlow/TFP-only compliance, density-factor
consistency, and retained-axis logic require the primary code/test ranges.

## Governing Plan

`docs/plans/bayesfilter-highdim-zhao-cui-p46-multistate-zhaocui-adapter-plan-2026-06-08.md`

Claude plan review iteration 1 returned `PASS_P46_PLAN_GOVERNANCE`.

## Changed Surfaces

- `bayesfilter/highdim/filtering.py`
  - `MultistateAdjacentTargetBuildResult`: lines 282--298.
  - `multistate_nonlinear_fixed_design_tt_value_path`: lines 989--1225.
  - `multistate_tt_grid_retained_filter`: lines 1353--1450.
  - `multistate_nonlinear_initial_adjacent_target_batch`: lines 1647--1714.
  - `multistate_nonlinear_transition_adjacent_target_batch`: lines 1717--1795.
  - `_validate_multistate_adjacent_target_common`: lines 2068--2095.
  - `_finalize_multistate_adjacent_target_result`: lines 2097--2198.
  - `_multistate_tt_predictive_log_density_from_retained`: lines 2246--2268.
  - `_multistate_grid_predictive_log_density_from_retained`: lines 2313--2356.
  - `_multistate_tt_retained_moments`: lines 2536--2558.
  - `_multistate_tt_grid_retained_from_density`: lines 2561--2599.
  - `_normalized_retained_density_values_chunked`: lines 2602--2625.
  - `_multistate_pairwise_transition_between_grids_log_density`: lines 2650--2670.
- `bayesfilter/highdim/__init__.py`
  - imported/exported new P46 subpackage symbols only: lines 57--83 and
    140--240.
- `tests/highdim/test_p46_multistate_zhaocui_adapter.py`
  - fixture/reference helpers: lines 15--253.
  - adapter call helper and dense value tieout: lines 256--298.
  - deterministic replay test: lines 300--309.
  - dimension-mismatch and scalar-rejection tests: lines 312--330.

Out of scope:

- Adaptive TT-cross/SIRT reproduction.
- Paper-scale Zhao--Cui reproduction.
- Production analytic score API.
- HMC readiness.
- P45 generalized-SV/spatial-SIR/predator-prey equality promotion.

## Local Evidence

CPU-only commands:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p46_multistate_zhaocui_adapter.py
```

Result: 5 passed, 2 TensorFlow Probability deprecation warnings.

Rerun on 2026-06-08 after claudecodex review-probe repair: 5 passed,
2 TensorFlow Probability deprecation warnings.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p45_multistate_zhaocui_route.py tests/highdim/test_p46_multistate_zhaocui_adapter.py
```

Result: 8 passed, 2 TensorFlow Probability deprecation warnings.

Rerun on 2026-06-08 after claudecodex review-probe repair: 8 passed,
2 TensorFlow Probability deprecation warnings.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim tests/highdim/test_p46_multistate_zhaocui_adapter.py
```

Result: passed.

Rerun on 2026-06-08 after claudecodex review-probe repair: passed.

```bash
git diff --check -- bayesfilter/highdim/filtering.py bayesfilter/highdim/__init__.py tests/highdim/test_p46_multistate_zhaocui_adapter.py docs/plans/bayesfilter-highdim-zhao-cui-p46-multistate-zhaocui-adapter-plan-2026-06-08.md
```

Result: passed.

Rerun on 2026-06-08 after claudecodex review-probe repair, including this
packet and the P46 result file in the diff check: passed.

Claude probe ladder after claudecodex review-probe repair:

```text
CLAUDE_PROBE_OK
CLAUDE_PACKET_READ_OK
BLOCK_PACKET_SELF_CONTAINED
```

Interpretation: Claude is operational and can read the packet.  The block is
not a model/runtime blocker; it is a valid governance finding that P46
implementation review must be a named line-range review over the primary code
and test ranges listed in this packet.

## Run Manifest

| Field | Value |
| --- | --- |
| Repo | `/home/chakwong/BayesFilter` |
| Git state | dirty/untracked execution workspace; P46 files are intentionally uncommitted execution artifacts |
| CPU/GPU | CPU-only; `CUDA_VISIBLE_DEVICES=-1`, no GPU evidence claimed |
| Randomness | deterministic P46 fixture seeds in test config |
| Plan | `docs/plans/bayesfilter-highdim-zhao-cui-p46-multistate-zhaocui-adapter-plan-2026-06-08.md` |
| Result | `docs/plans/bayesfilter-highdim-zhao-cui-p46-multistate-zhaocui-adapter-result-2026-06-08.md` |
| Logs | command outputs preserved in the active Codex conversation and summarized here |

## Pass/Block Criteria

Pass only if:

- the scoped implementation preserves the scalar route and P45 historical
  blocker tests;
- BayesFilter-owned P46 implementation is TensorFlow/TensorFlow Probability
  only;
- multistate reference-measure, coordinate-Jacobian, and uniform-reference
  density factors are internally consistent in the reviewed path;
- retained axes, shape checks, density hashes, and branch identities are
  explicit enough for this tiny fixed-branch adapter;
- dim-2/dim-3 dense tieout evidence is correctly bounded and not promoted to
  paper-scale/adaptive TT/SIRT evidence;
- no HMC, score API, or generalized-SV/SIR/predator-prey equality claim is
  made.

Block if:

- a scalar fallback or dimension mismatch can silently handle `state_dim > 1`;
- retained filter propagation mixes physical/reference density factors;
- local tests are only proxy evidence without the stated dense-reference
  comparator;
- any review artifact claims adaptive TT-cross/SIRT, paper-scale reproduction,
  production score API, HMC readiness, or P45 equality promotion;
- the review packet is still too vague to answer the review questions from the
  named files/ranges.

## Line-Range Review Questions

1. Does the implementation preserve the existing scalar route and P45
   historical blocker tests?
2. Is BayesFilter-owned implementation TensorFlow/TensorFlow Probability only?
3. Are the multistate reference-measure, coordinate Jacobian, and uniform
   reference weight terms applied consistently?
4. Are retained axes, shape checks, density hashes, and branch identities
   explicit enough for a tiny fixed-branch adapter?
5. Is the P46 evidence bounded correctly: dim 2 uses order-7 dense tieout; dim
   3 uses order-5 dense tieout because order 7 hit the fitter condition-number
   veto under the current caps?
6. Does the code avoid overclaiming adaptive TT-cross/SIRT, paper-scale
   Zhao--Cui reproduction, production score API, HMC readiness, or P45
   generalized-SV/SIR/predator-prey equality?

## Known Nonclaims

- no adaptive TT-cross/SIRT reproduction;
- no paper-scale Zhao--Cui reproduction;
- no stable public API;
- no production analytic score API;
- no HMC readiness;
- no P45 generalized-SV, spatial-SIR, or predator-prey equality promotion.

Expected pass token, only if the review passes:

`PASS_P46_CODE_GOVERNANCE`

Otherwise return:

`BLOCK_P46_CODE_GOVERNANCE`

The pass/block token must be based on the named file/range review, not on this
packet alone.
