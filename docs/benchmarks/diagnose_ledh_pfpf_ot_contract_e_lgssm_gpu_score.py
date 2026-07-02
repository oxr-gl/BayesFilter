"""Focused GPU/XLA/TF32 LGSSM score diagnostic for Contract E.

This runner answers the narrow R12 question: after the Contract E
Cholesky-ridge repair and manual reverse-scan score wiring, does the batched GPU
XLA TF32 route at ``N=1000`` put the seed-mean LGSSM value and score within two
MCSE of the exact Kalman reference?

It intentionally does not run the expensive 13-point finite-difference ladder.
It is a finite-particle bias diagnostic for the production-default GPU branch,
not a CPU material-route replay and not a same-scalar FD certificate.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import importlib.util
import json
import math
import platform
import sys
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
GRADIENT_SCRIPT_PATH = (
    ROOT / "docs" / "benchmarks" / "diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py"
)
SCHEMA_VERSION = "filter_bench.ledh_pfpf_ot_contract_e_lgssm_gpu_score.v2"
PLAN_PATH = (
    "docs/plans/"
    "bayesfilter-ledh-pfpf-ot-contract-e-phase3-r12-gpu-xla-manual-score-route-"
    "plan-2026-06-30.md"
)
PARAMETER_NAMES = ("ar_coefficient", "log_transition_variance", "log_observation_variance")
RELATIVE_ERROR_LIMIT = 0.01
RELATIVE_ERROR_DENOMINATOR_FLOOR = 1.0e-12


def _load_gradient_module() -> Any:
    spec = importlib.util.spec_from_file_location("contract_e_gradient_r11", GRADIENT_SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load Contract E gradient helper from {GRADIENT_SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


gradient_script = _load_gradient_module()


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--device-scope", choices=("visible",), default="visible")
    parser.add_argument("--cuda-visible-devices", default="0")
    parser.add_argument("--num-particles", type=int, default=1000)
    parser.add_argument("--seed-count", type=int, default=10)
    parser.add_argument("--time-steps", type=int, default=10)
    parser.add_argument("--state-dims", type=int, nargs="+", default=[2])
    parser.add_argument(
        "--settings",
        type=gradient_script.phase2._parse_setting,
        nargs="+",
        default=[gradient_script.phase2._parse_setting("0.55:2")],
    )
    parser.add_argument("--rho", type=float, default=1.0)
    parser.add_argument("--tau", type=float, default=1.0e-6)
    parser.add_argument("--spectral-floor", type=float, default=1.0e-6)
    parser.add_argument(
        "--contract-e-reset-factorization",
        choices=("cholesky-ridge",),
        default="cholesky-ridge",
    )
    parser.add_argument("--chol-ridge-rel", type=float, default=1.0e-8)
    parser.add_argument("--chol-ridge-abs", type=float, default=1.0e-10)
    parser.add_argument("--chol-ridge-escalation", type=float, default=10.0)
    parser.add_argument("--chol-ridge-max-attempts", type=int, default=12)
    parser.add_argument("--covariance-residual-limit", type=float, default=5.0e-4)
    parser.add_argument("--condition-limit", type=float, default=1.0e8)
    parser.add_argument("--tf32-mode", choices=("enabled",), default="enabled")
    parser.add_argument("--xla", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument(
        "--score-route",
        choices=("manual-reverse-scan", "outer-tape-legacy"),
        default="manual-reverse-scan",
        help="R12 evidence requires manual-reverse-scan; outer-tape-legacy is a non-evidence replay.",
    )
    parser.add_argument(
        "--reverse-contract-e-gradient-probe",
        choices=("full", "skip-reset-computation"),
        default="full",
        help="GPU/XLA localization probe; skip-reset-computation is not promotion evidence",
    )
    parser.add_argument("--output", required=True)
    parser.add_argument("--markdown-output", default="")
    args = parser.parse_args()
    if not args.xla:
        raise ValueError("R12 GPU diagnostic requires XLA; --no-xla is forbidden")
    if args.score_route != "manual-reverse-scan":
        raise ValueError("R12 GPU diagnostic requires --score-route manual-reverse-scan")
    if args.num_particles <= 2:
        raise ValueError("--num-particles must exceed 2")
    if args.seed_count != 10:
        raise ValueError("R12 freezes seed_count=10 for the batched route")
    if args.time_steps != 10:
        raise ValueError("R12 freezes T=10")
    if any(dim not in (1, 2) for dim in args.state_dims):
        raise ValueError("--state-dims supports only 1 and 2")
    if args.rho <= 0.0 or args.rho > 1.0:
        raise ValueError("--rho must be in (0, 1]")
    if args.tau < 0.0:
        raise ValueError("--tau must be nonnegative")
    if args.spectral_floor <= 0.0:
        raise ValueError("--spectral-floor must be positive")
    if args.chol_ridge_rel < 0.0:
        raise ValueError("--chol-ridge-rel must be nonnegative")
    if args.chol_ridge_abs <= 0.0:
        raise ValueError("--chol-ridge-abs must be strictly positive")
    if args.chol_ridge_escalation <= 1.0:
        raise ValueError("--chol-ridge-escalation must exceed one")
    if args.chol_ridge_max_attempts <= 1:
        raise ValueError("--chol-ridge-max-attempts must exceed one for minimal-ridge selection")
    if args.covariance_residual_limit <= 0.0:
        raise ValueError("--covariance-residual-limit must be positive")
    if args.condition_limit <= 1.0:
        raise ValueError("--condition-limit must exceed one")
    args.gate_mode = "smoke"
    args.reverse_transport_gradient_route = "manual-transport-vjp-only"
    args.material_scope = "nonmaterial"
    args.material_ridge_policy = "nonmaterial"
    return args


def _finite_list(values: list[float]) -> bool:
    return all(math.isfinite(float(value)) for value in values)


def _relative_error(delta: float, reference: float) -> float | None:
    if not math.isfinite(delta) or not math.isfinite(reference):
        return None
    denominator = max(abs(reference), RELATIVE_ERROR_DENOMINATOR_FLOOR)
    return abs(delta) / denominator


def _component_hmc_direction_gate(
    *,
    delta: float,
    reference: float,
    mcse: float,
    mcse_decreases_with_n_certificate: bool = False,
) -> dict[str, Any]:
    z = None if mcse <= 0.0 else delta / mcse
    relative_error = _relative_error(delta, reference)
    within_2_mcse = False if z is None else abs(z) <= 2.0
    within_4_mcse = False if z is None else abs(z) <= 4.0
    within_1pct_relative_error = (
        False if relative_error is None else relative_error <= RELATIVE_ERROR_LIMIT
    )
    four_mcse_with_certificate = bool(
        within_4_mcse and mcse_decreases_with_n_certificate
    )
    hmc_direction_gate = bool(
        within_2_mcse or four_mcse_with_certificate or within_1pct_relative_error
    )
    if within_2_mcse:
        reason = "within_2_mcse"
    elif four_mcse_with_certificate:
        reason = "within_4_mcse_with_n_ladder_mcse_decrease"
    elif within_1pct_relative_error:
        reason = "within_1pct_relative_error"
    else:
        reason = "failed_hmc_direction_gate"
    return {
        "z_over_mcse": z,
        "relative_error_to_kalman": relative_error,
        "relative_error_limit": RELATIVE_ERROR_LIMIT,
        "within_2_mcse_of_kalman": within_2_mcse,
        "within_4_mcse_of_kalman": within_4_mcse,
        "mcse_decreases_with_n_certificate": bool(mcse_decreases_with_n_certificate),
        "within_4_mcse_with_n_ladder_mcse_decrease": four_mcse_with_certificate,
        "within_1pct_relative_error_to_kalman": within_1pct_relative_error,
        "hmc_direction_gate": hmc_direction_gate,
        "hmc_direction_gate_reason": reason,
    }


def _gate_record(record: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    value = record["base"]["value"]
    gradient = record["base"]["gradient"]
    diagnostics = record["base"]["diagnostics"]
    value_mcse = float(value["mcse"])
    value_delta = float(value["delta_to_kalman"])
    value_component_gate = _component_hmc_direction_gate(
        delta=value_delta,
        reference=float(value["kalman"]),
        mcse=value_mcse,
    )
    value_z = value_component_gate["z_over_mcse"]
    parameter_gates = []
    for index, parameter in enumerate(PARAMETER_NAMES):
        grad_mean = float(gradient["mean"][index])
        grad_mcse = float(gradient["mcse"][index])
        kalman = float(gradient["kalman"][index])
        delta = grad_mean - kalman
        component_gate = _component_hmc_direction_gate(
            delta=delta,
            reference=kalman,
            mcse=grad_mcse,
        )
        z = component_gate["z_over_mcse"]
        parameter_gates.append(
            {
                "parameter": parameter,
                "gradient_mean": grad_mean,
                "kalman_gradient": kalman,
                "delta_to_kalman": delta,
                "gradient_sd": float(gradient["sd"][index]),
                "gradient_mcse": grad_mcse,
                "z_over_gradient_mcse": z,
                "within_2_gradient_mcse_of_kalman": component_gate[
                    "within_2_mcse_of_kalman"
                ],
                "within_4_gradient_mcse_of_kalman": component_gate[
                    "within_4_mcse_of_kalman"
                ],
                "mcse_decreases_with_n_certificate": component_gate[
                    "mcse_decreases_with_n_certificate"
                ],
                "within_4_gradient_mcse_with_n_ladder_mcse_decrease": component_gate[
                    "within_4_mcse_with_n_ladder_mcse_decrease"
                ],
                "relative_error_to_kalman": component_gate["relative_error_to_kalman"],
                "relative_error_limit": component_gate["relative_error_limit"],
                "within_1pct_relative_error_to_kalman": component_gate[
                    "within_1pct_relative_error_to_kalman"
                ],
                "hmc_direction_gate": component_gate["hmc_direction_gate"],
                "hmc_direction_gate_reason": component_gate["hmc_direction_gate_reason"],
            }
        )
    cov_residual = diagnostics["max_covariance_relative_residual"]
    condition = diagnostics["max_tilde_condition"]
    finite_base = (
        math.isfinite(float(value["mean"]))
        and math.isfinite(float(value["mcse"]))
        and _finite_list(gradient["mean"])
        and _finite_list(gradient["mcse"])
        and _finite_list(gradient["kalman"])
    )
    covariance_ok = cov_residual is not None and cov_residual <= args.covariance_residual_limit
    condition_ok = condition is not None and condition <= args.condition_limit
    ridge_ok = not bool(diagnostics["any_ridge_failure"])
    value_ok = value_component_gate["hmc_direction_gate"]
    gradients_ok = all(item["hmc_direction_gate"] for item in parameter_gates)
    return {
        "status": "pass"
        if finite_base and covariance_ok and condition_ok and ridge_ok and value_ok and gradients_ok
        else "fail",
        "value_mean": float(value["mean"]),
        "kalman_value": float(value["kalman"]),
        "value_delta_to_kalman": value_delta,
        "value_sd": float(value["sd"]),
        "value_mcse": value_mcse,
        "value_z_over_mcse": value_z,
        "value_relative_error_to_kalman": value_component_gate["relative_error_to_kalman"],
        "value_relative_error_limit": value_component_gate["relative_error_limit"],
        "value_within_2_mcse_of_kalman": value_component_gate[
            "within_2_mcse_of_kalman"
        ],
        "value_within_4_mcse_of_kalman": value_component_gate[
            "within_4_mcse_of_kalman"
        ],
        "value_mcse_decreases_with_n_certificate": value_component_gate[
            "mcse_decreases_with_n_certificate"
        ],
        "value_within_4_mcse_with_n_ladder_mcse_decrease": value_component_gate[
            "within_4_mcse_with_n_ladder_mcse_decrease"
        ],
        "value_within_1pct_relative_error_to_kalman": value_component_gate[
            "within_1pct_relative_error_to_kalman"
        ],
        "value_hmc_direction_gate": value_ok,
        "value_hmc_direction_gate_reason": value_component_gate["hmc_direction_gate_reason"],
        "finite_base": finite_base,
        "covariance_restoration_ok": covariance_ok,
        "conditioning_ok": condition_ok,
        "ridge_ok": ridge_ok,
        "parameter_gates": parameter_gates,
    }


def _overall_gate(records: list[dict[str, Any]], device: dict[str, Any]) -> dict[str, Any]:
    gpu_ok = bool(device["logical_gpus"])
    full_probe = all(item["manifest_probe"] == "full" for item in records)
    manual_score_route = all(item["score_route"] == "manual-reverse-scan" for item in records)
    route_ok = (
        bool(device["xla"])
        and bool(device["tf32_execution_enabled"])
        and gpu_ok
        and full_probe
        and manual_score_route
    )
    status = "passed" if route_ok and records and all(item["gate"]["status"] == "pass" for item in records) else "failed"
    return {
        "status": status,
        "route_ok": route_ok,
        "gpu_visible": gpu_ok,
        "xla_enabled": bool(device["xla"]),
        "tf32_execution_enabled": bool(device["tf32_execution_enabled"]),
        "manual_score_route": manual_score_route,
        "fixture_gates": [
            {
                "state_dim": item["state_dim"],
                "setting": item["setting"]["label"],
                **item["gate"],
            }
            for item in records
        ],
        "primary_criterion": (
            "GPU/XLA/TF32 batched Contract E seed-mean value and score satisfy "
            "the HMC-direction gate against exact FP64 Kalman: within 2 MCSE, "
            "or within 4 MCSE with an explicit N-ladder MCSE-decrease certificate, "
            "or within 1% relative error."
        ),
    }


def _render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Contract E LGSSM GPU XLA TF32 Score Diagnostic",
        "",
        f"Date: {payload['timestamp_utc']}",
        "",
        f"Status: `{payload['gate']['status']}`",
        "",
        "## Manifest",
        "",
        f"- num_particles: `{payload['manifest']['num_particles']}`",
        f"- seed_count: `{payload['manifest']['seed_count']}`",
        f"- time_steps: `{payload['manifest']['time_steps']}`",
        f"- state_dims: `{payload['manifest']['state_dims']}`",
        f"- settings: `{payload['manifest']['settings']}`",
        f"- device_scope: `{payload['device']['device_scope']}`",
        f"- logical_gpus: `{payload['device']['logical_gpus']}`",
        f"- xla: `{payload['device']['xla']}`",
        f"- tf32_execution_enabled: `{payload['device']['tf32_execution_enabled']}`",
        f"- reset_factorization: `{payload['manifest']['contract_e_reset_factorization']}`",
        f"- score_route: `{payload['manifest']['score_route']}`",
        f"- chol_ridge_abs: `{payload['manifest']['chol_ridge_abs']}`",
        f"- chol_ridge_rel: `{payload['manifest']['chol_ridge_rel']}`",
        "",
        "## Value Gate",
        "",
        "| dim | value mean | Kalman | delta | sd | MCSE | z | rel err | HMC gate | reason |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for record in payload["records"]:
        gate = record["gate"]
        z = gate["value_z_over_mcse"]
        rel = gate["value_relative_error_to_kalman"]
        lines.append(
            "| "
            f"{record['state_dim']} | "
            f"{gate['value_mean']:.6f} | "
            f"{gate['kalman_value']:.6f} | "
            f"{gate['value_delta_to_kalman']:.6f} | "
            f"{gate['value_sd']:.6f} | "
            f"{gate['value_mcse']:.6f} | "
            f"{'NA' if z is None else f'{z:.3f}'} | "
            f"{'NA' if rel is None else f'{100.0 * rel:.3f}%'} | "
            f"`{gate['value_hmc_direction_gate']}` | "
            f"`{gate['value_hmc_direction_gate_reason']}` |"
        )
    lines.extend(
        [
            "",
            "## Score Gate",
            "",
            "| dim | parameter | score mean | Kalman | delta | sd | MCSE | z | rel err | HMC gate | reason |",
            "| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |",
        ]
    )
    for record in payload["records"]:
        for gate in record["gate"]["parameter_gates"]:
            z = gate["z_over_gradient_mcse"]
            rel = gate["relative_error_to_kalman"]
            lines.append(
                "| "
                f"{record['state_dim']} | "
                f"`{gate['parameter']}` | "
                f"{gate['gradient_mean']:.6f} | "
                f"{gate['kalman_gradient']:.6f} | "
                f"{gate['delta_to_kalman']:.6f} | "
                f"{gate['gradient_sd']:.6f} | "
                f"{gate['gradient_mcse']:.6f} | "
                f"{'NA' if z is None else f'{z:.3f}'} | "
                f"{'NA' if rel is None else f'{100.0 * rel:.3f}%'} | "
                f"`{gate['hmc_direction_gate']}` | "
                f"`{gate['hmc_direction_gate_reason']}` |"
            )
    lines.extend(
        [
            "",
            "## Gate",
            "",
            "```json",
            json.dumps(payload["gate"], indent=2, sort_keys=True),
            "```",
            "",
            "## Nonclaims",
            "",
            "- This is not a CPU LEDH result.",
            "- This diagnostic does not run the 13-point finite-difference ladder.",
            "- This diagnostic does not certify SIR/SV/nonlinear correctness, HMC readiness, or production readiness.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    args = _parse_args()
    gradient_script._configure_import_environment(args)
    start = time.perf_counter()
    harness = gradient_script.phase2._load_harness(args)
    device = gradient_script.phase2._device_manifest(harness, args)
    records = []
    for state_dim in args.state_dims:
        for setting in args.settings:
            base = gradient_script._run_base_gradient(harness, int(state_dim), setting, args)
            record = {
                "state_dim": int(state_dim),
                "setting": dict(setting),
                "base": base,
                "manifest_probe": args.reverse_contract_e_gradient_probe,
                "score_route": args.score_route,
            }
            record["gate"] = _gate_record(record, args)
            records.append(record)
    payload = {
        "schema_version": SCHEMA_VERSION,
        "timestamp_utc": _dt.datetime.now(tz=_dt.timezone.utc).isoformat(),
        "host": platform.node(),
        "python_version": platform.python_version(),
        "tensorflow_version": harness.tf.__version__,
        "plan": PLAN_PATH,
        "manifest": {
            "route": "gpu_xla_tf32_batched_contract_e_manual_reverse_scan_score_diagnostic",
            "score_route": args.score_route,
            "num_particles": int(args.num_particles),
            "seed_count": int(args.seed_count),
            "time_steps": int(args.time_steps),
            "state_dims": [int(item) for item in args.state_dims],
            "settings": args.settings,
            "theta": [float(item) for item in harness.THETA.numpy().tolist()],
            "initial_transition_seed_schedule": (
                "seed indices 9100..9109; initial seeds [seed,17]; transition seeds [seed,29]"
            ),
            "contract_e_residual_seed_schedule": (
                "seed indices 9100..9109; residual seeds [seed,43+t] for t=0..9"
            ),
            "reverse_gradient_route": (
                "manual reverse scan of per-seed Contract E scalars with explicit "
                "transport/reset/normalization/log-density/LEDH-flow VJPs; no outer "
                "GradientTape score wrapper and no FD ladder in this runner"
            ),
            "reverse_contract_e_gradient_probe": args.reverse_contract_e_gradient_probe,
            "contract_e_reset_factorization": args.contract_e_reset_factorization,
            "rho": float(args.rho),
            "tau": float(args.tau),
            "spectral_floor": float(args.spectral_floor),
            "chol_ridge_rel": float(args.chol_ridge_rel),
            "chol_ridge_abs": float(args.chol_ridge_abs),
            "chol_ridge_escalation": float(args.chol_ridge_escalation),
            "chol_ridge_max_attempts": int(args.chol_ridge_max_attempts),
            "covariance_residual_limit": float(args.covariance_residual_limit),
            "condition_limit": float(args.condition_limit),
        },
        "device": device,
        "records": records,
        "gate": _overall_gate(records, device),
        "elapsed_seconds": time.perf_counter() - start,
        "nonclaims": [
            "not CPU LEDH evidence",
            "not same-scalar FD evidence",
            "not SIR/SV/nonlinear correctness",
            "not HMC readiness",
            "not production readiness",
        ],
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.markdown_output:
        markdown_output = Path(args.markdown_output)
        markdown_output.parent.mkdir(parents=True, exist_ok=True)
        markdown_output.write_text(_render_markdown(payload), encoding="utf-8")
    print(json.dumps({"status": payload["gate"]["status"], "elapsed_seconds": payload["elapsed_seconds"]}, sort_keys=True))
    if payload["gate"]["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
