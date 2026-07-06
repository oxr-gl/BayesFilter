"""LEDH same-target forward likelihood metadata contracts.

These contracts are intentionally metadata-only.  They do not admit a row,
prove a score route, or change the TensorFlow execution path.  Their job is to
make the observed-data likelihood scalar explicit and keep LEDH proposal/flow
terms from being mislabeled as the leaderboard value.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence


LEDH_TARGET_SCALAR_OBSERVED_DATA_LOG_LIKELIHOOD = (
    "observed_data_log_likelihood_estimator"
)
LEDH_OUTPUT_TENSOR_FIELD_LOG_LIKELIHOOD = "log_likelihood"
LEDH_TARGET_DENSITY_FIELDS = ("transition_log_density", "observation_log_density")
LEDH_PROPOSAL_FLOW_FIELDS = (
    "pre_flow_log_density",
    "forward_log_det",
    "proposal_observation_surface",
)
LEDH_CORRECTION_FORMULA = (
    "transition_log_density + observation_log_density "
    "- pre_flow_log_density + forward_log_det"
)

LGSSM_M3_T50_ROW_ID = "benchmark_lgssm_exact_oracle_m3_T50"
ACTUAL_SV_ROW_ID = "zhao_cui_sv_actual_nongaussian_T1000"
KSC_SV_ROW_ID = "zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000"
FIXED_SIR_AUSTRIA_ROW_ID = "zhao_cui_spatial_sir_austria_j9_T20"
PARAMETERIZED_SIR_DIAGNOSTIC_ROW_ID = (
    "zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale"
)
PREDATOR_PREY_ROW_ID = "zhao_cui_predator_prey_T20"
GENERALIZED_SV_ROW_ID = "zhao_cui_generalized_sv_synthetic_from_estimated_values"
MAIN_OBSERVED_DATA_ROW_SCOPE = "main_observed_data_filtering_row"
LEGACY_SCOPED_PARAMETERIZED_SIR_DIAGNOSTIC_SCOPE = (
    "legacy_scoped_parameterized_sir_diagnostic"
)
SIR_LOG_SCALE_PARAMETER_ORDER = (
    "log_kappa_scale",
    "log_nu_scale",
    "log_obs_noise_scale",
)
LGSSM_M3_T50_PARAMETER_ORDER = ("phi1", "phi2", "phi3", "q_scale", "r_scale")
SV_SYNTHETIC_PARAMETER_ORDER = ("gamma_unconstrained", "log_beta")
PREDATOR_PREY_PARAMETER_ORDER = ("r", "K", "a", "s", "u", "v")
GENERALIZED_SV_PARAMETER_ORDER = ("gamma_unconstrained", "log_tau", "mu")

_REQUIRED_TARGET_DENSITY_FIELDS = frozenset(LEDH_TARGET_DENSITY_FIELDS)
_REQUIRED_PROPOSAL_FLOW_FIELDS = frozenset(("pre_flow_log_density", "forward_log_det"))
_PROPOSAL_SCALAR_ALIASES = frozenset(
    {
        "flow_log_likelihood",
        "ledh_flow_log_likelihood",
        "ledh_flow_objective",
        "pre_flow_log_density",
        "proposal_log_likelihood",
        "proposal_observation_surface",
        "transport_objective",
    }
)


def _require_text(name: str, value: object) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{name} must be a nonempty string")
    return value


def _as_text_tuple(name: str, values: Sequence[str]) -> tuple[str, ...]:
    output = tuple(_require_text(f"{name}[{index}]", item) for index, item in enumerate(values))
    if not output:
        raise ValueError(f"{name} must be nonempty")
    return output


def _as_float_tuple(name: str, values: Sequence[float]) -> tuple[float, ...]:
    output = tuple(float(item) for item in values)
    if not output:
        raise ValueError(f"{name} must be nonempty")
    return output


@dataclass(frozen=True)
class LEDHThetaContract:
    """Theta-vector identity for an LEDH forward row."""

    row_id: str
    theta_coordinate_system: str
    theta_dimension: int
    parameter_order: Sequence[str]
    truth_theta: Sequence[float]
    theta_status: str = "phase1_frozen"
    source_classification: str = "row_metadata_contract"
    nonclaims: Sequence[str] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        row_id = _require_text("row_id", self.row_id)
        theta_coordinate_system = _require_text(
            "theta_coordinate_system",
            self.theta_coordinate_system,
        )
        parameter_order = _as_text_tuple("parameter_order", self.parameter_order)
        truth_theta = _as_float_tuple("truth_theta", self.truth_theta)
        theta_dimension = int(self.theta_dimension)
        if theta_dimension <= 0:
            raise ValueError("theta_dimension must be positive")
        if len(parameter_order) != theta_dimension:
            raise ValueError("parameter_order length must match theta_dimension")
        if len(truth_theta) != theta_dimension:
            raise ValueError("truth_theta length must match theta_dimension")
        if row_id == FIXED_SIR_AUSTRIA_ROW_ID:
            if theta_coordinate_system == "no_free_theta":
                raise ValueError("fixed SIR row must not use no_free_theta")
            if theta_coordinate_system != "sir_log_scale_theta":
                raise ValueError("fixed SIR row must use sir_log_scale_theta")
            if parameter_order != SIR_LOG_SCALE_PARAMETER_ORDER:
                raise ValueError("fixed SIR row parameter_order mismatch")
            if theta_dimension != 3:
                raise ValueError("fixed SIR row theta_dimension must be 3")
        if row_id == PARAMETERIZED_SIR_DIAGNOSTIC_ROW_ID:
            if theta_coordinate_system != "sir_log_scale_theta":
                raise ValueError("scoped parameterized SIR must use sir_log_scale_theta")
            if parameter_order != SIR_LOG_SCALE_PARAMETER_ORDER:
                raise ValueError("scoped parameterized SIR parameter_order mismatch")
        object.__setattr__(self, "row_id", row_id)
        object.__setattr__(self, "theta_coordinate_system", theta_coordinate_system)
        object.__setattr__(self, "theta_dimension", theta_dimension)
        object.__setattr__(self, "parameter_order", parameter_order)
        object.__setattr__(self, "truth_theta", truth_theta)
        object.__setattr__(self, "theta_status", _require_text("theta_status", self.theta_status))
        object.__setattr__(
            self,
            "source_classification",
            _require_text("source_classification", self.source_classification),
        )
        object.__setattr__(self, "nonclaims", tuple(str(item) for item in self.nonclaims))

    def to_manifest(self) -> dict[str, Any]:
        return {
            "row_id": self.row_id,
            "theta_coordinate_system": self.theta_coordinate_system,
            "theta_dimension": self.theta_dimension,
            "parameter_order": list(self.parameter_order),
            "truth_theta": list(self.truth_theta),
            "theta_status": self.theta_status,
            "source_classification": self.source_classification,
            "nonclaims": list(self.nonclaims),
        }


@dataclass(frozen=True)
class LEDHForwardLikelihoodContract:
    """Same-target LEDH forward scalar contract."""

    row_id: str
    row_scope: str
    theta_contract: LEDHThetaContract
    target_scalar: str = LEDH_TARGET_SCALAR_OBSERVED_DATA_LOG_LIKELIHOOD
    output_tensor_field: str = LEDH_OUTPUT_TENSOR_FIELD_LOG_LIKELIHOOD
    target_density_fields: Sequence[str] = LEDH_TARGET_DENSITY_FIELDS
    proposal_flow_fields: Sequence[str] = LEDH_PROPOSAL_FLOW_FIELDS
    correction_formula: str = LEDH_CORRECTION_FORMULA
    estimator_kind: str = "finite_N_fixed_randomness_ledh_log_likelihood_estimator"
    value_status: str = "metadata_only_value_not_admitted"
    score_status: str = "metadata_only_score_not_admitted"
    full_leaderboard_row: bool = False
    metadata: Mapping[str, Any] = field(default_factory=dict)
    nonclaims: Sequence[str] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        row_id = _require_text("row_id", self.row_id)
        row_scope = _require_text("row_scope", self.row_scope)
        if self.theta_contract.row_id != row_id:
            raise ValueError("theta_contract row_id must match forward row_id")
        target_scalar = _require_text("target_scalar", self.target_scalar)
        if target_scalar in _PROPOSAL_SCALAR_ALIASES:
            raise ValueError("proposal scalar cannot be exposed as target_scalar")
        if target_scalar != LEDH_TARGET_SCALAR_OBSERVED_DATA_LOG_LIKELIHOOD:
            raise ValueError(
                "target_scalar must be observed_data_log_likelihood_estimator"
            )
        output_tensor_field = _require_text("output_tensor_field", self.output_tensor_field)
        target_density_fields = _as_text_tuple(
            "target_density_fields",
            self.target_density_fields,
        )
        proposal_flow_fields = _as_text_tuple(
            "proposal_flow_fields",
            self.proposal_flow_fields,
        )
        missing_target = _REQUIRED_TARGET_DENSITY_FIELDS.difference(target_density_fields)
        if missing_target:
            raise ValueError(f"missing target density fields: {sorted(missing_target)}")
        missing_proposal = _REQUIRED_PROPOSAL_FLOW_FIELDS.difference(proposal_flow_fields)
        if missing_proposal:
            raise ValueError(f"missing proposal correction fields: {sorted(missing_proposal)}")
        if set(target_density_fields).intersection(proposal_flow_fields):
            raise ValueError("target density fields and proposal flow fields must be distinct")
        if output_tensor_field in proposal_flow_fields:
            raise ValueError("output_tensor_field must not name a proposal/flow field")
        correction_formula = _require_text("correction_formula", self.correction_formula)
        if correction_formula != LEDH_CORRECTION_FORMULA:
            raise ValueError("unexpected LEDH correction formula")
        if row_id == PARAMETERIZED_SIR_DIAGNOSTIC_ROW_ID:
            if row_scope != LEGACY_SCOPED_PARAMETERIZED_SIR_DIAGNOSTIC_SCOPE:
                raise ValueError("scoped parameterized SIR cannot be promoted to full row")
            if bool(self.full_leaderboard_row):
                raise ValueError("scoped parameterized SIR cannot be a full leaderboard row")
        if row_id == FIXED_SIR_AUSTRIA_ROW_ID and row_scope != MAIN_OBSERVED_DATA_ROW_SCOPE:
            raise ValueError("fixed SIR row must use main observed-data row scope")
        object.__setattr__(self, "row_id", row_id)
        object.__setattr__(self, "row_scope", row_scope)
        object.__setattr__(self, "target_scalar", target_scalar)
        object.__setattr__(self, "output_tensor_field", output_tensor_field)
        object.__setattr__(self, "target_density_fields", target_density_fields)
        object.__setattr__(self, "proposal_flow_fields", proposal_flow_fields)
        object.__setattr__(self, "correction_formula", correction_formula)
        object.__setattr__(
            self,
            "estimator_kind",
            _require_text("estimator_kind", self.estimator_kind),
        )
        object.__setattr__(self, "value_status", _require_text("value_status", self.value_status))
        object.__setattr__(self, "score_status", _require_text("score_status", self.score_status))
        object.__setattr__(self, "full_leaderboard_row", bool(self.full_leaderboard_row))
        object.__setattr__(self, "metadata", dict(self.metadata))
        object.__setattr__(self, "nonclaims", tuple(str(item) for item in self.nonclaims))

    def to_manifest(self) -> dict[str, Any]:
        return {
            "schema_version": "bayesfilter.highdim.ledh_forward_contract.v1",
            "row_id": self.row_id,
            "row_scope": self.row_scope,
            "target_scalar": self.target_scalar,
            "output_tensor_field": self.output_tensor_field,
            "target_density_fields": list(self.target_density_fields),
            "proposal_flow_fields": list(self.proposal_flow_fields),
            "correction_formula": self.correction_formula,
            "estimator_kind": self.estimator_kind,
            "value_status": self.value_status,
            "score_status": self.score_status,
            "full_leaderboard_row": self.full_leaderboard_row,
            "theta_contract": self.theta_contract.to_manifest(),
            "metadata": dict(self.metadata),
            "nonclaims": list(self.nonclaims),
        }


def validate_ledh_forward_contract_manifest(manifest: Mapping[str, Any]) -> dict[str, Any]:
    """Validate and normalize a serialized LEDH forward contract."""

    if manifest.get("schema_version") != "bayesfilter.highdim.ledh_forward_contract.v1":
        raise ValueError("invalid LEDH forward contract schema_version")
    theta_payload = manifest.get("theta_contract")
    if not isinstance(theta_payload, Mapping):
        raise ValueError("theta_contract must be a mapping")
    theta_contract = LEDHThetaContract(
        row_id=theta_payload["row_id"],
        theta_coordinate_system=theta_payload["theta_coordinate_system"],
        theta_dimension=theta_payload["theta_dimension"],
        parameter_order=theta_payload["parameter_order"],
        truth_theta=theta_payload["truth_theta"],
        theta_status=theta_payload.get("theta_status", "phase1_frozen"),
        source_classification=theta_payload.get(
            "source_classification",
            "row_metadata_contract",
        ),
        nonclaims=theta_payload.get("nonclaims", ()),
    )
    contract = LEDHForwardLikelihoodContract(
        row_id=manifest["row_id"],
        row_scope=manifest["row_scope"],
        theta_contract=theta_contract,
        target_scalar=manifest["target_scalar"],
        output_tensor_field=manifest.get(
            "output_tensor_field",
            LEDH_OUTPUT_TENSOR_FIELD_LOG_LIKELIHOOD,
        ),
        target_density_fields=manifest["target_density_fields"],
        proposal_flow_fields=manifest["proposal_flow_fields"],
        correction_formula=manifest["correction_formula"],
        estimator_kind=manifest.get(
            "estimator_kind",
            "finite_N_fixed_randomness_ledh_log_likelihood_estimator",
        ),
        value_status=manifest.get("value_status", "metadata_only_value_not_admitted"),
        score_status=manifest.get("score_status", "metadata_only_score_not_admitted"),
        full_leaderboard_row=bool(manifest.get("full_leaderboard_row", False)),
        metadata=manifest.get("metadata", {}),
        nonclaims=manifest.get("nonclaims", ()),
    )
    return contract.to_manifest()


def make_lgssm_m3_t50_forward_contract(
    *,
    truth_theta: Sequence[float],
    time_steps: int | None = None,
    num_particles: int | None = None,
    batch_seeds: Sequence[int] = (),
    full_leaderboard_row: bool = False,
) -> LEDHForwardLikelihoodContract:
    theta_contract = LEDHThetaContract(
        row_id=LGSSM_M3_T50_ROW_ID,
        theta_coordinate_system="physical_benchmark_exact_oracle",
        theta_dimension=5,
        parameter_order=LGSSM_M3_T50_PARAMETER_ORDER,
        truth_theta=truth_theta,
        source_classification="benchmark_exact_oracle_row",
    )
    return LEDHForwardLikelihoodContract(
        row_id=LGSSM_M3_T50_ROW_ID,
        row_scope=MAIN_OBSERVED_DATA_ROW_SCOPE,
        theta_contract=theta_contract,
        value_status="same_target_value_metadata_present",
        score_status="score_requires_no_tape_same_scalar_gate",
        full_leaderboard_row=full_leaderboard_row,
        metadata={
            "time_steps": time_steps,
            "num_particles": num_particles,
            "batch_seeds": [int(seed) for seed in batch_seeds],
        },
        nonclaims=(
            "metadata alone is not row admission",
            "metadata alone is not score evidence",
        ),
    )


def make_fixed_sir_logscale_forward_contract(
    *,
    time_steps: int | None = None,
    num_particles: int | None = None,
    batch_seeds: Sequence[int] = (),
    full_leaderboard_row: bool = True,
) -> LEDHForwardLikelihoodContract:
    theta_contract = LEDHThetaContract(
        row_id=FIXED_SIR_AUSTRIA_ROW_ID,
        theta_coordinate_system="sir_log_scale_theta",
        theta_dimension=3,
        parameter_order=SIR_LOG_SCALE_PARAMETER_ORDER,
        truth_theta=(0.0, 0.0, 0.0),
        source_classification="source_base_with_logscale_theta_extension",
        nonclaims=(
            "not Zhao-Cui author-source free-theta faithfulness",
            "not fixed-SIR score admission",
        ),
    )
    return LEDHForwardLikelihoodContract(
        row_id=FIXED_SIR_AUSTRIA_ROW_ID,
        row_scope=MAIN_OBSERVED_DATA_ROW_SCOPE,
        theta_contract=theta_contract,
        value_status="amended_sir_log_scale_theta_value_metadata_present",
        score_status="blocked_score_until_same_target_no_tape_gate",
        full_leaderboard_row=full_leaderboard_row,
        metadata={
            "time_steps": time_steps,
            "num_particles": num_particles,
            "batch_seeds": [int(seed) for seed in batch_seeds],
        },
        nonclaims=(
            "metadata alone is not fixed-SIR value admission",
            "metadata alone is not fixed-SIR score evidence",
        ),
    )


def make_parameterized_sir_diagnostic_forward_contract(
    *,
    time_steps: int | None = None,
    num_particles: int | None = None,
    batch_seeds: Sequence[int] = (),
) -> LEDHForwardLikelihoodContract:
    theta_contract = LEDHThetaContract(
        row_id=PARAMETERIZED_SIR_DIAGNOSTIC_ROW_ID,
        theta_coordinate_system="sir_log_scale_theta",
        theta_dimension=3,
        parameter_order=SIR_LOG_SCALE_PARAMETER_ORDER,
        truth_theta=(0.0, 0.0, 0.0),
        source_classification="legacy_scoped_diagnostic_theta_surface",
        nonclaims=(
            "not full observed-data fixed SIR score admission",
            "not a substitute for the amended fixed SIR row",
        ),
    )
    return LEDHForwardLikelihoodContract(
        row_id=PARAMETERIZED_SIR_DIAGNOSTIC_ROW_ID,
        row_scope=LEGACY_SCOPED_PARAMETERIZED_SIR_DIAGNOSTIC_SCOPE,
        theta_contract=theta_contract,
        value_status="legacy_scoped_parameterized_sir_diagnostic_value_metadata_present",
        score_status="legacy_scoped_diagnostic_score_only",
        full_leaderboard_row=False,
        metadata={
            "time_steps": time_steps,
            "num_particles": num_particles,
            "batch_seeds": [int(seed) for seed in batch_seeds],
        },
        nonclaims=(
            "not full observed-data fixed SIR score admission",
            "not a substitute for the amended fixed SIR same-target score gate",
        ),
    )


def make_actual_sv_forward_contract(
    *,
    time_steps: int | None = None,
    num_particles: int | None = None,
    batch_seeds: Sequence[int] = (),
    full_leaderboard_row: bool = False,
) -> LEDHForwardLikelihoodContract:
    theta_contract = LEDHThetaContract(
        row_id=ACTUAL_SV_ROW_ID,
        theta_coordinate_system="synthetic_unconstrained",
        theta_dimension=2,
        parameter_order=SV_SYNTHETIC_PARAMETER_ORDER,
        truth_theta=(0.2533471031357997, -0.916290731874155),
        source_classification="phase1_actual_sv_transformed_target_contract",
        nonclaims=(
            "not KSC surrogate likelihood",
            "not raw Gaussian-closure route admission",
        ),
    )
    return LEDHForwardLikelihoodContract(
        row_id=ACTUAL_SV_ROW_ID,
        row_scope=MAIN_OBSERVED_DATA_ROW_SCOPE,
        theta_contract=theta_contract,
        value_status="actual_sv_same_target_value_metadata_present",
        score_status="blocked_score_until_same_target_no_tape_gate",
        full_leaderboard_row=full_leaderboard_row,
        metadata={
            "time_steps": time_steps,
            "num_particles": num_particles,
            "batch_seeds": [int(seed) for seed in batch_seeds],
            "target_observation_policy": "transformed_actual_sv_log_y_square",
        },
        nonclaims=(
            "metadata alone is not actual-SV value admission",
            "metadata alone is not actual-SV score evidence",
        ),
    )


def make_ksc_sv_forward_contract(
    *,
    time_steps: int | None = None,
    num_particles: int | None = None,
    batch_seeds: Sequence[int] = (),
    full_leaderboard_row: bool = False,
) -> LEDHForwardLikelihoodContract:
    theta_contract = LEDHThetaContract(
        row_id=KSC_SV_ROW_ID,
        theta_coordinate_system="synthetic_unconstrained",
        theta_dimension=2,
        parameter_order=SV_SYNTHETIC_PARAMETER_ORDER,
        truth_theta=(0.2533471031357997, -0.916290731874155),
        source_classification="phase1_ksc_gaussian_mixture_surrogate_contract",
        nonclaims=(
            "not native actual-SV likelihood",
            "not raw SV callback evidence",
        ),
    )
    return LEDHForwardLikelihoodContract(
        row_id=KSC_SV_ROW_ID,
        row_scope=MAIN_OBSERVED_DATA_ROW_SCOPE,
        theta_contract=theta_contract,
        value_status="ksc_sv_same_target_value_metadata_present",
        score_status="blocked_score_until_same_target_no_tape_gate",
        full_leaderboard_row=full_leaderboard_row,
        metadata={
            "time_steps": time_steps,
            "num_particles": num_particles,
            "batch_seeds": [int(seed) for seed in batch_seeds],
            "target_observation_policy": "ksc_log_chi_square_gaussian_mixture_surrogate",
        },
        nonclaims=(
            "metadata alone is not KSC LEDH value admission",
            "metadata alone is not KSC score evidence",
        ),
    )


def make_predator_prey_forward_contract(
    *,
    time_steps: int | None = None,
    num_particles: int | None = None,
    batch_seeds: Sequence[int] = (),
    full_leaderboard_row: bool = False,
) -> LEDHForwardLikelihoodContract:
    theta_contract = LEDHThetaContract(
        row_id=PREDATOR_PREY_ROW_ID,
        theta_coordinate_system="physical",
        theta_dimension=6,
        parameter_order=PREDATOR_PREY_PARAMETER_ORDER,
        truth_theta=(0.6, 114.0, 25.0, 0.3, 0.5, 0.5),
        source_classification="phase1_predator_prey_additive_gaussian_contract",
    )
    return LEDHForwardLikelihoodContract(
        row_id=PREDATOR_PREY_ROW_ID,
        row_scope=MAIN_OBSERVED_DATA_ROW_SCOPE,
        theta_contract=theta_contract,
        value_status="predator_prey_same_target_value_metadata_present",
        score_status="blocked_score_until_same_target_no_tape_gate",
        full_leaderboard_row=full_leaderboard_row,
        metadata={
            "time_steps": time_steps,
            "num_particles": num_particles,
            "batch_seeds": [int(seed) for seed in batch_seeds],
            "target_observation_policy": "additive_gaussian_predator_prey",
        },
        nonclaims=(
            "metadata alone is not predator-prey value admission",
            "metadata alone is not predator-prey score evidence",
        ),
    )


def make_generalized_sv_forward_contract(
    *,
    time_steps: int | None = None,
    num_particles: int | None = None,
    batch_seeds: Sequence[int] = (),
    full_leaderboard_row: bool = False,
) -> LEDHForwardLikelihoodContract:
    theta_contract = LEDHThetaContract(
        row_id=GENERALIZED_SV_ROW_ID,
        theta_coordinate_system="source_route_active_transformed_prior_mean",
        theta_dimension=3,
        parameter_order=GENERALIZED_SV_PARAMETER_ORDER,
        truth_theta=(1.0824113944610982, -2.076793740349318, 0.0),
        source_classification="phase1_generalized_sv_source_row_contract",
        nonclaims=(
            "not actual-SV row",
            "not KSC row",
            "not native generalized-SV fixture substitution",
        ),
    )
    return LEDHForwardLikelihoodContract(
        row_id=GENERALIZED_SV_ROW_ID,
        row_scope=MAIN_OBSERVED_DATA_ROW_SCOPE,
        theta_contract=theta_contract,
        value_status="generalized_sv_same_target_value_metadata_present",
        score_status="blocked_score_until_same_target_no_tape_gate",
        full_leaderboard_row=full_leaderboard_row,
        metadata={
            "time_steps": time_steps,
            "num_particles": num_particles,
            "batch_seeds": [int(seed) for seed in batch_seeds],
            "target_observation_policy": "source_route_prior_mean_generalized_sv",
        },
        nonclaims=(
            "metadata alone is not generalized-SV value admission",
            "metadata alone is not generalized-SV score evidence",
        ),
    )
