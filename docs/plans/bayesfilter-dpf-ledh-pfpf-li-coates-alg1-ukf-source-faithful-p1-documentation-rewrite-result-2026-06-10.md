# P1 Result: LaTeX Documentation Rewrite For Li-Coates Algorithm 1 LEDH-PFPF

Date: 2026-06-10

## Status

`PASS_P1_DOCUMENTATION_REWRITE_READY_FOR_P2`

## Decision

`PASS_P1_DOCUMENTATION_REWRITE_READY_FOR_P2`

The LaTeX documentation now exposes the Algorithm 1 obligations that were
missing from the old LEDH-PFPF-OT evidence lane: particle-dependent LEDH
linearization, per-particle covariance lifecycle, auxiliary zero-noise anchor,
actual proposal particle, determinant product, PF-PF weight, and covariance
resampling.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the LaTeX documentation state the PFPF(LEDH) algorithm and Li-Coates Algorithm 1 in enough detail that implementation omissions are visible? |
| Baseline/comparator | Li-Coates source anchors in `/tmp/li2017_particle_flow_source/PFPF_jrnl_2017.tex`; current `docs/chapters/ch19b_dpf_literature_survey.tex`; current `docs/chapters/ch19c_dpf_implementation_literature.tex`; UKF exposition in existing sigma-point chapters. |
| Primary pass criterion | The documentation includes a detailed exposition of PF-PF(LEDH), Algorithm 1, per-particle covariance lifecycle, UKF prediction/update objects, determinant product, weight formula, and resampling of covariance state. |
| Veto diagnostics | Missing `P_{k-1}^i -> P^i -> P_k^i`; unsupported claim that UKF is the paper's simulation default; treating OT resampling as part of Li-Coates Algorithm 1; vague prose without equations or obligation mapping. |
| Explanatory diagnostics | Additional notation, source-boundary caveats, and audit-checklist text. |
| Not concluded | P1 does not prove implementation faithfulness, value accuracy, gradient accuracy, or numerical performance. |

## Skeptical Plan Audit

| Hazard | P1 audit result |
| --- | --- |
| Wrong baseline | Clear.  P1 compares chapter text against local Li-Coates source lines, not against old BayesFilter results. |
| Proxy metric promotion | Clear.  No numerical metrics are run or promoted in P1. |
| Missing stop condition | Clear.  P1 stops only at a documentation artifact and Claude review; implementation waits for P2-P4. |
| Unfair comparison | Not applicable.  No filter comparison is performed. |
| Hidden assumption | Controlled.  The text states that UKF is a permitted/requested implementation choice, not a paper-wide empirical default. |
| Stale context | Controlled.  P0 quarantine remains active and old LEDH-PFPF-OT results are not cited as support. |
| Artifact fit | Clear.  Chapter diffs plus source/claim-support table answer the P1 question. |

## Files Changed

| File | Change |
| --- | --- |
| `docs/chapters/ch19b_dpf_literature_survey.tex` | Added Li-Coates PF-PF(LEDH) source-form local linearization, particle-specific predicted covariance, zero-noise anchor, actual proposal particle, auxiliary and actual pseudo-time updates, and a warning that a global affine map is not Algorithm 1 LEDH. |
| `docs/chapters/ch19c_dpf_implementation_literature.tex` | Added `Li--Coates Algorithm 1 as an implementation contract`, including covariance lifecycle, UKF source boundary, auxiliary/proposal split, determinant product, weight formula, covariance resampling triple, and an implementation audit checklist. |

## Chapter Line Anchors

