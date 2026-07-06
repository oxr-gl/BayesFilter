# Actual-SIR Nystrom P05C High-N One-Seed Addendum

Date: 2026-06-22

Status: `SUPERSEDED_BY_RUNTIME_PROTOCOL_DIAGNOSTIC`

## Purpose

Adjust the actual-SIR Nystrom high-N ladder after the completed five-seed
evidence through `N=2048`.  Five seeds at `N=4096` and above are too expensive
for this stage.  This addendum originally converted `N=4096..65536` to a
one-seed feasibility/envelope screen, but it is now superseded for paired rows
because the P05B timing protocol was found to use a slow Python-level route loop
rather than the compiled production-style streaming path.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does Nystrom remain numerically valid and operationally feasible on actual-SIR d18 at larger particle counts? |
| Candidate | Nystrom `rank=32`, `epsilon=0.5`, `max_iterations=160`, active-all resampling. |
| Comparator | Streaming TF32 actual-SIR route only where feasible.  Paired evidence is optional beyond `N=4096`; Nystrom-only rows are envelope evidence only. |
| Seed policy | One seed only: `81120`. |
| Shape | `B=1,T=20,D=18,M=9`, particle counts `N=[4096,8192,16384,32768,65536]`. |
| Primary Nystrom-only pass criterion | JSON `status=PASS`, hard vetoes `[]`, actual-SIR semantics pass, route-fired count equals active steps, no materialized dense transport, finite outputs, final log-sum-exp residual `<=1e-5`, ESS fraction `>=0.01`, Nystrom residuals `<=5e-2`, GPU/TF32 provenance present. |
| Paired row criterion | If a paired row is launched, it must also pass paired log-likelihood/filter comparability thresholds. |
| Promotion role | One-seed high-N rows are feasibility/envelope evidence only. They cannot establish statistical ranking, default readiness, posterior correctness, or production superiority. |
| Stop condition | Stop at the first Nystrom hard veto, route execution error, timeout, nonfinite output, GPU unavailability, or artifact mismatch. |
| Explanatory diagnostics | Runtime, memory, warm-call timing, residual values below thresholds, ESS, landmarks, and GPU allocator state. |

## Skeptical Pre-Launch Audit

Status: `FAIL_FOR_PAIRED_SPEED_EVIDENCE_PASS_FOR_NYSTROM_ONLY_ENVELOPE`

The reduced one-seed ladder is acceptable only because the research question has
been narrowed from rigorous default promotion to high-N feasibility.  The
baseline/comparator remains the streaming TF32 route only for the optional
paired `N=4096` bridge; Nystrom-only rows at `N>=8192` must not be interpreted
as superiority, statistical ranking, posterior correctness, or default
readiness.  Runtime, memory, residual, and ESS diagnostics are either hard
vetoes under the thresholds above or explanatory envelope diagnostics; they are
not promotion criteria for a default policy.

Known risks are explicit: the paired `N=4096` row is not useful for speed
evidence under the current harness because P05B showed the streaming comparator
was run through a Python-level route loop with small chunks.  A same-GPU
compiled streaming sanity diagnostic at `B=5,T=20,N=2048` completed in
`20.397380776004866s` compile plus first call and `0.29988364898599684s` warm
call, while the P05B streaming warm call was `1160.5996048829984s`.  Therefore
same-protocol paired `N=4096` should not be launched until the Nystrom and
streaming routes are made comparable.  GPU selection must be freshly checked
before any Nystrom-only envelope launch, and output artifacts must preserve the
exact seed, shape, route, device, TF32 mode, and nonclaims.

## Launch Sequence

1. Do not run same-protocol paired `N=4096` until the runtime protocol is
   repaired.
2. If the purpose is high-N feasibility only, run `N=4096` Nystrom-only, one
   seed, timeout `3600s`.
3. Continue Nystrom-only to `N=8192`, `16384`, `32768`, `65536` only while each previous
   row passes and runtime remains acceptable.

## N4096 Paired Command Template

```bash
timeout 7200 python docs/benchmarks/benchmark_actual_sir_nystrom_default_promotion.py --route both --batch-seeds 81120 --time-steps 20 --num-particles 4096 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 128 --col-chunk-size 128 --particle-chunk-size 64 --nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --device-scope visible --cuda-visible-devices <0-or-1> --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu <0-or-1> --gpu-selection-note '<preflight selection note>' --phase-id ACTUAL-SIR-NYSTROM-P05C-ONE-SEED-PAIRED-N4096 --quiet --output docs/benchmarks/actual-sir-nystrom-default-promotion-p05c-one-seed-paired-n4096-2026-06-22.json --markdown-output docs/benchmarks/actual-sir-nystrom-default-promotion-p05c-one-seed-paired-n4096-2026-06-22.md
```

## Nystrom-Only Envelope Command Template

Replace `<N>` with the particle count.

```bash
timeout 3600 python docs/benchmarks/benchmark_actual_sir_nystrom_default_promotion.py --route nystrom --batch-seeds 81120 --time-steps 20 --num-particles <N> --transport-policy active-all --particle-chunk-size 64 --nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --device-scope visible --cuda-visible-devices <0-or-1> --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu <0-or-1> --gpu-selection-note '<preflight selection note>' --phase-id ACTUAL-SIR-NYSTROM-P05C-ONE-SEED-NYSTROM-N<N> --quiet --output docs/benchmarks/actual-sir-nystrom-default-promotion-p05c-one-seed-nystrom-n<N>-2026-06-22.json --markdown-output docs/benchmarks/actual-sir-nystrom-default-promotion-p05c-one-seed-nystrom-n<N>-2026-06-22.md
```
