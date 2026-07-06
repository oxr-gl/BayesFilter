# SVD-Nystrom No-HMC Promotion Claude Review Ledger

Date: 2026-06-25

Status: `P04C_BLOCKED_INVALID_CALIBRATION_ARTIFACT`

## Role Boundary

Claude is read-only reviewer only. Claude may inspect exact-path bounded plan
artifacts and report findings, but cannot edit files, run commands, launch
agents, authorize thresholds, approve default-policy changes, or cross
scientific/product boundaries.

## Standing Approval

The user granted bounded standing approval for this SVD-Nystrom no-HMC
promotion runbook:

- Claude Code may read and transmit to the external Claude service only files
  under `/home/ubuntu/python/BayesFilter/docs/plans/`,
  `/home/ubuntu/python/BayesFilter/docs/benchmarks/`, and
  `/home/ubuntu/python/BayesFilter/docs/plans/logs/` whose filenames start with
  `bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion` or
  `svd-nystrom-nohmc-promotion`, plus directly referenced same-lane benchmark
  artifacts needed to review phase evidence.
- Claude may use them only for read-only subplan/result/artifact consistency
  review.
- Claude may not read source code, unrelated paths, credentials, model files,
  run commands, edit files, launch agents, or authorize
  promotion/default/scientific/HMC/product/funding boundaries.

## Review Rounds

