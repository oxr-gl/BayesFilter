# BayesFilter-MacroFinance Stage 7 / Accepted Phase 3 Result: HMC Tuning Policy Layer

Date: 2026-06-09

## Status

`PASSED`

## Role And Runtime Classification

Codex is supervisor and executor. Claude is read-only reviewer only.

Stage/phase authority:

- This artifact is the visible-runbook Stage 7 precheck/result note.
- Stage 7 implements accepted Phase 3 of
  `docs/plans/bayesfilter_macrofinance_hmc_filtering_consolidation_plan_2026_06_09.md`.
- The filename keeps `phase_3` because accepted Phase 3 is the scientific
  phase authority. The live MacroFinance ledger records the visible execution
  stage as Stage 7.
- References to Stage 7 below mean "visible execution Stage 7 / accepted Phase
  3 HMC tuning policy layer."

Runtime classification:

- BayesFilter library primitive: accepted TF/TFP runtime policy metadata plus a
  tiny TF/TFP Gaussian diagnostic fixture.
- Fixed-screen behavior: accepted existing TF/TFP runtime path with no adaptive
  kernel.
- Dual averaging: reviewed diagnostic-only TF/TFP path on a bounded Gaussian
  fixture; not a default policy, posterior-sampling readiness claim, or
  production adaptation policy.
- MacroFinance compatibility: a no-HMC synthetic fixed-kernel diagnostic
  comparison against the current MacroFinance matched-DGP fixed-screen
  classifier. This is intentionally narrower than a MacroFinance model run:
  the BayesFilter Gaussian fixture tests actual TF/TFP tuning telemetry, while
  the MacroFinance check tests whether the fixed-screen classifier boundary and
  nonclaim semantics match the current client helper.
- No empirical HMC run, posterior convergence, sampler superiority, default
  sampler promotion, GPU/XLA readiness, full mass adaptation, or production
  readiness is authorized by this phase.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter expose reviewed, fail-closed HMC tuning policy labels so fixed-kernel screens remain explicit and diagnostic-only dual averaging can be exercised on a bounded fixture without becoming a default or posterior-convergence claim? |
| Baseline/comparator | Accepted Phase 3 of `docs/plans/bayesfilter_macrofinance_hmc_filtering_consolidation_plan_2026_06_09.md`, visible runbook Stage 7, current BayesFilter `FullChainHMCConfig` fail-closed `fixed_kernel_no_adaptation` behavior, Stage 3 HMC diagnostics, Stage 4 evidence manifests, a BayesFilter Gaussian TF/TFP fixture for actual tuning telemetry, and MacroFinance fixed-kernel matched-DGP screen classification helpers for client classifier compatibility. |
| Primary criterion | BayesFilter defines `HMCTuningPolicy` labels for `fixed_kernel_screen`, `dual_averaging_step_size`, `fixed_mass_dual_averaging`, `windowed_mass_adaptation_future`, and `manual_ladder_diagnostic`; preserves fail-closed rejection of unsupported adaptation; allows dual averaging only through an explicit reviewed policy on a Gaussian fixture; records adaptation steps, final step size, target accept, source policy, and nonclaims; and no policy reports posterior convergence. |
| Veto diagnostics | Adaptive kernels become the default; `fixed_kernel_no_adaptation` rejection is weakened without replacement evidence; unsupported adaptation labels are accepted; dual averaging is allowed without explicit reviewed policy; target invalidity is treated as tuning success; adaptation diagnostics are reported as convergence; or MacroFinance compatibility requires changing MacroFinance model/data/HMC defaults. |
| Repair triggers | Missing policy helper/export/test, stale config metadata, default adaptation accidentally enabled, missing nonclaims, missing final step-size/adaptation-step telemetry, unsupported label not failing closed, MacroFinance fixed-screen classification mismatch, or Claude `NEEDS_REVISION` with fixable findings. |
| Explanatory diagnostics | Step size, target accept, adaptation step count, acceptance rate, trace availability, runtime, and tiny-chain finite sample counts. |
| Non-claims | Passing this phase does not prove posterior convergence, sampler superiority, empirical validity, default adaptation readiness, GPU/XLA readiness, full mass adaptation readiness, or production large-scale CIP readiness. |

