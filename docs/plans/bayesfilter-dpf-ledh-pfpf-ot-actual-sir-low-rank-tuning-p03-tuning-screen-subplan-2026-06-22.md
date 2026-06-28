# P03 Actual-SIR Tuning Screen Subplan

Status: `REFRESHED_AFTER_P02`

## Phase Objective

Run bounded actual-SIR d18 tuning rows that can nominate one or more low-rank
parameter candidates for freezing, while preserving the separation between
tuning evidence and held-out support evidence. P03 is a tuning screen only; it
cannot promote a speedup or any scientific claim.

## Entry Conditions Inherited From Previous Phase

P02 passed with complete tiny actual-SIR artifacts. The tuning execution path
and artifact schema are known-good for execute-mode wrapper rows.

## Required Artifacts

- First-stage tuning aggregate:
  `docs/benchmarks/actual-sir-low-rank-tuning-p03-screen-stage-a-2026-06-22.json`
- First-stage tuning Markdown:
  `docs/benchmarks/actual-sir-low-rank-tuning-p03-screen-stage-a-2026-06-22.md`
- Optional second-stage aggregate, only if Stage A has at least one
  `freeze-nominated` candidate:
  `docs/benchmarks/actual-sir-low-rank-tuning-p03-screen-stage-b-2026-06-22.json`
- Optional second-stage Markdown, only if Stage A has at least one
  `freeze-nominated` candidate:
  `docs/benchmarks/actual-sir-low-rank-tuning-p03-screen-stage-b-2026-06-22.md`
- Row artifacts/logs as needed:
  `docs/benchmarks/actual-sir-low-rank-tuning-p03-screen-stage-*-2026-06-22*.json`
  and `docs/benchmarks/logs/actual-sir-low-rank-tuning-p03-screen-stage-*-2026-06-22*.log`
- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p03-tuning-screen-result-2026-06-22.md`
- P03 stop handoff, required if P03 does not satisfy P04 handoff conditions:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p03-stop-handoff-2026-06-22.md`
- Claude review ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-claude-review-ledger-2026-06-22.md`

## Required Checks/Tests/Reviews

- Stage A row: `B=1,T=20,N=256`, seed `81120`.
- Stage A grid: rank `16,32,64,128` where `rank <= N`; assignment epsilon
  `0.25,0.125,0.0625,0.03125,0.015625`; alpha fixed at `1e-8`; projection
  iterations fixed at `120`.
- Stage A exact command, subject to trusted GPU availability:

```bash
timeout 7200 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py \
  --mode execute \
  --num-particles 256 \
  --time-steps 20 \
  --batch-seeds 81120 \
  --low-rank-ranks 16,32,64,128 \
  --low-rank-assignment-epsilons 0.25,0.125,0.0625,0.03125,0.015625 \
  --low-rank-max-projection-iterations-list 120 \
  --warmups 1 \
  --repeats 2 \
  --device-scope visible \
  --cuda-visible-devices 1 \
  --device /GPU:0 \
  --expect-device-kind gpu \
  --tf32-mode enabled \
  --output docs/benchmarks/actual-sir-low-rank-tuning-p03-screen-stage-a-2026-06-22.json \
  --markdown-output docs/benchmarks/actual-sir-low-rank-tuning-p03-screen-stage-a-2026-06-22.md \
  --quiet
```

- Stage B row, only if Stage A has at least one `freeze-nominated` candidate:
  `B=1,T=20,N=256`, seed `81121`, same full Stage A grid. Stage B exists to
  prevent freezing from a single tuning seed when Stage A appears promising.
- Stage B exact command:

```bash
timeout 7200 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py \
  --mode execute \
  --num-particles 256 \
  --time-steps 20 \
  --batch-seeds 81121 \
  --low-rank-ranks 16,32,64,128 \
  --low-rank-assignment-epsilons 0.25,0.125,0.0625,0.03125,0.015625 \
  --low-rank-max-projection-iterations-list 120 \
  --warmups 1 \
  --repeats 2 \
  --device-scope visible \
  --cuda-visible-devices 1 \
  --device /GPU:0 \
  --expect-device-kind gpu \
  --tf32-mode enabled \
  --output docs/benchmarks/actual-sir-low-rank-tuning-p03-screen-stage-b-2026-06-22.json \
  --markdown-output docs/benchmarks/actual-sir-low-rank-tuning-p03-screen-stage-b-2026-06-22.md \
  --quiet
