#!/usr/bin/env python3
"""P15 fixed-branch squared-TT filtering reference example.

This is a deliberately small reference/prototype artifact.  It is not a
BayesFilter production implementation, not a TensorFlow/TFP backend, and not
evidence of high-dimensional performance.  Its only purpose is to test the
declared P15 value path and same-scalar gradient on a one-step scalar nonlinear
state-space model.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Branch:
    lower: np.ndarray
    upper: np.ndarray
    degree: int
    ranks: tuple[int, int, int]
    n_fit: int
    ridge: float
    sweeps: int
    eps_tau: float
    alpha0: float
    y_obs: tuple[float, float]
    sigma_x0: float
    sigma_eta: float
    sigma_eps: float


def first_primes(n: int) -> list[int]:
    primes: list[int] = []
    candidate = 2
    while len(primes) < n:
        ok = True
        for p in primes:
            if p * p > candidate:
                break
            if candidate % p == 0:
                ok = False
                break
        if ok:
            primes.append(candidate)
        candidate += 1
    return primes


def radical_inverse(j: int, base: int) -> float:
    value = 0.0
    place = 1.0 / base
    while j > 0:
        j, digit = divmod(j, base)
        value += digit * place
        place /= base
    return value


def halton_points(n: int, dim: int) -> np.ndarray:
    primes = first_primes(dim)
    pts = np.empty((n, dim), dtype=float)
    for j in range(1, n + 1):
        for k, p in enumerate(primes):
            pts[j - 1, k] = 2.0 * radical_inverse(j, p) - 1.0
    return pts


def legendre_basis(z: np.ndarray, degree: int) -> np.ndarray:
    z = np.asarray(z, dtype=float)
    out = np.empty((z.size, degree), dtype=float)
    out[:, 0] = math.sqrt(0.5)
    if degree > 1:
        p_prev = np.ones_like(z)
        p_curr = z.copy()
        out[:, 1] = math.sqrt(3.0 / 2.0) * p_curr
        for a in range(1, degree - 1):
            p_next = ((2 * a + 1) * z * p_curr - a * p_prev) / (a + 1)
            out[:, a + 1] = math.sqrt((2 * (a + 1) + 1) / 2.0) * p_next
            p_prev, p_curr = p_curr, p_next
    return out


def normal_logpdf(x: np.ndarray, mean: np.ndarray, sigma: float) -> np.ndarray:
    r = (x - mean) / sigma
    return -0.5 * r * r - math.log(sigma) - 0.5 * math.log(2.0 * math.pi)


@dataclass
class SavedFilter:
    c1: np.ndarray
    c2: np.ndarray
    dc1: np.ndarray
    dc2: np.ndarray
    zhat: float
    dzhat: float
    tau: float


def saved_filter_value_and_dot(x_prev: np.ndarray, saved: SavedFilter, branch: Branch) -> tuple[np.ndarray, np.ndarray]:
    # The kept coordinate after step 1 is x_1, represented on the same
    # one-dimensional affine box [-3, 3].  z = (x-a)/h.
    center = 0.5 * (branch.upper[0] + branch.lower[0])
    half = 0.5 * (branch.upper[0] - branch.lower[0])
    z_keep = (x_prev - center) / half
    b = legendre_basis(z_keep, branch.degree)
    g = b @ saved.c1
    dg = b @ saved.dc1
    norm_c2 = float(saved.c2 @ saved.c2)
    d_norm_c2 = float(2.0 * (saved.c2 @ saved.dc2))
    square = (g * g) * norm_c2
    dsquare = 2.0 * g * dg * norm_c2 + (g * g) * d_norm_c2
    defensive = saved.tau * 0.5
    numerator = square + defensive
    dnumerator = dsquare
    p = numerator / saved.zhat
    dp = dnumerator / saved.zhat - numerator * saved.dzhat / (saved.zhat**2)
    return p, dp


def transformed_logq_and_dot(
    z: np.ndarray,
    branch: Branch,
    alpha: float,
    c_shift: float,
    y_obs: float,
    prev_filter: SavedFilter | None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    center = 0.5 * (branch.upper + branch.lower)
    half = 0.5 * (branch.upper - branch.lower)
    x_t = center[0] + half[0] * z[:, 0]
    x_prev = center[1] + half[1] * z[:, 1]
    log_jac = float(np.sum(np.log(half)))

    if prev_filter is None:
        log_prior = normal_logpdf(x_prev, 0.0, branch.sigma_x0)
        dlog_prior = np.zeros_like(x_prev)
    else:
        p_prev, dp_prev = saved_filter_value_and_dot(x_prev, prev_filter, branch)
        log_prior = np.log(p_prev)
        dlog_prior = dp_prev / p_prev
    log_transition = normal_logpdf(x_t, alpha * x_prev, branch.sigma_eta)
    log_like = normal_logpdf(y_obs, x_t * x_t, branch.sigma_eps)
    logq = log_prior + log_transition + log_like + log_jac
    dlogq = dlog_prior + (x_t - alpha * x_prev) * x_prev / (branch.sigma_eta**2)
    y = np.exp(0.5 * (c_shift + logq))
    dy = 0.5 * y * dlogq
    return logq, y, dy


def compute_shift(branch: Branch, pts: np.ndarray, y_obs: float, prev_filter: SavedFilter | None) -> float:
    logq, _, _ = transformed_logq_and_dot(pts, branch, branch.alpha0, 0.0, y_obs, prev_filter)
    return -float(np.max(logq))


def initialize_cores(y: np.ndarray, degree: int) -> tuple[np.ndarray, np.ndarray]:
    c1 = np.zeros(degree, dtype=float)
    c2 = np.zeros(degree, dtype=float)
    c1[0] = float(np.mean(y))
    c2[0] = 1.0
    return c1, c2


def solve_update(
    basis_self: np.ndarray,
    other_eval: np.ndarray,
    other_dot_eval: np.ndarray,
    y: np.ndarray,
    dy: np.ndarray,
    ridge: float,
) -> tuple[np.ndarray, np.ndarray, float]:
    n = y.size
    weight = 1.0 / n
    a_mat = basis_self * other_eval[:, None]
    da_mat = basis_self * other_dot_eval[:, None]
    gram = weight * (a_mat.T @ a_mat) + ridge * np.eye(a_mat.shape[1])
    rhs = weight * (a_mat.T @ y)
    sol = np.linalg.solve(gram, rhs)

    dgram = weight * (da_mat.T @ a_mat + a_mat.T @ da_mat)
    drhs = weight * (da_mat.T @ y + a_mat.T @ dy)
    dsol = np.linalg.solve(gram, drhs - dgram @ sol)
    cond = float(np.linalg.cond(gram))
    return sol, dsol, cond


def fit_rank1_tt_and_dot(
    y: np.ndarray, dy: np.ndarray, b1: np.ndarray, b2: np.ndarray, branch: Branch
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, list[float], float]:
    c1, c2 = initialize_cores(y, branch.degree)
    dc1 = np.zeros_like(c1)
    dc2 = np.zeros_like(c2)
    conds: list[float] = []

    def update_core1() -> None:
        nonlocal c1, dc1
        other = b2 @ c2
        dother = b2 @ dc2
        c1, dc1, cond = solve_update(b1, other, dother, y, dy, branch.ridge)
        conds.append(cond)

    def update_core2() -> None:
        nonlocal c2, dc2
        other = b1 @ c1
        dother = b1 @ dc1
        c2, dc2, cond = solve_update(b2, other, dother, y, dy, branch.ridge)
        conds.append(cond)

    for _ in range(branch.sweeps):
        update_core1()
        update_core2()
        update_core2()
        update_core1()

    residual = float(np.linalg.norm((b1 @ c1) * (b2 @ c2) - y) / np.linalg.norm(y))
    return c1, c2, dc1, dc2, conds, residual


def step_scalar_and_gradient(
    alpha: float,
    branch: Branch,
    c_shift: float,
    y_obs: float,
    prev_filter: SavedFilter | None,
) -> dict[str, object]:
    pts = halton_points(branch.n_fit, 2)
    b1 = legendre_basis(pts[:, 0], branch.degree)
    b2 = legendre_basis(pts[:, 1], branch.degree)
    _, y, dy = transformed_logq_and_dot(pts, branch, alpha, c_shift, y_obs, prev_filter)
    c1, c2, dc1, dc2, conds, residual = fit_rank1_tt_and_dot(y, dy, b1, b2, branch)
    r0 = float((c1 @ c1) * (c2 @ c2))
    dr0 = float(2.0 * (c1 @ dc1) * (c2 @ c2) + (c1 @ c1) * 2.0 * (c2 @ dc2))
    tau = branch.eps_tau * (2.0**2)
    zhat = r0 + tau
    ell = math.log(zhat) - c_shift
    grad = dr0 / zhat
    return {
        "ell": ell,
        "grad": grad,
        "r0": r0,
        "dr0": dr0,
        "zhat": zhat,
        "tau": tau,
        "fit_residual": residual,
        "max_cond": max(conds),
        "cores": (c1, c2),
        "core_dots": (dc1, dc2),
    }


def make_saved_filter(step: dict[str, object]) -> SavedFilter:
    c1, c2 = step["cores"]  # type: ignore[misc]
    dc1, dc2 = step["core_dots"]  # type: ignore[misc]
    return SavedFilter(
        c1=np.asarray(c1, dtype=float),
        c2=np.asarray(c2, dtype=float),
        dc1=np.asarray(dc1, dtype=float),
        dc2=np.asarray(dc2, dtype=float),
        zhat=float(step["zhat"]),
        dzhat=float(step["dr0"]),
        tau=float(step["tau"]),
    )


def two_step_scalar_and_gradient(alpha: float, branch: Branch, c1_shift: float, c2_shift: float) -> dict[str, object]:
    step1 = step_scalar_and_gradient(alpha, branch, c1_shift, branch.y_obs[0], None)
    saved1 = make_saved_filter(step1)
    step2 = step_scalar_and_gradient(alpha, branch, c2_shift, branch.y_obs[1], saved1)
    return {
        "ell": float(step1["ell"]) + float(step2["ell"]),
        "grad": float(step1["grad"]) + float(step2["grad"]),
        "step1": step1,
        "step2": step2,
    }


def main() -> None:
    branch = Branch(
        lower=np.array([-3.0, -3.0]),
        upper=np.array([3.0, 3.0]),
        degree=5,
        ranks=(1, 1, 1),
        n_fit=96,
        ridge=1.0e-8,
        sweeps=5,
        eps_tau=1.0e-10,
        alpha0=0.72,
        y_obs=(0.35, 0.55),
        sigma_x0=1.0,
        sigma_eta=0.65,
        sigma_eps=0.45,
    )
    pts = halton_points(branch.n_fit, 2)
    c1_shift = compute_shift(branch, pts, branch.y_obs[0], None)
    step1_nominal = step_scalar_and_gradient(branch.alpha0, branch, c1_shift, branch.y_obs[0], None)
    saved1_nominal = make_saved_filter(step1_nominal)
    c2_shift = compute_shift(branch, pts, branch.y_obs[1], saved1_nominal)
    base = two_step_scalar_and_gradient(branch.alpha0, branch, c1_shift, c2_shift)
    print("P15_FIXED_BRANCH_REFERENCE_ONLY")
    print(f"alpha0={branch.alpha0:.12g}")
    print(f"c1_shift={c1_shift:.12g}")
    print(f"c2_shift={c2_shift:.12g}")
    print(f"ell={base['ell']:.12g}")
    print(f"grad={base['grad']:.12g}")
    print(f"step1_fit_residual={base['step1']['fit_residual']:.6e}")
    print(f"step2_fit_residual={base['step2']['fit_residual']:.6e}")
    print(f"step1_max_normal_eq_cond={base['step1']['max_cond']:.6e}")
    print(f"step2_max_normal_eq_cond={base['step2']['max_cond']:.6e}")

    for h_raw in [1.0e-3, 1.0e-4, 1.0e-5, 1.0e-6]:
        h = h_raw * max(1.0, abs(branch.alpha0))
        plus = two_step_scalar_and_gradient(branch.alpha0 + h, branch, c1_shift, c2_shift)
        minus = two_step_scalar_and_gradient(branch.alpha0 - h, branch, c1_shift, c2_shift)
        fd = (float(plus["ell"]) - float(minus["ell"])) / (2.0 * h)
        denom = 1.0 + abs(fd) + abs(float(base["grad"]))
        err = abs(fd - float(base["grad"])) / denom
        print(f"parity h={h:.3e} fd={fd:.12g} relerr={err:.6e}")

    errors = []
    for h_raw in [1.0e-3, 1.0e-4, 1.0e-5, 1.0e-6]:
        h = h_raw * max(1.0, abs(branch.alpha0))
        plus = two_step_scalar_and_gradient(branch.alpha0 + h, branch, c1_shift, c2_shift)
        minus = two_step_scalar_and_gradient(branch.alpha0 - h, branch, c1_shift, c2_shift)
        fd = (float(plus["ell"]) - float(minus["ell"])) / (2.0 * h)
        denom = 1.0 + abs(fd) + abs(float(base["grad"]))
        errors.append(abs(fd - float(base["grad"])) / denom)
    min_err = min(errors)
    print(f"min_parity_relerr={min_err:.6e}")
    if min_err > 1.0e-4:
        raise SystemExit("finite-difference parity failed")
    print("P15_REFERENCE_EXAMPLE_PASS")


if __name__ == "__main__":
    main()