## Skeptical Audit

- Wrong baseline: The baseline is BayesFilter's current fail-closed
  `FullChainHMCConfig` plus MacroFinance's fixed-screen classification helper,
  not a fresh matched-DGP HMC run, old mismatched Phase 4 artifact, or
  MacroFinance's broader default `dual_averaging` config.
- Proxy metric promotion: Acceptance rates, adapted step sizes, and finite
  tiny-chain samples are diagnostic telemetry only. They cannot become
  convergence, superiority, or default-readiness evidence.
- Stop conditions: Stop and repair if adaptation becomes default, unsupported
  labels are accepted, fixed-screen metadata drifts, target invalidity is
  treated as tuning success, or any output claims convergence.
- Fair comparison: Stage 7 uses a two-fixture split. BayesFilter's bounded
  Gaussian TF/TFP fixture exercises actual fixed-screen and reviewed
  dual-averaging telemetry. MacroFinance compatibility compares the same
  synthetic fixed-kernel diagnostic fields and classifier outcome because the
  accepted Phase 3 MacroFinance requirement is fixed-screen wrapper
  classification, not a new MacroFinance posterior run. This avoids treating
  old matched-DGP tuning pathologies or unrelated model/data details as
  evidence about the BayesFilter tuning-policy contract.
- Hidden assumptions: TFP dual averaging adapts step size only; this phase does
  not authorize mass adaptation or windowed adaptation. The
  `fixed_mass_dual_averaging` label is allowed only as explicit fixed-mass
  step-size adaptation metadata, not as learned mass-matrix adaptation.
- Stale context: BayesFilter and MacroFinance both have dirty worktrees;
  unrelated changes must be preserved.
- Environment/import mismatch: BayesFilter tests run from
  `/home/ubuntu/python/BayesFilter`. MacroFinance compatibility should use
  `PYTHONPATH=/home/ubuntu/python/BayesFilter` and CPU-only no-HMC settings.
- Artifact relevance: Required artifacts are this result note, focused
  BayesFilter policy tests, a focused Gaussian dual-averaging diagnostic test,
  a MacroFinance fixed-screen compatibility test, and Claude read-only
  pre/post reviews.
- Role-contract check: Claude pre-review must be read-only; Codex performs all
  edits and tests.
- BayesFilter/MacroFinance ownership: Reusable policy types and dual-averaging
  diagnostic runner belong in BayesFilter. MacroFinance remains a client
  compatibility fixture and should not force MacroFinance-specific fields into
  BayesFilter.

## Current Code Audit

BayesFilter currently accepts only
`FullChainHMCConfig(adaptation_policy="fixed_kernel_no_adaptation")`; any other
string raises a `ValueError`. This is the correct fail-closed baseline.

`run_full_chain_tfp_hmc(...)` builds a fixed
`tfp.mcmc.HamiltonianMonteCarlo` kernel and records
`adaptation_policy="fixed_kernel_no_adaptation"` plus nonclaims. It does not
currently expose reviewed policy labels or any explicit dual-averaging
diagnostic path.

BayesFilter Stage 3 diagnostics already classify fixed-kernel conservative
acceptance as a promotion veto rather than convergence. Stage 7 should reuse
that discipline; it should not create a second convergence authority.

MacroFinance already has a broader HMC runner that can wrap HMC with
`tfp.mcmc.DualAveragingStepSizeAdaptation` when
`kernel_policy="dual_averaging"`, but that broader behavior is not the
BayesFilter default and is not sufficient evidence to promote adaptive kernels
inside BayesFilter. MacroFinance also has fixed-kernel screen classifiers that
can be compared to BayesFilter on synthetic diagnostics without launching a
new model run. The synthetic no-HMC comparison is not a substitute for
posterior-runtime parity; it is a bounded compatibility check for the
fixed-screen classifier contract. Broader MacroFinance migration/runtime parity
belongs to visible Stage 8 / accepted Phase 8.

