from __future__ import annotations

import argparse
import os

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

from docs.benchmarks import diagnose_p8p_sir_active_transport_comparator_contract as diagnostic


def _args() -> argparse.Namespace:
    return argparse.Namespace(
        batch_seeds=[81120, 81121, 81122],
        time_steps=3,
        num_particles=3,
        theta_values=[0.02, -0.01, 0.01],
        fd_step=1.0e-5,
        sinkhorn_iterations=5,
        sinkhorn_epsilon=1.0,
        annealed_scaling=0.9,
        annealed_convergence_threshold=1.0e-3,
        manual_tape_atol=diagnostic.DEFAULT_MANUAL_TAPE_ATOL,
        fd_tape_atol=diagnostic.DEFAULT_FD_TAPE_ATOL,
        no_resampling_fd_atol=diagnostic.DEFAULT_NO_RESAMPLING_FD_ATOL,
        active_gap_min=diagnostic.DEFAULT_ACTIVE_GAP_MIN,
    )


def test_active_transport_comparator_contract_passes() -> None:
    payload = diagnostic.run_diagnostic(_args())

    assert payload["passed"] is True
    assert payload["status"] == "PASS"
    assert payload["environment"]["intentional_cpu_only"] is True
    assert payload["environment"]["visible_cuda_devices"] == "-1"
    policies = {item["transport_policy"]: item for item in payload["policies"]}
    assert set(policies) == {"no-resampling", "active-all"}

    no_resampling = policies["no-resampling"]
    assert no_resampling["manual_tape_pass"] is True
    assert no_resampling["raw_full_fd_pass"] is True
    assert no_resampling["policy_pass"] is True
    assert (
        no_resampling["manual_stopped_vs_literal_fd_max_abs"]
        <= diagnostic.DEFAULT_NO_RESAMPLING_FD_ATOL
    )

    active = policies["active-all"]
    assert active["manual_total_tape_pass"] is True
    assert active["manual_total_fd_pass"] is True
    assert active["raw_full_fd_pass"] is True
    assert active["policy_pass"] is True
    assert active["manual_total_vs_literal_fd_max_abs"] <= diagnostic.DEFAULT_FD_TAPE_ATOL


def test_active_transport_manual_total_matches_literal_fd_not_stopped_partial() -> None:
    payload = diagnostic.run_diagnostic(_args())
    active = {
        item["transport_policy"]: item
        for item in payload["policies"]
    }["active-all"]

    assert active["manual_total_tape_vs_literal_fd_max_abs"] <= diagnostic.DEFAULT_FD_TAPE_ATOL
    assert active["manual_total_vs_tape_max_abs"] <= diagnostic.DEFAULT_MANUAL_TAPE_ATOL
    assert active["manual_total_vs_literal_fd_max_abs"] <= diagnostic.DEFAULT_FD_TAPE_ATOL
    assert (
        active["manual_stopped_vs_literal_fd_max_abs"]
        > active["raw_full_tape_vs_literal_fd_max_abs"] * 1000.0
    )
