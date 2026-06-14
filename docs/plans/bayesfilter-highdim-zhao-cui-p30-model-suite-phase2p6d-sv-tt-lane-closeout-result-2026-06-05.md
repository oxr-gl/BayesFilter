# P37-M2.6d Result: SV TT Lane Replay And Governance Closeout

metadata_date: 2026-06-06
phase: P37-M2.6d

## Decision

Decision: `PASS_M2P6D`.

M2.6d closes the scalar stochastic-volatility TT lane as a governed prerequisite
for later model-suite phases.  It adds no new mathematical or numerical
capability.  It verifies that M2.6a--M2.6c pass tokens, traceability,
non-claims, focused replay tests, and broad guardrails are in place.

## Source-Governance Status

- P30 anchors identified: inherited from M2.6a--M2.6c, including SV equations,
  adjacent-target recursion, square-root fitting, square-mass normalizer, and
  retained-density identities.
- Zhao--Cui paper anchors identified: inherited from M2.6a--M2.6c, including
  the SSM/filtering equations, Algorithms 1--2, Eq. (13), Lemma 1,
  Proposition 2, and Eq. (14).
- MATLAB behavioral anchors identified: inherited from M2.6a--M2.6c; MATLAB is
  audit/reference material only.
- BayesFilter code/test anchors identified:
  `bayesfilter/highdim/models.py`,
  `bayesfilter/highdim/filtering.py`,
  `bayesfilter/highdim/fitting.py`,
  `bayesfilter/highdim/squared_tt.py`,
  `tests/highdim/test_p30_sv_fixed_design_tt_target.py`,
  `tests/highdim/test_p30_sv_squared_density_normalizer_marginal.py`, and
  `tests/highdim/test_p30_sv_short_sequential_tt_value_path.py`.
- Deviations listed: yes.  The lane is a fixed-design scalar BayesFilter
  extension, not MATLAB adaptive TT-cross/SIRT reproduction.
- Clean-room boundary respected: yes.
- Unsupported claims removed: yes.
- Reviewer verdict: `PASS_M2P6D_CODE_GOVERNANCE`.

## Closeout Checklist

| Item | Status |
|---|---|
| `PASS_M2P6A` present | `PASS` |
| `PASS_M2P6A_CODE_GOVERNANCE` present | `PASS` |
| `PASS_M2P6B` present | `PASS` |
| `PASS_M2P6B_CODE_GOVERNANCE` present | `PASS` |
| `PASS_M2P6C` present | `PASS` |
| `PASS_M2P6C_CODE_GOVERNANCE` present | `PASS` |
| SV traceability row names M2.6a evidence | `PASS` |
| SV traceability row names M2.6b evidence | `PASS` |
| SV traceability row names M2.6c evidence | `PASS` |
| SV traceability row status avoids promoted `BLOCKED_*` state | `PASS`; row remains `BAYESFILTER_EXTENSION` |
| Non-promoted claims remain blocked by wording | `PASS`; paper-scale, adaptive, SMC/real-data, derivative, HMC, DSGE, GPU, and scalability claims remain non-promoted |
| Focused SV lane tests | `PASS`; 14 passed |
| Broad highdim guardrail | `PASS`; 144 passed |

## Evidence Contract Status

| Field | Status |
|---|---|
| Primary criterion | `PASS_LOCAL`; M2.6a--M2.6c pass tokens and traceability are present, focused closeout tests pass, and broad highdim guardrail passes |
| Veto diagnostics | `PASS_LOCAL`; no unresolved M2.6a/M2.6b/M2.6c blocker, missing SV traceability row, promoted `BLOCKED_*` SV status, public/API/HMC/DSGE/GPU/scalability overclaim, or branch replay regression observed |
| Explanatory diagnostics | dirty/untracked workspace status, test counts, warning counts, and wall times |
| Main uncertainty | governance closeout only; no new numerical evidence beyond M2.6c |
| Next justified action | M3 spatial SIR plan gate |
| What is not concluded | no paper-scale or adaptive TT-cross reproduction, no derivative/HMC/DSGE/GPU readiness, no high-dimensional scalability claim |

## Run Manifest

git commit: `7ccb9c39883471c2d5ec2891cbf33b9ed436bada`

dirty/untracked status:

```text
dirty/untracked workspace; active highdim code, tests, and P30 plan files are
untracked in this repository state.
```

environment: `/home/chakwong/anaconda3/envs/tf-gpu`

CPU/GPU status:

```text
deliberate CPU-only tests; CUDA_VISIBLE_DEVICES=-1 set in pytest commands.
No GPU claim is made.
```

dtype: `tf.float64`

random seeds:

```text
N/A for M2.6d closeout itself; no new stochastic run or seeded numerical
procedure was introduced.  M2.6a--M2.6c seed values are preserved in their
respective result ledgers.
```

commands:

