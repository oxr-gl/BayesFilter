# BayesFilter Plan: Fixed-Mass HMC Tuning-Budget Ladder

Date: 2026-06-19

Status: `REVISED_AFTER_IMPLEMENTATION_REVIEW`

## Research Intent Ledger

| Field | Entry |
| --- | --- |
| Main question | Can BayesFilter provide a reusable, client-agnostic fixed-mass HMC budget ladder that retunes step size with increasing dual-averaging budgets, screens the fixed kernel, and stops under a predeclared pass/repair/veto contract? |
| Mechanism under test | New BayesFilter-owned TensorFlow/TFP orchestration around `PrecomputedMassArtifact`, `LatentAffineBatchValueScoreAdapter`, `HMCTuningPolicy.fixed_mass_dual_averaging`, and `run_full_chain_tfp_hmc`; clients supply the position-coordinate adapter, frozen mass artifact, latent initial-state factory, optional diagnostic-role callback, and artifact labels. |
| Expected failure mode | Short stochastic screens may produce near-boundary acceptance misses; the ladder must distinguish acceptance-only repair triggers from true hard vetoes such as nonfinite values, missing final tuned step, log-accept cliffs, target errors, or client callback hard/continuation vetoes. |
| Promotion criterion | BayesFilter exports an additive, tested generic API that can run a finite budget schedule, record every round/candidate with mass provenance, select a final config under a deterministic rule, and preserve nonclaims that tuning screens are not posterior validation. |
| Promotion veto | NumPy-only algorithmic implementation, hidden client-specific MacroFinance assumptions, unbounded retry loops, missing frozen-mass artifact provenance, acceptance-only overfitting without heldout/fresh-screen discipline, missing diagnostic-role separation, or changing mass/target/L without explicit policy. |
| Continuation veto | Existing BayesFilter HMC APIs cannot support dynamic retuning and fixed-kernel screening without unsafe rewrites, or tests reveal the controller cannot preserve deterministic artifact hashes and fail-closed semantics. |
| Repair trigger | If implementation review finds API ambiguity, evidence-role confusion, unfair tune/screen mismatch, or public-export instability, revise the API before MacroFinance wiring. |
| Explanatory diagnostics | Per-budget tuned step, fixed-kernel screen acceptance, acceptance by chain, finite/log-accept diagnostics, target-status telemetry when enabled, optional client callback diagnostics, step-ratio stability, selected-vs-rejected rows, mass artifact signature, runner metadata, elapsed time. |
| Must not conclude | No posterior convergence, no sampler superiority, no default sampler readiness, no empirical/scientific validity, no GPU/XLA readiness, and no proof that a selected budget is universally sufficient. |

## Skeptical Plan Audit