## Planned Minimal Implementation

1. Add a BayesFilter module such as `bayesfilter/inference/hmc_tuning.py`.
2. Define `HMCTuningPolicy` with bounded labels:
   `fixed_kernel_screen`, `dual_averaging_step_size`,
   `fixed_mass_dual_averaging`, `windowed_mass_adaptation_future`, and
   `manual_ladder_diagnostic`.
3. Include fields for `adaptation_policy`, `num_adaptation_steps`,
   `target_accept_prob`, `source`, `enabled`, `implemented`, and nonclaims.
4. Provide constructors or validators for fixed-screen and reviewed
   dual-averaging policies. Unsupported labels and future windowed mass
   adaptation must fail closed.
5. Update `FullChainHMCConfig` only enough to accept a first-class
   `HMCTuningPolicy` or the legacy fixed string. The default must remain
   fixed/no-adaptation, and raw non-fixed strings must still fail closed.
6. Add a narrowly scoped Gaussian diagnostic helper that runs TFP HMC with
   `DualAveragingStepSizeAdaptation` only when given an implemented reviewed
   dual-averaging policy. It must record adaptation steps, final step size,
   target accept, policy label, diagnostic role, and nonclaims. It must not
   report convergence.
7. Add focused BayesFilter tests:
   fixed-screen policy reproduces current metadata;
   unreviewed adaptation fails closed;
   future windowed mass adaptation fails closed;
   reviewed dual averaging records step-size telemetry and nonclaims on a
   Gaussian fixture;
   invalid target evaluation is not classified as tuning success;
   no policy payload contains a posterior convergence claim.
8. Add a MacroFinance compatibility test that feeds synthetic fixed-kernel
   diagnostics to MacroFinance's current fixed-screen classifier and to
   BayesFilter's fixed-screen wrapper/classifier, then compares classification
   fields such as failure class, diagnostic role, screen veto, and nonclaim
   boundary. This check answers only the fixed-screen classifier compatibility
   part of accepted Phase 3; it does not claim MacroFinance runtime parity,
   posterior readiness, or generated-data recovery.
9. Export public helpers through `bayesfilter.inference` and top-level
   `bayesfilter` if public API tests require it.

## Planned Checks

