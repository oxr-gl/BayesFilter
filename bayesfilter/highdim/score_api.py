"""Experimental score API contracts for P47 evidence-class readiness."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Callable, Mapping, Sequence

import tensorflow as tf

from bayesfilter.highdim.diagnostics import HighDimStatus, freeze_mapping
from bayesfilter.highdim.fixed_branch import BranchHash, BranchIdentity, BranchManifest


_ALLOWED_EVIDENCE_CLASSES = frozenset({"lower_rung", "production"})
_ALLOWED_HMC_STATUSES = frozenset(
    {
        "blocked_tier2_tier3_not_run",
        "blocked_missing_score_evidence",
        "blocked_missing_production_filtering_token",
        "not_requested",
    }
)


@dataclass(frozen=True)
class ExperimentalScoreAPIResult:
    """Frozen result for a small deterministic score API evaluation."""

    target_id: str
    evidence_class: str
    m1_route_label: str
    parameterization: str
    theta: tf.Tensor
    log_likelihood: tf.Tensor
    score: tf.Tensor
    branch_identity: BranchIdentity
    status: HighDimStatus
    diagnostics: Mapping[str, object]

    def __post_init__(self) -> None:
        target_id = _require_text("target_id", self.target_id)
        evidence_class = _require_text("evidence_class", self.evidence_class)
        if evidence_class not in _ALLOWED_EVIDENCE_CLASSES:
            raise ValueError("evidence_class must be lower_rung or production")
        m1_route_label = _require_text("m1_route_label", self.m1_route_label)
        if m1_route_label not in {
            "adaptive route candidate",
            "documented-deviation fixed-design substitute",
        }:
            raise ValueError("invalid M1 route label")
        parameterization = _require_text("parameterization", self.parameterization)
        theta = tf.convert_to_tensor(self.theta, dtype=tf.float64)
        value = tf.convert_to_tensor(self.log_likelihood, dtype=tf.float64)
        score = tf.convert_to_tensor(self.score, dtype=tf.float64)
        if theta.shape.rank != 1 or score.shape != theta.shape or value.shape.rank != 0:
            raise ValueError(f"score API result: {HighDimStatus.INVALID_SHAPE.value}")
        if not bool(
            tf.reduce_all(tf.math.is_finite(theta)).numpy()
            and tf.math.is_finite(value).numpy()
            and tf.reduce_all(tf.math.is_finite(score)).numpy()
        ):
            raise ValueError(f"score API result: {HighDimStatus.NONFINITE_VALUE.value}")
        if not isinstance(self.branch_identity, BranchIdentity):
            raise TypeError("branch_identity must be BranchIdentity")
        if not isinstance(self.status, HighDimStatus):
            raise TypeError("status must be HighDimStatus")
        object.__setattr__(self, "target_id", target_id)
        object.__setattr__(self, "evidence_class", evidence_class)
        object.__setattr__(self, "m1_route_label", m1_route_label)
        object.__setattr__(self, "parameterization", parameterization)
        object.__setattr__(self, "theta", theta)
        object.__setattr__(self, "log_likelihood", value)
        object.__setattr__(self, "score", score)
        object.__setattr__(self, "diagnostics", freeze_mapping(self.diagnostics))


@dataclass(frozen=True)
class ScoreReadinessRow:
    """Readiness-table row with explicit evidence-class boundaries."""

    target_id: str
    evidence_class: str
    upstream_tokens: tuple[str, ...]
    p42_tiers_passed: tuple[str, ...]
    api_status: str
    hmc_status: str
    promoted_claim: str
    forbidden_claims: tuple[str, ...]
    m1_route_label: str

    def __post_init__(self) -> None:
        target_id = _require_text("target_id", self.target_id)
        evidence_class = _require_text("evidence_class", self.evidence_class)
        if evidence_class not in _ALLOWED_EVIDENCE_CLASSES:
            raise ValueError("evidence_class must be lower_rung or production")
        api_status = _require_text("api_status", self.api_status)
        hmc_status = _require_text("hmc_status", self.hmc_status)
        if hmc_status not in _ALLOWED_HMC_STATUSES:
            raise ValueError("unknown HMC status")
        m1_route_label = _require_text("m1_route_label", self.m1_route_label)
        if m1_route_label not in {
            "adaptive route candidate",
            "documented-deviation fixed-design substitute",
        }:
            raise ValueError("invalid M1 route label")
        upstream_tokens = _text_tuple("upstream_tokens", self.upstream_tokens)
        p42_tiers = tuple(str(value).strip() for value in self.p42_tiers_passed)
        forbidden = _text_tuple("forbidden_claims", self.forbidden_claims)
        claim = _require_text("promoted_claim", self.promoted_claim)
        if evidence_class == "production" and "production" not in target_id:
            raise ValueError("production rows must use production target ids")
        if "production" in claim.lower() and evidence_class != "production":
            raise ValueError("lower-rung rows cannot promote production claims")
        claim_lower = claim.lower()
        if "hmc readiness" in claim_lower and "no " not in claim_lower and "not " not in claim_lower:
            raise ValueError("HMC readiness cannot be promoted by this P47-M6 table")
        if api_status.startswith("passed") and "TIER_1_LOCAL_VALUE_AND_DIRECTIONAL_SCORE" not in p42_tiers:
            raise ValueError("passed API score rows require P42 Tier 1 evidence")
        if api_status.startswith("blocked") and p42_tiers:
            raise ValueError("blocked API rows must not list passed P42 tiers")
        object.__setattr__(self, "target_id", target_id)
        object.__setattr__(self, "evidence_class", evidence_class)
        object.__setattr__(self, "upstream_tokens", upstream_tokens)
        object.__setattr__(self, "p42_tiers_passed", p42_tiers)
        object.__setattr__(self, "api_status", api_status)
        object.__setattr__(self, "hmc_status", hmc_status)
        object.__setattr__(self, "promoted_claim", claim)
        object.__setattr__(self, "forbidden_claims", forbidden)
        object.__setattr__(self, "m1_route_label", m1_route_label)

    def manifest_payload(self) -> Mapping[str, object]:
        return {
            "target_id": self.target_id,
            "evidence_class": self.evidence_class,
            "upstream_tokens": self.upstream_tokens,
            "p42_tiers_passed": self.p42_tiers_passed,
            "api_status": self.api_status,
            "hmc_status": self.hmc_status,
            "promoted_claim": self.promoted_claim,
            "forbidden_claims": self.forbidden_claims,
            "m1_route_label": self.m1_route_label,
        }


@dataclass(frozen=True)
class ScoreReadinessManifest:
    """P47-M6 readiness manifest separating API and HMC evidence classes."""

    phase: str
    rows: tuple[ScoreReadinessRow, ...]
    pass_token: str
    nonclaims: tuple[str, ...]

    def __post_init__(self) -> None:
        phase = _require_text("phase", self.phase)
        if phase != "P47-M6":
            raise ValueError("phase must be P47-M6")
        rows = tuple(self.rows)
        if not rows:
            raise ValueError("rows must be nonempty")
        if any(not isinstance(row, ScoreReadinessRow) for row in rows):
            raise TypeError("rows must contain ScoreReadinessRow")
        pass_token = _require_text("pass_token", self.pass_token)
        if pass_token != "PASS_P47_M6_SCORE_HMC_READINESS":
            raise ValueError("unexpected P47-M6 pass token")
        nonclaims = _text_tuple("nonclaims", self.nonclaims)
        text = " ".join(nonclaims).lower()
        for required in (
            "no production hmc readiness",
            "no production score api",
            "lower-rung rows are not production",
        ):
            if required not in text:
                raise ValueError(f"missing nonclaim: {required}")
        object.__setattr__(self, "phase", phase)
        object.__setattr__(self, "rows", rows)
        object.__setattr__(self, "pass_token", pass_token)
        object.__setattr__(self, "nonclaims", nonclaims)

    def manifest_payload(self) -> Mapping[str, object]:
        return {
            "phase": self.phase,
            "pass_token": self.pass_token,
            "rows": tuple(row.manifest_payload() for row in self.rows),
            "nonclaims": self.nonclaims,
        }


def evaluate_experimental_score_api(
    target_id: str,
    evidence_class: str,
    m1_route_label: str,
    parameterization: str,
    theta: tf.Tensor,
    value_fn: Callable[[tf.Tensor], tf.Tensor],
    diagnostics: Mapping[str, object] | None = None,
) -> ExperimentalScoreAPIResult:
    """Evaluate a deterministic value function and package its gradient.

    This is an experimental subpackage helper for fixed, smooth, tiny P42
    Tier-1 fixtures.  It does not create a stable top-level score API or HMC
    target.
    """

    theta_tensor = tf.convert_to_tensor(theta, dtype=tf.float64)
    if theta_tensor.shape.rank != 1:
        raise ValueError(f"theta: {HighDimStatus.INVALID_SHAPE.value}")
    with tf.GradientTape() as tape:
        tape.watch(theta_tensor)
        value = tf.convert_to_tensor(value_fn(theta_tensor), dtype=tf.float64)
    score = tape.gradient(value, theta_tensor)
    if score is None:
        raise ValueError("score gradient is None")
    payload = {
        "target_id": target_id,
        "evidence_class": evidence_class,
        "m1_route_label": m1_route_label,
        "parameterization": parameterization,
        "theta": theta_tensor,
        "log_likelihood": value,
        "score": score,
        "fixed_branch_only": True,
        "experimental_subpackage_only": True,
        "stable_top_level_api": False,
    }
    identity = BranchIdentity(
        manifest=BranchManifest("experimental_score_api_result.v1", payload),
        hash=BranchManifest("experimental_score_api_result.v1", payload).sha256(),
    )
    return ExperimentalScoreAPIResult(
        target_id=target_id,
        evidence_class=evidence_class,
        m1_route_label=m1_route_label,
        parameterization=parameterization,
        theta=theta_tensor,
        log_likelihood=value,
        score=score,
        branch_identity=identity,
        status=HighDimStatus.OK,
        diagnostics={
            **dict(diagnostics or {}),
            "fixed_branch_only": True,
            "experimental_subpackage_only": True,
            "stable_top_level_api": False,
            "hmc_readiness": "not_claimed",
        },
    )


def score_readiness_branch_hash(manifest: ScoreReadinessManifest) -> BranchHash:
    """Return an auditable hash for a score-readiness manifest."""

    return BranchManifest("p47_score_readiness_manifest.v1", manifest.manifest_payload()).sha256()


def _require_text(name: str, value: object) -> str:
    text = str(value).strip()
    if not text:
        raise ValueError(f"{name} must be nonempty")
    return text


def _text_tuple(name: str, values: Sequence[str]) -> tuple[str, ...]:
    normalized = tuple(str(value).strip() for value in values)
    if not normalized or any(not value for value in normalized):
        raise ValueError(f"{name} must contain nonempty strings")
    return normalized
