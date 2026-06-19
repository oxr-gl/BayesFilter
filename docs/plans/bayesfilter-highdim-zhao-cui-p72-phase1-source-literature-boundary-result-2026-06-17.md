# P72 Phase 1 Result: Source And Literature Boundary Audit

metadata_date: 2026-06-17
status: PHASE1_PASSED_CLAUDE_R2_AGREE
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-fixed-fit-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p72-visible-gated-execution-runbook-2026-06-17.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p72-phase1-source-literature-boundary-subplan-2026-06-17.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p72-phase0-repair-note-closeout-result-2026-06-17.md

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Which P72 repair operations are source-faithful author-route behavior, which are fixed-HMC freezing adaptations, and which are our support/stability extensions? |
| Baseline/comparator | P72 repair note, P70 Phase 6h failure, BayesFilter Zhao--Cui source-governance gate, local Zhao--Cui paper ledgers, local author source, and local bibliography. |
| Primary criterion | Every proposed operation has one classification with source anchors or an explicit source gap; no source-faithfulness claim is emitted without both paper and local author-source anchors; Phase 2 consumes only classified operations. |
| Veto diagnostics | Unsupported use of "faithful"; treating guard/stability additions as author behavior without anchors; using metadata or abstracts as theorem support; silently omitting relevant TT/SIRT or stable least-squares anchors; author-source paths not inspected; Phase 2 authorized to implement unclassified behavior. |
| Explanatory only | Candidate papers without checked technical anchors, citation/venue metadata, prior ledgers that were not rechecked line by line, and code line searches that reveal possible but uninterpreted anchors. |
| Not concluded | No implementation, no repaired diagnostic, no proof that guard additions are optimal, no continuum support certificate, no original Zhao--Cui failure claim, no adaptive parity, no d18 validation, no HMC readiness. |
| Artifact preserving result | This result, P72 ledgers, and refreshed Phase 2 subplan. |

## Skeptical Audit Result

Phase 1 survived the skeptical plan audit because it is read-only with respect
to production code and diagnostic execution.  The correct baseline is P70 Phase
6h plus the P72 repair note.  The phase does not use fit residuals, timing,
rank ladders, or implementation diffs as promotion evidence.  Its only
promotion criterion is classification discipline: a later design may use an
operation only after this phase classifies it and states what the classification
does and does not support.

## Local Checks And Inspected Inputs

Run time recorded in chat: 2026-06-17 11:54 HKT.

| Check/input | Outcome |
| --- | --- |
| `test -f docs/plans/bayesfilter-highdim-zhao-cui-p72-phase0-repair-note-closeout-result-2026-06-17.md` | Passed. |
| `test -d third_party/audit/tensor-ssm-paper-demo` | Passed. |
| Required `rg` source/governance search from the subplan | Passed, but broad search was noisy; Codex narrowed to listed ledgers and local source files. |
| Required `rg` stability/literature search from the subplan | Passed, but broad search was noisy; Codex treated uninspected stability literature as source gaps. |

Inspected local sources:

- bibliography entry for Zhao--Cui:
  `docs/references.bib:703-710`;
- P16 equation-by-equation ledger:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-equation-by-equation-ledger-2026-06-01.md:20-64`;
- P16 source-support ledger:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-source-support-ledger-2026-06-01.md:18-30`;
- P16 code crosswalk:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-code-crosswalk-ledger-2026-06-01.md:13-26`;
- P25 claim-support ledger:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p25-zhao-cui-claim-support-ledger-2026-06-02.md:21-31`;
- author source files:
  `third_party/audit/tensor-ssm-paper-demo/models/full_sol.m:21-136`,
  `third_party/audit/tensor-ssm-paper-demo/models/pre_sol.m:16-268`,
  `third_party/audit/tensor-ssm-paper-demo/models/computeL.m:1-47`,
  `third_party/audit/tensor-ssm-paper-demo/deep-tensor.dev/src/SIRT.m:1-87`,
  `third_party/audit/tensor-ssm-paper-demo/deep-tensor.dev/src/@TTSIRT/TTSIRT.m:1-253`,
  `third_party/audit/tensor-ssm-paper-demo/deep-tensor.dev/src/@TTSIRT/marginalise.m:1-87`,
  `third_party/audit/tensor-ssm-paper-demo/deep-tensor.dev/src/@DIRT/build.m:1-77`,
  `third_party/audit/tensor-ssm-paper-demo/deep-tensor.dev/src/@DIRT/build_bases.m:1-61`,
  `third_party/audit/tensor-ssm-paper-demo/deep-tensor.dev/src/Christoffel/ChristoffelSampling.m:1-37`;
- source-faithfulness prior audits:
  `docs/plans/bayesfilter-highdim-zhao-cui-p55-source-paper-code-discrepancy-audit-2026-06-10.md:50-87`,
  `docs/plans/bayesfilter-highdim-zhao-cui-p61-merged-source-faithfulness-reaudit-ledger-2026-06-12.md:19-49`;
