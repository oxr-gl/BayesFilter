# BayesFilter Minimal SSL-LSTM Zhao-Cui HMC Ladder Master Program

Date: 2026-07-06

Status: `PHASE5_DEFERRED_READY_FOR_PHASE6_CLOSEOUT`

## Objective

Operationalize a minimal HMC evidence ladder for the one-dimensional
state-space LSTM `zhaocui_fixed` lane:

- `latent_dim=1`
- `hidden_dim=1`
- `observation_dim=1`
- `horizon=2`

The narrow target question is:

Can the completed minimal scalar SSL-LSTM `zhaocui_fixed` mechanics smoke be
consumed by BayesFilter HMC machinery and produce finite, reproducible,
diagnosable short-run artifacts?

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Can the minimal scalar SSL-LSTM `zhaocui_fixed` target be admitted to a staged HMC mechanics ladder? |
| Candidate/mechanism under test | Existing clean-room deterministic `zhaocui_fixed` fixed replay adapter, wrapped for BayesFilter HMC through a minimal internal target adapter. |
| Expected failure mode | Target adapter shape mismatch, nonfinite value/gradient, invalid HMC authority metadata, runner crash, nonfinite samples, too-large step size, or unsupported claim leakage. |
| Promotion criterion | Each ladder tier writes a structured artifact whose hard-veto screen passes for its declared scope. |
| Promotion veto | Nonfinite target value/score, target-path autodiff/NumPy, invalid value/score authority, HMC runtime exception, nonfinite HMC samples, invalid artifact, wrong scalar fixture, or unsupported HMC/posterior/default/source-faithful claim. |
| Continuation veto | Required fix would change default policy, broaden into LEDH/source-faithful TTSIRT work, modify model files/public API, install packages, require detached execution without approval, require GPU without approval, or change pass/fail criteria after seeing results. |
| Repair trigger | Local implementation, adapter, initialization, step-size, artifact, or documentation failure fixable within the scalar HMC mechanics question. |
| What must not be concluded | No posterior correctness, HMC convergence, method superiority, source-faithful Zhao-Cui parity, GPU/XLA production readiness, default readiness, or LEDH result. |

## Global Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Whether the scalar SSL-LSTM `zhaocui_fixed` target can pass staged HMC mechanics gates with structured artifacts. |
| Exact baseline/comparator | Completed minimal smoke artifact `docs/benchmarks/minimal_ssl_lstm_zhaocui_smoke_cpu_hidden_2026-07-06.json`; existing `run_full_chain_tfp_hmc` and Phase 7 SSL-LSTM launch-smoke pattern. |
| Primary pass criterion | Scalar `zhaocui_fixed` target adapter and HMC canary/ladder artifacts pass their declared hard-veto screens. |
| Veto diagnostics | Nonfinite target value/score, wrong parameter dimension, nondeterminism, target-path autodiff/NumPy, invalid HMC metadata, HMC crash, nonfinite samples, invalid artifact, unsupported claims, or CPU/GPU evidence-class mismatch. |
| Explanatory diagnostics | Runtime, score norm, initial log prob, acceptance rate, sample finite counts, R-hat/ESS only in later predeclared replicated tier, and TensorFlow CUDA warnings under CPU-hidden execution. |
| Not concluded | Posterior correctness, HMC convergence, ranking, method superiority, source-faithful parity, LEDH result, GPU/XLA production readiness, or default readiness. |
| Preserved artifacts | Plans/results/reviews under `docs/plans` and `docs/reviews`; JSON/Markdown/log artifacts under `docs/benchmarks`. |

## Minimal Fixture Definition

| Quantity | Value | Provenance |
| --- | --- | --- |
| `horizon` | `2` | Completed minimal smoke fixture. |
| `latent_dim` | `1` | User request and completed minimal smoke fixture. |
| `hidden_dim` | `1` | User request and completed minimal smoke fixture. |
| `observation_dim` | `1` | User request and completed minimal smoke fixture. |
| observation vector | `[[0.12], [-0.03]]` | Completed minimal smoke artifact and focused adapter tests. |
| parameter dimension | `24` | `SSLLSTMStaticConfig` for scalar SSL-LSTM. |
| primary filter | `zhaocui_fixed` | User direction and completed smoke program. |
| HMC runner | `run_full_chain_tfp_hmc` | Existing BayesFilter HMC runner used by Phase 7 SSL-LSTM launch smoke. |

Numeric HMC settings are hypotheses or debug conveniences until a phase result
records their behavior. They are not sacred defaults.

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance, fixture freeze, and review setup | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase0-governance-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase0-governance-result-2026-07-06.md` |
| 1 | Minimal HMC target adapter bridge | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase1-target-adapter-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase1-target-adapter-result-2026-07-06.md` |
| 2 | CPU-hidden HMC canary | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase2-cpu-hidden-canary-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase2-cpu-hidden-canary-result-2026-07-06.md` |
| 3 | Repair loop and retest gate | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase3-repair-loop-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase3-repair-loop-result-2026-07-06.md` |
| 4 | Short replicated debug ladder | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase4-short-replicated-ladder-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase4-short-replicated-ladder-result-2026-07-06.md` |
| 5 | Optional trusted GPU/XLA bridge | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase5-optional-gpu-xla-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase5-optional-gpu-xla-result-2026-07-06.md` |
| 6 | Closeout and reset memo | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase6-closeout-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase6-closeout-result-2026-07-06.md` |

## Review And Repair Loop

1. Codex is supervisor and executor.
2. Claude is a read-only reviewer only.
3. Material subplans/results use compact review bundles in `docs/reviews`.
4. Claude review uses `claude_review_gate.sh` only after trusted execution is
   approved.
5. If Claude returns `REVISE`, patch the same artifact visibly and rerun
   focused local checks.
6. If Claude does not respond, use the tiny-probe protocol. If the probe
   responds, redesign the prompt/bundle. If the probe fails, use a fresh local
   Codex read-only substitute review and record the fallback.
7. Stop after five review rounds for the same blocker.
8. Claude cannot authorize runtime, model-file, funding, product-capability,
   public API, default-policy, GPU, detached, or scientific-claim boundaries.

## Boundary Rules

- Do not claim HMC convergence from canaries or short debug ladders.
- Do not claim posterior correctness.
- Do not claim method ranking or superiority.
- Do not claim source-faithful SSL-LSTM Zhao-Cui parity.
- Do not use target-path autodiff, finite differences, `tf.py_function`, or
  NumPy as the HMC target score.
- Do not let LEDH into this program.
- Do not change default policy, public API, model files, or package metadata.
- Do not launch long, GPU, detached, package-install, network, or external
  reviewer commands before explicit approval.
