# SSL-LSTM Filter-HMC Visible Stop Handoff

Date: 2026-07-04

Status: `STOPPED_PENDING_PHASE3_REVIEW_DECISION`

## Stop Condition

The requested Claude review gate was rejected by the approval reviewer before
launch because it would send repo-local planning documents and possibly related
workspace context to an external Claude service. The user then authorized a
Codex-only local review exception for Phase 0 and directed continuation to
Phase 1. Phase 2 later reached the same material review boundary; after the
handoff identified the boundary, the user directed Codex to continue with the
runbook. Codex treated this as a Phase 2 no-export continuation only.

Phase 4 is now blocked for a different reason: the repository does not yet
contain an SSL-LSTM Zhao-Cui fixed-variant adapter to wire, so the blocker is
implementation availability rather than review logistics.

## Last Completed Phase

Phase 3 local checks passed for fixed SGQF and SVD-UKF analytic SSL-LSTM
adapters, but material review remains unresolved.

## Active Phase

Phase 4: Zhao-Cui fixed adapter, blocked by missing SSL-LSTM implementation
rather than by review logistics.

## Required Resume Action

Resume by reading:

- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-master-program-2026-07-04.md`
- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-visible-gated-overnight-execution-plan-2026-07-04.md`
- the latest phase result artifact
- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-claude-review-ledger-2026-07-04.md`

Then continue from the latest active phase result. The Phase 0 and Phase 2
exceptions are not blanket exceptions for future material Claude reviews or
external exports. Phase 4 stays blocked until a human-approved scope change
introduces an actual SSL-LSTM Zhao-Cui route; that blocker does not stop the
separate LEDH Phase 5 planning work. If Claude fails to return a material
verdict for a bounded review gate, Codex may substitute a separate local
read-only review on the same bounded bundle and record the fallback in the
review ledger before advancing.

The bounded Claude review gate for the Phase 4 blocker bundle did not return a
material verdict, so Codex executed the authorized local substitute review on
the same bounded bundle and recorded it in
`docs/reviews/ssl-lstm-phase4-blocked-codex-substitute-review.md`. The Phase 4
implementation blocker remains in force; only the review path fell back.

Phase 5 is also blocked: the current LEDH streaming value/score helper still
uses `tf.GradientTape`, and no manual VJP streaming-OT score path is available
to admit LEDH under this runbook. Phase 6 may proceed as benchmark-harness
planning over admitted adapters only, with Zhao-Cui and LEDH recorded as
blocked candidate statuses.

Phase 6 precheck is complete. No existing benchmark runner in the repo was
accepted as answering the SSL-LSTM invariant-metric contract. The next step is
to implement the Phase 6 benchmark harness and tests for admitted `fixed_sgqf`
and `svd_ukf` candidates only, while carrying `zhaocui_fixed` and
`ledh_streaming_ot` as blocked status rows.

Phase 6 is now complete with local checks and a persistent smoke artifact:
`docs/benchmarks/ssl_lstm_filter_hmc_phase6_shared_benchmark_cpu_hidden_2026-07-04.json`
and its Markdown companion. The runner is benchmark-only, uses the shared
deterministic SSL-LSTM fixture, records target-scope provenance, and keeps
`heldout_predictive_log_score` in proxy/explanatory status. Phase 7 may now be
refreshed for HMC mechanics and evidence ladder planning.
