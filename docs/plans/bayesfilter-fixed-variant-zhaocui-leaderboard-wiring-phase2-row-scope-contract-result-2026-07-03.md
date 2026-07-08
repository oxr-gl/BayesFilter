# Phase 2 Result: Row Scope And Evidence Contract

Date: 2026-07-03

Status: `PASS_PHASE2_ROW_SCOPE_CONTRACT_REV1_CLAUDE_AGREE`

## Direct Verdict

```text
scoped_component_row_admitted
```

The admitted row is not the historical fixed/no-free-theta row. The admitted
row is:

```text
zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale
```

The declared scope is:

```text
local_complete_data_zhao_cui_sir_d18_component
```

The original row
`zhao_cui_spatial_sir_austria_j9_T20` remains fixed/no-free-theta source-parity
evidence and must not be silently mutated into a parameterized row.

Important row-id boundary:

- the row id encodes the free-theta parameterization, not the full target
  scope;
- the local-complete-data/component boundary must be carried by explicit
  metadata fields such as `target_scope`, `target_contract_status`,
  `score_derivative_provenance`, `reason_codes`, and `nonclaims`;
- Phase 3 tests must fail if downstream consumers could infer full
  observed-data/filtering admission from row id or row presence alone.

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Admit a distinct scoped component row for parameterized-logscale Zhao-Cui SIR fixed-variant local complete-data value and analytical/manual score. |
| Primary criterion status | Passed: the row id, theta semantics, computed quantity, score provenance, and nonclaims are explicit. |
| Veto diagnostic status | Passed: no full observed-data/filtering likelihood or score identity is claimed; retained-grid is not admitted; autodiff/FD gradients are not admitted. |
| Main uncertainty | This row is a scoped local component row. It does not complete the full observed-data/filtering SIR leaderboard row. |
| Next justified action | Phase 3 should wire the runner and tests to emit the scoped row and preserve the fixed row. |
| What is not being concluded | No exact likelihood proof, no full observed-data/filtering score identity, no posterior correctness, no universal GPU speed superiority, no source-faithful inference-theta claim. |

## Row Contract

| Field | Contract |
| --- | --- |
| Row id | `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale` |
| Algorithm id | `zhao_cui_scalar_or_multistate` |
| Row admission | `scoped_component_row_admitted` |
| Route role | `fixed_variant_zhao_cui_source_route` |
| Retained-grid admission | `not_admitted_for_production_leaderboard_use_fixed_variant_zhao_cui` |
| Target scope | `local_complete_data_zhao_cui_sir_d18_component` |
| Theta coordinate | `sir_log_scale_theta` |
| Truth theta | `[0.0, 0.0, 0.0]` |
| Parameter order | `log_kappa_scale`, `log_nu_scale`, `log_obs_noise_scale` |
| Truth semantics | Log-scale origin reproduces the fixed source SIR base parameters. |
| Source/adaptation classification | `extension_or_invention` for the inference theta over source-anchored fixed SIR formulas. |
| Value quantity | Complete-data log density along the generated T20 latent state path and observations for the parameterized SIR model. |
| Value implementation | `ParameterizedZhaoCuiSIRSSM.initial_log_density`, `transition_log_density`, and `observation_log_density`, optionally cross-checked by `zhao_cui_sir_austria_local_complete_data_log_density_xla`. |
| Score quantity | Analytical/manual derivative of the complete-data log density with respect to the three log-scale parameters. |
| Score implementation | `initial_log_density_parameter_score`, `transition_log_density_parameter_score`, and `observation_log_density_parameter_score`. |
| Score status | `analytical_score_emitted` if finite under Phase 3 implementation checks. |
| Score provenance | `zhao_cui_sir_d18_local_complete_data_manual_parameter_score_methods` |
| Sidecar status | P91 CPU/GPU/XLA/HMC evidence remains scoped supporting evidence, not full-filtering timing/ranking evidence. |
| Fixed-row preservation | `zhao_cui_spatial_sir_austria_j9_T20` remains fixed/no-free-theta and may stay value-only or blocked for parameter score. |

