# P69 Phase 5c Result: Rank Activity And Degree-Normalizer Design Diagnostic

metadata_date: 2026-06-15
status: P69_PHASE5C_RANK_ACTIVITY_DEGREE_NORMALIZER_DIAGNOSTIC_PASSED
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p69-remaining-gaps-master-program-2026-06-15.md
phase: 5c
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

review_status: CLAUDE_VERDICT_AGREE

## Decision

Phase 5c produced a bounded CPU-only diagnostic artifact:

`docs/plans/bayesfilter-highdim-zhao-cui-p69-phase5c-rank-activity-degree-normalizer-diagnostics-2026-06-15.json`

The fixed-variant lower gates do not justify launching Phase 6 d18 validation.
The next phase should be a bounded repair-design phase:

`RANK_CHANNEL_ACTIVATION_AND_DEGREE_NORMALIZER_REPAIR_DESIGN`

The central finding is sharper than the Phase 5b read-only inference.  In the
realized fitted TT cores, the current constant-path one-sweep fixed fit uses
only channel 0.  This is true for both rank 2 and rank 3 rows, and for both
time steps.  Therefore the rank-ladder zero-delta is not evidence that larger
rank is unnecessary; it is direct evidence that the current fixed fitting path
does not activate the additional rank channels.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Are rank-3 channels inactive by construction/fit, and is degree-2 instability driven by normalizer/design scaling rather than a route wiring bug? |
| Baseline/comparator | Exact Phase 3 comparator rows: rank 2 vs rank 3 at degree 1/fit 36, and degree 1 vs degree 2 at rank 2/fit 24. |
| Primary criterion | Satisfied: direct fitted-core, normalizer, target-scale, design, and holdout/replay diagnostics were produced without changing thresholds or source-route semantics. |
| Veto diagnostics | No source-route semantic change; no threshold tuning; no broad ladder; no GPU/HMC command; no adaptive parity, d18 correctness, scaling, or HMC-readiness claim. |
| Explanatory diagnostics | Per-rank-channel norms, basis-channel norms, fit/holdout/replay residuals, normalizer terms, target-value scale, sample adequacy, and condition summaries. |
| Not concluded | No correctness, scaling readiness, HMC readiness, adaptive Zhao--Cui parity, or paper-failure claim. |
| Artifact preserving result | Phase 5c JSON artifact above. |

## Skeptical Audit

The plan survived the required skeptical audit only after narrowing the run to
the four existing Phase 3 comparator rows.  The audit rejected low/high branch
closeness as a promotion criterion, treated fit residuals and sample adequacy as
diagnostic only, and allowed `gauge-hidden/unresolved` as a possible rank
classification.  Existing Phase 3 JSON was insufficient because it exposed only
aggregate core counts; it did not expose per-channel activity.  A small
diagnostic script was therefore necessary.

## Commands And Checks

