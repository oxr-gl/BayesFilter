#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

PLAN_PATH = ROOT / (
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-source-paper-blocker-closure-plan-2026-06-11.md"
)
P10_RESULT_PATH = ROOT / "docs/plans/bayesfilter-p10-truth-prior-literature-audit-result-2026-06-11.md"
P8_CONTRACT_PATH = ROOT / (
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-truth-contract-2026-06-11.json"
)
RUNBOOK_PATH = ROOT / (
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-gap-visible-gated-execution-runbook-2026-06-10.md"
)
MASTER_PATH = ROOT / (
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-gap-closure-master-program-2026-06-10.md"
)

DEFAULT_JSON = ROOT / (
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-contract-2026-06-11.json"
)
DEFAULT_CSV = ROOT / (
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-summary-2026-06-11.csv"
)
DEFAULT_MD = ROOT / (
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-summary-2026-06-11.md"
)
GENERALIZED_SV_SPEC_JSON = ROOT / (
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-generalized-sv-testing-spec-2026-06-11.json"
)
GENERALIZED_SV_SPEC_MD = ROOT / (
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-generalized-sv-testing-spec-2026-06-11.md"
)

ALGORITHM_IDS = [
    "kalman_exact_or_mixture_enumeration",
    "ukf",
    "svd_sigma_point",
    "cut4",
    "zhao_cui_scalar_or_multistate",
    "bootstrap_dpf_current",
    "ledh_pfpf_alg1_ukf_current",
]

