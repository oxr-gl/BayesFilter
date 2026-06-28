# Nystrom Algorithm-Complete Final Result

Date: 2026-06-22T02:06:37+08:00

Status: `LEADERBOARD_READY_DIAGNOSTIC_CANDIDATE`

## Final Decision

Fixed-rank Nystrom kernel Sinkhorn is ready to enter a future scalable-OT
screening leaderboard as a real diagnostic candidate.

This decision means the lane now has an executable harness, focused tests,
small dense-reference checks, downstream LEDH smoke evidence, and a bounded
trusted-GPU operational envelope. It does not select Nystrom as a default,
rank it against other candidates, or certify scientific/posterior correctness.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Passed: Nystrom is ready for later leaderboard screening as a diagnostic candidate. |
| Baseline/comparator | P02 dense small-reference, P03 downstream smoke, and P04 GPU scale envelope. |
| Primary criterion | Passed: P01-P04 results exist, completed benchmark JSON artifacts parse, hard vetoes are empty for P02-P04, and this result preserves claim boundaries. |
| Veto diagnostics | No missing phase result, no failed benchmark JSON parse, no unsupported default/ranking/posterior/HMC/API claim found in local closeout checks, and the final Claude closeout review converged after bookkeeping repair. |
| Explanatory diagnostics | Runtime, memory proxy, dense-reference errors, selected ranks, optional GPU row, TF32/device metadata. |
| Not concluded | No final algorithm ranking, production/default readiness, posterior correctness, HMC readiness, public API readiness, statistical superiority, or broad large-N guarantee. |

## Phase Summary

| Phase | Status | Key evidence | Main nonclaim |
| --- | --- | --- | --- |
| P00 governance/source lock | `PASSED` | Plan/runbook/subplans reviewed; Claude R2 `VERDICT: AGREE` | No default/product/scientific claim |
| P01 harness | `PASSED` | Harness/tests created; compile passed; focused tests `8 passed` | Harness existence only |
| P02 small reference | `PASSED` | Top-level hard vetoes `[]`; `14 / 15` rows passed; each required fixture had viable ranks | No large-N, speedup, or posterior claim |
| P03 downstream smoke | `PASSED` | Two CPU LEDH smoke rows passed; ESS/log-weight/residual gates passed | No posterior validation or ranking |
| P04 trusted GPU scale | `PASSED` | GPU1 selected; required rows and optional `N=16384` row passed; TF32 enabled and GPU evidence recorded | No statistical speedup or default readiness |

## Selected Evidence

| Metric | Value |
| --- | ---: |
| P02 hard vetoes | `[]` |
| P02 viable ranks, `tiny_manual` | `2, 3, 4` |
| P02 viable ranks, `small_parity` | `2, 4, 8` |
| P02 viable ranks, `high_dim_low_rank` | `4, 8, 16, 32` |
| P02 viable ranks, `ledh_specific_smoke` | `4, 8, 16, 32` |
| P03 max row residual | `2.8744214464193618e-05` |
| P03 min ESS fraction | `0.9999939940500705` |
| P04 selected physical GPU | `1` |
| P04 rows passed | `4 / 4` |
| P04 max row residual | `3.540515899658203e-05` |
| P04 min ESS fraction | `0.9999862909317017` |
| P04 TF32 recorded enabled | `True` |

One P02 row-level diagnostic miss remains: `high_dim_low_rank` rank `2`
exceeded the dense max-error threshold. This does not block closeout because the
P02 gate was fixture-level and `high_dim_low_rank` had viable planned ranks.

## Artifact Manifest