```text
focused closeout pytest command
broad highdim guardrail pytest command
python -m compileall -q bayesfilter/highdim tests/highdim
git diff --check over M2.6d-owned closeout artifacts
explicit trailing-whitespace scan over M2.6d-owned closeout artifacts because
the P30 closeout files are currently untracked
```

Focused closeout command:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p30_sv_fixed_design_tt_target.py \
  tests/highdim/test_p30_sv_squared_density_normalizer_marginal.py \
  tests/highdim/test_p30_sv_short_sequential_tt_value_path.py
```

result:

```text
14 passed, 2 warnings in 7.88s
```

wall time: `7.88s`

Broad highdim guardrail:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/test_v1_public_api.py \
  tests/highdim/test_phase0_contracts.py \
  tests/highdim/test_bases.py \
  tests/highdim/test_tt_algebra.py \
  tests/highdim/test_squared_tt_density.py \
  tests/highdim/test_transport.py \
  tests/highdim/test_fixed_branch_fit.py \
  tests/highdim/test_failure_exits.py \
  tests/highdim/test_filtering_kalman_exact.py \
  tests/highdim/test_fixed_branch_derivatives.py \
  tests/highdim/test_scaling_smoke.py \
  tests/highdim/test_public_api_highdim.py \
  tests/highdim/test_p30_model_suite_contracts.py \
  tests/highdim/test_p30_lgssm_exact_reference.py \
  tests/highdim/test_p30_stochastic_volatility.py \
  tests/highdim/test_p30_sv_fixed_design_tt_target.py \
  tests/highdim/test_p30_sv_squared_density_normalizer_marginal.py \
  tests/highdim/test_p30_sv_short_sequential_tt_value_path.py
```

result:

```text
144 passed, 2 warnings in 13.23s
```

wall time: `13.23s`

Compile:

```bash
python -m compileall -q bayesfilter/highdim tests/highdim
```

result:

```text
passed
```

Whitespace:

```bash
git diff --check -- \
  docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6d-sv-tt-lane-closeout-subplan-2026-06-05.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6d-sv-tt-lane-closeout-claude-review-ledger-2026-06-05.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6d-sv-tt-lane-closeout-result-2026-06-05.md \
  docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md
```

result:

```text
passed
```

File-content whitespace check:

```bash
grep -n '[[:blank:]]$' \
  docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6d-sv-tt-lane-closeout-subplan-2026-06-05.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6d-sv-tt-lane-closeout-claude-review-ledger-2026-06-05.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6d-sv-tt-lane-closeout-result-2026-06-05.md \
  docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md
```

result:

```text
passed; no trailing whitespace matches were reported.  The command returned
exit status 1 because grep found no matches.
```

output artifacts:

```text
docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6d-sv-tt-lane-closeout-subplan-2026-06-05.md
docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6d-sv-tt-lane-closeout-claude-review-ledger-2026-06-05.md
docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6d-sv-tt-lane-closeout-result-2026-06-05.md
docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md
```

## Failure And Repair Log

failed attempt:

```text
Claude code/governance review iteration 1 returned
BLOCKED_M2P6D_CODE_GOVERNANCE.
```

blocker classification:

```text
fixable ledger/evidence-recording issue.  The scientific contract, test
evidence, traceability status, pass tokens, and non-claims were unchanged.
```

plan amendment:

```text
N/A; the reviewed M2.6d plan already required a runbook-compliant result
ledger and whitespace/self-check evidence.  The repair implements that
existing requirement.
```

Claude repair review:

```text
N/A before repair; the original Claude code/governance review supplied the
required fix.  A second Claude code/governance review is required before
promotion.
```

rerun evidence:

```text
Focused and broad test evidence remains as recorded above.  Whitespace check
over all M2.6d-owned artifacts passed after this patch.  An explicit
file-content trailing-whitespace scan also found no matches, which matters
because the M2.6d artifacts are currently untracked and therefore not fully
covered by git diff --check.
```

## Decision Table

| Field | Status |
|---|---|
| Decision | `PASS_M2P6D` |
| Primary criterion status | `PASS_LOCAL` |
| Veto diagnostic status | `PASS_LOCAL` |
| Strongest uncertainty | closeout only; no new numerical claim |
| Next justified action | M3 spatial SIR plan gate |
| Non-claims | no paper-scale, adaptive, derivative, HMC, DSGE, GPU, public API, or scalability claim |

## Post-Run Red Team

Strongest alternative explanation:

- The closeout may make the scalar SV TT lane easier to cite than it should be.
  The traceability row therefore keeps the status as `BAYESFILTER_EXTENSION`
  and names the exact scalar/two-observation scope.

What would overturn promotion:

- Claude finds an overclaim in the traceability row or result ledgers;
- a focused M2.6a--M2.6c test fails under replay;
- a broad guardrail exposes API or adjacent highdim regression.

Weakest evidence:

- This is a governance gate.  It depends entirely on the M2.6a--M2.6c evidence
  and does not add independent numerical validation.
