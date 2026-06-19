# P75 Phase 7 Result: UKF/Source-Guided Initializer Design

metadata_date: 2026-06-18
status: PHASE7_DESIGN_PASSED_LOCAL_CHECKS_CLAUDE_AGREE_READY_FOR_PHASE8
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p75-stochastic-density-training-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p75-visible-gated-execution-runbook-2026-06-17.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p75-phase7-ukf-source-guided-initializer-subplan-2026-06-18.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p75-phase6-guided-warm-start-smoke-result-2026-06-18.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Scientific/engineering question | What is the smallest coherent guide-informed initializer that can build on the Phase 6 scale fix without pretending that the constant warm start solved the fit? |
| Exact baseline/comparator | Phase 6 same-draw random-vs-calibrated-constant warm-start smoke. |
| Primary criterion | Satisfied locally by selecting one bounded implementation target: an opt-in source-guided square-root prefit initialized from the calibrated constant and followed by the existing P75 density objective. |
| Diagnostics that can veto | No audit-data use, no lower-gate claim, no UKF-as-truth claim, no full Gaussian TT projection claim, no larger pilot launch, and no default behavior change. |
| Explanatory only | Phase 6 residual magnitudes, UKF scout metadata, source-route anchor cloud, line-gate failure, training loss traces. |
| What is not concluded | No lower-gate repair, validation readiness, HMC readiness, scaling, rank/sample policy, source-faithful Zhao--Cui parity, or full UKF initializer success. |
| Artifact preserving result | This design result, Phase 8 subplan, amended master/runbook, ledgers, Claude review. |

## Why We Amend P75 Instead Of Creating A New Master Program

The current question is still inside the P75 scientific thread.  P75 asks
whether stochastic differentiable density training can repair the fixed
variant's lower-gate failure after the undersampled ALS route collapsed.
Phase 6 showed that one failure mode is not only sample count or optimizer
choice: random TT square-root initialization makes
\[
    \rho_\theta(z)=h_\theta(z)^2+\tau q_0(z)
\]
nearly equal to the defensive floor in 36 dimensions.  A guided constant
initializer fixed scale and gradient flow, but not target geometry.

Therefore the right governance action is to amend the existing P75 master
program with Phases 6--9.  A new master program would be appropriate only if
we abandoned P75 and started a separate algorithmic lane, for example a full
UKF-filter replacement or a source-faithful adaptive Zhao--Cui reproduction.
That is not the current action.

## Mathematical Design

Let \(z\in\mathcal D\subset\mathbb R^d\) be the source-route local coordinate
and \(r=\mu+Lz\) the frozen physical coordinate map used by the fixed branch.
The source-route target evaluator provides the shifted square-root target
\[
    y(z)=\exp\{-\ell_{\rm sh}(z)/2\},
\]
where \(\ell_{\rm sh}\) is the shifted local negative log target.  P75 uses
the trainable density
\[
    p_\theta(z)
    =
    \frac{\rho_\theta(z)}{Z_\theta},
    \qquad
    \rho_\theta(z)=h_\theta(z)^2+\tau q_0(z),
    \qquad
    Z_\theta=\int_{\mathcal D}\rho_\theta(z)\,d\omega(z).
\]

The stochastic density objective already implemented is the empirical
cross-entropy form
\[
    \mathcal L_{\rm CE}(\theta;B)
    =
    -\sum_{i\in B}\alpha_i\log\rho_\theta(z_i)
    +\log Z_\theta
    +\lambda \|\theta\|_2^2,
    \qquad
    \alpha_i
    \propto
    w_i\{y(z_i)^2+\tau q_0(z_i)\}.
\]
Up to the entropy of the sampled target, this is the forward
\(\mathrm{KL}\{p_\star\|p_\theta\}\) for the source-route training cloud.

