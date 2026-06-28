# P07 Final Default-Readiness Closeout Subplan

Date: 2026-06-24

Status: `COMPLETE_P07_FINAL_CLOSEOUT_PASSED`

## Phase Objective

Make the final bounded engineering default-readiness decision for the actual-SIR
d18 GPU/TF32 LEDH-PFPF-OT low-rank route, using the completed phase artifacts
and preserving all nonclaims and unresolved boundaries.

P07 may conclude one of:

- `LOW_RANK_LEDH_DEFAULT_ENGINEERING_READY_BOUNDED`
- `LOW_RANK_LEDH_OPTIONAL_ROUTE_ONLY`
- `BLOCKED_OR_REPAIR_REQUIRED`

P07 is a decision/closeout phase. It does not by itself authorize new code
changes, public API expansion, package release, HMC readiness, posterior
correctness, dense Sinkhorn equivalence, scientific validity, or statistical
superiority.

## Entry Conditions Inherited From Previous Phase

- P00 through P05 results exist and pass.
- P06 result exists and is explicitly skipped with HMC preserved as a nonclaim.
- P07 subplan has been refreshed after P05/P06 close.
- All required benchmark, implementation, review, and ledger artifacts are
  available or their absence is explained as a blocker.
- P07 may write a documentation-only bounded engineering readiness decision
  using completed artifacts. That decision does not switch any package-level,
  public API, broad product, model-file, dependency, or runtime default.
- Explicit final approval is required before any final default-policy switch or
  any conclusion/action beyond the reviewed actual-SIR low-rank
  validation/reporting surface.
- No approval is inherited for new code changes, public API expansion, package
  release, model-file changes, dependency changes, HMC-readiness claims,
  posterior-correctness claims, statistical superiority claims, or scientific
  claims.

## Required Artifacts