CPU-only diagnostic and local checks:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q scripts/p69_phase5c_rank_activity_degree_normalizer_diagnostic.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p69_phase5c_rank_activity_degree_normalizer_diagnostic.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q scripts/p69_phase5c_rank_activity_degree_normalizer_diagnostic.py tests/highdim/test_p69_phase5c_diagnostic_script.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p69_phase5c_diagnostic_script.py
```

The first diagnostic run completed all four rows but failed during final summary
serialization because the script looked for `log_mixture_normalizer` instead of
the actual `mixture_normalizer` field.  The repair was visible: the script now
computes the log-mixture delta from `mixture_normalizer`, checkpoints after each
row, and has a focused unit test for the field contract.

Final diagnostic rerun completed successfully in `1174.532` seconds.  The
focused test passed:

`1 passed, 2 warnings in 3.16s`.

TensorFlow printed CUDA plugin/cuInit messages even under
`CUDA_VISIBLE_DEVICES=-1`; these are recorded as CPU-only framework
initialization noise, not GPU evidence.

## Rank Activity Diagnosis

The rank pair has different branch hashes and rank tuples, so the rank-3 row is
not literally identical to the rank-2 row.  But the realized fitted cores expose
only one active declared channel.

Rank-2 row, degree 1, fit 36:

- step 1 active declared channels: `[0]`; inactive channels: `[1]`;
- step 2 active declared channels: `[0]`; inactive channels: `[1]`;
- extra-channel max slice norm: `0.0` in both steps.

Rank-3 row, degree 1, fit 36:

- step 1 active declared channels: `[0]`; inactive channels: `[1, 2]`;
- step 2 active declared channels: `[0]`; inactive channels: `[1, 2]`;
- extra-channel max slice norm: `0.0` in both steps.

Bounded classification:

`RANK_CHANNEL_INACTIVE_IN_REALIZED_FIT`

More precisely, the current fixed path realizes a rank-one channel path inside
the declared rank-2 or rank-3 tensor train.  The most plausible local mechanism
is the constant-path initialization together with a single left-to-right sweep:
zero later channels remain unavailable to the design matrices generated by the
current path.  This is an implementation/repair-design diagnosis for the fixed
variant, not a claim about the adaptive Zhao--Cui method.

Updated explanation status:

- deterministic degeneracy: resolved as a direct realized-core degeneracy for
  the current fixed path;
- gauge-hidden extra channel: weakened, because the direct channel slice norms
  for inactive channels are exactly zero in the realized cores;
- rank-capacity evidence: blocked until rank-channel activation is repaired.

## Degree-Normalizer Diagnosis

The degree-2 row improves in-sample residuals but makes the normalizer and
holdout/replay behavior unstable.

Degree 2 minus degree 1:

- fit residual delta by step: `[-0.04189557323319159, -0.1074918548251745]`;
- log transport normalizer delta by step:
  `[59.54048065746218, -20.333098348263263]`;
- mixture normalizer ratio high over low:
  `[7.212771921978597e25, 1.4772281921684692e-09]`;
- max condition-number delta:
  `[2050828122.4367867, 1817063968.3352828]`;
- degree-2 preferred sample gap: `24` samples below the preferred P66
  heuristic, although it passes the diagnostic minimum.

Degree-2 step 1 is especially unstable:

- fit residual improves to `0.040451316910524164`;
- holdout residual is `2.6312960308794235e18`;
- replay residual is `4.714792131035494e19`;
- mixture normalizer is `6.126661753753613e32`;
- degree-2 basis channel norms are active and large: max norms
  `{0: 75.4822398097916, 1: 14.201083293699762, 2: 68.40674171074602}`.

Bounded classification:

`DEGREE_NORMALIZER_DESIGN_SENSITIVITY_SUPPORTED`

The degree-2 issue is not a simple failure to fit the training target.  It is a
normalizer/design/target-scale instability under the current fixed path.  It
does not yet prove overfitting as the sole mechanism, but overfitting and target
scaling remain live explanations.

Updated explanation status:

- design coverage insufficiency: supported more strongly, but still a bounded
  diagnostic mechanism rather than a proof of convergence behavior;
- overfitting: supported as a live explanation, not resolved;
- target scaling: supported as a live explanation, not resolved;
- route wiring failure: weakened, because branch hashes are distinct, diagnostics
  are available, and the problem is localized to realized rank-channel and
  normalizer behavior.

## Repair Implication

Do not proceed to Phase 6 d18 validation.  The next phase should design a
minimal fixed-variant repair with two separate targets:

1. rank-channel activation repair:
   - replace or augment the constant-path initialization with a reviewed
     activation rule that gives nonzero access to all declared internal
     channels;
   - or run a reviewed multi-sweep/gauge-aware fitting diagnostic that can
     activate channels without changing the scientific target;
   - require direct post-fit channel activity diagnostics before any rank
     ladder is interpreted.
2. degree-normalizer repair:
   - keep degree 2 blocked from validation until target scaling, normalizer
     stabilization, or design coverage is repaired and rechecked;
   - preserve degree 1/rank 2 only as a conservative diagnostic branch, not as a
     validated paper-scale branch.

## Forbidden Nonclaims

- No d18 validation readiness.
- No d50/d100 scaling readiness.
- No HMC readiness.
- No adaptive Zhao--Cui parity.
- No claim that the Zhao--Cui paper or author code fails.
- No claim that rank 1 is scientifically sufficient.
- No claim that degree 2 should be discarded generally.

## Next Handoff

Write and execute Phase 5d:

`P69 Phase 5d: Rank-Channel Activation And Degree-Normalizer Repair Design`

Phase 5d must remain a design/implementation-precheck phase unless it first
states a reviewed evidence contract for a bounded repair.  Phase 6 remains
blocked until Phase 5d or a later repair phase demonstrates nonzero declared
rank-channel activity and bounded normalizer behavior under predeclared checks.