PROMOTED_ROWS: list[dict[str, Any]] = [
    {
        "row_id": "benchmark_lgssm_exact_oracle_m3_T50",
        "model_family": "linear_gaussian_state_space",
        "source_status": "USER_AMENDED_EXACT_ORACLE_BENCHMARK",
        "promotion_status": "promoted_exact_oracle_benchmark_row",
        "numeric_readiness": "reviewed_evaluator_pending",
        "replaces_or_supersedes": ["lgssm_exact_kalman_dim_1_2_3"],
        "truth_or_test_values": {
            "benchmark_policy": (
                "User-amended exact-oracle LGSSM row. Any valid identifiable "
                "LGSSM is admissible; this row does not claim to reproduce the "
                "Zhao-Cui MATLAB rng(0); rand(3,3) observation matrix."
            ),
            "state_dim": 3,
            "observation_dim": 3,
            "horizon": 50,
            "estimated_parameters": ["phi1", "phi2", "phi3", "q_scale", "r_scale"],
            "truth": {
                "phi1": 0.72,
                "phi2": 0.55,
                "phi3": 0.35,
                "q_scale": 0.35,
                "r_scale": 0.45,
            },
            "prior": {
                "type": "benchmark_box",
                "lower": {
                    "phi1": -0.95,
                    "phi2": -0.95,
                    "phi3": -0.95,
                    "q_scale": 0.05,
                    "r_scale": 0.05,
                },
                "upper": {
                    "phi1": 0.95,
                    "phi2": 0.95,
                    "phi3": 0.95,
                    "q_scale": 2.0,
                    "r_scale": 2.0,
                },
            },
            "transition_matrix": [
                [0.72, 0.0, 0.0],
                [0.0, 0.55, 0.0],
                [0.0, 0.0, 0.35],
            ],
            "observation_matrix": [
                [1.0, 0.25, -0.15],
                [0.2, 1.1, 0.3],
                [-0.1, 0.35, 0.9],
            ],
            "process_covariance": [
                [0.1225, 0.0, 0.0],
                [0.0, 0.1225, 0.0],
                [0.0, 0.0, 0.1225],
            ],
            "observation_covariance": [
                [0.2025, 0.0, 0.0],
                [0.0, 0.2025, 0.0],
                [0.0, 0.0, 0.2025],
            ],
            "initial_mean": [0.0, 0.0, 0.0],
            "initial_covariance_policy": "stationary diagonal covariance q_scale^2 / (1 - phi_i^2)",
            "identifiability_diagnostics": {
                "transition_spectral_radius": 0.72,
                "observation_matrix_rank": 3,
                "observation_matrix_full_rank": True,
                "positive_process_and_observation_covariances": True,
            },
        },
        "source_anchors": [
            "user amendment in dialogue on 2026-06-12: LGSSM may use any valid identifiable exact-oracle model",
            "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-lgssm-oracle-amendment-result-2026-06-12.md",
        ],
        "residual_tasks": [
            "add exact-oracle LGSSM target/evaluator row or mapping adapter",
            "run all algorithms on the T=50 benchmark LGSSM row",
        ],
    },
    {
        "row_id": "zhao_cui_sv_actual_nongaussian_T1000",
        "model_family": "stochastic_volatility_transformed_actual_nongaussian",
        "source_status": "PAPER_AND_AUTHOR_CODE_VALUE_FOUND",
        "promotion_status": "promoted_source_paper_row",
        "numeric_readiness": "reviewed_evaluator_pending",
        "replaces_or_supersedes": ["sv_exact_transformed_actual_nongaussian_dim_1_2_3"],
        "truth_or_test_values": {
            "state_dim": 1,
            "observation_dim": 1,
            "horizon": 1000,
            "fixed_sigma": 1.0,
            "estimated_parameters": ["gamma", "beta"],
            "truth": {"gamma": 0.6, "beta": 0.4},
            "prior": {
                "type": "uniform_box",
                "lower": {"gamma": 0.1, "beta": 0.1},
                "upper": {"gamma": 0.9, "beta": 0.9},
            },
            "initial_state_prior": "x0 | theta ~ N(0, 1 / (1 - gamma^2))",
        },
        "source_anchors": [
            "docs/plans/bayesfilter-p10-truth-prior-literature-audit-result-2026-06-11.md",
            "third_party/audit/zhao_cui_tensor_ssm_p10/source/eg2_sv/mainscript.m",
            "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/sv/setup.m",
        ],
        "residual_tasks": [
            "wire source-paper T=1000 actual transformed SV evaluator for every algorithm",
            "report score/gradient status honestly for stochastic and approximate filters",
        ],
    },
    {
        "row_id": "zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000",
        "model_family": "stochastic_volatility_ksc_gaussian_mixture_surrogate",
        "source_status": "SOURCE_VALUES_FOUND_MIXTURE_DETAILS_SOURCE_GAP",
        "promotion_status": "promoted_surrogate_row_with_explicit_source_gap",
        "numeric_readiness": "reviewed_evaluator_pending",
        "replaces_or_supersedes": ["sv_ksc_gaussian_mixture_surrogate_dim_1_2_3"],
        "truth_or_test_values": {
            "state_dim": 1,
            "observation_dim": 1,
            "horizon": 1000,
            "fixed_sigma": 1.0,
            "estimated_parameters": ["gamma", "beta"],
            "truth": {"gamma": 0.6, "beta": 0.4},
            "prior": {
                "type": "uniform_box",
                "lower": {"gamma": 0.1, "beta": 0.1},
                "upper": {"gamma": 0.9, "beta": 0.9},
            },
            "surrogate_policy": "same SV truth values; Gaussian-mixture observation target is reported as a surrogate, not the actual non-Gaussian target",
        },
        "source_anchors": [
            "docs/plans/bayesfilter-p10-truth-prior-literature-audit-result-2026-06-11.md",
            "third_party/audit/zhao_cui_tensor_ssm_p10/source/eg2_sv/mainscript.m",
            "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/sv/setup.m",
        ],
        "residual_tasks": [
            "inspect or cite KSC mixture-table source before making mixture-specific literature claims",
            "wire source-paper T=1000 surrogate evaluator for every algorithm where applicable",
        ],
    },
    {
        "row_id": "zhao_cui_spatial_sir_austria_j9_T20",
        "model_family": "spatial_sir_austria_fixed_parameter",
        "source_status": "PAPER_AND_AUTHOR_CODE_FIXED_PARAMETER_FOUND",
        "promotion_status": "promoted_source_paper_row_route_repair_required",
        "numeric_readiness": "blocked_value_route_pending_rank_selection_repair",
        "replaces_or_supersedes": [
            "spatial_sir_lower_rung_j1_dim_2",
            "spatial_sir_scaling_route_admitted_rank_selection_blocked_d18",
        ],
        "truth_or_test_values": {
            "J": 9,
            "state_dim": 18,
            "observation_dim": 9,
            "horizon": 20,
            "theta_dimension": 0,
            "fixed_parameters": {
                "kappa": [0.1] * 9,
                "nu": [18.0] * 9,
                "delta": 0.02,
                "rk4_internal_step": 0.005,
                "process_covariance": "identity_18x18",
                "observation_covariance": "100 * identity_9x9",
                "initial_covariance": "identity_18x18",
                "initial_mean": [
                    486.0,
                    14.0,
                    487.0,
                    13.0,
                    488.0,
                    12.0,
                    489.0,
                    11.0,
                    490.0,
                    10.0,
                    491.0,
                    9.0,
                    492.0,
                    8.0,
                    493.0,
                    7.0,
                    494.0,
                    6.0,
                ],
            },
        },
        "source_anchors": [
            "docs/plans/bayesfilter-p10-truth-prior-literature-audit-result-2026-06-11.md",
            "third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m",
            "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/sir_austria/setup.mlx",
        ],
        "residual_tasks": [
            "repair d=18 rank-selection/value route before numeric source-paper SIR performance",
            "keep J=1 lower rung as diagnostic only, not promoted source-paper evidence",
        ],
    },
    {
        "row_id": "zhao_cui_predator_prey_T20",
        "model_family": "predator_prey_additive_gaussian",
        "source_status": "PAPER_AND_AUTHOR_CODE_VALUE_FOUND",
        "promotion_status": "promoted_source_paper_row",
        "numeric_readiness": "reviewed_evaluator_pending",
        "replaces_or_supersedes": [
            "predator_prey_lower_rung_dim_2",
            "predator_prey_production_tuned_h25_dim_2",
        ],
        "truth_or_test_values": {
            "state_dim": 2,
            "observation_dim": 2,
            "horizon": 20,
            "initial_state": [50.0, 5.0],
            "process_covariance": "4 * identity_2x2",
            "observation_covariance": "4 * identity_2x2",
            "paper_physical_truth": {
                "r": 0.6,
                "K": 114.0,
                "a": 25.0,
                "s": 0.3,
                "u": 0.5,
                "v": 0.5,
            },
            "author_code_normalized_truth": [0.6, 1.2, 0.5, 0.3, 0.5, 0.5],
            "author_code_ncons": [0.1, 1.0, 0.1, 0.1, 0.0, 0.0],
            "normalization_notes": {
                "K": "physical K = 90 + 20 * 1.2 = 114",
                "a": "physical a = 20 + 10 * 0.5 = 25",
            },
            "prior_box_physical": {
                "lower": {"r": 0.1, "K": 110.0, "a": 20.0, "s": 0.1, "u": 0.0, "v": 0.0},
                "upper": {"r": 1.1, "K": 130.0, "a": 30.0, "s": 1.1, "u": 1.0, "v": 1.0},
            },
        },
        "source_anchors": [
            "docs/plans/bayesfilter-p10-truth-prior-literature-audit-result-2026-06-11.md",
            "third_party/audit/zhao_cui_tensor_ssm_p10/source/eg4_predatorprey/mainscript.m",
            "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/pp/setup.mlx",
            "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/pp/truetheta.mlx",
        ],
        "residual_tasks": [
            "wire source-paper T=20 predator-prey evaluator for every algorithm",
            "keep T=25 production row as project stress/diagnostic unless explicitly requested",
        ],
    },
    {
        "row_id": "zhao_cui_generalized_sv_synthetic_from_estimated_values",
        "model_family": "generalized_stochastic_volatility_svmodels_synthetic",
        "source_status": "SOURCE_MODEL_AND_SP500_PRIOR_FOUND_PRIOR_MEAN_TEST_POINT_READY",
        "promotion_status": "promoted_source_paper_synthetic_row_prior_mean",
        "numeric_readiness": "reviewed_evaluator_pending",
        "replaces_or_supersedes": ["native_generalized_sv_dense_lower_rung_dim_2"],
        "truth_or_test_values": {
            "benchmark_data_policy": (
                "generate synthetic data from the finite-coordinate mean of "
                "the Zhao-Cui S&P 500 prior distribution; do not use SP500 "
                "returns as benchmark data"
            ),
            "source_real_data_role": (
                "SP500 returns are source-estimation input only, not the "
                "benchmark data series for this amended synthetic row"
            ),
            "legacy_row_id_note": (
                "The row id retains 'estimated_values' for compatibility with "
                "existing P8 artifacts; the current truth/test point is the "
                "S&P prior mean convention, not a posterior estimate."
            ),
            "state_dim": 1,
            "observation_dim": 1,
            "horizon": 1008,
            "source_author_route": "svmodels",
            "parameter_order": ["gamma", "tau", "mu", "phi", "a", "delta", "nu1", "nu2"],
            "estimated_indices": [1, 2, 3],
            "estimated_parameters": ["gamma", "tau", "mu"],
            "paper_prior_contract": {
                "(gamma+1)/2": "Beta(20, 1.5)",
                "sigma_squared": "IG(1, 0.005)",
                "log_beta_given_sigma": "Normal(0, sigma^2 / 0.8)",
                "initial_state": "X0 | gamma, sigma ~ Normal(0, sigma^2 / (1 - gamma^2))",
            },
            "prior_mean_test_point": {
                "status": "ready",
                "mean_convention": (
                    "finite-coordinate prior center: E[(gamma+1)/2], "
                    "E[sigma], and E[log(beta)/sigma]=0"
                ),
                "physical_values": {
                    "gamma": 0.8604651162790697,
                    "tau_or_sigma": 0.12533141373155002,
                    "mu_or_log_beta_center_coordinate": 0.0,
                    "phi": 0.0,
                    "a": 0.0,
                    "delta": 0.0,
                    "nu1": "inf",
                    "nu2": "inf",
                },
                "transformed_active_values": [
                    1.0824113944610982,
                    -2.076793740349318,
                    0.0,
                ],
                "nonfinite_mean_caveats": [
                    "E[sigma^2] is infinite under IG(shape=1, scale=0.005).",
                    "The ordinary unconditional E[beta] is not used.",
                    "This is not a posterior estimate from SP500 returns.",
                ],
            },
            "author_code_defaults_not_estimates": {
                "gamma": 0.95,
                "tau": {"expression": "sqrt(3/64)", "value": 0.21650635094610965},
                "mu": 0.0,
                "phi": 0.0,
                "a": 0.0,
                "delta": 0.0,
                "nu1": "inf",
                "nu2": "inf",
            },
            "source_route_transform_notes": {
                "gamma": "ftt2true uses normcdf, so physical gamma is in (0, 1)",
                "tau": "ftt2true uses exp",
                "mu_phi_a": "when estimated, ftt2true multiplies the transformed coordinate by tau",
                "paper_code_coordinate_caveat": (
                    "the paper writes log(beta)/sigma as the third active "
                    "coordinate, while the mirrored svmodels code names the "
                    "third coordinate mu; both centers are zero for this test point"
                ),
                "delta": "ftt2true uses 4 * (normcdf(x) - 0.5)",
                "nu": "ftt2true uses 5 * x + 20",
            },
            "testing_spec": {
                "json": "docs/plans/bayesfilter-filtering-value-gradient-benchmark-generalized-sv-testing-spec-2026-06-11.json",
                "markdown": "docs/plans/bayesfilter-filtering-value-gradient-benchmark-generalized-sv-testing-spec-2026-06-11.md",
            },
        },
        "source_anchors": [
            ".local_sources/highdim_nonlinear_filtering/zhao_cui_tt_sequential_learning_jmlr_23-0743.pdf",
            "third_party/audit/zhao_cui_tensor_ssm_p10/source/eg2_sv/mainscriptSP500.m",
            "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/svmodels/setup.m",
            "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/svmodels/ftt2true.m",
            "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/svmodels/true2ftt.m",
            "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/svmodels/st_process.m",
            "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/svmodels/ob_process.m",
            "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/svmodels/like.m",
        ],
        "residual_tasks": [
            "wire the source-route svmodels evaluator in TensorFlow/TFP for value and eligible score tables",
            "carry the paper/code third-coordinate caveat into the score-coordinate contract",
            "do not substitute author-code defaults, SP500 returns, or the BayesFilter native generalized-SV fixture for this prior-center row",
        ],
    },
]