| Risk | Audit Result |
| --- | --- |
| Wrong baseline | Pass if tests compare against simple deterministic fake runners and, in MacroFinance integration, against the current Phase 4/5T handoff behavior. |
| Proxy metric misuse | The API must label acceptance as tuning-screen evidence only. Acceptance can pass, repair, or hard-veto under policy, but cannot claim posterior convergence. |
| Missing stop conditions | The config must require a finite `budget_schedule`; stop on pass, callback or runtime hard veto, callback continuation veto, budget exhausted, invalid config, missing acceptance, missing final tuned step, nonfinite diagnostics, runner error, or acceptance outside repair band. |
| Unfair comparisons | Tune and screen initial-state policies must be explicit and comparable; clients may use distinct seeds but not hidden state-policy changes. The frozen mass artifact and fixed `num_leapfrog_steps` remain unchanged inside one ladder call. |
| Hidden assumptions | The API must not mention MacroFinance, MIDAS, SVD, Phase 4, or Phase 5T. Domain-specific checks enter only through a diagnostic-role callback payload. |
| Environment mismatch | BayesFilter implementation is CPU/GPU agnostic TFP orchestration; tests use small CPU-safe fixtures and do not claim GPU/XLA readiness. |
| Artifact answers question | The result must contain enough data to reconstruct budget rounds, selected config hash, failure role, frozen mass signature, and nonclaims. |
| Public API stability | Exports must be additive in `bayesfilter.inference` and top-level `bayesfilter`; no existing public name or payload schema may be broken. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Can BayesFilter own the adaptive fixed-mass tuning-budget ladder currently being hand-coded in MacroFinance? |
| Exact comparator | Existing BayesFilter `GenericHMCTuningConfig`/`GenericHMCTuningResult` schema, `PrecomputedMassArtifact` provenance, and lower-level HMC runtime APIs. The new tool should complement, not break, existing generic tuning artifacts. |
| Primary pass/fail criterion | Focused BayesFilter tests pass and the new public API can run a fake/deterministic ladder and a tiny TFP Gaussian fixture with fail-closed artifacts. |
| Veto diagnostics | Unbounded loops, NumPy algorithmic HMC, missing finite budget validation, hidden local-client imports, missing frozen-mass validation, no diagnostic-role separation, non-deterministic selection hashes, breaking public exports, or tests requiring MacroFinance. |
| Explanatory only | Runtime, exact acceptance values from tiny stochastic fixtures, step-ratio stability unless explicitly configured as a hard check, and descriptive differences between budgets. |
| Will not conclude | The tool does not prove convergence or recommend default budgets; client projects still need downstream validation. |
| Artifact | Plan, implementation, tests, Claude review notes, and MacroFinance integration result notes. |

## Proposed BayesFilter API

Add a new module:

```text
bayesfilter/inference/hmc_budget_ladder.py
```

Export from `bayesfilter.inference` and top-level `bayesfilter`:

```python
FixedMassHMCTuningBudgetLadderConfig
FixedMassHMCTuningBudgetRound
FixedMassHMCTuningBudgetLadderResult
FixedMassHMCTuningBudgetCallbackResult
run_fixed_mass_hmc_tuning_budget_ladder
```

### Config Fields

Required or strongly recommended:

- `budget_schedule`: finite positive integer tuple, e.g. `(384, 768, 1536, 3072, 6144)`.
- `target_accept_prob`: finite in `(0, 1)`, default `0.70`.
- `acceptance_band`: closed pass band, default `(0.65, 0.75)`.
- `repair_band`: wider closed band for acceptance-only repair, default proposed `(0.55, 0.85)`.
- `initial_step_size`: positive finite scalar for the first budget.
- `num_leapfrog_steps`: fixed positive integer for single-L use.
- `tune_num_results`, `screen_num_results`, `screen_num_burnin_steps`.
- `tune_seed_base`, `screen_seed_base`.
- `chain_execution_mode`, `use_xla`, `target_scope`.
- `tuning_trace_policy`: must be `standard` because final dual-averaged step extraction requires step-size trace.
- `screen_trace_policy`: may be `standard` or a validated reduced policy, but acceptance and log-accept diagnostics must be available for classification.
- `target_status_trace_policy`: optional BayesFilter telemetry hook; if set to `per_chain_step`, the adapter must satisfy the existing target-status telemetry contract and its diagnostics are recorded as BayesFilter-owned diagnostics.
- `step_stability_rtol`: optional convergence diagnostic, not a pass criterion unless `step_stability_is_hard_veto=True`.

Call-time dependencies:

- `adapter`: BayesFilter posterior/value-score adapter in position coordinates.
- `mass_artifact`: `PrecomputedMassArtifact` or reviewed equivalent BayesFilter frozen-mass artifact. The ladder validates it against the position-coordinate adapter, builds the BayesFilter-owned latent fixed-mass adapter internally, and records deterministic position-adapter, latent-HMC-adapter, and mass signatures.
- `initial_state_factory(seed, role, round_index, budget, step_size) -> tensor-like` in latent fixed-mass coordinates.
- Optional `screen_callback(round_payload, samples, diagnostics) -> FixedMassHMCTuningBudgetCallbackResult | Mapping[str, Any]`.

### Callback Role Schema

