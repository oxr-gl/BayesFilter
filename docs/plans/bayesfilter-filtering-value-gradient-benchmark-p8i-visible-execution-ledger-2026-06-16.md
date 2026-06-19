# P8i Visible Execution Ledger

Date: 2026-06-16

Status: `P8I_CLOSED_REVIEWED`

## Program

- Master program: `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-remaining-gap-master-program-2026-06-16.md`
- Runbook: `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-visible-gated-execution-runbook-2026-06-16.md`
- Claude review ledger: `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-claude-review-ledger-2026-06-16.md`
- Stop handoff: `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-visible-stop-handoff-2026-06-16.md`

## Ledger

### 2026-06-16 - Program Bootstrap - PRECHECK

Evidence contract:

- Question: create a reviewed visible gated program for P8h remaining-gap
  closure.
- Baseline/comparator: closed P8h Phase 10/11 boundary and P8h Phase 5-8
  reviewed artifacts.
- Primary criterion: master/runbook/subplans exist, pass local checks, and
  receive bounded read-only review before material execution.
- Veto diagnostics: Stage 0 particle count promoted to full-horizon adequacy;
  Tier-0 HMC promoted to readiness; stochastic PF marginal-gradient or
  exact-likelihood claim without a reviewed derivation/evidence gate; Claude
  used as executor.
- Non-claims: no new numerical, GPU, gradient, HMC, NUTS, ranking, default
  policy, or production-readiness claim follows from planning artifacts alone.

Skeptical audit:

- Wrong-baseline check: P8i starts from reviewed P8h limitations, not from an
  assumption that P8h already solved them.
- Proxy-metric check: planning completeness and review can authorize only the
  next bounded phase, not scientific promotion.
- Stop-condition check: any long GPU/HMC/NUTS run requires its phase-specific
  evidence contract and trusted execution.
- Artifact-fit check: the bootstrap artifacts define gates and stop conditions
  before running new experiments.

Gate status:

- `P8I_BOOTSTRAP_PASS_REVIEWED`; Claude review round 1 requested Phase 1
  repair for pilot-before-full-ladder staging, fresh trusted-GPU precheck,
  self-contained thresholds, P8h runner-flag provenance, and run-manifest
  coverage. Claude review round 2 accepted the first four repairs and required
  explicit run-manifest/provenance coverage. Claude review round 3 returned
  `VERDICT: AGREE` after the result-level manifest checklist and validation
  requirement were added. Phase 0 may launch.

### 2026-06-16 - Phase 0 - Governance And Gap Ledger

Evidence contract:

- Question: are all remaining P8h limitations mapped to explicit P8i gates
  with nonclaim boundaries before execution?
- Baseline/comparator: P8h Phase 11 closure result, P8h artifact index, and
  P8h Phase 5-8 results.
- Primary criterion: a ledger maps each remaining gap to a planned P8i phase,
  required artifacts, promotion gate, veto diagnostics, and nonclaims.
- Non-claims: no numerical, GPU, gradient, HMC, NUTS, ranking,
  default-policy, or production-readiness claim follows from Phase 0.

Actions:

- Created P8i remaining-gap ledger.
- Wrote Phase 0 result.

Review:

- Claude read-only review returned `VERDICT: AGREE`.

Gate status:

- `P8I_PHASE0_PASS_REVIEWED`; Phase 1 fresh GPU precheck and pilot rung may
  launch. Full Phase 1 ladder remains conditional on the pilot result and
  runtime projection.

### 2026-06-16 - Phase 1 - Longer-Prefix Particle And Value Ladder

Evidence contract:

- Question: does the exact P8h route remain finite, transport-valid,
  trusted-GPU, and adjacent-rung stable at longer prefixes `16,32` for five
  fixed seeds?
- Baseline/comparator: P8h Phase 5 short-prefix `4,8` ladder and within-P8i
  adjacent particle rungs.
- Primary criterion: select a diagnostic longer-prefix count by the
  finite/trusted-GPU/transport/runtime/five-seed-MCSE/adjacent-rung rule, or
  write an explicit blocker.
