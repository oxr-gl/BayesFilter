# P12E-1 Subplan: Diagnostic Implementation

Date: 2026-06-19
Master program:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-ledh-sparse-locality-screen-master-program-2026-06-19.md`

## Phase Objective

Implement the lane-owned P12E LEDH sparse-locality diagnostic script.  The
script must generate deterministic LEDH-like fixtures, compute dense transport
locality and truncation diagnostics, and write JSON/Markdown artifacts.

This phase writes code only.  It may run syntax/import checks, but it does not
run the smoke or official diagnostic.

## Entry Conditions Inherited From Previous Phase

- P12E-0 result records pass.
- Current-agent status records `FIRST_CHECKS_RUN`.
- The Phase 8 diagnostic context compiles.
- CPU-scoped `ledh_flow_batch_tf` import check passed.
- No shared-contract blocker is open.

## Required Artifacts

- This subplan.
- Diagnostic script:
  `docs/benchmarks/scalable_ot_p12e_ledh_sparse_locality_screen.py`
- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-p1-diagnostic-implementation-result-2026-06-19.md`
- Updated lane status.
- Next subplan, refreshed if needed:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-p2-smoke-diagnostic-subplan-2026-06-19.md`

## Required Checks, Tests, And Reviews

Local checks after implementation:

```bash
python -m py_compile docs/benchmarks/scalable_ot_p12e_ledh_sparse_locality_screen.py
CUDA_VISIBLE_DEVICES=-1 python -c "import docs.benchmarks.scalable_ot_p12e_ledh_sparse_locality_screen as m; print(m.__name__)"
```

Review:

- Codex skeptical audit before implementation.
- Claude read-only review is material for this phase because implementation
  may affect evidence, boundaries, and claims.
- Claude prompt must use a concise review packet and targeted snippets/diff,
  not the whole file pasted into the prompt.
- If Claude returns `REVISE`, patch the same script/subplan/result visibly and
  rerun focused checks.  Stop after five rounds for the same blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the lane-owned diagnostic script implement the reviewed P12E fixture/provenance, locality-threshold, truncation, and non-claim contract without executing the diagnostic? |
| Baseline/comparator | Reviewed P12E master/subplan and read-only Phase 8 locality semantics. |
| Primary pass criterion | Script compiles/imports CPU-scoped and code review confirms fixture provenance, CPU import ordering, Phase 8 orientation/truncation semantics, diagnostic roles, and non-claims are represented. |
| Veto diagnostics | TensorFlow import before CPU hiding; missing deterministic fixture provenance; missing stable content digests; missing threshold roles; sparse solver implementation; external solver/package/network/GPU need; shared-file edit need. |
| Explanatory diagnostics | Static code structure and review comments. |
| Not concluded | No diagnostic result, no sparse locality pass/fail, no solver validity, no speedup/ranking/posterior/default/HMC/API readiness. |
| Artifact preserving result | Script, P1 result note, and Claude review ledger entry. |

## Forbidden Claims And Actions

- Do not run smoke or official diagnostics in this phase.
- Do not implement a sparse solver.
- Do not run POT, C++, external sparse solvers, package installs, network
  fetches, or GPU evidence.
- Do not edit Phase 1, Phase 3, Phase 8, peer-agent, shared ledger,
  shared stop-handoff, public API, or default-policy files.
- Do not claim locality pass/fail before P12E-2/P12E-3 artifacts exist.

## Exact Next-Phase Handoff Conditions

P12E-2 may begin only if:

- diagnostic script exists;
- required local checks pass;
- P1 result note exists;
- material Claude review converges to `VERDICT: AGREE`;
- current-agent status records implementation completion;
- P12E-2 subplan exists and has passed Codex consistency review.

## Stop Conditions

Stop and write P1 blocker result if:

- CPU import ordering cannot be preserved;
- fixture provenance cannot be made deterministic;
- Phase 8 orientation/truncation semantics cannot be preserved;
- implementation requires shared-file edits or prohibited external actions;
- Claude/Codex do not converge after five review rounds for the same material
  blocker.

## End-Of-Phase Checklist

1. Run required local checks.
2. Write the P1 result/close record.
3. Draft or refresh the P12E-2 subplan.
4. Review the P12E-2 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
