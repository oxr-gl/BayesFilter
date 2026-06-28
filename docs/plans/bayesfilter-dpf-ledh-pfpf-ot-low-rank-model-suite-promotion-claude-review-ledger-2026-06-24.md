# Low-Rank LEDH-PFPF-OT Model-Suite Promotion Claude Review Ledger

Date: 2026-06-24

Status: `P01A_IMPLEMENTATION_PASSED_PENDING_P01B_APPROVAL`

Claude is read-only reviewer only. Claude cannot authorize crossing human,
runtime, model-file, funding, product-capability, default-policy, public API,
HMC, or scientific-claim boundaries.

## Review Entries

### Round 1 - Claude Opus/max - Program/P00/P01 Review - `VERDICT: REVISE`

Command:

```bash
bash /home/ubuntu/python/claudecodex/scripts/claude_worker.sh --cwd /home/ubuntu/python/BayesFilter --name low-rank-model-suite-plan-review-r1 --model opus --effort max --output-format text "<read-only review prompt>"
```

Findings summary:

- Material: P01 exact-Kalman pass/fail gate was not operationalized because
  the case set, seed set, and tolerances were not pinned before runtime.
- Material: P00 did not explicitly vet the concrete P01 exact-Kalman
  harness/validator and could pass without proving the first runtime gate had a
  pinned executable surface.
- Medium: "model-suite engineering default" wording needed tighter scope to
  avoid being read as an actual package/default-policy switch.
- Positive findings: wrong-baseline and proxy-metric risks were mostly fenced;
  runtime/default/API/HMC/scientific boundaries were clearly blocked; P01 did
  require exact Kalman metrics rather than recycling LGSSM-shaped efficiency
  evidence.

Repairs applied:

- Reworded final target from "model-suite engineering default" to bounded
  internal "model-suite engineering recommendation" and explicitly forbade
  interpreting it as a package-level or public default switch.
- Added pinned P01 LGSSM case IDs, dimensions, time steps, particles, seeds,
  and exact-Kalman tolerance screens before runtime.
- Added P00 executable-surface audit requiring a concrete P01 exact-Kalman
  harness/validator or a refreshed harness-implementation-before-runtime
  subplan.
- Added P01 preferred harness/test artifact paths and stop/handoff conditions
  for missing harness implementation.

Next action:

- Rerun focused local document checks and Claude review round 2.

### Round 2 - Claude Opus/max - Focused Repair Review - `VERDICT: AGREE`

Command:

```bash
bash /home/ubuntu/python/claudecodex/scripts/claude_worker.sh --cwd /home/ubuntu/python/BayesFilter --name low-rank-model-suite-plan-review-r2 --model opus --effort max --output-format text "<focused read-only repair review prompt>"
```

Findings summary:

- Cleared: P01 now pins exact-Kalman case IDs, dimensions, particle counts,
  seeds, and tolerances before runtime.
- Cleared: P00 now requires concrete P01 harness/validator audit or a refreshed
  implementation-before-runtime subplan before P01 runtime.
- Cleared: final-decision wording is bounded to an internal engineering
  recommendation and blocks package/public default-switch interpretation.
- Cleared: wrong-baseline, proxy-metric, stop-condition, environment,
  unsupported-claim, and repair-loop controls are aligned across reviewed
  artifacts.
- Minor watch item, not a blocker: P00 must ensure the P01 case IDs map to
  concrete fixture definitions before P01 runtime.

Verdict:

- `VERDICT: AGREE`

### Round 3 - Claude Opus/max - P00 Result / P01 Refresh Review - `VERDICT: REVISE`

Command:

```bash
bash /home/ubuntu/python/claudecodex/scripts/claude_worker.sh --cwd /home/ubuntu/python/BayesFilter --name low-rank-model-suite-p01-refresh-review-r1 --model opus --effort max --output-format text "<focused read-only P00/P01 refresh review prompt>"
```

Findings summary:

- Material: P01 handoff still allowed P02 continuation if P01 trusted-GPU
  runtime did not happen but a reviewed blocker was written. This conflicted
  with the master-program hard-gate contract. Repair required blocker-only
  outcomes to stop at P01, allowing only a non-executable P02 draft refresh.
- Minor: visible execution ledger status header was stale.
- Minor: P00 run manifest did not record the git commit.

Repairs applied:

- P01 handoff now requires P01 trusted-GPU runtime completion for P02 handoff.
  Runtime unavailable/unapproved/blocked outcomes must write a blocker result
  and stop at P01. Any P02 draft in that case must be labeled
  `P02_DRAFT_NO_EXECUTION_AUTHORIZED`.
- Visible execution ledger status changed to
  `P01_IMPLEMENTATION_REFRESH_UNDER_REVIEW`.
- P00 run manifest records git commit
  `01213338c7037c468f38b01d013e4ce13526c9e4` while preserving the dirty
  worktree caveat.

Next action:

- Rerun focused local checks and Claude read-only review round 4 on the P01
  repair.

### Round 4 - Claude Opus/max - Focused P01 Repair Review - `VERDICT: REVISE`

Command:

