# P83 Phase 2 Result: Transport And Proposition-2 Marginalization Design

Date: 2026-06-22

Status: `PASS_P83_PHASE2_TRANSPORT_MARGINALIZATION_DESIGN`

## Decision

Phase 2 chooses a narrow repair design for the next implementation phase:

1. Preserve the existing fixed-TTSIRT transport surface only as a fixed-HMC
   source-route mechanics substrate.
2. Explicitly classify the current numerical CDF-grid KR path as a reviewed
   approximation/diagnostic surface, not production source-route closure.
3. Use paired-core mass-contraction marginal values as the retained-marginal
   slice for Phase 3.
4. Add metadata and readiness checks so Phase 3 cannot silently substitute:
   tensor-product suffix-grid conditionals, base/reference-density-only
   proposal correction, zero defensive mass, or old local/operator routes.
5. Defer full production KR replacement and author-scale d=18 validation until
   after the minimal slice proves the retained-object mechanics honestly.

This is a design result only.  It does not implement code and does not validate
the source route numerically.

## Evidence Contract Result

| Field | Result |
|---|---|
| Question | What is the narrow source-backed transport and marginalization repair design needed before implementation? |
| Baseline/comparator | P83-1 inventory, P56/P61 source anchors, P57-M2 transport contract, P57-M6 retained-object loop, P58-M9 readiness guard, and Zhao-Cui author `full_sol`, `SIRT`, `AbstractIRT`, and `@TTSIRT` operations. |
| Primary criterion status | PASS: the design names required operations, classifies the numerical CDF-grid path, rejects base-density and tensor-product suffix-grid substitutes, defines focused Phase 3 tests, and preserves nonclaims. |
| Veto diagnostic status | PASS: no d=18/LEDH/GPU/numerical launch is authorized; no source-faithful production closure is claimed. |
| Explanatory diagnostics | P83-1 inventory table, code/source anchors, and Phase 3 test design. |
| Not concluded | No code implementation, no source-route correctness, no production KR closure, no d=18 validation, no derivative readiness, no LEDH readiness, no HMC readiness. |

## Design Classifications

| Surface | Phase 2 classification | Reason | Phase 3 treatment |
|---|---|---|---|
| `SourceRouteTransportProtocol` | `fixed_hmc_adaptation` interface substrate | It requires the author-facing map/pdf/proposal/marginalizer surface but does not prove production semantics. | Keep and add focused guard tests around metadata and proposal semantics. |
| `SquaredTTDensity.normalized_marginal_density_values` for prefix/suffix retained axes | `fixed_hmc_adaptation` retained-marginal slice | It uses paired-core mass contractions and positive defensive contribution when configured. | Use for the minimal retained marginal mechanics slice. |
| `SquaredTTDensity.conditional_density` | `extension_or_invention` for source-route closure | It uses tensor-product suffix-grid integration and is not the author CDF-constructor/mass-recursion route. | Phase 3 tests/metadata must not rely on it as production Proposition-2/KR evidence. |
| `FixedTTSIRTTransport._source_conditional_density` plus `_cdf_from_conditional_grid` | `fixed_hmc_adaptation` diagnostic approximation only | It uses marginal ratios from paired-core marginal evaluators, but CDFs and inversion are numerical grid/trapezoid approximations rather than source CDF-constructor semantics. | Metadata must label this route and nonclaims; mechanics tests may use it but cannot certify production KR closure. |
| `FixedTTSIRTTransport.eval_pdf` and `proposal_log_density` | `fixed_hmc_adaptation` if defensive mass and marginal metadata pass | Proposal denominator matches the `eval_pdf` identity used by author correction. | Phase 3 must reject base/reference-density-only substitutes. |
| Current local all-grid/operator filter route | `extension_or_invention` | P56/P83-1 classify it outside retained-object TTSIRT/KR source route. | Must remain quarantined. |

## Required Phase 3 Implementation Slice

Phase 3 should make the smallest code/test change set that enforces this design:

1. Add explicit manifest metadata to `FixedTTSIRTTransport.manifest_payload()`:
   - `proposition2_marginal_backend`;
   - `conditional_cdf_backend`;
   - `conditional_cdf_route_class`;
   - `production_kr_closure`;
   - `proposal_density_backend`;
   - `p83_nonclaims`.
2. Add a metadata/readiness guard or focused tests that require, for the P83
   minimal source-route slice:
   - `source_contract_level == "fixed_ttsirt"`;
   - `defensive_mass_positive is True`;
   - marginal backend is paired-core/mass-contraction based;
   - proposal density backend is `eval_pdf` on local transported samples;
   - numerical CDF-grid backend is not advertised as production KR closure;
   - local/operator/all-grid route markers are absent.
3. Add focused tests using a small positive-defensive-mass `FixedTTSIRTTransport`
   to verify:
   - manifest metadata and nonclaims;
   - prefix retained marginal evaluation uses the marginal object/evaluator;
   - proposal correction uses `eval_pdf`, not base/reference density;
   - a tiny two-step retained-object mechanics path can carry the previous
     retained object while preserving the nonclaim that KR closure is not
     certified.

Phase 3 should not replace the full KR implementation, fit author-scale
TTSIRTs, change rank policy, or run d=18 validation.

## Source Anchors Preserved

