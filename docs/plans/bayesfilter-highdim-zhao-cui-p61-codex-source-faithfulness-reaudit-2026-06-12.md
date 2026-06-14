# P61 Codex Audit: Zhao-Cui Source-Faithfulness Reaudit

metadata_date: 2026-06-12
status: CODEX_BOUNDED_AUDIT_COMPLETE
supervisor: Codex
scope: bounded source/paper/code discrepancy audit only

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What source-code and paper-level discrepancies remain between the Zhao-Cui author SIR route and the BayesFilter P57/P59/P60 source-route implementation, excluding the intentional fixed/HMC-compatible variant requirement? |
| Author baseline | `third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m`, `models/full_sol.m`, `models/Y_sol.m`, `models/computeL.m`, `deep-tensor.dev/src/SIRT.m`, `@TTSIRT/TTSIRT.m`, `@TTSIRT/marginalise.m`, `@TTSIRT/eval_*_reference.m`, `Options/TTOption.m`. |
| BayesFilter implementation inspected | `bayesfilter/highdim/source_route.py`, `squared_tt.py`, `transport.py`, `fitting.py`, and prior P55/P60 result ledgers. |
| Classification labels | `MATCH`, `FIXED_VARIANT_ACCEPTED`, `MISMATCH`, `MISSING`, `AGENT_INVENTED`, `NEEDS_SOURCE_CHECK`. |
| Veto checks | This audit must include author anchors, the known defensive-density issue, the fixed-variant carveout, and must not claim repair, d=18 success, rank convergence, d=50/d=100 readiness, or HMC production readiness. |

## Fixed-Variant Carveout

The fixed branch remains intentional and allowed: fixed ranks, fixed samples,
fixed seeds, TensorFlow/TFP implementation, and no adaptive rank mutation inside
an HMC likelihood call are not counted as source noncompliance.  The carveout
does not allow source-created replacements to be labeled as author-faithful
without author-code or paper anchors.

## Source Anchors Checked

| Topic | Author anchor | BayesFilter anchor |
| --- | --- | --- |
| SIR row | `eg3_sir/mainscript.m:14-17`, `39-56` | `source_route.py:1826-1994`, `2180-2452` |
| Full filtering loop | `full_sol.m:21-43` | `source_route.py:2180-2452` |
| ESS enhancement and recentering | `full_sol.m:49-68`; `computeL.m:14-47`; `ESS.m:1-4` | `source_route.py:4694-4740`, P55 ledger |
| Prior/previous retained density | `full_sol.m:72-81` | `source_route.py:2292-2361`, `2486-2525` |
| Shift/determinant/InputData | `full_sol.m:84-98` | `source_route.py:1875-1900`, `2265-2281`, `2323-2335` |
| TTSIRT construction and options | `full_sol.m:101-124`; `TTOption.m:1-93`; `TTSIRT.m:185-244` | `fitting.py:181-302`; `source_route.py:1910-1952`, `2570-2624` |
| Defensive squared-SIRT semantics | `TTSIRT.m:185-188`; `SIRT.m:73-85`; `marginalise.m:85`; `eval_irt_reference.m:25-42`; `eval_rt_reference.m:23-46`; `eval_cirt_reference.m:88-100`; `eval_potential_reference.m:20-33` | `squared_tt.py:112-184`; `transport.py:316-340`, `452-473`; `source_route.py:1965-1982`, `2625-2642` |

## Discrepancy Ledger

