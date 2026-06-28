# Actual-SIR Low-Rank Repair Classification Master Program

Date: 2026-06-22
Status: `DRAFT_FOR_REVIEW`

Supervisor/executor: Codex in this conversation.

Claude role: read-only reviewer only. Claude cannot authorize crossing human,
runtime, model-file, funding, product-capability, default-policy, public API, or
scientific-claim boundaries. Claude review prompts must name paths only and must
not paste whole file contents.

## Reset Anchor

This program starts from the P03 tuning stop:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p03-tuning-screen-result-2026-06-22.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p03-stop-handoff-2026-06-22.md`

P03 status was `NO_FREEZE_CANDIDATE_REPAIR_REQUIRED`: `0`
freeze-nominated candidates, `7` comparable-but-slow candidates, `11`
incomparable candidates, and `2` ESS hard-vetoed candidates.

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Is the P03 no-freeze outcome primarily a route-execution/performance repair problem, an exposed-parameter tuning/comparability/ESS repair problem, or both? |
| Candidate/mechanism under diagnosis | Existing TensorFlow low-rank actual-SIR route as exercised by the P03 tuning grid. |
| Comparator | Existing compiled streaming actual-SIR TF32/GPU route used by `docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py` with `--streaming-timing-source compiled_core`. |
| Expected failure modes | Comparable low-rank candidates may be slow because the low-rank route is timed through diagnostic/eager paths; other candidates may fail comparability or ESS because exposed rank/epsilon settings are not viable. |
| Primary classification criterion | Existing P03 artifacts plus source inspection support a bounded classifier: `ROUTE_PERFORMANCE_REPAIR`, `TUNING_REPAIR`, `BOTH_REPAIRS`, or `UNCLASSIFIED_NEEDS_MICROPROBE`. |
| Promotion criterion | None. This program cannot promote a candidate, speedup, default route, posterior correctness, or scientific claim. |
| Promotion veto | Any attempt to treat artifact-only descriptive timing, one-seed tuning rows, source inspection, or a microprobe as speedup/default/scientific promotion. |
| Continuation veto | Missing or corrupted P03 artifacts, stale or mismatched source anchors, unsupported claim, route-internal edit before a reviewed implementation subplan, trusted GPU required but unavailable for any optional GPU probe, or five unresolved Claude review rounds for the same blocker. |
| Repair trigger | Classification identifies a specific next repair lane and the smallest next subplan needed to test it. |
| Explanatory diagnostics | Candidate labels, warm-time ratios, log-likelihood deltas, ESS hard vetoes, factor residuals, timing-source asymmetry, `tf.function`/XLA coverage, and eager/host-sync diagnostics. |
| What must not be concluded | No candidate freeze, no held-out support, no speedup claim, no posterior correctness, no HMC readiness, no dense Sinkhorn equivalence, no public API/default readiness, no statistical ranking, and no production route change. |

## Phase Index

| Phase | Name | Subplan | Required result |
| ---: | --- | --- | --- |
| 0 | Governance and launch audit | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-repair-classification-p00-governance-subplan-2026-06-22.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-repair-classification-p00-governance-result-2026-06-22.md` |
| 1 | P03 artifact classifier | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-repair-classification-p01-artifact-classifier-subplan-2026-06-22.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-repair-classification-p01-artifact-classifier-result-2026-06-22.md` |
| 2 | Code-path classifier | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-repair-classification-p02-code-path-classifier-subplan-2026-06-22.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-repair-classification-p02-code-path-classifier-result-2026-06-22.md` |
| 3 | Conditional microprobe plan | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-repair-classification-p03-conditional-microprobe-subplan-2026-06-22.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-repair-classification-p03-conditional-microprobe-result-2026-06-22.md` |
| 4 | Closeout and next repair handoff | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-repair-classification-p04-closeout-subplan-2026-06-22.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-repair-classification-result-2026-06-22.md` |

## Classification Vocabulary

