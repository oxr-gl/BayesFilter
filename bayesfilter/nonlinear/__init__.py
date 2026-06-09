"""TensorFlow nonlinear filtering backends and sigma-point rules."""

from __future__ import annotations

from importlib import import_module

__all__ = [
    "CompiledValuePathClassification",
    "CompiledValuePathMode",
    "InvalidCompiledValuePathContract",
    "NonlinearFilterValuePathContract",
    "NonlinearFilterValueStaticShape",
    "TFStructuralFirstDerivatives",
    "TFSmoothEighFactorFirstDerivatives",
    "TFSigmaPointDiagnostics",
    "TFSigmaPointRule",
    "TFSigmaPointValueBackend",
    "find_forbidden_compiled_value_tokens",
    "stable_nonlinear_filter_value_path_signature",
    "tf_svd_sigma_point_filter",
    "tf_svd_sigma_point_log_likelihood",
    "tf_svd_sigma_point_log_likelihood_with_rule",
    "tf_svd_sigma_point_placement",
    "tf_cut4g_sigma_point_rule",
    "tf_svd_cubature_score",
    "tf_svd_cut4_filter",
    "tf_svd_cut4_log_likelihood",
    "tf_svd_cut4_score",
    "tf_unit_sigma_point_rule",
    "tf_svd_sigma_point_score_with_rule",
    "tf_svd_ukf_score",
    "tensorflow_nonlinear_value_path_contract",
]

_EXPORT_MODULES = {
    "CompiledValuePathClassification": "bayesfilter.nonlinear.compiled_value_paths",
    "CompiledValuePathMode": "bayesfilter.nonlinear.compiled_value_paths",
    "InvalidCompiledValuePathContract": "bayesfilter.nonlinear.compiled_value_paths",
    "NonlinearFilterValuePathContract": "bayesfilter.nonlinear.compiled_value_paths",
    "NonlinearFilterValueStaticShape": "bayesfilter.nonlinear.compiled_value_paths",
    "TFStructuralFirstDerivatives": (
        "bayesfilter.nonlinear.svd_sigma_point_derivatives_tf"
    ),
    "TFSmoothEighFactorFirstDerivatives": (
        "bayesfilter.nonlinear.svd_sigma_point_derivatives_tf"
    ),
    "TFSigmaPointDiagnostics": "bayesfilter.nonlinear.sigma_points_tf",
    "TFSigmaPointRule": "bayesfilter.nonlinear.sigma_points_tf",
    "TFSigmaPointValueBackend": "bayesfilter.nonlinear.sigma_points_tf",
    "find_forbidden_compiled_value_tokens": "bayesfilter.nonlinear.compiled_value_paths",
    "stable_nonlinear_filter_value_path_signature": (
        "bayesfilter.nonlinear.compiled_value_paths"
    ),
    "tf_svd_sigma_point_filter": "bayesfilter.nonlinear.sigma_points_tf",
    "tf_svd_sigma_point_log_likelihood": "bayesfilter.nonlinear.sigma_points_tf",
    "tf_svd_sigma_point_log_likelihood_with_rule": (
        "bayesfilter.nonlinear.sigma_points_tf"
    ),
    "tf_svd_sigma_point_placement": "bayesfilter.nonlinear.sigma_points_tf",
    "tf_cut4g_sigma_point_rule": "bayesfilter.nonlinear.cut_tf",
    "tf_svd_cubature_score": (
        "bayesfilter.nonlinear.svd_sigma_point_derivatives_tf"
    ),
    "tf_svd_cut4_filter": "bayesfilter.nonlinear.svd_cut_tf",
    "tf_svd_cut4_log_likelihood": "bayesfilter.nonlinear.svd_cut_tf",
    "tf_svd_cut4_score": "bayesfilter.nonlinear.svd_sigma_point_derivatives_tf",
    "tf_unit_sigma_point_rule": "bayesfilter.nonlinear.sigma_points_tf",
    "tf_svd_sigma_point_score_with_rule": (
        "bayesfilter.nonlinear.svd_sigma_point_derivatives_tf"
    ),
    "tf_svd_ukf_score": "bayesfilter.nonlinear.svd_sigma_point_derivatives_tf",
    "tensorflow_nonlinear_value_path_contract": (
        "bayesfilter.nonlinear.compiled_value_paths"
    ),
}


def __getattr__(name: str):
    try:
        module_name = _EXPORT_MODULES[name]
    except KeyError as exc:
        raise AttributeError(
            f"module {__name__!r} has no attribute {name!r}"
        ) from exc
    value = getattr(import_module(module_name), name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(__all__))
