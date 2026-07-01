from __future__ import annotations

import json
import re

import pytest

import bayesfilter
from bayesfilter.inference import (
    SEQUENTIAL_RHAT_CHECKPOINT_PUBLIC_REFERENCE_FIELDS,
    assert_sequential_rhat_checkpoint_public_reference_safe,
    build_sequential_rhat_checkpoint_public_reference,
    sequential_rhat_verification_checkpoint_contract,
)


_HASH = "a" * 64
_OPAQUE_ID = "srhat-v1-" + "0123456789abcdef0123456789abcdef"


def test_sequential_rhat_checkpoint_contract_separates_public_and_private_fields() -> None:
    contract = sequential_rhat_verification_checkpoint_contract()

    assert contract["artifact_type"] == "bayesfilter_sequential_rhat_checkpoint_contract"
    assert contract["public_reference_artifact_type"] == (
        "bayesfilter_sequential_rhat_checkpoint_public_reference"
    )
    assert contract["private_manifest_artifact_type"] == (
        "bayesfilter_private_sequential_rhat_checkpoint_manifest"
    )
    assert set(contract["checkpoint_kinds"]) == {
        "pre_verification_handoff",
        "verification_chunk",
    }
    assert re.fullmatch(contract["hash_pattern"], _HASH)
    assert re.fullmatch(
        contract["opaque_checkpoint_id_pattern"],
        _OPAQUE_ID,
    )
    assert contract["opaque_checkpoint_id_policy"] == {
        "format": "srhat-v1-<32 lowercase hex chars>",
        "semantic_payload_allowed": False,
        "generation_source": "private manifest or writer nonce/hash material",
        "forbidden_semantic_tokens": [
            "run",
            "chunk",
            "handoff",
            "sample",
            "state",
            "trace",
            "target",
            "accept",
            "step",
            "leapfrog",
            "mass",
            "kernel",
            "manifest",
            "path",
            "private",
            "result",
            "verification",
        ],
    }
    assert set(contract["public_reference_fields"]) == set(
        SEQUENTIAL_RHAT_CHECKPOINT_PUBLIC_REFERENCE_FIELDS
    )
    assert contract["public_id_fields"] == ["checkpoint_id"]
    assert contract["public_hash_fields"] == ["checkpoint_sha256", "contract_sha256"]

    private_fields = set(contract["private_manifest_required_fields"])
    assert "manifest_path" in private_fields
    assert "private_shards" in private_fields
    assert "private_diagnostics" in private_fields
    assert "samples_shard" in contract["private_verification_chunk_fields"]
    assert "selected_kernel_private_payload" in contract["private_handoff_fields"]
    assert contract["private_manifest_schema"] == {
        "artifact_type": "literal private_manifest_artifact_type",
        "schema_version": "integer 1",
        "checkpoint_kind": "one of checkpoint_kinds",
        "checkpoint_id": "matches opaque_checkpoint_id_pattern",
        "manifest_path": "private absolute or caller-private relative path",
        "manifest_core_sha256": (
            "lowercase sha256 hex over manifest core payload excluding this field"
        ),
        "config_private_signature": "lowercase sha256 hex over private config payload",
        "adapter_signature": "stable non-empty adapter signature string",
        "created_at_utc": "ISO-8601 UTC timestamp",
        "private_shards": "mapping of shard role to shard_record",
        "private_diagnostics": "private_diagnostics_record",
        "privacy_contract": "privacy_contract_record",
        "nonclaims": "non-empty sequence including no posterior convergence claim",
    }
    shard_schema = contract["private_shard_record_schema"]
    assert set(shard_schema) == {
        "role",
        "path",
        "sha256",
        "bytes",
        "shape",
        "dtype",
        "serializer",
    }
    assert "never allowed in public progress" in shard_schema["path"]
    assert contract["private_shard_roles"] == [
        "samples",
        "valid_mask",
        "final_state",
        "reduced_trace",
        "target_log_prob_summary",
        "log_accept_ratio_summary",
        "rhat_summary",
        "selected_kernel_private_payload",
        "mass_payload",
    ]
    assert contract["private_manifest_required_shard_roles_by_kind"] == {
        "pre_verification_handoff": [
            "selected_kernel_private_payload",
            "final_state",
            "mass_payload",
        ],
        "verification_chunk": [
            "samples",
            "valid_mask",
            "final_state",
            "reduced_trace",
            "target_log_prob_summary",
            "log_accept_ratio_summary",
            "rhat_summary",
        ],
    }
    diagnostic_schema = contract["private_diagnostics_record_schema"]
    assert set(diagnostic_schema) == {
        "chunk_index",
        "retained_sample_count",
        "valid_sample_count",
        "nonfinite_valid_sample_count",
        "rhat_summary",
        "acceptance_summary",
        "target_log_prob_summary",
        "divergence_summary",
    }
    assert contract["rhat_summary_schema"] == {
        "rhat_threshold": "positive finite float greater than 1",
        "max_finite_rhat": "finite float or null",
        "finite_rhat_count": "non-negative integer",
        "nonfinite_rhat_count": "non-negative integer",
        "all_finite_rhat_at_or_below_threshold": "boolean",
    }
    assert contract["log_accept_ratio_summary_schema"] == {
        "finite_count": "non-negative integer",
        "nonfinite_count": "non-negative integer",
        "max_abs_finite": "finite float or null",
    }
    assert contract["target_log_prob_summary_schema"] == {
        "finite_count": "non-negative integer",
        "nonfinite_count": "non-negative integer",
        "min_finite": "finite float or null",
        "max_finite": "finite float or null",
    }
    assert contract["privacy_contract_record_schema"] == {
        "manifest_contains_private_paths": True,
        "manifest_contains_private_raw_tensors": False,
        "manifest_points_to_private_raw_tensors": True,
        "public_reference_contains_paths": False,
        "public_reference_contains_tensor_descriptors": False,
        "public_reference_contains_hmc_mechanics": False,
    }

    public_text = json.dumps(contract["public_reference_fields"], sort_keys=True)
    for forbidden in (
        "manifest_path",
        "archive_dir",
        "sample_path",
        "samples",
        "valid_mask",
        "final_state",
        "trace",
        "target_log_prob",
        "log_accept",
        "step_size",
        "leapfrog",
        "mass",
        "selected_kernel",
        "private_manifest",
    ):
        assert forbidden not in public_text

    assert contract["privacy_contract"] == {
        "public_progress_contains_private_paths": False,
        "public_progress_contains_raw_tensors": False,
        "public_progress_contains_tensor_descriptors": False,
        "public_progress_contains_hmc_mechanics": False,
        "private_manifest_contains_readback_authority": True,
    }
    assert "no posterior convergence claim" in contract["nonclaims"]
    assert "no resume claim" in contract["nonclaims"]
    assert re.fullmatch(r"[0-9a-f]{64}", contract["contract_sha256"])


