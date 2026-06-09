# BayesFilter-MacroFinance Phase 5 Result: HMC Diagnostics And Classification

Date: 2026-06-09

## Status

`PASSED`

## Role And Runtime Classification

Codex is supervisor and executor. Claude is read-only reviewer only.

Runtime classification:

- BayesFilter library primitive: NumPy verification oracle and deterministic
  fixture/test helper for this phase.
- MacroFinance compatibility: small diagnostic client gate that reads existing
  Phase 4 HMC artifacts and synthetic dictionaries; it does not run HMC.
- No long-run HMC, posterior convergence, sampler superiority, GPU/XLA
  readiness, default sampler promotion, or empirical claim is authorized by
  this phase.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter provide reusable HMC screen diagnostics and failure classification that distinguish hard vetoes, promotion vetoes, continuation vetoes, and explanatory diagnostics without promoting short-chain diagnostics to convergence? |
| Baseline/comparator | Existing BayesFilter `HMCDiagnosticSummary` and `summarize_hmc_diagnostics`; MacroFinance `screen_payload`, `classify_matched_hmc_screen_failure`, `trial_acceptance_degenerate`, `trial_hard_stop_failure`, and the current matched-DGP fixed-kernel/coarse and refined bracket artifacts. |
| Primary criterion | BayesFilter exposes target-agnostic `HMCScreenResult` and `HMCFailureClassification` or equivalent; counts nonfinite log-accept ratios, divergence threshold exceedances, max absolute log accept, per-chain acceptance, diagnostic unavailability, and acceptance degeneracy; focused tests pass; MacroFinance classification cases match. |
| Veto diagnostics | Unavailable diagnostics reported as zero/pass, short-chain R-hat/ESS promoted to convergence, acceptance degeneracy treated as posterior success, hard divergence/nonfinite log-accept treated as tuning-only, or classification changes Phase 4 interpretation without evidence. |
| Repair triggers | Missing diagnostic role, missing nonclaims, failed synthetic log-accept count, failed reduced-trace unavailable handling, mismatch with MacroFinance acceptance-degenerate or hard-stop cases, or Claude `NEEDS_REVISION` with fixable findings. |
| Explanatory diagnostics | Runtime, exact class names, per-chain acceptance, split R-hat, rank-normalized split R-hat, ESS, bulk ESS, tail ESS, and max log-accept magnitude unless a screen explicitly marks one as a veto. |
| Non-claims | No posterior convergence, sampler superiority, empirical validity, GPU/XLA readiness, default sampler promotion, or production readiness is concluded. |

## Skeptical Audit

- Wrong baseline: The baseline is current BayesFilter diagnostics plus current
  MacroFinance Phase 4 classification artifacts, not a new HMC run or old
  mismatched data.
- Proxy metric promotion: Acceptance, R-hat, ESS, tail ESS, and runtime are
  diagnostics; this phase only classifies screen outcomes and does not rank or
  promote samplers.
- Stop conditions: Reporting unavailable diagnostics as zero, treating
  acceptance equal to one as success, or treating divergence/nonfinite
  log-accept hard stops as tuning-only stops the phase until repaired.
- Fair comparison: Compatibility must compare the same screen checks used in
  MacroFinance: finite arrays, zero divergences, zero nonfinite log-accept
  ratios, finite per-chain acceptance, and nondegenerate per-chain acceptance.
- Hidden assumptions: MacroFinance's clean acceptance-one case is a
  fixed-kernel conservative tuning/envelope veto, not DGP or posterior math
  evidence.
- Stale context: BayesFilter and MacroFinance both have dirty worktrees;
  unrelated changes must not be reverted. Artifact compatibility must read
  existing reviewed JSON results only as diagnostic comparators.
- Environment/import mismatch: BayesFilter tests run from
  `/home/ubuntu/python/BayesFilter`; MacroFinance compatibility should use
  `PYTHONPATH=/home/ubuntu/python/BayesFilter` or an equivalent explicit local
  import contract.
- Artifact relevance: The required artifacts are this result note, focused
  BayesFilter tests, a MacroFinance compatibility test or fixture, and Claude
  read-only pre/post reviews.
- Role-contract check: Claude pre-review must be read-only; Codex performs all
  edits and tests.
- BayesFilter/MacroFinance ownership: Reusable diagnostics and classifications
  belong in `bayesfilter.inference`; MacroFinance remains a client
  compatibility fixture.

## Current Code Audit

BayesFilter already has `HMCDiagnosticSummary` and `summarize_hmc_diagnostics`,
which expose acceptance, divergence count, split R-hat, ESS, and nonclaims.
The current helper correctly distinguishes unavailable divergences from zero
divergences, but it does not yet expose:

