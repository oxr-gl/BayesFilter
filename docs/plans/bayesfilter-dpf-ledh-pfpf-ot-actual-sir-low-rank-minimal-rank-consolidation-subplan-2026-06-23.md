# Actual-SIR Low-Rank Minimal-Rank Consolidation Subplan

Date: 2026-06-23

Status: `DRAFT_READY_FOR_READ_ONLY_REVIEW_BEFORE_EXECUTION`

## Phase Objective

Consolidate the five viable low-rank actual-SIR candidates into a
minimal-rank survivor tier for the next larger-`N` validation phase, using only
hard-veto survival and resource-envelope criteria. This phase is document and
artifact analysis only; it does not run a GPU benchmark.

## Entry Conditions Inherited From Previous Phase

- The N1024 seed-replication result
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n1024-seed-replication-result-2026-06-23.md`
  left exactly five candidates viable.
- The five viable candidates are:
  - `r16_eps0p25_alpha1em08_it120`
  - `r16_eps0p125_alpha1em08_it120`
  - `r32_eps0p25_alpha1em08_it120`
  - `r64_eps0p25_alpha1em08_it120`
  - `r128_eps0p25_alpha1em08_it120`
- All five candidates passed the predeclared hard-veto, paired-comparability,
  warm-screen, GPU/XLA provenance, and artifact-presence gates at `N=512`, the
  first `N=1024` paired-validation screen, and the independent `N=1024`
  seed-replication screen.
- `r64_eps0p125_alpha1em08_it120` remains excluded because it failed heldout
  paired comparability. It must not be revived without a separate repair/tuning
  subplan.

## Required Artifacts

- This subplan.
- Consolidation result/close record:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-minimal-rank-consolidation-result-2026-06-23.md`
- Artifact consistency check output recorded in the close record.
- Next larger-`N` validation subplan for the consolidated survivor tier if the
  consolidation criteria pass.
- Claude read-only review ledger if the subplan is materially revised:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-minimal-rank-consolidation-review-ledger-2026-06-23.md`

The phase result/close record must include a decision table,
inference-status table, post-run red-team note, and run manifest with git
commit, command, environment, CPU/GPU status as applicable, source artifact
paths, plan path, and result path.

## Source Artifact Manifest

The consolidation phase must use exactly these source artifacts:

| Source | Result note | Aggregate JSON | Aggregate Markdown |
| --- | --- | --- | --- |
| `n512_seed_replication` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n512-seed-replication-result-2026-06-23.md` | `docs/benchmarks/actual-sir-low-rank-n512-seed-replication-2026-06-23.json` | `docs/benchmarks/actual-sir-low-rank-n512-seed-replication-2026-06-23.md` |
| `n1024_paired_validation` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n1024-paired-validation-result-2026-06-23.md` | `docs/benchmarks/actual-sir-low-rank-n1024-paired-validation-2026-06-23.json` | `docs/benchmarks/actual-sir-low-rank-n1024-paired-validation-2026-06-23.md` |
| `n1024_seed_replication` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n1024-seed-replication-result-2026-06-23.md` | `docs/benchmarks/actual-sir-low-rank-n1024-seed-replication-2026-06-23.json` | `docs/benchmarks/actual-sir-low-rank-n1024-seed-replication-2026-06-23.md` |

Each source aggregate must contain exactly these row ids in this order:

1. `r16_eps0p25_alpha1em08_it120`
2. `r16_eps0p125_alpha1em08_it120`
3. `r32_eps0p25_alpha1em08_it120`
4. `r64_eps0p25_alpha1em08_it120`
5. `r128_eps0p25_alpha1em08_it120`

For each row id, the exact `row_json`, `row_markdown`, and `row_log` paths
recorded in the source aggregate JSON are part of this manifest and must exist.
Any source-manifest mismatch, missing result note, missing aggregate artifact,
or missing recorded row artifact triggers a blocker/repair result rather than
partial consolidation.

## Required Checks, Tests, And Reviews

- Skeptical plan audit before execution.
- Local artifact consistency check over:
  - `docs/benchmarks/actual-sir-low-rank-n512-seed-replication-2026-06-23.json`
  - `docs/benchmarks/actual-sir-low-rank-n1024-paired-validation-2026-06-23.json`
  - `docs/benchmarks/actual-sir-low-rank-n1024-seed-replication-2026-06-23.json`
- The consistency check must verify:
  exact candidate ids, aggregate `PASS` status, row `PASS` status, empty hard
  vetoes, paired comparability pass, warm-screen pass, GPU/TF32 provenance,
  low-rank provenance, and row JSON/Markdown/log artifact presence.