- monograph local context:
  `docs/chapters/ch35_highdim_particle_transport_tensor_filters.tex:325-344`,
  `docs/chapters/ch35_highdim_particle_transport_tensor_filters.tex:399-419`,
  `docs/chapters/ch36_highdim_low_rank_density_filters_and_kr_maps.tex:151-181`.

## Repair-Operation Classification Ledger

| Operation family | Classification | Anchors and reasoning | Phase 2 consequence |
| --- | --- | --- | --- |
| Sequential TT/SIRT filtering route: propagate samples, form adjacent-state target, fit TT/SIRT, sample retained object, update log marginal likelihood | `source_faithful` for the broad route only | Paper ledger expands Zhao--Cui Algorithms 1--5 and Eqs. (9)--(35) in P16 lines 20--64.  Author `full_sol.solve` propagates samples and reapproximates at lines 21--43; `full_sol.reapprox` constructs the target and fits `TTIRT`/`TTSIRT` at lines 46--124. | Phase 2 may cite the broad route as the source route, but must not claim the fixed repair is the adaptive route. |
| Squared-TT density, positive defensive mass, normalizer, and marginalization | `source_faithful` for existence/role; details remain source-anchored, not proof | P16 source ledger allows squared-TT construction and marginalization claims at lines 18--23.  `SIRT` records approximation of the square root target and `tau` at lines 9--16 and constructs approximation/marginalization at lines 74--85.  `TTSIRT.defaultTau` is positive at lines 185--188.  `@TTSIRT/marginalise.m` sets `obj.z = obj.fun_z + obj.tau` at lines 15--87. | Phase 2 may require finite normalizer and defensive-mass diagnostics.  It must not choose a defensive mass by folklore; executable source versus script-declared `tau` ambiguity remains from P61. |
| KR/inverse/conditional transport operations | `source_faithful` for author-route existence | P16 ledger expands Eq. (17)--(26), Algorithms 3--4, and conditional maps at lines 43--55.  `TTSIRT.m` documents inverse/conditional/Rosenblatt tasks at lines 69--175. | Phase 2 may include branch identity for transport objects only as source-route context.  It must not require transport validation inside P72 lower-gate design. |
| Preconditioning route | `source_faithful` for author-route existence; not part of P72 repair unless separately chosen | P16 ledger expands Eqs. (30)--(35) and Algorithm 5 at lines 58--64.  `pre_sol.reapprox` constructs preconditioned and residual targets at lines 131--243 and proposal correction at lines 245--256. | Phase 2 should not include preconditioning unless it explicitly classifies a design branch for it.  P72 lower gate can remain unpreconditioned. |
| Weighted recentering, covariance/Cholesky frame, quantile scaling, finite-sample pruning | `source_faithful` for author route; fixed use is `fixed_hmc_adaptation` | `computeL.m` prunes `Inf`/`NaN`, normalizes weights, computes weighted mean/covariance/Cholesky, and applies quantile scaling at lines 14--47. | Phase 2 may use source-style frame diagnostics, but any frozen deterministic frame must be marked fixed-HMC adaptation. |
| Fixed ranks, bases, domains, samples, seeds, sweep schedules, branch identity, and beta branch | `fixed_hmc_adaptation` | P55 explicitly treats deterministic fixed/fixed-gradient branches as legitimate HMC carveout at lines 34--48 while excluding adaptive parity as required repair at lines 72--74.  Author SIR/PP scripts use random/adaptive `TTOption` settings and random seeds at `eg3_sir/mainscript.m:37-56` and `eg4_predatorprey/mainscript.m:43-79`. | Phase 2 may freeze these choices to define a same scalar, but cannot label that freeze as source-faithful adaptive reproduction. |
| UKF-guided center, scale, covariance orientation, or branch scout | `fixed_hmc_adaptation` if retained; otherwise source gap | P61 classifies UKF/rank calibration as a BayesFilter heuristic, not source route, at lines 28--29. | Phase 2 may use UKF only as a scout and must not use UKF as truth or promotion criterion. |
| Current objective-preserving column-scaled augmented ridge solve and condition-number gate | `fixed_hmc_adaptation`; source-faithfulness gap for author route | Current code says "stable solve is fixed_hmc_adaptation not source_faithful" in `bayesfilter/highdim/fitting.py:1067-1070`.  Author source uses TT/SIRT adaptive fit machinery rather than this TensorFlow fixed local solve. | Phase 2 may design conditioning gates around this fixed solver, but must label them fixed-variant stabilization. |
| Guard cloud, audit cloud, collocation residuals, holdout/replay residual gates, max residual gates, line-probe paths, line-growth ceilings, support-distance gates | `extension_or_invention` | P72 note proposes these to address P70 Phase 6h off-cloud growth.  No inspected author paper/source anchor shows finite guard clouds or line-probe admission gates as author-route requirements. | Phase 2 may design these only as P72 fixed-variant repair gates.  They do not close a Zhao--Cui source-faithfulness gap. |
| Shape penalties, derivative-energy penalties, line-growth objective penalties | `extension_or_invention` and literature/source gap | No inspected author anchor.  No local primary stable-LS technical anchor was checked in Phase 1 for these penalties. | Phase 2 may include these only as optional deferred candidates or must write a separate literature/derivation note before using them. |
| Christoffel/leverage/oversampling/stable-sampling ideas | candidate support; `extension_or_invention` if used in P72 | Author source contains `ChristoffelSampling.m` with a weight evaluator at lines 1--37, but Phase 1 did not inspect a paper theorem tying it to P72 guard design.  No local primary stable-LS source was closed in this phase. | Phase 2 should not make these mandatory unless it records them as candidate engineering support or opens a separate literature audit. |
| Rank-direction activity gates | `extension_or_invention` | They address P69/P70 fixed-variant inactive-direction hiding and Phase 6h/P72 gate discipline.  No author-route anchor was found. | Phase 2 may include activity diagnostics only as fixed-variant guardrails. |

