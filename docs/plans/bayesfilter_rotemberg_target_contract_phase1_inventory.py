#!/usr/bin/env python3
"""Read-only Rotemberg target-contract reconstruction inventory.

This helper does not import or execute legacy model code.  It reads fixed JSON
artifacts and source text from /home/chakwong/python, records file hashes, and
classifies whether each generic SSMTargetContract field is supported, blocked,
or requires a later reviewed decision.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import socket
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
LEGACY_ROOT = Path("/home/chakwong/python")

PHASE4_BRIDGE_JSON = (
    REPO_ROOT
    / "docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase4-target-signature-bridge-2026-07-04.json"
)
PHASE4_RESULT = (
    REPO_ROOT
    / "docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase4-target-signature-bridge-result-2026-07-04.md"
)
PREFLIGHT_JSON = (
    LEGACY_ROOT
    / "docs/plans/artifacts/rotemberg-linear-kalman-certified-neutra-2026-06-22/phase5/preflight/rotemberg_linear_kalman_target_preflight.json"
)
CERTIFICATE_JSON = (
    LEGACY_ROOT
    / "docs/plans/artifacts/rotemberg-linear-kalman-certified-neutra-2026-06-22/phase5/preflight/rotemberg_linear_kalman_structural_certificate.json"
)
CANARY_TRAINING_STATE = (
    LEGACY_ROOT
    / "docs/plans/artifacts/rotemberg-linear-kalman-certified-neutra-2026-06-22/phase7/rotemberg_trainable_canary.json.training_state.json"
)
PREFLIGHT_SCRIPT = LEGACY_ROOT / "scripts/prepare_neutra_rotemberg_linear_kalman_target.py"
BASELINE_SCRIPT = LEGACY_ROOT / "scripts/run_neutra_paper_style_at_baseline.py"
ROTEMBERG_SOURCE = LEGACY_ROOT / "src/dsge_hmc/models/rotemberg_nk.py"
BAYESFILTER_SVD_SOURCE = REPO_ROOT / "bayesfilter/linear/kalman_svd_derivatives_tf.py"
GENERIC_CONTRACT_SOURCE = REPO_ROOT / "bayesfilter/ssm/contracts.py"

SERIOUS_BASELINE_PATHS = (
    LEGACY_ROOT
    / "docs/plans/artifacts/rotemberg-linear-kalman-certified-neutra-2026-06-22/executable_contract_2026-06-23/serious_baseline_launch_2026-06-23/run/paper_dense_iaf_seed20260622.json",
    LEGACY_ROOT
    / "docs/plans/artifacts/rotemberg-linear-kalman-certified-neutra-2026-06-22/executable_contract_2026-06-23/serious_baseline_launch_2026-06-23/run/paper_dense_iaf_seed20260622_replay_state.json",
    LEGACY_ROOT
    / "docs/plans/artifacts/rotemberg-linear-kalman-certified-neutra-2026-06-22/executable_contract_2026-06-23/serious_baseline_launch_2026-06-23/run/paper_dense_iaf_seed20260622.training_state.json",
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    bridge = _read_json(PHASE4_BRIDGE_JSON)
    preflight = _read_json(PREFLIGHT_JSON)
    certificate = _read_json(CERTIFICATE_JSON)
    canary_training_state = _read_json(CANARY_TRAINING_STATE)

    rotemberg_embedded_payloads = [
        row
        for row in bridge.get("bridge_candidates", [])
        if row.get("is_embedded_payload_candidate") and "rotemberg" in str(row.get("path", "")).lower()
    ]

    source_hashes = {
        "phase4_bridge_json": _file_record(PHASE4_BRIDGE_JSON),
        "phase4_result": _file_record(PHASE4_RESULT),
        "preflight_json": _file_record(PREFLIGHT_JSON),
        "structural_certificate_json": _file_record(CERTIFICATE_JSON),
        "canary_training_state_json": _file_record(CANARY_TRAINING_STATE),
        "prepare_preflight_script": _file_record(PREFLIGHT_SCRIPT),
        "baseline_runner_script": _file_record(BASELINE_SCRIPT),
        "rotemberg_source": _file_record(ROTEMBERG_SOURCE),
        "bayesfilter_svd_score_source": _file_record(BAYESFILTER_SVD_SOURCE),
        "generic_contract_source": _file_record(GENERIC_CONTRACT_SOURCE),
    }

    source_anchors = {
        "preflight_data_and_target_builder": _anchor(
            PREFLIGHT_SCRIPT,
            213,
            248,
            "model/data simulation and BayesFilter linear-Kalman adapter construction",
        ),
        "runner_preflight_validation": _anchor(
            BASELINE_SCRIPT,
            3768,
            3908,
            "legacy runner validation of preflight/certificate/data/probe hashes",
        ),
        "parameter_names_constructor": _anchor(
            ROTEMBERG_SOURCE,
            360,
            378,
            "15 parameter names selected when estimate_obs_noise=False",
        ),
        "derivative_contract": _anchor(
            ROTEMBERG_SOURCE,
            2745,
            2805,
            "Rotemberg linear-Kalman derivative contract and computational state dimension",
        ),
        "transform_and_prior": _anchor(
            ROTEMBERG_SOURCE,
            3850,
            4100,
            "unconstrained transform and analytical prior value/score",
        ),
        "generic_contract_fields": _anchor(
            GENERIC_CONTRACT_SOURCE,
            62,
            449,
            "BayesFilter generic SSMTargetContract field requirements",
        ),
    }

    field_support = _field_support(preflight, certificate)
    required_field_classifications = _required_field_classifications(field_support)
    artifact_presence = _artifact_presence(preflight, canary_training_state)
    draft_contract = _draft_contract_manifest(preflight, certificate, source_hashes)

    blockers = _blockers(field_support, artifact_presence, required_field_classifications)
    status = (
        "PHASE1_RECONSTRUCTION_INVENTORY_COMPLETE_WITH_BLOCKERS"
        if blockers
        else "PHASE1_RECONSTRUCTION_INVENTORY_COMPLETE_CONTRACT_READY_FOR_REVIEW"
    )

    payload: dict[str, Any] = {
        "schema": "bayesfilter.rotemberg_target_contract_reconstruction.phase1_inventory.v1",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "created_at_local_date": "2026-07-04",
        "hostname": socket.gethostname(),
        "status": status,
        "phase4_bridge_json": str(PHASE4_BRIDGE_JSON),
        "rotemberg_embedded_payload_candidates": rotemberg_embedded_payloads,
        "rotemberg_embedded_payload_candidate_count": len(rotemberg_embedded_payloads),
        "source_records": source_hashes,
        "source_anchors": source_anchors,
        "artifact_presence": artifact_presence,
        "field_support": field_support,
        "required_field_classifications": required_field_classifications,
        "draft_contract_manifest": draft_contract,
        "blockers": blockers,
        "cpu_gpu_status": "CPU-only/read-only metadata inventory; no GPU/CUDA device was probed or used",
        "network_status": "No network fetch",
        "external_mutation": "None; /home/chakwong/python was read-only",
        "nonclaims": [
            "metadata reconstruction inventory only",
            "no canonical target_signature minted",
            "no historical transport payload exported",
            "no historical artifact loaded through BayesFilter",
            "no HMC convergence claim",
            "no posterior correctness claim",
            "no sampler superiority claim",
            "no GPU readiness claim",
            "no default policy change",
        ],
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _required_field_classifications(field_support: dict[str, Any]) -> dict[str, Any]:
    problem = field_support["problem_id"]
    static_shape = field_support["static_shape"]
    data_signature = field_support["data_signature"]
    chart = field_support["parameter_chart"]
    prior = field_support["parameter_prior"]
    filter_program = field_support["filter_program"]
    model_manifest = field_support["model_manifest"]

    static_value = static_shape["proposed_value"]
    data_value = data_signature["proposed_value"]
    chart_value = chart["proposed_value"]
    prior_value = prior["proposed_value"]
    filter_value = filter_program["proposed_value"]
    model_value = model_manifest["proposed_value"]

    return {
        "SSMTargetContract.problem.BayesianSSMProblem.problem_id": _classification(
            "supported", problem["value"], problem["evidence"]
        ),
        "SSMTargetContract.problem.static_shape.horizon": _classification(
            "supported", static_value["horizon"], static_shape["evidence"]
        ),
        "SSMTargetContract.problem.static_shape.state_dim": _classification(
            static_shape["status"],
            static_value["state_dim"],
            static_shape["evidence"],
            note=static_shape["required_decision"],
        ),
        "SSMTargetContract.problem.static_shape.observation_dim": _classification(
            "supported", static_value["observation_dim"], static_shape["evidence"]
        ),
        "SSMTargetContract.problem.static_shape.innovation_dim": _classification(
            "supported", static_value["innovation_dim"], static_shape["evidence"]
        ),
        "SSMTargetContract.problem.static_shape.parameter_dim": _classification(
            "supported", static_value["parameter_dim"], static_shape["evidence"]
        ),
        "SSMTargetContract.problem.data_signature.dataset_id": _classification(
            "supported", data_value["dataset_id"], data_signature["evidence"]
        ),
        "SSMTargetContract.problem.data_signature.observation_shape": _classification(
            "supported", data_value["observation_shape"], data_signature["evidence"]
        ),
        "SSMTargetContract.problem.data_signature.mask_shape": _classification(
            "supported", data_value["mask_shape"], data_signature["evidence"]
        ),
        "SSMTargetContract.problem.data_signature.data_hash": _classification(
            "supported", data_value["data_hash"], data_signature["evidence"]
        ),
        "SSMTargetContract.problem.target_coordinate_convention": _classification(
            "supported", "unconstrained", model_manifest["evidence"]
        ),
        "SSMTargetContract.problem.model_manifest.model_id": _classification(
            "supported", model_value["model_id"], model_manifest["evidence"]
        ),
        "SSMTargetContract.problem.model_manifest.model_hash": _classification(
            "supported", "sha256:<rotemberg_source_sha256>", model_manifest["evidence"]
        ),
        "SSMTargetContract.problem.model_manifest.capabilities": _classification(
            "supported", model_value["capabilities"], model_manifest["evidence"]
        ),
        "SSMTargetContract.chart.parameter_names": _classification(
            "supported", chart_value["parameter_names"], chart["evidence"]
        ),
        "SSMTargetContract.chart.unconstrained_dim": _classification(
            "supported", chart_value["unconstrained_dim"], chart["evidence"]
        ),
        "SSMTargetContract.chart.constrained_shape": _classification(
            "supported", chart_value["constrained_shape"], chart["evidence"]
        ),
        "SSMTargetContract.chart.transform_manifest.transform_id": _classification(
            "supported", chart_value["transform_id"], chart["evidence"]
        ),
        "SSMTargetContract.chart.transform_manifest.transform_hash": _classification(
            "supported", "sha256:<rotemberg_source_sha256>", chart["evidence"]
        ),
        "SSMTargetContract.chart.log_jacobian_convention": _classification(
            "supported", chart_value["log_jacobian_convention"], chart["evidence"]
        ),
        "SSMTargetContract.prior.prior_manifest.prior_id": _classification(
            "supported", prior_value["prior_id"], prior["evidence"]
        ),
        "SSMTargetContract.prior.prior_manifest.prior_hash": _classification(
            "supported", "sha256:<rotemberg_source_sha256>", prior["evidence"]
        ),
        "SSMTargetContract.prior.support_policy": _classification(
            "supported", prior_value["support_policy"], prior["evidence"]
        ),
        "SSMTargetContract.prior.log_density_authority": _classification(
            "supported", prior_value["log_density_authority"], prior["evidence"]
        ),
        "SSMTargetContract.filter_program.filter_id": _classification(
            "supported", filter_value["filter_id"], filter_program["evidence"]
        ),
        "SSMTargetContract.filter_program.required_model_capabilities": _classification(
            "supported",
            filter_value["required_model_capabilities"],
            filter_program["evidence"],
        ),
        "SSMTargetContract.filter_program.deterministic_target_policy": _classification(
            "supported",
            filter_value["deterministic_target_policy"],
            filter_program["evidence"],
        ),
        "SSMTargetContract.filter_program.approximation_semantics": _classification(
            "supported", filter_value["approximation_semantics"], filter_program["evidence"]
        ),
        "SSMTargetContract.filter_program.filter_manifest.filter_id": _classification(
            "supported", filter_value["filter_id"], filter_program["evidence"]
        ),
        "SSMTargetContract.filter_program.filter_manifest.filter_hash": _classification(
            "supported",
            "sha256:<bayesfilter_svd_score_source_sha256>",
            filter_program["evidence"],
        ),
        "SSMTargetContract.frozen_transport": _classification(
            "not_applicable_untransported_signature",
            None,
            [
                str(GENERIC_CONTRACT_SOURCE) + ":394",
                str(PHASE4_RESULT),
            ],
            note=(
                "Phase 1 reconstructs the untransported target signature only; "
                "frozen transport binding belongs to a later bridge/load phase."
            ),
        ),
    }


def _classification(
    status: str,
    value: Any,
    evidence: list[str],
    *,
    note: str | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "status": status,
        "value": value,
        "evidence": list(evidence),
    }
    if note is not None:
        payload["note"] = note
    return payload


def _field_support(preflight: dict[str, Any], certificate: dict[str, Any]) -> dict[str, Any]:
    data = preflight.get("data", {})
    model = preflight.get("model", {})
    derivative_contract = model.get("derivative_contract", {})
    u_space = derivative_contract.get("parameter_spaces", {}).get("unconstrained_u", {})
    filt = preflight.get("filter", {})
    target_wrapper = preflight.get("target_wrapper", {})
    target_identity = {
        "problem_id": "rotemberg_linear_kalman_local",
        "model_class": model.get("class"),
        "target_surface": model.get("target_surface"),
        "estimate_obs_noise": model.get("estimate_obs_noise"),
        "target_coordinate_convention": "unconstrained",
    }
    state_dim_candidates = {
        "structural_state_dim_from_model": model.get("state_dim"),
        "bayesfilter_computational_state_dim": model.get("bayesfilter_computational_state_dim"),
        "structural_certificate_minimal_filter_state_count": len(
            certificate.get("minimal_filter_state_names", [])
        ),
    }
    return {
        "problem_id": {
            "status": "supported",
            "value": target_identity["problem_id"],
            "evidence": [
                str(PREFLIGHT_JSON),
                str(CERTIFICATE_JSON),
                str(BASELINE_SCRIPT) + ":3768",
            ],
        },
        "static_shape": {
            "status": "supported_with_semantic_decision_required",
            "proposed_value": {
                "horizon": data.get("t_obs"),
                "state_dim": model.get("bayesfilter_computational_state_dim"),
                "observation_dim": model.get("observation_dim"),
                "innovation_dim": model.get("innovation_dim"),
                "parameter_dim": u_space.get("dim"),
            },
            "state_dim_candidates": state_dim_candidates,
            "required_decision": (
                "Use BayesFilter computational state_dim=6 for the generic target "
                "signature, while recording structural_state_dim=4 as model metadata."
            ),
            "evidence": [
                str(PREFLIGHT_JSON),
                str(PREFLIGHT_SCRIPT) + ":229",
                str(PREFLIGHT_SCRIPT) + ":235",
                str(ROTEMBERG_SOURCE) + ":2745",
            ],
        },
        "data_signature": {
            "status": "supported",
            "proposed_value": {
                "dataset_id": "rotemberg_linear_kalman_local/simulated_seed42_t40",
                "observation_shape": data.get("shape"),
                "mask_shape": None,
                "data_hash": "sha256:" + str(data.get("sha256")),
            },
            "evidence": [
                str(PREFLIGHT_JSON),
                str(PREFLIGHT_SCRIPT) + ":216",
                str(PREFLIGHT_SCRIPT) + ":219",
            ],
        },
        "parameter_chart": {
            "status": "supported",
            "proposed_value": {
                "parameter_names": model.get("param_names"),
                "unconstrained_dim": u_space.get("dim"),
                "constrained_shape": [int(u_space.get("dim", 0))],
                "transform_id": "RotembergNKEstimable.transform_from_unconstrained.estimate_obs_noise_false",
                "log_jacobian_convention": "included_in_prior",
            },
            "evidence": [
                str(PREFLIGHT_JSON),
                str(ROTEMBERG_SOURCE) + ":360",
                str(ROTEMBERG_SOURCE) + ":3850",
                str(ROTEMBERG_SOURCE) + ":3939",
            ],
        },
        "parameter_prior": {
            "status": "supported",
            "proposed_value": {
                "prior_id": "RotembergNKEstimable.log_prior_value_and_score_analytical_batch.estimate_obs_noise_false",
                "support_policy": "enforced_by_transform",
                "log_density_authority": "reviewed_external_adapter",
            },
            "evidence": [
                str(PREFLIGHT_JSON),
                str(ROTEMBERG_SOURCE) + ":3939",
                str(ROTEMBERG_SOURCE) + ":3999",
                str(PREFLIGHT_JSON) + "#batched_value_score_parity.metadata.prior_score_source",
            ],
        },
        "filter_program": {
            "status": "supported",
            "proposed_value": {
                "filter_id": "bayesfilter.linear.svd_graph_status_linear_gaussian",
                "required_model_capabilities": [
                    "time_invariant_linear_gaussian_state_space",
                    "first_order_state_space_derivatives_unconstrained_u",
                    "analytical_prior_value_score",
                    "dense_observations",
                ],
                "deterministic_target_policy": "deterministic",
                "approximation_semantics": "exact",
                "implementation_backend": "tensorflow_probability_tensorflow_float64",
            },
            "evidence": [
                str(PREFLIGHT_JSON),
                str(CERTIFICATE_JSON),
                str(BAYESFILTER_SVD_SOURCE),
                str(BASELINE_SCRIPT) + ":3824",
                str(BASELINE_SCRIPT) + ":3854",
            ],
        },
        "model_manifest": {
            "status": "supported",
            "proposed_value": target_identity
            | {
                "model_id": "RotembergNKEstimable.first_order_linear_kalman.estimate_obs_noise_false",
                "capabilities": [
                    "time_invariant_linear_gaussian_state_space",
                    "first_order_state_space_derivatives_unconstrained_u",
                    "analytical_prior_value_score",
                    "dense_observations",
                ],
            },
            "evidence": [
                str(PREFLIGHT_JSON),
                str(CERTIFICATE_JSON),
                str(ROTEMBERG_SOURCE),
            ],
        },
    }


def _artifact_presence(preflight: dict[str, Any], canary_training_state: dict[str, Any]) -> dict[str, Any]:
    return {
        "phase4_embedded_training_state": {
            "path": str(CANARY_TRAINING_STATE),
            "exists": CANARY_TRAINING_STATE.exists(),
            "target": canary_training_state.get("target"),
            "completed_steps": canary_training_state.get("completed_steps"),
            "artifact_role": "embedded canary training state, not serious baseline",
        },
        "serious_baseline_files": [
            _file_record(path, hash_missing=False) for path in SERIOUS_BASELINE_PATHS
        ],
        "serious_baseline_summary_only": {
            "path": str(
                LEGACY_ROOT
                / "docs/plans/BayesFilterDSGE/rotemberg-fixed-neutra-serious-training-state-artifact-summary-2026-06-28.md"
            ),
            "exists": (
                LEGACY_ROOT
                / "docs/plans/BayesFilterDSGE/rotemberg-fixed-neutra-serious-training-state-artifact-summary-2026-06-28.md"
            ).exists(),
            "classification": (
                "summary_evidence_only_until actual serious baseline JSON files are present in this local filesystem"
            ),
        },
        "preflight_checks_passed": preflight.get("checks", {}).get("passed"),
        "preflight_veto_reasons": preflight.get("veto_reasons"),
    }


def _draft_contract_manifest(
    preflight: dict[str, Any],
    certificate: dict[str, Any],
    source_hashes: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    model = preflight.get("model", {})
    data = preflight.get("data", {})
    u_space = (
        model.get("derivative_contract", {})
        .get("parameter_spaces", {})
        .get("unconstrained_u", {})
    )
    return {
        "status": "draft_not_canonical_signature",
        "problem": {
            "problem_id": "rotemberg_linear_kalman_local",
            "static_shape": {
                "horizon": data.get("t_obs"),
                "state_dim": model.get("bayesfilter_computational_state_dim"),
                "observation_dim": model.get("observation_dim"),
                "innovation_dim": model.get("innovation_dim"),
                "parameter_dim": u_space.get("dim"),
            },
            "data_signature": {
                "dataset_id": "rotemberg_linear_kalman_local/simulated_seed42_t40",
                "observation_shape": data.get("shape"),
                "mask_shape": None,
                "data_hash": "sha256:" + str(data.get("sha256")),
            },
            "target_coordinate_convention": "unconstrained",
            "model_manifest": {
                "model_id": "RotembergNKEstimable.first_order_linear_kalman.estimate_obs_noise_false",
                "model_hash": "sha256:" + source_hashes["rotemberg_source"]["sha256"],
                "model_class": model.get("class"),
                "target_surface": model.get("target_surface"),
                "estimate_obs_noise": model.get("estimate_obs_noise"),
                "structural_state_dim": model.get("state_dim"),
                "structural_certificate_sha256": (
                    "sha256:" + source_hashes["structural_certificate_json"]["sha256"]
                ),
                "preflight_sha256": "sha256:" + source_hashes["preflight_json"]["sha256"],
                "capabilities": [
                    "time_invariant_linear_gaussian_state_space",
                    "first_order_state_space_derivatives_unconstrained_u",
                    "analytical_prior_value_score",
                    "dense_observations",
                ],
            },
        },
        "chart": {
            "parameter_names": model.get("param_names"),
            "unconstrained_dim": u_space.get("dim"),
            "constrained_shape": [u_space.get("dim")],
            "transform_manifest": {
                "transform_id": "RotembergNKEstimable.transform_from_unconstrained.estimate_obs_noise_false",
                "transform_hash": "sha256:" + source_hashes["rotemberg_source"]["sha256"],
                "source_anchor": str(ROTEMBERG_SOURCE) + ":3850-3900",
            },
            "log_jacobian_convention": "included_in_prior",
        },
        "prior": {
            "prior_manifest": {
                "prior_id": "RotembergNKEstimable.log_prior_value_and_score_analytical_batch.estimate_obs_noise_false",
                "prior_hash": "sha256:" + source_hashes["rotemberg_source"]["sha256"],
                "source_anchor": str(ROTEMBERG_SOURCE) + ":3939-4100",
            },
            "support_policy": "enforced_by_transform",
            "log_density_authority": "reviewed_external_adapter",
        },
        "filter_program": {
            "filter_id": "bayesfilter.linear.svd_graph_status_linear_gaussian",
            "required_model_capabilities": [
                "time_invariant_linear_gaussian_state_space",
                "first_order_state_space_derivatives_unconstrained_u",
                "analytical_prior_value_score",
                "dense_observations",
            ],
            "deterministic_target_policy": "deterministic",
            "approximation_semantics": "exact",
            "filter_manifest": {
                "filter_id": "bayesfilter.linear.svd_graph_status_linear_gaussian",
                "filter_hash": "sha256:" + source_hashes["bayesfilter_svd_score_source"]["sha256"],
                "filter_class": preflight.get("filter", {}).get("class"),
                "filter_gradient_api": preflight.get("filter", {}).get("filter_gradient_api"),
                "structural_certificate_sha256": (
                    "sha256:" + source_hashes["structural_certificate_json"]["sha256"]
                ),
            },
        },
    }


def _blockers(
    field_support: dict[str, Any],
    artifact_presence: dict[str, Any],
    required_field_classifications: dict[str, Any],
) -> list[dict[str, Any]]:
    blockers: list[dict[str, Any]] = []
    if any("status" not in item for item in required_field_classifications.values()):
        blockers.append(
            {
                "code": "BLOCK_REQUIRED_FIELD_CLASSIFICATION_MISSING_STATUS",
                "meaning": "At least one required field classification lacks a status.",
                "fixable_in_next_phase": False,
            }
        )
    static_status = field_support.get("static_shape", {}).get("status")
    if static_status == "supported_with_semantic_decision_required":
        blockers.append(
            {
                "code": "BLOCK_STATE_DIM_SEMANTIC_DECISION",
                "meaning": (
                    "Canonical signature minting needs a reviewed decision to use "
                    "BayesFilter computational state_dim=6 rather than structural state_dim=4."
                ),
                "fixable_in_next_phase": True,
            }
        )
    missing_serious = [
        item for item in artifact_presence.get("serious_baseline_files", []) if not item.get("exists")
    ]
    if missing_serious:
        blockers.append(
            {
                "code": "BLOCK_SERIOUS_BASELINE_PAYLOAD_ABSENT_LOCALLY",
                "meaning": (
                    "The serious Rotemberg linear/Kalman baseline files are referenced "
                    "by summaries but are not present at their expected local paths."
                ),
                "missing_paths": [item["path"] for item in missing_serious],
                "fixable_in_next_phase": False,
            }
        )
    return blockers


def _anchor(path: Path, start_line: int, end_line: int, description: str) -> dict[str, Any]:
    return {
        "path": str(path),
        "start_line": int(start_line),
        "end_line": int(end_line),
        "description": description,
        "exists": path.exists(),
        "sha256": _sha256(path) if path.exists() else None,
    }


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _file_record(path: Path, *, hash_missing: bool = True) -> dict[str, Any]:
    exists = path.exists()
    record: dict[str, Any] = {
        "path": str(path),
        "exists": exists,
        "size_bytes": path.stat().st_size if exists else None,
        "sha256": None,
    }
    if exists or hash_missing:
        record["sha256"] = _sha256(path) if exists else None
    return record


if __name__ == "__main__":
    main()
