# P57-M1 Claude Read-Only Review

metadata_date: 2026-06-11
phase: P57-M1
reviewer: Claude Code Opus max-effort, read-only
supervisor: Codex

## Iteration 1 Full Prompt

Verdict:

`VERDICT: AGREE`

Summary:

- Claude agreed the M1 primary criterion is satisfied.
- Claude agreed `zhao_cui_sir_austria_model()` matches author setup, ordering,
  parameters, initial mean, covariance/noise, ODE adjacency, transition density,
  transition push/clipping, likelihood, prior, and author RK convention.
- Claude agreed `transition_push_from_standard_normal` is a valid fixed-HMC
  adaptation of the MATLAB random push.
- Claude agreed the old `p30_spatial_sir_fixture_model` is correctly kept as an
  extension/diagnostic fixture for P57.
- Claude agreed M1 does not overclaim later transport/filtering/rank/HMC
  success.
- Claude noted one non-blocking nit: MATLAB `like.mlx` has a NaN-to-zero guard.

## Iteration 1 Verbatim Findings

```text
- Primary criterion is satisfied. The subplan requires a parity ledger covering state ordering, parameters, transition density, push/noise, prior, likelihood, observation indexing, covariance choices, and fixed-HMC adaptations; the result note records all of those explicitly and keeps the veto boundary in place (`docs/plans/bayesfilter-highdim-zhao-cui-p57-m1-author-model-callback-parity-subplan-2026-06-11.md:9-13`, `docs/plans/bayesfilter-highdim-zhao-cui-p57-m1-author-model-callback-parity-result-2026-06-11.md:10-16`, `:21-43`).

- `zhao_cui_sir_austria_model()` matches the author callback contract on the items you asked to check. In BayesFilter it is `d=0`, `m=18`, `n=9`, state ordered as `(S_1,I_1,...,S_9,I_9)`, with shared `kappa=0.1`, `nu=18`, initial pairs `[486+j, 14-j]`, `Q=I`, `R=100 I`, prior `N(priormean, I)`, infectious-only observation map, and the author-specific 9-node adjacency (`bayesfilter/highdim/models.py:431-498`, `:572-620`, `:674-692`, `:1046-1061`). The focused parity test file independently reconstructs the author adjacency and RK step and checks factory contract, transition mean, likelihood indexing, clipping behavior, and old-fixture separation (`tests/highdim/test_p57_m1_author_sir_callback_parity.py:7-57`, `:60-149`).

- `transition_push_from_standard_normal` is a valid fixed-HMC adaptation, not route drift. The author source push is `sir_step(prev, theta) + sigma1*randn`, then clip susceptible coordinates only; BayesFilter implements exactly the same route with caller-supplied standard-normal noise and Cholesky scaling, followed by susceptible-only clipping (`bayesfilter/highdim/models.py:466-481`, `:642-650`, `:674-692`). For this author model, `process_covariance = I` and `sigma1 = 1`, so the helper is a replayable replacement for MATLAB randomness rather than a changed transition rule.

- The old `p30_spatial_sir_fixture_model` is correctly kept as extension/diagnostic, and the result note does not overclaim later phases. The old fixture remains a chain graph with shifted initial pairs, classical RK4, and no post-noise susceptible clipping (`bayesfilter/highdim/models.py:654-671`), and the tests explicitly keep it separate from the author target (`tests/highdim/test_p57_m1_author_sir_callback_parity.py:143-149`, `tests/highdim/test_p30_spatial_sir.py:168-179`). The result note explicitly says M1 concludes no transport correctness, filtering success, rank correctness, HMC readiness, d=18 success, d=50/d=100 success, adaptive parity, S&P reproduction, or smoothing support (`docs/plans/bayesfilter-highdim-zhao-cui-p57-m1-author-model-callback-parity-result-2026-06-11.md:13-16`, `:92-97`).

- Non-blocking nit only: MATLAB `like.mlx` contains a `pdf(isnan(pdf)) = 0` guard, while `observation_log_density` is a straight log-Gaussian evaluation on the finite-input path. I do not think that blocks M1, because this milestone is about source-target callback identity on the declared formulas, not NaN-handling policy.

VERDICT: AGREE
```

## Compact Retry

The original full prompt was slow, so Codex also sent a compact prompt after a
minimal probe returned `PROBE_OK`.  The compact retry also returned:

`VERDICT: AGREE`

```text
- No material mismatch found. `zhao_cui_sir_austria_model()` in `bayesfilter/highdim/models.py:674` matches the author `sir_austria` callbacks on the checked M1 items: setup/prior mean and variances, odd-index infectious observation matrix, 9-node adjacency, author-specific 4x0.005 RK variant with the half-step fourth stage, Gaussian transition/likelihood/prior structure, and susceptible-only post-noise clipping in the push path (`bayesfilter/highdim/models.py:445`, `bayesfilter/highdim/models.py:466`, `bayesfilter/highdim/models.py:483`, `bayesfilter/highdim/models.py:612`, `bayesfilter/highdim/models.py:642`, `bayesfilter/highdim/models.py:1046`). The dedicated checks in `tests/highdim/test_p57_m1_author_sir_callback_parity.py:61` cover the source-faithful factory contract, transition mean, observation indexing, clipping policy, and separation from the older fixture.
- No demotion/overclaim issue found. The old `p30_spatial_sir_fixture_model()` remains clearly separate as a clean-room fixture (`bayesfilter/highdim/models.py:654`) and is explicitly tested as not equal to the author target in `tests/highdim/test_p57_m1_author_sir_callback_parity.py:144`. The result note keeps later transport/filtering/rank/HMC claims out of scope rather than promoting them (`docs/plans/bayesfilter-highdim-zhao-cui-p57-m1-author-model-callback-parity-result-2026-06-11.md:10`, `docs/plans/bayesfilter-highdim-zhao-cui-p57-m1-author-model-callback-parity-result-2026-06-11.md:15`, `docs/plans/bayesfilter-highdim-zhao-cui-p57-m1-author-model-callback-parity-result-2026-06-11.md:39`).

VERDICT: AGREE
```
