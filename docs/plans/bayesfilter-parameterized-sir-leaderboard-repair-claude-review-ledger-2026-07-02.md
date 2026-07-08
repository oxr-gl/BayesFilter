# Claude Review Ledger: Parameterized Zhao-Cui SIR Leaderboard Repair

Date: 2026-07-02

## Role Contract

Codex is supervisor and executor.

Claude Opus max effort is a read-only reviewer only. Claude may inspect the
single requested path, report findings, and end with `VERDICT: AGREE` or
`VERDICT: REVISE`. Claude must not edit files, run experiments, launch agents,
or review the whole repository.

## Review Rounds

### Master Program Iteration 1

Command:

```text
bash scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name parameterized-sir-master-review-iter1 --model opus --effort max "<single-path bounded review prompt>"
```

Reviewed path:

- `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-master-program-2026-07-02.md`

Verdict:

- `VERDICT: REVISE`

Material findings:

- Primary pass criterion promoted finite value/score as a proxy for repaired
  leaderboard behavior.
- Baseline was not pinned to exact artifacts and commit.
- Stop conditions did not explicitly fail wrong row id/theta/provenance.
- Fixed source-parity and parameterized inference rows needed a no-comparison
  guard.
- Truth-theta legitimacy was not yet a direct gate.
- Governing facts needed file/test anchors.

Disposition:

- Accepted and patched in the master program, runbook, Phase 1 subplan, Phase 5
  subplan, and execution ledger.

### Master Program Iteration 2

Command:

```text
bash scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name parameterized-sir-master-review-iter2 --model opus --effort max "<single-path bounded rereview prompt>"
```

Reviewed path:

- `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-master-program-2026-07-02.md`

Verdict:

- `VERDICT: REVISE`

Material finding:

- Anticipated approval wording mentioned `HMC-readiness` even though this
  program only authorizes optional GPU/XLA smoke diagnostics.

Disposition:

- Accepted and patched.

### Target Contract Iteration 3

Command:

```text
bash scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name parameterized-sir-target-contract-review-iter3 --model opus --effort max "<single-path bounded target-contract rereview prompt>"
```

Reviewed path:

- `docs/plans/bayesfilter-parameterized-sir-target-contract-2026-07-02.md`

Verdict:

- `VERDICT: REVISE`

Material finding:

- Concrete published value/score implementation bindings were required but not
  yet instantiated.

Disposition:

- Accepted and patched by naming the candidate fixed-design TT value/score
  route and local model score hooks, with full-row admission still pending
  Phase 3.

### Target Contract Iteration 2

Command:

```text
bash scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name parameterized-sir-target-contract-review-iter2 --model opus --effort max "<single-path bounded target-contract rereview prompt>"
```

Reviewed path:

- `docs/plans/bayesfilter-parameterized-sir-target-contract-2026-07-02.md`

Verdict:

- `VERDICT: REVISE`

Material findings:

- Truth-theta semantics needed final binding.
- Published value and score needed binding to exact implementation
  paths/methods.
- Theta domain and finite evaluated-point veto needed to be explicit.

Disposition:

- Accepted and patched.

### Target Contract Iteration 4

Command:

```text
bash scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name parameterized-sir-target-contract-review-iter4 --model opus --effort max "<single-path bounded target-contract rereview prompt>"
```

Reviewed path:

- `docs/plans/bayesfilter-parameterized-sir-target-contract-2026-07-02.md`

Verdict:

- `VERDICT: REVISE`

Material findings:

- The reviewed theta domain needed an explicit boundary/corner admission
  diagnostic, not only a finite-point veto.
- The score-route proof or local math-contract citation needed to name the
  actual route, hooks, and tests.

Disposition:

- Accepted and patched in the target contract and semantic binding.

### Target Contract Iteration 5

Command:

```text
bash scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name parameterized-sir-target-contract-review-iter5 --model opus --effort max "<line-range bounded target-contract review prompt>"
```

Reviewed path:

- `docs/plans/bayesfilter-parameterized-sir-target-contract-2026-07-02.md`, selected line ranges.
- `docs/plans/bayesfilter-parameterized-sir-semantic-binding-2026-07-02.md`, selected line ranges.

Verdict:

- `VERDICT: AGREE`

Disposition:

- Phase 1 target contract review converged.

### Phase 2 Result Iteration 1

Command:

```text
bash scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name parameterized-sir-phase2-result-review-iter1 --model opus --effort max "<single-path bounded Phase 2 result review prompt>"
```

Reviewed path:

- `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase2-dataset-row-contract-result-2026-07-02.md`

Verdict:

- `VERDICT: AGREE`

Minor note:

- The result records one `rg` check with an ellipsis rather than full path
  list, but Claude did not treat this as material because manifest
  regeneration, focused tests, and nonclaims supplied the primary evidence.

Disposition:

- Phase 2 result review converged.

### Phase 3 Blocker Iteration 1

Command:

