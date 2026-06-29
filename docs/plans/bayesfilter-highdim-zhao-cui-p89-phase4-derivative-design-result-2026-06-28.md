# P89 Phase 4 Result: Diagnostic Source-Route Derivative Design Inventory

Date: 2026-06-28

Status: `P89_PHASE4_REVIEWED_DIAGNOSTIC_DERIVATIVE_DESIGN_CLOSED`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Phase 4 closes locally as diagnostic/design inventory only. Source-backed derivative-capable TTSIRT operations exist in the author route, and local source-route value mechanics exist, but source-route full-history analytical derivative readiness remains blocked. |
| Primary criterion status | Met locally for diagnostic/design inventory: derivative components are classified, `BLOCK_SOURCE_ROUTE_VALUE_BRIDGE_MISSING` is preserved, and the derivative-readiness blocker is preserved. |
| Veto diagnostic status | No derivative implementation, TensorFlow/Python runtime, FD validation, HMC/sampler, GPU/CUDA, production benchmark, package/network, or default-policy command was run. |
| Main uncertainty | A future replacement program could build a same-target value bridge and then design derivative-carry data structures, but this phase does not implement or certify them. |
| Next justified action | Review this result and the refreshed Phase 5 no-runtime derivative-implementation blocker subplan. If both agree, Phase 5 may close derivative implementation as blocked. |
| What is not being concluded | No `D18_CORRECTNESS_CANDIDATE`, value correctness, posterior correctness, source-route analytical-gradient readiness, derivative implementation readiness, FD validation, HMC readiness, GPU/XLA readiness, production readiness, LEDH agreement, scale readiness, or default-policy change. |

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | What source-route analytical derivative gaps remain, and can a future implementation design be specified without weakening the missing value-bridge blocker? |
| Baseline/comparator | P89 Phase 3 value-bridge blocker, P89 target manifest, P88 Phase 5 derivative blocker, local source-route code, and author TTSIRT derivative/marginalization anchors. |
| Primary criterion | Passed locally as diagnostic inventory only: missing value bridge and source-route derivative-readiness blockers are preserved, and future derivative implementation prerequisites are explicit. |
| Veto diagnostics | Passed locally: no derivative readiness promotion, value-bridge weakening, fixed-branch/JVP/autodiff promotion, runtime authorization, code edit, FD/HMC/GPU/production crossing, or unanchored source-faithful claim occurred. |
| Explanatory diagnostics | Component classification, author derivative-capable anchors, local source-route scalar surfaces, and missing derivative-carry paths. |
| Not concluded | No value correctness, gradient correctness, analytical-gradient readiness, FD validation, HMC/GPU/production readiness, LEDH agreement, scale readiness, or default-policy change. |
| Artifact | This Phase 4 result, refreshed Phase 5 subplan, ledgers, stop handoff. |

## Skeptical Audit Result

| Risk Checked | Result |
| --- | --- |
| Wrong baseline | Avoided. The baseline is the reviewed Phase 3 value-bridge blocker plus P88 derivative blocker, not rank/degree evidence or P87 fixed-branch evidence. |
| Proxy metrics promoted | Avoided. No JVP, FD, fixed-branch, rank/degree, validation-loss, or holdout evidence is promoted. |
| Missing stop conditions | Avoided. Phase 5 is refreshed as a no-runtime blocker closeout. |
| Unfair comparison | Avoided. No comparator or runtime is run. |
| Hidden assumptions | Exposed. Author derivative-capable operations are anchors for future design, not evidence that the local scalar derivative is implemented. |
| Stale context | Phase 3 and P88 Phase 5 reviewed blockers are inherited explicitly. |
| Environment mismatch | No framework/runtime command was run. |
| Artifact usefulness | The result identifies the exact derivative-carry gaps and prevents accidental implementation before the value bridge gate is repaired. |

## Component Classification

| Component | Local anchors | Author/source anchors | Classification | Phase 4 decision |
| --- | --- | --- | --- | --- |
| Source-route sequential scalar | `bayesfilter/highdim/source_route.py:7970-8039`; `bayesfilter/highdim/source_route.py:8086-8215` | `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:21-135` | source-route value mechanics | Present for value route, but no full derivative carry. |
| Retained sample/proposal correction | `bayesfilter/highdim/source_route.py:7837-7891`; `bayesfilter/highdim/source_route.py:8159-8192` | `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:90-94`; author TTSIRT inverse route below | source-route mechanics without dot objects | Needs derivative of proposal log density, target log density, correction weights, normalized correction, and normalizer. |
| Previous retained marginal | `bayesfilter/highdim/source_route.py:7894-7947`; `bayesfilter/highdim/source_route.py:8020-8025`; `bayesfilter/highdim/source_route.py:8138-8142` | `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/marginalise.m:1-87`; `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/AbstractIRT.m:299-307` | source-backed marginalization semantics | Needs derivative of marginal transport evaluation and affine prefix determinant. |
| Author inverse/potential/gradient | `bayesfilter/highdim/source_route.py:7837-7891` calls local protocol methods but does not expose source-backed derivative objects | `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/eval_irt_reference.m:1-188`; `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/AbstractIRT.m:160-184` | source-backed derivative-capable operation | Anchor for future transport and log-density derivative design; not locally wired. |
| Author map Jacobian | No source-route scalar derivative integration | `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/eval_rt_jac_reference.m:1-208`; `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/AbstractIRT.m:275-294` | source-backed map-Jacobian operation | Candidate future anchor for transport/proposal derivative, not readiness. |
| Local fixed-branch score plumbing | P87/P88 results and local filtering/model score hooks | No direct retained-object full-history author derivative route | fixed-HMC/local substrate | Useful as implementation substrate only; cannot close source-route derivative readiness. |
| Branch identity and retained object lineage | `bayesfilter/highdim/source_route.py:8180-8215`; `docs/plans/bayesfilter-highdim-zhao-cui-p89-target-manifest-2026-06-28.md` | Author full sequential retained-object lineage from `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:21-135` | fixed-HMC adaptation surface | Needs same-branch derivative manifest tying value and derivative to identical retained objects. |