| Artifact | Path |
| --- | --- |
| Harness | `docs/benchmarks/scalable_ot_nystrom_ledh_pfpf_algorithm_complete.py` |
| Focused tests | `tests/test_nystrom_ledh_pfpf_algorithm_complete.py` |
| P01 result | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p01-implementation-harness-result-2026-06-21.md` |
| P02 JSON | `docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p02-small-reference-2026-06-21.json` |
| P02 Markdown | `docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p02-small-reference-2026-06-21.md` |
| P02 log | `docs/benchmarks/logs/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p02-small-reference-2026-06-21.log` |
| P02 result | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p02-small-reference-result-2026-06-21.md` |
| P03 JSON | `docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p03-downstream-smoke-2026-06-21.json` |
| P03 Markdown | `docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p03-downstream-smoke-2026-06-21.md` |
| P03 log | `docs/benchmarks/logs/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p03-downstream-smoke-2026-06-21.log` |
| P03 result | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p03-downstream-smoke-result-2026-06-21.md` |
| P04 JSON | `docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p04-gpu-scale-2026-06-21.json` |
| P04 Markdown | `docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p04-gpu-scale-2026-06-21.md` |
| P04 log | `docs/benchmarks/logs/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p04-gpu-scale-2026-06-21.log` |
| P04 result | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p04-gpu-scale-result-2026-06-21.md` |
| Execution ledger | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-visible-execution-ledger-2026-06-21.md` |
| Stop handoff | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-visible-stop-handoff-2026-06-21.md` |
| Review ledger | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-claude-review-ledger-2026-06-21.md` |

## Local Closeout Checks

| Check | Status | Evidence |
| --- | --- | --- |
| Artifact existence | `PASS` | P02-P04 JSON artifacts exist. |
| JSON parse | `PASS` | P02, P03, and P04 JSON artifacts parse and report `PASS` with zero hard vetoes. |
| Claim-boundary scan | `PASS` | Local scan found nonclaim/not-concluded wording and forbidden-claim lists only, not unsupported positive claims. |
| Final Claude closeout review | `PASS_AFTER_REPAIR` | R3-R5 returned bookkeeping-only `VERDICT: REVISE` findings; Codex repaired final-result/review-ledger/execution-ledger state, recorded each review, and closed the review ledger. |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Mark Nystrom as leaderboard-ready diagnostic candidate | `PASS` | No local veto; final Claude review converged after bookkeeping repair | Later leaderboard must compare candidates under its own baseline ladder and uncertainty rules | Start a separate screening-leaderboard program only if explicitly requested | No ranking, speedup, posterior correctness, HMC readiness, public API readiness, production/default readiness, or statistical superiority |

## Inference Status

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for P02-P04. |
| Statistically supported ranking | Not evaluated; no ranking is supported. |
| Descriptive-only differences | Runtime, memory, and row-level dense-reference magnitudes are descriptive only. |
| Default-readiness | Not established and not requested. |
| Next evidence needed | A separate governed screening leaderboard with common baselines, uncertainty handling, and predeclared promotion criteria. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `5ea363e594516be236ca7c78ab2067b28a5b6eb5` |
| Commands | P01 compile/tests; P02/P03 CPU exact commands; P04 trusted `nvidia-smi` preflight and exact GPU command. |
| Environment | TensorFlow/TFP harness; P02/P03 CPU-hidden; P04 trusted GPU with `CUDA_VISIBLE_DEVICES=1`. |
| CPU/GPU status | P02/P03 CPU only; P04 physical GPU1 selected by predeclared rule. |
| Seeds | Harness default seed `20260621`. |
| Wall time | P02 `2.0806500411126763` s, P03 `0.32868878194130957` s, P04 `12.462970233988017` s in recorded JSON artifacts. |
| Data version | N/A; deterministic synthetic fixtures. |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-master-program-2026-06-21.md` |
| Result file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-result-2026-06-21.md` |

## Post-Run Red-Team Note

Strongest alternative explanation: these fixtures and rows may be too benign to
predict behavior on harder filtering problems or under a fair multi-candidate
leaderboard. P02-P04 show operational viability under predeclared gates, not
algorithmic superiority.

Result that would overturn this closeout: a reproduced artifact parse failure,
missing hard-veto field, evidence that candidate dense matrices were
materialized, wrong GPU selection, or an unsupported positive claim in the final
result/review ledger.

Weakest part of the evidence: no uncertainty analysis or cross-candidate
comparison exists, so no ranking or speedup claim is defensible.
