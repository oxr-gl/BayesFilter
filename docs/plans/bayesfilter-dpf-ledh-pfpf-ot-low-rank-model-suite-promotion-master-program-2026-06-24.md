# Low-Rank LEDH-PFPF-OT Model-Suite Promotion Master Program

Date: 2026-06-24

Status: `STOPPED_AT_P01_HARD_ROUTE_DIAGNOSTIC_VETO`

Supervisor/executor: Codex in this conversation.

Claude role: read-only reviewer only. Claude cannot authorize crossing human,
runtime, model-file, funding, product-capability, default-policy, public API,
HMC, or scientific-claim boundaries.

## Purpose

Decide whether the locked low-rank LEDH-PFPF-OT route can be promoted beyond
the completed actual-SIR d18 validation/reporting lane into a bounded
model-suite engineering recommendation, or whether it must remain a bounded
optional route.

The starting point is the completed result:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-result-2026-06-24.md`

That result remains valid in its bounded lane regardless of later model-suite
outcomes. This program tests additional boundaries and does not rewrite the
earlier verdict.

## Candidate Lock

Candidate:

- route: low-rank LEDH-PFPF-OT through TensorFlow/TFP paths;
- candidate id: `r16_eps0p25_alpha1em08_it120`;
- rank: `16`;
- assignment epsilon: `0.25`;
- alpha: `1e-8`;
- max projection iterations: `120`;
- convergence threshold: `1e-6`;
- denominator floor: `1e-30`;
- execution target: GPU/TF32/XLA where runtime evidence is claimed;
- comparator: current streaming GPU/TF32 LEDH-PFPF-OT route unless a phase
  explicitly names an exact reference or separate comparator.

Candidate settings may not be changed after seeing model-suite results unless
a reviewed repair phase explicitly reopens candidate selection and downgrades
promotion claims.

## Possible Final States

- `LOW_RANK_LEDH_MODEL_SUITE_ENGINEERING_RECOMMENDED_BOUNDED`
- `LOW_RANK_LEDH_OPTIONAL_ROUTE_ONLY`
- `LOW_RANK_LEDH_REPAIR_REQUIRED`
- `BLOCKED_HUMAN_DIRECTION_REQUIRED`

No final state in this program alone authorizes an actual default-policy
change, public API switch, package release, funding claim, scientific claim, or
HMC readiness unless the corresponding phase explicitly passes, separate human
approval is recorded, and the final decision preserves scope. In particular,
the phrase "model-suite engineering recommendation" is a bounded internal
evidence verdict, not a package-level or public default switch.

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Does the locked low-rank LEDH-PFPF-OT route remain valid, useful, and safe enough across a minimal model suite to justify a bounded internal engineering recommendation beyond actual-SIR d18? |
| Candidate under test | Locked low-rank route `r16_eps0p25_alpha1em08_it120`. |
| Baseline/comparator | Streaming GPU/TF32 LEDH-PFPF-OT; exact Kalman for LGSSM quality; phase-local references where declared. |
| Expected failure mode | Low-rank may be fast but degrade filtering quality, fail exact-reference checks, become unstable under nonlinear/stiff/non-Gaussian models, lose differentiability, or fail resource gates. |
| Promotion criterion | All required model gates pass their hard validity and quality screens, implementation remains TensorFlow/TFP GPU/XLA oriented with no active-path NumPy barrier, and final review converges without unsupported claims. |
| Promotion veto | Exact-reference failure in LGSSM, hard route/provenance failure, active-path NumPy, dense materialization in default path, nonfinite outputs, missing comparator, unsupported claim, or failed final review. |
| Continuation veto | Corrupt artifacts, harness invalidity, missing required diagnostics, unapproved runtime boundary, Claude/Codex nonconvergence after five rounds for the same blocker, or a result that invalidates the implementation rather than only rejecting the candidate. |
| Repair trigger | Fixable metadata, harness, diagnostic, or review issue that does not change observed promotion criteria after seeing results. |
| Explanatory diagnostics | Timings, memory deltas, ESS, tail metrics, Jacobian diagnostics, and descriptive seed variation unless a phase declares them as hard screens. |
| Must not conclude | Statistical superiority, posterior correctness, dense Sinkhorn equivalence, broad production readiness, package/API readiness, or HMC readiness unless explicitly gated. |

## Phase Index

| Phase | Name | Primary role | Subplan | Result |
| --- | --- | --- | --- | --- |
| P00 | Governance and launch review | plan safety | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p00-governance-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p00-governance-result-2026-06-24.md` |
| P01 | LGSSM exact-Kalman gate | exact-reference quality | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p01-lgssm-kalman-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p01-lgssm-kalman-result-2026-06-24.md` |
| P02 | Actual-SIR stress extension | target-family robustness | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p02-actual-sir-stress-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p02-actual-sir-stress-result-2026-06-24.md` |
| P03 | Nonlinear Gaussian gate | local-linearization stress | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p03-nonlinear-gaussian-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p03-nonlinear-gaussian-result-2026-06-24.md` |
| P04 | Stochastic-volatility and heavy-tail gate | non-Gaussian filtering stress | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p04-sv-heavy-tail-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p04-sv-heavy-tail-result-2026-06-24.md` |
| P05 | Stiff nonlinear dynamics gate | stiff/Jacobian stress | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p05-stiff-nonlinear-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p05-stiff-nonlinear-result-2026-06-24.md` |
| P06 | Large-N and long-T resource envelope | scale and storage | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p06-resource-envelope-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p06-resource-envelope-result-2026-06-24.md` |
| P07 | HMC/autodiff mechanics | inference-readiness boundary | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p07-hmc-autodiff-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p07-hmc-autodiff-result-2026-06-24.md` |
| P08 | Final promotion decision | scoped verdict | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p08-closeout-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-result-2026-06-24.md` |

