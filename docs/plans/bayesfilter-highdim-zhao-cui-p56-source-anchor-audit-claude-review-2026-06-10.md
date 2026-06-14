# P56 Claude Review: Zhao-Cui Source-Anchor Audit

metadata_date: 2026-06-10

reviewer: Claude Code, Opus max effort, read-only

supervisor: Codex

reviewed_artifact:
`docs/plans/bayesfilter-highdim-zhao-cui-p56-source-anchor-audit-2026-06-10.md`

## Invocation Notes

The first full prompt and the first compact prompt were slow/silent beyond the
useful threshold.  A minimal probe returned `PROBE_OK`, so Claude availability
was confirmed.  The compact source-anchor prompt eventually returned.  The
first full prompt also returned late after the compact response.  Both reviews
are recorded below because the late first response caught a sharper
proposal-density semantic issue.

## Claude Verdict

`VERDICT: REVISE`

Claude agreed with the draft's overall negative judgment but found material
corrections required before the artifact could be marked converged.

## Anchors Claude Reported Checking

- Governance gate: `AGENTS.md:32-60`.
- Codex draft:
  `docs/plans/bayesfilter-highdim-zhao-cui-p56-source-anchor-audit-2026-06-10.md:12-331`.
- P55 baseline:
  `docs/plans/bayesfilter-highdim-zhao-cui-p55-source-paper-code-repair-result-2026-06-10.md:12-17`,
  `:109-120`.
- Paper recursion/basic/squared-TT/KR/particle/preconditioning/SIR:
  `/tmp/zhao_cui_jmlr_2024.txt:339-366`, `:457-520`,
  `:549-626`, `:627-670`, `:693-719`, `:830-924`,
  `:1461-1706`, `:2249-2365`.
- Author source: `full_sol.m:21-135`, `pre_sol.m:16-260`,
  `ssmodel.m:45-59`, `computeL.m:14-47`, `eg3_sir/mainscript.m:14-56`,
  `SIRT.m:77-85`, `AbstractIRT.m:152-355`,
  `@TTSIRT/marginalise.m:1-87`,
  `@TTSIRT/eval_potential_reference.m:1-36`.
- BayesFilter code: `source_route.py:20-44`, `:373-438`, `:500-510`,
  `:1022-1092`, `:1116-1208`, `:1211-1283`, `:1325-1480`;
  `squared_tt.py:103-285`; `transport.py:1-221`;
  `fitting.py:181-302`, `:595-600`;
  `filtering.py:989-1008`, `:1353-1441`, `:2246-2356`;
  `transition_route.py:1-100`, `:616-746`; `rank_budget.py:1-314`.

## Required Revisions

1. The fixed-HMC adaptation rule should explicitly include freezing
   ESS-enhancement stop conditions and resampling policy, not only randomness,
   ranks, bases, schedules, and samples.  The author code adapts sample doubling
   based on ESS in `full_sol.m:53-62` and `pre_sol.m:41-99`.
2. The draft underplays that the BayesFilter transport protocol is missing
   forward KR and conditional KR interfaces.  `SourceRouteTransportProtocol`
   only requires `inverse_transport`, `log_reference_density`, and
   `log_normalizer`, while the author route requires `eval_rt` and `eval_cirt`
   semantics for Algorithm 3/5 and smoothing.
3. The P55 retained-sample routine computes proposal density through
   `transport.log_reference_density(reference)` before inverse transport.  The
   author correction uses target samples after `eval_irt` and `eval_pdf(sirt,r)`.
   This is not automatically wrong, but it is a high-risk semantic point needing
   proof/tests once a real transport exists.

## Late Full-Prompt Revision

The late full-prompt response strengthened item 3 above:

- `source_route_generate_retained_samples` currently computes proposal density
  as `transport.log_reference_density(reference) - log|det L|`.  The author code
  computes correction by dividing by `eval_pdf(sol.SIRTs{t}, r)` after
  `eval_irt(...)` in transport/local coordinates.  For a real SIRT/KR map, the
  proposal density is not merely the base/reference density; it includes the
  transported approximate-density or KR Jacobian semantics represented by
  `eval_pdf`.
- Therefore the current P55 proposal API is not just incomplete.  It risks
  baking in the wrong denominator semantics unless the transport protocol is
  changed to expose an `eval_pdf`-like density on local transported samples, or
  an equivalent Jacobian-aware log proposal density.
- Classification correction from the late full prompt: current
  `SourceRouteTransportProtocol` plus `source_route_generate_retained_samples`
  should be marked `extension_or_invention` or source-inconsistent as written,
  not merely governance substrate, until the proposal-density semantics are
  repaired.

## Classification Corrections

1. Split `source_route.py`:
   - `source_route_push_and_augment_samples`, `source_route_recenter`, and
     `source_route_log_normalizer_update` are `fixed_hmc_adaptation` substrate.
   - `SourceRouteTransportProtocol` and retained-manifest contracts are
     governance/interface substrate only, not an implemented transport
     adaptation.
2. `FixedTTFitter` should be classified as an `extension_or_invention`
   candidate, not a `fixed_hmc_adaptation` candidate, until there is a
   paper/source-backed proof that it preserves Proposition-2/KR semantics.
3. D06 should be classified as a source-faithfulness gap, not merely partial
   fixed-HMC adaptation, because the author correction is inseparable from the
   actual conditional KR transport.

## Highest-Risk Drift Points

- Mistaking grid-retained predictive propagation in `filtering.py:2246-2356`
  for a faithful stand-in for Algorithm 2/3 recursion.
- Treating `SquaredTTDensity.conditional_density` grid trapezoid integration as
  Proposition-2 marginal/KR closure.
- Promoting `FixedTTFitter` to a source-faithful transport fit without proving
  `marginalise`, `eval_pdf`, `eval_rt`, and `eval_cirt` equivalence.
- Missing the preconditioned retained-marginal step Algorithm 5(c.2), which is
  required for paper-scale SIR because the paper's SIR result uses Algorithm 2
  with linear preconditioning.

## Codex Disposition

Accepted.  The main audit is patched to incorporate both the compact review
corrections and the late full-prompt proposal-density correction.