The callback is for client/domain diagnostics that BayesFilter cannot know, but
it must not collapse evidence roles into a plain boolean. Returned payloads must
include role-separated fields:

- `hard_vetoes`: tuple/list of strings that stop fail-closed.
- `continuation_vetoes`: tuple/list of strings that stop because the ladder artifact is invalid or cannot answer the question.
- `promotion_vetoes`: tuple/list of strings that block selection for the current round.
- `repair_triggers`: tuple/list of strings that allow the next budget when the run is otherwise valid.
- `diagnostics`: JSON-serializable explanatory payload.

Callback exceptions are recorded as `hard_vetoes=("callback_error",)`. If both
a repair trigger and hard/continuation veto are present, the hard/continuation
role wins. The ladder never upgrades a callback `promotion_veto` into a
continuation veto unless the callback explicitly returns a continuation veto.

### Runtime Semantics

For each budget round:

1. Validate `mass_artifact` against the position-coordinate `adapter`; build a BayesFilter-owned latent fixed-mass adapter from `mass_artifact.build_latent_transform()` and record target dimension, position-adapter signature, latent-HMC-adapter signature, and mass signature.
2. Build a fixed-mass dual-averaging policy with `num_adaptation_steps=budget`.
3. Run a tune chain with `num_burnin_steps=budget` or an explicit tune burn-in schedule satisfying `adaptation_steps <= burnin_steps`.
4. Extract final tuned step from `standard` tuning trace/diagnostics.
5. Hard-veto the round if the tune run errors, acceptance is missing/nonfinite, final step is missing/nonfinite/nonpositive, log-accept diagnostics are nonfinite, target-status telemetry hard-vetoes when enabled, or optional hard stability checks fail.
6. Run a fresh fixed-kernel screen at the tuned step with no adaptation on the latent fixed-mass adapter.
7. Hard-veto the screen if acceptance is missing/nonfinite, samples or log-accept diagnostics are nonfinite, target-status telemetry hard-vetoes when enabled, the callback returns hard vetoes, or acceptance is outside `repair_band`.
8. Classify the round:
   - `passed`: finite diagnostics, no hard/continuation/promotion veto, acceptance inside pass band.
   - `acceptance_repair`: finite diagnostics, no hard/continuation veto, acceptance outside pass band but inside repair band, and no callback promotion veto other than declared repair triggers.
   - `promotion_veto_repair`: finite diagnostics and callback promotion veto or repair trigger permits the next budget. A repair trigger alone blocks promotion even when acceptance is inside the pass band.
   - `continuation_veto`: callback continuation veto stops because the ladder artifact cannot answer the question, without being collapsed into a hard-veto label.
   - `hard_veto`: runtime hard veto, callback hard veto, or acceptance outside repair band.
   - `budget_exhausted`: all budget rounds end in repair-compatible states without pass.
9. If `passed`, return selected config; if repair-compatible, continue to next budget; if hard or continuation veto, stop fail-closed.

The selected payload should include:

- final step size;
- selected budget;
- target accept;
- pass/repair bands;
- fixed `num_leapfrog_steps`;
- HMC config payloads;
- adapter signature and target scope when available;
- latent HMC adapter signature;
- frozen mass artifact signature and validation payload;
- target-status policy and diagnostics availability;
- deterministic selected-config hash;
- all nonclaims.

## Boundary With Existing Generic Tuning

This ladder is a lower-level per-fixed-`L` primitive. It owns budget escalation
for one fixed mass artifact, one target, one initial-state policy, and one fixed
`num_leapfrog_steps`. It does not own outer `L`-grid selection in this phase.
Client projects may call the ladder once per `L` and apply their documented
selection/tie policy outside this API. A later BayesFilter plan may add an
outer grid artifact, but this plan keeps the implementation scoped to the
budget-ladder mechanism.

## Implementation Steps