## Whole-Program Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the locked low-rank LEDH-PFPF-OT route be promoted beyond actual-SIR d18 into a bounded model-suite engineering recommendation? |
| Baseline/comparator | Streaming GPU/TF32 LEDH-PFPF-OT and exact Kalman for LGSSM; phase-local references as declared. |
| Primary pass criterion | P01 through P06 pass hard gates; P07 passes if HMC readiness is claimed or is explicitly skipped as a nonclaim; P08 review converges without unsupported claims. |
| Veto diagnostics | Active-path NumPy, untrusted GPU evidence for GPU claims, exact-reference failure, nonfinite outputs, route mismatch, dense materialization, missing artifacts, failed local tests, unsupported claim, or review nonconvergence. |
| Explanatory diagnostics | Timings, memory, ESS, q95/q99 tails, warm ratios, Jacobian summaries, and per-seed descriptive variation. |
| Not concluded | Statistical superiority, posterior correctness beyond tested references, dense Sinkhorn equivalence, package/public API readiness, package-level or public default-policy change, broad product readiness, or scientific validity. |
| Artifacts | Master program, visible runbook, per-phase subplans/results, JSON/Markdown benchmark artifacts, logs under `docs/logs/low-rank-ledh-model-suite-promotion-2026-06-24/`, Claude review ledger, execution ledger, final result. |

## Skeptical Plan Audit

| Audit item | Status |
| --- | --- |
| Wrong baseline | Guarded: each phase names exact reference or streaming comparator; actual-SIR is not used as the sole promotion model. |
| Proxy metric promoted | Guarded: timing and memory are explanatory unless a phase declares a hard resource screen; quality gates precede speed claims. |
| Missing stop conditions | Guarded: each subplan names hard stops and human approval boundaries. |
| Unfair comparison | Guarded: paired runtime rows require same seeds, shape, dtype, TF32 mode, GPU, and timing contract. |
| Hidden assumptions | Guarded: LGSSM exact reference, synthetic LGSSM-shaped benchmarks, and real actual-SIR target-family evidence are kept distinct. |
| Stale context | Guarded: P00 reruns source/artifact inventory before material execution. |
| Environment mismatch | Guarded: GPU claims require trusted GPU execution; CPU/local checks cannot establish GPU readiness. |
| Artifact mismatch | Guarded: every phase names result and structured artifact paths before execution. |

Conclusion: this draft is suitable for local document checks and read-only
Claude review. P00 may launch after review convergence. Later GPU, model-suite,
code-writing, and HMC boundaries require the approvals listed below.

## Anticipated Human Approvals

This program asks for approval in advance only as scoped permission intent, not
as authority to skip phase gates:

- Claude Code reviewer usage through
  `bash /home/ubuntu/python/claudecodex/scripts/claude_worker.sh` with
  `--model opus --effort max`, read-only prompts only.
- Trusted GPU probes and benchmark execution for P01 through P06 after each
  material subplan converges.
- Bounded documentation and harness edits inside `docs/benchmarks`,
  `tests`, and `docs/plans` only if a phase discovers a fixable local harness
  gap before runtime.
- HMC/autodiff runtime only in P07, and only if P07 is explicitly approved
  after P01 through P06 results.

No approval is requested for package installation, network fetches, commits,
pushes, destructive git operations, public API changes, package-level default
switches, model-file changes, or scientific claims.

## Repair Loop

If Claude or local checks find a fixable material issue:

1. Patch the same subplan or result visibly.
2. Rerun focused local checks.
3. Rerun Claude review at Opus/max effort for material issues.
4. Stop after five rounds for the same blocker and write a blocker result.

Claude is never an execution authority. Claude agreement is evidence of review
convergence only.

## Status Update Protocol

Every phase must append to:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-visible-execution-ledger-2026-06-24.md`

Every Claude review must append to:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-claude-review-ledger-2026-06-24.md`

If blocked or complete, update:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-visible-stop-handoff-2026-06-24.md`
