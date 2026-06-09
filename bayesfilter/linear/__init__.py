"""Linear Gaussian filtering contracts and backends."""

from __future__ import annotations

from importlib import import_module

__all__ = [
    "LinearGaussianStateSpace",
    "LinearGaussianStateSpaceDerivatives",
    "TFQRLinearValueBackend",
    "TFQRLinearDerivativeBackend",
    "TFLinearValueBackend",
    "TFSVDLinearValueBackend",
    "tf_qr_linear_gaussian_log_likelihood",
    "tf_qr_linear_gaussian_score_hessian",
    "tf_qr_sqrt_kalman_filter",
    "tf_qr_sqrt_kalman_log_likelihood",
    "tf_qr_sqrt_kalman_score_hessian",
    "tf_qr_sqrt_masked_kalman_filter",
    "tf_qr_sqrt_masked_kalman_log_likelihood",
    "tf_qr_sqrt_masked_kalman_score_hessian",
    "tf_kalman_filter",
    "tf_kalman_log_likelihood",
    "tf_linear_gaussian_log_likelihood",
    "tf_masked_kalman_filter",
    "tf_masked_kalman_log_likelihood",
    "tf_svd_kalman_log_likelihood",
    "tf_svd_linear_gaussian_score_hessian",
    "tf_svd_linear_gaussian_log_likelihood",
    "tf_svd_masked_kalman_log_likelihood",
    "cholesky_factor",
    "cholesky_factor_derivatives",
    "factor_covariance_derivatives",
    "factor_derivative_reconstruction_errors",
    "factor_solve",
    "lower_factor_from_horizontal_stack",
    "qr_factor_derivatives",
    "qr_factor_full_derivatives",
    "qr_factor_second_derivatives",
    "qr_positive",
    "stack_covariance_derivatives",
    "stack_qr_lower_factor_derivatives",
    "symmetrize",
    "trace_factor_solve",
    "TFLinearGaussianStateSpace",
    "TFLinearGaussianStateSpaceDerivatives",
]

_EXPORT_MODULES = {
    "LinearGaussianStateSpace": "bayesfilter.linear.types",
    "LinearGaussianStateSpaceDerivatives": "bayesfilter.linear.types",
    "TFQRLinearValueBackend": "bayesfilter.linear.kalman_qr_tf",
    "TFQRLinearDerivativeBackend": "bayesfilter.linear.kalman_qr_derivatives_tf",
    "TFLinearValueBackend": "bayesfilter.linear.kalman_tf",
    "TFSVDLinearValueBackend": "bayesfilter.linear.kalman_svd_tf",
    "tf_qr_linear_gaussian_log_likelihood": "bayesfilter.linear.kalman_qr_tf",
    "tf_qr_linear_gaussian_score_hessian": (
        "bayesfilter.linear.kalman_qr_derivatives_tf"
    ),
    "tf_qr_sqrt_kalman_filter": "bayesfilter.linear.kalman_qr_tf",
    "tf_qr_sqrt_kalman_log_likelihood": "bayesfilter.linear.kalman_qr_tf",
    "tf_qr_sqrt_kalman_score_hessian": (
        "bayesfilter.linear.kalman_qr_derivatives_tf"
    ),
    "tf_qr_sqrt_masked_kalman_filter": "bayesfilter.linear.kalman_qr_tf",
    "tf_qr_sqrt_masked_kalman_log_likelihood": (
        "bayesfilter.linear.kalman_qr_tf"
    ),
    "tf_qr_sqrt_masked_kalman_score_hessian": (
        "bayesfilter.linear.kalman_qr_derivatives_tf"
    ),
    "tf_kalman_filter": "bayesfilter.linear.kalman_tf",
    "tf_kalman_log_likelihood": "bayesfilter.linear.kalman_tf",
    "tf_linear_gaussian_log_likelihood": "bayesfilter.linear.kalman_tf",
    "tf_masked_kalman_filter": "bayesfilter.linear.kalman_tf",
    "tf_masked_kalman_log_likelihood": "bayesfilter.linear.kalman_tf",
    "tf_svd_kalman_log_likelihood": "bayesfilter.linear.kalman_svd_tf",
    "tf_svd_linear_gaussian_score_hessian": (
        "bayesfilter.linear.kalman_svd_derivatives_tf"
    ),
    "tf_svd_linear_gaussian_log_likelihood": "bayesfilter.linear.kalman_svd_tf",
    "tf_svd_masked_kalman_log_likelihood": "bayesfilter.linear.kalman_svd_tf",
    "cholesky_factor": "bayesfilter.linear.qr_factor_tf",
    "cholesky_factor_derivatives": "bayesfilter.linear.qr_factor_tf",
    "factor_covariance_derivatives": "bayesfilter.linear.qr_factor_tf",
    "factor_derivative_reconstruction_errors": "bayesfilter.linear.qr_factor_tf",
    "factor_solve": "bayesfilter.linear.qr_factor_tf",
    "lower_factor_from_horizontal_stack": "bayesfilter.linear.qr_factor_tf",
    "qr_factor_derivatives": "bayesfilter.linear.qr_factor_tf",
    "qr_factor_full_derivatives": "bayesfilter.linear.qr_factor_tf",
    "qr_factor_second_derivatives": "bayesfilter.linear.qr_factor_tf",
    "qr_positive": "bayesfilter.linear.qr_factor_tf",
    "stack_covariance_derivatives": "bayesfilter.linear.qr_factor_tf",
    "stack_qr_lower_factor_derivatives": "bayesfilter.linear.qr_factor_tf",
    "symmetrize": "bayesfilter.linear.qr_factor_tf",
    "trace_factor_solve": "bayesfilter.linear.qr_factor_tf",
    "TFLinearGaussianStateSpace": "bayesfilter.linear.types_tf",
    "TFLinearGaussianStateSpaceDerivatives": "bayesfilter.linear.types_tf",
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
