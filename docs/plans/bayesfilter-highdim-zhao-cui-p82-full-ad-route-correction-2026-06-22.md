# P82 Correction: Full Transport AD Is Not The N10000 Route

status: ACTIVE_CORRECTION
date: 2026-06-22

## Human Correction

The human owner pointed out that the `transport_ad_mode=full` route had already
been shown to be infeasible at `N=10000` because of memory/runtime explosion.
Retrying it in P82 was therefore not a new discriminating test.

## Correction

P82 remains useful as an FD-only same-scalar consistency program, but it is
now blocked on the availability of a memory-disciplined LEDH-PFPF-OT gradient
route.

The following is no longer an executable P82 validation route:

```text
N=10000, five seeds, streaming active-all LEDH-PFPF-OT,
transport_ad_mode=full, raw TensorFlow autodiff/JVP through Sinkhorn transport
```

This route is allowed only for tiny or small primitive diagnostics whose
purpose is local comparison, not for the governed `N=10000` actual-gradient
estimate.

## Prior Evidence

`docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3j-n10000-full-transport-fd-result-2026-06-19.md`
already recorded:

- reverse-gradient `N=10000`, `transport_ad_mode=full` OOM attempts at chunk
  sizes `4096`, `1024`, and `512`;
- a forward-JVP streaming full-AD run active for more than six hours with no
  result artifact;
- near-ceiling GPU memory on the 16 GB device;
- closure as `BLOCKED_RUNTIME_FEASIBILITY_RUN_ABORTED`.

P82 Phase 4 repeated the same bad structural route in shorter form:

- tiny GPU mechanics smoke passed;
- `N=10000`, five-seed, `transport_ad_mode=full` forward-JVP produced no
  output or progress artifact in the bounded window;
- GPU memory again approached the device ceiling;
- the run was interrupted and P4 was closed as
  `BLOCKED_RUNTIME_FEASIBILITY_N10000_FULL_TRANSPORT_ADONLY`.

## Revised Boundary

P82 must not launch the full `N=1000` regression-FD comparison until the LEDH
actual-gradient side is supplied by a reviewed memory-disciplined route.

The expected upstream route is the LEDH-PFPF-OT manual-adjoint/custom-gradient
program:

`docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-master-program-2026-06-22.md`

## Evidence Contract After Correction

| Field | Contract |
|---|---|
| Question | Can LEDH-PFPF-OT SIR d=18 gradients be checked against same-scalar regression FD once a memory-disciplined gradient route exists? |
| Comparator | Regression FD of the same LEDH scalar: 13 points, five seeds, `N=1000`, value-outlier trim, OLS on 11 retained mean values, slope SE recorded. |
| Actual-gradient route | `N=10000`, five seeds, but not raw/full autodiff through the whole Sinkhorn transport solve.  The route must be manual/custom adjoint or another reviewed memory-disciplined route. |
| Veto diagnostics | Any attempt to reuse `transport_ad_mode=full` raw AD/JVP as the governed `N=10000` route; FD promoted as oracle; missing SE; missing five seeds; missing 13/11 FD protocol; unsupported HMC/default/posterior/scientific-superiority claims. |
| Not concluded | No LEDH-vs-FD agreement, no HMC readiness, no default-gradient readiness, no posterior correctness, no exact likelihood correctness, no manual-adjoint correctness yet. |

## Decision

Close the current P82 execution path as downstream-blocked:

```text
BLOCKED_WAITING_FOR_MEMORY_DISCIPLINED_LEDHPFPFOT_GRADIENT_ROUTE
```

Create and execute a separate manual/custom-adjoint master program before
returning to P82 FD-only validation.