| Classifier | Meaning | Allowed next step |
| --- | --- | --- |
| `ROUTE_PERFORMANCE_REPAIR` | Comparable candidates exist, but the measured failure is dominated by a route/timing implementation asymmetry, and comparability/ESS failures are not material for the next smallest repair. | Draft a reviewed route-performance implementation subplan. |
| `TUNING_REPAIR` | Route timing source is not the main blocker; exposed parameters plausibly need tuning for comparability/ESS before performance repair. | Draft a reviewed tuning-repair subplan. |
| `BOTH_REPAIRS` | P03 has independent evidence for route-performance failure among comparable candidates and parameter/comparability/ESS failure elsewhere. | Draft a route-performance-first subplan if source evidence shows timing asymmetry; otherwise draft the smallest discriminating probe. |
| `UNCLASSIFIED_NEEDS_MICROPROBE` | Artifact and source evidence cannot separate route overhead from tuning/comparability/ESS. | Execute Phase 3 only after reviewed microprobe plan and any required trusted GPU approval. |

## Owned Write Set

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-repair-classification-*.md`
- `docs/benchmarks/actual-sir-low-rank-repair-classification-*.json`
- `docs/benchmarks/actual-sir-low-rank-repair-classification-*.md`
- `docs/benchmarks/logs/actual-sir-low-rank-repair-classification-*.log`

## Forbidden Writes And Actions

- Do not edit low-rank solver internals in this program.
- Do not edit streaming route internals in this program.
- Do not run P04, P05, or P06 from the earlier tuning master program.
- Do not change public API, default policy, package metadata, dependency files,
  model files, or unrelated dirty worktree files.
- Do not widen gates or reinterpret P03 tuning rows after seeing results.
- Do not run long GPU tuning or held-out support from this classification
  program.

## Skeptical Plan Audit

| Audit item | Status |
| --- | --- |
| Wrong baseline | Guarded: the comparator remains the compiled streaming actual-SIR route used in P03, not synthetic rows or dense Sinkhorn. |
| Proxy metrics promoted | Guarded: timing/source/artifact diagnostics classify repairs only; they do not promote speedup or correctness. |
| Missing stop conditions | Guarded by phase stop conditions and continuation vetoes. |
| Unfair comparison | Guarded: P01 uses the exact paired P03 artifacts; P02 inspects timing-source asymmetry before any timing conclusion. |
| Hidden assumptions | Guarded: low-rank route may be diagnostic/eager; source inspection must verify before classification. |
| Stale context | Guarded by P00 artifact/source existence checks. |
| Environment mismatch | Guarded: optional GPU microprobe is conditional and trusted-context only. |
| Artifact mismatch | Guarded: every phase writes a result artifact that answers only its phase question. |

Audit conclusion: execution may start only after local structural checks and
read-only Claude review of this master program and the initial subplans.

## Repair Loop Protocode

For each phase:

1. Read the subplan and restate the phase evidence contract.
2. Run only the smallest local check or command that answers the phase question.
3. Preserve full output in declared logs when output may be noisy.
4. Assess hard vetoes before descriptive diagnostics.
5. Write the phase result or blocker result.
6. Draft or refresh the next subplan.
7. Review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
8. Use Claude read-only review for material subplans/results.
9. If review finds a fixable problem, patch the same subplan visibly, rerun
   focused checks, and rerun Claude review.
10. Stop after five Claude review rounds for the same blocker.

Expected P03 failure is not a continuation veto. Stop only when a true
continuation veto fires or when the classification result requires a separate
implementation/tuning program.

## Claude Review Protocol

Use the narrow worker wrapper with escalation:

```bash
timeout 900 bash /home/ubuntu/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/ubuntu/python/BayesFilter \
  --name actual-sir-lr-repair-classification-review \
  --model opus \
  --effort max \
  --output-format text \
  "<path-only read-only review prompt>"
```

If Claude does not respond, run a small read-only probe. If the probe responds,
redesign the review prompt and retry. If review finds a fixable problem, patch
the same subplan visibly and rerun focused checks. Stop after five rounds for
the same blocker.