- `python -m pytest tests/test_common_inference_runtime_contracts.py -q`
- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_nonlinear_ssm_phase4_full_chain_hmc.py -q`
- `python -m pytest tests/test_v1_public_api.py -q` if export surface changes.
- MacroFinance focused compatibility test with
  `PYTHONPATH=/home/ubuntu/python/BayesFilter CUDA_VISIBLE_DEVICES=-1
  PYTHONDONTWRITEBYTECODE=1`, targeting a small no-HMC test that compares the
  fixed-screen classifiers.

Warnings from TensorFlow Probability, gast, or read-only pytest caches are
explanatory unless a test fails or a planned artifact is missing.

## Pre-Review Request

Claude should verify that this Stage 7 precheck is consistent with accepted
Phase 3, preserves BayesFilter's fail-closed default, does not silently promote
MacroFinance's broader dual-averaging behavior, separates tuning diagnostics
from posterior convergence, keeps unsupported/windowed adaptation rejected, and
uses MacroFinance only as a client compatibility fixture.

## Pre-Review Trail

- `docs/plans/bayesfilter_macrofinance_stage_7_hmc_tuning_pre_review_round_01.md`
  returned `VERDICT: NEEDS_REVISION` with three repairable findings:
  make the Stage 7 / accepted Phase 3 authority pairing explicit; justify why
  the MacroFinance no-HMC synthetic classifier comparison is sufficient for the
  fixed-screen compatibility boundary; and ensure the live ledger visibly
  records the Stage 7 evidence contract, skeptical audit, and next action.
- Codex patched this note and the live MacroFinance ledger without changing
  the scientific contract, fail-closed default, unsupported/windowed adaptation
  rejection, or nonclaims.
- `docs/plans/bayesfilter_macrofinance_stage_7_hmc_tuning_pre_review_round_02.md`
  returned `VERDICT: PROCEED` with no material findings. Claude confirmed that
  the Stage 7 / accepted Phase 3 authority pairing, ledger visibility,
  two-fixture comparator scope, fail-closed/default discipline, nonclaims, and
  MacroFinance-as-client boundary are ready for implementation.

## Implementation Summary

Implemented a BayesFilter-owned HMC tuning policy layer in
`bayesfilter/inference/hmc_tuning.py`.

The implementation adds:

- `HMC_TUNING_POLICY_LABELS`;
- `HMCTuningPolicy`;
- `HMCTuningDiagnosticResult`;
- `normalize_hmc_tuning_policy(...)`;
- `require_executable_tuning_policy(...)`;
- `classify_fixed_kernel_screen_with_tuning_policy(...)`;
- `classify_hmc_tuning_diagnostic(...)`;
- `run_gaussian_dual_averaging_diagnostic(...)`.

The default policy remains fixed/no-adaptation. Raw `adaptation_policy` strings
other than `fixed_kernel_no_adaptation` still fail closed. Reviewed
dual-averaging requires an explicit `HMCTuningPolicy` object. Future windowed
mass adaptation and manual ladder labels are named but not executable in this
phase.

`FullChainHMCConfig` now normalizes to a first-class `HMCTuningPolicy` while
preserving the legacy fixed default. It rejects dual averaging under XLA in
this phase and rejects adaptation steps greater than burn-in steps. The full
chain runner wraps TFP `DualAveragingStepSizeAdaptation` only when a reviewed
policy object is supplied, and records policy payload, adaptation steps, target
accept probability, final step size, source, and nonclaims.

The Gaussian diagnostic helper runs only a bounded standard-normal fixture. It
is diagnostic telemetry for policy gating and step-size extraction, not
posterior evidence.

## MacroFinance Compatibility Pin

Exact MacroFinance compatibility test:

- `/home/ubuntu/python/MacroFinance/tests/test_mixed_frequency_tfp_phase4_matched_dgp_svd_derived_hmc_pilot.py::test_bayesfilter_hmc_classification_matches_matched_dgp_acceptance_and_hard_stops`

The test now compares the explicit BayesFilter
`HMCTuningPolicy.fixed_kernel_screen()` classifier wrapper with MacroFinance's
current matched-DGP fixed-screen conservative acceptance classifier on the same
synthetic fixed-kernel diagnostics. This is a no-HMC classifier compatibility
check only. It does not change MacroFinance model construction, data payloads,
HMC defaults, generated-data recovery, or posterior-runtime parity.

## Files Touched For Stage 7

BayesFilter:

- `bayesfilter/inference/hmc_tuning.py`
- `bayesfilter/inference/hmc.py`
- `bayesfilter/inference/__init__.py`
- `bayesfilter/__init__.py`
- `tests/test_common_inference_runtime_contracts.py`
- `tests/test_nonlinear_ssm_phase4_full_chain_hmc.py`
- `tests/test_v1_public_api.py`
- `docs/plans/bayesfilter_macrofinance_phase_3_hmc_tuning_policy_layer_result_2026_06_09.md`
- `docs/plans/bayesfilter_macrofinance_stage_7_hmc_tuning_pre_review_round_01.md`
- `docs/plans/bayesfilter_macrofinance_stage_7_hmc_tuning_pre_review_round_02.md`

MacroFinance:

- `tests/test_mixed_frequency_tfp_phase4_matched_dgp_svd_derived_hmc_pilot.py`
- `docs/plans/bayesfilter_macrofinance_visible_execution_ledger_2026_06_09.md`

## Checks Run

| Command | Result | Role |
| --- | --- | --- |
| `PYTHONPYCACHEPREFIX=/tmp/bayesfilter_pycache python -m py_compile bayesfilter/inference/hmc_tuning.py bayesfilter/inference/hmc.py` from `/home/ubuntu/python/BayesFilter` | Passed | Syntax/import sanity without writing bytecode into read-only BayesFilter cache paths |
| `PYTHONDONTWRITEBYTECODE=1 python -m pytest tests/test_common_inference_runtime_contracts.py -q` from `/home/ubuntu/python/BayesFilter` | `51 passed, 1 warning in 0.25s` | BayesFilter tuning policy contract gate |
| `CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 python -m pytest tests/test_nonlinear_ssm_phase4_full_chain_hmc.py -q` from `/home/ubuntu/python/BayesFilter` | `9 passed, 48 warnings in 4.69s` | Full-chain fixed default plus reviewed dual-averaging Gaussian diagnostic gate |
| `PYTHONDONTWRITEBYTECODE=1 python -m pytest tests/test_v1_public_api.py -q` from `/home/ubuntu/python/BayesFilter` | `4 passed, 3 warnings in 2.47s` | Public export/lazy import gate |
| `env PYTHONPATH=/home/ubuntu/python/BayesFilter CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 python -m pytest tests/test_mixed_frequency_tfp_phase4_matched_dgp_svd_derived_hmc_pilot.py::test_bayesfilter_hmc_classification_matches_matched_dgp_acceptance_and_hard_stops -q` from `/home/ubuntu/python/MacroFinance` | `1 passed, 2 warnings in 2.54s` | Focused MacroFinance fixed-screen policy compatibility gate |
| `env PYTHONPATH=/home/ubuntu/python/BayesFilter CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 python -m pytest tests/test_mixed_frequency_tfp_phase4_matched_dgp_svd_derived_hmc_pilot.py -q` from `/home/ubuntu/python/MacroFinance` | `14 passed, 20867 warnings in 153.31s` | Full matched-DGP compatibility module |

Warnings were TensorFlow Probability `distutils` deprecations, `gast`
deprecations, and BayesFilter `.pytest_cache` write warnings from a read-only
cache path. They are explanatory only for this CPU-only Stage 7 gate.

## Decision Table

| Item | Status |
| --- | --- |
| Decision | Stage 7 implementation ready for Claude read-only post-review |
| Primary criterion status | Passed focused BayesFilter and MacroFinance compatibility checks |
| Veto diagnostic status | No adaptation default promotion, raw unsupported adaptation acceptance, executable windowed mass adaptation, target-invalidity-as-success, convergence claim, or MacroFinance model/default change observed |
| Main uncertainty | Dual-averaging telemetry is proven only on a tiny Gaussian diagnostic fixture, not on MacroFinance posterior runtime |
| Next justified action | Claude read-only post-review |
| What is not concluded | No posterior convergence, sampler superiority, empirical validity, default adaptation readiness, GPU/XLA readiness, full mass adaptation readiness, or production readiness |

## Post-Run Red Team

Strongest alternative explanation: The tests prove policy plumbing and
telemetry extraction on bounded fixtures, but they do not prove that adaptive
HMC will behave well on the mixed-frequency TFP posterior or any large CIP
model.

Result that would overturn the current gate: a Claude finding or future test
showing that raw adaptation strings no longer fail closed, dual averaging
activates by default, future/windowed mass adaptation is executable, or
diagnostic telemetry is being reported as convergence.

Weakest part of the evidence: The MacroFinance compatibility check is
deliberately no-HMC and classifier-only. Broader MacroFinance runtime migration
remains Stage 8 / accepted Phase 8.

## Post-Review Trail

- `docs/plans/bayesfilter_macrofinance_stage_7_hmc_tuning_post_review_round_01.md`
  returned `VERDICT: PROCEED` with no material findings.
- Claude residual risks match this result note's nonclaims: dual averaging is
  proven only on a bounded Gaussian fixture; MacroFinance coverage is
  classifier-only; and dual averaging under XLA remains fail-closed.
