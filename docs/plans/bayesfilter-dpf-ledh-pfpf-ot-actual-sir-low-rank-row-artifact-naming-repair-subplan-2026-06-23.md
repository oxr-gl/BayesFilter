# Actual-SIR Low-Rank Row Artifact Naming Repair Subplan

Date: 2026-06-23

Status: `DRAFT_READY_FOR_READ_ONLY_REVIEW_BEFORE_EXECUTION`

## Phase Objective

Repair the actual-SIR low-rank grid orchestrator so row JSON, Markdown, and log
artifact filenames are deterministically bounded below common filesystem
component limits while preserving full row identity and request provenance in
the aggregate and row JSON.

## Entry Conditions Inherited From Previous Phase

- The N2048 minimal-rank validation subplan converged after read-only Claude
  review.
- The required N2048 pre-execution checks passed.
- The first N2048 execution attempt was blocked by overlong row artifact
  filenames before a valid aggregate could be produced.
- The two candidate ids remain exactly:
  - `r16_eps0p25_alpha1em08_it120`
  - `r16_eps0p125_alpha1em08_it120`
- The blocker is classified as harness/artifact failure, not candidate failure.

## Required Artifacts

- This repair subplan.
- Blocker result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n2048-minimal-rank-validation-blocker-result-2026-06-23.md`
- Patched grid orchestrator:
  `docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py`
- Focused test coverage in:
  `tests/test_actual_sir_low_rank_tuning_grid.py`
- Repair result or close note under `docs/plans` if the repair cannot directly
  proceed into the N2048 rerun.
- Refreshed N2048 aggregate after rerun:
  `docs/benchmarks/actual-sir-low-rank-n2048-minimal-rank-validation-2026-06-23.json`
  and
  `docs/benchmarks/actual-sir-low-rank-n2048-minimal-rank-validation-2026-06-23.md`

## Required Checks, Tests, And Reviews

- Skeptical plan audit before patching.
- Claude read-only review of this subplan for boundary safety and artifact
  adequacy if practical; Claude is not an execution authority.
- Local syntax check:
  `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_tuning_grid.py`
- Focused grid tests:
  `python -m pytest tests/test_actual_sir_low_rank_tuning_grid.py -q`
- Exact N2048 dry-run after patch, verifying:
  - exact candidate ids;
  - two rows;
  - each row JSON/Markdown/log filename component is no longer than `255`
    characters;
  - row JSON/Markdown/log paths are distinct across candidates and cannot
    overwrite another row in the same aggregate;
  - each row command writes to the bounded paths;
  - request signatures still preserve full configuration.
- Trusted GPU precheck before rerunning N2048.

## Evidence Contract

- Question: can the harness artifact blocker be removed without changing
  algorithmic execution, candidate selection, numerical thresholds, route
  semantics, timing-source policy, GPU/XLA policy, or scientific interpretation
  boundaries?
- Baseline/comparator: the pre-repair N2048 attempt failed only because the
  row artifact filename components were too long.
- Primary pass criterion: the patched runner emits deterministic bounded row
  artifact names and passes the focused tests plus exact N2048 dry-run.
- Diagnostics that can veto: candidate-id mismatch, changed command semantics,
  missing full request signature, non-deterministic row paths, row artifact path
  collision/overwrite risk, filename component still above `255` characters,
  failed focused tests, or any use of NumPy or a non-default backend in
  BayesFilter-owned algorithmic paths.
- Explanatory diagnostics only: exact digest string, exact row filename length,
  row path uniqueness count, and whether short historical rows keep their
  previous verbose names.
- What will not be concluded: candidate viability, speedup, posterior
  correctness, HMC readiness, dense Sinkhorn equivalence, public API/default
  readiness, statistical ranking, or broad scientific validity.
- Artifact preserving result: patched code, focused test output, exact dry-run
  JSON/Markdown, and the subsequent N2048 aggregate if rerun succeeds.

## Skeptical Plan Audit

- Wrong baseline check: this repair compares against the observed artifact
  failure only, not against numerical candidate performance.
- Proxy metric check: filename length is a harness-validity criterion, not a
  scientific or performance criterion.
- Stop condition check: if the patch changes command semantics, candidate
  enumeration, thresholds, timing-source policy, GPU/XLA flags, or row request
  signatures, stop and revise.
- Fairness check: both N2048 candidates must use the same naming rule and keep
  the same command arguments as the reviewed subplan.
- Hidden assumption check: bounded names are acceptable only because full row
  identity remains in JSON metadata and aggregate request signatures.
- Environment mismatch check: GPU availability remains a separate trusted
  precheck before rerun; CPU-only checks do not validate the GPU result.
- Artifact sufficiency check: aggregate rows must preserve row JSON, Markdown,
  and log paths, and the row JSON must still preserve the full run metadata.

Audit result: passes as a narrow harness repair because it changes only artifact
filename construction and test coverage, while preserving the reviewed
candidate set, command semantics, and evidence boundaries.

## Forbidden Claims And Actions

- Do not modify filtering, transport, TensorFlow, TensorFlow Probability, or
  numerical algorithm implementation paths in this phase.
- Do not use NumPy as BayesFilter-owned algorithmic implementation.
- Do not change candidate ids, seeds, thresholds, timing sources, TF32 mode,
  GPU visibility, XLA flags, or route semantics.
- Do not interpret the failed pre-repair run as candidate rejection.
- Do not claim speedup, ranking, posterior correctness, HMC readiness, dense
  Sinkhorn equivalence, public API/default readiness, or scientific validity.
- Do not revive excluded/deferred candidates.

## Exact Next-Phase Handoff Conditions

- If checks and exact dry-run pass, rerun the reviewed N2048 minimal-rank
  validation command under trusted GPU context.
- If checks fail because the bounded naming repair is incomplete, patch the
  repair and rerun focused checks before any GPU execution.
- If the repair would require command-semantic or algorithmic changes, stop and
  write a blocker result for human direction.
- If the rerun reaches a valid aggregate, resume the N2048 validation result
  interpretation under the existing N2048 evidence contract.

## Stop Conditions

- Filename components remain longer than `255` characters in the exact N2048
  dry-run.
- Any two candidate rows share the same JSON, Markdown, or log path in the
  exact N2048 dry-run.
- Row command arguments differ from the reviewed N2048 subplan except for the
  bounded artifact output paths.
- Request signature or candidate metadata no longer preserve full row identity.
- Focused tests or syntax checks fail.
- Trusted GPU precheck fails before rerun.
- Any interpretation would cross the forbidden claim boundaries.

## End-Of-Subplan Duties

1. Run the required local checks.
2. Write a repair result or incorporate the repair outcome into the N2048 close
   record.
3. Draft or refresh the next subplan before any further phase beyond the N2048
   rerun.
4. Review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.

## Subplan Self-Review

- Consistency: addresses the observed N2048 blocker without changing the
  reviewed candidate set or evidence contract.
- Correctness: preserves full request provenance in JSON while bounding only
  filesystem component names.
- Feasibility: requires a small runner patch and focused tests before rerun.
- Artifact coverage: includes blocker record, patched runner, focused test,
  dry-run, and rerun aggregate.
- Boundary safety: avoids algorithmic changes and all scientific/product
  readiness claims.
