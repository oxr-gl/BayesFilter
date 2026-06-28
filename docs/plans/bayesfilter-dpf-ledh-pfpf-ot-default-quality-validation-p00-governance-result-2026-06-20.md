# P00 Result: Governance, Evidence Contract, And Claude Review

Date: 2026-06-20

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | P00 passed; proceed to P01 paired quality harness implementation. |
| Primary criterion status | Passed after local checks and Claude read-only review convergence. |
| Veto diagnostic status | No remaining plan veto: wrong baseline, proxy-metric promotion, missing stop conditions, stale route context, and unsupported claims were checked. |
| Main uncertainty | This phase produced no filter-quality evidence; it only governs the next executable rung. |
| Next justified action | Implement the paired-seed quality aggregator in P01. |
| What is not concluded | No GPU quality result, no posterior correctness, no HMC readiness, no sampler convergence, no speedup, no statistical superiority, and no target-shape scientific validity. |

## Checks Actually Run

```bash
python -m py_compile docs/benchmarks/compare_experimental_batched_ledh_pfpf_ot_streaming_precision.py
```

```bash
python -c "import pathlib; paths=[...]; missing=[p for p in paths if not pathlib.Path(p).is_file()]; assert not missing, missing"
```

```bash
python -c "import pathlib; paths=[...]; text='\n'.join(pathlib.Path(p).read_text() for p in paths); required=[...]; missing=[r for r in required if r not in text]; assert not missing, missing"
```

## Claude Review

Round 1 returned `VERDICT: REVISE`. Material findings were fixable:

- require explicit preservation and inspection of per-seed/per-output drift
  fields and paired-seed count;
- define the exact drift formula and tolerance semantics;
- specify field-level default precision metadata assertions;
- carry comparator, tolerance, and worst-drift evidence into closeout.

The same plan artifacts were patched visibly. Round 2 returned
`VERDICT: AGREE` and found no remaining material blocker for P01/P02 execution.

## Evidence Contract After Repair

| Field | Contract |
| --- | --- |
| Comparator | Paired FP64 TF32-disabled streaming arm; FP32 TF32-disabled diagnostic arm. |
| Drift formula | `max(abs(candidate - reference) / max(1.0, abs(reference)))` per output array and paired seed. |
| Primary P02 criterion | Default-arm drift `<= 1.0e-2` for `log_likelihood`, `filtered_means`, `filtered_variances`, and `ess_by_time` across three paired seeds after child hard screens pass. |
| Required metadata | `precision_default_policy=production_ledh_pfpf_ot_gpu_tf32`, `default_execution_target=gpu`, `default_algorithm_target=ledh_pfpf_ot_tf32`, `default_target_status=production_default_by_owner_directive`, `default_dtype=float32`, `active_dtype=float32`, `default_tf32_mode=enabled`, `tf32_mode=enabled`, `tf32_execution_enabled=true`. |
| Nonclaims | No posterior correctness, HMC readiness, sampler convergence, speedup, statistical superiority, dense Sinkhorn equivalence, public API readiness, or target-shape scientific validity. |

## Artifacts

- Master program:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-master-program-2026-06-20.md`
- Visible runbook:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-visible-gated-execution-runbook-2026-06-20.md`
- Claude review ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-claude-review-ledger-2026-06-20.md`
- Execution ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-visible-execution-ledger-2026-06-20.md`

## Post-Run Red-Team Note

Strongest alternative explanation: a well-scoped plan can still be defeated by
an implementation bug in the P01 aggregator or by a trusted-GPU environment
failure in P02.

What would overturn P00: discovering that the P01/P02 artifacts do not actually
encode the repaired evidence contract, or that the selected wrapper targets an
obsolete route.

Weakest part of the evidence: Claude review was a plan review only, not an
execution or numerical validation.

