# LEDH Highdim Row Score Admission Master Program

Date: 2026-07-05

Status: `DRAFT_PENDING_LOCAL_CHECKS_AND_REVIEW`

## Program Objective

Repair the remaining LEDH high-dimensional leaderboard score rows in the only
scientifically acceptable order:

1. freeze the exact row target;
2. freeze the free parameter vector for that row;
3. prove that the current forward LEDH code computes that same finite scalar,
   or replace it with code that does;
4. implement the no-tape total derivative of that exact executed scalar;
5. test tiny correctness, then `N=10000` correctness and memory;
6. promote the row into the leaderboard only after those gates pass.

This program exists because most remaining LEDH score rows are blocked before
the derivative stage. Their forward scalar is still unproved, missing, or wrong
relative to the requested leaderboard row.

## Inherited State

Current admitted LEDH score-route test evidence
(not the same thing as admitted full leaderboard-row score evidence):

- `benchmark_lgssm_exact_oracle_m3_T50`: admitted compact no-autodiff same-scalar
  score with `N=10000` correctness and memory test.
- `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale`: admitted scoped
  diagnostic no-autodiff score with `N=10000` correctness and memory test.

Current blocked or not-yet-admitted LEDH scoreboard rows:

- `zhao_cui_spatial_sir_austria_j9_T20`: value-only; no admitted full-row score.
- `zhao_cui_sv_actual_nongaussian_T1000`: no reviewed same-target LEDH value
  adapter; score blocked.
- `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000`: no KSC LEDH adapter;
  score blocked.
- `zhao_cui_predator_prey_T20`: no reviewed current GPU/XLA same-target adapter;
  score blocked.
- `zhao_cui_generalized_sv_synthetic_from_estimated_values`: no reviewed
  same-target adapter; score blocked.

Relevant anchor artifacts:

- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase1-row-admission-ledger-2026-07-03.json`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase6-closeout-result-2026-07-03.md`
- `docs/plans/bayesfilter-highdim-actual-sv-single-target-corrected-derivation-note-2026-06-29.md`
- `docs/plans/ledh-score-memory-test-suite-plan-2026-07-05.md`
- `docs/plans/ledh-score-memory-test-suite-result-2026-07-05.md`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | In what order should the remaining LEDH highdim score blockers be repaired so that every promoted row has a correct same-target forward scalar and a no-tape total derivative? |
| Baseline/comparator | The July 3 LEDH row-admission ledger, the July 3 LEDH closeout result, the actual-SV corrected derivation note, and the July 5 LEDH `N=10000` score-memory suite. |
| Primary pass criterion | Every phase has a bounded subplan, explicit result artifact target, explicit stop condition, exact next-phase handoff condition, and the execution sequence respects model dependencies. |
| Veto diagnostics | Any phase that tries to implement a score before the forward scalar is admitted; any phase that treats autodiff score code as admitted leaderboard evidence; any phase that treats a scoped diagnostic row as a full leaderboard row; any phase that changes the row target after seeing results. |
| Explanatory diagnostics | Legacy callback traces, diagnostic lower-rung fixtures, runtime notes, memory notes, and scoped component score evidence. |
| Not concluded at launch | No new row is admitted at launch. No scientific correctness claim is made for blocked rows. No leaderboard rerun is justified yet. No HMC readiness or posterior claim is made. |
| Artifacts | This master program, Phase 0-6 subplans, the visible runbook, visible execution ledger, stop handoff, Claude/Codex review bundle, phase result notes, and later model-specific implementation/test artifacts. |

## Dependency Graph

The repair dependencies are:

1. **Full-row fixed spatial SIR** first.
   - Reason: a value route already exists, and the scoped parameterized SIR
     manual score already exists. The missing step is to promote from scoped
     diagnostic to the real full leaderboard row.
2. **Actual SV** second.
   - Reason: the target math is partly repaired already, and the transformed-SV
     target discipline must be fixed before KSC.
3. **KSC SV** third.
   - Reason: KSC should reuse the transformed-SV same-target adapter pattern
     from actual SV instead of inventing an unrelated route.
4. **Predator-prey** fourth.
   - Reason: it needs a current same-target GPU/XLA adapter, but it does not
     depend on transformed-SV target machinery.
5. **Generalized SV** fifth.
   - Reason: it has the highest risk of wrong-target substitution and should be
     tackled after the simpler target families are settled.
6. **Leaderboard reassembly** last.
   - Reason: row promotion is only meaningful after the row-specific value and
     score gates pass.

## Skeptical Plan Audit