The new initializer should not replace this objective.  It should place
\(h_\theta\) in the right scale and rough geometry before cross-entropy
training.  The selected prefit objective is
\[
    \mathcal L_{\rm pre}(\theta;G)
    =
    \frac{\sum_{i\in G} w_i\{h_\theta(z_i)-y(z_i)\}^2}
         {\sum_{i\in G} w_i\,y(z_i)^2+\epsilon}
    +\lambda_{\rm pre}\|\theta-\theta_{\rm const}\|_2^2 .
\]
Here \(G\) is a guide cloud drawn only from training-eligible source-route
clouds, \(\theta_{\rm const}\) is the calibrated constant initializer from
Phase 6, and \(\epsilon>0\) is a fixed numerical scale floor.  This prefit is
not a validation criterion.  It is a warm start for the actual P75
cross-entropy objective.

## Role Of UKF Guidance

The UKF scout contributes geometry, not truth.  Its allowed outputs are
centers, scales, covariance spectra, effective dimensions, and correlation
structure.  In the notation of p50/P70, the UKF can help choose or sanity-check
\[
    \mu,\quad L,\quad \mathcal D,\quad b_{1:d},\quad r,
\]
and can suggest which directions need larger rank or denser sampling.  It
does not directly provide \(y(z)\), \(p_\star(z)\), or a correct likelihood.

For this repository's current code surface, the source-route branch already
constructs a local frame and training clouds, while the UKF scout is available
as `scout_not_truth` metadata.  A full analytic Gaussian-to-TT initializer
\[
    h_0(z)\approx C\exp\{-\tfrac14(z-m)^\top\Sigma^{-1}(z-m)\}
\]
would require a reviewed TT projection or cross approximation surface that is
not currently present.  Phase 8 therefore should not attempt that full route.

The smallest implementable UKF/source-guided step is:

1. Use the source-route frame and training target evaluator to obtain
   \(G=\{(z_i,y_i,w_i)\}\).
2. Initialize \(h_\theta\) by the Phase 6 calibrated constant.
3. Run a small number of supervised square-root prefit steps on \(G\), or on
   renewed training-eligible guide batches.
4. Hand the resulting \(\theta_{\rm pre}\) to the existing P75
   cross-entropy objective.
5. Audit only on fresh holdout/replay/line samples that were not used in
   initialization, prefit, stopping, or hyperparameter selection.

This is source-guided immediately and UKF-compatible structurally.  It is not
a full UKF Gaussian TT initializer.

## Selected Phase 8 Implementation Target

Phase 8 should implement exactly one opt-in mode:

`source_guided_prefit`

The mode should:

- start from `calibrated_constant`;
- run bounded supervised square-root prefit steps using only
  training-eligible source-route batches;
- record guide provenance, prefit losses, prefit step count, and audit
  exclusion;
- then run the existing P75 density objective;
- compare against random and calibrated-constant arms on identical target,
  training, and audit draws in a tiny CPU-only smoke.

The first tiny diagnostic should be intentionally small, for example degree 1
or 2, rank 1 or 2, batch size no larger than 64, prefit steps no larger than
20, density-objective batches no larger than 4, and no GPU.  It should answer
only whether a nonconstant guide prefit improves geometry over the constant
warm start without introducing provenance or numerical failures.

## Required Evidence For Phase 8

The Phase 8 tiny test may pass only if:

- all arms use identical source-route target and audit draws, except for the
  intended initializer/prefit difference;
- `source_guided_prefit` has finite prefit loss, finite objective terms,
  finite gradients, and finite parameters;
- audit data are excluded from initialization, prefit, stopping, and
  hyperparameter selection;
- the prefit arm materially improves at least one geometry diagnostic over
  calibrated constant, such as holdout RMS relative, line RMS residual, or
  replay RMS relative, under a frozen criterion declared before the run;
- the result explicitly says that passing the tiny diagnostic is not
  lower-gate repair.

The prefit arm may still fail audit gates.  That would not make Phase 8 a
failure if the declared mechanism criterion passes; it would mean the next
action must remain a bounded design or tuning phase rather than a larger pilot.

## Code Surface Map

Current relevant surfaces:

