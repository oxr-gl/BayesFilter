"""Diagnose finite Contract E residual-affine reset moments.

This is a synthetic weighted-cloud diagnostic for the Contract E reset described
in ``docs/chapters/ch32c_entropic_ot_sinkhorn.tex``.  It is a NumPy reference
diagnostic only: it does not implement the production LEDH-PFPF-OT route,
certify gradients, certify filtering correctness, or make GPU/XLA claims.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import math
import platform
from pathlib import Path
from typing import Any

import numpy as np


SCHEMA_VERSION = "filter_bench.ledh_pfpf_ot_contract_e_reset_moments.v1"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--dtype", choices=("float64", "float32"), default="float64")
    parser.add_argument("--seed", type=int, default=20260628)
    parser.add_argument("--rho", type=float, default=1.0)
    parser.add_argument("--tau", type=float, default=1.0e-6)
    parser.add_argument("--spectral-floor", type=float, default=1.0e-10)
    parser.add_argument("--output", required=True)
    parser.add_argument("--markdown-output", default="")
    args = parser.parse_args()
    if args.rho <= 0.0 or args.rho > 1.0:
        raise ValueError("--rho must be in (0, 1]")
    if args.tau < 0.0:
        raise ValueError("--tau must be nonnegative")
    if args.spectral_floor <= 0.0:
        raise ValueError("--spectral-floor must be positive")
    return args


def _sym(matrix: np.ndarray) -> np.ndarray:
    return 0.5 * (matrix + matrix.T)


def _eigh_psd(matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    values, vectors = np.linalg.eigh(_sym(matrix))
    return values, vectors


def _sqrt_psd(matrix: np.ndarray, *, floor: float = 0.0) -> np.ndarray:
    values, vectors = _eigh_psd(matrix)
    clipped = np.maximum(values, floor)
    return (vectors * np.sqrt(clipped)[None, :]) @ vectors.T


def _pinv_sqrt_psd(matrix: np.ndarray, *, spectral_floor: float) -> np.ndarray:
    values, vectors = _eigh_psd(matrix)
    inv_sqrt = np.zeros_like(values)
    mask = values > spectral_floor
    inv_sqrt[mask] = 1.0 / np.sqrt(values[mask])
    return (vectors * inv_sqrt[None, :]) @ vectors.T


def _projector_psd(matrix: np.ndarray, *, spectral_floor: float) -> tuple[np.ndarray, int, np.ndarray]:
    values, vectors = _eigh_psd(matrix)
    mask = values > spectral_floor
    if not np.any(mask):
        return np.zeros_like(matrix), 0, values
    basis = vectors[:, mask]
    return basis @ basis.T, int(np.count_nonzero(mask)), values


def _weighted_moments(x: np.ndarray, w: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    mean = x @ w
    centered = x - mean[:, None]
    cov = centered @ np.diag(w) @ centered.T
    return mean, _sym(cov)


def _uniform_moments(y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    count = y.shape[1]
    mean = np.mean(y, axis=1)
    centered = y - mean[:, None]
    cov = centered @ centered.T / float(count)
    return mean, _sym(cov)


def _contract_e_reset(
    *,
    x: np.ndarray,
    weights: np.ndarray,
    seed: int,
    rho: float,
    tau: float,
    spectral_floor: float,
    dtype: np.dtype[Any],
) -> dict[str, Any]:
    x = np.asarray(x, dtype=dtype)
    weights = np.asarray(weights, dtype=dtype)
    weights = weights / np.sum(weights)
    state_dim, particle_count = x.shape
    if particle_count <= 1:
        raise ValueError("particle_count must exceed one")

    # A deliberately simple nonnegative first-order transform:
    # D_{ij}=w_i.  It satisfies column sums one and row sums N w.
    d_plus = np.tile(weights[:, None], (1, particle_count)).astype(dtype)
    mu_w, sigma_w = _weighted_moments(x, weights)
    y_plus = x @ d_plus
    mu_plus, sigma_plus = _uniform_moments(y_plus)
    g_plus = _sym(sigma_w - sigma_plus)
    projector_w, rank_sigma_w, eig_sigma_w = _projector_psd(
        sigma_w,
        spectral_floor=spectral_floor,
    )
    b_matrix = math.sqrt(float(rho)) * _sqrt_psd(g_plus + tau * projector_w)

    rng = np.random.default_rng(seed)
    z = rng.standard_normal(size=(state_dim, particle_count)).astype(dtype)
    h = np.eye(particle_count, dtype=dtype) - np.ones(
        (particle_count, particle_count),
        dtype=dtype,
    ) / float(particle_count)
    xi = math.sqrt(float(particle_count) / float(particle_count - 1)) * (z @ h)
    y_tilde = y_plus + b_matrix @ xi
    mu_tilde, sigma_tilde = _uniform_moments(y_tilde)

    sigma_w_sqrt = _sqrt_psd(sigma_w)
    sigma_tilde_pinv_sqrt = _pinv_sqrt_psd(sigma_tilde, spectral_floor=spectral_floor)
    affine = sigma_w_sqrt @ sigma_tilde_pinv_sqrt
    y_star = mu_w[:, None] + affine @ (y_tilde - mu_tilde[:, None])
    mu_star, sigma_star = _uniform_moments(y_star)

    eig_g_plus, _ = _eigh_psd(g_plus)
    eig_tilde, _ = _eigh_psd(sigma_tilde)
    support_rank = int(np.count_nonzero(eig_tilde > spectral_floor))
    positive_tilde = eig_tilde[eig_tilde > spectral_floor]
    condition_number = (
        float(np.max(positive_tilde) / np.min(positive_tilde))
        if positive_tilde.size
        else float("inf")
    )
    sigma_norm = float(np.linalg.norm(sigma_w, ord="fro"))
    covariance_residual = float(
        np.linalg.norm(sigma_star - sigma_w, ord="fro") / max(sigma_norm, 1.0e-30)
    )
    mean_residual = float(np.max(np.abs(mu_star - mu_w)))
    row_target = particle_count * weights
    return {
        "particle_count": int(particle_count),
        "state_dim": int(state_dim),
        "rho": float(rho),
        "tau": float(tau),
        "spectral_floor": float(spectral_floor),
        "mean_linf_residual": mean_residual,
        "covariance_relative_frobenius_residual": covariance_residual,
        "min_eig_G_plus": float(np.min(eig_g_plus)),
        "max_eig_Sigma_w": float(np.max(eig_sigma_w)),
        "support_rank": support_rank,
        "rank_Sigma_w": rank_sigma_w,
        "condition_number_tilde_cov": condition_number,
        "lambda_min_tilde_cov": float(np.min(eig_tilde)),
        "lambda_max_tilde_cov": float(np.max(eig_tilde)),
        "d_plus_min": float(np.min(d_plus)),
        "d_plus_row_sum_linf_residual": float(np.max(np.abs(np.sum(d_plus, axis=1) - row_target))),
        "d_plus_column_sum_linf_residual": float(np.max(np.abs(np.sum(d_plus, axis=0) - 1.0))),
        "pre_covariance_trace": float(np.trace(sigma_w)),
        "plus_covariance_trace": float(np.trace(sigma_plus)),
        "tilde_covariance_trace": float(np.trace(sigma_tilde)),
        "star_covariance_trace": float(np.trace(sigma_star)),
    }


def _case_inputs(case_name: str, dtype: np.dtype[Any]) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    if case_name == "1d_strict_gap_pass":
        x = np.asarray([[-2.0, -0.5, 0.25, 1.0, 3.0]], dtype=dtype)
        weights = np.asarray([0.10, 0.20, 0.30, 0.25, 0.15], dtype=dtype)
        return x, weights, {"expected": "pass", "tau_multiplier": 1.0}
    if case_name == "2d_full_rank_strict_gap_pass":
        x = np.asarray(
            [
                [-2.0, -1.0, 0.5, 1.5, 2.2, 0.1],
                [1.0, -0.5, 2.0, -1.0, 0.5, -2.0],
            ],
            dtype=dtype,
        )
        weights = np.asarray([0.12, 0.18, 0.20, 0.15, 0.10, 0.25], dtype=dtype)
        return x, weights, {"expected": "pass", "tau_multiplier": 1.0}
    if case_name == "2d_rank_deficient_support_repair_pass":
        t = np.asarray([-2.0, -1.0, 0.0, 1.0, 2.0], dtype=dtype)
        x = np.vstack([t, 2.0 * t])
        weights = np.asarray([0.05, 0.25, 0.40, 0.20, 0.10], dtype=dtype)
        return x, weights, {"expected": "pass", "tau_multiplier": 1.0}
    if case_name == "2d_conditioning_expected_veto":
        t = np.asarray([-2.0e4, -1.0e4, 0.0, 1.0e4, 2.0e4], dtype=dtype)
        x = np.vstack([t, np.asarray([-1.0e-3, 2.0e-3, -2.0e-3, 1.0e-3, 0.0], dtype=dtype)])
        weights = np.asarray([0.18, 0.22, 0.20, 0.16, 0.24], dtype=dtype)
        return x, weights, {"expected": "veto", "tau_multiplier": 1.0e-12}
    raise ValueError(f"unknown case: {case_name}")


def _gate_case(record: dict[str, Any], *, dtype_name: str, expected: str) -> dict[str, Any]:
    if dtype_name == "float32":
        mean_tol = 1.0e-5
        cov_tol = 5.0e-5
        eig_factor = 1.0e-6
        cond_limit = 1.0e8
    else:
        mean_tol = 1.0e-10
        cov_tol = 1.0e-9
        eig_factor = 1.0e-11
        cond_limit = 1.0e12
    max_eig_sigma = max(1.0, abs(float(record["max_eig_Sigma_w"])))
    checks = {
        "mean_linf_residual": bool(record["mean_linf_residual"] <= mean_tol),
        "covariance_relative_frobenius_residual": bool(
            record["covariance_relative_frobenius_residual"] <= cov_tol
        ),
        "min_eig_G_plus": bool(record["min_eig_G_plus"] >= -eig_factor * max_eig_sigma),
        "support_rank": bool(record["support_rank"] == record["rank_Sigma_w"]),
        "condition_number_tilde_cov": bool(record["condition_number_tilde_cov"] <= cond_limit),
        "d_plus_nonnegative": bool(record["d_plus_min"] >= -eig_factor),
        "d_plus_marginals": bool(
            record["d_plus_row_sum_linf_residual"] <= mean_tol
            and record["d_plus_column_sum_linf_residual"] <= mean_tol
        ),
    }
    pass_checks = bool(all(checks.values()))
    if expected == "pass":
        status = "pass" if pass_checks else "fail"
    else:
        non_condition_checks = [
            passed for name, passed in checks.items() if name != "condition_number_tilde_cov"
        ]
        status = (
            "expected_veto"
            if (not checks["condition_number_tilde_cov"]) and all(non_condition_checks)
            else "fail"
        )
    return {
        "expected": expected,
        "checks": checks,
        "status": status,
        "thresholds": {
            "mean_linf_residual": mean_tol,
            "covariance_relative_frobenius_residual": cov_tol,
            "min_eig_G_plus_factor": eig_factor,
            "condition_number_tilde_cov": cond_limit,
        },
    }


def _write_markdown(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Contract E Moment Diagnostic",
        "",
        f"Status: `{payload['status']}`",
        "",
        "| Case | Expected | Status | Mean residual | Cov residual | Rank | Cond |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for case in payload["cases"]:
        lines.append(
            "| {name} | {expected} | {status} | {mean:.3e} | {cov:.3e} | {rank}/{target} | {cond:.3e} |".format(
                name=case["case"],
                expected=case["gate"]["expected"],
                status=case["gate"]["status"],
                mean=case["metrics"]["mean_linf_residual"],
                cov=case["metrics"]["covariance_relative_frobenius_residual"],
                rank=case["metrics"]["support_rank"],
                target=case["metrics"]["rank_Sigma_w"],
                cond=case["metrics"]["condition_number_tilde_cov"],
            )
        )
    lines.extend(
        [
            "",
            "## Nonclaims",
            "",
            "This diagnostic does not certify LEDH filtering correctness, gradients, "
            "LGSSM Kalman agreement, production readiness, posterior correctness, "
            "or GPU/XLA performance.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = _parse_args()
    dtype = np.dtype(args.dtype)
    case_names = [
        "1d_strict_gap_pass",
        "2d_full_rank_strict_gap_pass",
        "2d_rank_deficient_support_repair_pass",
        "2d_conditioning_expected_veto",
    ]
    cases = []
    for index, name in enumerate(case_names):
        x, weights, config = _case_inputs(name, dtype)
        metrics = _contract_e_reset(
            x=x,
            weights=weights,
            seed=args.seed + index,
            rho=args.rho,
            tau=args.tau * float(config["tau_multiplier"]),
            spectral_floor=args.spectral_floor,
            dtype=dtype,
        )
        gate = _gate_case(metrics, dtype_name=args.dtype, expected=str(config["expected"]))
        cases.append(
            {
                "case": name,
                "metrics": metrics,
                "gate": gate,
            }
        )
    pass_cases_ok = all(
        case["gate"]["status"] == "pass"
        for case in cases
        if case["gate"]["expected"] == "pass"
    )
    expected_veto_ok = all(
        case["gate"]["status"] == "expected_veto"
        for case in cases
        if case["gate"]["expected"] == "veto"
    )
    payload = {
        "schema_version": SCHEMA_VERSION,
        "created_at": _dt.datetime.now(tz=_dt.timezone.utc).isoformat(),
        "status": "passed" if pass_cases_ok and expected_veto_ok else "failed",
        "environment": {
            "implementation": "numpy_reference_diagnostic",
            "cpu_gpu_status": "cpu_only_no_gpu_framework_imported",
            "python": platform.python_version(),
            "platform": platform.platform(),
            "numpy": np.__version__,
            "dtype": args.dtype,
        },
        "parameters": {
            "seed": args.seed,
            "rho": args.rho,
            "tau": args.tau,
            "spectral_floor": args.spectral_floor,
        },
        "cases": cases,
        "nonclaims": [
            "not LEDH filtering correctness",
            "not LGSSM Kalman agreement",
            "not gradient correctness",
            "not production readiness",
            "not GPU/XLA evidence",
        ],
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    if args.markdown_output:
        markdown_output = Path(args.markdown_output)
        markdown_output.parent.mkdir(parents=True, exist_ok=True)
        _write_markdown(markdown_output, payload)
    if payload["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