| Risk checked | Control |
| --- | --- |
| Wrong baseline | The program uses the July 3 row ledger as the blocker baseline and the July 5 `N=10000` suite as the current admitted-score baseline. |
| Proxy metric promoted | Memory success, compile success, or finite outputs are not row-admission proof. Each row still needs same-target value evidence and no-tape total-derivative evidence. |
| Missing stop conditions | Every phase below has explicit stop conditions and exact next-phase handoff conditions. |
| Hidden assumption | The scoped parameterized SIR score is not treated as the full fixed-SIR row score. Legacy callbacks are not treated as current same-target GPU/XLA evidence. |
| Unfair comparison | Leaderboard rerun is isolated to the final phase. Runtime cross-ranking against frozen non-LEDH rows remains forbidden unless separately rerun. |
| Stale context | The program names the exact current admitted rows, blocked rows, and actual-SV target note. |
| Environment mismatch | GPU/CUDA/XLA and Claude CLI review commands must run in trusted execution. CPU-only checks must explicitly hide GPU before import. |
| Useless artifacts | Each phase must write a result note that answers one narrow blocker question directly. |

Audit status: passed for launch planning only. Execution begins with Phase 0.

## Program Order

| Phase | Name | Why this phase exists | Subplan | Required result artifact |
| --- | --- | --- | --- | --- |
| 0 | Launch and blocker freeze | Freeze the exact sequence, boundaries, and row meanings before code changes. | `docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase0-launch-blocker-freeze-subplan-2026-07-05.md` | `docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase0-launch-blocker-freeze-result-2026-07-05.md` |
| 1 | Fixed spatial SIR full-row score promotion | Convert the current scoped/manual SIR evidence into a real full-row same-target score plan. | `docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase1-fixed-spatial-sir-full-row-subplan-2026-07-05.md` | `docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase1-fixed-spatial-sir-full-row-result-2026-07-05.md` |
| 2 | Actual SV same-target adapter and score | Repair the actual-SV forward scalar first, then its no-tape total derivative. | `docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase2-actual-sv-same-target-subplan-2026-07-05.md` | `docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase2-actual-sv-same-target-result-2026-07-05.md` |
| 3 | KSC SV same-target adapter and score | Build the KSC-specific LEDH route on top of the transformed-SV target discipline. | `docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase3-ksc-sv-same-target-subplan-2026-07-05.md` | `docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase3-ksc-sv-same-target-result-2026-07-05.md` |
| 4 | Predator-prey same-target adapter and score | Admit a current GPU/XLA same-target predator-prey LEDH row and its no-tape score. | `docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase4-predator-prey-same-target-subplan-2026-07-05.md` | `docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase4-predator-prey-same-target-result-2026-07-05.md` |
| 5 | Generalized SV same-target adapter and score | Admit the hardest remaining row only after wrong-target substitution is excluded. | `docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase5-generalized-sv-same-target-subplan-2026-07-05.md` | `docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase5-generalized-sv-same-target-result-2026-07-05.md` |
| 6 | Leaderboard reassembly and row test expansion | Rerun the LEDH-inclusive leaderboard only with rows that passed the earlier gates. | `docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase6-leaderboard-reassembly-subplan-2026-07-05.md` | `docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase6-leaderboard-reassembly-result-2026-07-05.md` |

## Phase Invariants

These rules hold in every phase:

- The forward scalar must be named explicitly.
- The differentiated parameter vector must be named explicitly.
- If the code computes a different scalar than the stated row target, the phase
  must call it `wrong relative to the stated target`.
- No admitted leaderboard score may use `GradientTape`, `ForwardAccumulator`,
  or hidden autodiff.
- Tiny correctness checks are required before `N=10000` checks.
- `N=10000` memory success alone is not score evidence.
- A blocked row must remain blocked until its own phase passes.

## Review Protocol

Claude is a read-only reviewer only. If Claude review stalls or returns no
verdict:

1. run a tiny probe;
2. if the probe passes, narrow or rewrite the review prompt and retry;
3. if the probe fails in trusted execution, treat Claude as unavailable for the
   current gate and replace the review with a fresh Codex review packet;
4. do not treat silence as agreement.

Stop after five review rounds for the same blocker.

## Anticipated Approval/Execution Boundaries

Expected trusted commands during this program:

- bounded Claude review-gate commands;
- GPU/CUDA/XLA TensorFlow checks;
- `pytest` or benchmark commands that initialize GPU;
- long `N=10000` score-memory tests.

Human direction is still required before:

- changing leaderboard pass/fail criteria after seeing results;
- installing packages;
- destructive git actions;
- publishing claims beyond the reviewed artifacts;
- changing default policy beyond the explicitly scoped row admissions.