- This subplan, refreshed after P05/P06.
- Final result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-result-2026-06-24.md`
- Evidence matrix covering P00 through P06.
- Decision table.
- Inference-status table.
- Run manifest summary for material runtime artifacts.
- Post-run red-team note.
- Updated execution ledger.
- Updated Claude review ledger.
- Stop handoff if the final decision is blocked.

## Required Checks, Tests, And Reviews

- Skeptical closeout audit over the full evidence chain.
- Artifact existence and status scan for P00 through P06 results.
- Boundary scan over final result and ledgers for unsupported default,
  posterior, HMC, dense-equivalence, statistical, public API, production, or
  scientific claims.
- Consistency scan that the final decision matches phase results and does not
  upgrade descriptive timing to statistical superiority.
- If P05 changed code: rerun the focused P05 tests or record why the latest P05
  result already covers the exact final state.
- If P05 changed only harness/runner defaults, verify the final decision does
  not claim public API readiness, package-level default behavior, HMC readiness,
  posterior correctness, dense equivalence, or broad production readiness.
- Claude Opus/max read-only final review before finalizing the P07 result.

## Skeptical Plan Audit

| Audit item | Status |
| --- | --- |
| Wrong baseline | Guarded: P07 must use the streaming comparator and locked low-rank candidate evidence recorded in P03/P04. |
| Proxy metric promoted | Guarded: timing remains descriptive unless a phase provided statistical evidence, which current provisional plan does not expect. |
| Missing stop conditions | Guarded by artifact/status scan, boundary scan, final approval for policy switch, and blocked handoff. |
| Unfair comparison | Guarded: P07 can only summarize paired evidence from reviewed benchmark phases. |
| Hidden assumptions | Guarded: unresolved HMC, posterior, dense equivalence, API, and scientific claims must remain explicit nonclaims. |
| Stale context | Guarded: P07 must be refreshed after P05/P06 and before final review. |
| Environment mismatch | Guarded: runtime evidence comes from manifests in P03/P04/P05/P06, not new unrecorded assumptions. |
| Artifact mismatch | Guarded: P07 requires an evidence matrix and final result with exact source artifacts. |

Audit conclusion: P07 is provisional until P05/P06 close. Without separate
final approval, P07 can only write a documentation-only bounded engineering
readiness decision and cannot switch package-level, public API, broad product,
model-file, dependency, or runtime defaults.

## Evidence Contract

- Question: does the completed evidence chain justify a bounded engineering
  default-readiness decision for the locked low-rank actual-SIR d18 GPU/TF32
  LEDH-PFPF-OT route?
- Baseline/comparator: current streaming GPU/TF32 route, preserved as explicit
  comparator/fallback.
- Primary pass criterion: every required phase result exists, hard-veto gates
  pass or are explicitly bounded, implementation/default-surface tests pass if
  code changed, no-NumPy/default-path evidence is preserved, artifacts are
  complete, and final review converges without unsupported claims.
- Veto diagnostics: missing required result; unresolved hard veto; failed P04
  resource-boundary gate without accepted blocker; failed P05 implementation
  test; NumPy implementation path; missing streaming fallback; unsupported
  claim; final approval absent for a default-policy switch; Claude/Codex review
  nonconvergence.
- Explanatory diagnostics: P03/P04 descriptive timings, wall times, memory
  snapshots, paired deltas, residuals, warning counts, code diff summary, test
  output, HMC skipped/pass/fail status.
- Not concluded unless separately proven by phase evidence: posterior
  correctness, HMC readiness, dense Sinkhorn equivalence, statistical
  superiority, public API readiness, formal memory scaling, package release
  readiness, production readiness beyond the bounded lane, or scientific
  validity.
- Artifact preserving result: final result, evidence matrix, ledgers, and stop
  handoff if blocked.

## Forbidden Claims And Actions

- Do not finalize a package-level, public API, broad product, model-file,
  dependency, or runtime default-policy switch without explicit final approval.
- Do not represent the documentation-only bounded closeout decision as an
  automatic package/public/product default switch.
- Do not make new code changes in P07.
- Do not claim posterior correctness, HMC readiness, dense Sinkhorn equivalence,
  statistical superiority, public API readiness, scientific validity, formal
  memory scaling, package release readiness, or broad production readiness
  unless a prior phase explicitly supplied that evidence and approval.
- Do not reinterpret descriptive timing as statistical ranking.
- Do not hide failed or skipped phases.
- Do not treat Claude as execution authority.

## Exact Next-Phase Handoff Conditions

- If P07 decides `LOW_RANK_LEDH_DEFAULT_ENGINEERING_READY_BOUNDED`, write the
  final result and name remaining nonclaims and future evidence needs.
- If P07 decides `LOW_RANK_LEDH_OPTIONAL_ROUTE_ONLY`, write the final result and
  preserve low-rank as optional or candidate-only according to P05/P06 evidence.
- If P07 decides `BLOCKED_OR_REPAIR_REQUIRED`, write the final result and stop
  handoff with the exact blocker and smallest reviewed repair.
- There is no next execution phase in this master program unless the user
  starts a new repair or expansion program.

## Stop Conditions

- Required prior phase result is absent or internally inconsistent.
- P07 subplan is stale after P05/P06.
- Final approval is absent for any package-level, public API, broad product,
  model-file, dependency, or runtime default-policy switch.
- Boundary scan finds unsupported claims.
- Evidence matrix cannot reconcile phase outcomes.
- Claude/Codex final review does not converge after five rounds for the same
  blocker.

## End-Of-Subplan Duties

1. Run final local scans/checks.
2. Write the final result or blocked stop handoff.
3. Update execution and review ledgers.
4. State remaining evidence gaps and nonclaims.

## Self-Review

- Consistency: closes the existing master program without adding new work.
- Correctness: separates engineering default readiness from scientific/HMC/API
  claims.
- Feasibility: artifact and boundary scans only, plus focused P05 tests already
  run in the P05 result.
- Artifact coverage: final result, evidence matrix, ledgers, and stop handoff.
- Boundary safety: requires final approval before any policy switch and forbids
  new code changes.