```bash
bash /home/ubuntu/python/claudecodex/scripts/claude_worker.sh --cwd /home/ubuntu/python/BayesFilter --name low-rank-model-suite-p01-refresh-review-r2 --model opus --effort max --output-format text "<focused read-only repair review prompt>"
```

Findings summary:

- The prior P02 handoff bug was substantively repaired.
- Material traceability/artifact issue: the review ledger still had stale
  top-level convergence status and had not yet recorded a converged review of
  the repaired P01.
- Material artifact-contract issue: P01 listed runtime JSON, Markdown, and log
  artifacts as unconditionally required, while the plan also had a valid
  stop-at-P01 blocker path before runtime. The artifact contract needed to
  split P01A/blocker outputs from P01B runtime outputs.
- Minor: master-program status was stale relative to the execution ledger.

Repairs applied:

- P01 required artifacts are now split into always-required P01A artifacts,
  blocker-path artifacts, and P01B-runtime-only artifacts.
- P01 evidence contract now states the conditional artifact contract.
- Master-program status changed to `P01_IMPLEMENTATION_REFRESH_UNDER_REVIEW`.
- Claude review ledger status changed to
  `P01_IMPLEMENTATION_REFRESH_UNDER_REVIEW`.

Next action:

- Rerun focused local checks and Claude read-only review round 5 on the split
  artifact contract and status traceability.

### Round 5 - Claude Opus/max - Focused P01 Artifact Contract Review - `VERDICT: AGREE`

Command:

```bash
bash /home/ubuntu/python/claudecodex/scripts/claude_worker.sh --cwd /home/ubuntu/python/BayesFilter --name low-rank-model-suite-p01-refresh-review-r3 --model opus --effort max --output-format text "<focused read-only artifact-contract review prompt>"
```

Findings summary:

- Cleared: prior conditional-artifact defect is repaired. P01 now splits
  always-required P01A outputs, blocker-path outputs, and runtime-only outputs.
- Cleared: prior P02 handoff boundary is repaired. Executable handoff requires
  completed P01A, explicit trusted-GPU approval after P01A, completed P01
  runtime, written P01 result, validator pass, and review agreement.
- Cleared: blocked/unapproved runtime stops at P01; any P02 document in that
  path must be `P02_DRAFT_NO_EXECUTION_AUTHORIZED`.
- Cleared: status traceability is aligned across master program, review
  ledger, and execution ledger.
- Residual watch item: if P01A requires any support edit outside the new
  harness/test and plan/result/ledger artifacts, treat it as a visible scoped
  P01A repair instead of silently expanding the write set.
- Residual watch item: master phase index still lists the canonical P01 runtime
  result; remember during execution that the P01A implementation result and
  blocker result carry pre-runtime control weight.

Verdict:

- `VERDICT: AGREE`

Next action:

- Proceed to P01A harness implementation within the reviewed narrow write set.

### P01A Implementation Local-Check Note - No Material Claude Rerun Required

Codex implemented the reviewed P01A write set:

- `docs/benchmarks/benchmark_low_rank_ledh_lgssm_kalman_gate.py`
- `tests/test_low_rank_ledh_lgssm_kalman_gate.py`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p01-lgssm-kalman-implementation-result-2026-06-24.md`

Local checks passed:

- compile check passed;
- focused pytest passed, `3 passed`;
- no NumPy imports or `np.` references were found in the new harness/test;
- `.numpy()` hits are reporting/materialization helpers outside the TensorFlow
  route core.

The only test failure encountered was a reporting-only JSON serialization bug;
it was patched in the same harness and the focused tests passed on rerun. This
did not alter phase boundaries, runtime approval, pass/fail criteria, or the
reviewed write set, so no additional material Claude review was required before
asking for P01B trusted-GPU approval.

### Round 6 - Claude Opus/max - P01 Result Stop Review - `VERDICT: AGREE`

Command:

```bash
bash /home/ubuntu/python/claudecodex/scripts/claude_worker.sh --cwd /home/ubuntu/python/BayesFilter --name low-rank-model-suite-p01-result-review-r1 --model opus --effort max --output-format text "<focused read-only P01 result stop review prompt>"
```

Findings summary:

- Cleared: stopping at P01 rather than executing P02 is consistent with the
  master-program hard-gate contract and the P01 handoff conditions.
- Cleared: the result separates route-diagnostic/tuning failure from Kalman
  quality failure and broad algorithm rejection.
- Cleared: the all-in-one command-pattern defect is treated as a non-candidate
  execution defect, while row-level trusted-GPU artifacts are used as evidence.
- Cleared: no material wrong-baseline, proxy-metric, unsupported-claim,
  artifact-mismatch, or boundary-safety issue was found.
- Residual readability risk: the P01 subplan explicitly discusses exact-Kalman
  quality failure continuation but not route/provenance failure in the same
  paragraph; the master program covers route/provenance failure as a promotion
  veto.
- Residual traceability risk: the markdown result summarizes row commands,
  while exact row commands are preserved in JSON run manifests.

Verdict:

- `VERDICT: AGREE`

Next action:

- Do not execute P02-P07 under this promotion run. Prepare P08 closeout or a
  separate focused repair plan for the low-rank projection residual.
