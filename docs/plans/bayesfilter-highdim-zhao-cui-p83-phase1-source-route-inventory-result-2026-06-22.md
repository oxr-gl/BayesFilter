# P83 Phase 1 Result: Anchored Source-Route Inventory

Date: 2026-06-22

Status: `PASS_P83_PHASE1_SOURCE_ROUTE_INVENTORY`

## Decision

P83 Phase 1 completes the read-only inventory and hands off to P83-2 transport
and Proposition-2 marginalization design.

The current checkout has meaningful source-route substrate:

- source-route operation contracts and forbidden drift markers;
- a transport protocol requiring `eval_pdf`, KR-style maps, marginalization,
  proposal log density, and normalizer semantics;
- squared-TT density with defensive mass and paired-core marginal value
  evaluation for prefix/suffix retained axes;
- a `FixedTTSIRTTransport` map surface;
- proposal correction through transport `eval_pdf` semantics;
- a two-step fixed-HMC sequential runner over supplied/frozen transports;
- rank-governance policy that rejects UKF and old local/operator rank evidence
  as source-route truth;
- a d=18 launch-readiness guard.

The same inventory keeps the source-route claim bounded:

- production author-scale fixed TTSIRT fitting quality is not certified;
- the `FixedTTSIRTTransport` conditional CDF/inversion path still uses numerical
  CDF grids over source-style marginal ratios, so Phase 2 must decide whether
  and how to replace or explicitly classify that approximation;
- previous marginal mechanics exist over supplied/frozen transports, but not as
  a validated author-SIR d=18 fitted source-route pipeline;
- the local all-grid/operator route remains `extension_or_invention`;
- UKF, validation CE, FD, and ForwardAccumulator/JVP remain diagnostic-only.

## Evidence Contract Result

| Field | Result |
|---|---|
| Question | What source-route pieces are implemented, partial, missing, or diagnostic-only, and what repair should Phase 2 design? |
| Baseline/comparator | P50/P56 source-route operations, P57/P58 contracts, P61 discrepancy audit, and Zhao-Cui author source. |
| Primary criterion status | PASS: every material row below has local anchors, paper/project or prior-audit anchors, author-source anchors where applicable, status, classification, and next repair action. |
| Veto diagnostic status | PASS: no unanchored source-faithful closure is made; local/operator, UKF, FD, validation CE, and JVP paths are not promoted. |
| Explanatory diagnostics | Read-only code/test/source/doc anchors and prior audit ledgers. |
| Not concluded | No implementation repair, no code correctness certification, no d=18 success, no transport production readiness, no analytical derivative readiness, no LEDH readiness, no HMC readiness. |

## Read-Only Commands

The inventory used read-only `rg`, `sed`, `nl`, and `git status` commands over:

- `bayesfilter/highdim/source_route.py`
- `bayesfilter/highdim/transport.py`
- `bayesfilter/highdim/squared_tt.py`
- `bayesfilter/highdim/rank_budget.py`
- `bayesfilter/highdim/fitting.py`
- source-route tests under `tests/highdim`
- P50/P56/P57/P58/P61/P81/P82 artifacts
- Zhao-Cui author source under
  `third_party/audit/zhao_cui_tensor_ssm_p10/source`

No implementation code, tests, GPU jobs, or numerical experiments were run.

## Inventory Table