```

- Do not run Stage B if Stage A has no `freeze-nominated` candidate.
- Do not widen to `240` or `480` projection iterations inside P03 unless a
  written P03 repair amendment cites Stage A/B residual or iteration-cap
  evidence and passes focused review before execution.
- Classify each candidate using the wrapper labels: `hard-vetoed`,
  `freeze-nominated`, `comparable-but-slow`, `faster-but-incomparable`,
  `schema-valid-nonpromotional`, or `incomparable`.
- A candidate is freeze-eligible only if it is `freeze-nominated` on every P03
  tuning row it ran. That means no hard vetoes, paired log-likelihood and
  filtered-summary comparability pass, warm-time screen pass, complete
  low-rank provenance, and complete visible GPU/TF32 provenance.
- Freeze exactly one candidate if the fastest freeze-eligible candidate is the
  same as the first selected candidate.
- Select the first frozen candidate by this deterministic key: lowest P03
  aggregate log-likelihood mean absolute delta; then lower log-likelihood max
  absolute delta; then lower rank; then lower warm median; then lexicographic
  parameter tuple.
- Freeze exactly two candidates if the fastest freeze-eligible candidate differs
  from the first selected candidate. The fastest candidate is selected by this
  deterministic key: lower warm median; then lower P03 aggregate
  log-likelihood mean absolute delta; then lower log-likelihood max absolute
  delta; then lower rank; then lexicographic parameter tuple.
- If the fastest deterministic key selects the same candidate as the first key,
  freeze only that one candidate.
- Claude read-only review for tuning interpretation and the next produced
  artifact, either the P04 freeze plan or a stop handoff.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which exposed low-rank settings are viable enough on actual-SIR d18 tuning rows to freeze before held-out support? |
| Baseline/comparator | Existing compiled streaming actual-SIR route for paired tuning rows. |
| Primary pass criterion | At least one candidate is freeze-eligible under the predeclared rule above. Stage A alone can stop as no-freeze/repair-required, but Stage B is required before P04 if Stage A produces any freeze-nominated candidate. |
| Veto diagnostics | Nonfinite outputs, invalid factors, dense materialization, route-fired mismatch, actual-SIR semantics missing, paired comparability failure for all candidates after bounded repair, no warm-time screen pass for any otherwise comparable candidate, missing aggregate, or trusted GPU unavailable for GPU tuning. |
| Explanatory diagnostics | Runtime, memory, projection iterations, factor residuals, ESS, and warm-time ratios on tuning rows. |
| Not concluded | No promotion, held-out support, speedup claim, posterior correctness, HMC readiness, default readiness, or statistical ranking. |
| Artifact | P03 aggregate, row artifacts/logs, phase result, Claude review ledger, and P03 stop handoff if P03 does not advance to P04. |

## Forbidden Claims/Actions

- Do not promote from tuning rows.
- Do not rank viable stochastic candidates as statistically superior.
- Do not widen gates after seeing results.
- Do not continue to large-N from P03.
- Do not repair route internals without a separate reviewed route-repair plan.
- Do not freeze a `comparable-but-slow` candidate.
- Do not use Stage B as held-out support; it is still tuning evidence.

## Exact Next-Phase Handoff Conditions

Advance to P04 only if Stage A and Stage B, when required, record at least one
freeze-eligible candidate with exact parameters, deterministic selection basis,
and no unresolved hard-veto/schema issues. If Stage A has no
`freeze-nominated` candidate but artifacts are valid, write the P03 result and
stop as follows:

- `ROUTE_REPAIR_REQUIRED` if candidates are comparable but fail only the
  warm-time screen;
- `TUNING_REPAIR_REQUIRED` if failures are parameter-dependent comparability or
  factor-validity failures that a predeclared parameter repair can address;
- blocker result if all candidates hard-veto for the same implementation,
  schema, artifact, or environment reason.

## Stop Conditions

- Stop if all candidates hard-veto due to implementation, schema, or artifact
  invalidity.
- Stop if trusted GPU evidence is required but unavailable.
- Stop after five unresolved Claude review rounds for the same tuning blocker.

## End-Of-Subplan Duties

1. Run required local checks.
2. Write the P03 phase result.
3. Draft or refresh P04 with exact candidate parameters only if P03 satisfies
   the exact next-phase handoff conditions for P04. If P03 stops as
   `ROUTE_REPAIR_REQUIRED`, `TUNING_REPAIR_REQUIRED`, or blocker, write a stop
   handoff at
   `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p03-stop-handoff-2026-06-22.md`
   instead of drafting P04.
4. Review the next artifact actually produced, either P04 or the stop handoff,
   for consistency, correctness, feasibility, artifact coverage, and boundary
   safety. Record the review result in
   `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-claude-review-ledger-2026-06-22.md`.
