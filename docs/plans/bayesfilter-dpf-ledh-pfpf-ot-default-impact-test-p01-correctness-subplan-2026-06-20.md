# P01 Subplan: Small Deterministic Correctness Gate

Date: 2026-06-20

## Phase Objective

Run the smallest deterministic streaming LEDH-PFPF-OT correctness gate to check
fixed-branch accounting, finite outputs, shape/device metadata, and FP64
reference preservation before any trusted GPU precision or target-shape runs.

## Entry Conditions Inherited From Previous Phase

- P00 governance artifacts exist and passed review.
- GPU TF32 LEDH-PFPF-OT remains the default target by owner directive.
- No benchmark result has yet shown target-shape viability in this ladder.
- Peer low-rank artifacts and unrelated HMC dirty files remain out of scope.

## Required Artifacts

- JSON:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p01-correctness-cpu-2026-06-20.json`
- Markdown:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p01-correctness-cpu-2026-06-20.md`
- P01 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p01-correctness-result-2026-06-20.md`
- P02 subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p02-precision-gpu-subplan-2026-06-20.md`

## Required Checks, Tests, And Reviews

- Syntax check:
  `python -m py_compile docs/benchmarks/check_experimental_batched_ledh_pfpf_ot_streaming_correctness.py`
- Correctness gate:
  `python docs/benchmarks/check_experimental_batched_ledh_pfpf_ot_streaming_correctness.py --cuda-visible-devices -1 --device-scope cpu --device /CPU:0 --expect-device-kind cpu --batch-size 2 --time-steps 2 --num-particles 3 --transport-policy no-resampling --sinkhorn-iterations 2 --row-chunk-size 2 --col-chunk-size 2 --particle-chunk-size 2 --skip-score-fd --output docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p01-correctness-cpu-2026-06-20.json --markdown-output docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p01-correctness-cpu-2026-06-20.md`
- Check JSON reports `overall_passed: true`,
  `cuda_visible_devices: "-1"`, `device: "/CPU:0"`,
  `device_scope: "cpu"`, and `expect_device_kind: "cpu"`.
- Write P01 result.
- Draft P02 subplan and review it locally for consistency, correctness,
  feasibility, artifact coverage, and boundary safety.  Claude review is
  optional for P02 unless P01 output or P02 scope changes materially.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the deterministic streaming LEDH-PFPF-OT correctness gate still pass after default promotion? |
| Baseline/comparator | Existing fixed-branch FP64 baseline inside `check_experimental_batched_ledh_pfpf_ot_streaming_correctness.py`. |
| Primary pass criterion | Script exits 0, writes JSON/MD, and JSON reports `overall_passed: true`, `cuda_visible_devices: "-1"`, `device: "/CPU:0"`, `device_scope: "cpu"`, and `expect_device_kind: "cpu"`. |
| Veto diagnostics | Nonfinite output, failed value parity, failed score FD when not skipped, missing artifact, unexpected visible GPU metadata, CPU/device metadata mismatch, or metadata/nonclaim contradiction. |
| Explanatory diagnostics | Runtime, physical/logical GPU lists after CPU hiding, warning text, exact residual magnitudes. |
| Not concluded | No GPU evidence, no TF32 precision adequacy, no target-shape viability, no speedup, no posterior correctness, no HMC readiness. |
| Artifact | P01 JSON/MD and P01 result note. |

## Forbidden Claims/Actions

- Do not claim GPU success from this CPU/default correctness gate.
- Do not treat this artifact as trusted GPU evidence; GPU devices are
  intentionally hidden with `--cuda-visible-devices -1`.
- Do not treat tiny deterministic correctness as posterior correctness.
- Do not edit algorithm code unless the correctness gate reveals a fixable
  harness defect and a repair subplan is written first.
- Do not touch unrelated low-rank or HMC dirty files.

## Exact Next-Phase Handoff Conditions

Proceed to P02 only if:

- syntax check passes;
- correctness JSON/MD are written;
- `overall_passed` is true;
- CPU-hidden metadata is preserved:
  `cuda_visible_devices == "-1"`, `device == "/CPU:0"`,
  `device_scope == "cpu"`, and `expect_device_kind == "cpu"`;
- P01 result preserves command, artifact paths, interpretation, and nonclaims;
- P02 subplan exists and is reviewed locally or by Claude if material changes
  are made.

## Stop Conditions

- Correctness gate exits nonzero.
- Required artifact is missing or malformed.
- Result requires changing pass/fail criteria after seeing output.
- Fix would require algorithm changes beyond a reviewed repair subplan.
- Any finding invalidates the harness rather than merely failing the candidate.