| Obligation | Chapter anchor |
| --- | --- |
| Particle-specific predicted covariance and zero-noise anchor | `docs/chapters/ch19b_dpf_literature_survey.tex:563` |
| Local Jacobian at moving auxiliary state | `docs/chapters/ch19b_dpf_literature_survey.tex:576` |
| Li-Coates source-form LEDH coefficients | `docs/chapters/ch19b_dpf_literature_survey.tex:592` |
| Auxiliary and actual state pseudo-time migration | `docs/chapters/ch19b_dpf_literature_survey.tex:612` |
| Statement that global affine/local mean map is not Algorithm 1 LEDH | `docs/chapters/ch19b_dpf_literature_survey.tex:634` |
| Algorithm 1 implementation-contract section | `docs/chapters/ch19c_dpf_implementation_literature.tex:227` |
| Covariance lifecycle `P_{k-1}^i -> P^i -> P_k^i` | `docs/chapters/ch19c_dpf_implementation_literature.tex:236` |
| UKF permitted/requested boundary and OT exclusion | `docs/chapters/ch19c_dpf_implementation_literature.tex:248` |
| Zero-noise anchor and actual pre-flow proposal split | `docs/chapters/ch19c_dpf_implementation_literature.tex:257` |
| Pseudo-time auxiliary/actual updates | `docs/chapters/ch19c_dpf_implementation_literature.tex:271` |
| Determinant product | `docs/chapters/ch19c_dpf_implementation_literature.tex:290` |
| PF-PF Algorithm 1 weight | `docs/chapters/ch19c_dpf_implementation_literature.tex:313` |
| Covariance resampling triple | `docs/chapters/ch19c_dpf_implementation_literature.tex:333` |
| Implementation audit checklist | `docs/chapters/ch19c_dpf_implementation_literature.tex:345` |

## Source-Support Ledger

| Source | Classification | Local source status | Inspected technical anchors | Allowed claims | Forbidden claims |
| --- | --- | --- | --- | --- | --- |
| Li and Coates, 2017, `Particle Filtering with Invertible Particle Flow`, `\citep{li2017particle}` | `DIRECT_METHOD` | Local TeX source available at `/tmp/li2017_particle_flow_source/PFPF_jrnl_2017.tex`; publication metadata from `docs/references.bib`; no network metadata/retraction check in P1. | Lines 428-443 for LEDH coefficients and local linearization; lines 542-599 for invertible-map proposal and PF-PF weight; lines 602-634 for predicted covariance and EKF/UKF option; lines 636-682 for Algorithm 1 recursion. | PF-PF treats flow endpoint as deterministic proposal with Jacobian correction; LEDH coefficients are particle-local; Algorithm 1 requires a particle-specific covariance lifecycle; EKF/UKF covariance prediction/update can estimate `P` in nonlinear models. | UKF is not claimed as the paper's universal simulation default; OT/differentiable resampling is not part of source Algorithm 1; old BayesFilter LEDH-PFPF-OT results do not establish Algorithm 1 faithfulness. |

Citation counts, venue rankings, forward snowballing, and retraction metadata
were not queried in P1 because the phase was a local source-faithfulness rewrite
with an existing local full-text source.  This is a metadata limitation, not a
negative result.

## Claim-Support Table

| Documentation claim | Support class | Source or project anchor |
| --- | --- | --- |
| PF-PF(LEDH) uses an invertible deterministic map and proposal-density correction | `PRIMARY_TECHNICAL_SUPPORT` | Li-Coates source lines 542-599; chapter weight equations in `docs/chapters/ch19c_dpf_implementation_literature.tex:313` |
| LEDH coefficients are particle-local and depend on local linearization | `PRIMARY_TECHNICAL_SUPPORT` | Li-Coates source lines 428-443 and 654-657; chapter anchors `docs/chapters/ch19b_dpf_literature_survey.tex:576` and `:592` |
| Algorithm 1 has covariance lifecycle `P_{k-1}^i -> P^i -> P_k^i` | `PRIMARY_TECHNICAL_SUPPORT` | Li-Coates source lines 642-643 and 672-673; chapter anchor `docs/chapters/ch19c_dpf_implementation_literature.tex:236` |
| EKF or UKF may be used for nonlinear covariance prediction/update | `PRIMARY_TECHNICAL_SUPPORT_WITH_PROJECT_CHOICE` | Li-Coates source lines 631-634; BayesFilter chooses UKF for this repair program |
| Algorithm 1 maintains a zero-noise auxiliary anchor and an actual proposal particle | `PRIMARY_TECHNICAL_SUPPORT` | Li-Coates source lines 644-648 and 654-660; chapter anchors `docs/chapters/ch19b_dpf_literature_survey.tex:563` and `docs/chapters/ch19c_dpf_implementation_literature.tex:257` |
| Determinant product is `prod_j |det(I + eps_j A_j^i)|` | `PRIMARY_TECHNICAL_SUPPORT` | Li-Coates source lines 586-599 and 661-662; chapter anchor `docs/chapters/ch19c_dpf_implementation_literature.tex:290` |
| Algorithm 1 resamples `{x_k^i, P_k^i, w_k^i}` if resampling is used | `PRIMARY_TECHNICAL_SUPPORT` | Li-Coates source lines 676-677; chapter anchor `docs/chapters/ch19c_dpf_implementation_literature.tex:333` |
| OT/differentiable resampling is a BayesFilter extension, not a Li-Coates Algorithm 1 source claim | `PROJECT_BOUNDARY_STATEMENT` | Absence from Li-Coates Algorithm 1 plus P0 quarantine rule; chapter anchor `docs/chapters/ch19c_dpf_implementation_literature.tex:248` |

