"""TensorFlow eigen/SVD helpers for PSD covariance solves."""

from __future__ import annotations

import tensorflow as tf


def symmetrize(matrix: tf.Tensor) -> tf.Tensor:
    """Return the symmetric part of a covariance-like matrix."""

    matrix = tf.convert_to_tensor(matrix, dtype=tf.float64)
    return 0.5 * (matrix + tf.linalg.matrix_transpose(matrix))


def psd_eigh(
    covariance: tf.Tensor,
    singular_floor: tf.Tensor | float,
) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor]:
    """Return PSD eigensystem and implemented covariance under eigenvalue floor."""

    covariance = symmetrize(covariance)
    floor = tf.cast(singular_floor, tf.float64)
    eigenvalues, eigenvectors = tf.linalg.eigh(covariance)
    floored_eigenvalues = tf.maximum(eigenvalues, floor)
    implemented_covariance = (
        eigenvectors
        @ tf.linalg.diag(floored_eigenvalues)
        @ tf.linalg.matrix_transpose(eigenvectors)
    )
    projection_residual = tf.linalg.norm(implemented_covariance - covariance)
    return (
        eigenvalues,
        floored_eigenvalues,
        eigenvectors,
        implemented_covariance,
        projection_residual,
    )


def psd_eigh_graph_status(
    covariance: tf.Tensor,
    singular_floor: tf.Tensor | float,
) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor]:
    """Return a PSD eigensystem after guarding nonfinite eigensolver inputs.

    This is a graph-status helper for callers that must return tensor
    diagnostics instead of letting ``tf.linalg.eigh`` abort on invalid
    covariance entries.  When the covariance is nonfinite, the eigensolver sees
    a benign identity covariance only so graph execution can complete; callers
    must treat the returned score/value payload as blocked diagnostics.
    """

    covariance = symmetrize(covariance)
    floor = tf.cast(singular_floor, tf.float64)
    covariance_is_finite = tf.reduce_all(tf.math.is_finite(covariance))
    floor_is_finite = tf.math.is_finite(floor)
    valid_eigensolver_input = tf.logical_and(covariance_is_finite, floor_is_finite)
    dimension = tf.shape(covariance)[0]
    safe_floor = tf.cond(
        floor_is_finite,
        lambda: floor,
        lambda: tf.constant(1.0, dtype=tf.float64),
    )
    benign_scale = tf.maximum(tf.abs(safe_floor), tf.constant(1.0, dtype=tf.float64))
    benign_covariance = benign_scale * tf.eye(dimension, dtype=tf.float64)
    safe_covariance = tf.cond(
        valid_eigensolver_input,
        lambda: covariance,
        lambda: benign_covariance,
    )
    eigenvalues, eigenvectors = tf.linalg.eigh(safe_covariance)
    floored_eigenvalues = tf.maximum(eigenvalues, safe_floor)
    implemented_covariance = (
        eigenvectors
        @ tf.linalg.diag(floored_eigenvalues)
        @ tf.linalg.matrix_transpose(eigenvectors)
    )
    residual = tf.cond(
        valid_eigensolver_input,
        lambda: tf.linalg.norm(implemented_covariance - covariance),
        lambda: tf.constant(float("nan"), dtype=tf.float64),
    )
    return (
        eigenvalues,
        floored_eigenvalues,
        eigenvectors,
        implemented_covariance,
        residual,
        tf.logical_not(valid_eigensolver_input),
    )


def eigh_solve(
    eigenvectors: tf.Tensor,
    eigenvalues: tf.Tensor,
    rhs: tf.Tensor,
) -> tf.Tensor:
    """Solve with an eigensystem whose eigenvalues are already floored."""

    eigenvectors = tf.convert_to_tensor(eigenvectors, dtype=tf.float64)
    eigenvalues = tf.convert_to_tensor(eigenvalues, dtype=tf.float64)
    rhs = tf.convert_to_tensor(rhs, dtype=tf.float64)
    if rhs.shape.rank == 1:
        projected = tf.linalg.matvec(tf.linalg.matrix_transpose(eigenvectors), rhs)
        scaled = projected / eigenvalues
        return tf.linalg.matvec(eigenvectors, scaled)
    projected = tf.linalg.matrix_transpose(eigenvectors) @ rhs
    scaled = projected / eigenvalues[:, tf.newaxis]
    return eigenvectors @ scaled


def eigh_logdet(eigenvalues: tf.Tensor) -> tf.Tensor:
    """Return log determinant from already-floored eigenvalues."""

    return tf.reduce_sum(tf.math.log(tf.convert_to_tensor(eigenvalues, dtype=tf.float64)))


def floor_count(eigenvalues: tf.Tensor, singular_floor: tf.Tensor | float) -> tf.Tensor:
    """Count eigenvalues at or below the floor branch."""

    floor = tf.cast(singular_floor, tf.float64)
    return tf.reduce_sum(tf.cast(eigenvalues <= floor, tf.int32))
