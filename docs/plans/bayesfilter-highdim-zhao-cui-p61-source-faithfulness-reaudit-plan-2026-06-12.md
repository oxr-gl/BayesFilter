# P61 Plan: Zhao-Cui Source-Faithfulness Reaudit

metadata_date: 2026-06-12
status: PLAN_CREATED_FOR_EXECUTION

## Trigger

P60 exposed a source-faithfulness miss: the author squared SIRT route uses a
defensive term `tau` in the density, CDFs, potentials, and normalizer, while
the P59/P60 source-route helper used `tau = 0.0`.  This created a zero-mass
normalizer failure that the previous audit did not catch.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What source-code and paper-level discrepancies remain between the Zhao-Cui author SIR route and the BayesFilter P57/P59/P60 source-route implementation, excluding the intentional fixed-variant requirement? |
| Baseline/comparator | Author code under `third_party/audit/zhao_cui_tensor_ssm_p10/source`, especially `eg3_sir/mainscript.m`, `models/full_sol.m`, `models/computeL.m`, `models/ESS.m`, `deep-tensor.dev/src/SIRT.m`, `@TTSIRT/*.m`, `Options/TTOption.m`, and the local Zhao-Cui paper/source ledgers. |
| Primary criterion | A discrepancy ledger under `docs/plans` that cites author anchors, maps each behavior to BayesFilter implementation anchors, classifies each item, and separates intentional fixed-variant differences from unfaithful mismatches. |
| Veto diagnostics | Audit lacks author line anchors, treats fixed-variant necessity as a mismatch, treats agent-created behavior as source-faithful without source evidence, omits the known `tau`/defensive-density issue, omits independent Claude Opus max-effort review, or fails to compare Claude and Codex notes. |
| Nonclaims | No implementation repair, no P60-2 repair, no d=18 correctness claim, no rank convergence claim, no d=50/d=100 launch, no HMC production readiness claim. |

## Scope

The audit must cover at least:

- SIR row dimensions, horizon, data-generation seeds, particle counts, and
  selected solver route.
- Squared SIRT density semantics: `h^2 + tau`, normalizer `z`, CDFs,
  potentials, proposal density, and marginal density.
- Basis and domain mapping: `Lagrangep(4,8)`, `AlgebraicMapping(1)`, reference
  and physical-coordinate change of variables.
- Rank/training semantics: `TTOption`, random/adaptive construction, maximum
  rank, initialization rank, kick rank, ALS counts, and fixed-variant
  exception boundaries.
- Affine recentering/scaling: `computeL`, expansion factor, sample resampling,
  debug/init split, and determinant handling.
- Sequential route: previous SIRT marginalization, prior term for `t > 1`,
  retained sample generation, proposal correction, ESS, and log-marginal
  update.
- BayesFilter fixed-branch constraints: fixed rank, fixed samples/seeds, no
  adaptive rank mutation inside HMC likelihood calls, TensorFlow/TFP backend.

## Artifacts

- Codex audit:
  `docs/plans/bayesfilter-highdim-zhao-cui-p61-codex-source-faithfulness-reaudit-2026-06-12.md`
- Claude audit:
  `docs/plans/bayesfilter-highdim-zhao-cui-p61-claude-source-faithfulness-reaudit-2026-06-12.md`
- Merged discrepancy ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p61-merged-source-faithfulness-reaudit-ledger-2026-06-12.md`

## Execution Steps

1. Re-read author source anchors and current BayesFilter implementation anchors.
2. Write Codex discrepancy ledger with classifications:
   `MATCH`, `FIXED_VARIANT_ACCEPTED`, `MISMATCH`, `MISSING`, `AGENT_INVENTED`,
   or `NEEDS_SOURCE_CHECK`.
3. Run Claude Opus max-effort in read-only mode with the same task.
4. Compare Codex and Claude notes.
5. Write the merged ledger with agreed gaps, additional Claude-only findings,
   Codex-only findings, and proposed repair ordering.

## Stop Rules

Stop and report rather than repair if:

- author source anchors are unavailable;
- Claude cannot complete after probe-and-shortened-prompt retry;
- the audit finds a discrepancy that invalidates the P60 comparator contract;
- a proposed fix would require choosing between source faithfulness and the
  fixed-HMC branch requirement without user approval.

## Skeptical Plan Audit

Passes with caveat: this is a bounded audit and not a repair.  The plan
explicitly blocks the common failure modes that caused the P60 miss: missing
author anchors, treating fixed-variant necessity as noncompliance, and
reviewing only governance rather than implementation semantics.