- `bayesfilter/highdim/stochastic_density_training.py`: trainable
  `P75TrainableTTConfig`, `P75ObjectiveBatch`, `TrainableFunctionalTT`,
  `rho_theta`, exact normalizer, cross-entropy objective, and optimizer step.
- `scripts/p75_stochastic_density_training_pilot.py`: target context,
  source-route target values, random/calibrated initializer modes, same-draw
  compare mode, JSON manifest.
- `tests/highdim/test_p75_stochastic_density_training.py`: focused unit tests
  for trainable TT mechanics and the calibrated initializer.
- `bayesfilter/highdim/ukf_scout.py`: UKF `scout_not_truth` metadata.
- `docs/plans/bayesfilter-highdim-zhao-cui-p50-chapter-discipline-rewrite-2026-06-12.tex:9311`:
  monograph UKF scout role and nonclaims.
- `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase1-mathematical-fixed-branch-contract-result-2026-06-16.md`:
  fixed-branch and UKF-scout claim boundaries.

Missing surfaces for Phase 8:

- a `source_guided_prefit` initializer mode;
- a prefit loss/step on `TrainableFunctionalTT`;
- CLI flags for bounded prefit step count and comparison;
- manifest fields recording train-only guide provenance;
- tests that prefit reduces a synthetic square-root residual and does not use
  audit records.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Amend P75 and implement a bounded `source_guided_prefit` mode next | Satisfied locally for design | No audit-data use or lower-gate overclaim in design | Whether a tiny prefit improves geometry beyond constant scale | Draft and review Phase 8 implementation subplan | No lower-gate repair, validation/HMC readiness, scaling, rank/sample policy, source-faithfulness, or full UKF initializer success |

## Local Checks Planned

```text
rg -n "Phase 7|Phase 8|source_guided_prefit|UKF/source-guided|not lower-gate" docs/plans/bayesfilter-highdim-zhao-cui-p75-*.md
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p75-stochastic-density-training-master-program-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p75-visible-gated-execution-runbook-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p75-phase7-ukf-source-guided-initializer-design-result-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p75-phase8-source-guided-prefit-implementation-subplan-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p75-visible-execution-ledger-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p75-claude-review-ledger-2026-06-17.md
```

## Skeptical Plan Audit

The design passes the skeptical audit locally because it uses the actual Phase
6 result as baseline, does not treat audit residuals or training loss as
validation, separates UKF geometry from source-route target evaluation, selects
one bounded implementation target, forbids the larger pilot, and preserves
audit holdout as certification-only data.

## Local Checks

Passed:

```text
rg -n "Phase 7|Phase 8|source_guided_prefit|UKF/source-guided|not lower-gate|lower-gate repair|source-faithful|degree 2/rank 4|1024|500" docs/plans/bayesfilter-highdim-zhao-cui-p75-stochastic-density-training-master-program-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p75-visible-gated-execution-runbook-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p75-phase7-ukf-source-guided-initializer-design-result-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p75-phase8-source-guided-prefit-implementation-subplan-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p75-visible-execution-ledger-2026-06-17.md
```

Passed:

```text
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p75-stochastic-density-training-master-program-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p75-visible-gated-execution-runbook-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p75-phase7-ukf-source-guided-initializer-design-result-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p75-phase8-source-guided-prefit-implementation-subplan-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p75-visible-execution-ledger-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p75-claude-review-ledger-2026-06-17.md
```

Result:

```text
no output
```

## Claude Review

Claude reviewed the amended master/runbook, Phase 6 result, Phase 7 subplan,
this Phase 7 design result, and the Phase 8 subplan.  Claude returned
`VERDICT: AGREE`.

Claude agreed that amending P75 instead of creating a new master program is
logically consistent, that Phase 7 follows from Phase 6 without overclaiming,
that Phase 8 has sufficient entry conditions/artifacts/checks/evidence
contract/forbidden actions/handoff/stop conditions, and that Phase 7 produces
the plan-level prerequisites Phase 8 needs.
