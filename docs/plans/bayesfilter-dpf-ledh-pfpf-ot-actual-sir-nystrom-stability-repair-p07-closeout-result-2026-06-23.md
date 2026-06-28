# Actual-SIR Nystrom Stability Repair P07 Closeout Result

Date: 2026-06-23

Status: `REPAIR_FAILED_OR_BLOCKED`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Close the master program as `REPAIR_FAILED_OR_BLOCKED` | `PASS`: final handoff separates finite rescue from paired-comparability failure | P06 hard veto remains active: paired max log-likelihood delta exceeded threshold | A less intrusive repair may preserve paired comparability, but it needs a new reviewed plan | Stop this master program; do not reopen P09/P10 from this result | No default readiness, no repair success, no broad robustness/unusability, no ranking, no posterior correctness, no dense equivalence, no scalable/high-N readiness, no HMC readiness |

## Program Summary

P03 localized the known failures:

- `rank=32,epsilon=0.25`: `T=2` passed, `T=4` failed by row residual.
- `rank=64,epsilon=0.3`: `T=2` passed, `T=4` failed by residual and nonfinite
  particles.
- `rank=32,epsilon=0.5` control passed at `T=4` and `T=20`.

P04 selected one focused repair family after Claude review:

- opt-in `kernel_mode="positive_projected"` Nystrom kernel diagnostic.

P05 implemented the opt-in mode and passed focused checks:

- `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_nystrom_transport_tf.py tests/test_actual_sir_nystrom_compiled_redo.py`
- Result: `10 passed`.

P06 ran the first required serious GPU repair row:

- `rank=32,epsilon=0.25`
- `--nystrom-kernel-mode positive_projected`
- GPU1 selected after trusted preflight.

P06 result:

- Nystrom route status: `PASS`;
- finite factors: true;
- finite particles: true;
- projection floor hits: `95517.0`;
- max row residual: `0.001790761947631836`;
- max column residual: `7.62939453125e-06`;
- aggregate status: `FAIL`;
- hard veto: `paired:paired_log_likelihood_max_abs_delta`;
- observed paired max delta: `12.91107177734375`;
- threshold: `10.0`.

## Final Handoff

`REPAIR_FAILED_OR_BLOCKED`

The positive projection repaired finite/residual behavior on the first failing
row, but it did not preserve paired comparability.  Therefore P09/P10 remain
blocked.

## Artifacts

- Master program:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-master-program-2026-06-23.md`
- Visible runbook:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-visible-gated-execution-runbook-2026-06-23.md`
- Execution ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-visible-execution-ledger-2026-06-23.md`
- Review ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-claude-review-ledger-2026-06-23.md`
- Stop handoff:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-visible-stop-handoff-2026-06-23.md`
- P03 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p03-minimal-ablations-result-2026-06-23.md`
- P04 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p04-repair-selection-result-2026-06-23.md`
- P05 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p05-focused-repair-result-2026-06-23.md`
- P06 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p06-p09-regate-decision-result-2026-06-23.md`
- P06 row:
  `docs/benchmarks/actual-sir-nystrom-stability-repair-p06-positive-projected-r32-eps0p25-2026-06-23.json`

## Local Closeout Check

```bash
python - <<'PY'
from pathlib import Path
required = [...]
...
print('P07 artifact/status check PASS')
PY
```

Result: `P07 artifact/status check PASS`.

## Inference Status

| Ledger | Status |
| --- | --- |
| Hard veto screen | `FAIL` in P06 due to paired max threshold. |
| Statistically supported ranking | `NO`. |
| Descriptive-only differences | Projection hits, residuals, runtime, and per-seed deltas. |
| Default-readiness | `NO`. |
| Next evidence needed | New reviewed subplan only: fixed-policy closeout or less intrusive repair preserving paired comparability. |

## Post-Run Red Team

Strongest alternative explanation: `positive_projected` may be too strong a
semantic modification.  It restores finite residual-valid transport but changes
the actual filtering computation enough to violate paired likelihood
comparability.

What would overturn this closeout: a reviewed follow-up repair that keeps the
same failing row finite, keeps residuals below threshold, records that the
repair path is exercised, and passes the original paired thresholds without
changing thresholds after observing results.

## Stop Rule

This master program is closed.  Do not launch more phases from it.
