# P38-CUT4 Result: Statistical Comparator First Gate

metadata_date: 2026-06-06
phase: P38-CUT4

## Decision

Decision: `PASS_P38_CUT4`.

The P38 first gate adds a governed CUT4 statistical-comparator layer for the
P30/highdim model suite.  It implements:

- a scoped `P30Cut4StatisticalComparatorManifest` and
  `P30Cut4ComparatorStatus` in the experimental highdim subpackage;
- an affine LGSSM exact-plus-CUT4 paired-equivalence bridge where exact Kalman
  remains the primary exact reference;
- an explicit stochastic-volatility `COMPARATOR_NOT_APPLICABLE` boundary for
  native heteroskedastic SV;
- clean-room additive-Gaussian CUT4 diagnostic closures for small SIR and
  predator-prey rows;
- manifest vetoes that block diagnostic rows from carrying equivalence metrics
  and block default promotion from first-gate equivalence evidence.

## Source-Governance Status

- P30 anchors identified: yes, through the existing P37/P30 model-suite rows.
- Zhao--Cui paper anchors identified: yes, at model-family context level.
- MATLAB behavioral anchors identified: yes, audit/reference only.
- BayesFilter code/test anchors identified: yes, `bayesfilter/highdim/validation.py`,
  `bayesfilter/highdim/__init__.py`, and
  `tests/highdim/test_p30_cut4_statistical_comparators.py`.
- Deviations listed: yes, direct native SV CUT4 non-applicability and
  SIR/predator-prey clean-room Gaussian-closure diagnostics.
- Clean-room boundary respected: yes; no MATLAB code copied or ported.
- Unsupported claims removed: yes.
- Reviewer verdict: `PASS_P38_CUT4_CODE_GOVERNANCE`.

## Local Evidence

Focused CPU-only gate:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p30_cut4_statistical_comparators.py
```

result:

```text
7 passed, 2 warnings in 5.89s
```

Focused plus API guard:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/test_v1_public_api.py \
  tests/highdim/test_public_api_highdim.py \
  tests/highdim/test_p30_cut4_statistical_comparators.py
```

result:

```text
14 passed, 2 warnings in 5.95s
```

Full highdim CPU-only guardrail:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/test_v1_public_api.py \
  tests/highdim
```

result:

```text
190 passed, 2 warnings in 14.38s
```

Static checks:

```bash
python -m compileall -q bayesfilter/highdim tests/highdim
git diff --check
grep -RIn '[[:blank:]]$' bayesfilter/highdim/validation.py \
  bayesfilter/highdim/__init__.py \
  tests/highdim/test_p30_cut4_statistical_comparators.py \
  docs/plans/bayesfilter-highdim-zhao-cui-p30-cut4-*.md \
  docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md
```

result:

```text
compileall passed; git diff --check passed; trailing-whitespace grep returned
no matches.
```

CPU/GPU status:

```text
Deliberate CPU-only validation.  CUDA_VISIBLE_DEVICES=-1 was set for pytest
commands.  No GPU claim is made.
```

## Recovery Note

The first focused gate failed because the initial LGSSM CUT4 bridge compared
different time conventions: the highdim Kalman path observes its initial law,
while the structural CUT4 path predicts through one transition before the first
observation.  The fixture was repaired by using the structural first predictive
law as the highdim initial law.  The equivalence band was not widened to hide
the mismatch.

## Traceability

The traceability ledger now has explicit P38 rows for:

- LGSSM exact-plus-CUT4 bridge;
- SV direct-CUT4 boundary;
- SIR CUT4 Gaussian-closure diagnostic;
- predator-prey CUT4 Gaussian-closure diagnostic;
- CUT4 stress feasibility guard;
- CUT4 smooth-score sanity.

The end-to-end fixed-branch score API remains `BLOCKED_UNVALIDATED`.

## Decision Table

| Field | Status |
|---|---|
| Decision | `PASS_P38_CUT4` |
| Primary criterion status | `PASS_LOCAL`; focused and full highdim CPU-only guards pass |
| Veto diagnostic status | `PASS_LOCAL`; no CUT4-as-truth, exact nonlinear equality, native SV/SIR/predator-prey overclaim, production Hessian, stable score API, HMC, DSGE, GPU, paper-scale, or adaptive MATLAB claim is promoted |
| Strongest uncertainty | P38 is a first-gate comparator-governance layer; most nonlinear P30 rows remain diagnostic-only or not applicable |
| Next justified action | use P38 as the seed for future same-model candidate-vs-CUT4 equivalence rows |
| Non-claims | no full Zhao--Cui reproduction; no adaptive MATLAB TT-cross/SIRT reproduction; no paper-scale validation; no GPU/HMC/DSGE readiness; no stable public API; no stable end-to-end score API; no production CUT4 Hessian; no CUT4 nonlinear ground-truth claim |

## Run Manifest

git commit: `7ccb9c39883471c2d5ec2891cbf33b9ed436bada`

python/environment: repo default TensorFlow environment; pytest executed from
`/home/chakwong/BayesFilter`.

random seeds:

```text
SIR diagnostic seed: 3802
predator-prey diagnostic seed: 3803
LGSSM audit observations: fixed deterministic tensors
```

artifact paths:

```text
bayesfilter/highdim/validation.py
bayesfilter/highdim/__init__.py
tests/highdim/test_p30_cut4_statistical_comparators.py
docs/plans/bayesfilter-highdim-zhao-cui-p30-cut4-statistical-comparator-master-plan-2026-06-06.md
docs/plans/bayesfilter-highdim-zhao-cui-p30-cut4-*-subplan-2026-06-06.md
docs/plans/bayesfilter-highdim-zhao-cui-p30-cut4-statistical-comparator-claude-review-ledger-2026-06-06.md
docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md
docs/plans/bayesfilter-highdim-zhao-cui-p30-cut4-statistical-comparator-result-2026-06-06.md
```

dirty/untracked status:

```text
Workspace is dirty/untracked; the highdim tree and P38 plans are untracked in
the current repository state.  No unrelated tracked changes were reverted.
```

## Post-Run Red-Team Note

Strongest alternative explanation: the LGSSM bridge is exact/affine and the
nonlinear P30 rows are mostly diagnostic-only, so P38 should not be read as
evidence that the current highdim TT lane agrees with CUT4 on native nonlinear
model filtering.

Result that would overturn this closeout: a later audit finding that P38
diagnostic-only rows were used as candidate-vs-CUT4 equivalence, or that the
SV non-applicability boundary was ignored.

Weakest evidence area: no native nonlinear candidate-vs-CUT4 equivalence row is
yet promoted for SV, SIR, or predator-prey.