- Non-claims: no full-horizon adequacy, gradient correctness, HMC readiness,
  NUTS readiness, ranking, or default policy.

Skeptical audit:

- Wrong-baseline check: P8h Stage 0 `N=5` was re-tested at longer prefixes,
  not inherited as adequate.
- Proxy-metric check: ESS stayed explanatory; the selection used the
  predeclared gate.
- Stop-condition check: the pilot rung ran before the full ladder; no
  full-horizon run was launched.
- Artifact-fit check: Phase 1 artifacts carry P8i phase and plan provenance
  despite reusing the P8h tuning codepath flag.

Gate status:

- Pilot and full ladder executed on trusted GPU. The full ladder selected
  diagnostic `N=5` for horizons `16,32`; result written and Phase 2 subplan
  refreshed. Review is pending before Phase 2 GPU execution.

### 2026-06-16 - Phase 2 - Longer-Horizon OT Gradient Ladder

Evidence contract:

- Question: are AD gradients finite, connected, repeatable, and
  finite-difference-consistent enough at horizons `16,32`, `N=5`, to justify
  the next GPU/HMC diagnostic?
- Baseline/comparator: P8h Phase 6 horizon `4` gradient result and P8i Phase 1
  selected longer-prefix count.
- Primary criterion: both horizon artifacts pass finite connected gradients,
  FD residual threshold `1e-5`, trusted GPU, exact route/count provenance, and
  runtime budget.
- Non-claims: no stochastic PF marginal-gradient correctness, HMC readiness,
  NUTS readiness, posterior convergence, ranking, or default policy.

Skeptical audit:

- Wrong-baseline check: P8h Phase 6 did not substitute for the longer-prefix
  test.
- Proxy-metric check: finite-difference residuals are a veto/consistency
  diagnostic, not a stochastic-gradient proof.
- Stop-condition check: H32 launched only after H16 passed all gates.
- Artifact-fit check: both JSON artifacts record P8i phase/provenance,
  gate diagnostics, blocker fields, trusted GPU tensor devices, and runtime
  budget.

Gate status:

- H16 and H32 passed the executable gradient gates on trusted GPU. Phase 2
  result written and Phase 3 subplan refreshed. Read-only review returned
  `VERDICT: AGREE`; Phase 3 selected `N=5` GPU profile may launch.

### 2026-06-16 - Phase 3 - GPU Scaling Profile

Evidence contract:

- Question: is the selected longer-prefix route/count practically executable
  on trusted GPU for the next bounded HMC diagnostic?
- Baseline/comparator: P8h Phase 7 short-prefix GPU profile and P8i Phase 1/2
  value/gradient runtimes.
- Primary criterion: finite trusted-GPU values and transport diagnostics at
  horizons `16,32`, `N=5`, with the HMC projection rule passing.
- Non-claims: no full GPU scaling law, HMC readiness, production readiness,
  posterior convergence, ranking, or default policy.

Skeptical audit:

- Wrong-baseline check: Phase 3 measured H16/H32 directly rather than relying
  on P8h H4/H8 timings.
- Proxy-metric check: value-profile runtime is only a gate for whether a tiny
  HMC diagnostic is worth attempting.
- Stop-condition check: Phase 4 is allowed only as a tiny fixed-kernel Tier-1
  diagnostic if reviewed.
- Artifact-fit check: selected and adjacent profiles record P8i phase/plan,
  route/count/horizon/seed, trusted GPU, runtime, and transport diagnostics.

Gate status:

- Selected `N=5` and adjacent `N=10` profiles ran on trusted GPU. The selected
  `N=5` profile passed finite/transport/runtime gates and the HMC projection
  rule. Phase 3 result written and Phase 4 subplan refreshed. Read-only review
  and provenance repair returned `VERDICT: AGREE`; Phase 4 Tier-1 HMC
  diagnostic may launch.

### 2026-06-16 - Phase 4 - HMC Tier-1 Fixed-Kernel Diagnostic

