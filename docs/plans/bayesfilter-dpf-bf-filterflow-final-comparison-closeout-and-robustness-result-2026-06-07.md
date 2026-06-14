# DPF BayesFilter/FilterFlow Final Comparison Closeout And Robustness Result

metadata_date: 2026-06-07
plan: docs/plans/bayesfilter-dpf-bf-filterflow-final-comparison-closeout-and-robustness-plan-2026-06-07.md
decision: PASS_BF_FILTERFLOW_DETERMINISTIC_TIEOUT_CLOSEOUT_WITH_DIAGNOSTICS

## Scope

The user removed item 4 from the work.  This result therefore contains no
student-repository execution, no student-derived metric, and no student
match/mismatch/correctness/failure conclusion.

Covered items:

1. consolidated BayesFilter/FilterFlow closeout statement;
2. seeded fixed-ancestor robustness diagnostic;
3. controlled 1D LGSSM horizon ladder diagnostic;
5. DPF chapter documentation.

## Question

After the V2 production BayesFilter/FilterFlow tie-out, what can we
responsibly say about DPF agreement, and do small robustness diagnostics reveal
any blocker to that statement?

## Evidence Contract

Primary criterion: the final closeout may say BayesFilter and the executable
local FilterFlow-side adapters match on the frozen deterministic V2 comparison
contract if the existing V2 density, no-resampling path, fixed-ancestor path,
and fixed-branch AD-gradient artifacts validate, and if all non-claims are
preserved.

Veto diagnostics:

- any student command or student-derived metric;
- any `.localsource/filterflow` mutation;
- oracle framing for BayesFilter, FilterFlow, TT, dense quadrature, paper
  tables, stochastic simulation, or student repositories;
- tolerance, fixture, scalar, branch, comparator, or gradient-contract changes
  after results without reviewed amendment;
- finite differences used as a gradient gate;
- nonfinite V2 scalar/path/AD-gradient values;
- unclassified BF/FF mismatch on a primary V2 deterministic field.

Explanatory-only diagnostics:

- finite differences;
- seeded fixed-ancestor robustness;
- 1D LGSSM horizon ladder and Sinkhorn residual fields;
- CPU-only TensorFlow CUDA/cuInit stderr.

Not concluded:

- no filter correctness proof;
- no claim that BayesFilter or FilterFlow is mathematically correct;
- no stochastic-resampling distribution correctness claim;
- no differentiable-resampling or gradient-through-random-ancestor claim;
- no student match, mismatch, correctness, or failure claim;
- no TT/SIRT, paper-table, GPU, HMC, DSGE, scalability, deployment, or
  production-readiness claim.

## Claude Plan Review

Plan review: PASS.

Runner review: PASS.

Ledger:
`docs/plans/bayesfilter-dpf-bf-filterflow-final-comparison-closeout-and-robustness-claude-review-ledger-2026-06-07.md`.

## Evidence Results

### V2 Deterministic Basis

Validated commands:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_v2_density_tf --validate-only
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_v2_noresampling_tf --validate-only
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_v2_fixed_resampling_tf --validate-only
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_v2_gradients_tf --validate-only
```

All four validation commands exited 0.

The governing phase ledgers are closed PASS:

| Surface | Phase decision | Primary result |
|---|---|---|
| V2 density | `PASS_P2_DENSITY_READY_FOR_P3` | six matched rows, max abs delta `0.0` |
| V2 no-resampling path | `PASS_P3_NORESAMPLING_READY_FOR_P4` | six matched rows, max abs delta `0.0` |
| V2 fixed-ancestor path | `PASS_P4_FIXED_RESAMPLING_READY_FOR_P5` | six matched rows, max abs delta `0.0`; expected one resampling event |
| V2 fixed-branch AD gradients | `PASS_P5_GRADIENTS_READY_FOR_P6` | five executable rows matched; max scalar delta `0.0`; max AD-gradient delta `0.0`; `spatial_sir_j3_rk4` contract-blocked |

Note: the V2 JSON files still contain runner-time decision strings
`PENDING_CLAUDE_REVIEW`; the governing result ledgers listed above are the
closed PASS artifacts.

### Seeded Fixed-Ancestor Robustness

Command:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_bf_filterflow_seeded_ancestor_robustness_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_bf_filterflow_seeded_ancestor_robustness_tf --validate-only
```

Result:

- decision: `PASS_SEEDED_ANCESTOR_DIAGNOSTIC`;
- artifact:
  `experiments/dpf_implementation/reports/outputs/dpf_bf_filterflow_seeded_ancestor_robustness_2026-06-07.json`;
- report:
  `experiments/dpf_implementation/reports/dpf-bf-filterflow-seeded-ancestor-robustness-2026-06-07.md`;
- digest:
  `8663b8a99c66c6a52b3b70ef5bb68563399a8612e7d15cba4901aea8eda5330d`;
- status counts: `{'MATCHED': 18}`;
- max abs delta: `0.0`;
- seeds: `[1101, 2202, 3303]`;
- interpretation: branch-robustness diagnostic only.  The ancestor schedules
  were seeded, frozen, and replayed on both sides.  This is not random-number
  equality and not stochastic-resampling distribution correctness.

### 1D LGSSM Horizon Ladder

