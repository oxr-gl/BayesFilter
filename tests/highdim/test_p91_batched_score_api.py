from __future__ import annotations

import pytest
import tensorflow as tf

import bayesfilter
import bayesfilter.highdim as highdim


DTYPE = tf.float64


def _setup_identity(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "target_id": "zhao_cui_sir_austria_d18",
        "time_index": 1,
        "parameter_dim": 18,
        "state_dim": 18,
        "physical_ordering": (
            "theta",
            "current_state",
            "next_state",
        ),
        "basis_family": "lagrangep",
        "basis_order": 3,
        "basis_elements": 8,
        "tt_rank_tuple": (3, 3, 3),
        "sample_count": 256,
        "seed": 9101,
        "transport_branch_hash": "transport_hash_fixture",
        "coordinate_frame_hash": "coordinate_frame_hash_fixture",
        "transition_log_density_id": "transition_fixture",
        "likelihood_log_density_id": "likelihood_fixture",
        "prior_log_density_id": "prior_fixture",
        "tolerance_version": "p91.batched_score_api.fixture.v1",
    }
    payload.update(overrides)
    return payload


def _quadratic_value(center: tf.Tensor, shift: float = 0.0):
    def value_fn(theta: tf.Tensor) -> tf.Tensor:
        residual = tf.convert_to_tensor(theta, dtype=DTYPE) - center
        return -0.5 * tf.reduce_sum(tf.square(residual)) + tf.constant(shift, dtype=DTYPE)

    return value_fn


def test_p91_batched_score_api_exports_are_subpackage_only() -> None:
    symbols = {"HighDimBatchedScoreAPIResult", "evaluate_batched_highdim_score_api"}

    assert symbols.issubset(set(highdim.__all__))
    assert all(hasattr(highdim, name) for name in symbols)
    assert symbols.isdisjoint(set(bayesfilter.__all__))
    assert all(not hasattr(bayesfilter, name) for name in symbols)


def test_p91_batched_score_api_shared_identity_matches_looped_single() -> None:
    theta = tf.constant([1.0, -2.0], dtype=DTYPE)
    centers = (
        tf.constant([0.25, -0.75], dtype=DTYPE),
        tf.constant([-0.50, -1.50], dtype=DTYPE),
    )
    value_fns = (
        _quadratic_value(centers[0], shift=0.1),
        _quadratic_value(centers[1], shift=-0.2),
    )
    setup_identity = _setup_identity()
    looped = [
        highdim.evaluate_highdim_score_api(
            target_id="p91_batched_score_api_fixture",
            evidence_class="lower_rung",
            route_label="hmc_compatible_deterministic_filtering",
            parameterization="theta=(theta_0, theta_1)",
            theta=theta,
            value_fn=value_fn,
            diagnostics={"fixture": "p91_batched_looped_single"},
            setup_identity=setup_identity,
        )
        for value_fn in value_fns
    ]

    batched = highdim.evaluate_batched_highdim_score_api(
        target_id="p91_batched_score_api_fixture",
        evidence_class="lower_rung",
        route_label="hmc_compatible_deterministic_filtering",
        parameterization="theta=(theta_0, theta_1)",
        theta=theta,
        value_fns=value_fns,
        diagnostics={"fixture": "p91_batched_shared_identity"},
        shared_setup_identity=setup_identity,
    )

    assert isinstance(batched, highdim.HighDimBatchedScoreAPIResult)
    assert batched.status is highdim.HighDimStatus.OK
    assert batched.log_likelihoods.shape == (2,)
    assert batched.score.shape == (2, 2)
    assert batched.theta.dtype == DTYPE
    assert batched.score.dtype == DTYPE
    tf.debugging.assert_near(
        batched.log_likelihoods,
        tf.stack([result.log_likelihood for result in looped]),
    )
    tf.debugging.assert_near(batched.score, tf.stack([result.score for result in looped]))
    assert batched.diagnostics["setup_identity_channel"] == "diagnostics_and_branch_manifest"
    assert batched.diagnostics["batch_identity_mode"] == "shared_setup_identity"
    assert batched.diagnostics["batch_size"] == 2
    assert batched.diagnostics["per_item_branch_hashes"] == tuple(
        identity.hash.value for identity in batched.branch_identities
    )
    assert all(
        identity.manifest.payload["setup_identity"] == setup_identity
        for identity in batched.branch_identities
    )