| Operation | Source anchor | Phase 3 implication |
|---|---|---|
| Sequential solve and proposal correction | `full_sol.m:21-43`, especially `:33-38` | Keep proposal correction as target density divided by transport `eval_pdf`, not base density. |
| Previous retained marginal | `full_sol.m:72-81`, `:117-120` | Retained marginal must be a real marginal evaluator of the previous transport. |
| Log normalizer increment | `full_sol.m:84-124` | Mechanics result may sum `log(z)-const`, but cannot claim author-scale likelihood correctness. |
| CDF construction and marginalization | `SIRT.m:74-85`; `@TTSIRT/marginalise.m:25-85`; `eval_potential_reference.m:10-33` | Phase 3 metadata must distinguish current numerical CDF grid from source CDF-constructor semantics. |
| KR API | `AbstractIRT.m:152-333` | Protocol methods remain required, but production KR closure is not claimed until a later design/implementation gate. |

## Phase 3 Test Matrix

| Test intent | Required check | Forbidden pass condition |
|---|---|---|
| Manifest honesty | Positive-defensive `FixedTTSIRTTransport` reports paired-core marginal backend, numerical CDF-grid approximation, `production_kr_closure=False`, and proposal `eval_pdf` backend. | Manifest says or implies production KR/source-faithful closure from numerical CDF grids alone. |
| Defensive mass | P83 readiness/test fixture uses `defensive_mass_positive=True`. | Zero defensive mass accepted for the P83 minimal source-route slice. |
| Proposal denominator | Retained-sample proposal log density equals `log(eval_pdf(local))`. | Base/reference-density-only proposal passes. |
| Retained marginal | Previous marginal path evaluates the marginal transport/evaluator for prefix axes. | Old all-grid/local/operator retained storage or tensor-product suffix-grid conditional route passes as source closure. |
| Two-step mechanics | Retained object after step 1 is carried into step 2 and previous marginal evidence exists. | Any claim of d=18 correctness, production KR closure, HMC readiness, or exact likelihood correctness. |

## Stop Conditions For Phase 3

Phase 3 must stop if:

- the current code cannot expose honest metadata without changing unrelated
  route behavior;
- tests require relying on tensor-product suffix-grid conditionals as production
  source-route evidence;
- proposal correction can only be implemented through base/reference density;
- positive defensive mass breaks the minimal fixture in a way that needs a
  larger design;
- implementation would require broad refactors or d=18/GPU/LEDH work.

## Local Checks

Passed:

```text
rg -n "fixed TT|TTSIRT|defensive|normalizer|Proposition-2|Proposition 2|mass-matrix|QR|eval_pdf|potential|forward|inverse|conditional|KR|proposal|retained|branch|numerical CDF-grid|production_kr_closure" \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase2-transport-marginalization-design-subplan-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase2-transport-marginalization-design-result-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase3-minimal-transport-slice-subplan-2026-06-22.md -S
```

Result: passed with expected design-topic hits.

Passed:

```text
rg -n "tensor-product grid|tensor-product suffix-grid|base-density-only|extension_or_invention|source_faithful|fixed_hmc_adaptation|BLOCK_SOURCE_UNGROUNDED|d=18|LEDH|GPU|HMC|production" \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase2-transport-marginalization-design-subplan-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase2-transport-marginalization-design-result-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase3-minimal-transport-slice-subplan-2026-06-22.md -S
```

Result: passed with expected veto/nonclaim hits.

Passed:

```text
git diff --check -- \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase2-transport-marginalization-design-subplan-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase2-transport-marginalization-design-result-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase3-minimal-transport-slice-subplan-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-visible-execution-ledger-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-claude-review-ledger-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-visible-stop-handoff-2026-06-22.md
```

Result: passed with no output.

## Claude Read-Only Review

Review `p83-p2-design-p3-handoff-review-r1` returned `VERDICT: AGREE`.

Key review points:

- no wrong-baseline blocker;
- no proxy-promotion blocker;
- numerical conditional-CDF grid route-boundary risk is acknowledged and
  contained;
- Phase 3 artifacts are manifest/readiness/mechanics artifacts, not scientific
  validation artifacts;
- Phase 3 scope is appropriately narrow.

Review caution:

- Phase 3 should hard-fail any accidental production KR closure metadata for
  the current grid-CDF route.

## Decision Table

| Decision | Primary criterion | Veto diagnostics | Main uncertainty | Next justified action | Not concluded |
|---|---|---|---|---|---|
| Pass Phase 2 design. | Design classifies the current transport pieces, names the minimal Phase 3 slice, and blocks silent grid/base-density substitutes. | No early implementation or validation launch; no source-faithful production closure from CDF grids. | Whether the metadata/readiness guard is enough for Phase 3 mechanics before full KR replacement. | Implement Phase 3 minimal slice. | No production source-route transport, d=18 validation, derivative readiness, or HMC readiness. |

## Next-Phase Handoff

P83-3 may begin only if:

- Phase 2 local checks pass;
- Claude read-only review agrees or non-material comments are resolved;
- Phase 3 subplan exists and preserves the design above;
- implementation scope is limited to metadata/readiness guard and focused tests;
- no d=18, GPU, LEDH, or broad refactor work is included.
