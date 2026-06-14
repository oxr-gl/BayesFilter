# DPF Common Model Suite V2 P0 Governance Subplan

metadata_date: 2026-06-07
phase: P0
status: REVIEWED_READY_FOR_PHASE_EXECUTION

## Question

Can we define the v2 production-suite governance contract before any v2 code or
experiment work, while preserving closed v1 artifacts and preventing accidental
student, FilterFlow-source, or oracle misuse?

## Inputs

- Master plan:
  `docs/plans/bayesfilter-dpf-common-model-suite-v2-production-master-plan-2026-06-07.md`
- Closed v1 closeout:
  `docs/plans/bayesfilter-dpf-cross-implementation-common-sense-tieout-gated-self-recovery-closeout-result-2026-06-07.md`
- Highdim closeout:
  `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase7-integration-closeout-result-2026-06-05.md`

## Evidence Contract

Primary criterion:

- A v2 manifest schema exists and records model ids, source surfaces, dtype,
  CPU/GPU policy, frozen path contracts, gradient knobs, tolerances, checksums,
  blocked-state taxonomy, non-claims, and retirement state.

Veto diagnostics:

- any plan language treating BayesFilter, FilterFlow, students, TT, dense
  quadrature, simulated truth, or paper tables as an oracle;
- any student command before v2 BF/FF closure;
- any need to mutate `.localsource/filterflow`;
- any silent overwrite or reinterpretation of closed v1 artifacts;
- missing stop conditions for tolerance/fixture/scalar/branch changes after
  seeing results.

Non-claims:

- no v2 model value, path, gradient, student, TT, paper-scale, HMC, DSGE, GPU,
  or production-readiness claim is made by P0.

Artifacts:

- P0 result ledger under `docs/plans/`;
- v2 manifest schema or draft JSON under
  `experiments/dpf_implementation/reports/outputs/`.

## Tasks

1. Record editable file scope and blocked file scope.
2. Define v2 result taxonomy: `MATCHED`, `EXPLAINED_MISMATCH`,
   `INTERFACE_BLOCKED`, `CONTRACT_BLOCKED`, `SCIENTIFIC_CONTRACT_BLOCKED`.
3. Define closed-artifact preservation checks for v1.
4. Define CPU-only TensorFlow execution policy:
   `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import.
5. Define Claude review loop rules for master plan, subplans, phase results,
   and repair amendments.
6. Define retirement semantics for `lgssm_tf.py`,
   `stochastic_volatility_tf.py`, and `range_bearing_tf.py`.
7. Define mandatory phase artifact fields: `review_round`,
   `open_material_blockers`, `repair_amendment_required`, and
   `next_allowed_action`.
8. Define the v2 isolation preflight gate: no v2 runner may call the old
   three-row `common_model_specs()` API or write old 2026-06-06 artifact names.

## Exit Criteria

- Claude review returns PASS or convergence for the P0 governance contract.
- The result ledger states that no v2 evidence commands, student commands, or
  `.localsource/filterflow` mutations occurred during P0.
- The result ledger defines the P1 six-row model-id gate and the P2 pre-run
  row classification table requirement.
- P1 is authorized only after P0 records the frozen governance contract.

## Stop Conditions

- Claude flags a material blocker that cannot be repaired within five review
  rounds.
- Any requested fix would weaken the scientific contract.
- Any requested fix requires mutating `.localsource/filterflow`.