EXCLUDED_OR_HISTORICAL_ROWS: list[dict[str, Any]] = [
    {
        "row_id": "p44_cubic_additive_gaussian_dim_1_2_3",
        "disposition": "excluded_from_promoted_source_paper_scope",
        "reason": "BayesFilter P44 diagnostic fixture, not a checked author-paper/code benchmark model",
    },
    {
        "row_id": "p44_quadratic_observation_dim_1_2_3",
        "disposition": "excluded_from_promoted_source_paper_scope",
        "reason": "BayesFilter P44 diagnostic fixture, not a checked author-paper/code benchmark model",
    },
    {
        "row_id": "p44_nonlinear_transition_h2_dim_1_2_3",
        "disposition": "excluded_from_promoted_source_paper_scope",
        "reason": "BayesFilter P44 tanh-transition diagnostic fixture, not a checked author-paper/code benchmark model",
    },
    {
        "row_id": "p44_nonlinear_transition_h4_cut4_extension_dim_1_2_3",
        "disposition": "excluded_from_promoted_source_paper_scope",
        "reason": "BayesFilter P44 tanh-transition diagnostic extension, not a checked author-paper/code benchmark model",
    },
    {
        "row_id": "lgssm_exact_kalman_dim_1_2_3",
        "disposition": "historical_exact_diagnostic_superseded_for_source_paper_scope",
        "reason": "Project P44-M1 exact diagnostic row; amended benchmark uses an explicit identifiable T=50 LGSSM oracle row",
    },
    {
        "row_id": "zhao_cui_lgssm_kalman_m3_T50",
        "disposition": "superseded_by_benchmark_lgssm_exact_oracle_row",
        "reason": (
            "The user amended the LGSSM benchmark policy on 2026-06-12: exact "
            "Zhao-Cui MATLAB rng(0); rand(3,3) reproduction is not required for LGSSM."
        ),
    },
    {
        "row_id": "native_generalized_sv_dense_lower_rung_dim_2",
        "disposition": "excluded_project_fixture_replacement_required",
        "reason": "Project lower-rung fixture; amended source row uses Zhao-Cui svmodels with synthetic data generated from the S&P prior-mean test point",
    },
    {
        "row_id": "zhao_cui_generalized_sv_sp500_author_code",
        "disposition": "superseded_by_synthetic_prior_mean_amendment",
        "reason": "User amended generalized SV benchmark to generate synthetic data from the Zhao-Cui S&P prior-mean convention rather than using SP500 returns directly",
    },
    {
        "row_id": "spatial_sir_lower_rung_j1_dim_2",
        "disposition": "diagnostic_only_not_promoted",
        "reason": "Lower-rung J=1 diagnostic; source-paper row has J=9 and d=18",
    },
    {
        "row_id": "predator_prey_production_tuned_h25_dim_2",
        "disposition": "project_stress_or_diagnostic_not_promoted",
        "reason": "Uses source truth values but horizon differs from the Zhao-Cui T=20 source-paper row",
    },
]