## Source-Support And Source-Gap Ledger

| Source/support item | Status | Allowed use | Forbidden use |
| --- | --- | --- | --- |
| Zhao--Cui JMLR 2024, local bibliography key `zhao2024ttsequential` | `PRIMARY_TECHNICAL_SUPPORT` through prior P16/P25 checked ledgers for Eqs. (1)--(35), Algorithms 1--5, squared TT, KR maps, and preconditioning | Broad TT/SIRT filtering route, squared density, marginalization, KR map context, preconditioning context | Claim that P72 finite guard/max/line gates are author algorithm; claim adaptive branch differentiability; claim BayesFilter repaired diagnostic success |
| Author source `tensor-ssm-paper-demo` | `IMPLEMENTATION_EVIDENCE` for route existence and executable behavior | Source-route loop, sample push/reapproximation, `computeL`, TTSIRT construction, normalizer, transport sampling, proposal correction | Mathematical proof, Python production readiness, exact paper-figure reproduction |
| Oseledets TT and TT-cross references | `PRIMARY_TECHNICAL_SUPPORT` for TT format/TT-SVD via P1S; TT-cross primary source partially blocked | TT rank/storage/rounding caution; checked TT-cross context only where local source closure allows | Claim TT compression controls off-cloud residuals or P72 support stability |
| Cui--Dolgov squared inverse Rosenblatt transports | inherited support via P16/P25 and monograph context | Background for squared/KR transport concepts | New theorem-level claims about P72 guard design |
| Stable weighted least squares / Christoffel / leverage / oversampling literature | `SOURCE_GAP_BLOCKER` for theorem-level support in P72 | Mention as candidate direction only | Use as justification for a Phase 2 theorem or mandatory algorithmic default without checked technical anchors |

## Omitted-Paper And Reviewer-Risk Notes

- Stable polynomial least-squares sampling literature is the main omission risk
  if Phase 2 wants a theorem-level support statement for guard or collocation
  design.  Phase 1 did not perform network/API metadata lookup and did not
  inspect primary full text for Cohen--Davenport--Leviatan, Migliorati, Hampton
  and Doostan, Narayan, or related work.  This is acceptable only because
  Phase 2 can design a finite diagnostic gate without claiming a literature
  theorem.
- The author source contains Christoffel sampling code, but Phase 1 did not
  prove that the Zhao--Cui paper used Christoffel sampling for the P72 fixed
  guard problem.  It remains candidate implementation evidence, not source
  faithfulness for guard-cloud repair.
- Prior P55/P61 audits report source-route gaps and defensive-mass ambiguity.
  P72 must not silently use those as solved unless a later phase explicitly
  consumes and repairs them.

## Decision

`PHASE1_CLASSIFICATION_READY_FOR_PHASE2`

Phase 2 may design a finite-support-certified fixed lower gate using the P72
repair operations, but the classification boundary is binding:

- broad TT/SIRT/squared-density/KR/normalizer concepts are source-anchored;
- freezing the branch to define a differentiable scalar is a fixed-HMC
  adaptation;
- guard clouds, audit clouds, line probes, max residual gates, rank-activity
  gates, and conditioning admission are P72 fixed-variant stabilization
  additions unless a later source audit proves otherwise.

## Phase 2 Handoff

Phase 2 inherits:

- P70 Phase 6h failed evidence remains the baseline;
- no implementation or diagnostic execution has occurred in P72;
- source-faithfulness claims remain blocked unless they cite both paper and
  author-source line anchors;
- support-certified repair machinery must be labeled
  `extension_or_invention` or `fixed_hmc_adaptation` as classified above;
- thresholds, guard clouds, line-probe statistics, scaling conventions, and
  effective-rank conventions must be frozen in Phase 2 before implementation
  or diagnostic outputs are seen.

Required next artifact:

- `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase2-support-certified-design-subplan-2026-06-17.md`.