| Component | Required Zhao-Cui operation | Local implementation anchor | Paper/project anchor | Author-source anchor | Status | Classification | Next repair action |
|---|---|---|---|---|---|---|---|
| Route identity and drift guard | Retained-object TTSIRT/KR route, not all-grid/operator route | `source_route.py:44-68` defines route label, required operations, and forbidden drift markers; `source_route.py:8338-8358` rejects all-grid retained storage and pairwise grid propagation for source route | P56 decision table and source-anchor gate; reset memo | `full_sol.m:21-43` retained-object solve loop | implemented as governance guard | `fixed_hmc_adaptation` substrate | Keep guard active; Phase 2 must not design around forbidden local/operator substitutes. |
| Transport protocol surface | Inverse KR, forward KR, conditional KR, `eval_pdf`, potential, proposal density, marginalization, normalizer | `source_route.py:619-797`; tests `test_p57_m2_fixed_ttsirt_transport_contract.py:97-160` | P57-M2 result; P50 KR sections around `1562`, `1597`, `1923` | `AbstractIRT.m:152-188`, `192-213`, `217-270`, `299-333` | implemented interface; production semantics still require repair/audit | `fixed_hmc_adaptation` substrate | Phase 2 must specify production semantics and tests for all protocol methods. |
| FixedTTSIRT map surface | TTSIRT-style KR maps and density evaluation | `transport.py:289-479`; tests `test_p57_m4_source_kr_cdf_maps.py:67-112` | P57-M4 result; P50 KR construction sections | `AbstractIRT.m:152-333`; `SIRT.m:74-85`; `TTSIRT.m:238-248` | partial | `fixed_hmc_adaptation` with approximation risk | Phase 2 must address that `transport.py:560-640` builds CDFs by numerical grid/trapezoid over conditional densities. |
| CDF/KR construction internals | Conditional CDFs from Proposition-2 marginal ratios | `transport.py:560-603`, `616-640` | P50 KR ratio sections around `1562-1718`, `1923-1930` | `SIRT.m:80-85`; `@TTSIRT/eval_irt_reference.m`, `eval_rt_reference.m`, `eval_cirt_reference.m` | partial/diagnostic risk | `fixed_hmc_adaptation` only if Phase 2 gives error/semantics contract; otherwise `extension_or_invention` for production claim | Design source-style CDF constructor or explicitly classify grid CDF approximation with veto/error tests. |
| Squared density and defensive mass | Nonnegative density `h^2 + tau q0`, normalizer, positive defensive term | `squared_tt.py:112-190`; `source_route.py:215-220`; `transport.py:316-346`; P61 notes prior tau mismatch | P50 defensive sections around `1445-1464`, `3897-4020`, `4424-4437` | `TTSIRT.m:185-188`; `SIRT.m:73-85`; `marginalise.m:85`; `eval_potential_reference.m:20-33` | implemented structurally; source-scale policy partial | `fixed_hmc_adaptation` | Phase 2 must pin positive defensive-mass policy and source-resolution note for executable `1e-8` versus script `tau=10`. |
| Proposition-2 marginal values | Mass contractions for retained marginal density | `squared_tt.py:164-185`, `212-260`, `262-312`; tests `test_p57_m3_proposition2_marginalization.py:56-113` | P50 Proposition-2 sections around `4011-4020`, retained evaluator sections around `7271-7488`; P56 D04 | `@TTSIRT/marginalise.m:25-85`; `eval_potential_reference.m:10-33` | partial | `fixed_hmc_adaptation` for prefix/suffix retained axes | Phase 2 must design full mass-matrix/QR retained-object marginalization semantics, supported axes, and normalizer/evaluator invariants. |
| Legacy conditional-density helper | Conditional density via suffix tensor-product grid integration | `squared_tt.py:334-392` | P56 D04/D05 warning | Author uses CDF constructors and `@TTSIRT` marginal data, not this tensor-product suffix grid | diagnostic-only | `extension_or_invention` for source-route closure | Phase 2 must forbid relying on this helper as production Proposition-2/KR source route. |
| Proposal sampling and correction | Sample via inverse map and correct by `exp(-fun_post(r))/eval_pdf(sirt,r)` | `source_route.py:7665-7719`; tests `test_p57_m5_proposal_density_retained_sampling.py:90-140` | P56 D06; P57-M5 result | `full_sol.m:33-38`; `AbstractIRT.m:299-307` | implemented for supplied transport | `fixed_hmc_adaptation` substrate | Phase 2/3 must verify production transport denominator is `eval_pdf`-equivalent, not base/reference density. |
| Previous retained marginal at `t>1` | Marginalize previous SIRT, evaluate under previous affine frame | `source_route.py:7722-7795`; tests `test_p57_m6_sequential_fixed_hmc_source_loop.py:203-290` | P50 retained filter sections around `1520`, `3748-3765`, `5988-6028`; P57-M6 result | `full_sol.m:72-81`, `117-120` | implemented mechanics over supplied transports; production source loop partial | `fixed_hmc_adaptation` substrate | Phase 2 must ensure marginal transport is a source-style retained marginal, not a grid/base-density substitute. |
| Sequential fixed-HMC source loop skeleton | Carry retained object and sum `log(z)-const` increments across at least two steps | `source_route.py:985-1038`, `1042-1090`, `1268-1295`, `7914-8049`; tests `test_p57_m6_sequential_fixed_hmc_source_loop.py:203-367` | P57-M6 result; P50 fixed-branch sections around `5724-5775` | `full_sol.m:21-43`, `84-124` | implemented skeleton over frozen specs; no fitting/rank certification | `fixed_hmc_adaptation` | Phase 3/5 can use this for mechanics smoke only after Phase 2 repair design. |
| Recenter/shift/normalizer helpers | `computeL`, shifted target, `log(sirt.z)-const` | `source_route.py:8090-8216`; P61 D07/D10 | P50 fixed-branch scalar and retained normalizer sections | `full_sol.m:64-93`, `124`; `computeL.m` | partial | `fixed_hmc_adaptation` | Phase 2 should include affine determinant and normalizer invariant tests; later phase must integrate source sample/resampling path. |
| Fixed TT fitter | Deterministic fixed-rank ALS for replayable fixed branch | `fitting.py:221-330`; P61 D04/D06 | P50 fixed-branch specialization sections around `4131-4173`, `5724-5775` | Author uses `TTFun` through `TTSIRT.m:238-248` with random/adaptive options in `eg3_sir/mainscript.m:48-51` | partial/fixed-variant only | `fixed_hmc_adaptation` if explicitly scoped; not adaptive source reproduction | Phase 6 must design parameter-count/sample-budget and rank ladder before source-route claims. |
| Rank policy | Rank chosen from fixed TT/SIRT comparator evidence; UKF only scout | `rank_budget.py:24-51`, `195-235`, `342-479`; tests `test_p57_m7_source_faithful_rank_ukf_calibration.py:71-153` | P57-M7 result | `eg3_sir/mainscript.m:48-56` | implemented governance policy | `fixed_hmc_adaptation` governance | Later rank claims require actual fixed TT/SIRT comparator evidence, not UKF or old `R_eff`. |
| M9/d=18 launch guard | Block d=18 launch without assembled source-route prerequisites | `source_route.py:1360-1425`; tests `test_p58_m9_source_route_pipeline_readiness.py:27-88` | P58-M9 result | `eg3_sir/mainscript.m:14-56`; `full_sol.m:21-43` | implemented guard | governance substrate | Keep d=18 blocked until required assembly flags are honest and comparator tier is reviewed. |
| Author SIR d=18 settings | d=0, m=18, T=20, N=5000, squared TTSIRT, rank controls, `full_sol(...); solve(...)` | Local model/runner status still partial per P61/P58 | P56 paper-scale SIR anchors; P61 D12 | `eg3_sir/mainscript.m:14-17`, `39-56` | missing as validated pipeline | not yet classifiable as source-faithful implementation | Phase 7 only after Phase 2-6 gates. |
| Local all-grid/operator route | Not part of author retained-object TTSIRT/KR route | `filtering.py:2075-2115`; `filtering.py:3992`; P81 Phase 12 result | P56 classifies as `extension_or_invention`; reset memo | No author retained-object match | diagnostic-only | `extension_or_invention` | Do not use to close source-route gaps. |
| Current multistate derivative/JVP surface | Diagnostic derivative backend, not source-backed analytical comparator | `filtering.py:1130`, `1369`, `1376`, `1460-1466`, `1697-1703`, `4327`; P82 Phase 1 result | P50 fixed-branch derivative sections around `4131-4173`, `7744-7880` | No inspected author-source derivative route for this local score path | diagnostic-only | `extension_or_invention` for source analytical comparator | P83-4 must audit/repair same-branch analytical route or write blocker. |
| UKF/minibatch/generated-sample lane | Scout/initializer only | `rank_budget.py:36-44`; P57-M7; reset memo | P56/P61 D11 | No UKF path in `full_sol`/TTSIRT author route | diagnostic-only | `extension_or_invention` for source-route evidence | Keep as scout; do not use to certify rank, target measure, or correctness. |