```text
bash scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name parameterized-sir-phase3-blocker-review-iter1 --model opus --effort max "<single-path bounded Phase 3 blocker review prompt>"
```

Reviewed path:

- `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase3-full-evaluator-result-2026-07-02.md`

Verdict:

- No usable verdict after repeated polling; worker was interrupted and
  returned `Execution error`.

Disposition:

- Followed runbook probe/narrowing path.

### Phase 3 Blocker Probe After Iteration 1

Command:

```text
bash scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name parameterized-sir-phase3-blocker-probe-after-iter1 --model opus --effort max "READ-ONLY PROBE ONLY. Return exactly CLAUDE_PROBE_OK."
```

Verdict:

- `CLAUDE_PROBE_OK`

Disposition:

- Claude was responsive; prompt was narrowed to exact line ranges.

### Phase 3 Blocker Iteration 1B

Command:

```text
bash scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name parameterized-sir-phase3-blocker-line-review-iter1b --model opus --effort max "<line-range bounded Phase 3 blocker review prompt>"
```

Reviewed paths:

- `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase3-full-evaluator-result-2026-07-02.md`, lines 33-79.
- `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase3-full-evaluator-blocker-2026-07-02.json`, lines 20-56.
- `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase4-score-validation-subplan-2026-07-02.md`, lines 5-34.

Verdict:

- `VERDICT: AGREE`

Disposition:

- Phase 3 blocker and Phase 4 stop boundary reviewed as internally
  consistent and boundary-safe.

### Visible Runbook Iteration 3

Command:

```text
bash scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name parameterized-sir-runbook-review-iter3 --model opus --effort max "<single-path bounded runbook rereview prompt>"
```

Verdict:

- No usable verdict. Interrupted after repeated no-output polling; worker
  returned `Execution error`.

Disposition:

- Followed runbook probe/narrowing path.

### Visible Runbook Probe After Iteration 3

Command:

```text
bash scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name parameterized-sir-runbook-probe-after-iter3 --model opus --effort max "READ-ONLY PROBE ONLY. Return exactly CLAUDE_PROBE_OK."
```

Verdict:

- `CLAUDE_PROBE_OK`

Disposition:

- Claude was responsive; prompt was narrowed to exact line ranges.

### Visible Runbook Iteration 3B

Command:

```text
bash scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name parameterized-sir-runbook-line-review-iter3b --model opus --effort max "<line-range bounded review prompt>"
```

Reviewed path:

- `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-visible-gated-execution-runbook-2026-07-02.md`, lines 41-43 and 149-173.

Verdict:

- `VERDICT: AGREE`

Disposition:

- Runbook review converged after probe and narrowed line-range review.

### Target Contract Iteration 1

Command:

```text
bash scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name parameterized-sir-target-contract-review-iter1 --model opus --effort max "<single-path bounded target-contract review prompt>"
```

Reviewed path:

- `docs/plans/bayesfilter-parameterized-sir-target-contract-2026-07-02.md`

Verdict:

- `VERDICT: REVISE`

Material findings:

- Ideal exact likelihood and operational approximate evaluator value/score were
  not semantically bound.
- Admission stop conditions were implicit.
- Score-at-true rule was referenced but not defined.
- Needed forbidden claim against exact-gradient-of-exact-likelihood language.

Disposition:

- Accepted and patched.

### Master Program Iteration 3

Command:

```text
bash scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name parameterized-sir-master-review-iter3 --model opus --effort max "<single-path bounded rereview prompt>"
```

Reviewed path:

- `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-master-program-2026-07-02.md`

Verdict:

- `VERDICT: AGREE`

Disposition:

- Master program review converged after three iterations.

### Visible Runbook Iteration 1

Command:

```text
bash scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name parameterized-sir-runbook-review-iter1 --model opus --effort max "<single-path bounded runbook review prompt>"
```

Reviewed path:

- `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-visible-gated-execution-runbook-2026-07-02.md`

Verdict:

- `VERDICT: REVISE`

Material findings:

- Claude review transport needed to be foreground/read-only, not a detached or
  nested launch loophole.
- Baseline artifacts needed checksums/content snapshots.
- Pass criterion needed semantic binding, not just row appearance.
- Old fixed row retirement required human authorization.
- Repeated local retry loops needed a cap.
- Phase results needed environment context.

Disposition:

- Accepted and patched in runbook, master, Phase 1, Phase 3, Phase 5, and
  execution ledger.

### Visible Runbook Iteration 2

Command:

```text
bash scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name parameterized-sir-runbook-review-iter2 --model opus --effort max "<single-path bounded runbook rereview prompt>"
```

Reviewed path:

- `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-visible-gated-execution-runbook-2026-07-02.md`

Verdict:

- `VERDICT: REVISE`

Material findings:

- Canonical semantic-binding artifact path was not pinned.
- If foreground Claude review remained unavailable after probe and narrowing,
  the runbook needed an explicit stop/handoff rule.

Disposition:

- Accepted and patched.
