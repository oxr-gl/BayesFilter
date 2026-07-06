# Actual-SIR Low-Rank LEDH Default-Certification Master Program

Date: 2026-06-24

Status: `COMPLETE_LOW_RANK_LEDH_DEFAULT_ENGINEERING_READY_BOUNDED`

Supervisor/executor: Codex in this conversation.

Claude role: read-only reviewer only. Claude cannot authorize crossing human,
runtime, model-file, funding, product-capability, default-policy, public API,
or scientific-claim boundaries.

## Purpose

Certify whether the TensorFlow/TFP low-rank coupling-solver route can become
the engineering default route for GPU/TF32 LEDH-PFPF-OT on the actual-SIR d18
lane, using the existing streaming TF32 route as comparator.

This program starts from the completed N3072 actual-SIR d18 replicated
low-rank evidence. It does not start from a blank slate, and it does not treat
warm transport timing alone as default-readiness evidence.

This program can end in one of three ways:

- `LOW_RANK_LEDH_DEFAULT_ENGINEERING_READY_BOUNDED`
- `LOW_RANK_LEDH_OPTIONAL_ROUTE_ONLY`
- `BLOCKED_OR_REPAIR_REQUIRED`

Even a pass does not establish posterior correctness, HMC readiness, dense
Sinkhorn equivalence, statistical superiority, public API readiness, broad
scientific validity, or formal memory-scaling proof unless a separately gated
phase explicitly adds that evidence.

## Current Evidence Anchor

The current strongest low-rank actual-SIR d18 result is:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-replicated-evidence-resource-boundary-result-2026-06-23.md`

That result validates four N3072 actual-SIR d18 rows across seed batches
`81137,81138` and `81139,81140` for two rank-16 candidates:

- `r16_eps0p25_alpha1em08_it120`
- `r16_eps0p125_alpha1em08_it120`

Both candidates remain viable under that bounded screen. The result explicitly
does not certify default readiness.

## Candidate Default

Default-certification candidate:

- route: `low_rank`
- rank: `16`
- assignment epsilon: `0.25`
- alpha: `1e-8`
- max projection iterations: `120`
- convergence threshold: `1e-6`
- denominator floor: `1e-30`
- dtype/target: `float32`, GPU, TF32 enabled
- timing source: compiled core

Rationale: this candidate passed all completed N3072 screens and had
descriptively smaller paired deltas than the other rank-16 survivor in the
completed N3072 artifacts. This is an engineering candidate selection only. It
is not a statistically supported ranking or a claim that the other viable
rank-16 candidate is invalid.

Fallback/repair candidate:

- `r16_eps0p125_alpha1em08_it120`

Fallback use requires a repair or selection subplan. It must not be silently
substituted after seeing a failed default-candidate result.

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Can the low-rank route, with a locked candidate configuration, be certified as the bounded engineering default for actual-SIR d18 GPU/TF32 LEDH-PFPF-OT? |
| Candidate or mechanism | TensorFlow/TFP low-rank coupling-solver resampling route, rank 16, epsilon 0.25, alpha `1e-8`, max projection iterations 120 |
| Comparator | Existing streaming TF32 actual-SIR route under the same model, seeds, shape, dtype, TF32 mode, GPU, and compiled-core timing contract |
| Serious model | `zhao_cui_spatial_sir_austria_j9_T20`, state dim `18`, obs dim `9`, actual callback/tensor setup from the owned validation harness |
| Expected failure mode | Default candidate may fail end-to-end timing, paired comparability, resource envelope, implementation-surface audit, no-NumPy audit, API/default test, HMC/autodiff screen, or review boundary |
| Engineering promotion criterion | Bounded default readiness requires: locked candidate, no-NumPy implementation path, current N3072 evidence preserved, additional end-to-end actual-SIR evidence passing hard vetoes and paired comparability, resource-boundary evidence or a documented N4096 blocker, focused implementation/default-surface tests, and final review convergence |
| Promotion veto | Any hard veto, missing actual-SIR semantics, missing GPU/XLA/TF32 provenance, dense transport materialization in the low-rank route, failed paired comparability, failed end-to-end gate, unreviewed default-code change, NumPy implementation backend in default path, unsupported claim, or missing required artifact |
| Continuation veto | Trusted GPU unavailable for GPU phases, corrupted artifacts, route mismatch, path-length failure, package/network dependency, default-policy change without human approval, public API change without human approval, or Claude/Codex nonconvergence after five rounds for the same blocker |
| Repair trigger | Fixable harness/reporting bug, path-length risk, stale artifact mismatch, narrow implementation-surface issue, or review finding that can be patched without changing the research question after seeing results |
| Explanatory diagnostics | Warm transport timings, first-call times, wall times, memory snapshots, log-likelihood deltas, ESS, residual magnitudes, projection iteration counts, filename lengths |
| Must not conclude without separate gate | Posterior correctness, HMC readiness, dense Sinkhorn equivalence, statistical superiority, scientific validity, formal memory scaling, public API readiness, or invalidity of viable/deferred candidates |

## Evidence Gates

| Gate | Required evidence | Role |
| --- | --- | --- |
| Actual-SIR semantics | row id/model metadata, `D=18`, `M=9`, actual callbacks used | hard veto |
| TensorFlow/TFP implementation | default path is TensorFlow/TFP and GPU/XLA-compatible; no NumPy implementation backend | hard veto |
| Route-fired evidence | low-rank route fires on all active resampling steps | hard veto |
| Nonmaterialization | low-rank route does not materialize dense `N x N` transport matrices | hard veto |
| Factor validity | finite nonnegative factors, positive `g`, residuals below threshold | hard veto |
| Log-weight normalization | final logsumexp residual `<= 1e-5` | hard veto |
| ESS floor | ESS fraction min `>= 0.01` | hard veto |
| Paired comparability | predeclared log-likelihood, filtered mean/variance, and final particle mean thresholds | hard veto for default candidate |
| End-to-end timing | whole command/row wall time and route warm medians recorded; default promotion cannot rely on warm median alone | promotion evidence with uncertainty limits |
| Resource envelope | N3072 replicated evidence plus N4096 feasibility or explicit reviewed resource-boundary blocker | default-readiness evidence or blocker |
| API/default surface | focused tests and docs/config review for any default switch | hard veto before code default change |
| HMC/autodiff | separate if the default claim includes differentiable/HMC use | optional branch; nonpass keeps HMC nonclaim |

## Phase Index

| Phase | Name | Subplan | Required result |
| ---: | --- | --- | --- |
| P00 | Governance, scope lock, and program review | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p00-governance-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p00-governance-result-2026-06-24.md` |
| P01 | Evidence inventory and default-surface audit | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p01-evidence-surface-audit-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p01-evidence-surface-audit-result-2026-06-24.md` |
| P02 | Reference, no-NumPy, and implementation-path audit | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p02-implementation-audit-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p02-implementation-audit-result-2026-06-24.md` |
| P03 | End-to-end actual-SIR benchmark harness/gate | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p03-end-to-end-benchmark-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p03-end-to-end-benchmark-result-2026-06-24.md` |
| P04 | N4096 resource-boundary feasibility | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p04-n4096-resource-boundary-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p04-n4096-resource-boundary-result-2026-06-24.md` |
| P05 | Default-route implementation and focused tests | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p05-default-implementation-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p05-default-implementation-result-2026-06-24.md` |
| P06 | Optional HMC/autodiff mechanics branch | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p06-hmc-autodiff-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p06-hmc-autodiff-result-2026-06-24.md` |
| P07 | Final default-readiness decision | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p07-closeout-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-result-2026-06-24.md` |

## Owned Write Set

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-*.md`
- `docs/benchmarks/actual-sir-low-rank-default-certification-*.json`
- `docs/benchmarks/actual-sir-low-rank-default-certification-*.md`
- `docs/benchmarks/logs/actual-sir-low-rank-default-certification-*.log`
- Focused tests or code only after a dedicated implementation subplan and
  human approval for default-route changes.

