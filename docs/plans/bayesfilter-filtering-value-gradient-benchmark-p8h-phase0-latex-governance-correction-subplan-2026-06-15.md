# P8h Phase 0 Subplan: LaTeX Documentation And Governance Correction

Date: 2026-06-15

Status: `PASS_REVIEWED`

## Phase Objective

Patch the LaTeX documentation and planning governance so the DPF/LEDH lane
clearly states:

- Algorithm 1 UKF covariance state is Li-Coates state, not a BayesFilter
  invention;
- Corenflos OT/Sinkhorn or annealed-transport resampling is the intended
  differentiable resampling mechanism for the serious route;
- OT auxiliary-state carry for Algorithm 1 covariances is a BayesFilter
  integration/bookkeeping rule, not a new filter claim;
- no-resampling P8g evidence is demoted to graph/kernel sanity evidence.

## Entry Conditions

- User approved creating the P8h phased master program with this documentation
  phase inserted as Phase 0.
- P8h master program and visible runbook exist.
- Worktree is dirty; unrelated Zhao-Cui, SGQF, monograph, and existing P8g
  changes must be preserved.

## Required Artifacts

- Updated LaTeX documentation, expected primary targets:
  - `docs/chapters/ch19b_dpf_literature_survey.tex`;
  - `docs/chapters/ch32_diff_resampling_neural_ot.tex`;
  - `docs/chapters/ch19e_dpf_hmc_target_suitability.tex`.
- Phase result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase0-latex-governance-correction-result-2026-06-15.md`.
- Updated execution and Claude review ledgers.

## Required Checks, Tests, Reviews

- `git diff --check`.
- `rg -n "Algorithm 1 UKF covariance|OT auxiliary-state carry|Corenflos|no-resampling" docs/chapters docs/plans`.
- A focused LaTeX build check:
  `latexmk -pdf -interaction=nonstopmode -halt-on-error docs/main.tex`.
  If it fails, Phase 0 may advance only if the result artifact includes the
  exact failing log excerpt, a file/line attribution showing the failure is
  unrelated to P8h edits, and a focused syntax/search check proving the P8h
  documentation edits are present and coherent.
- Focused stale-language search in all DPF/HMC chapters touched by this lane:
  `rg -n "no-resampling|no resampling|fixed-randomness|HMC readiness|categorical-resampling gradient|OT auxiliary-state carry|Corenflos" docs/chapters/ch19b_dpf_literature_survey.tex docs/chapters/ch32_diff_resampling_neural_ot.tex docs/chapters/ch19e_dpf_hmc_target_suitability.tex`.
- Claude read-only review of the bounded documentation diff and phase result.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Does the repo documentation now express the corrected Algorithm 1 + Corenflos OT relationship without implying a new filter invention or overclaiming gradients/HMC? |
| Baseline/comparator | Existing DPF chapters, P8g artifacts, historical LEDH-PFPF-OT tests, and P8h master program. |
| Primary criterion | Documentation contains the corrected route, covariance-state, OT auxiliary-state-carry, no-resampling demotion, and claim-boundary language; local checks pass or a blocker is written. |
| Veto diagnostics | Saying covariance state was invented by BayesFilter; saying Corenflos is insufficient as a resampler; claiming categorical-resampling gradients; HMC readiness claim; editing unrelated Zhao-Cui/monograph text. |
| Explanatory diagnostics | LaTeX build output, grep hits, Claude wording suggestions. |
| Not concluded | No implementation, value tuning, gradient correctness, GPU scaling, or HMC readiness. |

## Forbidden Claims And Actions

- Do not claim the serious OT route has passed.
- Do not claim stochastic PF marginal-gradient correctness.
- Do not claim HMC readiness.
- Do not rewrite unrelated chapters beyond the minimal DPF/LEDH clarification.
- Do not treat Claude as execution authority.

## Exact Next-Phase Handoff Conditions

Advance to Phase 1 only if:

- documentation diff is reviewed locally across all three required LaTeX
  targets;
- required local checks pass or any LaTeX build issue is documented as unrelated
  pre-existing state with exact log/file evidence and a focused P8h syntax/search
  check;
- Phase 0 result is written;
- Claude review returns `VERDICT: AGREE` or any material issue is patched and
  re-reviewed within the five-round limit.

## Stop Conditions

- Documentation correction requires scientific or source claims beyond current
  evidence.
- LaTeX changes conflict with unrelated dirty user work.
- Claude/Codex do not converge after five material review rounds.
- Required checks reveal a material documentation/build break that cannot be
  repaired within Phase 0 scope.
