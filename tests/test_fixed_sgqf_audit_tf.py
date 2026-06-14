import numpy as np
import tensorflow as tf

from bayesfilter.nonlinear.fixed_sgqf_tf import (
    TFFixedSGQFBranchConfig,
    TFFixedSGQFCloud,
    tf_fixed_sgqf_branch_identity,
    tf_fixed_sgqf_cloud,
    tf_fixed_sgqf_filter,
    tf_fixed_sgqf_p47_one_step_oracle,
)


def test_fixed_sgqf_branch_manifest_contains_core_p47_contract_fields() -> None:
    cloud = tf_fixed_sgqf_cloud(dim=3, sparse_level=2)
    branch = TFFixedSGQFBranchConfig(
        observation_preprocessing="identity",
        initial_condition_policy="theta_defined_initial_law",
        failure_record_policy="time_stage_reason_diagnostics",
        predictive_epsilon=1e-10,
        innovation_epsilon=1e-10,
    )
    manifest = branch.branch_manifest(cloud)
    payload = manifest.payload
    cloud_payload = payload["cloud"]

    assert payload["observation_preprocessing"] == "identity"
    assert payload["initial_condition_policy"] == "theta_defined_initial_law"
    assert payload["failure_record_policy"] == "time_stage_reason_diagnostics"
    assert payload["factor_branch"] == "chol_lower_positive_diag"
    assert payload["additive_noise_policy"] == "analytic_q_r_no_state_augmentation"
    assert payload["veto_policy"] == "symmetrize_then_veto"
    np.testing.assert_allclose(payload["predictive_epsilon"], 1e-10, atol=0.0)
    np.testing.assert_allclose(payload["innovation_epsilon"], 1e-10, atol=0.0)

    assert cloud_payload["merge_tolerance_policy"] == "scaled_by_max_1_supnorm"
    assert cloud_payload["node_ordering"] == "lexicographic"
    assert cloud_payload["stored_representation"] == "points_and_weights"
    assert cloud_payload["rule_family"] == "standard_normal_ghq"
    assert cloud_payload["active_multi_indices"] == ((1, 1, 1), (1, 1, 2), (1, 2, 1), (2, 1, 1))
    assert cloud_payload["combination_coefficients"] == (-2, 1, 1, 1)
    np.testing.assert_allclose(cloud_payload["weight_total"], 1.0, atol=1e-14)
    assert cloud_payload["negative_weight_count"] == 0


def test_fixed_sgqf_branch_identity_changes_when_branch_policy_changes() -> None:
    cloud = tf_fixed_sgqf_cloud(dim=1, sparse_level=2)
    base = tf_fixed_sgqf_branch_identity(cloud)
    changed_initial_policy = tf_fixed_sgqf_branch_identity(
        cloud,
        initial_condition_policy="fixed_fixture_initial_law",
    )
    changed_failure_policy = tf_fixed_sgqf_branch_identity(
        cloud,
        failure_record_policy="time_stage_reason_only",
    )

    assert base.hash != changed_initial_policy.hash
    assert base.hash != changed_failure_policy.hash


def test_fixed_sgqf_filter_records_cloud_weight_sum_failure_explicitly() -> None:
    oracle, cloud = tf_fixed_sgqf_p47_one_step_oracle()
    bad_cloud = TFFixedSGQFCloud(
        dim=cloud.dim,
        sparse_level=cloud.sparse_level,
        points=cloud.points,
        weights=cloud.weights * 2.0,
        active_multi_indices=cloud.active_multi_indices,
        combination_coefficients=cloud.combination_coefficients,
        merge_tolerance=cloud.merge_tolerance,
        zero_weight_tolerance=cloud.zero_weight_tolerance,
        node_ordering=cloud.node_ordering,
        stored_representation=cloud.stored_representation,
        rule_family=cloud.rule_family,
        merge_tolerance_policy=cloud.merge_tolerance_policy,
    )
    result = tf_fixed_sgqf_filter(oracle.observation, oracle.model(), cloud=bad_cloud, return_filtered=True)

    assert result.failure is not None
    assert result.failure.stage == "cloud"
    assert result.failure.reason == "weight_sum_failure"
    assert result.step_results[0].accepted is False
    assert result.diagnostics["branch_hash"] == result.branch_identity.hash.value


def test_fixed_sgqf_innovation_failure_records_stage_reason_and_branch_hash() -> None:
    cloud = tf_fixed_sgqf_cloud(dim=1, sparse_level=2)
    model = tf_fixed_sgqf_p47_one_step_oracle()[0].model()
    blocked_model = type(model)(
        initial_mean=model.initial_mean,
        initial_covariance=model.initial_covariance,
        process_covariance=model.process_covariance,
        observation_covariance=tf.constant([[-10.0]], dtype=tf.float64),
        transition_fn=model.transition_fn,
        observation_fn=model.observation_fn,
        name="innovation_failure_audit_fixture",
    )
    result = tf_fixed_sgqf_filter(
        tf.constant([[2.0]], dtype=tf.float64),
        blocked_model,
        cloud=cloud,
        branch_config=TFFixedSGQFBranchConfig(predictive_epsilon=1e-10, innovation_epsilon=1e-10),
        return_filtered=True,
    )

    assert result.failure is not None
    assert result.failure.stage == "innovation_covariance"
    assert result.failure.reason in {"positive_definiteness_veto", "cholesky_failure"}
    assert result.step_results[0].diagnostics["branch_hash"] == result.branch_identity.hash.value
    assert "innovation_covariance_diagnostics" in result.step_results[0].diagnostics