## Forbidden Writes

- BayesFilter public exports or defaults before P05 approval.
- Package metadata, lock files, model files, or dependency files.
- Existing benchmark result artifacts except read-only validation.
- Existing low-rank/Nystrom validation results except read-only context.
- Unrelated dirty worktree files.
- Any NumPy-backed BayesFilter-owned algorithmic default implementation.

## Skeptical Plan Audit

| Audit item | Status |
| --- | --- |
| Wrong baseline | Guarded: comparator remains paired streaming TF32 actual-SIR route, not synthetic-only evidence. |
| Proxy metric promoted | Guarded: warm ratios are explanatory unless paired validity and end-to-end/default gates pass. |
| Missing stop conditions | Guarded by phase-local stop conditions and review loop. |
| Unfair comparison | Guarded: paired rows must use same seeds, shape, dtype, TF32 mode, physical GPU, and timing contract. |
| Hidden assumptions | Guarded: default readiness is separated from posterior correctness, HMC, dense equivalence, API readiness, and scientific validity. |
| Stale context | Guarded: P01 must validate current artifacts and code surfaces before runtime. |
| Environment mismatch | Guarded: GPU phases require trusted GPU precheck and manifest evidence. |
| Artifact mismatch | Guarded: every phase has required result, ledger, and artifact validation. |

Audit conclusion: the program may proceed to P00 review and local-check-only
governance execution. P00/P01 may run local syntax, pytest, text search, and
artifact-validation commands, but GPU benchmark runtime, default-code changes,
API changes, HMC work, and scientific claims remain blocked until their own
reviewed subplans and human/runtime approvals.

## Claude Review Protocol

Claude prompts must send paths and concise scope only. Do not send whole files
inline. Claude is read-only and must end with exactly `VERDICT: AGREE` or
`VERDICT: REVISE`.

If Claude does not respond, Codex must run a small probe. If the probe
responds, Codex must redesign the review prompt and retry. Stop after five
review rounds for the same blocker.