Evidence contract:

- Question: can a tiny bounded fixed-kernel HMC diagnostic run at horizon `32`,
  `N=5`, without numerical/runtime validity vetoes?
- Baseline/comparator: reviewed P8i Phase 1 value/count gate, Phase 2
  relaxed-OT AD gradient gate, and Phase 3 GPU runtime projection.
- Primary criterion: finite trusted-GPU fixed-kernel HMC diagnostic with finite
  initial value/gradient, finite samples, finite target/log-accept traces,
  exact P8i provenance, and runtime within `900` seconds.
- Non-claims: no production HMC readiness, posterior convergence, valid
  tuning, NUTS readiness, stochastic PF marginal-gradient correctness,
  ranking, or default policy.

Skeptical audit:

- Wrong-baseline check: artifact identity uses P8i Tier-1 provenance even
  though the fixed-kernel codepath is reused from P8h.
- Proxy-metric check: acceptance and displacement are explanatory only.
- Stop-condition check: any nonfinite diagnostic, CPU fallback, runtime
  failure, or execution error would block.
- Artifact-fit check: the JSON records P8i schema/phase/status, predecessor
  paths, plan path, runtime budget, device diagnostics, HMC trace diagnostics,
  gate diagnostics, and nonclaims.

Gate status:

- The tiny fixed-kernel HMC Tier-1 diagnostic passed its execution gate on
  trusted GPU. Phase 4 result written and Phase 5 NUTS-readiness subplan
  refreshed; review is pending before Phase 5.

### 2026-06-16 - Phase 5 - NUTS Readiness Decision

Evidence contract:

- Question: is a NUTS diagnostic scientifically and computationally justified
  for the selected P8i route now?
- Baseline/comparator: Phase 4 HMC diagnostics and Phase 1-3
  value/gradient/GPU gates.
- Primary criterion: write a blocker if NUTS lacks implementation path,
  adaptation budget, or diagnostics.
- Non-claims: no NUTS readiness, production HMC readiness, posterior
  convergence, or default sampler policy.

Skeptical audit:

- Wrong-baseline check: Phase 4 tiny HMC execution is not NUTS readiness.
- Proxy-metric check: acceptance rate and finite trace quantities are not
  readiness evidence.
- Stop-condition check: no NUTS command path exists in the runner.
- Artifact-fit check: a decision artifact, not a compute run, answers the
  Phase 5 question.

Gate status:

- NUTS blocked. Phase 5 result written and Phase 6 claim-boundary subplan
  refreshed. Claude review attempt 16 produced no usable verdict after a
  monitored silence and interrupt; a small Claude probe returned `PROBE_OK`.
  A narrower review returned `VERDICT: REVISE`; Phase 6 needed to explicitly
  carry forward production-HMC/posterior/default-policy nonclaims and stronger
  stop conditions for derivation/tieout/estimator-contract needs. The Phase 6
  subplan was patched and focused checks passed. Claude review round 17
  returned `VERDICT: AGREE`; Phase 6 may launch.

### 2026-06-16 - Phase 6 - Stochastic-Gradient And Likelihood Boundary

Evidence contract:

- Question: what exactly has been shown about gradients and likelihood values,
  and what remains unproved or untested?
- Baseline/comparator: P8h/P8i gradient artifacts, value ladders, HMC/NUTS
  boundary results, and the declared relaxed Sinkhorn OT covariance-carry
  route.
- Primary criterion: classify each gradient/likelihood claim as passed,
  blocked, diagnostic-only, or out of scope.
- Non-claims: no stochastic PF marginal-gradient correctness, exact nonlinear
  likelihood correctness, NUTS readiness, production HMC readiness, posterior
  convergence, generic high-dimensional LEDH readiness, filter ranking, or
  default sampler policy.

Skeptical audit:

- Wrong-baseline check: Phase 6 treats Phase 2 as an AD graph diagnostic, not
  as proof of the stochastic PF marginal score.
- Proxy-metric check: finite-difference residuals and HMC execution are
  consistency/execution diagnostics only.