- Focused documentation check that this subplan contains the resource-envelope
  criterion, nonclaims, stop conditions, and exact next-phase handoff.
- Claude Opus/max may be used as a read-only reviewer for this material
  subplan. Claude is not an execution authority and cannot authorize crossing
  human, runtime, model-file, funding, product-capability, default-policy, or
  scientific-claim boundaries.

## Evidence Contract

- Question: among the five candidates that remain viable after independent
  `N=1024` seed replication, which candidates should be carried forward as the
  smallest resource-envelope survivor tier for the next larger-`N` validation?
- Comparator: not a performance comparator. The criterion is hard-veto
  survival plus implementation resource envelope.
- Candidate set:
  - `r16_eps0p25_alpha1em08_it120`
  - `r16_eps0p125_alpha1em08_it120`
  - `r32_eps0p25_alpha1em08_it120`
  - `r64_eps0p25_alpha1em08_it120`
  - `r128_eps0p25_alpha1em08_it120`
- Consolidation criterion:
  1. a candidate must have passed all required gates in the source artifacts;
  2. among passing candidates, select the smallest low-rank rank tier;
  3. if multiple candidates share that smallest rank, carry all of them forward
     unless a separate reviewed subplan declares an additional engineering
     criterion.
- For this subplan, resource envelope means low-rank rank tier only; timing,
  warm ratios, wall times, deltas, and residual magnitudes are explanatory only
  and may not eliminate or rank viable candidates.
- Expected consolidated survivor tier:
  - `r16_eps0p25_alpha1em08_it120`
  - `r16_eps0p125_alpha1em08_it120`
- Deferred but still viable candidates:
  - `r32_eps0p25_alpha1em08_it120`
  - `r64_eps0p25_alpha1em08_it120`
  - `r128_eps0p25_alpha1em08_it120`
- Promotion vetoes: missing source artifact, corrupt JSON, candidate mismatch,
  aggregate failure, row failure, nonempty hard vetoes, failed paired
  comparability, failed warm screen, missing GPU/TF32 or low-rank provenance,
  missing row artifacts, or any need to rank candidates by descriptive timing
  or deltas.
- Explanatory diagnostics only: warm ratios, row wall times, log-likelihood
  deltas, factor residual magnitudes below threshold, and observed row ordering.
- What will not be concluded: statistical ranking, speedup, posterior
  correctness, HMC readiness, dense Sinkhorn equivalence, public API/default
  readiness, broad scalable-OT superiority, production scientific validity, or
  that deferred higher-rank candidates are worse.
- Artifact preserving result: the consolidation result/close record and the
  source aggregate artifacts listed above.

## Research Intent Ledger

| Field | Entry |
| --- | --- |
| Main question | Which viable candidates form the smallest resource-envelope tier for the next larger-`N` screen? |
| Candidate or mechanism under test | Low-rank actual-SIR route candidate tiering after hard-veto survival |
| Expected failure mode | Source artifact mismatch, missing provenance, missing row artifacts, or accidental ranking by descriptive metrics |
| Promotion criterion | All source artifacts pass consistency checks and the smallest passing rank tier is identified |
| Promotion veto | Any source artifact or row gate failure; any attempt to rank by descriptive timing/delta metrics |
| Continuation veto | Missing/corrupt artifacts, inconsistent candidate set, unsupported claim boundary, or inability to draft a next subplan |
| Repair trigger | Artifact/provenance mismatch requiring a focused artifact repair or rerun subplan |
| Explanatory diagnostics | Warm ratios, row times, deltas, residual magnitudes, and observed per-row variation |
| Must not conclude | Best candidate, statistical superiority, speedup, correctness, default readiness, or invalidity of deferred viable candidates |

## Skeptical Plan Audit

- Wrong baseline check: this phase is not a baseline comparison and must not
  compare candidates as if descriptive timing proves performance.
- Proxy metric check: warm ratios, wall times, and deltas are explanatory only;
  they do not choose the consolidated tier.
- Stop condition check: missing artifacts, candidate mismatches, source gate
  failures, or forbidden claim pressure block consolidation.
- Fairness check: the consolidation criterion uses only hard-veto survival and
  rank as a resource-envelope parameter; it does not prefer a candidate because
  of observed descriptive timing.
- Hidden assumption check: the smallest rank tier is a resource-envelope
  representative for larger-`N` validation, not a proof that higher ranks are
  unnecessary or inferior.