| Round | Scope | Verdict | Findings | Action |
| --- | --- | --- | --- | --- |
| P00-R1 | Master plus same-prefix plan set | Unusable empty output | Claude worker exited code 0 with zero-byte log after broad exact-prefix prompt. Probe returned `CLAUDE_PROBE_OK`. | Narrowed prompt to exact master path. |
| P00-R1b | Exact master path only | `VERDICT: REVISE` | Needed explicit predecessor gating, no-regression/operational-viability scoping for non-LGSSM comparator, and phase ownership of ledgers/handoff. | Patched master and runbook. |
| P00-R2 | Exact master path, focused on R1 repairs | `VERDICT: REVISE` | Mid-program custody for shared artifacts remained ambiguous. | Patched P01-P07 in-flight ledger/handoff and Claude-review-ledger custody. |
| P00-R3 | Exact master path, focused on custody repair | `VERDICT: AGREE` | Custody text is explicit and internally consistent; no new ambiguity found. | P00 review converged. |
| P02A-R1 | P02A/P02 repair result plus P03 handoff paths | Not launched | External review command was rejected because the current approval did not explicitly cover transmitting these new repair-review paths to Claude. | Stop before P03 and ask for exact path-scoped approval. |
| P02A-R1b | Approved exact P02A/P02/P03 paths | `VERDICT: REVISE` | Repair evidence was internally consistent, but P03 still carried the old deterministic-blocker status and expected the old `P02_PASS_TO_P03_ACTUAL_SIR_STRESS` token. | Patched P02A/P02/P03 to define `P02_REPAIR_REVIEW_AGREE_PASS_TO_P03_ACTUAL_SIR_STRESS` as the explicit post-review handoff token. |
| P02A-R2 | Approved exact P02A/P02/P03 paths, focused token-sync repair review | `VERDICT: AGREE` | Post-review P03-opening token is now single and consistent; P03 no longer carries the old deterministic GPU/TF32 blocker status; no unsupported promotion/default/HMC/scientific claim introduced. | Material repair review converged; P03 may enter pre-run audit. |
| P03-R1 | P03 actual-SIR stress subplan | `VERDICT: REVISE` | Residual thresholds were required but undeclared; terminal artifacts were not fully pinned; phase objective was broader than the frozen same-shape panel. | Patched residual/log-weight thresholds, exact result/P04 paths, and same-shape objective. |
| P03-R2 | P03 actual-SIR stress subplan repair | `VERDICT: REVISE` | Residual thresholds and objective were fixed, but per-row JSON/Markdown/log artifacts remained wildcard/directory scoped and command placeholders remained unconstrained. | Patched a complete seed-by-seed artifact manifest for seeds `83000..83029` and exact command path mapping. |
| P03-R3 | P03 exact per-row artifact repair | `VERDICT: AGREE` | All per-row artifacts are fully pinned, command outputs map to exact manifest paths, initial/reserved seed bounds are clear, and no new boundary-safety or evidence-contract inconsistency was found. | P03 subplan review converged; P03 may execute after local pre-run skeptical audit. |
| P03/P04-R1 | P03 result plus refreshed P04 subplan | `VERDICT: AGREE` | P03 result and P04 subplan were internally consistent; no unsupported promotion/default/HMC/scientific claim was introduced. | P04 may proceed to local harness implementation/tests before trusted GPU rows. |
| P04-R1 | P04 subplan, local harness review note, P04 local test log, P03 result/summary; no source code | `VERDICT: AGREE` | Entry/handoff, evidence contract, per-row artifact gating, forbidden-claim boundaries, and local-check artifact coverage are consistent. Residual risks: no P04 GPU row exists yet, and source/test files were intentionally out of scope. | P04 may proceed only to trusted GPU preflight and seed `84000`. |
| P04A-R1 | P04 result, P04 summary, P04 row artifact, P04A subplan, ledgers; no source code | `VERDICT: AGREE` | P04 failure classification is consistent with the row artifact; P05 remains blocked; P04A is bounded, exact-artifact gated, statistically humble, and cannot backdoor promotion. Residual risk: GPU memory provenance uses different sampling times. | P04A may proceed to trusted GPU preflight and one-at-a-time diagnostic rows. |
| P04A-result-R1 | P04A result, P04A summary, P04A subplan, P04 result, ledgers, stop handoff, and same-prefix P04A artifacts; no source code | `VERDICT: AGREE` | P04A result matches frozen panel and row artifacts; stop/handoff state is correct; P05 remains blocked; statistical/nonclaim boundaries are preserved. Residual risks: threshold-level reproduction is not bitwise equality, and GPU memory snapshots use different sampling times. | Current promotion ladder remains stopped as repair-required. |
| P04B-R1 | P04B subplan exact path only | `VERDICT: REVISE` | Handoff allowed too much ambiguity around local checks, Claude convergence, P04C required sections, inherited no-claims boundary, and positive replacement status. | Patched P04B handoff/review requirements. |
| P04B-R2 | P04B focused repair review | `VERDICT: AGREE` | R1 findings fixed; local checks and explicit Claude agreement are required; P04C sections and no-claims boundary are pinned. | P04B plan review converged. |
| P04C-R1 | P04C subplan exact path only | `VERDICT: REVISE` | Ambiguous handling of one or two deterministic-invalid calibration rows; possible reduced-panel scale extraction. | Patched P04C to require all 12 calibration rows deterministic-valid and no reduced-panel pass. |
| P04C-R2 | P04C focused repair review | `VERDICT: AGREE` | All 12 rows required, no reduced-panel pass, no post-hoc row-rejection rules, candidate margin summaries remain unapproved/unvalidated/unfrozen, and P04C remains scale extraction only. | P04C subplan review converged. |
| P04C1-R1 | P04C1 streaming-nonfinite diagnostic subplan plus P04C/P04C0 same-lane artifacts | `VERDICT: REVISE` | Exact ledger/handoff artifact paths were not named, and the streaming-only row overclaimed "without running Nystrom" while still carrying Nystrom flags. | Patched exact execution-ledger, Claude-review-ledger, and stop-handoff paths; changed row wording to streaming route selection rather than non-execution of Nystrom. |
| P04C1-R2 | P04C1 focused repair review plus large referenced artifacts | No verdict; aborted oversized-read attempt | Claude stayed within same-lane scope but over-read large benchmark JSON artifacts and entered API/file-read failure/retry behavior. | Terminated the attempt and narrowed the prompt to the exact P04C1 subplan plus locally established artifact facts. |
| P04C1-R3 | Exact P04C1 subplan only, focused on R1 repairs with local artifact facts supplied | `VERDICT: AGREE` | Prior R1 findings fixed: ledger/handoff paths are exact, row wording no longer overclaims, and seed `84101` is not excluded. | P04C1 review converged; proceed only to skeptical pre-run audit and trusted GPU preflight. |
| P04C2-R1 | Exact P04C2 subplan plus exact P04C1 result | `VERDICT: REVISE` | P04C2 plan was internally coherent but the Claude-review scope allowed same-prefix benchmark artifacts/logs while the active review prompt forbade them; the local precheck also required P04C1 summary parsing in a way that could confuse restricted review scope. | Patched P04C2 so Claude plan review may read only the exact subplan and exact P04C1 result unless separately authorized, and made P04C1 summary parsing an execution-side local check. |
| P04C2-R2 | Exact P04C2 subplan only, focused on R1 repair convergence | `VERDICT: AGREE` | Claude confirmed the review scope is narrowed to exact subplan plus exact P04C1 result, benchmark/log/source/test reads are forbidden, and P04C1 summary parsing is execution-side/local only unless separately authorized. | P04C2 review converged; proceed only to skeptical pre-run audit and trusted GPU preflight. |
| P04C2A-R1 | Exact P04C2A subplan plus exact P04C2 result; no source/test/log reads | `VERDICT: AGREE` | Claude agreed P04C2A is correctly scoped as opt-in harness exception-artifact repair, treats P04C2 as missing structured diagnostics rather than SVD-Nystrom failure, preserves no-claim boundaries, and forbids paired deltas from exception rows. Minor nits did not change verdict. | P04C2A plan review converged; proceed to scoped implementation and focused local tests. |
| P04C3-R1 | Exact P04C3 subplan plus exact P04C2/P04C2A results; no source/test/log/benchmark JSON reads | `VERDICT: REVISE` | Plan kept comparator/SVD-Nystrom boundaries, but inverse-to-Cholesky wording overclaimed equivalence, no-jitter/no-stabilization boundary was under-specified, and the canary artifact trio needed tighter exact-row coverage. | Patched P04C3 wording to avoid proof claims, explicitly forbid jitter/stabilization-policy changes, and pin exact canary JSON/Markdown/log plus seed/device/mode row. |
| P04C3-R2 | Exact P04C3 subplan only, focused on R1 repairs | `VERDICT: AGREE` | Claude confirmed inverse-to-Cholesky-solve wording is scoped to comparator validity, no general proof is claimed, no-jitter/no-stabilization-policy boundary is explicit, exact canary artifacts are pinned, and no P04C/P05/threshold/promotion leakage remains. | P04C3 plan review converged; proceed to scoped implementation, focused tests, and trusted GPU canary. |

## Pending Review

- No Claude source-code review was run for P04C0 because the standing approval
  forbids Claude from reading source code or tests.
- The P04C1 streaming-comparator diagnostic subplan review converged. Any
  material next subplan after P04C1 still requires local review and, when
  appropriate, bounded Claude read-only review.
- Claude must not read the P04 harness source or focused test source unless the
  user grants explicit source-code disclosure approval.

## Prompt Boundary

Use exact absolute paths and avoid whole-file prompt pastes. If a prompt blocks,
retry with a narrower exact-path heading/checklist prompt before asking the user
for explicit path/content export approval.