| ID | Classification | Topic | Finding | Source evidence | BayesFilter evidence | Repair implication |
| --- | --- | --- | --- | --- | --- | --- |
| P61-D01 | `MISMATCH` | Defensive mass disabled in P59/P60 source-route construction | Author TTSIRT has a positive default defensive term and uses `+ obj.tau` in the normalizer, inverse/forward CDFs, conditional inverse CDF, and potential. The P59/P60 author-SIR route constructs `SquaredTTDensity` with `tau=0.0`, disabling this behavior. This is the direct explanation for the P60 rank-2 zero-normalizer failure. | `TTSIRT.m:185-188`; `SIRT.m:73-85`; `marginalise.m:85`; `eval_irt_reference.m:25-42`; `eval_rt_reference.m:23-46`; `eval_cirt_reference.m:88-100`; `eval_potential_reference.m:20-33` | `source_route.py:1965-1982`, `2625-2642`; `squared_tt.py:177-184`; P60-2 result records `NORMALIZER_FLOOR_EXCEEDED` | Make the fixed source route use a positive frozen defensive mass matching author semantics, with explicit fixed-branch metadata and tests that zero TT mass still has positive normalizer. |
| P61-D02 | `NEEDS_SOURCE_CHECK` | SIR script `tau=10` versus TTSIRT operative defensive value | The SIR script declares `tau=10`, but `full_sol(model, sqr, poly, opt, lowopt, N, epd)` does not receive or pass that variable to `TTSIRT`; the operative TTSIRT constructor default is `1e-8` unless another source path modifies it. Therefore the repair should not blindly set `tau=10`; it should document whether the author intended `tau=10` but failed to wire it, or whether `1e-8` is the actual executable behavior. | `eg3_sir/mainscript.m:39-40`, `53-56`; `full_sol.m:9-10`, `116-120`; `TTSIRT.m:185-188`; `AbstractIRT.m:104-120` | `source_route.py:1969`, `1977`, `2629`, `2637` | Add a source-resolution note and a parameterized repair path: default to executable author-code TTSIRT `1e-8` unless a reviewed source argument justifies SIR `tau=10`. |
| P61-D03 | `MISMATCH` | Manifest overstates defensive density | `FixedTTSIRTTransport.manifest_payload()` declares `defensive_density_declared=True`, but the author-SIR route instances use `tau=0.0`, so the defensive component exists structurally but contributes zero mass. | TTSIRT source uses `obj.tau` additively throughout maps and normalizer | `transport.py:316-340`; `source_route.py:1969-1977`, `2629-2637` | Manifest must distinguish `defensive_density_object_present` from `defensive_mass_positive`. |
| P61-D04 | `FIXED_VARIANT_ACCEPTED` | Fixed-rank deterministic fitting rather than random/adaptive TT construction | Author uses `TTOption('tt_method','random', max_rank=40, max_als=8, init_rank=20, kick_rank=5)` and then `lowopt` with `max_als=2` after the first step. BayesFilter uses fixed rank, fixed initial cores, one sweep, deterministic samples. This is acceptable only under the fixed/HMC-compatible lane and cannot be called an adaptive author reproduction. | `eg3_sir/mainscript.m:48-51`; `full_sol.m:115-120`; `TTOption.m:1-93` | `fitting.py:181-302`; `source_route.py:1918-1952`, `2588-2624` | Keep the carveout, but label all results as fixed source-route approximations; do not treat adaptive parity as a future gap unless explicitly requested. |
| P61-D05 | `MISMATCH` | Basis/domain mapping is simplified | Author SIR uses `Lagrangep(4,8)` with `AlgebraicMapping(1)` on dimension `d+2m=36`. BayesFilter P59/P60 route uses `LegendreBasis1D(BoundedInterval(-1,1), fit_degree)` with tiny degrees. | `eg3_sir/mainscript.m:43-45` | `source_route.py:1910-1917`, `2581-2587` | Repair should either implement/document the author Lagrange/algebraic mapping semantics or explicitly classify the fixed Legendre bounded basis as a lower-rung diagnostic, not paper-scale faithfulness. |
| P61-D06 | `MISMATCH` | Sample counts and fitting data are diagnostic, not source scale | Author SIR uses `N=5e3`, pushes/resamples weighted samples, splits unweighted transformed samples into `InputData(samples_init, samples_debug)`. P59/P60 use tiny deterministic reference grids/samples by default. | `eg3_sir/mainscript.m:39`; `full_sol.m:64-98` | `source_route.py:1828`, `1865-1867`, `2244-2252`, `1918-1929`, `2588-2600` | Treat current P59/P60 as wiring/smoke evidence. Source-scale fixed execution needs source-derived sample generation, weighted resampling, and an explicit memory/rank budget. |
| P61-D07 | `PARTIAL/MISMATCH` | `computeL`/affine frame integration incomplete for source loop | Author computes weighted mean/covariance, prunes nonfinite samples, applies quantile scaling if ESS is high, then multiplies `L_temp` by `epd=4` for SIR. BayesFilter has related helpers, but the P59/P60 author-SIR assembly uses deterministic coordinate frames rather than the full source sampled `computeL -> datasample -> InputData` loop. | `computeL.m:14-47`; `full_sol.m:64-68`; `eg3_sir/mainscript.m:54-55` | `source_route.py:2073-2107`, `4694-4740`; P55-D05 | Implement the source-loop affine frame as part of source-route fitting before claiming d=18 paper-scale behavior. |
| P61-D08 | `MISSING` | Full executable filtering loop and proposal correction | Author loop pushes particles, fits/reapproximates, samples from `eval_irt`, maps back through `L`, corrects by `exp(-fun_post(r))./eval_pdf(sirt,r)`, and records ESS/weights. BayesFilter has step specs and retained objects, but no full executable source-route filter loop at author scale. | `full_sol.m:21-43` | `source_route.py:2180-2452`; P55-D01, D07, D08 | Build and test the full fixed source-route loop only after defensive mass and one-step transport validity pass. |
| P61-D09 | `PARTIAL/MISSING` | Previous SIRT marginalization for `t>1` | Author reuses previous SIRT, marginalizes it to `int_dir=1` when needed, evaluates its density under the previous affine frame, and uses it as the prior for the next augmented target. BayesFilter has previous-marginal evidence in P59-9b, but it depends on the bounded fixed transport and not yet the full source loop. | `full_sol.m:72-81`, `117-120` | `source_route.py:2299-2327`, `2346-2361`, `2486-2525` | Keep as partial until tested inside an executable multi-step fixed source loop with positive defensive mass. |
| P61-D10 | `MISMATCH` | Log marginal accounting is not yet source-faithful in execution | Author updates `logmarginal_likelihood += log(sirt.z) - const`. P59/P60 has normalizer objects and manifests, but not a full source-loop marginal likelihood tied to the source shift/determinant path and proposal correction. | `full_sol.m:84-93`, `124` | `squared_tt.py:177-184`; `transport.py:472-473`; `source_route.py:2394-2442` | Add a first-class fixed source-loop result that records `log(z)-const` and determinant accounting before using the value path scientifically. |
| P61-D11 | `AGENT_INVENTED` | UKF/rank calibration is not in Zhao-Cui source | UKF can be useful as a scout/comparator for fixed-rank selection, but it is not part of the author SIR source route. It should remain a BayesFilter calibration heuristic, not a source-faithfulness claim. | No UKF path in `eg3_sir/full_sol/TTSIRT` anchors | `rank_budget.py`, `ukf_scout.py`, P57-M7/P52/P53 artifacts | Keep UKF in a separately labeled calibration lane; source-faithful repair must first follow author route semantics. |
| P61-D12 | `MISSING` | Paper-scale d=18 claim remains blocked | Author target dimension is 36 for `d=0,m=18,T=20`. P59/P60 provides bounded assembly evidence and P60 exposes a rank comparator blocker; it does not establish d=18 filtering performance, rank convergence, d=50/d=100 scaling, or HMC readiness. | `eg3_sir/mainscript.m:14-17`, `39-56` | P60-2 result; `source_route.py:2435-2442` | Do not declare paper-scale success until the repaired fixed source loop passes d=18 gates. |

## Repair Ordering Suggested By This Audit

1. Resolve defensive-mass source semantics: executable author default `1e-8`
   versus script-declared `tau=10`; implement a positive frozen defensive mass
   with explicit metadata.
2. Add zero-mass/low-rank defensive tests: a fitted TT with zero square mass
   must still produce positive normalizer/CDF/potential under the defensive
   route.
3. Correct transport manifests so positive defensive mass is an invariant, not
   a vague declaration.
4. Re-run the P60-2 same-route comparator after the defensive repair.
5. Only then move to source-loop gaps: source `computeL`, weighted resampling,
   `InputData`, proposal correction, previous marginalization, and
   `log(sirt.z)-const`.

## What Is Not Concluded

- No implementation repair was made.
- No d=18 filtering success is claimed.
- No rank convergence, d=50/d=100 launch, or HMC production readiness is
  claimed.
- No adaptive Zhao-Cui parity is required by this fixed/HMC-compatible lane.

