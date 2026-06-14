from __future__ import annotations

import sys

import pytest

from bayesfilter.inference import (
    InvalidNonlinearSSMContract,
    NonlinearSSMAdapterContract,
    NonlinearSSMStaticShape,
    ObservationSemantics,
    ParameterTransformMetadata,
    RegularizationConvention,
    ValueScoreCapability,
    stable_nonlinear_ssm_program_signature,
    validate_nonlinear_ssm_contract,
)


def _contract(**overrides):
    values = {
        "parameter_names": ("rho", "sigma", "beta"),
        "static_shape": NonlinearSSMStaticShape(
            horizon=3,
            state_dim=2,
            observation_dim=1,
            innovation_dim=1,
            parameter_dim=3,
            constrained_parameter_shape=(3,),
            unconstrained_parameter_shape=(3,),
        ),
        "transform": ParameterTransformMetadata(
            orientation="identity",
            inverse_orientation="identity",
            log_det_jacobian_convention="not_included_in_toy_target",
            transform_source="toy_fixture_identity",
        ),
        "observation_semantics": ObservationSemantics(
            mask_convention="none",
            missingness_convention="none",
            mask_shape=(3, 1),
        ),
        "regularization": RegularizationConvention(
            jitter=0.0,
            covariance_floor=1e-12,
            psd_repair="tf.linalg.eigh_floor",
            symmetrize=True,
            logdet_convention="implemented_regularized_covariance",
            implemented_covariance="post_floor_innovation_covariance",
            repair_role="target",
        ),
        "value_score": ValueScoreCapability(
            value_score_authority="graph_native",
            xla_hmc_ready=True,
            runtime_backend="tensorflow",
            evidence_path="tests/test_nonlinear_ssm_phase1_contract.py",
            target_scope="model_b_toy",
            nonclaims=("toy fixture only",),
        ),
        "prior_term": "explicit_toy_gaussian_prior",
        "likelihood_term": "tf_svd_cut4_score",
        "dtype": "float64",
        "backend": "tensorflow",
        "filter_implementation": "tf_svd_cut4",
        "compile_mode": "xla",
        "trace_policy": "full_trace",
        "return_filtered": False,
        "seed_policy": "stateless_required",
        "map_source": "not_used",
        "mass_matrix_source": "identity_toy",
        "hessian_source": "not_used",
    }
    values.update(overrides)
    return NonlinearSSMAdapterContract(**values)


def test_phase1_contract_accepts_complete_xla_metadata() -> None:
    contract = _contract()

    validated = validate_nonlinear_ssm_contract(contract, require_xla_hmc_ready=True)

    assert validated.xla_hmc_ready is True
    assert validated.regularization.repair_role == "target"
    assert stable_nonlinear_ssm_program_signature(validated) == stable_nonlinear_ssm_program_signature(
        _contract()
    )


def test_phase1_signature_changes_with_static_shape_dtype_backend_and_compile_mode() -> None:
    base = _contract()
    different_shape = _contract(
        static_shape=NonlinearSSMStaticShape(
            horizon=4,
            state_dim=2,
            observation_dim=1,
            innovation_dim=1,
            parameter_dim=3,
            constrained_parameter_shape=(3,),
            unconstrained_parameter_shape=(3,),
        )
    )
    different_dtype = _contract(dtype="float32")
    different_backend = _contract(backend="tensorflow_reference")
    different_compile = _contract(compile_mode="tf_function")

    signatures = {
        stable_nonlinear_ssm_program_signature(base),
        stable_nonlinear_ssm_program_signature(different_shape),
        stable_nonlinear_ssm_program_signature(different_dtype),
        stable_nonlinear_ssm_program_signature(different_backend),
        stable_nonlinear_ssm_program_signature(different_compile),
    }

    assert len(signatures) == 5


def test_phase1_contract_fails_closed_on_missing_regularization_convention() -> None:
    with pytest.raises(InvalidNonlinearSSMContract, match="implemented_covariance"):
        RegularizationConvention(
            jitter=0.0,
            covariance_floor=1e-12,
            psd_repair="tf.linalg.eigh_floor",
            symmetrize=True,
            logdet_convention="implemented_regularized_covariance",
            implemented_covariance="",
            repair_role="target",
        )


def test_phase1_contract_rejects_unknown_regularization_role_and_authority() -> None:
    with pytest.raises(InvalidNonlinearSSMContract, match="unknown repair_role"):
        RegularizationConvention(
            jitter=0.0,
            covariance_floor=1e-12,
            psd_repair="tf.linalg.eigh_floor",
            symmetrize=True,
            logdet_convention="implemented_regularized_covariance",
            implemented_covariance="post_floor_innovation_covariance",
            repair_role="silent_repair",  # type: ignore[arg-type]
        )

    with pytest.raises(ValueError, match="unsupported value/score authority"):
        ValueScoreCapability("unknown", True)  # type: ignore[arg-type]


def test_phase1_unscoped_gradient_tape_fallback_is_not_xla_hmc_ready() -> None:
    contract = _contract(
        value_score=ValueScoreCapability(
            "gradient_tape_fallback",
            False,
            runtime_backend="tensorflow",
            nonclaims=("debug only",),
        )
    )

    with pytest.raises(InvalidNonlinearSSMContract, match="XLA HMC requires"):
        validate_nonlinear_ssm_contract(contract, require_xla_hmc_ready=True)


def test_phase1_reviewed_gradient_tape_exception_must_be_scoped() -> None:
    with pytest.raises(ValueError, match="target_scope"):
        ValueScoreCapability(
            "reviewed_gradient_tape_xla_exception",
            True,
            evidence_path="docs/plans/reviewed-target.md",
            nonclaims=("reviewed exception",),
        )

    capability = ValueScoreCapability(
        "reviewed_gradient_tape_xla_exception",
        True,
        evidence_path="docs/plans/reviewed-target.md",
        target_scope="model_b_toy",
        nonclaims=("reviewed exception",),
    )
    contract = _contract(value_score=capability)

    assert validate_nonlinear_ssm_contract(
        contract,
        require_xla_hmc_ready=True,
    ).xla_hmc_ready


def test_phase1_contract_rejects_process_local_identity_in_signature_fields() -> None:
    with pytest.raises(InvalidNonlinearSSMContract, match="process-local"):
        _contract(filter_implementation=f"adapter object at 0x{id(object()):x}")


def test_phase1_bayesfilter_core_imports_do_not_import_external_model_modules() -> None:
    forbidden = ("dsge_hmc", "MacroFinance", "macrofinance")
    imported = sorted(name for name in sys.modules if name.startswith(forbidden))

    assert imported == []
