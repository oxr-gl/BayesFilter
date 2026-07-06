# Actual-SIR Nystrom Stability Repair P04 Repair Selection Result

Date: 2026-06-23

Status: `SELECT_POSITIVE_PROJECTED_NYSTROM_DIAGNOSTIC_REPAIR`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Select an opt-in `positive_projected` Nystrom kernel diagnostic repair for P05 | `PASS`: exactly one repair family selected after P03 and Claude review | No default-policy, broad-grid, core-solver-only, or semantic-replacement veto remains | Positive projection may rescue `N=1024` rows while still being dense/diagnostic and not scalable; P05/P06 must prove behavior before any wider gate | Implement the opt-in mode in P05 and run focused tests with a discriminating floor-hit fixture | No repair effectiveness, no default readiness, no scalable/high-N readiness, no dense Sinkhorn equivalence, no posterior correctness, no HMC readiness |

## Evidence Contract Outcome

| Field | Outcome |
| --- | --- |
| Question | Which repair path is justified by P03 diagnostics without tuning after the fact? |
| Primary criterion | `PASS`: selected one path, opt-in positive-projected Nystrom kernel diagnostic repair. |
| Veto diagnostics | `PASS`: no multiple simultaneous repairs, no missing control, no unsupported default claim, no broad tuning grid. |
| Explanatory diagnostics | P03 scaling ranges nominated the repair family; they do not prove effectiveness. |
| Not concluded | Repair effectiveness deferred to P05/P06. |

## Review History

Claude P04 review round 1 returned `REVISE`:

- The initial `positive_clipped` scaling idea was not distinct enough because
  the existing raw Sinkhorn update already floors denominators.
- P05 needed a discriminating fixture so a no-op implementation could not pass.
- P05/P06 handoff needed explicit paired-comparison invariants.

P04/P05 were patched to select `kernel_mode="positive_projected"` instead.
Claude P04 review round 2 returned `VERDICT: AGREE`:

- `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p04-selection-claude-review-r2-2026-06-23.log`

## Selected Repair Contract

P05 will implement an opt-in Nystrom kernel mode:

- default remains `kernel_mode="raw"`;
- opt-in mode is `kernel_mode="positive_projected"`;
- the opt-in diagnostic may materialize the approximate Nystrom kernel
  internally at `N=1024` scale;
- it must project the approximate kernel elementwise to at least
  `denominator_floor` before Sinkhorn mass applications, residual/mass
  diagnostics, and final transport application;
- it must record raw kernel minimum, projected kernel minimum, and projection
  floor-hit count;
- it must not change rank/epsilon defaults, residual thresholds, paired
  thresholds, core solver, landmark selection, or default policy.

## Rejected Alternatives

| Alternative | Reason rejected |
| --- | --- |
| Another core-solver sweep | P09D already showed `svd_truncated,rcond=1e-6` did not rescue both failing rows, and P03 spectra were finite. |
| Broad rank/epsilon grid | P04 is a repair-selection gate, not a tuning or promotion grid. |
| Immediate fixed `rank=32,epsilon=0.5` policy closeout | Still possible later, but P03 provides a plausible focused repair to test first. |
| Positive-feature or low-rank-coupling route | Too broad and changes the transport object class. |

## Local Checks

```bash
python - <<'PY'
from pathlib import Path
checks = {
 'docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p04-repair-selection-subplan-2026-06-23.md': ['positive_projected','raw path already floors update denominators','projected-kernel diagnostics','P04 Skeptical Plan Audit','Forbidden Claims And Actions','Exact Next-Phase Handoff Conditions'],
 'docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p05-focused-repair-subplan-2026-06-23.md': ['kernel_mode="raw"','kernel_mode="positive_projected"','projection floor hits are positive','--nystrom-kernel-mode positive_projected','shape, seeds','paired thresholds'],
}
for path, needles in checks.items():
    text=Path(path).read_text()
    missing=[needle for needle in needles if needle not in text]
    if missing:
        raise SystemExit(f'{path}: missing {missing}')
print('P04/P05 focused revision check PASS')
PY
```

Result: `P04/P05 focused revision check PASS`.

## Inference Status

| Ledger | Status |
| --- | --- |
| Hard veto screen | `PASS` for selection; P05/P06 still pending. |
| Statistically supported ranking | `NO`. |
| Descriptive-only differences | P03 scaling ranges and residual magnitudes. |
| Default-readiness | `NO`. |
| Next evidence needed | P05 focused implementation tests, then P06 serious GPU repair gate if P05 passes. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Command | Local structural checks plus Claude read-only review rounds 1-2 |
| Environment | Repository docs/code review; no GPU row in P04 |
| GPU status | N/A |
| Data/model | P03 actual-SIR artifacts from seeds `81920..81924` |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p04-repair-selection-subplan-2026-06-23.md` |
| Result file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p04-repair-selection-result-2026-06-23.md` |

## Next Action

Open P05 and implement the opt-in `positive_projected` Nystrom kernel diagnostic
repair exactly as scoped in the refreshed P05 subplan.