## Main Phase 2 Design Requirements

Phase 2 must design, before implementation:

- fixed TT/SIRT core representation and branch metadata;
- positive defensive mass semantics, including executable author default
  `1e-8` versus script-declared `tau=10`;
- normalizer and log-normalizer semantics;
- Proposition-2 mass-matrix/QR retained-object marginalization and supported
  retained-axis order;
- `eval_pdf`, potential, and proposal log-density semantics;
- forward/inverse/conditional KR APIs and whether current numerical CDF grids
  are production-eligible, diagnostic-only, or need replacement;
- affine-frame determinant placement;
- retained-object manifest and branch identity;
- focused tests for Phase 3 that reject tensor-product grid conditional
  integration and base-density-only proposal correction as source-route
  substitutes.

## Local Checks

Passed:

```text
rg -n "source_faithful|fixed_hmc_adaptation|extension_or_invention|implemented|partial|missing|diagnostic-only|diagnostic_only|BLOCK_SOURCE_UNGROUNDED" \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase1-source-route-inventory-result-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase2-transport-marginalization-design-subplan-2026-06-22.md -S
```

Result: passed with expected classification and status hits.

Passed:

```text
rg -n "multistate_tt_grid_retained_filter|ForwardAccumulator|UKF|validation CE|LEDH|d=18|tensor-product grid|base-density-only|numerical CDF-grid|suffix-grid" \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase1-source-route-inventory-result-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase2-transport-marginalization-design-subplan-2026-06-22.md -S
```

