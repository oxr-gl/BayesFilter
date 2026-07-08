# SSL-LSTM Phase 6 Shared Benchmark

- Schema: `ssl_lstm.filter_hmc.phase6_benchmark.v1`
- Status: `PHASE6_SHARED_BENCHMARK_READY`
- Git commit: `f98be292faabf3d1728f876ad211a70ac1ddf98c`
- Device: `/CPU:0`
- TF32: `disabled`

## Nonclaims

- shared benchmark harness only
- not HMC convergence evidence
- not posterior correctness evidence
- not filter sufficiency evidence
- not parameter-recovery evidence
- not a ranking claim
- parameter-by-parameter matching is not a primary criterion
- heldout predictive log score is a filter-likelihood proxy
- blocked candidate rows are status-only

## Candidate Status

| filter | status | target scope | gradient path | score finite | heldout predictive log score | decoded latent RMSE |
| --- | --- | --- | --- | --- | --- | --- |
| fixed_sgqf | admitted | ssl_lstm_filter_hmc:fixed_sgqf:phase3 | analytic_first_order_fixed_sgqf | True | 0.624174555480506 | 0.01975989748616466 |
| svd_ukf | admitted | ssl_lstm_filter_hmc:svd_ukf:phase3 | analytic_first_order_svd_ukf | True | 0.6241745156376752 | 0.019759891157126463 |
| zhaocui_fixed | admitted | ssl_lstm_filter_hmc:zhaocui_fixed:phase2 | analytic_first_order_zhaocui_fixed | True | 0.5626428710176841 | 0.06893349352719229 |
| ledh_streaming_ot | blocked | None | manual_vjp_streaming_ot | None | None | None |
