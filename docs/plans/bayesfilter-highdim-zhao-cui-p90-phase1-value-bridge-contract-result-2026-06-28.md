# P90 Phase 1 Result: Same-Target Value Bridge Contract

Date: 2026-06-28

Status: `P90_PHASE1_REVIEWED_VALUE_BRIDGE_CONTRACT_CLOSED`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Phase 1 locally designs an admissible same-target value bridge contract: author-formula replay for the exact P89/P90 Zhao-Cui SIR d18 source-route scalar. |
| Primary criterion status | Met locally pending review: the contract names exact scalar, source anchors, branch/retained identity, setup-static fields, deterministic cases, pinned tolerances, fail-closed rules, and Phase 2/3 boundaries. |
| Veto diagnostic status | No bridge execution, runtime command, algorithmic code edit, proxy-correctness claim, value-correctness claim, derivative/FD/HMC/GPU/package/default-policy command, or blocker weakening occurred. |
| Main uncertainty | Phase 2 must still implement the independent author-formula helper and fail-closed tests; Phase 3 must still execute the bridge. |
| Next justified action | Review the bridge contract, this Phase 1 result, and refreshed Phase 2 implementation subplan. If all agree, Phase 2 may implement the bridge. |
| What is not being concluded | No value correctness, source-route correctness, analytical-gradient correctness, FD validation, HMC readiness, GPU/XLA readiness, production readiness, packaging readiness, or default-policy change. |

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can P90 specify an admissible same-target source-backed value bridge for the exact Zhao-Cui SIR d18 scalar? |
| Baseline/comparator | P89 target manifest, P89 missing-bridge blocker, local source-route value mechanics, and author source anchors. |
| Primary criterion | Passed locally pending review: the bridge contract specifies exact scalar, reference route, source anchors, branch/retained identity, setup-static fields, parameterization, deterministic cases, tolerances, and fail-closed rules. |
| Veto diagnostics | Passed locally: no wrong-target bridge, proxy correctness, missing tolerance, missing retained/branch binding, runtime execution, or unsupported source-faithful claim was accepted. |
| Explanatory diagnostics | Source inventory over P89/P90 artifacts, local source-route scalar/marginal surfaces, and author `full_sol`, `eval_irt_reference`, `marginalise`, and `AbstractIRT` anchors. |
| Not concluded | No value correctness until Phase 2 implementation and Phase 3 execution pass. |
| Artifact | Bridge contract, this Phase 1 result, and refreshed Phase 2 subplan. |

## Skeptical Audit Result

| Risk Checked | Result |
| --- | --- |
| Wrong baseline | Avoided. The contract uses the P89 target scalar, not UKF, LEDH, all-grid, rank/degree, or another lower-rung route. |
| Proxy metrics promoted | Avoided. Proxy diagnostics are explicitly forbidden bridge substitutes. |
| Missing stop conditions | Avoided. The contract blocks if the independent helper collapses to the same production call path or cannot bind previous retained branch identity. |
| Unfair comparison | Avoided by requiring same scalar, branch, retained object, setup-static fields, parameterization, and tolerances. |
| Hidden assumptions | Exposed. The bridge is an author-formula replay comparator, not a production/scientific readiness claim. |
| Stale context | P89 missing-bridge blocker is treated as open until Phase 2/3 pass. |
| Environment mismatch | No runtime command was run; Phase 1 is design-only. |
| Artifact usefulness | The contract gives Phase 2 exact implementation requirements and Phase 3 exact pass/fail criteria. |

## Bridge Contract Summary

The bridge contract is:

- `docs/plans/bayesfilter-highdim-zhao-cui-p90-value-bridge-contract-2026-06-28.md`

Core idea:

```text
local source-route scalar
  source_route_sequential_negative_log_physical_density(...)

versus

independent author-formula replay scalar
  - prior_or_previous_log_density
  - transition_log_density
  - likelihood_log_density
```

The independent replay helper must not call the production scalar or previous
marginal helper internally. It must implement the `t=1` prior formula and
the `t>1` previous-retained marginal formula as separate bridge logic,
anchored to the author `full_sol.reapprox` and TTSIRT marginal/eval-pdf
operations.

## Local Checks

Commands:

```bash
rg -n "target_id|same-scalar|branch identity|retained object|source_route_sequential_negative_log_physical_density|source_route_previous_marginal_log_density|source_route_generate_retained_samples|eval_pdf|eval_irt_reference|eval_rt_jac_reference|marginalise|full_sol|tolerance|BLOCK_SOURCE_ROUTE_VALUE_BRIDGE_MISSING" docs/plans/bayesfilter-highdim-zhao-cui-p89*.md docs/plans/bayesfilter-highdim-zhao-cui-p90*.md bayesfilter/highdim/source_route.py third_party/audit/zhao_cui_tensor_ssm_p10/source -g '*.md' -g '*.py' -g '*.m'
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p90*.md
```

Outcomes:

- Local source-route scalar, retained-sample, previous-marginal, branch
  identity, and retained-object surfaces were found.
- Author `full_sol` prior/transition/likelihood, TTSIRT `eval_irt_reference`,
  marginalization, and `eval_pdf` anchors were found.
- P89 missing-bridge blocker remains visible and is not treated as closed by
  Phase 1 alone.
- P90 artifact diff hygiene passed after contract/result/subplan updates.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `c815edc52162779e969b2982723b2f52770fd849` |
| Worktree status | Dirty pre-existing/research worktree; unrelated dirty work preserved. |
| Execution target | Local document/code/source-surface design only. |
| CPU/GPU status | No TensorFlow numerical command and no GPU/CUDA command were run. |
| Runtime/HMC status | No runtime, bridge execution, FD, HMC, sampler, package/network, production benchmark, release, CI, or default-policy command was run. |
| Plan | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase1-value-bridge-contract-subplan-2026-06-28.md` |
| Bridge contract | `docs/plans/bayesfilter-highdim-zhao-cui-p90-value-bridge-contract-2026-06-28.md` |
| Result | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase1-value-bridge-contract-result-2026-06-28.md` |

## Boundary Notes

- Phase 1 does not claim value correctness.
- Phase 1 does not close `D18_CORRECTNESS_CANDIDATE`.
- Phase 1 does not implement or execute the bridge.
- Phase 1 does not authorize derivative implementation, FD, HMC, GPU/XLA,
  packaging, CI, release, production, or default-policy work.

## Phase 2 Handoff

Phase 2 may start because Claude review agreed on:

- bridge contract;
- this Phase 1 result;
- refreshed Phase 2 implementation subplan.

Phase 2 should implement the independent author-formula replay helper and
fail-closed tests required by the bridge contract. If it cannot do so without
calling the same production scalar path or drifting from the target, Phase 2
must write a blocker rather than execute Phase 3.

## Claude Review Status

Bounded read-only Claude Opus max-effort reviews returned:

- bridge contract: `VERDICT: AGREE`;
- Phase 1 result: `VERDICT: AGREE`;
- Phase 2 implementation subplan: `VERDICT: AGREE` on the narrowed retry after
  a prompt-stall/probe cycle.
