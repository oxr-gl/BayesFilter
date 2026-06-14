# P12 Zhao-Cui TT Claude Review Ledger

metadata_date: 2026-05-31

seed_papers:
- P12 proof-expansion plan.
- P12 proof-expansion note.
- Zhao-Cui JMLR 2024.
- Cui-Dolgov 2022.

what_is_not_concluded:
- Claude review is not mathematical certification.
- Claude review is not source-completeness proof.
- Claude review is not HMC readiness.

## Plan Review Iteration 1

Command:

```text
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name highdim-p12-zhao-cui-tt-proof-expansion-plan-review-iter1 --model sonnet --effort high "<bounded hostile plan review prompt>"
```

Result:
`REJECT`

Major findings:
- the plan did not force the policy-required scoped source-support,
  claim-support, snowball/omission, and quarantine/version checks;
- no explicit retraction/quarantine/version-conflict checks were forced;
- no scoped omission-risk gate was forced;
- Proposition 2 needed clearer separation between assumed differentiability of
  exogenous maps and derived differentiability of TT cores.

Codex disposition:
Accepted.  Codex patched the plan to add source-support, claim-support,
coverage-and-omission, and quarantine/version requirements.

## Plan Review Iteration 2

Command:

```text
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name highdim-p12-zhao-cui-tt-proof-expansion-plan-review-iter2 --model sonnet --effort high "<bounded hostile plan review prompt>"
```

Result:
`ACCEPT`

Residual risks:
- execution must actually classify omitted foundational/background sources;
- the fixed branch must be precise enough in the final note;
- the scoped audit is narrower than a full literature survey, which is
  acceptable only because P12 is a local proof note.

## Execution Review

### Iteration 1

Command:

```text
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name highdim-p12-zhao-cui-tt-proof-expansion-exec-review-iter1 --model sonnet --effort high "<bounded hostile execution review prompt>"
```

Result:
`REJECT`

Major findings:
- compiled PDF was missing at the time Claude reviewed;
- Proposition 2 sketched the previous-filter numerator derivative but did not
  prove it inside the proposition-proof block;
- source/code anchors in the note were too coarse;
- fixed interpolation and least-squares sensitivity formulas needed more
  derivational bridge from the declared scalar to the same computation path;
- execution ledgers still recorded pending/in-progress status.

Codex disposition:
Accepted.  Codex compiled the PDF, moved the core-sensitivity and
previous-filter derivative material into the Proposition 2 proof, added the
explicit previous-marginal derivative formula, and tightened the note's
source-anchor section with equation/proposition/algorithm numbers.

### Iteration 2

Command:

```text
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name highdim-p12-zhao-cui-tt-proof-expansion-exec-review-iter2 --model sonnet --effort high "<bounded hostile execution review prompt>"
```

Result:
`ACCEPT`

Residual risks recorded by Claude:
- the final boxed score assumes fixed normalized \(\lambda_t\); future
  parameter-dependent defensive densities would need the extra term already
  discussed in the proof;
- least-squares sensitivity is human-reviewed rather than fully
  machine-certified;
- the note is readable for a mixed numerical panel but still dense.

Codex disposition:
Accepted.  These are residual limits rather than blockers.