## Validation Commands

```bash
git diff -- docs/chapters/ch19b_dpf_literature_survey.tex docs/chapters/ch19c_dpf_implementation_literature.tex
git diff --check -- docs/chapters/ch19b_dpf_literature_survey.tex docs/chapters/ch19c_dpf_implementation_literature.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
rg -n "undefined|Reference .* undefined|Rerun" docs/main.log
rg -n "bf-pff-li-coates|bf-pfpf-alg1|Li--Coates Algorithm" docs/chapters/ch19b_dpf_literature_survey.tex docs/chapters/ch19c_dpf_implementation_literature.tex
```

Validation outcome:

- `git diff --check` passed.
- `latexmk` completed successfully under `docs/` and wrote `docs/main.pdf`.
- The post-build log check found no undefined-reference warnings; the only
  `Rerun` occurrence was the loaded `rerunfilecheck` package identifier.
- No TensorFlow, GPU, or numerical comparison command was run in P1.

## Run Manifest

| Field | Value |
| --- | --- |
| git branch | `main` |
| git commit | `26485010c28e11b3591da59b7ca375d4764c3d8d` |
| phase | `P1` |
| execution mode | visible current-dialogue execution |
| detached execution | `False` |
| CPU/GPU status | no TensorFlow/GPU command run |
| random seeds | `N/A` |
| output artifact | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p1-documentation-rewrite-result-2026-06-10.md` |
| execution ledger | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-visible-overnight-execution-ledger-2026-06-10.md` |
| subplan | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p1-documentation-rewrite-subplan-2026-06-10.md` |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| `P1_DOCUMENTATION_REWRITE_READY_FOR_READ_ONLY_REVIEW` | Source-grounded Algorithm 1 exposition added to both target chapters | No old LEDH-PFPF-OT evidence cited; UKF and OT boundaries stated; covariance lifecycle included | Literature metadata was not refreshed from network; implementation still not audited | Claude read-only P1 review, then repair or advance to P2 | No implementation faithfulness, no value/gradient performance, no replacement comparison table |

## Claude Review

Iteration 1 command:

```bash
bash scripts/dpf_v2_algorithm_full_comparison_claude_readonly_review.sh \
  --cwd /home/chakwong/BayesFilter \
  --name li-coates-alg1-ukf-p1-documentation-review-iter1 \
  "<read-only P1 documentation review prompt>"
```

Verdict:

`VERDICT: AGREE`

Findings:

- P1 satisfies the evidence contract.
- The particle-dependent LEDH exposition, zero-noise auxiliary anchor, actual
  proposal particle, local linearization, and rejection of a global affine
  surrogate are present and source-supported.
- The Algorithm 1 implementation contract covers covariance lifecycle,
  EKF/UKF prediction-update objects, determinant product, PF-PF weight, and
  covariance-resampling triple.
- No UKF paper-default, OT source-boundary, old LEDH-PFPF-OT evidence, or
  source-anchor veto issue was found.