def test_build_public_checkpoint_reference_contains_only_opaque_id_and_hashes() -> None:
    reference = build_sequential_rhat_checkpoint_public_reference(
        checkpoint_kind="verification_chunk",
        checkpoint_id=_OPAQUE_ID,
        checkpoint_sha256=_HASH,
    )

    assert set(reference) == set(SEQUENTIAL_RHAT_CHECKPOINT_PUBLIC_REFERENCE_FIELDS)
    assert reference["checkpoint_id"] == _OPAQUE_ID
    assert reference["checkpoint_sha256"] == _HASH
    assert reference["private_paths_publicized"] is False
    assert reference["public_summary_contains_paths"] is False
    assert reference["public_summary_contains_raw_values"] is False
    assert reference["public_summary_contains_tensor_descriptors"] is False
    assert reference["public_summary_contains_kernel_payload"] is False
    assert "no posterior convergence claim" in reference["nonclaims"]

    text = json.dumps(reference, sort_keys=True)
    for forbidden in (
        "/",
        "\\",
        "results/cross_country_multi_asset",
        "private_manifest",
        "manifest_path",
        "sample_path",
        "samples",
        "valid_mask",
        "final_state",
        "trace",
        "target_log_prob",
        "log_accept",
        "step_size",
        "num_leapfrog_steps",
        "mass",
        "selected_kernel",
        "chunk_0003",
        "run_20260630",
        ".tftensor",
    ):
        assert forbidden not in text


@pytest.mark.parametrize(
    ("field", "value", "message"),
    (
        ("checkpoint_id", "results/cross_country_multi_asset/chunk_0001", "opaque"),
        ("checkpoint_id", "../private/chunk_0001", "opaque"),
        ("checkpoint_id", "srhat-v1-run_20260630-chunk_0003", "opaque"),
        ("checkpoint_sha256", "not-a-sha", "SHA-256"),
        ("private_paths_publicized", True, "must be false"),
    ),
)
def test_public_checkpoint_reference_rejects_path_hash_and_flag_leakage(
    field: str,
    value: object,
    message: str,
) -> None:
    reference = dict(
        build_sequential_rhat_checkpoint_public_reference(
            checkpoint_kind="verification_chunk",
            checkpoint_id=_OPAQUE_ID,
            checkpoint_sha256=_HASH,
        )
    )
    reference[field] = value

    with pytest.raises(ValueError, match=message):
        assert_sequential_rhat_checkpoint_public_reference_safe(reference)


def test_public_checkpoint_reference_rejects_extra_private_mechanics_keys() -> None:
    reference = dict(
        build_sequential_rhat_checkpoint_public_reference(
            checkpoint_kind="pre_verification_handoff",
            checkpoint_id=_OPAQUE_ID,
            checkpoint_sha256=_HASH,
        )
    )
    reference["manifest_path"] = "private/checkpoints/handoff.json"

    with pytest.raises(ValueError, match="fields mismatch"):
        assert_sequential_rhat_checkpoint_public_reference_safe(reference)


def test_sequential_rhat_checkpoint_contract_public_exports() -> None:
    assert (
        bayesfilter.sequential_rhat_verification_checkpoint_contract
        is sequential_rhat_verification_checkpoint_contract
    )
    assert (
        bayesfilter.build_sequential_rhat_checkpoint_public_reference
        is build_sequential_rhat_checkpoint_public_reference
    )
    assert (
        bayesfilter.assert_sequential_rhat_checkpoint_public_reference_safe
        is assert_sequential_rhat_checkpoint_public_reference_safe
    )
    assert "sequential_rhat_verification_checkpoint_contract" in bayesfilter.__all__
    assert "build_sequential_rhat_checkpoint_public_reference" in bayesfilter.__all__
    assert (
        "assert_sequential_rhat_checkpoint_public_reference_safe"
        in bayesfilter.__all__
    )
