# P65 Claude Review Ledger

metadata_date: 2026-06-14
status: STARTED
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p65-fixed-branch-rank-capacity-master-program-2026-06-14.md
reviewer: Claude Opus max effort, read-only and bounded

## Review Protocol

Claude is read-only.  Prompts must use bounded excerpts or exact line spans and
must not ask Claude to execute commands, edit files, launch agents, or authorize
scientific/product/runtime boundary crossings.

If a review prompt stalls, Codex runs a tiny read-only probe.  If the probe
responds, the stalled prompt is treated as too large or malformed and must be
redesigned.  Stop after five rounds for the same material blocker.

## Reviews

### 2026-06-14 - Phase 0 plan review R1

Command:

```bash
bash scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter \
  --name p65-phase0-plan-review-r1-20260614 --model opus --effort max \
  "<bounded read-only plan review prompt>"
```

Result: `VERDICT: REVISE`.

Accepted findings:

- Phase 0 baseline probe used shorthand defaults instead of the full pinned P64
  comparator tuple.
- Phase 0 probe did not print the exact high defensive-only gate fields.
- Runbook forbade nested/detached agents without explicitly allowing the
  intended foreground bounded read-only Claude reviewer path.
- Phase 0 allowed ambiguous acceptance instead of requiring final
  `VERDICT: AGREE`.
- Phase 1 retained-sample ladder did not predeclare how infeasible rows are
  separated from evidence.

Resolution: patched the master program, Phase 0 subplan, Phase 1 subplan, and
visible runbook.  R2 review required before Phase 0 execution.

### 2026-06-14 - Phase 0 plan review R2

Command:

```bash
bash scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter \
  --name p65-phase0-plan-review-r2-20260614 --model opus --effort max \
  "<bounded read-only R1-repair verification prompt>"
```

Result: `VERDICT: AGREE`.

Findings:

- Full pinned P64 tuple is now explicit in the Phase 0 evidence contract and
  JSON probe command.
- The Phase 0 probe prints blockers, high defensive-only steps, high fitted
  square-root normalizers, and the full normalizer decomposition.
- The runbook now forbids detached/autonomous agents while allowing only the
  foreground bounded read-only Claude worker review path.
- Phase 0 now requires final `VERDICT: AGREE`.
- Phase 1 separates infeasible retained-sample rows from evidence.

Resolution: Phase 0 may launch.

### 2026-06-14 - Phase 1 subplan review R1

Command:

```bash
bash scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter \
  --name p65-phase1-subplan-review-r1-20260614 --model opus --effort max \
  "<bounded read-only Phase 1 launch review prompt>"
```

Result: `VERDICT: AGREE`.

Findings:

- No wrong-baseline drift: Phase 1 inherits the exact Phase 0/P64 tuple and
  reproduced symptoms.
- The subplan does not promote high nonzero square-root mass into a bug-fix
  criterion.
- It separates infeasible rows from evidence and preserves target/order/axis,
  defensive `tau`, and thresholds.
- Caution: the degree/rank family must be interpreted only as a tuple-level
  screen, not as isolated evidence for degree alone or rank alone.

Resolution: Phase 1 may launch with the tuple-level caution recorded.

### 2026-06-14 - Phase 1 result review R1

Command:

```bash
bash scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter \
  --name p65-phase1-result-review-r1-20260614 --model opus --effort max \
  "<bounded read-only Phase 1 result interpretation review prompt>"
```

Result: `VERDICT: REVISE`.

Accepted findings:

- The observed blocker `BLOCK_P65_HIGH_RANK_FIXED_ALS_ZERO_SQRT_TT` is supported
  as a failure signature.
- The result correctly avoids treating untested larger fit-data rows as negative
  evidence.
- The degree/rank tuple caution is preserved.
- Phase 2 must not launch as currently written.
- One mechanism sentence overclaimed by implying that an underdetermined ridge
  solve caused the zero square-root TT; Phase 1 supports that only as a
  hypothesis.
- Safest next boundary is stop for human direction; an admissibility guard,
  stabilization plan, or larger diagnostic plan would be a new scoped choice.

Resolution: patched the Phase 1 result to describe the ALS cause as a hypothesis
and to make the stop-for-human-direction boundary explicit.  R2 focused review
required.

### 2026-06-14 - Phase 1 result review R2

Command:

```bash
bash scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter \
  --name p65-phase1-result-review-r2-20260614 --model opus --effort max \
  "<bounded read-only focused R2 review prompt>"
```

Result: `VERDICT: AGREE`.

Findings:

- The Phase 1 result now limits the evidence to the observed zero/near-zero
  high-rank fitted square-root TT failure signature.
- The ALS cause is explicitly labeled as a hypothesis, not a proved mechanism.
- The Phase 2 handoff explicitly says not to launch the existing Phase 2 subplan
  and that the safest boundary is stop for human direction.

Resolution: Phase 1 result review converged.

### 2026-06-15 - Planning error correction review R1

Command:

```bash
bash scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter \
  --name p65-planning-error-correction-review-r1-20260615 --model opus --effort max \
  "<bounded read-only planning-error correction review prompt>"
```

Result: `VERDICT: REVISE`.

Accepted findings:

- The correction now properly separates the repair target from the unproved
  causal mechanism.