Result: passed with expected boundary and veto hits.

Passed:

```text
git diff --check -- \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase1-source-route-inventory-result-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase2-transport-marginalization-design-subplan-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-visible-execution-ledger-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-claude-review-ledger-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-visible-stop-handoff-2026-06-22.md
```

Result: passed with no output.

## Claude Read-Only Review

Review `p83-p1-inventory-p2-handoff-review-r1` stalled with no output.  It was
interrupted and the probe `p83-p1-claude-probe` returned `PROBE_OK`, so the
prompt was redesigned.

Review `p83-p1-inventory-p2-handoff-review-r2` returned `VERDICT: AGREE`.

Key review points:

- no wrong-baseline blocker;
- no proxy-promotion blocker;
- numerical CDF-grid conditional/inversion path is correctly elevated as a
  Phase 2 design risk;
- Phase 1 may close as inventory-only;
- Phase 2 may launch as design-only.

## Decision Table

| Decision | Primary criterion | Veto diagnostics | Main uncertainty | Next justified action | Not concluded |
|---|---|---|---|---|---|
| Pass Phase 1 inventory. | Inventory rows have anchors, status, classification, and next repair action. | No wrong-route or proxy evidence is promoted. | Whether current `FixedTTSIRTTransport` numerical CDF grid is acceptable only as fixed-HMC approximation or must be replaced for source-route production claims. | Launch Phase 2 design under the refreshed subplan. | No source-route implementation repair, d=18 validation, derivative readiness, LEDH readiness, HMC readiness, or production readiness. |

## Next-Phase Handoff

P83-2 may begin after local checks and read-only review agree that:

- the inventory conservatively classifies the current source-route substrate;
- Phase 2 is design-only;
- Phase 2 explicitly forbids tensor-product grid and base-density-only
  substitutes as production source-route closure unless it writes a reviewed
  approximation/error contract;
- Phase 2 does not authorize implementation, d=18 validation, GPU jobs, or
  LEDH comparison.
