# DPF Cross-Implementation Gated Self-Recovery Closeout Result

metadata_date: 2026-06-07
decision: PASS_GATED_EXECUTION_CLOSED_WITH_BF_FF_MATCHED_AND_STUDENT_INTERFACE_BLOCKED

## Question

Did the DPF cross-implementation common-sense tie-out program execute under the
gated self-recovery plan, closing BayesFilter/FilterFlow first and touching
student implementations only after P0--P5 closure?

## Execution Summary

| Phase | Decision | Claude status | Primary artifact |
|---|---|---|---|
| P0 governance | `PASS_P0_GOVERNANCE_READY_FOR_P1` | PASS | `docs/plans/bayesfilter-dpf-cross-implementation-common-sense-tieout-p0-governance-result-2026-06-07.md` |
| P1 density contracts | `PASS_P1_DENSITY_CONTRACTS_MATCHED` | PASS | `experiments/dpf_implementation/reports/outputs/dpf_common_model_suite_tieout_2026-06-06.json` |
| P2 no-resampling paths | `PASS_P2_NORESAMPLING_VALUE_PATHS_MATCHED` | PASS | `experiments/dpf_implementation/reports/outputs/dpf_common_filter_path_noresampling_2026-06-06.json` |
| P3 fixed-ancestor paths | `PASS_P3_FIXED_ANCESTOR_VALUE_PATHS_MATCHED` | PASS | `experiments/dpf_implementation/reports/outputs/dpf_common_filter_path_fixed_resampling_2026-06-06.json` |
| P4 fixed-branch gradients | `PASS_P4_FIXED_BRANCH_GRADIENTS_MATCHED` | PASS | `experiments/dpf_implementation/reports/outputs/dpf_common_fixed_branch_gradient_2026-06-06.json` |
| P5 remaining BF/FF coverage | `PASS_P5_BF_FF_COVERAGE_CLASSIFIED_READY_FOR_P6_MANIFEST_GATE` | PASS | `docs/plans/bayesfilter-dpf-cross-implementation-common-sense-tieout-p5-remaining-bf-ff-coverage-result-2026-06-07.md` |
| P6 terminal student repetition | `PASS_P6_TERMINAL_STUDENT_REPETITION_CLASSIFIED_NO_EXECUTABLE_SAME_FIXTURE_STUDENT_SURFACE` | PASS after checksum repair | `experiments/dpf_implementation/reports/outputs/dpf_cross_impl_terminal_student_repetition_2026-06-07.json` |

## Main Results

BayesFilter and executable float64 FilterFlow matched on the closed common
suite:

- density components for LGSSM, stochastic volatility, and range-bearing;
- deterministic no-resampling filter paths;
- fixed-ancestor resampling paths;
- fixed-branch physical-parameter gradients with finite-difference
  self-checks.

P5 classified remaining BayesFilter/FilterFlow surfaces:

- spatial SIR and predator-prey are `INTERFACE_BLOCKED` for this campaign
  because no same executable FilterFlow surface was identified;
- structural, CUT4, UKF, Kalman, stress, paper-table, and
  annealed-transport debugging lanes are diagnostic or out of scope for the
  closed common fixture;
- older mixed student-prep artifacts are superseded inventory, not active
  P0--P5 evidence.

P6 created the closed-fixture manifest and terminal student classification:

- closed manifest:
  `experiments/dpf_implementation/reports/outputs/dpf_cross_impl_closed_fixture_manifest_2026-06-07.json`
- manifest sha256:
  `38aa0984d006e7e29fd30ac8f2fb6ec06700a454a8315bdbf6c469db3163c723`
- terminal student artifact:
  `experiments/dpf_implementation/reports/outputs/dpf_cross_impl_terminal_student_repetition_2026-06-07.json`
- terminal artifact sha256:
  `ffb98254d8c9c1810285f27bb975b2d7dd1d7b8e4d92eb5e474599bd1e87ee79`
- P6 summary:
  `24` cells, all `INTERFACE_BLOCKED`, zero student filter commands executed.

The student implementations were not run as equality attempts because the
available adapters do not expose the same closed fixture surfaces: frozen
density components, fixed particles and transition innovations, fixed ancestor
replay, the closed scalar objective, and fixed-branch physical gradients.

## Repair History

P5:

- first Claude attempt stalled without verdict;
- compact rerun returned PASS;
- no P5 evidence repair was required.

P6:

- initial review attempts with larger prompts stalled or were stopped without
  verdict;
- summary review returned a material blocker: adapter checksums were missing
  despite the P6 contract requiring them;
- repaired by adding SHA256s for the student adapter contract, implementation
  adapters, common fixture file, and materially inspected runner files;
- post-patch Claude review returned PASS.

No tolerance, fixture, scalar, branch, model, comparator, or parameterization
was changed after seeing results.  No `.localsource/filterflow` mutation was
performed during P5/P6.

## Decision Table

| Decision | Primary criterion | Veto status | Main uncertainty | Next justified action | Not concluded |
|---|---|---|---|---|---|
| PASS_GATED_EXECUTION_CLOSED_WITH_BF_FF_MATCHED_AND_STUDENT_INTERFACE_BLOCKED | P0--P5 BF/FF phases are reviewed closed; P6 is terminally classified with checksums | no open veto | future adapter work could expose exact closed student surfaces | optional follow-up: write a new reviewed adapter-implementation plan if exact student fixture runners are desired | no filtering correctness, student correctness/failure, TT, paper-scale, random resampling distribution, GPU, HMC, DSGE, or production-readiness claim |

## Non-Claims

- BayesFilter, FilterFlow, students, TT, dense quadrature, and paper tables are
  not oracles.
- Agreement on the closed common suite is common-sense consistency evidence,
  not proof of filter correctness.
- Interface-blocked student cells are not student failures.
- The terminal student result does not say the student repositories cannot be
  adapted later; it says the current adapters do not already expose the exact
  closed fixture contract.

## Post-Run Red Team

Strongest alternative explanation:

- an exact same-fixture student adapter might be possible with new adapter
  implementation work.  That would be a new reviewed P6 repair/follow-up, not
  evidence against the current terminal interface classification.

Result that would overturn the closeout:

- discovery of an existing command that already runs a student implementation
  on the closed P1--P4 fixtures with the same scalar, branch, particles,
  innovations, observations, dtype, tolerances, and gradients.

Weakest evidence link:

- P6 is based on the available adapter/runner inventory, not exhaustive proof
  over every vendored student source file.