def _rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def _summary_rows(artifact: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in artifact["promoted_or_replacement_source_rows"]:
        rows.append(
            {
                "row_id": row["row_id"],
                "model_family": row["model_family"],
                "scope_class": "source_or_replacement_row",
                "promotion_status": row["promotion_status"],
                "numeric_readiness": row["numeric_readiness"],
                "source_status": row["source_status"],
                "replaces_or_supersedes": ";".join(row["replaces_or_supersedes"]),
            }
        )
    for row in artifact["excluded_or_historical_rows"]:
        rows.append(
            {
                "row_id": row["row_id"],
                "model_family": "N/A",
                "scope_class": "excluded_or_historical_row",
                "promotion_status": row["disposition"],
                "numeric_readiness": "not_in_promoted_source_paper_numeric_tables",
                "source_status": "project_fixture_or_historical",
                "replaces_or_supersedes": "",
            }
        )
    return rows


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    columns = [
        "row_id",
        "model_family",
        "scope_class",
        "promotion_status",
        "numeric_readiness",
        "source_status",
        "replaces_or_supersedes",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _write_markdown(path: Path, rows: list[dict[str, Any]]) -> None:
    columns = [
        "row_id",
        "scope_class",
        "promotion_status",
        "numeric_readiness",
        "source_status",
    ]
    lines = ["| " + " | ".join(columns) + " |"]
    lines.append("| " + " | ".join(["---"] * len(columns)) + " |")
    for row in rows:
        lines.append("| " + " | ".join(str(row[column]) for column in columns) + " |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_artifact() -> dict[str, Any]:
    source_scope_ids = [row["row_id"] for row in PROMOTED_ROWS]
    promoted_ids = [
        row["row_id"]
        for row in PROMOTED_ROWS
        if row["promotion_status"].startswith("promoted_")
    ]
    replacement_required_ids = [
        row["row_id"]
        for row in PROMOTED_ROWS
        if row["promotion_status"] == "replacement_required_before_numeric_promotion"
    ]
    estimates_pending_ids = [
        row["row_id"]
        for row in PROMOTED_ROWS
        if "estimates_pending" in row["promotion_status"]
        or "estimated_values_pending" in row["numeric_readiness"]
    ]
    excluded_ids = [row["row_id"] for row in EXCLUDED_OR_HISTORICAL_ROWS]
    p44_removed = [row_id for row_id in excluded_ids if row_id.startswith("p44_")]
    return {
        "schema_version": "filter_bench.source_paper_scope.v1",
        "metadata_date": "2026-06-11",
        "phase": "FILTER_BENCH_SOURCE_PAPER_BLOCKER_CLOSURE",
        "status": "PASS_FILTER_BENCH_SOURCE_PAPER_SCOPE_CONTRACT",
        "numeric_benchmark_status": "BLOCK_FILTER_BENCH_SOURCE_PAPER_NUMERIC_RUN_PENDING",
        "purpose": (
            "Superseding source-paper scope contract for promoted filtering "
            "value/gradient benchmark execution after removing BayesFilter-only "
            "P44 diagnostic rows."
        ),
        "role_contract": {
            "supervisor_and_executor": "Codex in this dialogue",
            "reviewer": "Claude Code read-only",
            "detached_agent_allowed": False,
        },
        "source_artifacts": {
            "blocker_closure_plan": _rel(PLAN_PATH),
            "p10_literature_audit_result": _rel(P10_RESULT_PATH),
            "historical_p8_contract": _rel(P8_CONTRACT_PATH),
            "visible_runbook": _rel(RUNBOOK_PATH),
            "master_program": _rel(MASTER_PATH),
        },
        "algorithm_ids": ALGORITHM_IDS,
        "source_scope_row_ids": source_scope_ids,
        "promoted_source_row_ids": promoted_ids,
        "replacement_required_source_row_ids": replacement_required_ids,
        "estimated_values_pending_source_row_ids": estimates_pending_ids,
        "p44_diagnostic_rows_removed_from_promoted_scope": p44_removed,
        "promoted_or_replacement_source_rows": PROMOTED_ROWS,
        "excluded_or_historical_rows": EXCLUDED_OR_HISTORICAL_ROWS,
        "scope_policy": {
            "historical_artifacts_preserved": True,
            "old_p8_roster_mutated_in_place": False,
            "future_promoted_numeric_tables_use_this_scope": True,
            "old_ledh_pfpf_ot_current_evidence_allowed": False,
            "preflight_or_smoke_values_are_performance_evidence": False,
            "all_approximate_filters_can_be_attempted_on_source_rows": True,
            "kalman_non_lgssm_policy": "structured not-applicable or declared mixture-surrogate cell status only",
        },
        "remaining_fixable_tasks": [
            "implement exact-oracle LGSSM T=50, source-paper SV T=1000, predator-prey T=20, and KSC surrogate target/evaluator rows",
            "repair or explicitly block spatial SIR J=9 d=18 rank-selection/value route",
            "implement source-route svmodels evaluator for the generalized-SV prior-mean test point",
            "run accepted source values/data/evaluators and produce value, componentwise score, curvature, failure, and stochastic uncertainty tables",
            "ask Claude for read-only execution review before ranking filters or claiming filtering closeout",
        ],
        "decision_table": [
            {
                "decision": "pass_source_paper_scope_contract",
                "primary_criterion": "source-paper rows and exclusions are frozen with source anchors and no P44 diagnostic promotion",
                "veto_diagnostics": "no scope veto fired",
                "main_uncertainty": "numeric evaluator implementation and runs remain pending",
                "next_justified_action": "implement source-paper numeric benchmark phase using this scope",
                "not_concluded": "filter ranking, DPF gradient validity, SIR d=18 readiness, Bayesian-estimation handoff",
            },
            {
                "decision": "block_source_paper_numeric_performance",
                "primary_criterion": "no source-paper numeric benchmark values have been generated in this phase",
                "veto_diagnostics": "numeric-run-pending block active",
                "main_uncertainty": "which route repairs are needed for SIR d=18 and generalized-SV source-route evaluator execution",
                "next_justified_action": "write/execute focused numeric source-paper benchmark implementation plan",
                "not_concluded": "that any algorithm performs better or worse on source-paper rows",
            },
        ],
        "run_manifest": {
            "git_commit": "dirty worktree; source-paper scope artifacts uncommitted",
            "command": "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_emit_source_paper_scope.py",
            "environment": "local Python environment",
            "cpu_gpu_status": "CPU-only metadata/schema emission; no GPU conclusion",
            "seeds": "N/A; no random draws generated",
            "plan_file": _rel(PLAN_PATH),
            "output_json": _rel(DEFAULT_JSON),
            "output_csv": _rel(DEFAULT_CSV),
            "output_markdown": _rel(DEFAULT_MD),
        },
        "nonclaims": [
            "not a numeric benchmark result",
            "not a filter ranking",
            "not a DPF gradient certification",
            "not evidence that source-paper generalized SV adapter exists",
            "not evidence that Zhao-Cui generalized-SV posterior estimated values have been extracted",
            "not evidence that spatial SIR d=18 value route is unblocked",
            "not Bayesian-estimation readiness",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--summary-csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--summary-markdown", type=Path, default=DEFAULT_MD)
    args = parser.parse_args()

    artifact = build_artifact()
    rows = _summary_rows(artifact)
    args.output_json.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
    _write_csv(args.summary_csv, rows)
    _write_markdown(args.summary_markdown, rows)
    print(f"wrote {args.output_json}")
    print(f"status {artifact['status']}")
    print(f"numeric_benchmark_status {artifact['numeric_benchmark_status']}")
    print(f"promoted_or_replacement_rows {len(artifact['promoted_or_replacement_source_rows'])}")
    print(f"excluded_or_historical_rows {len(artifact['excluded_or_historical_rows'])}")


if __name__ == "__main__":
    main()