- nonfinite log-accept count;
- divergence count by log-accept threshold;
- maximum absolute log-accept ratio;
- per-chain acceptance;
- screen pass/fail with unavailable diagnostics preserved;
- acceptance degeneracy classification;
- hard-stop versus promotion-veto classification.

MacroFinance currently implements those ideas locally in Phase 4 scripts:

- `screen_payload(...)` checks sample-chain return, finite arrays, zero
  divergences, zero nonfinite log-accept ratios, finite acceptance, and
  per-chain acceptance strictly between 0.05 and 0.99.
- `classify_matched_hmc_screen_failure(...)` distinguishes a clean
  acceptance-one trace as `fixed_kernel_conservative_acceptance_veto`.
- fixed-kernel ladder artifacts distinguish acceptance-degenerate trials from
  hard stops before clean nondegenerate trials.

Stage 3 should lift only generic diagnostic/classification logic into
BayesFilter. It must not move MacroFinance model construction or Phase scripts.

## Planned Minimal Implementation

1. Extend `bayesfilter/inference/hmc_diagnostics.py` with:
   `HMCScreenResult`, `HMCFailureClassification`, and small helper functions
   such as `summarize_log_accept_ratios`, `screen_hmc_diagnostics`, and
   `classify_hmc_screen`.
2. Preserve `summarize_hmc_diagnostics` compatibility.
3. Treat unavailable diagnostics as unavailable, not zero.
4. Make diagnostic roles explicit:
   hard veto, promotion veto, continuation veto, repair trigger, or
   explanatory diagnostic.
5. Classify:
   clean screen pass;
   fixed-kernel conservative acceptance veto;
   hard stop before promotion because of divergence, nonfinite log accept, or
   nonfinite required arrays;
   generic screen veto after trace materialization;
   blocked/no trace.
6. Add focused BayesFilter tests for:
   synthetic log-accept nonfinite and threshold divergence counts;
   reduced trace unavailable versus zero;
   clean acceptance-one fixed-kernel conservative veto;
   hard divergence/nonfinite log-accept stop;
   short-chain R-hat/ESS remaining nonclaims.
7. Add a MacroFinance compatibility test comparing BayesFilter classification
   to the current matched-DGP acceptance-one fixture and the reviewed fixed
   coarse/refined artifact hard-stop cases.

## Planned Checks

- `python -m pytest tests/test_common_inference_runtime_contracts.py -q`
- `python -m pytest tests/test_v1_public_api.py -q` if export surface changes.
- MacroFinance focused compatibility test with
  `PYTHONPATH=/home/ubuntu/python/BayesFilter CUDA_VISIBLE_DEVICES=-1
  PYTHONDONTWRITEBYTECODE=1`, targeting the matched-DGP SVD pilot test module.

If the MacroFinance compatibility gate cannot be run because of import-path,
environment, stale-artifact, or fixture issues, Stage 3 enters the repair loop.
It must not substitute a synthetic-only check for the accepted Phase 4
classification compatibility gate.

## Pre-Review Request

Claude should verify that this Stage 3 precheck is consistent with accepted
Phase 5, starts from existing BayesFilter diagnostics, preserves nonclaims,
does not promote short-chain diagnostics to convergence, and compares the
correct MacroFinance classification cases.

## Pre-Review Trail

- `docs/plans/bayesfilter_macrofinance_stage_3_hmc_diagnostics_classification_pre_review_round_01.md` returned `VERDICT: PROCEED`; implementation may proceed.

## Implementation Summary

Implemented BayesFilter-owned HMC diagnostic and classification helpers in
`bayesfilter/inference/hmc_diagnostics.py`.

New public contracts:

- `HMCLogAcceptSummary`;
- `HMCScreenResult`;
- `HMCFailureClassification`;
- `summarize_log_accept_ratios(...)`;
- `screen_hmc_diagnostics(...)`;
- `classify_hmc_screen(...)`.

The implementation preserves the existing `HMCDiagnosticSummary` and
`summarize_hmc_diagnostics(...)` compatibility surface.

Implemented classification behavior:

- unavailable diagnostics remain unavailable and cannot pass as zero;
- nonfinite log-accept ratios are counted separately from finite threshold
  exceedances;
- threshold divergence count uses `abs(log_accept_ratio) > threshold`;
- per-chain acceptance equal to one under a fixed no-adaptation kernel is a
  `fixed_kernel_conservative_acceptance_veto`;
- divergence, nonfinite log-accept, invalid required arrays, invalid
  acceptance, no trace, or HMC execution error are hard vetoes before
  promotion;
- a clean screen pass remains `screen_passed_not_convergence`;
- all classifications carry nonclaims.

Exports were updated through `bayesfilter.inference` and the top-level
`bayesfilter` lazy export table.