Command:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_1d_lgssm_horizon_ladder_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_1d_lgssm_horizon_ladder_tf --validate-only
```

Result:

- decision: `one_d_lgssm_horizon_ladder_agreement_residual_veto`;
- artifact:
  `experiments/dpf_implementation/reports/outputs/dpf_filterflow_1d_lgssm_horizon_ladder_2026-06-01.json`;
- report:
  `experiments/dpf_implementation/reports/dpf-filterflow-1d-lgssm-horizon-ladder-2026-06-01.md`;
- digest:
  `90d4b2c46003738c3a94296d8e6c16856d01246b96d58f2b756b108f94cb28e6`;
- summary: `all_implementation_agreement=True`,
  `all_forward_match=False`, `gradient_promotion=not_concluded`;
- `T2_anchor`: implementation agreement true, forward match true, scalar
  delta `6.201557778418021e-08`, AD-gradient delta
  `2.1969256280840455e-07`, max row residual
  `3.77402173978858e-06`;
- `T4_extension`: implementation agreement true, forward match false, scalar
  delta `1.7313559519394062e-07`, AD-gradient delta
  `3.0408782158986014e-08`, max row residual
  `0.0005233287811279297`.

Interpretation: this is an explanatory older 1D Sinkhorn residual diagnostic.
It does not overturn the V2 deterministic BF/FF match because the ladder itself
records implementation agreement and leaves residuals/FD as diagnostic-only.

### DPF Chapter Documentation

Edited:

- `docs/chapters/ch19f_dpf_debugging_crosswalk.tex`

Added section:

- `BayesFilter/FilterFlow deterministic tie-out contract`

The section records the frozen comparison objects, V2 results, SIR gradient
contract block, FD diagnostic-only policy, seeded-ancestor diagnostic, horizon
ladder diagnostic, and explicit non-claims.

Build command:

```bash
cd docs
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Result: PASS; `docs/main.pdf` rebuilt successfully.  The build emitted
pre-existing overfull/underfull and rerun/cross-reference warnings, but no
fatal LaTeX error.

## Command Manifest

| Field | Value |
|---|---|
| git commit | `7ccb9c39883471c2d5ec2891cbf33b9ed436bada` |
| git branch | `main` |
| execution environment | `/home/chakwong/BayesFilter`; shell `bash` |
| CPU/GPU status | TensorFlow commands were CPU-only with `CUDA_VISIBLE_DEVICES=-1` before import; artifacts record visible GPUs `[]`; TensorFlow emitted CPU-only CUDA/cuInit stderr |
| random seeds | V2 deterministic fixtures as previously recorded; seeded diagnostic used `[1101, 2202, 3303]` only to generate frozen ancestor schedules |
| dtype | `tf.float64` / JSON float64 |
| student commands | `0` |
| `.localsource/filterflow` mutation | none performed |
| PDF artifact | `docs/main.pdf` |

## Veto Diagnostics

| Veto | Status |
|---|---|
| student command or metric | PASS; none run or derived |
| `.localsource/filterflow` mutation | PASS; none performed |
| oracle framing | PASS; agreement stated only under same frozen contract |
| tolerance/fixture/scalar/branch/comparator/gradient weakening after results | PASS; none changed |
| FD used as gradient gate | PASS; FD diagnostic-only |
| nonfinite V2 primary value or AD gradient | PASS; validation commands exited 0 |
| unclassified BF/FF primary mismatch | PASS; no open primary deterministic mismatch |
| stochastic distribution claim | PASS; explicitly not claimed |

## Decision Table

| Decision | Primary criterion | Veto status | Main uncertainty | Next justified action | Not concluded |
|---|---|---|---|---|---|
| `PASS_BF_FILTERFLOW_DETERMINISTIC_TIEOUT_CLOSEOUT_WITH_DIAGNOSTICS` | V2 deterministic density, path, fixed-ancestor, and fixed-branch AD-gradient artifacts validated; seeded branch diagnostic matched; chapter documented | no material veto open | stochastic resampling distributions and gradients through random/discrete ancestor selection remain untested | use this as the BF/FF deterministic closeout; any stochastic-resampling or student work requires a separate reviewed plan | no filter correctness, implementation correctness, stochastic distribution, differentiable resampling, student, TT/SIRT, paper-scale, GPU, HMC, DSGE, scalability, deployment, or production-readiness claim |

## Post-Run Red Team

Strongest alternative explanation: BF/FF agreement may reflect shared frozen
adapter contracts rather than independent scientific truth.

Result that would overturn this closeout: evidence that a student command
influenced the result, `.localsource/filterflow` was mutated, a tolerance or
scalar was changed after results, FD was used as a gate, or a primary V2
deterministic field is later found to mismatch under the frozen contract.

Weakest evidence link: stochastic resampling behavior remains represented only
by fixed-schedule branch replay; no distributional or differentiable-resampling
claim is supported.

## Non-Claims

- no filter correctness proof;
- no BayesFilter correctness claim;
- no FilterFlow correctness claim;
- no stochastic-resampling distribution correctness claim;
- no random-number-generator equality claim;
- no differentiable-resampling or gradient-through-random/discrete-ancestor
  claim;
- no student match, mismatch, correctness, or failure claim;
- no TT/SIRT, dense quadrature, simulated-truth, or paper-table oracle claim;
- no GPU, HMC, DSGE, scalability, deployment, or production-readiness claim.