1. Add `hmc_budget_ladder.py` with dataclasses, validation, callback coercion, payload/hash helpers, and the runtime loop.
2. Reuse `PrecomputedMassArtifact`, `LatentAffineBatchValueScoreAdapter`, `FullChainHMCConfig`, `HMCTuningPolicy.fixed_mass_dual_averaging`, and `run_full_chain_tfp_hmc` initially. Use reusable runner only for fixed-kernel screens where the static contract is stable; do not prematurely complicate tuning-run reuse because adaptation budget changes per round.
3. Add helper functions to extract diagnostics from `FullChainHMCRunResult` for reporting/serialization only. NumPy conversions are allowed only after TensorFlow/TFP execution to summarize artifacts; they are not an algorithmic HMC path.
4. Preserve existing target-status telemetry semantics by passing through `target_status_trace_policy` and recording its diagnostics when enabled.
5. Add focused tests:
   - config validation rejects empty/infinite/unbounded budgets and reduced tuning trace;
   - mass artifact is required, validated, and fingerprinted;
   - acceptance-only repair advances through budgets;
   - pass selects a config and stable hash;
   - hard veto stops immediately;
   - callback role separation is preserved and callback hard/continuation vetoes stop;
   - budget exhaustion is distinct from hard veto;
   - public exports are additive;
   - tiny Gaussian TFP fixture runs at least one real HMC ladder round.
6. Export the new API in `bayesfilter/inference/__init__.py` and top-level `bayesfilter/__init__.py`.
7. Write result note after implementation.
8. Run Claude implementation review and address findings.
9. In MacroFinance, replace the custom Phase 4/5T budget loop with the BayesFilter ladder as the active tuning authority, preserving MacroFinance-specific target/mass/context reconstruction, outer L-grid selection, and MIDAS boundary callback outside BayesFilter.

## MacroFinance Wiring Plan

After BayesFilter implementation passes review:

- Add a MacroFinance Phase 4/5 replacement runner that calls
  `run_fixed_mass_hmc_tuning_budget_ladder` once per candidate L through a thin
  client-side L-grid loop.
- Keep MacroFinance-specific pieces outside BayesFilter:
  graph-status SVD target wrapper, Phase 3 frozen mass loading, selected-L tie
  rule if multiple L ladders pass, MIDAS boundary callback, result-note paths.
- Replace current one-shot `384/384` Phase 4 and Phase 5T step-repair logic
  with a single BayesFilter-owned per-L budget ladder artifact plus
  MacroFinance-owned L-grid summary.
- Focused tests should prove MacroFinance imports the BayesFilter ladder and
  does not implement its own adaptive tuning-budget loop.

## Claude Review Protocol

Run up to five read-only Claude review rounds over this plan. Stop early only
when Claude returns `VERDICT: AGREE` or no material findings. Each revision
must address material findings or explicitly document why a finding is not
adopted.

Round 1 response:

- Adopted `PrecomputedMassArtifact`/frozen-mass provenance as an explicit call-time dependency and result field.
- Replaced boolean callback contract with role-separated callback schema.
- Required standard tuning trace for final step extraction.
- Added optional target-status telemetry handling.
- Enumerated missing final-step, missing acceptance, nonfinite log-accept, and stability stop conditions.
- Declared the ladder as a lower-level per-fixed-`L` primitive.
- Clarified NumPy use as serialization/reporting only.
- Added additive public-export stability to the evidence contract and tests.

Implementation review repair:

- Claude found that continuation vetoes were being collapsed into hard vetoes,
  pure repair triggers could not force a next-budget retry, and the frozen mass
  artifact was provenance-only unless callers manually supplied a latent
  wrapper.
- The implementation was revised so continuation vetoes have a distinct
  terminal status, repair triggers independently block promotion, optional step
  stability is recorded and can hard-veto when configured, and BayesFilter
  builds the latent fixed-mass adapter internally from the position adapter and
  `PrecomputedMassArtifact`.

After implementation, run a read-only Claude implementation review over:

- new BayesFilter module;
- exports;
- tests;
- MacroFinance wiring runner/tests;
- result notes.

Do not commit or push unless explicitly requested.
