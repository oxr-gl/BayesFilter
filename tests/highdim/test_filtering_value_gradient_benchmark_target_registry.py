from __future__ import annotations

import json
from pathlib import Path


REGISTRY_PATH = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-target-registry-2026-06-10.json"
)

REQUIRED_ROW_IDS = {
    "lgssm_exact_kalman_dim_1_2_3",
    "p44_cubic_additive_gaussian_dim_1_2_3",
    "p44_quadratic_observation_dim_1_2_3",
    "p44_nonlinear_transition_h2_dim_1_2_3",
    "p44_nonlinear_transition_h4_cut4_extension_dim_1_2_3",
    "sv_exact_transformed_actual_nongaussian_dim_1_2_3",
    "sv_ksc_gaussian_mixture_surrogate_dim_1_2_3",
    "native_generalized_sv_dense_lower_rung_dim_2",
    "spatial_sir_lower_rung_j1_dim_2",
    "spatial_sir_scaling_route_admitted_rank_selection_blocked_d18",
    "predator_prey_lower_rung_dim_2",
    "predator_prey_production_tuned_h25_dim_2",
}

REQUIRED_ROW_FIELDS = {
    "row_id",
    "model_family",
    "row_class",
    "reference_type",
    "target_identity",
    "state_dim",
    "observation_dim",
    "horizon",
    "dtype",
    "observations",
    "theta",
    "value_scalar",
    "gradient_parameterization",
    "gradient_metadata",
    "reference_route",
    "current_admission",
    "nonclaims",
}


def _registry() -> dict[str, object]:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def test_filter_bench_target_registry_has_required_rows_and_schema() -> None:
    registry = _registry()

    assert registry["schema_version"] == "filter_bench.target_registry.v1"
    assert registry["phase"] == "FILTER_BENCH_P1"
    assert registry["status"] in {
        "PENDING_CLAUDE_REVIEW",
        "PASS_FILTER_BENCH_P1_TARGET_REGISTRY",
    }
    assert set(registry["reference_type_vocabulary"]) == {
        "exact",
        "dense_numerical",
        "transformed_actual_nongaussian",
        "gaussian_mixture_surrogate",
        "diagnostic",
        "blocked_only",
    }

    rows = {row["row_id"]: row for row in registry["rows"]}
    assert set(registry["required_row_ids"]) == REQUIRED_ROW_IDS
    assert REQUIRED_ROW_IDS.issubset(rows)
    assert len(rows) == len(registry["rows"])

    for row_id, row in rows.items():
        assert REQUIRED_ROW_FIELDS.issubset(row), row_id
        assert row["reference_type"] in registry["reference_type_vocabulary"], row_id
        assert row["row_class"] in registry["row_class_vocabulary"], row_id
        assert row["target_identity"], row_id
        assert row["value_scalar"], row_id
        assert row["gradient_parameterization"], row_id
        gradient_metadata = row["gradient_metadata"]
        assert gradient_metadata["status"], row_id
        assert "theta_dimension" in gradient_metadata, row_id
        assert "theta_coordinates" in gradient_metadata or "theta_coordinates_by_dimension" in gradient_metadata, row_id
        assert gradient_metadata["coordinate_type"], row_id
        assert gradient_metadata["backend"], row_id
        assert row["reference_route"]["label"], row_id
        assert row["reference_route"]["implementation_hint"], row_id
        assert row["theta"]["parameterization"], row_id
        assert row["observations"]["kind"], row_id
        assert row["nonclaims"], row_id


def test_filter_bench_target_registry_freezes_admitted_observations_and_theta() -> None:
    rows = {row["row_id"]: row for row in _registry()["rows"]}

    for row_id, row in rows.items():
        admission = row["current_admission"]
        observations = row["observations"]
        theta = row["theta"]
        if admission == "blocked_current_scope_not_performance_cell":
            assert observations["kind"] == "deterministic_nominal_path_blocked_before_filtering"
            assert theta["value"] == []
            continue

        assert observations["kind"] != "generated_by_fixture", row_id
        assert "values" in observations or "values_full_dim3" in observations, row_id
        assert theta.get("value") != "fixture_locked", row_id
        assert theta.get("dimension") != "fixture_locked", row_id

    assert rows["spatial_sir_lower_rung_j1_dim_2"]["observations"]["values"] == [
        [14.10],
        [11.85],
    ]
    assert rows["spatial_sir_lower_rung_j1_dim_2"]["theta"]["value"] == []
    assert rows["predator_prey_lower_rung_dim_2"]["theta"]["value"] == [
        0.6,
        114.0,
        25.0,
        0.3,
        0.5,
        0.5,
    ]
    assert len(rows["predator_prey_production_tuned_h25_dim_2"]["observations"]["values"]) == 25
    assert len(rows["spatial_sir_scaling_route_admitted_rank_selection_blocked_d18"]["observations"]["values"]) == 25


