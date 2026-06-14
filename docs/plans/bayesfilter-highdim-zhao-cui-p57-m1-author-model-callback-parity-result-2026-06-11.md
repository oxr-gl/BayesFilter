# P57-M1 Result: Author Model Callback Parity

metadata_date: 2026-06-11
phase: P57-M1
status: PASS_CLAUDE_REVIEWED

## Decision Table

| Field | Result |
| --- | --- |
| Decision | Add a source-anchored BayesFilter callback target for the Zhao-Cui `sir_austria` spatial SIR example and keep the older generic P30 fixture classified as an extension/diagnostic fixture. |
| Primary criterion status | PASS: the parity ledger below records state ordering, parameters, transition density, push/noise policy, prior, likelihood, observation indexing, covariance choices, and fixed-HMC/source classifications. |
| Veto diagnostic status | PASS: the old chain-graph P30 fixture is not promoted as the author target; source-route filtering remains blocked until later transport/marginalization/proposal phases pass. |
| Main uncertainty | Exact stochastic replay equality with MATLAB RNG is not tested; M1 only locks callback formulas and source-target identity. |
| Next justified action | Claude read-only source-anchor review; if agreed, advance to P57-M2 transport-contract work. |
| What is not concluded | No TT/SIRT transport correctness, rank correctness, HMC readiness, d=18 filtering success, d=50/d=100 scaling success, adaptive parity, S&P reproduction, or smoothing support. |

Required token:

`PASS_P57_M1_AUTHOR_MODEL_CALLBACK_PARITY`

## Source Anchors

| Author operation | Anchor | P57 classification |
| --- | --- | --- |
| Example dimensions and run settings | `third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m:14-17`, `:39-56` set `d=0`, `m=18`, `n=9`, `T=20`, `N=5e3`, `tau=10`, squared TTSIRT, and max rank 40. | `source_faithful` target metadata. |
| Generic state-space push/weight API | `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/ssmodel.m:21-59` initializes `X`, `Y`, pushes samples with `st_process`, and updates weights with `like`. | `source_faithful` callback boundary. |
| SIR setup | `sir_austria/setup.mlx` code cell sets `theta=[]`, `type=0`, `theta=[.1,18]`, `sigma1=1`, `sigma2=10`, prior mean, and observation matrix selecting even MATLAB indices. | `source_faithful` in `zhao_cui_sir_austria_model()`. |
| Transition density | `sir_austria/transition.mlx` code cell computes `sir_step(x_{t-1}, theta)` and evaluates `mvnpdf(x_t, mean, sigma1^2 I)`. | `source_faithful` formula via `transition_log_density`. |
| Transition push | `sir_austria/st_process.mlx` code cell computes `sir_step(x_t, theta) + sigma1*randn` and clips susceptible coordinates `1:2:m` to nonnegative. | `fixed_hmc_adaptation` via deterministic standard-normal push with declared clipping policy. |
| SIR ODE | `sir_austria/odefun.mlx` code cell defines the fixed 9-node adjacency, infection term `theta1*S_k*I_k`, recovery `theta2*I_k`, and 0.5 neighbor diffusion. | `source_faithful` in author-specific graph/RHS. |
| Author RK step | `sir_austria/sir_step.mlx` code cell uses four steps of size `.005`; its fourth stage is `odefun(x + fp3*delta/2, theta)`. | `source_faithful` as `rk4_variant="zhao_cui_sir_step"`. |
| Observation process and likelihood | `sir_austria/ob_process.mlx` and `sir_austria/like.mlx` code cells use `C*x + sigma2*randn` and `mvnpdf(y, C*x, sigma2^2 I)`. | `source_faithful` observation density over infectious coordinates only. |
| Prior | `sir_austria/priorpdf.mlx` and `priorsam.mlx` code cells use `N(priormean, I_m)`. | `source_faithful` initial density. |

## Discrepancy Ledger

| BayesFilter component | Classification | M1 disposition |
| --- | --- | --- |
| Existing `p30_spatial_sir_fixture_model(9)` | `extension_or_invention` for P57 source-faithful spatial SIR | Kept unchanged for older P30/P52/P53 diagnostics. It uses a chain graph, initial pairs `[485+j, 15-j]`, classical RK4, and no susceptible clipping after process noise. |
| New `zhao_cui_sir_austria_model()` | `source_faithful` callback target plus fixed-HMC deterministic push adapter | Added as the P57 spatial SIR callback target. It uses the author 9-node adjacency, initial pairs `[486+j, 14-j]`, `sigma1=1`, `sigma2=10`, author `sir_step` RK convention, and susceptible clipping in the push path. |
| `transition_push_from_standard_normal` | `fixed_hmc_adaptation` | Replaces MATLAB random draw with caller-supplied standard-normal draws so the fixed branch is replayable for HMC. The route and clipping policy match `st_process.mlx`. |
| `rk4_variant="zhao_cui_sir_step"` | `source_faithful` for author callback parity | Preserves the author live-script RK formula, including the fourth-stage half-step convention. |

## Implementation Changes

- Added `SpatialSIRSSM.rk4_variant` with supported values `classical` and
  `zhao_cui_sir_step`.
- Added `SpatialSIRSSM.process_noise_policy` with supported values
  `diagnose_negative_after_noise` and `clip_susceptible_after_noise`.
- Added `transition_push_from_standard_normal(...)` for fixed/replayable
  source-style pushes.
- Added `zhao_cui_sir_austria_model()` author-specific factory.
- Exported `zhao_cui_sir_austria_model` from `bayesfilter.highdim`.
- Added `tests/highdim/test_p57_m1_author_sir_callback_parity.py`.

## Claude Review

- Full read-only review returned `VERDICT: AGREE`.
- Compact retry also returned `VERDICT: AGREE`.
- One non-blocking nit was noted: MATLAB `like.mlx` has a `pdf(isnan(pdf))=0`
  guard while BayesFilter finite-input log density does not encode a NaN guard.
  This is not material for M1 formula parity and can be revisited only if a
  later phase needs exact nonfinite-value policy parity.

## Checks

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p57_m1_author_sir_callback_parity.py tests/highdim/test_p30_spatial_sir.py
12 passed, 2 warnings
```

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/models.py bayesfilter/highdim/__init__.py tests/highdim/test_p57_m1_author_sir_callback_parity.py
```

Passed:

```text
git diff --check -- bayesfilter/highdim/models.py bayesfilter/highdim/__init__.py tests/highdim/test_p57_m1_author_sir_callback_parity.py
```

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | Not recorded; dirty worktree contains prior unrelated changes. |
| Environment | Codex visible supervisor/executor in `/home/chakwong/BayesFilter`; TensorFlow/TFP CPU-only validation. |
| CPU/GPU status | CPU-only by `CUDA_VISIBLE_DEVICES=-1`; GPU not used. |
| Data version | Local author source under `third_party/audit/zhao_cui_tensor_ssm_p10/source`. |
| Random seeds | N/A for tests; push test uses deterministic supplied noise. |
| Wall time | Focused pytest ~3 seconds. |
| Plan file | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m1-author-model-callback-parity-subplan-2026-06-11.md`. |
| Result file | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m1-author-model-callback-parity-result-2026-06-11.md`. |

## Post-Run Red-Team Note

Strongest alternative explanation: passing M1 only proves the BayesFilter target
callbacks can represent the author SIR formulas; it does not prove the later
TT/SIRT source route can fit, marginalize, sample, or correct proposals on this
target.  The weakest evidence point is that `.mlx` source anchors are extracted
from OOXML code cells rather than plain `.m` files; the commands and source
paths are recorded so later phases can re-open the same source cells.