MacroFinance compatibility was implemented as a focused test in
`/home/ubuntu/python/MacroFinance/tests/test_mixed_frequency_tfp_phase4_matched_dgp_svd_derived_hmc_pilot.py`.
It compares BayesFilter classification to:

- the matched-DGP clean acceptance-one conservative tuning/envelope veto;
- the reviewed coarse fixed-kernel hard-stop artifact;
- the reviewed refined bracket hard-stop artifact.

## Repair Note

The first focused BayesFilter test run failed during collection with an
`IndentationError` in `bayesfilter/inference/__init__.py`; the new export names
had been inserted after the closing `__all__` bracket. Codex repaired the export
list and reran the same gate successfully. This was an implementation syntax
repair, not a diagnostic-contract failure.

## Files Touched For Stage 3

BayesFilter:

- `bayesfilter/inference/hmc_diagnostics.py`
- `bayesfilter/inference/__init__.py`
- `bayesfilter/__init__.py`
- `tests/test_common_inference_runtime_contracts.py`
- `tests/test_v1_public_api.py`
- `docs/plans/bayesfilter_macrofinance_phase_5_hmc_diagnostics_classification_result_2026_06_09.md`
- `docs/plans/bayesfilter_macrofinance_stage_3_hmc_diagnostics_classification_pre_review_round_01.md`

MacroFinance:

- `tests/test_mixed_frequency_tfp_phase4_matched_dgp_svd_derived_hmc_pilot.py`
- `docs/plans/bayesfilter_macrofinance_visible_execution_ledger_2026_06_09.md`

## Checks Run

| Command | Result | Role |
| --- | --- | --- |
| `python -m pytest tests/test_common_inference_runtime_contracts.py -q` from `/home/ubuntu/python/BayesFilter` | first run failed at collection with `IndentationError`; repaired export list | Repair trigger |
| `python -m pytest tests/test_common_inference_runtime_contracts.py -q` from `/home/ubuntu/python/BayesFilter` | `30 passed in 0.14s` | BayesFilter focused contract gate |
| `python -m pytest tests/test_v1_public_api.py -q` from `/home/ubuntu/python/BayesFilter` | `4 passed, 2 warnings in 2.46s` | BayesFilter public export gate |
| `env PYTHONPATH=/home/ubuntu/python/BayesFilter CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 python -m pytest tests/test_mixed_frequency_tfp_phase4_matched_dgp_svd_derived_hmc_pilot.py::test_bayesfilter_hmc_classification_matches_matched_dgp_acceptance_and_hard_stops -q` from `/home/ubuntu/python/MacroFinance` | `1 passed, 2 warnings in 2.87s` | Direct MacroFinance matched-DGP classification compatibility gate |
| `env PYTHONPATH=/home/ubuntu/python/BayesFilter CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 python -m pytest tests/test_mixed_frequency_tfp_phase4_matched_dgp_svd_derived_hmc_pilot.py -q` from `/home/ubuntu/python/MacroFinance` | `11 passed, 20867 warnings in 115.83s` | Existing real-client matched-DGP suite evidence |

The warnings are TensorFlow Probability `distutils` deprecation warnings and
TensorFlow AutoGraph/gast deprecation warnings; they are explanatory only for
this phase.

## Gate Assessment

| Gate | Status |
| --- | --- |
| Nonfinite log-accept count | passed |
| Threshold divergence count | passed |
| Unavailable diagnostics not treated as zero/pass | passed |
| Per-chain acceptance degeneracy classification | passed |
| Hard divergence/nonfinite log-accept classification | passed |
| Short-chain R-hat/ESS remain nonclaims | passed |
| Public export | passed |
| MacroFinance matched-DGP acceptance-one compatibility | passed |
| MacroFinance coarse/refined hard-stop compatibility | passed |
| Posterior convergence, sampler superiority, default, or GPU/XLA promotion claimed | no |

## Decision Table

| Item | Status |
| --- | --- |
| Decision | Stage 3 implementation passed focused checks and Claude read-only post-review |
| Primary criterion status | passed focused BayesFilter and MacroFinance compatibility checks |
| Veto diagnostic status | no unavailable-as-zero, convergence-promotion, acceptance-one-success, or hard-stop-as-tuning-only behavior observed |
| Main uncertainty | this is a diagnostic/classification contract only; later phases still own manifests, parity gates, invalid-region policy, tuning, and migration |
| Next justified action | advance to Stage 4, evidence manifest and artifact schema |
| What is not concluded | no posterior convergence, sampler superiority, default sampler promotion, empirical validity, GPU/XLA readiness, or production readiness |

## Post-Review Trail

- `docs/plans/bayesfilter_macrofinance_stage_3_hmc_diagnostics_classification_post_review_round_01.md` returned `VERDICT: PROCEED`.
