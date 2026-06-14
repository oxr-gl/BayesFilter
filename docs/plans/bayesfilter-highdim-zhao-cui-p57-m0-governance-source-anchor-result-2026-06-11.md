# P57-M0 Result: Governance And Source-Anchor Lock

metadata_date: 2026-06-11
phase: P57-M0
status: PASS_CLAUDE_REVIEWED

## Decision Table

| Field | Result |
| --- | --- |
| Decision | Lock the P57 source-faithfulness boundary before implementation resumes. |
| Primary criterion status | PASS: this checked-in result records the binding source-anchor rule, demotes P52/P53 UKF/rank artifacts to diagnostic-only status for source-faithful claims, and lists durable paper identifiers plus source files each implementation phase must re-open. |
| Veto diagnostic status | PASS: no adaptive parity, S&P reproduction, smoothing, old `R_eff` route, UKF scout, local/operator route, or all-grid route is allowed to close a source-faithful Zhao-Cui claim. |
| Main uncertainty | None for governance. Implementation correctness and source-route adequacy remain open to later phases. |
| Next justified action | Send this result to Claude read-only review; if agreed, advance to P57-M1. |
| What is not concluded | No filtering correctness, rank readiness, HMC readiness, paper-scale SIR success, or faithful implementation completion. |

Required token:

`PASS_P57_M0_GOVERNANCE_SOURCE_ANCHOR`

## Binding Rule

`BLOCK_SOURCE_UNGROUNDED` is binding for P57.

For the Zhao-Cui high-dimensional filtering lane, a claim of "faithful",
"source-faithful", "paper-scale Zhao-Cui", or equivalent language is invalid
unless the phase artifact cites:

1. the relevant Zhao-Cui paper/math anchor; and
2. the local author source file and line-level operation under
   `third_party/audit/zhao_cui_tensor_ssm_p10/source`.

Every implementation choice must be classified before it is accepted:

| Classification | Meaning |
| --- | --- |
| `source_faithful` | Matches a cited paper/source operation. |
| `fixed_hmc_adaptation` | Preserves the author's route while freezing randomness, ranks, bases, random draws, sample schedules, ESS stop conditions, resampling policy, and branch choices before likelihood evaluation. |
| `extension_or_invention` | Not present in the paper/source; useful only as an explicitly approved extension, not as closure of a source-faithfulness gap. |

## Diagnostic-Only Demotion

P52/P53 UKF scouting, route-rank selection, memory forecasts, and transition
operator work remain available as lower-rung diagnostics.  They cannot close a
P57 source-faithfulness claim when they rely on:

- `transition_route.py`;
- `rank_budget.py` `R_eff` route metadata;
- local-neighborhood transition operators;
- all-grid retained storage;
- UKF as likelihood/correctness oracle;
- d=18/d=50/d=100 spatial SIR runs without a source-route transport object.

For P57, rank selection must be tied to the fixed TT/SIRT retained-object
route.  UKF may scout centers, scales, covariance structure, effective
dimension, candidate rank ranges, preconditioner initialization, and basis
scales, but it cannot certify likelihood, source faithfulness, final rank,
HMC readiness, or filtering correctness.

## Non-Goals Removed From Missing Gaps

The following are not P57 missing gaps unless the user explicitly re-scopes the
program:

- adaptive Zhao-Cui parity;
- S&P 500 reproduction;
- smoothing support.

They may be mentioned as non-goals or future separate programs, but they must
not block this fixed-HMC source-route repair lane.

## Required Source Anchors For Later Phases

Each implementation phase must re-open and cite the relevant anchors below.
P56 is useful checked-in prior evidence, but later phase artifacts must preserve
their own paper/source references before accepting implementation choices.
Ephemeral extracted-text paths such as `/tmp/zhao_cui_jmlr_2024.txt` are not
durable anchors. Later phases may use such extracts only as convenience while
inspecting the paper; the cited evidence must be direct paper identifiers
(section/equation/algorithm/proposition/example) plus author source file and
line-level anchors under `third_party/audit/zhao_cui_tensor_ssm_p10/source`, or
a checked-in artifact that records those anchors.