- The refreshed Phase 2 subplan is correctly framed as a bounded
  repair-mechanism phase for `BLOCK_P65_HIGH_RANK_FIXED_ALS_ZERO_SQRT_TT`.
- Guard-only changes are correctly blocked from being called a high-branch
  repair.
- Source, `tau`, threshold, target-order, and axis invariants are protected.
- Material remaining issue 1: stabilization route must restore the Phase 1
  requirement for mathematical documentation and paper/source anchors before a
  behavior-changing patch.
- Material remaining issue 2: branch-substitution/admissibility outcomes must
  not be presented as repairing the failing high-rank branch.

Resolution: patched the Phase 2 subplan to require mathematical/source-anchor
documentation before behavior-changing stabilization and to classify branch
substitution as adaptation/blocker unless the original promoted high branch is
actually repaired.  R2 focused review required.

### 2026-06-15 - Planning error correction review R2

Command:

```bash
bash scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter \
  --name p65-planning-error-correction-review-r2-20260615 --model opus --effort max \
  "<bounded read-only focused R2 review prompt>"
```

Result: `VERDICT: AGREE`.

Findings:

- Behavior-changing stabilization now requires mathematical/source documentation
  or explicit `fixed_hmc_adaptation` / `extension_or_invention` classification
  before implementation.
- Branch substitution is now explicitly barred from being described as repairing
  the failing high-rank branch unless the original promoted high branch itself
  is repaired under the declared comparison target.

Resolution: planning-error correction converged.

### 2026-06-15 - Phase 2 P50 stabilization documentation review R1

Command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name p65-phase2-p50-stabilization-review-r1-20260615 \
  --model opus --effort max \
  "<bounded read-only derivation/source-anchor/readability review prompt>"
```

Result: `VERDICT: REVISE`.

Accepted findings:

- The two new propositions were mathematically sound in the stated fixed-ALS
  setting:
  `prop:p50-zero-environment-cascade` and
  `prop:p50-constant-path-initialization`.
- The prose correctly classified the stabilization as a fixed-branch adaptation,
  not an unqualified source-faithful Zhao--Cui operation.
- The text was acceptable human-facing monograph prose.
- Material blocker: one source-anchor sentence overclaimed that
  `@TTSIRT/marginalise.m:81--85` itself adds defensive mass.  The bounded source
  span only proved the squared approximation mass and total-normalizer update;
  the defensive parameter storage is in the shared `SIRT` constructor.
- Suggested improvement: mention the ESS-dependent coordinate stretch in
  `computeL.m:31--47`.

Resolution: patched the P50 source-anchor paragraph to split the `SIRT` and
`TTSIRT.marginalise` responsibilities and to mention the coordinate stretch.
R2 focused review required.

### 2026-06-15 - Phase 2 P50 stabilization documentation review R2

Command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name p65-phase2-p50-stabilization-review-r2-20260615 \
  --model opus --effort max \
  "<bounded read-only focused R2 source-anchor review prompt>"
```

Result: `VERDICT: AGREE`.

Findings:

- The defensive-mass/source-anchor overclaim is fixed.
- The added `computeL` coordinate-stretch detail is accurate.
- No new overclaim was found in the bounded prose.
- The documentation gate is adequate for a small behavior-changing
  fixed-branch adaptation patch, subject to branch identity recording and
  tests.

### 2026-06-15 - Phase 2 implementation review R1

Command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name p65-phase2-implementation-review-r1-20260615 \
  --model opus --effort max \
  "<bounded read-only implementation review prompt>"
```

Result: `VERDICT: AGREE`.

Findings:

- The implementation satisfies the Phase 2 repair target on the bounded record:
  it changes the fixed-branch initialization, not the target/order/axes,
  source-pushed fit-data route, or P60 thresholds.
- The explicit metadata
  `fixed_branch_adaptation_class=fixed_hmc_adaptation` and
  `fit_initialization_rule=fixed_hmc_constant_path_weighted_mean` is sufficient
  to avoid an unqualified source-faithfulness claim, provided downstream
  writeups preserve that boundary.
- The compile, focused P59/P60 pytest run, and JSON probe are sufficient for
  Phase 2 handoff only.
- The residual P60 threshold blockers are real Phase 3 work:
  `log_marginal_delta_threshold_exceeded` and
  `normalizer_increment_delta_threshold_exceeded`.

Resolution: Phase 2 implementation review converged; write the Phase 2 result
and refresh Phase 3 around threshold-closeout evidence without claiming d=18
correctness.

### 2026-06-15 - Phase 3 closeout review R1

Command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name p65-phase3-closeout-review-r1-20260615 \
  --model opus --effort max \
  "<bounded read-only Phase 3 closeout review prompt>"
```

Result: `VERDICT: AGREE`.

Findings:

- The Phase 2 and Phase 3 statuses are logically consistent with the evidence:
  the high-rank zero-TT failure is repaired, while the P60 quantitative
  threshold blockers remain.
- The closeout avoids overclaiming source-faithful Zhao--Cui parity, d=18
  correctness, full P60 rank-convergence pass, threshold success, or HMC
  readiness.
- The residual blockers are explicit enough for a future plan: failing criteria,
  magnitudes, source-route invariants, adaptation metadata, and CPU-only test
  context are preserved.
- No material patch is required before stopping the visible runbook.

Resolution: Phase 3 closeout review converged.

Resolution: Phase 2 may proceed to the small reviewed implementation patch.