## Why This Is The Correct Scope

Phase 1 established that the fixed-variant implementation already has:

- a local complete-data value route;
- analytical/manual initial, transition, and observation score methods;
- P91 score-at-true evidence under the local complete-data/component scope;
- P91 GPU/XLA and HMC smoke evidence only under the same scoped target.

The July 2 parameterized-SIR program established that:

- the distinct dataset row
  `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale` exists;
- the fixed row is preserved as no-free-theta evidence;
- the attempted generic full tensor-product retained-grid evaluator is blocked
  and has now been demoted to diagnostic/historical evidence.

Therefore the safe repair is not to revive the retained-grid full-filtering
route. The safe repair is to make the scoped fixed-variant component row
visible and numerically populated, with the parameterization stated in the row
id and the local-complete-data/component scope stated in explicit metadata.

## Forbidden Claims Preserved

The final row must not claim:

- exact observed-data filtering likelihood;
- full observed-data/filtering score identity;
- exact likelihood correctness;
- posterior correctness or convergence;
- source-faithful inference parameterization;
- universal GPU speed superiority;
- production default change beyond the scoped row admission;
- full-row admission inferred from row id or row presence alone;
- timing ranking from P91 sidecar evidence;
- autodiff or finite-difference gradient as the leaderboard analytical score.

## Required Phase 3 Behavior

Phase 3 must:

- add `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale` to the
  highdim leaderboard rows;
- create or use a dataset helper that returns the generated T20 parameterized
  SIR states and observations at seed `81103`;
- emit a `zhao_cui_scalar_or_multistate` cell with finite local complete-data
  value and finite analytical/manual score;
- set `comparison_status = executed_value_score`;
- set `row_admission_status = scoped_component_row_admitted`;
- set `target_scope = local_complete_data_zhao_cui_sir_d18_component`;
- set `score_status = analytical_score_emitted`;
- set `score_derivative_provenance =
  zhao_cui_sir_d18_local_complete_data_manual_parameter_score_methods`;
- set `target_contract_status =
  target_compatible_scoped_local_complete_data_component`;
- attach P91 scoped evidence without treating P91 timing as main-row ranking;
- leave the original fixed row distinct and honest;
- add tests proving that the new row is parameterized, finite, manual-score
  only, metadata-scoped as local complete-data/component evidence, and not
  retained-grid production evidence.

Phase 3 must not:

- call the demoted retained-grid route;
- report the generic retained-grid complexity blocker as solved;
- report a full observed-data/filtering score for SIR;
- use the XLA helper's `GradientTape` gradient as the leaderboard score.

## Local Checks

Commands:

```bash
rg -n "parameterized_logscale|source_scope_row_ids|zhao_cui_spatial_sir" docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-contract-2026-06-11.json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-numeric-results-2026-06-13.json docs/plans/bayesfilter-parameterized-sir-target-contract-2026-07-02.md docs/plans/bayesfilter-parameterized-sir-semantic-binding-2026-07-02.md
sed -n "1,280p" docs/plans/bayesfilter-parameterized-sir-target-contract-2026-07-02.md
sed -n "1,180p" docs/plans/bayesfilter-parameterized-sir-semantic-binding-2026-07-02.md
sed -n "1,260p" docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase3-full-evaluator-result-2026-07-02.md
python -m json.tool docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase3-full-evaluator-blocker-2026-07-02.json
git diff --check -- docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-*.md
```

Outcome:

- Parameterized row contract artifacts were found.
- The July 2 full retained-grid evaluator blocker was found and preserved.
- The old source-scope row list does not yet include the parameterized row;
  Phase 3 must update leaderboard code/metadata rather than rely on stale P8d
  cells.
- `git diff --check` passed.

## Phase 3 Handoff

Phase 3 may start after Claude boundary review agrees with this Phase 2 result.

The required implementation target is narrow:

- add the scoped parameterized-logscale local complete-data row;
- leave the original fixed row untouched;
- require metadata scope checks rather than relying on row id alone;
- preserve all full-filtering nonclaims and retained-grid demotion.
