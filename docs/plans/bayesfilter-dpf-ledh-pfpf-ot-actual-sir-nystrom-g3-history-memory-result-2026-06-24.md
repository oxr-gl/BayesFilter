# G3 Result: Fixed-Policy Full-History And Memory Gate

Date: 2026-06-24

Status: `G3_HISTORY_MEMORY_PASS`

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Close G3 as passed for the required full-history row and the optional `N=2048` row. |
| Primary criterion status | `PASS`: required `N=1024,T=20`, seeds `83920..83922`, full-history row passed; optional `N=2048,T=20`, seed `83920`, full-history row passed. |
| Veto diagnostic status | `PASS`: no hard vetoes, paired thresholds passed, fixed-policy metadata matched, GPU/TF32 evidence present, finite factors/particles true, and history payload shapes matched. |
| Main uncertainty | This is bounded memory/history evidence only; it does not establish broad memory scalability or handle the known seed `82921` hard case. |
| Next justified action | Draft and run G4 Nystrom-specific gradient mechanics smoke. |
| What is not being concluded | No default readiness, no broad memory scalability guarantee, no HMC readiness, no posterior correctness, no acceptance of seed `82921`. |

## Row Outcomes

| Row | Status | Hard vetoes | Paired mean delta | Paired max delta | History shapes | Wall seconds |
| --- | --- | --- | ---: | ---: | --- | ---: |
| `N=1024`, seeds `83920..83922` | `PASS` | `[]` | `3.0362345377604165` | `4.889892578125` | means/vars `[20,3,18]`, ESS `[20,3]` | `34.234880534000695` |
| `N=2048`, seed `83920` optional | `PASS` | `[]` | `2.61895751953125` | `2.61895751953125` | means/vars `[20,1,18]`, ESS `[20,1]` | `32.27259719790891` |

## Artifacts

- Summary JSON:
  `docs/benchmarks/actual-sir-nystrom-g3-history-memory-summary-2026-06-24.json`
- Required JSON:
  `docs/benchmarks/actual-sir-nystrom-g3-history-full-n1024-r32-eps0p5-2026-06-24.json`
- Required Markdown:
  `docs/benchmarks/actual-sir-nystrom-g3-history-full-n1024-r32-eps0p5-2026-06-24.md`
- Required log:
  `docs/plans/logs/actual-sir-nystrom-g3-history-full-n1024-r32-eps0p5-2026-06-24.log`
- Optional JSON:
  `docs/benchmarks/actual-sir-nystrom-g3-history-full-n2048-r32-eps0p5-2026-06-24.json`
- Optional Markdown:
  `docs/benchmarks/actual-sir-nystrom-g3-history-full-n2048-r32-eps0p5-2026-06-24.md`
- Optional log:
  `docs/plans/logs/actual-sir-nystrom-g3-history-full-n2048-r32-eps0p5-2026-06-24.log`

## Local Checks

G3 final artifact audit: `PASS`.

The audit verified status, hard vetoes, fixed-policy metadata, GPU/TF32
evidence, history mode, and full-history payload shapes for every launched row.

Focused implementation checks before G4 script work:

- `CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m py_compile docs/benchmarks/run_actual_sir_nystrom_gradient_mechanics_smoke.py`: `PASS`
- `CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_nystrom_transport_tf.py tests/test_actual_sir_nystrom_compiled_redo.py`: `13 passed`

## Inference Status

| Evidence class | Status |
| --- | --- |
| Hard veto screen | `PASS` for launched G3 full-history rows. |
| Statistically supported ranking | None. |
| Descriptive-only differences | Runtime, ESS, residual magnitudes, paired delta magnitudes. |
| Default-readiness | No. |
| Next evidence needed | G4 Nystrom-specific gradient mechanics smoke. |

## Post-Run Red-Team Note

Strongest alternative explanation: the tested full-history rows are bounded and
may not represent larger history/memory workloads.

What would overturn this result: a malformed history artifact, shape mismatch,
or rerun showing hard-veto failure under the same fixed policy.

Weakest part of the evidence: only one optional larger row was run, and G3 does
not address gradient mechanics, posterior correctness, HMC readiness, or seed
`82921`.