| Topic | Paper/source anchors to re-open |
| --- | --- |
| Adjacent-state posterior recursion and retained marginalization | Paper equations (9)--(11); checked-in prior anchor `docs/plans/bayesfilter-highdim-zhao-cui-p56-source-anchor-audit-2026-06-10.md:45`; author `models/full_sol.m:21-43`, `:72-81`. |
| Basic and squared TT/SIRT route | Paper Algorithm 1, Algorithm 2, equation (13), Proposition 2, and equation (14); checked-in prior anchor `docs/plans/bayesfilter-highdim-zhao-cui-p56-source-anchor-audit-2026-06-10.md:46-51`; author `deep-tensor.dev/src/SIRT.m:50-86`, `deep-tensor.dev/src/@TTSIRT/marginalise.m:1-87`. |
| Conditional KR maps and inverse/forward maps | Paper conditional density/CDF/Knothe-Rosenblatt map construction following Proposition 2; checked-in prior anchor `docs/plans/bayesfilter-highdim-zhao-cui-p56-source-anchor-audit-2026-06-10.md:52`; author `deep-tensor.dev/src/AbstractIRT.m:152-188`, `:192-213`, `:217-270`, `:299-354`. |
| Proposal sampling and density correction | Paper Algorithm 3 and equations (21)--(23); checked-in prior anchor `docs/plans/bayesfilter-highdim-zhao-cui-p56-source-anchor-audit-2026-06-10.md:53`; author `models/full_sol.m:33-38`, `deep-tensor.dev/src/@TTSIRT/eval_potential_reference.m:1-36`. |
| Target formula and recentering | Paper sequential target formula from Algorithm 2/equations (15)--(16); checked-in prior anchors `docs/plans/bayesfilter-highdim-zhao-cui-p56-source-anchor-audit-2026-06-10.md:50`, `:62-65`; author `models/full_sol.m:46-135`, `models/ssmodel.m:45-59`, and `computeL.m` line anchors to be re-opened by the phase that modifies recentering code. |
| Preconditioned route for paper-scale examples | Paper Algorithm 5 and equations (30)--(35); checked-in prior anchor `docs/plans/bayesfilter-highdim-zhao-cui-p56-source-anchor-audit-2026-06-10.md:54`; author `models/pre_sol.m:33-260`. |
| Paper-scale spatial SIR scope | Paper spatial SIR numerical example with state dimension 18, `T=20`, rank ladder `{10,20,40}`, and linear preconditioning; checked-in prior anchors `docs/plans/bayesfilter-highdim-zhao-cui-p56-source-anchor-audit-2026-06-10.md:55`, `:59`; author `eg3_sir/mainscript.m:14-17`, `:39-56`. |

## Commands Run

- `sed -n '1,220p' docs/plans/bayesfilter-highdim-zhao-cui-p57-m0-governance-source-anchor-subplan-2026-06-11.md`
- `sed -n '1,220p' docs/plans/bayesfilter-highdim-zhao-cui-p57-visible-gated-execution-runbook-2026-06-11.md`
- `sed -n '1,140p' docs/plans/bayesfilter-highdim-zhao-cui-p56-source-anchor-audit-2026-06-10.md`
- `sed -n '1,180p' docs/plans/bayesfilter-highdim-zhao-cui-p56-source-anchor-audit-claude-review-2026-06-10.md`
- `sed -n '1,120p' AGENTS.md`
- `sed -n '1,80p' memory.md`
- `rg -n "BLOCK_SOURCE_UNGROUNDED|source" AGENTS.md CLAUDE.md memory.md docs/plans/bayesfilter-highdim-zhao-cui-p56-source-anchor-audit-2026-06-10.md docs/plans/bayesfilter-highdim-zhao-cui-p57-*.md`
- Claude read-only review iteration 1 returned `VERDICT: REVISE`; this result
  was patched to remove ephemeral `/tmp` paths as required anchors and to
  require direct paper identifiers plus source file/line anchors in later
  phases.
- Claude read-only review iteration 2 returned `VERDICT: AGREE`.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | Not recorded for M0; governance/document-only gate in dirty worktree. |
| Environment | Codex visible supervisor/executor in `/home/chakwong/BayesFilter`. |
| CPU/GPU status | CPU-only/static document gate; GPU not used. |
| Data version | N/A. |
| Random seeds | N/A. |
| Wall time | N/A. |
| Plan file | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m0-governance-source-anchor-subplan-2026-06-11.md`. |
| Result file | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m0-governance-source-anchor-result-2026-06-11.md`. |

## Post-Run Red-Team Note

Strongest alternative explanation: this result can only prevent source-drift
claims; it does not implement the missing source-route machinery.  The weakest
part of the evidence is that M0 still relies on P56 as checked-in prior
evidence rather than redoing the full paper audit.  That is acceptable for M0
because implementation phases are required to re-open their exact paper/source
anchors before code changes, and ephemeral `/tmp` extracted-text paths are not
accepted as durable source anchors.