def test_filter_bench_target_registry_keeps_sv_actual_and_surrogate_distinct() -> None:
    rows = {row["row_id"]: row for row in _registry()["rows"]}

    actual = rows["sv_exact_transformed_actual_nongaussian_dim_1_2_3"]
    surrogate = rows["sv_ksc_gaussian_mixture_surrogate_dim_1_2_3"]

    assert actual["reference_type"] == "transformed_actual_nongaussian"
    assert surrogate["reference_type"] == "gaussian_mixture_surrogate"
    assert actual["reference_route"]["label"] == "dense_exact_transformed_sv_reference"
    assert surrogate["reference_route"]["label"] == "kalman_mixture_enumeration"
    assert "not KSC Gaussian mixture surrogate" in actual["nonclaims"]
    assert "not exact transformed actual non-Gaussian target" in surrogate["nonclaims"]


def test_filter_bench_target_registry_supersedes_stale_blockers_without_erasing_history() -> None:
    registry = _registry()
    rows = {row["row_id"]: row for row in registry["rows"]}

    supersession_text = json.dumps(registry["historical_supersession"])
    assert "blocked_current_scalar_nonlinear_route_requires_state_dim_1" in supersession_text
    assert "LEDH-PFPF-OT" in supersession_text
    assert "historical_or_superseded_not_current_admission_logic" in supersession_text
    assert "historical_only_not_algorithm1_evidence" in supersession_text

    row_text = json.dumps(registry["rows"])
    assert "blocked_current_scalar_nonlinear_route_requires_state_dim_1" not in row_text
    assert "LEDH-PFPF-OT" not in row_text
    assert rows["native_generalized_sv_dense_lower_rung_dim_2"]["current_admission"] == (
        "lower_rung_benchmark_admitted"
    )
    assert rows["predator_prey_production_tuned_h25_dim_2"]["current_admission"] == (
        "benchmark_admitted"
    )
    assert rows["spatial_sir_scaling_route_admitted_rank_selection_blocked_d18"]["reference_type"] == (
        "blocked_only"
    )


def test_filter_bench_target_registry_has_machine_checkable_gradient_metadata() -> None:
    rows = {row["row_id"]: row for row in _registry()["rows"]}

    sir_lower = rows["spatial_sir_lower_rung_j1_dim_2"]["gradient_metadata"]
    sir_blocked = rows["spatial_sir_scaling_route_admitted_rank_selection_blocked_d18"][
        "gradient_metadata"
    ]
    predator_lower = rows["predator_prey_lower_rung_dim_2"]["gradient_metadata"]
    predator_prod = rows["predator_prey_production_tuned_h25_dim_2"]["gradient_metadata"]

    assert sir_lower["theta_dimension"] == 0
    assert sir_lower["theta_coordinates"] == []
    assert sir_lower["cell_status_required"] == "NO_THETA_GRADIENT_DIM0"
    assert sir_blocked["status"] == "blocked_value_route_no_theta_gradient_dim0"
    assert sir_blocked["cell_status_required"] == "BLOCKED_VALUE_ROUTE"
    assert predator_lower["theta_coordinates"] == ["r", "K", "a", "s", "u", "v"]
    assert predator_lower["cell_status_required_if_missing"] == "GRADIENT_NOT_EXPOSED"
    assert predator_prod["theta_coordinates"] == ["r", "K", "a", "s", "u", "v"]
    assert predator_prod["cell_status_required_if_missing"] == "GRADIENT_NOT_EXPOSED"


def test_filter_bench_target_registry_policy_allows_approximate_filters_on_non_gaussian_rows() -> None:
    registry = _registry()
    policy = registry["cell_applicability_policy"]
    algorithms = set(registry["algorithm_roster_for_later_phases"])

    assert "Exactness is required only for LGSSM exact rows" in policy["exactness_scope"]
    assert "benchmarkable on non-Gaussian rows" in policy["approximate_filters"]
    assert "invalid gradients are findings" in policy["dpf_policy"]
    assert "ledh_pfpf_alg1_ukf_current" in algorithms
    assert "bootstrap_dpf_current" in algorithms
    assert "zhao_cui_scalar_or_multistate" in algorithms
    assert "ledh_pfpf_ot" not in algorithms
