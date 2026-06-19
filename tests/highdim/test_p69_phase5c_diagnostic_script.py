from __future__ import annotations

import importlib.util
import math
from pathlib import Path

import pytest


def _load_phase5c_script():
    script_path = (
        Path(__file__).resolve().parents[2]
        / "scripts"
        / "p69_phase5c_rank_activity_degree_normalizer_diagnostic.py"
    )
    spec = importlib.util.spec_from_file_location("p69_phase5c_diagnostic", script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_p69_phase5c_pair_summary_uses_mixture_normalizer_field() -> None:
    module = _load_phase5c_script()

    rows = {
        "rank_candidate_1_2_fit36": {"fit_branch_hashes": ("rank2",)},
        "rank_stronger_1_3_fit36": {
            "fit_branch_hashes": ("rank3",),
            "step_diagnostics": [
                {
                    "rank_channel_summary": {
                        "active_channel_count": 1,
                        "extra_channel_norms_all_zero": True,
                    }
                },
                {
                    "rank_channel_summary": {
                        "active_channel_count": 1,
                        "extra_channel_norms_all_zero": True,
                    }
                },
            ],
        },
        "degree_candidate_1_2_fit24": {
            "fit_branch_hashes": ("degree1",),
            "normalizer_terms_by_step": [
                {"log_transport_normalizer": 2.0, "mixture_normalizer": 2.0},
                {"log_transport_normalizer": 4.0, "mixture_normalizer": 10.0},
            ],
            "step_diagnostics": [
                {
                    "fit_quality": {"fit_residual": 0.5},
                    "condition_summary": {"condition_number_max": 3.0},
                },
                {
                    "fit_quality": {"fit_residual": 0.7},
                    "condition_summary": {"condition_number_max": 4.0},
                },
            ],
        },
        "degree_stronger_2_2_fit24": {
            "fit_branch_hashes": ("degree2",),
            "fit_sample_count": 24,
            "sample_adequacy": {
                "preferred_fit_samples": 48,
                "status": "PASS_SAMPLE_ADEQUATE_FOR_DIAGNOSTIC",
            },
            "normalizer_terms_by_step": [
                {"log_transport_normalizer": 5.0, "mixture_normalizer": 20.0},
                {"log_transport_normalizer": 1.0, "mixture_normalizer": 5.0},
            ],
            "step_diagnostics": [
                {
                    "fit_quality": {"fit_residual": 0.25},
                    "condition_summary": {"condition_number_max": 8.0},
                },
                {
                    "fit_quality": {"fit_residual": 0.2},
                    "condition_summary": {"condition_number_max": 9.0},
                },
            ],
        },
    }

    summary = module._pair_summary(rows)

    assert summary["rank_pair"]["rank_high_classification"] == (
        "extra_channel_inactive_in_realized_fit"
    )
    degree = summary["degree_pair"]
    assert degree["mixture_normalizer_ratio_high_over_low"] == (10.0, 0.5)
    assert degree["log_mixture_normalizer_delta_high_minus_low"] == pytest.approx(
        (math.log(10.0), math.log(0.5))
    )
    assert degree["log_transport_normalizer_delta_high_minus_low"] == (3.0, -3.0)