- Stop-condition check: stronger gradient or likelihood claims would require a
  derivation, exact-likelihood tieout, stochastic PF marginal-score estimator
  contract, or new empirical artifact outside this phase.
- Artifact-fit check: existing artifacts and nonclaim checks answer the phase;
  no new numerical run is needed.

Gate status:

- Phase 6 boundary result written and Phase 7 subplan refreshed. Claude
  review round 18 returned `VERDICT: REVISE`; Phase 7 needed a tighter
  P8h/P8i baseline boundary, runner/test coverage in boundary checks, and a
  required artifact coverage matrix. The Phase 7 subplan was patched and
  focused checks passed. Claude review round 19 returned `VERDICT: AGREE`;
  Phase 7 may launch as a no-compute decision phase.

### 2026-06-16 - Phase 7 - Scope, Ranking, And Default-Policy Decision

Evidence contract:

- Question: do the reviewed P8i artifacts justify any ranking,
  high-dimensional readiness, or default-policy change?
- Baseline/comparator: reviewed P8i results and blockers, including Phase 6;
  P8h is used only through artifacts explicitly inherited or re-tested by
  P8i.
- Primary criterion: a conservative decision table either justifies a narrow
  claim or preserves the nonclaim with explicit missing evidence.
- Non-claims: no filter ranking, generic high-dimensional LEDH readiness,
  default sampler policy, NUTS readiness, production HMC readiness, posterior
  convergence, exact likelihood correctness, or stochastic PF
  marginal-gradient correctness.

Skeptical audit:

- Wrong-baseline check: P8h is not treated as a live comparator or proof of
  broader readiness.
- Proxy-metric check: finite values, finite gradients, runtime, and tiny HMC
  execution are not promotion criteria for ranking or default policy.
- Stop-condition check: ranking or policy claims would require new
  comparative experiments or code-default changes, both outside this phase.
- Artifact-fit check: a decision artifact answers the phase; no numerical run
  is needed.

Gate status:

- Phase 7 result written and Phase 8 closeout subplan refreshed. Claude
  review round 20 returned `VERDICT: REVISE`; Phase 8 needed to require
  accepted Phase 7/8 review before entry and to stop on review
  rejection/non-acceptance. The Phase 8 subplan was patched and focused
  checks passed. Claude review round 21 returned `VERDICT: AGREE`; Phase 8
  may launch.

### 2026-06-16 - Phase 8 - Closeout, Artifact Index, And Repo Boundary

Evidence contract:

- Question: can P8i artifacts and code changes, if any, be preserved without
  pulling in unrelated lanes or overclaiming results?
- Baseline/comparator: P8i reviewed results, current worktree, and P8h Phase
  10 boundary manifest only as historical repo-boundary context.
- Primary criterion: write a boundary manifest separating intended P8i files
  from unrelated dirty groups and preserving all nonclaims/blockers.
- Non-claims: no remote synchronization, merge safety, bit-for-bit
  reproduction, production readiness, final ranking, default policy, NUTS
  readiness, exact likelihood correctness, or stochastic PF marginal-gradient
  correctness.

Skeptical audit:

- Wrong-baseline check: P8h is historical boundary context only.
- Proxy-metric check: artifact completeness and diff hygiene do not promote
  scientific claims.
- Stop-condition check: no commit, push, destructive action, package install,
  network fetch, or default-policy code change is needed.
- Artifact-fit check: the index, reset memo, boundary manifest, and result
  answer the closeout question.

Gate status:

- Phase 8 artifact index, repo-boundary manifest, reset memo, and result were
  written. JSON validation and diff checks passed; `git status --short`
  confirms the intended P8i files are separable from unrelated dirty work.
  Claude review round 22 returned `VERDICT: REVISE` only because the ledgers
  still said `PHASE8_READY` and did not record that Phase 8 artifacts had been
  written. This ledger was patched; Claude review round 23 returned
  `VERDICT: AGREE`. P8i is closed. No commit or push was performed.
