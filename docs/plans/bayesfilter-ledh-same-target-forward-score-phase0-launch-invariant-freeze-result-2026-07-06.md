# Phase 0 Result: Launch And Invariant Freeze

Date: 2026-07-06

Status: `PASSED`

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Launch the new LEDH construction program. The corrected runbook now forces same-target observed-data likelihood scalar admission before any row score work. |
| Primary criterion status | Passed: the launch artifacts make the forward scalar the first repair target and sequence target/theta freeze, common API, model forward admission, manual score, tests, then leaderboard rebuild. |
| Veto diagnostic status | Passed: no inventory-only closure path remains, no score-before-scalar phase is present, no proposal scalar is treated as the leaderboard value, and no authority was transferred to Claude. |
| Main uncertainty | Phase 1 must still freeze the actual-SV raw/transformed target and the fixed-SIR nonempty-score policy before implementation can begin. |
| Next justified action | Advance to Phase 1 row target and theta freeze. |
| What is not concluded | No code repair, no row admission, no score correctness, no HMC readiness, and no leaderboard promotion. |

## Question Answered

Phase 0 asked:

- Does the new program force same-target likelihood scalar construction before
  score work?

Answer:

- Yes.

The launch artifacts now state that the row value must be `log p_theta(y_1:T)`
or the finite-`N`, fixed-randomness LEDH estimator of that exact scalar, and
that no row score work may begin before same-target forward scalar admission.

## Checks Run

```bash
git diff --check -- docs/plans/bayesfilter-ledh-same-target-forward-score-*.md docs/reviews/ledh-same-target-forward-score-launch-review-bundle-2026-07-06.md
```

Result: passed.

```bash
rg -n "log p_theta\\(y_1:T\\)|No LEDH score work may begin|wrong relative to the stated target|proposal|leaderboard rebuild|score before scalar|inventory-only" docs/plans/bayesfilter-ledh-same-target-forward-score-*.md docs/reviews/ledh-same-target-forward-score-launch-review-bundle-2026-07-06.md
```

Result: passed.

```bash
rg -n "GradientTape|ForwardAccumulator|callback existence|scoped SIR|fixed SIR|no_free_theta|N=10000|Claude is a read-only reviewer" docs/plans/bayesfilter-ledh-same-target-forward-score-*.md docs/reviews/ledh-same-target-forward-score-launch-review-bundle-2026-07-06.md
```

Result: passed.

Claude review:

- `REVIEW_STATUS=agreed`
- `VERDICT=AGREE`
- run dir:
  `/home/chakwong/BayesFilter/.claude_reviews/20260706-040854-ledh-same-target-forward-score-launch`

## Evidence Contract Result

| Field | Status |
| --- | --- |
| Question | Answered directly: the plan now requires same-target likelihood admission before score work. |
| Baseline/comparator | Passed: prior closeout, July 5 score-memory result, and corrected user instruction align with the new launch artifacts. |
| Primary criterion | Passed: construction-first sequencing is explicit. |
| Veto diagnostics | Passed: no score-before-scalar or inventory-only launch path remains. |
| Explanatory diagnostics | Historical blocker artifacts remain useful inputs for Phase 1 row target freeze. |
| Not concluded | No code or model row has changed yet. |

## Next-Phase Handoff

Phase 1 should now freeze:

- each row's exact observed-data likelihood target;
- each row's free theta vector and score dimensionality;
- actual-SV raw-versus-transformed target policy;
- the fixed SIR row's free-theta policy, now amended by human direction to use
  the existing `sir_log_scale_theta` model-parameter surface at truth theta
  `[0,0,0]`.
