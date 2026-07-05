from __future__ import annotations

from types import SimpleNamespace

import pytest

from scripts import audit_ledh_no_autodiff as audit


MANIFEST_PATH = (
    "docs/plans/"
    "bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase2-current-route-manifest-2026-06-23.json"
)
WHITELIST_PATH = (
    "docs/plans/"
    "bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-audit-whitelist-2026-06-23.json"
)
P8_MANIFEST_PATH = (
    "docs/plans/"
    "bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase8-exact-route-manifest-2026-06-23.json"
)


def _manifest() -> dict:
    return audit.load_json(MANIFEST_PATH)


def _whitelist() -> dict:
    return audit.load_json(WHITELIST_PATH)


def _p8_manifest() -> dict:
    return audit.load_json(P8_MANIFEST_PATH)


def test_p7_manifest_closes_selected_outer_tape_ids_but_keeps_certification_open() -> None:
    result = audit.audit_manifest(_manifest(), _whitelist())

    assert result["decision"] == "FAIL_CURRENT_ROUTE"
    failed_p1_ids = set(result["failed_p1_ids"])
    assert "P1-L001" not in failed_p1_ids
    assert "P1-L003" not in failed_p1_ids
    assert "P1-L013" not in failed_p1_ids
    assert "P1-L015" not in failed_p1_ids
    assert result["bad_route_flag_vetoes"] == []
    assert _manifest()["route_flags"]["ad_evaluation_mode"] == "manual-reverse"


def test_p2_custom_gradient_boundary_is_not_automatic_pass() -> None:
    result = audit.audit_manifest(_manifest(), _whitelist())
    boundaries = {
        (item["path"], item["decorator_line"]): item
        for item in result["custom_gradient_boundary_results"]
    }

    manual_finite = boundaries[
        ("experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py", 1960)
    ]
    assert manual_finite["status"] == "PASS_GRAD_BODY_SCAN"
    assert manual_finite["findings"] == []

    blockwise = boundaries[
        ("experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py", 2064)
    ]
    assert blockwise["status"] == "PASS_GRAD_BODY_SCAN"


def test_p8_exact_route_audit_passes_selected_manual_route() -> None:
    result = audit.audit_manifest(_p8_manifest(), _whitelist())

    assert result["decision"] == "PASS_NO_AUTODIFF_AUDIT"
    assert result["production_findings"] == []
    assert result["bad_route_flag_vetoes"] == []
    assert result["unapproved_custom_gradient_boundary_results"] == []
    assert result["raw_production_findings_count"] > 0
    boundaries = {
        (item["path"], item["decorator_line"]): item
        for item in result["custom_gradient_boundary_results"]
    }
    selected = boundaries[
        ("experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py", 1960)
    ]
    assert selected["status"] == "PASS_GRAD_BODY_SCAN"


def test_p8_exact_route_bad_flags_still_veto() -> None:
    manifest = _p8_manifest()
    manifest["route_flags"] = dict(manifest["route_flags"])
    manifest["route_flags"]["transport_gradient_mode"] = "filterflow_custom_op"

    result = audit.audit_manifest(manifest, _whitelist())

    assert result["decision"] == "FAIL_CURRENT_ROUTE"
    assert {
        "flag": "transport_gradient_mode",
        "value": "filterflow_custom_op",
        "reason": "bad_production_route_flag",
    } in result["bad_route_flag_vetoes"]


def test_p8_exact_route_unapproved_custom_gradient_boundary_fails() -> None:
    manifest = _p8_manifest()
    manifest["allowed_custom_gradient_boundaries"] = []
    manifest["excluded_symbols"] = [
        entry
        for entry in manifest["excluded_symbols"]
        if entry["symbol"] != "_filterflow_manual_streaming_finite_transport_stopped_scale_keys"
    ]

    result = audit.audit_manifest(manifest, _whitelist())

    assert result["decision"] == "FAIL_CURRENT_ROUTE"
    assert any(
        item["decorator_line"] == 1960
        for item in result["unapproved_custom_gradient_boundary_results"]
    )


def test_p6_transport_replay_route_grad_body_has_no_autodiff() -> None:
    result = audit.audit_manifest(_manifest(), _whitelist())
    boundaries = {
        (item["path"], item["decorator_line"]): item
        for item in result["custom_gradient_boundary_results"]
    }

    manual_finite = boundaries[
        ("experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py", 1960)
    ]

    assert manual_finite["status"] == "PASS_GRAD_BODY_SCAN"
    assert not any(
        finding["pattern"] in {"tf.GradientTape", "GradientTape(", ".gradient("}
        for finding in manual_finite["findings"]
    )


def test_p2_whitelist_rejects_directory_and_production_entries() -> None:
    manifest = _manifest()
    whitelist = {
        "schema_version": "test",
        "zero_default": True,
        "entries": [
            {"path_prefix": "tests/", "reason": "too broad"},
            {
                "path": "docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py",
                "reason": "production route cannot be whitelisted",
            },
        ],
    }

    vetoes = audit.validate_whitelist(whitelist, manifest["production_files"])

    reasons = {item["reason"] for item in vetoes}
    assert "directory_wide_entry" in reasons
    assert "production_path_whitelisted" in reasons


@pytest.mark.parametrize(
    ("flag", "value"),
    [
        ("transport_ad_mode", "full"),
        ("ad_evaluation_mode", "reverse-gradient"),
        ("ad_evaluation_mode", "forward-jvp"),
        ("transport_gradient_mode", "filterflow_custom_op"),
    ],
)
def test_p2_bad_route_flags_are_vetoed(flag: str, value: str) -> None:
    manifest = _manifest()
    manifest["route_flags"] = dict(manifest["route_flags"])
    manifest["route_flags"][flag] = value

    vetoes = audit.bad_route_flag_vetoes(manifest["route_flags"])

    assert {"flag": flag, "value": value, "reason": "bad_production_route_flag"} in vetoes


def test_p2_runtime_sentinel_blocks_and_restores_autodiff_entrypoints() -> None:
    def gradient_tape() -> str:
        return "original_tape"

    def forward_accumulator() -> str:
        return "original_accumulator"

    fake_tf = SimpleNamespace(
        GradientTape=gradient_tape,
        autodiff=SimpleNamespace(ForwardAccumulator=forward_accumulator),
    )

    with audit.AutodiffRuntimeSentinel(fake_tf, route_id="test_route"):
        with pytest.raises(audit.RuntimeAutodiffViolation, match="GradientTape"):
            fake_tf.GradientTape()
        with pytest.raises(audit.RuntimeAutodiffViolation, match="ForwardAccumulator"):
            fake_tf.autodiff.ForwardAccumulator()

    assert fake_tf.GradientTape() == "original_tape"
    assert fake_tf.autodiff.ForwardAccumulator() == "original_accumulator"