- Environment mismatch check: no GPU run is part of this phase; CPU/GPU status
  in the close record is documentation-only.
- Artifact sufficiency check: source aggregate JSONs and row artifacts must be
  present and internally consistent.

Audit result: passes as a document-only consolidation gate because it narrows
the next execution tier by predeclared resource-envelope logic while preserving
the viability of deferred candidates and all scientific-claim boundaries.

## Candidate Artifact Check Command

```bash
python - <<'PY'
import json
from pathlib import Path

source_paths = [
    Path("docs/benchmarks/actual-sir-low-rank-n512-seed-replication-2026-06-23.json"),
    Path("docs/benchmarks/actual-sir-low-rank-n1024-paired-validation-2026-06-23.json"),
    Path("docs/benchmarks/actual-sir-low-rank-n1024-seed-replication-2026-06-23.json"),
]
expected = [
    "r16_eps0p25_alpha1em08_it120",
    "r16_eps0p125_alpha1em08_it120",
    "r32_eps0p25_alpha1em08_it120",
    "r64_eps0p25_alpha1em08_it120",
    "r128_eps0p25_alpha1em08_it120",
]
for path in source_paths:
    data = json.loads(path.read_text())
    ids = [row["candidate"]["candidate_id"] for row in data["rows"]]
    assert data["status"] == "PASS", path
    assert ids == expected, (path, ids)
    for row in data["rows"]:
        cls = row["classification"]
        assert row["status"] == "PASS", (path, row["candidate"]["candidate_id"])
        assert not cls["hard_vetoes"], (path, row["candidate"]["candidate_id"])
        assert cls["paired_comparability_pass"] is True
        assert cls["warm_time_screen_pass"] is True
        assert cls["gpu_tf32_provenance_complete"] is True
        assert cls["low_rank_provenance_complete"] is True
        for key in ("row_json", "row_markdown", "row_log"):
            assert Path(row[key]).exists(), (path, row["candidate"]["candidate_id"], key)
print("minimal-rank-consolidation-source-artifact-check-pass")
PY
```

## Forbidden Claims And Actions

- Do not use NumPy as BayesFilter-owned algorithmic implementation.
- Do not run a GPU benchmark in this consolidation phase.
- Do not rank candidates statistically from descriptive warm timing, wall time,
  or deltas.
- Do not claim speedup, posterior correctness, HMC readiness, dense Sinkhorn
  equivalence, public API/default readiness, scientific superiority, or
  production readiness.
- Do not claim the deferred rank-32/64/128 candidates are inferior or invalid.
- Do not revive `r64_eps0p125_alpha1em08_it120` without a new repair/tuning
  subplan.

## Exact Next-Phase Handoff Conditions

- If the artifact checks pass, write the consolidation result and draft a
  larger-`N` validation subplan for the minimal-rank survivor tier:
  `r16_eps0p25_alpha1em08_it120` and
  `r16_eps0p125_alpha1em08_it120`.
- If artifact checks fail, write a blocker result and draft a focused artifact
  repair or rerun subplan.
- If review finds the consolidation criterion unsafe, patch the subplan and
  rerun focused checks before execution.
- If the next subplan cannot preserve nonclaim boundaries, stop for human
  direction.

## Stop Conditions

- Any source aggregate JSON is missing, corrupt, or not `PASS`.
- The source artifacts do not contain the exact five expected candidates.
- Any candidate row has failed status, nonempty hard vetoes, failed paired
  comparability, failed warm screen, missing GPU/TF32 provenance, missing
  low-rank provenance, or missing row artifacts.
- The result would require ranking by descriptive timing, deltas, or residuals.
- The result would require claiming that deferred viable candidates are worse,
  invalid, or scientifically rejected.
- The next subplan cannot be drafted without crossing a forbidden claim
  boundary.

## End-Of-Subplan Duties

1. Run the required local artifact checks.
2. Write the minimal-rank consolidation result or blocker result.
3. Draft or refresh the next larger-`N` validation subplan.
4. Review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.

## Subplan Self-Review

- Consistency: carries forward the five candidates from the N1024
  seed-replication result and preserves the excluded candidate boundary.
- Correctness: uses rank as a resource-envelope parameter only after hard-veto
  survival.
- Feasibility: document-only phase with small local JSON checks.
- Artifact coverage: source aggregate artifacts, row artifacts, close record,
  and next subplan are specified.
- Boundary safety: avoids statistical ranking, speedup, correctness,
  default-readiness, scientific-validity claims, and descriptive timing rank.