def test_p91_batched_score_api_per_item_identity_metadata() -> None:
    theta = tf.constant([1.0, -2.0], dtype=DTYPE)
    value_fns = (
        _quadratic_value(tf.constant([0.25, -0.75], dtype=DTYPE)),
        _quadratic_value(tf.constant([-0.50, -1.50], dtype=DTYPE)),
    )
    identities = (
        _setup_identity(seed=9101),
        _setup_identity(seed=9102),
    )

    result = highdim.evaluate_batched_highdim_score_api(
        target_id="p91_batched_score_api_fixture",
        evidence_class="lower_rung",
        route_label="hmc_compatible_deterministic_filtering",
        parameterization="theta=(theta_0, theta_1)",
        theta=theta,
        value_fns=value_fns,
        per_item_setup_identities=identities,
    )

    assert result.diagnostics["batch_identity_mode"] == "per_item_setup_identity"
    assert len(set(result.diagnostics["per_item_branch_hashes"])) == 2
    assert result.branch_identities[0].manifest.payload["setup_identity"]["seed"] == 9101
    assert result.branch_identities[1].manifest.payload["setup_identity"]["seed"] == 9102


def test_p91_batched_score_api_rejects_ambiguous_or_missing_identity() -> None:
    theta = tf.constant([1.0, -2.0], dtype=DTYPE)
    value_fns = (_quadratic_value(tf.constant([0.25, -0.75], dtype=DTYPE)),)

    with pytest.raises(ValueError, match="requires setup identity metadata"):
        highdim.evaluate_batched_highdim_score_api(
            target_id="missing_identity",
            evidence_class="lower_rung",
            route_label="hmc_compatible_deterministic_filtering",
            parameterization="theta",
            theta=theta,
            value_fns=value_fns,
        )

    with pytest.raises(ValueError, match="not both"):
        highdim.evaluate_batched_highdim_score_api(
            target_id="ambiguous_identity",
            evidence_class="lower_rung",
            route_label="hmc_compatible_deterministic_filtering",
            parameterization="theta",
            theta=theta,
            value_fns=value_fns,
            shared_setup_identity=_setup_identity(),
            per_item_setup_identities=(_setup_identity(),),
        )

    with pytest.raises(ValueError, match="must match value_fns length"):
        highdim.evaluate_batched_highdim_score_api(
            target_id="identity_length_mismatch",
            evidence_class="lower_rung",
            route_label="hmc_compatible_deterministic_filtering",
            parameterization="theta",
            theta=theta,
            value_fns=value_fns,
            per_item_setup_identities=(_setup_identity(), _setup_identity(seed=9102)),
        )


def test_p91_batched_score_api_rejects_bad_shapes_and_disconnected_values() -> None:
    with pytest.raises(ValueError, match="INVALID_SHAPE"):
        highdim.evaluate_batched_highdim_score_api(
            target_id="bad_theta",
            evidence_class="lower_rung",
            route_label="hmc_compatible_deterministic_filtering",
            parameterization="theta matrix",
            theta=tf.zeros([1, 2], dtype=DTYPE),
            value_fns=(_quadratic_value(tf.constant([0.25, -0.75], dtype=DTYPE)),),
            shared_setup_identity=_setup_identity(),
        )

    with pytest.raises(ValueError, match="INVALID_SHAPE"):
        highdim.evaluate_batched_highdim_score_api(
            target_id="bad_value_shape",
            evidence_class="lower_rung",
            route_label="hmc_compatible_deterministic_filtering",
            parameterization="theta",
            theta=tf.zeros([2], dtype=DTYPE),
            value_fns=(lambda current_theta: current_theta,),
            shared_setup_identity=_setup_identity(),
        )

    with pytest.raises(ValueError, match="score gradient is None"):
        highdim.evaluate_batched_highdim_score_api(
            target_id="disconnected",
            evidence_class="lower_rung",
            route_label="hmc_compatible_deterministic_filtering",
            parameterization="theta",
            theta=tf.zeros([2], dtype=DTYPE),
            value_fns=(lambda _current_theta: tf.constant(1.0, dtype=DTYPE),),
            shared_setup_identity=_setup_identity(),
        )
