# Li-Coates Algorithm 1 LEDH-PFPF UKF Source-Faithful Master Program

Date: 2026-06-10

## Status

`DRAFT_FOR_VISIBLE_CLAUDE_REVIEW`

## Decision

Create a new source-faithfulness program for BayesFilter's LEDH-PFPF work.  The
program treats all previous `LEDH-PFPF-OT` result artifacts as superseded for
method evidence until a Li-Coates Algorithm 1 implementation with per-particle
UKF covariance prediction/update has passed documentation, implementation,
faithfulness, and rerun gates.

Historical files are not deleted.  They are quarantined for auditability and may
be cited only as evidence of the older implementation lineage, not as evidence
about source-faithful LEDH-PFPF performance.

## Role Contract

Codex in the current dialogue is the visible supervisor and executor.

Claude is a read-only reviewer only.  Claude review is required for material
plan, implementation, audit, and result gates, with convergence required or a
maximum of five review loops per gate.

Execution must be visible in this dialogue.  Do not use detached supervisors,
copied workspaces, `codex exec`, `overnight_gated_launch.sh`, `setsid`, `nohup`,
backgrounded phase runners, or nested agent execution for this program.

## Program Files

- Master program: `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-master-program-2026-06-10.md`
- Visible execution runbook: `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-visible-gated-execution-runbook-2026-06-10.md`
- Claude review ledger: `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-claude-review-ledger-2026-06-10.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| P0 | Governance and Evidence Quarantine | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p0-governance-quarantine-subplan-2026-06-10.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p0-governance-quarantine-result-2026-06-10.md` |
| P1 | LaTeX Documentation Rewrite | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p1-documentation-rewrite-subplan-2026-06-10.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p1-documentation-rewrite-result-2026-06-10.md` |
| P2 | UKF Covariance Lifecycle Design | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p2-ukf-covariance-design-subplan-2026-06-10.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p2-ukf-covariance-design-result-2026-06-10.md` |
| P3 | Algorithm 1 Implementation | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p3-implementation-subplan-2026-06-10.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p3-implementation-result-2026-06-10.md` |
| P4 | Faithfulness Audit | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p4-faithfulness-audit-subplan-2026-06-10.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p4-faithfulness-audit-result-2026-06-10.md` |
| P5 | Test Rerun And Comparisons | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p5-rerun-comparison-subplan-2026-06-10.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p5-rerun-comparison-result-2026-06-10.md` |
| P6 | Supersession Closeout | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p6-supersession-closeout-subplan-2026-06-10.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p6-supersession-closeout-result-2026-06-10.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter replace the previous LEDH-PFPF-OT evidence with a source-faithful Li-Coates Algorithm 1 LEDH-PFPF implementation that carries per-particle UKF prediction/update covariance state and then rerun the affected tests/comparisons? |
| Baseline/comparator | Primary source: Li and Coates, `Particle Filtering with Invertible Particle Flow`, local source `/tmp/li2017_particle_flow_source/PFPF_jrnl_2017.tex`, especially LEDH coefficients, PF-PF proposal/weight derivation, Algorithm 1, and covariance-estimation discussion. Documentation baselines: `docs/chapters/ch19b_dpf_literature_survey.tex` and `docs/chapters/ch19c_dpf_implementation_literature.tex`. Implementation baseline to supersede: current LEDH-PFPF-OT and `run_ledh_pfpf_source_faithful_repair_tf.py` lineage. |
| Primary pass criterion | A new documented and audited implementation follows Algorithm 1's per-particle covariance lifecycle: maintain `P_{k-1}^i`, apply UKF prediction to obtain `(m_{k|k-1}^i, P^i)`, use `P^i` in the LEDH flow, apply UKF update to obtain `P_k^i`, and resample covariance state consistently with particle state and weights. |
| Veto diagnostics | Missing per-particle covariance state; using one shared covariance as if it were Algorithm 1; omitting UKF prediction or update; dropping covariance state during resampling/OT; using the previous auxiliary-flow-only repair as final evidence; unsupported LaTeX claims; non-finite particles, weights, determinants, UKF covariances, or Cholesky/SVD factors; changing pass criteria after seeing results. |
| Explanatory diagnostics | Particle-count ladders, old-vs-new LEDH row deltas, bootstrap-OT comparisons, UKF/CUT4/Zhao-Cui comparisons on compatible models, runtime, ESS, determinant distributions, covariance eigenvalue summaries, fixed-branch gradient residuals. These explain behavior but cannot promote a non-faithful implementation. |
| Not concluded | No production default change, no HMC-readiness claim, no universal LEDH-PFPF superiority claim, no claim that OT resampling is part of Li-Coates Algorithm 1, no claim that UKF is mandated by the paper's experiments. |
| Artifacts | Phase results, Claude review ledger, source-support/claim-support tables, implementation diffs, test logs, comparison JSON/Markdown reports, and final supersession closeout. |

## Source-Support Anchors

| Source object | Local anchor | Current interpretation |
| --- | --- | --- |
| LEDH particle-local coefficients | `/tmp/li2017_particle_flow_source/PFPF_jrnl_2017.tex` lines 428-443 | LEDH linearizes at particle-local or auxiliary states and forms particle-specific `A^i(lambda), b^i(lambda)`. |
| PF-PF proposal and weight | same source lines 542-599 | The post-flow proposal density is corrected by the forward map determinant; PF-PF(LEDH) uses a product of per-pseudo-time determinants. |
| Predictive covariance need | same source lines 602-634 | The LEDH flow for each particle requires predicted covariance. EKF or UKF covariance prediction can estimate it when the dynamic model is not linear Gaussian. |
| Algorithm 1 lifecycle | same source lines 636-682 | The algorithm carries per-particle covariance through prediction, flow, update, and optional resampling. |
| Invertibility proof conditions | same source lines 686-740 and following proof text | Bounded local linearization and nonsingular discretized steps are part of the determinant/invertibility story and should become diagnostics. |
| Paper simulation choice | same source around lines 1388-1390 and 1513 | The paper reports using Kalman/EKF covariance equations in simulations; BayesFilter's requested UKF route is an Algorithm 1 allowed option and must be labelled as such. |

## Algorithm 1 Obligation Table

| Obligation | Source anchor | Documentation requirement | Implementation requirement | Test/audit requirement |
| --- | --- | --- | --- | --- |
| Maintain per-particle covariance | Algorithm 1 lines 642-643, 672-676 | Explain `P_{k-1}^i`, `P^i`, and `P_k^i` as particle-indexed state. | Store covariance tensor with shape `[num_particles, dim, dim]` or equivalent structured representation. | Unit test proves covariances differ by particle on nonlinear fixtures and survive resampling. |
| UKF prediction | Algorithm 1 lines 642-643, covariance discussion lines 631-634 | Derive the UKF prediction object used by BayesFilter and distinguish it from EKF/paper simulation choices. | Implement `(x_{k-1}^i, P_{k-1}^i) -> (m_{k|k-1}^i, P^i)` with TensorFlow/TFP, float64, and PSD diagnostics. | Linear-Gaussian collapse test matches Kalman covariance within numerical tolerance; nonlinear smoke emits finite covariances. |
| Zero-noise transition anchor for flow | Algorithm 1 lines 644-648 | Explain `bar_eta^i` and `bar_eta_0^i = g_k(x_{k-1}^i, 0)` separately from the UKF predictive mean. | Do not silently replace `bar_eta_0^i` with `m_{k|k-1}^i` unless a reviewed BayesFilter extension is explicitly labelled. | Audit route identifier records whether the flow anchor is `zero_noise_transition` or a reviewed extension. |
| Flow coefficients use predicted covariance | Algorithm 1 lines 654-657 | State that the LEDH coefficients use `P = P^i` for each particle. | Coefficient builder receives the particle's own predicted covariance. | Code audit maps coefficient inputs to `P^i`; shared-covariance shortcuts veto. |
| Migrate auxiliary and actual particles | Algorithm 1 lines 658-660 | Explain auxiliary-state migration and actual-particle migration as separate roles. | Flow updates both `bar_eta^i` and `eta_1^i` with the same local affine step. | Diagnostic records auxiliary-vs-actual separation and determinant product. |
| Accumulate determinant product | Algorithm 1 lines 661-662 and equation around lines 587-599 | Derive forward log determinant as sum of log absolute determinants. | Accumulate `sum_j log abs det(I + epsilon_j A_j^i)`. | Finite-difference/autodiff determinant check on scalar/small fixtures; singular steps veto. |
| PF-PF weight | Algorithm 1 lines 665-668 | State density objects: transition density at post-flow state, observation density, pre-flow proposal density, determinant, previous weight. | Weight update uses the same objects from the same path. | Hand-calculation fixture and non-finite log-weight veto. |
| UKF update | Algorithm 1 lines 670-673 | Derive UKF update and relation to observation model. | Implement `(m_{k|k-1}^i, P^i) -> (m_{k|k}^i, P_k^i)`. | Linear-Gaussian collapse test matches Kalman update covariance; nonlinear covariances finite/PSD. |
| Resample covariance state | Algorithm 1 lines 675-676 | Explain optional resampling of `{x_k^i, P_k^i, w_k^i}` and distinguish classical vs OT resampling. | Any resampling route must move/select covariance state consistently with particle state. OT is a BayesFilter extension and must be labelled. | Test verifies covariance ancestry/transport under resampling; dropping `P_k^i` vetoes. |

## Phase Gates

Each phase must pass a skeptical plan audit before execution.  Material phases
must pass Claude read-only review before advancing.  A phase can advance only if
its result artifact records:

- the phase evidence contract;
- exact commands and files changed;
- diagnostics and veto status;
- a decision table;
- what was not concluded;
- Claude review verdict or the reason review was not applicable.

Serious execution phases, including P3 implementation checks and P5 comparison
runs, must also include a run manifest with:

- git branch and commit;
- exact command;
- environment or conda environment;
- CPU/GPU status and `CUDA_VISIBLE_DEVICES` status before TensorFlow import;
- data/model fixture version or digest where applicable;
- random seeds and particle counts;
- pseudo-time schedule and UKF parameter settings;
- route identifiers;
- wall time;
- output artifact paths;
- plan and result artifact paths.

## Review Loop

For every material plan, implementation, audit, or result review:

1. Codex writes or updates the artifact.
2. Codex asks Claude for read-only review with the current artifact paths and
   explicit instruction not to edit, run experiments, or change state.
3. If Claude returns `VERDICT: REVISE`, Codex either repairs the artifact or
   records a blocker, then repeats.
4. Stop after `VERDICT: AGREE` or after five review loops for the same gate.

## Pre-Mortem

How this program could pass while still being wrong:

- The implementation could keep the previous auxiliary-flow-only repair and add
  a superficial UKF call whose covariance is not actually used in `A^i,b^i`.
  Control: route identifiers plus code audit must prove `P^i` feeds the LEDH
  coefficient builder.
- The implementation could use one global covariance while claiming
  per-particle UKF state.  Control: tests must show particle-indexed covariance
  tensors and resampled covariance ancestry.
- The documentation could summarize Algorithm 1 but omit the `P_k^i` lifecycle.
  Control: P1 claim-support table must include all Algorithm 1 obligation rows.
- OT resampling could be treated as source-faithful Algorithm 1.  Control: OT is
  labelled as a BayesFilter extension after the core Li-Coates filter.

How this program could fail for reasons other than the idea being bad:

- UKF sigma-point parameters or covariance stabilization could be poorly tuned.
  Control: linear-Gaussian collapse and small nonlinear smoke tests precede full
  comparison ladders.
- LEDH pseudo-time steps could produce near-singular affine factors.
  Control: determinant/eigenvalue diagnostics report the first failing
  particle/time/step before changing the algorithm.
- Monte Carlo uncertainty could obscure comparison rankings.
  Control: P5 uses multi-seed uncertainty intervals and normalized metrics; no
  one-seed ranking is promoted.

## Skeptical Plan Audit

| Risk | Audit status | Control |
| --- | --- | --- |
| Wrong baseline | pass for review | Primary baseline is Li-Coates Algorithm 1 plus checked source anchors, not the previous BayesFilter result table. |
| Proxy metrics promoted | pass for review | Particle ladders and value/gradient errors cannot promote the filter unless P4 faithfulness passes. |
| Missing stop condition | pass for review | Vetoes include missing covariance lifecycle, shared covariance shortcut, non-finite numerics, unsupported claims, and failed Claude convergence. |
| Unfair comparison | pass for review | P5 compares only on model/filter pairs with valid oracle/comparator scope and records unsupported pairs as not applicable. |
| Hidden assumption | pass for review | UKF is labelled as a permitted Algorithm 1 option requested by BayesFilter, not as the paper's simulation default. |
| Stale context | pass for review | P0 requires a fresh LEDH-PFPF-OT artifact inventory before supersession. |
| Artifact mismatch | pass for review | Every phase has a required result artifact and review trail. |
| Environment mismatch | pass for review | CPU-only TensorFlow runs must set `CUDA_VISIBLE_DEVICES=-1` before import; GPU/CUDA commands require trusted escalation. |

## Execution Order

Do not implement or rerun comparisons until P0-P2 pass review.  Do not treat any
performance result as meaningful until P4 passes.  P5 comparison tables replace
previous LEDH-PFPF-OT evidence only after P6 writes the supersession closeout.