## Remaining Design Gaps

Before any future source-route analytical-gradient readiness claim, a reviewed
replacement plan must provide all of the following:

- a same-target source-backed value bridge that closes
  `BLOCK_SOURCE_ROUTE_VALUE_BRIDGE_MISSING`;
- a derivative manifest tying value and derivative to the same scalar, branch,
  retained objects, ranks, bases, samples, schedules, parameterization, and
  normalizer convention;
- explicit dot-object contracts for retained transports, retained samples,
  correction weights, normalized correction weights, normalizer terms, and
  branch identity hashes;
- source-backed derivative operations for marginal transport evaluation,
  inverse/potential gradient, map Jacobian, proposal log density, target log
  density, affine-prefix determinant, and normalizer carry;
- tests that use FD/JVP/autodiff only as diagnostics and fail if the promoted
  path depends on them;
- a clear separation between local SIR model score algebra and full
  filter-level source-route derivative correctness.

## Blockers Preserved

```text
BLOCK_SOURCE_ROUTE_VALUE_BRIDGE_MISSING
P88_PHASE5_REVIEWED_BLOCK_SOURCE_ROUTE_DERIVATIVE_READINESS_CLOSED
```

Consequences:

- `D18_CORRECTNESS_CANDIDATE` remains blocked.
- Source-route full-history analytical derivative readiness remains blocked.
- Phase 5 cannot implement derivatives as a readiness-promotional phase.
- Phase 6 FD validation, Phase 7 HMC, Phase 8 GPU/XLA, and production
  promotion remain blocked.

## Local Checks

Commands:

```bash
rg -n "P89_PHASE3.*BLOCK_SOURCE_ROUTE_VALUE_BRIDGE_MISSING|BLOCK_SOURCE_ROUTE_VALUE_BRIDGE_MISSING|P88_PHASE5_REVIEWED_BLOCK_SOURCE_ROUTE_DERIVATIVE_READINESS_CLOSED|source-route full-history analytical derivative readiness|source_route_previous_marginal_log_density|source_route_generate_retained_samples|source_route_sequential_negative_log_physical_density|source_route_run_sequential_fixed_hmc|eval_irt_reference|eval_rt_jac_reference|marginalise|AbstractIRT" docs/plans/bayesfilter-highdim-zhao-cui-p88*.md docs/plans/bayesfilter-highdim-zhao-cui-p89*.md bayesfilter/highdim/source_route.py third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src -g '*.md' -g '*.py' -g '*.m'
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p89*.md
```

Outcomes:

- P89 Phase 3 value-bridge blocker and P88 Phase 5 derivative blocker were
  found.
- Local retained-sample, previous-marginal, sequential scalar, and fixed-HMC
  source-route surfaces were found.
- Author TTSIRT inverse/potential/gradient, map-Jacobian, marginalization, and
  abstract API anchors were found.
- Diff hygiene passed for P89 plan artifacts after this result and the Phase 5
  blocker subplan were written.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `c815edc52162779e969b2982723b2f52770fd849` |
| Worktree status | Dirty pre-existing/research worktree; unrelated dirty work preserved. |
| Execution target | Local document/code/source audit only. |
| CPU/GPU status | No TensorFlow numerical command and no GPU/CUDA command were run. |
| Runtime/HMC status | No derivative implementation, FD validation, HMC, sampler, production benchmark, package/network, or default-policy command was run. |
| Phase 3 upstream fact | `P89_PHASE3_REVIEWED_NO_RUNTIME_VALUE_BRIDGE_BLOCKER_CLOSED` |
| Derivative upstream fact | `P88_PHASE5_REVIEWED_BLOCK_SOURCE_ROUTE_DERIVATIVE_READINESS_CLOSED` |
| Plan | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase4-derivative-design-subplan-2026-06-28.md` |
| Result | `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase4-derivative-design-result-2026-06-28.md` |

## Boundary Notes

- This phase does not implement derivatives.
- Author derivative-capable operations are future design anchors, not a local
  implementation certificate.
- Local fixed-branch score work remains an implementation substrate only.
- Even a future derivative implementation would not establish
  `D18_CORRECTNESS_CANDIDATE` without a same-target source-backed value bridge.

## Phase 5 Handoff

The refreshed Phase 5 subplan is:

- `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase5-derivative-implementation-subplan-2026-06-28.md`

Phase 5 is refreshed as a no-runtime derivative-implementation blocker
closeout. It may preserve blockers and hand off to an FD blocker closeout, but
it must not edit algorithmic code, run runtime checks, implement derivatives,
or claim source-route analytical-gradient readiness.

## Claude Review Status

Bounded read-only Claude Opus max-effort review returned `VERDICT: AGREE`.

Reviewer confirmed this result safely closes Phase 4 as diagnostic derivative
design inventory only, preserves `BLOCK_SOURCE_ROUTE_VALUE_BRIDGE_MISSING` and
the source-route derivative-readiness blocker, avoids value/gradient/FD/HMC/
GPU/production/default-policy overclaims, and hands off only to a no-runtime
Phase 5 derivative-implementation blocker closeout.
