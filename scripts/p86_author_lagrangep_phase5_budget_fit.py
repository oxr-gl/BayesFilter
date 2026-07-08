#!/usr/bin/env python
"""P86 Phase 5 training-base budget preflight for the author Lagrangep route."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import resource
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Mapping, Sequence

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")
os.environ.setdefault("MPLCONFIGDIR", "/tmp")

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import tensorflow as tf  # noqa: E402

from bayesfilter.highdim.bases import (  # noqa: E402
    P85_AUTHOR_SIR_CLASSIFICATION,
    P85_AUTHOR_SIR_DEGREE_COMPARATOR_CLASSIFICATION,
    P85_AUTHOR_SIR_DEGREE_COMPARATOR_SUBTYPE,
    P85_AUTHOR_SIR_SUBTYPE,
    P85_AUTHOR_SIR_LAGRANGEP_NUM_ELEMS,
    P85_AUTHOR_SIR_LAGRANGEP_ORDER,
    p85_author_sir_lagrangep_algebraic_product_basis_spec,
)
from bayesfilter.highdim.diagnostics import (  # noqa: E402
    DensityMeasure,
    MassMeasure,
    MeasureConvention,
)
from bayesfilter.highdim.models import zhao_cui_sir_austria_model  # noqa: E402
from bayesfilter.highdim.source_route import (  # noqa: E402
    P62_AUTHOR_TTSIRT_EXECUTABLE_DEFAULT_TAU,
    P63_AUTHOR_SIR_EXPANSION_FACTOR,
    P65_FIXED_BRANCH_ADAPTATION_CLASS,
    P70_FIXED_BRANCH_INITIALIZATION_RULE,
    _p59_author_sir_deterministic_weighted_resample,
    _p59_author_sir_source_density_callbacks,
    _p59_author_sir_source_push_result,
    _source_route_seeded_channel_initial_cores,
    _weighted_mean_target_value,
    source_route_recenter,
    source_route_shifted_negative_log_target,
    SourceRouteSequentialDensityComponents,
    _p59_author_sir_prior_sample_batch,
)
from bayesfilter.highdim.stochastic_density_training import (  # noqa: E402
    P75ObjectiveBatch,
    P75TrainableTTConfig,
    TrainableFunctionalTT,
    config_payload,
    make_adam_optimizer,
    prefit_terms_payload,
    terms_payload,
)
from bayesfilter.highdim.tt import TTCore  # noqa: E402


SCRIPT_RELATIVE = "scripts/p86_author_lagrangep_phase5_budget_fit.py"
PHASE5_SUBPLAN = (
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p86-phase5-budget-compliant-fit-subplan-2026-06-24.md"
)
PHASE5_RESULT = (
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p86-phase5-budget-compliant-fit-result-2026-06-24.md"
)
PHASE6_SUBPLAN = (
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p86-phase6-rank-degree-convergence-subplan-2026-06-24.md"
)
PREFLIGHT_OUTPUT = Path(
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p86-phase5-budget-compliant-fit-preflight-2026-06-24.json"
)
FIT_OUTPUT = Path(
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p86-phase5-budget-compliant-fit-2026-06-24.json"
)
TRAINING_BASE_RETRY_OUTPUT = Path(
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p86-training-base-retry-smoke-2026-06-24.json"
)
PHASE6R_ADAPTIVE_SMOKE_OUTPUT = Path(
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p86-phase6r-tiny-adaptive-training-smoke-2026-06-24.json"
)
PHASE6_RANK_PREFLIGHT_OUTPUT = Path(
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p86-phase6-rank-convergence-preflight-2026-06-24.json"
)
PHASE6_RANK5_FIT_OUTPUT = Path(
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p86-phase6-rank5-comparator-fit-2026-06-24.json"
)
PHASE6S_RANK5_ADAPTIVE_PREFLIGHT_OUTPUT = Path(
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p86-phase6s-rank5-adaptive-preflight-2026-06-25.json"
)
PHASE6S_RANK5_ADAPTIVE_FIT_OUTPUT = Path(
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p86-phase6s-rank5-adaptive-comparator-fit-2026-06-25.json"
)
PHASE6T_L1_TUNING_PREFLIGHT_OUTPUT = Path(
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p86-phase6t-l1-regularization-tuning-preflight-2026-06-25.json"
)
PHASE6T_L1_TUNING_DIAGNOSTIC_OUTPUT = Path(
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p86-phase6t-l1-regularization-tuning-diagnostic-2026-06-25.json"
)
PHASE6V_L1_SELECTION_PREFLIGHT_OUTPUT = Path(
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-preflight-2026-06-25.json"
)
PHASE6V_L1_SELECTION_L1_0_OUTPUT = Path(
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-rank5-lr3e-4-l1-0-fit-2026-06-25.json"
)
PHASE6V_L1_SELECTION_L1_3E_10_OUTPUT = Path(
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-rank5-lr3e-4-l1-3e-10-fit-2026-06-25.json"
)
PHASE6V_L1_SELECTION_L1_3E_9_OUTPUT = Path(
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-rank5-lr3e-4-l1-3e-9-fit-2026-06-25.json"
)
PHASE6W_SAME_POLICY_RANK_PREFLIGHT_OUTPUT = Path(
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p86-phase6w-same-policy-rank-convergence-preflight-2026-06-25.json"
)
PHASE6W_RANK4_L1_0_OUTPUT = Path(
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p86-phase6w-rank4-lr3e-4-l1-0-fit-2026-06-25.json"
)
PHASE6W_RANK4_L1_3E_10_OUTPUT = Path(
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p86-phase6w-rank4-lr3e-4-l1-3e-10-fit-2026-06-25.json"
)
PHASE6W_RANK4_L1_1E_9_OUTPUT = Path(
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p86-phase6w-rank4-lr3e-4-l1-1e-9-fit-2026-06-25.json"
)
PHASE6W_RANK4_L1_3E_9_OUTPUT = Path(
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p86-phase6w-rank4-lr3e-4-l1-3e-9-fit-2026-06-25.json"
)
PHASE6Y_DEGREE_COMPARATOR_PREFLIGHT_OUTPUT = Path(
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p86-phase6y-degree-comparator-preflight-2026-06-26.json"
)
PHASE6Y_DEGREE_ORDER3_RANK4_L1_0_OUTPUT = Path(
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p86-phase6y-degree-order3-rank4-lr3e-4-l1-0-fit-2026-06-26.json"
)
P88_PHASE2_DEGREE_COMPARATOR_PREFLIGHT_OUTPUT = Path(
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p88-phase2-degree-comparator-preflight-2026-06-27.json"
)
P88_PHASE2_DEGREE_ORDER3_RANK4_L1_0_OUTPUT = Path(
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p88-phase2-degree-order3-rank4-lr3e-4-l1-0-fit-2026-06-27.json"
)
TRAINING_BACKEND = "training_base_optimizer"
HISTORICAL_ALS_TRAINING_STATUS = (
    "historical_buggy_stale_route_not_allowed_for_fixed_variant_zhao_cui_training"
)
DEFAULT_OPTIMIZER_BATCH_SIZE = 4096
DEFAULT_PREFIT_STEPS = 0
DEFAULT_TRAIN_STEPS = 89
DEFAULT_LEARNING_RATE = 1e-3
DEFAULT_TRAIN_PRIOR_SEED = 6301
DEFAULT_TRAIN_PROCESS_SEED = 6401
DEFAULT_HOLDOUT_PRIOR_SEED = 7301
DEFAULT_HOLDOUT_PROCESS_SEED = 7401
DEFAULT_AUDIT_PRIOR_SEED = 7311
DEFAULT_AUDIT_PROCESS_SEED = 7501
DEFAULT_ADAPTIVE_TRAINING = False
DEFAULT_VALIDATION_CHECK_EVERY = 0
DEFAULT_PLATEAU_PATIENCE = 0
DEFAULT_PLATEAU_MIN_DELTA = 0.0
DEFAULT_LR_REDUCTION_FACTOR = 0.5
DEFAULT_MIN_LEARNING_RATE = 1e-6
DEFAULT_EARLY_STOP_AFTER_LR_DROPS = 0
DEFAULT_SERIALIZE_TRAINED_CORES = False
DEFAULT_L1_WEIGHT = 0.0
DEFAULT_L2_WEIGHT = 1e-8
DEFAULT_LOGZ_ANCHOR_WEIGHT = 0.0
ZHAO_CUI_L1_TUNING_DEFAULT_POLICY = (
    "l1_weight_tuning_required_for_zhao_cui_training_base_decisions"
)
ZHAO_CUI_L1_TUNING_SELECTION_STATUS = (
    "requires_reviewed_tuning_selection_ledger_before_rank_convergence_or_production"
)
PHASE6_RANK5_FIT_RANK = 5
PHASE6_RANK5_TRAINING_SAMPLE_COUNT = 567600
PHASE6_RANK5_TRAIN_STEPS = 139
PHASE6_RANK5_SEED = 8606
PHASE6_RANK5_TRAIN_PRIOR_SEED = 8301
PHASE6_RANK5_TRAIN_PROCESS_SEED = 8401
PHASE6_RANK5_HOLDOUT_PRIOR_SEED = 9301
PHASE6_RANK5_HOLDOUT_PROCESS_SEED = 9401
PHASE6_RANK5_AUDIT_PRIOR_SEED = 9311
PHASE6_RANK5_AUDIT_PROCESS_SEED = 9501
PHASE6S_RANK5_ADAPTIVE_TRAIN_STEPS = 1024
PHASE6S_RANK5_ADAPTIVE_VALIDATION_CHECK_EVERY = 16
PHASE6S_RANK5_ADAPTIVE_PLATEAU_PATIENCE = 4
PHASE6S_RANK5_ADAPTIVE_PLATEAU_MIN_DELTA = 1e-6
PHASE6S_RANK5_ADAPTIVE_EARLY_STOP_AFTER_LR_DROPS = 4
PHASE6T_L1_TUNING_TRAIN_STEPS = 512
PHASE6T_L1_TUNING_LEARNING_RATE = 3e-4
PHASE6T_L1_TUNING_L1_WEIGHT = 1e-9
PHASE6T_L1_TUNING_L2_WEIGHT = DEFAULT_L2_WEIGHT
PHASE6T_L1_TUNING_LOGZ_ANCHOR_WEIGHT = DEFAULT_LOGZ_ANCHOR_WEIGHT
PHASE6T_L1_TUNING_MAX_SECONDS = 7200
PHASE6V_L1_SELECTION_TRAIN_STEPS = 512
PHASE6V_L1_SELECTION_LEARNING_RATE = 3e-4
PHASE6V_L1_SELECTION_L2_WEIGHT = DEFAULT_L2_WEIGHT
PHASE6V_L1_SELECTION_LOGZ_ANCHOR_WEIGHT = DEFAULT_LOGZ_ANCHOR_WEIGHT
PHASE6V_L1_SELECTION_MAX_SECONDS = 7200
PHASE6V_L1_SELECTION_HOLDOUT_THRESHOLD = 0.5 * 0.22090990401849483
PHASE6W_RANK4_FIT_RANK = 4
PHASE6W_RANK4_TRAINING_SAMPLE_COUNT = 364320
PHASE6W_RANK4_TRAIN_STEPS = 512
PHASE6W_RANK4_LEARNING_RATE = 3e-4
PHASE6W_RANK4_L2_WEIGHT = DEFAULT_L2_WEIGHT
PHASE6W_RANK4_LOGZ_ANCHOR_WEIGHT = DEFAULT_LOGZ_ANCHOR_WEIGHT
PHASE6W_RANK4_MAX_SECONDS = 7200
PHASE6Y_DEGREE_FIT_RANK = 4
PHASE6Y_DEGREE_BASIS_ORDER = 3
PHASE6Y_DEGREE_BASIS_NUM_ELEMS = 8
PHASE6Y_DEGREE_BASIS_DIM = 25
PHASE6Y_DEGREE_P_THETA = 13800
PHASE6Y_DEGREE_TRAINING_SAMPLE_COUNT = 276000
PHASE6Y_DEGREE_TRAIN_STEPS = 512
PHASE6Y_DEGREE_LEARNING_RATE = 3e-4
PHASE6Y_DEGREE_L1_WEIGHT = DEFAULT_L1_WEIGHT
PHASE6Y_DEGREE_L2_WEIGHT = DEFAULT_L2_WEIGHT
PHASE6Y_DEGREE_LOGZ_ANCHOR_WEIGHT = DEFAULT_LOGZ_ANCHOR_WEIGHT
PHASE6Y_DEGREE_MAX_SECONDS = 7200
PHASE6Y_DEGREE_SEED = 8608
PHASE6Y_DEGREE_TRAIN_PRIOR_SEED = 8303
PHASE6Y_DEGREE_TRAIN_PROCESS_SEED = 8403
PHASE6Y_DEGREE_HOLDOUT_PRIOR_SEED = 9303
PHASE6Y_DEGREE_HOLDOUT_PROCESS_SEED = 9403
PHASE6Y_DEGREE_AUDIT_PRIOR_SEED = 9313
PHASE6Y_DEGREE_AUDIT_PROCESS_SEED = 9503
FIT_COMMAND = (
    "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
    f"{SCRIPT_RELATIVE} --fit --preflight-json {PREFLIGHT_OUTPUT} "
    "--target-dimension 36 --fit-rank 4 --training-sample-count 364320 "
    "--holdout-sample-count 65536 --audit-sample-count 65536 --seed 8605 "
    "--optimizer-batch-size 4096 --prefit-steps 0 --train-steps 89 "
    "--learning-rate 0.001 --max-seconds 14400 --memory-cap-mib 12288 --output "
    f"{FIT_OUTPUT}"
)
TRAINING_BASE_SMOKE_COMMAND = (
    "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
    f"{SCRIPT_RELATIVE} --training-base-smoke --target-dimension 36 --fit-rank 1 "
    "--training-sample-count 64 --holdout-sample-count 32 --seed 8615 "
    "--optimizer-batch-size 32 --prefit-steps 1 --train-steps 1 "
    "--learning-rate 0.001 --max-seconds 120 --memory-cap-mib 12288 --output "
    f"{TRAINING_BASE_RETRY_OUTPUT}"
)
PHASE6R_ADAPTIVE_SMOKE_COMMAND = (
    "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
    f"{SCRIPT_RELATIVE} --phase6r-adaptive-smoke --target-dimension 36 "
    "--fit-rank 1 --training-sample-count 64 --holdout-sample-count 32 "
    "--seed 8615 --optimizer-batch-size 32 --prefit-steps 1 "
    "--train-steps 6 --learning-rate 0.001 --max-seconds 120 "
    "--memory-cap-mib 12288 --adaptive-training --validation-check-every 2 "
    "--plateau-patience 1 --plateau-min-delta 0.0 "
    "--lr-reduction-factor 0.5 --min-learning-rate 0.000001 "
    "--early-stop-after-lr-drops 2 --serialize-trained-cores --output "
    f"{PHASE6R_ADAPTIVE_SMOKE_OUTPUT}"
)
PREFLIGHT_COMMAND = (
    "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
    f"{SCRIPT_RELATIVE} --preflight-only --output {PREFLIGHT_OUTPUT}"
)
PHASE6_RANK_PREFLIGHT_COMMAND = (
    "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
    f"{SCRIPT_RELATIVE} --phase6-rank-preflight --output {PHASE6_RANK_PREFLIGHT_OUTPUT}"
)
PHASE6_RANK5_FIT_COMMAND = (
    "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
    f"{SCRIPT_RELATIVE} --fit --preflight-json {PHASE6_RANK_PREFLIGHT_OUTPUT} "
    "--target-dimension 36 --fit-rank 5 --training-sample-count 567600 "
    "--holdout-sample-count 65536 --audit-sample-count 65536 --seed 8606 "
    "--optimizer-batch-size 4096 --prefit-steps 0 --train-steps 139 "
    "--learning-rate 0.001 --max-seconds 14400 --memory-cap-mib 12288 "
    "--train-prior-seed 8301 --train-process-seed 8401 "
    "--holdout-prior-seed 9301 --holdout-process-seed 9401 "
    "--audit-prior-seed 9311 --audit-process-seed 9501 --output "
    f"{PHASE6_RANK5_FIT_OUTPUT}"
)
PHASE6S_RANK5_ADAPTIVE_PREFLIGHT_COMMAND = (
    "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
    f"{SCRIPT_RELATIVE} --phase6s-adaptive-rank5-preflight --output "
    f"{PHASE6S_RANK5_ADAPTIVE_PREFLIGHT_OUTPUT}"
)
PHASE6S_RANK5_ADAPTIVE_FIT_COMMAND = (
    "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
    f"{SCRIPT_RELATIVE} --fit --preflight-json {PHASE6S_RANK5_ADAPTIVE_PREFLIGHT_OUTPUT} "
    "--target-dimension 36 --fit-rank 5 --training-sample-count 567600 "
    "--holdout-sample-count 65536 --audit-sample-count 65536 --seed 8606 "
    "--optimizer-batch-size 4096 --prefit-steps 0 --train-steps 1024 "
    "--learning-rate 0.001 --max-seconds 14400 --memory-cap-mib 12288 "
    "--adaptive-training --validation-check-every 16 --plateau-patience 4 "
    "--plateau-min-delta 0.000001 --lr-reduction-factor 0.5 "
    "--min-learning-rate 0.000001 --early-stop-after-lr-drops 4 "
    "--serialize-trained-cores --train-prior-seed 8301 --train-process-seed 8401 "
    "--holdout-prior-seed 9301 --holdout-process-seed 9401 "
    "--audit-prior-seed 9311 --audit-process-seed 9501 --output "
    f"{PHASE6S_RANK5_ADAPTIVE_FIT_OUTPUT}"
)
PHASE6T_L1_TUNING_PREFLIGHT_COMMAND = (
    "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
    f"{SCRIPT_RELATIVE} --phase6t-l1-tuning-preflight --output "
    f"{PHASE6T_L1_TUNING_PREFLIGHT_OUTPUT}"
)
PHASE6T_L1_TUNING_FIT_COMMAND = (
    "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
    f"{SCRIPT_RELATIVE} --fit --preflight-json {PHASE6T_L1_TUNING_PREFLIGHT_OUTPUT} "
    "--target-dimension 36 --fit-rank 5 --training-sample-count 567600 "
    "--holdout-sample-count 65536 --audit-sample-count 65536 --seed 8606 "
    "--optimizer-batch-size 4096 --prefit-steps 0 --train-steps 512 "
    "--learning-rate 0.0003 --l1-weight 0.000000001 "
    "--l2-weight 0.00000001 --logz-anchor-weight 0.0 "
    "--max-seconds 7200 --memory-cap-mib 12288 --adaptive-training "
    "--validation-check-every 16 --plateau-patience 4 "
    "--plateau-min-delta 0.000001 --lr-reduction-factor 0.5 "
    "--min-learning-rate 0.000001 --early-stop-after-lr-drops 4 "
    "--serialize-trained-cores --train-prior-seed 8301 --train-process-seed 8401 "
    "--holdout-prior-seed 9301 --holdout-process-seed 9401 "
    "--audit-prior-seed 9311 --audit-process-seed 9501 --output "
    f"{PHASE6T_L1_TUNING_DIAGNOSTIC_OUTPUT}"
)
PHASE6V_L1_SELECTION_PREFLIGHT_COMMAND = (
    "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
    f"{SCRIPT_RELATIVE} --phase6v-l1-selection-preflight --output "
    f"{PHASE6V_L1_SELECTION_PREFLIGHT_OUTPUT}"
)


def _basis_cli_suffix(*, basis_order: int, basis_num_elems: int) -> str:
    if (
        int(basis_order) == P85_AUTHOR_SIR_LAGRANGEP_ORDER
        and int(basis_num_elems) == P85_AUTHOR_SIR_LAGRANGEP_NUM_ELEMS
    ):
        return ""
    return (
        f" --basis-order {int(basis_order)}"
        f" --basis-num-elems {int(basis_num_elems)} "
    )


def _phase6v_l1_selection_fit_command(
    *,
    l1_weight_text: str,
    output: Path,
    basis_order: int = P85_AUTHOR_SIR_LAGRANGEP_ORDER,
    basis_num_elems: int = P85_AUTHOR_SIR_LAGRANGEP_NUM_ELEMS,
) -> str:
    basis_suffix = _basis_cli_suffix(
        basis_order=basis_order,
        basis_num_elems=basis_num_elems,
    )
    return (
        "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
        f"{SCRIPT_RELATIVE} --fit --preflight-json {PHASE6V_L1_SELECTION_PREFLIGHT_OUTPUT} "
        "--target-dimension 36 --fit-rank 5 --training-sample-count 567600 "
        "--holdout-sample-count 65536 --audit-sample-count 65536 --seed 8606 "
        "--optimizer-batch-size 4096 --prefit-steps 0 --train-steps 512 "
        f"--learning-rate 0.0003 --l1-weight {l1_weight_text} "
        "--l2-weight 0.00000001 --logz-anchor-weight 0.0 "
        "--max-seconds 7200 --memory-cap-mib 12288 --adaptive-training "
        "--validation-check-every 16 --plateau-patience 4 "
        "--plateau-min-delta 0.000001 --lr-reduction-factor 0.5 "
        "--min-learning-rate 0.000001 --early-stop-after-lr-drops 4 "
        "--serialize-trained-cores --train-prior-seed 8301 --train-process-seed 8401 "
        f"{basis_suffix}"
        "--holdout-prior-seed 9301 --holdout-process-seed 9401 "
        "--audit-prior-seed 9311 --audit-process-seed 9501 --output "
        f"{output}"
    )


PHASE6V_L1_SELECTION_L1_0_FIT_COMMAND = _phase6v_l1_selection_fit_command(
    l1_weight_text="0.0",
    output=PHASE6V_L1_SELECTION_L1_0_OUTPUT,
)
PHASE6V_L1_SELECTION_L1_3E_10_FIT_COMMAND = _phase6v_l1_selection_fit_command(
    l1_weight_text="0.0000000003",
    output=PHASE6V_L1_SELECTION_L1_3E_10_OUTPUT,
)
PHASE6V_L1_SELECTION_L1_3E_9_FIT_COMMAND = _phase6v_l1_selection_fit_command(
    l1_weight_text="0.000000003",
    output=PHASE6V_L1_SELECTION_L1_3E_9_OUTPUT,
)
def _phase6w_same_policy_rank_preflight_command(
    *,
    output: Path,
    basis_order: int = P85_AUTHOR_SIR_LAGRANGEP_ORDER,
    basis_num_elems: int = P85_AUTHOR_SIR_LAGRANGEP_NUM_ELEMS,
) -> str:
    basis_suffix = _basis_cli_suffix(
        basis_order=basis_order,
        basis_num_elems=basis_num_elems,
    )
    return (
        "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
        f"{SCRIPT_RELATIVE} --phase6w-same-policy-rank-preflight{basis_suffix} --output "
        f"{output}"
    )


PHASE6W_SAME_POLICY_RANK_PREFLIGHT_COMMAND = _phase6w_same_policy_rank_preflight_command(
    output=PHASE6W_SAME_POLICY_RANK_PREFLIGHT_OUTPUT
)


def _phase6w_rank4_fit_command(
    *,
    l1_weight_text: str,
    output: Path,
    basis_order: int = P85_AUTHOR_SIR_LAGRANGEP_ORDER,
    basis_num_elems: int = P85_AUTHOR_SIR_LAGRANGEP_NUM_ELEMS,
) -> str:
    basis_suffix = _basis_cli_suffix(
        basis_order=basis_order,
        basis_num_elems=basis_num_elems,
    )
    return (
        "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
        f"{SCRIPT_RELATIVE} --fit --preflight-json {PHASE6W_SAME_POLICY_RANK_PREFLIGHT_OUTPUT} "
        "--target-dimension 36 --fit-rank 4 --training-sample-count 364320 "
        "--holdout-sample-count 65536 --audit-sample-count 65536 --seed 8606 "
        "--optimizer-batch-size 4096 --prefit-steps 0 --train-steps 512 "
        f"--learning-rate 0.0003 --l1-weight {l1_weight_text} "
        "--l2-weight 0.00000001 --logz-anchor-weight 0.0 "
        "--max-seconds 7200 --memory-cap-mib 12288 --adaptive-training "
        "--validation-check-every 16 --plateau-patience 4 "
        "--plateau-min-delta 0.000001 --lr-reduction-factor 0.5 "
        "--min-learning-rate 0.000001 --early-stop-after-lr-drops 4 "
        "--serialize-trained-cores --train-prior-seed 8301 --train-process-seed 8401 "
        f"{basis_suffix}"
        "--holdout-prior-seed 9301 --holdout-process-seed 9401 "
        "--audit-prior-seed 9311 --audit-process-seed 9501 --output "
        f"{output}"
    )


PHASE6W_RANK4_L1_0_FIT_COMMAND = _phase6w_rank4_fit_command(
    l1_weight_text="0.0",
    output=PHASE6W_RANK4_L1_0_OUTPUT,
)
PHASE6W_RANK4_L1_3E_10_FIT_COMMAND = _phase6w_rank4_fit_command(
    l1_weight_text="0.0000000003",
    output=PHASE6W_RANK4_L1_3E_10_OUTPUT,
)
PHASE6W_RANK4_L1_1E_9_FIT_COMMAND = _phase6w_rank4_fit_command(
    l1_weight_text="0.000000001",
    output=PHASE6W_RANK4_L1_1E_9_OUTPUT,
)
PHASE6W_RANK4_L1_3E_9_FIT_COMMAND = _phase6w_rank4_fit_command(
    l1_weight_text="0.000000003",
    output=PHASE6W_RANK4_L1_3E_9_OUTPUT,
)

PHASE6Y_DEGREE_COMPARATOR_PREFLIGHT_COMMAND = (
    "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
    f"{SCRIPT_RELATIVE} --phase6y-degree-comparator-preflight --output "
    f"{PHASE6Y_DEGREE_COMPARATOR_PREFLIGHT_OUTPUT}"
)
PHASE6Y_DEGREE_ORDER3_RANK4_L1_0_FIT_COMMAND = (
    "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
    f"{SCRIPT_RELATIVE} --fit --preflight-json {PHASE6Y_DEGREE_COMPARATOR_PREFLIGHT_OUTPUT} "
    "--target-dimension 36 --fit-rank 4 --basis-order 3 --basis-num-elems 8 "
    "--training-sample-count 276000 --holdout-sample-count 65536 "
    "--audit-sample-count 65536 --seed 8608 --optimizer-batch-size 4096 "
    "--prefit-steps 0 --train-steps 512 --learning-rate 0.0003 "
    "--l1-weight 0.0 --l2-weight 0.00000001 --logz-anchor-weight 0.0 "
    "--max-seconds 7200 --memory-cap-mib 12288 --adaptive-training "
    "--validation-check-every 16 --plateau-patience 4 "
    "--plateau-min-delta 0.000001 --lr-reduction-factor 0.5 "
    "--min-learning-rate 0.000001 --early-stop-after-lr-drops 4 "
    "--serialize-trained-cores --train-prior-seed 8303 "
    "--train-process-seed 8403 --holdout-prior-seed 9303 "
    "--holdout-process-seed 9403 --audit-prior-seed 9313 "
    "--audit-process-seed 9503 --output "
    f"{PHASE6Y_DEGREE_ORDER3_RANK4_L1_0_OUTPUT}"
)
P88_PHASE2_DEGREE_COMPARATOR_PREFLIGHT_COMMAND = (
    "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
    f"{SCRIPT_RELATIVE} --p88-phase2-degree-comparator-preflight --output "
    f"{P88_PHASE2_DEGREE_COMPARATOR_PREFLIGHT_OUTPUT}"
)
P88_PHASE2_DEGREE_ORDER3_RANK4_L1_0_FIT_COMMAND = (
    "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
    f"{SCRIPT_RELATIVE} --fit --preflight-json {P88_PHASE2_DEGREE_COMPARATOR_PREFLIGHT_OUTPUT} "
    "--target-dimension 36 --fit-rank 4 --basis-order 3 --basis-num-elems 8 "
    "--training-sample-count 276000 --holdout-sample-count 65536 "
    "--audit-sample-count 65536 --seed 8608 --optimizer-batch-size 4096 "
    "--prefit-steps 0 --train-steps 512 --learning-rate 0.0003 "
    "--l1-weight 0.0 --l2-weight 0.00000001 --logz-anchor-weight 0.0 "
    "--max-seconds 7200 --memory-cap-mib 12288 --adaptive-training "
    "--validation-check-every 16 --plateau-patience 4 "
    "--plateau-min-delta 0.000001 --lr-reduction-factor 0.5 "
    "--min-learning-rate 0.000001 --early-stop-after-lr-drops 4 "
    "--serialize-trained-cores --train-prior-seed 8303 "
    "--train-process-seed 8403 --holdout-prior-seed 9303 "
    "--holdout-process-seed 9403 --audit-prior-seed 9313 "
    "--audit-process-seed 9503 --output "
    f"{P88_PHASE2_DEGREE_ORDER3_RANK4_L1_0_OUTPUT}"
)
STATUS_PREFLIGHT_READY = "P86_PHASE5_BUDGET_FIT_PREFLIGHT_READY_NOT_FIT"
STATUS_PHASE6_RANK_PREFLIGHT_READY = "P86_PHASE6_RANK_CONVERGENCE_PREFLIGHT_READY_NOT_FIT"
STATUS_PHASE6S_ADAPTIVE_RANK5_PREFLIGHT_READY = (
    "P86_PHASE6S_ADAPTIVE_RANK5_PREFLIGHT_READY_NOT_FIT"
)
STATUS_PHASE6T_L1_TUNING_PREFLIGHT_READY = (
    "P86_PHASE6T_L1_REGULARIZATION_TUNING_PREFLIGHT_READY_NOT_FIT"
)
STATUS_PHASE6V_L1_SELECTION_PREFLIGHT_READY = (
    "P86_PHASE6V_L1_SELECTION_PREFLIGHT_READY_NOT_FIT"
)
STATUS_PHASE6W_SAME_POLICY_RANK_PREFLIGHT_READY = (
    "P86_PHASE6W_SAME_POLICY_RANK_CONVERGENCE_PREFLIGHT_READY_NOT_FIT"
)
STATUS_PHASE6Y_DEGREE_COMPARATOR_PREFLIGHT_READY = (
    "P86_PHASE6Y_DEGREE_COMPARATOR_PREFLIGHT_READY_NOT_FIT"
)
STATUS_P88_PHASE2_DEGREE_COMPARATOR_PREFLIGHT_READY = (
    "P88_PHASE2_DEGREE_COMPARATOR_PREFLIGHT_READY_NOT_FIT"
)
STATUS_FIT_BLOCKED = "BLOCK_P86_PHASE5_FIT_REQUIRES_EXACT_APPROVAL_GATE"
STATUS_TRAINING_BASE_COMPLETED = "P86_PHASE5_BUDGET_COMPLIANT_TRAINING_BASE_COMPLETED"
STATUS_TRAINING_BASE_BLOCKED = "BLOCK_P86_PHASE5_BUDGET_COMPLIANT_TRAINING_BASE"
STATUS_PHASE6_RANK5_COMPLETED = "P86_PHASE6_RANK5_COMPARATOR_TRAINING_BASE_COMPLETED"
STATUS_PHASE6_RANK5_BLOCKED = "BLOCK_P86_PHASE6_RANK5_COMPARATOR_TRAINING_BASE"
STATUS_PHASE6S_ADAPTIVE_RANK5_COMPLETED = (
    "P86_PHASE6S_ADAPTIVE_RANK5_COMPARATOR_TRAINING_BASE_COMPLETED"
)
STATUS_PHASE6S_ADAPTIVE_RANK5_BLOCKED = (
    "BLOCK_P86_PHASE6S_ADAPTIVE_RANK5_COMPARATOR_TRAINING_BASE"
)
STATUS_PHASE6T_L1_TUNING_COMPLETED = (
    "P86_PHASE6T_L1_REGULARIZATION_TUNING_DIAGNOSTIC_TRAINING_BASE_COMPLETED"
)
STATUS_PHASE6T_L1_TUNING_BLOCKED = (
    "BLOCK_P86_PHASE6T_L1_REGULARIZATION_TUNING_DIAGNOSTIC_TRAINING_BASE"
)
STATUS_PHASE6V_L1_SELECTION_COMPLETED = (
    "P86_PHASE6V_L1_SELECTION_CANDIDATE_TRAINING_BASE_COMPLETED"
)
STATUS_PHASE6V_L1_SELECTION_BLOCKED = (
    "BLOCK_P86_PHASE6V_L1_SELECTION_CANDIDATE_TRAINING_BASE"
)
STATUS_PHASE6W_RANK4_SAME_POLICY_COMPLETED = (
    "P86_PHASE6W_RANK4_SAME_POLICY_CANDIDATE_TRAINING_BASE_COMPLETED"
)
STATUS_PHASE6W_RANK4_SAME_POLICY_BLOCKED = (
    "BLOCK_P86_PHASE6W_RANK4_SAME_POLICY_CANDIDATE_TRAINING_BASE"
)
STATUS_PHASE6Y_DEGREE_ORDER3_COMPLETED = (
    "P86_PHASE6Y_DEGREE_ORDER3_RANK4_CANDIDATE_TRAINING_BASE_COMPLETED"
)
STATUS_PHASE6Y_DEGREE_ORDER3_BLOCKED = (
    "BLOCK_P86_PHASE6Y_DEGREE_ORDER3_RANK4_CANDIDATE_TRAINING_BASE"
)
STATUS_P88_PHASE2_DEGREE_ORDER3_COMPLETED = (
    "P88_PHASE2_DEGREE_ORDER3_RANK4_CANDIDATE_TRAINING_BASE_COMPLETED"
)
STATUS_P88_PHASE2_DEGREE_ORDER3_BLOCKED = (
    "BLOCK_P88_PHASE2_DEGREE_ORDER3_RANK4_CANDIDATE_TRAINING_BASE"
)
STATUS_TRAINING_BASE_SMOKE_COMPLETED = "P86_PHASE5_TRAINING_BASE_RETRY_SMOKE_COMPLETED"
STATUS_TRAINING_BASE_SMOKE_BLOCKED = "BLOCK_P86_PHASE5_TRAINING_BASE_RETRY_SMOKE"
STATUS_PHASE6R_ADAPTIVE_SMOKE_COMPLETED = "P86_PHASE6R_ADAPTIVE_TRAINING_SMOKE_COMPLETED"
STATUS_PHASE6R_ADAPTIVE_SMOKE_BLOCKED = "BLOCK_P86_PHASE6R_ADAPTIVE_TRAINING_SMOKE"
COMMON_NONCLAIMS = (
    "ALS training is historical and stale for fixed-variant Zhao-Cui",
    "training-base optimizer wiring is fixed_hmc_adaptation/extension mechanics, not a source-faithful author TT-cross proof",
    "no author SIR fit quality claim",
    "no rank convergence claim",
    "no posterior correctness claim",
    "no KR closure claim",
    "no HMC readiness claim",
    "no LEDH comparison claim",
    "no d50 or d100 scale claim",
    "no production readiness claim",
)
PREFLIGHT_NONCLAIMS = (
    "no Phase 5 training-base fit has been run by this preflight",
) + COMMON_NONCLAIMS
FIT_NONCLAIMS = (
    "Phase 5 budget-compliant training-base fit admission does not close later P86 gates",
) + COMMON_NONCLAIMS
PHASE6_PREFLIGHT_NONCLAIMS = (
    "Phase 6 rank preflight does not run the comparator fit",
    "rank-5 comparator fit requires exact Claude-agreed command handoff before execution",
    "degree convergence remains blocked pending a reviewed configurable-basis path",
    "rank convergence cannot be claimed from preflight or from fit residuals alone",
) + COMMON_NONCLAIMS
PHASE6_FIT_NONCLAIMS = (
    "Phase 6 rank-5 comparator fit does not by itself close rank convergence",
    "rank convergence interpretation requires a reviewed convergence ledger",
    "degree convergence remains blocked pending a reviewed configurable-basis path",
) + COMMON_NONCLAIMS
PHASE6S_PREFLIGHT_NONCLAIMS = (
    "Phase 6S adaptive rank-5 preflight does not run the comparator fit",
    "adaptive rank-5 comparator fit requires exact Claude-agreed command handoff before execution",
    "validation holdout may drive scheduler/veto decisions but is not production evidence",
    "audit cloud remains reserved and not used for tuning",
    "rank convergence cannot be claimed from preflight or from validation loss alone",
) + COMMON_NONCLAIMS
PHASE6S_FIT_NONCLAIMS = (
    "Phase 6S adaptive rank-5 comparator fit does not by itself close rank convergence",
    "rank convergence interpretation requires a reviewed convergence ledger",
    "validation holdout may drive scheduler/veto decisions but is not production evidence",
    "audit cloud remains reserved and not used for tuning",
    "degree convergence remains blocked pending a reviewed configurable-basis path",
) + COMMON_NONCLAIMS
PHASE6T_PREFLIGHT_NONCLAIMS = (
    "Phase 6T L1 regularization preflight does not run the tuning diagnostic",
    "regularization tuning diagnostic requires exact Claude-agreed command handoff before execution",
    "validation holdout may tune/veto only inside the reviewed protocol",
    "audit cloud remains reserved and not used for tuning",
    "L1 regularization controls do not by themselves establish rank convergence",
) + COMMON_NONCLAIMS
PHASE6T_FIT_NONCLAIMS = (
    "Phase 6T L1 regularization diagnostic does not by itself close rank convergence",
    "regularization tuning requires a reviewed selection/convergence ledger",
    "validation holdout may tune/veto only inside the reviewed protocol",
    "audit cloud remains reserved and not used for tuning",
    "degree convergence remains blocked pending a reviewed configurable-basis path",
) + COMMON_NONCLAIMS
PHASE6V_PREFLIGHT_NONCLAIMS = (
    "Phase 6V L1 selection preflight does not run any fitting command",
    "Phase 6V fitting arms require exact Claude-agreed command handoff before execution",
    "validation holdout may select or veto L1 candidates only inside the reviewed protocol",
    "audit cloud remains reserved and not used for tuning",
    "L1 selection does not by itself establish rank convergence",
    "Phase 7 remains blocked until a later reviewed same-policy rank/degree convergence gate",
) + COMMON_NONCLAIMS
PHASE6V_FIT_NONCLAIMS = (
    "Phase 6V L1 selection candidate does not by itself close rank convergence",
    "selection interpretation requires a reviewed convergence ledger",
    "validation holdout may select or veto L1 candidates only inside the reviewed protocol",
    "audit cloud remains reserved and not used for tuning",
    "degree convergence remains blocked pending a reviewed configurable-basis path",
) + COMMON_NONCLAIMS
PHASE6W_PREFLIGHT_NONCLAIMS = (
    "Phase 6W same-policy rank preflight does not run any fitting command",
    "Phase 6W rank-4 fitting arms require exact Claude-agreed command handoff before execution",
    "Phase 5 rank-4 is historical context only, not a same-policy lower rung",
    "validation holdout may select or veto L1 candidates only inside the reviewed protocol",
    "audit cloud remains reserved and not used for tuning",
    "Phase 7 remains blocked until same-policy rank and degree gates are reviewed",
) + COMMON_NONCLAIMS
PHASE6W_FIT_NONCLAIMS = (
    "Phase 6W rank-4 same-policy candidate does not by itself close rank convergence",
    "rank convergence interpretation requires a reviewed same-policy convergence ledger",
    "validation holdout may select or veto L1 candidates only inside the reviewed protocol",
    "audit cloud remains reserved and not used for tuning",
    "degree convergence remains blocked pending a reviewed configurable-basis path",
) + COMMON_NONCLAIMS
PHASE6Y_PREFLIGHT_NONCLAIMS = (
    "Phase 6Y degree-comparator preflight does not run any fitting command",
    "Phase 6Y order-3 degree comparator requires exact Claude-agreed command handoff before execution",
    "non-default Lagrangep bases are extension_or_invention comparators, not source-faithful author defaults",
    "validation holdout may select or veto degree candidates only inside a later reviewed protocol",
    "audit cloud remains reserved and not used for tuning",
    "Phase 7 remains blocked until degree convergence is reviewed or owner-reframed",
) + COMMON_NONCLAIMS
PHASE6Y_FIT_NONCLAIMS = (
    "Phase 6Y order-3 degree candidate does not by itself close degree convergence",
    "degree convergence interpretation requires a reviewed convergence ledger",
    "non-default Lagrangep bases are extension_or_invention comparators, not source-faithful author defaults",
    "validation holdout may select or veto degree candidates only inside a later reviewed protocol",
    "audit cloud remains reserved and not used for tuning",
    "Phase 7 remains blocked until degree convergence is reviewed or owner-reframed",
) + COMMON_NONCLAIMS
SMOKE_NONCLAIMS = (
    "training-base retry smoke is not a Phase 5 budget-compliant fit",
    "training-base retry smoke does not close rank or production gates",
) + COMMON_NONCLAIMS
SOURCE_ANCHORS = (
    "third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m:43-55",
    "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:64-98",
    "third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/Domains/AlgebraicMapping.m:5-43",
    "third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/SIRT.m:51-67",
    "third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/Polynomials/Lagrangep.m:12-52",
    "docs/plans/bayesfilter-highdim-zhao-cui-p83-phase6-fitting-budget-design-result-2026-06-22.md:117-159",
    "docs/plans/bayesfilter-highdim-zhao-cui-p86-phase2-algebraic-measure-contract-result-2026-06-24.md:54-71",
)


def _fit_status_succeeded(status: str) -> bool:
    return status in {
        STATUS_TRAINING_BASE_COMPLETED,
        STATUS_PHASE6_RANK5_COMPLETED,
        STATUS_PHASE6S_ADAPTIVE_RANK5_COMPLETED,
        STATUS_PHASE6T_L1_TUNING_COMPLETED,
        STATUS_PHASE6V_L1_SELECTION_COMPLETED,
        STATUS_PHASE6W_RANK4_SAME_POLICY_COMPLETED,
        STATUS_PHASE6Y_DEGREE_ORDER3_COMPLETED,
        STATUS_P88_PHASE2_DEGREE_ORDER3_COMPLETED,
    }


def _training_protocol_defaults() -> Mapping[str, Any]:
    return {
        "adaptive_training": DEFAULT_ADAPTIVE_TRAINING,
        "validation_check_every": DEFAULT_VALIDATION_CHECK_EVERY,
        "plateau_patience": DEFAULT_PLATEAU_PATIENCE,
        "plateau_min_delta": DEFAULT_PLATEAU_MIN_DELTA,
        "lr_reduction_factor": DEFAULT_LR_REDUCTION_FACTOR,
        "min_learning_rate": DEFAULT_MIN_LEARNING_RATE,
        "early_stop_after_lr_drops": DEFAULT_EARLY_STOP_AFTER_LR_DROPS,
        "serialize_trained_cores": DEFAULT_SERIALIZE_TRAINED_CORES,
        "l1_weight": DEFAULT_L1_WEIGHT,
        "l2_weight": DEFAULT_L2_WEIGHT,
        "logz_anchor_weight": DEFAULT_LOGZ_ANCHOR_WEIGHT,
    }


def _finite_nonnegative_float(value: float) -> bool:
    return math.isfinite(float(value)) and float(value) >= 0.0


def _zhao_cui_regularization_default_policy() -> Mapping[str, Any]:
    return {
        "schema_version": "p86_zhao_cui_regularization_default_policy.v1",
        "policy": ZHAO_CUI_L1_TUNING_DEFAULT_POLICY,
        "owner_directive": (
            "L1 regularization with L1 weight tuning is the default "
            "Zhao-Cui training-base procedure going forward."
        ),
        "scope": "zhao_cui_training_base_route_only_not_global_p75_default",
        "global_p75_l1_scalar_default": DEFAULT_L1_WEIGHT,
        "default_procedure": "tune_l1_weight_under_reviewed_validation_audit_split",
        "allowed_l1_comparator_arm": 0.0,
        "candidate_l1_grid": (0.0, 1e-10, 3e-10, 1e-9, 3e-9, 1e-8),
        "candidate_learning_rate_grid": (1e-4, 3e-4),
        "validation_holdout_role": "candidate_selection_and_veto_not_audit_not_production",
        "audit_cloud_role": "reserved_final_only_not_tuning",
        "selection_status": ZHAO_CUI_L1_TUNING_SELECTION_STATUS,
        "phase6t_diagnostic_status": "promising_single_diagnostic_not_final_selection",
        "historical_als_training_status": HISTORICAL_ALS_TRAINING_STATUS,
        "nonclaims": (
            "no universal L1 scalar selected",
            "no rank convergence claim",
            "no production readiness claim",
            "no source-faithful TT-cross training claim",
        ),
    }


def _jsonable(value: Any) -> Any:
    if hasattr(value, "numpy"):
        return _jsonable(value.numpy())
    if isinstance(value, Mapping):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, float):
        if math.isnan(value):
            return "nan"
        if math.isinf(value):
            return "inf" if value > 0 else "-inf"
        return value
    if isinstance(value, (str, int, bool)) or value is None:
        return value
    try:
        return float(value)
    except (TypeError, ValueError):
        return str(value)


def _write_payload(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_jsonable(payload), indent=2, sort_keys=True) + "\n")


def _git_state_summary() -> Mapping[str, Any]:
    try:
        head = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO_ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        porcelain = subprocess.check_output(
            ["git", "status", "--short"],
            cwd=REPO_ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).splitlines()
        return {
            "head": head,
            "dirty": bool(porcelain),
            "status_short_count": len(porcelain),
        }
    except (OSError, subprocess.CalledProcessError) as exc:
        return {
            "head": "unknown",
            "dirty": "unknown",
            "status_error": str(exc),
        }


def _convention() -> MeasureConvention:
    return MeasureConvention(
        density_measure=DensityMeasure.REFERENCE_MEASURE,
        mass_measure=MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )


def _rank_tuple(dimension: int, fit_rank: int) -> tuple[int, ...]:
    return (1, *([int(fit_rank)] * (int(dimension) - 1)), 1)


def _parameter_count(
    basis_dim_tuple: Sequence[int],
    ranks: Sequence[int],
) -> int:
    return sum(
        int(ranks[axis]) * int(basis_dim_tuple[axis]) * int(ranks[axis + 1])
        for axis in range(len(basis_dim_tuple))
    )


def _core_column_counts(
    basis_dim_tuple: Sequence[int],
    ranks: Sequence[int],
) -> tuple[int, ...]:
    return tuple(
        int(ranks[axis]) * int(basis_dim_tuple[axis]) * int(ranks[axis + 1])
        for axis in range(len(basis_dim_tuple))
    )


def _memory_forecast(
    *,
    training_sample_count: int,
    holdout_sample_count: int,
    optimizer_batch_size: int,
    target_dimension: int,
    basis_dim_tuple: Sequence[int],
    ranks: Sequence[int],
    memory_cap_mib: int,
) -> Mapping[str, Any]:
    dtype_bytes = 8
    n = min(int(training_sample_count), int(optimizer_batch_size))
    core_cols = _core_column_counts(basis_dim_tuple, ranks)
    max_cols = max(core_cols)
    point_batch_bytes = n * int(target_dimension) * dtype_bytes
    max_basis_eval_bytes = n * max(int(dim) for dim in basis_dim_tuple) * dtype_bytes
    max_core_matrix_batch_bytes = (
        n * max(int(ranks[axis]) * int(ranks[axis + 1]) for axis in range(int(target_dimension))) * dtype_bytes
    )
    sample_target_weight_bytes = n * 3 * dtype_bytes
    persistent_cloud_bytes = (
        (int(training_sample_count) + int(holdout_sample_count))
        * (int(target_dimension) + 2)
        * dtype_bytes
    )
    parameter_bytes = _parameter_count(basis_dim_tuple, ranks) * dtype_bytes
    adam_slot_bytes = 2 * parameter_bytes
    fixed_overhead_bytes = 1 * 1024**3
    planned_peak_bytes = (
        point_batch_bytes
        + max_basis_eval_bytes
        + max_core_matrix_batch_bytes
        + sample_target_weight_bytes
        + persistent_cloud_bytes
        + parameter_bytes
        + adam_slot_bytes
        + fixed_overhead_bytes
    )
    memory_cap_bytes = int(memory_cap_mib) * 1024**2
    return {
        "memory_model": "p86_phase5_training_base_optimizer_batch_memory_model_v1",
        "dtype_bytes": dtype_bytes,
        "optimizer_batch_size": int(optimizer_batch_size),
        "active_batch_size": n,
        "max_core_columns": max_cols,
        "point_batch_bytes": point_batch_bytes,
        "max_basis_eval_bytes": max_basis_eval_bytes,
        "max_core_matrix_batch_bytes": max_core_matrix_batch_bytes,
        "sample_target_weight_bytes": sample_target_weight_bytes,
        "persistent_cloud_bytes": persistent_cloud_bytes,
        "parameter_bytes": parameter_bytes,
        "adam_slot_bytes": adam_slot_bytes,
        "fixed_overhead_bytes": fixed_overhead_bytes,
        "planned_peak_bytes": planned_peak_bytes,
        "planned_peak_mib": planned_peak_bytes / 1024**2,
        "memory_cap_mib": int(memory_cap_mib),
        "memory_cap_bytes": memory_cap_bytes,
        "planned_under_cap": planned_peak_bytes <= memory_cap_bytes,
        "diagnostic_source": "resource.getrusage(RUSAGE_SELF).ru_maxrss in training-base runner; preflight uses static optimizer-batch model only",
    }


def _peak_memory_mib() -> float:
    usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    # Linux reports ru_maxrss in KiB.
    return float(usage) / 1024.0


def _cloud_manifest(
    *,
    training_sample_count: int,
    holdout_sample_count: int,
    audit_sample_count: int,
    label_prefix: str = "p86-phase5",
    train_prior_seed: int = DEFAULT_TRAIN_PRIOR_SEED,
    train_process_seed: int = DEFAULT_TRAIN_PROCESS_SEED,
    holdout_prior_seed: int = DEFAULT_HOLDOUT_PRIOR_SEED,
    holdout_process_seed: int = DEFAULT_HOLDOUT_PROCESS_SEED,
    audit_prior_seed: int = DEFAULT_AUDIT_PRIOR_SEED,
    audit_process_seed: int = DEFAULT_AUDIT_PROCESS_SEED,
) -> tuple[Mapping[str, Any], ...]:
    return (
        {
            "role": "training",
            "cloud_label": (
                f"{label_prefix}-train-source-push-t1-prior{train_prior_seed}"
                f"-process{train_process_seed}"
            ),
            "sample_count": int(training_sample_count),
            "prior_seed": int(train_prior_seed),
            "process_noise_seed": int(train_process_seed),
            "may_fit_or_tune": True,
            "may_veto": True,
            "author_route_coordinate_policy": "unclipped_author_algebraic_input_coordinates",
        },
        {
            "role": "validation_holdout",
            "cloud_label": (
                f"{label_prefix}-holdout-source-push-t1-prior{holdout_prior_seed}"
                f"-process{holdout_process_seed}"
            ),
            "sample_count": int(holdout_sample_count),
            "prior_seed": int(holdout_prior_seed),
            "process_noise_seed": int(holdout_process_seed),
            "may_fit_or_tune": False,
            "may_veto": True,
            "author_route_coordinate_policy": "reuse_training_frame_and_shift_unclipped_author_algebraic_input_coordinates",
        },
        {
            "role": "audit_reserved_not_used_for_phase5_tuning",
            "cloud_label": (
                f"{label_prefix}-audit-reserved-source-push-t1-prior{audit_prior_seed}"
                f"-process{audit_process_seed}"
            ),
            "sample_count": int(audit_sample_count),
            "prior_seed": int(audit_prior_seed),
            "process_noise_seed": int(audit_process_seed),
            "may_fit_or_tune": False,
            "may_veto": False,
            "reserved_for": "later final-only audit after separate approval",
        },
    )


def _cloud_separation_status(clouds: Sequence[Mapping[str, Any]]) -> str:
    labels = [str(cloud["cloud_label"]) for cloud in clouds]
    seed_pairs = [
        (cloud.get("prior_seed"), cloud.get("process_noise_seed"))
        for cloud in clouds
        if cloud.get("prior_seed") is not None
    ]
    audit_used_for_tuning = any(
        str(cloud["role"]).startswith("audit") and bool(cloud.get("may_fit_or_tune"))
        for cloud in clouds
    )
    return (
        "ok"
        if len(labels) == len(set(labels))
        and len(seed_pairs) == len(set(seed_pairs))
        and not audit_used_for_tuning
        else "block"
    )


def _route_payload(target_dimension: int) -> Mapping[str, Any]:
    return _route_payload_with_basis(
        target_dimension=target_dimension,
        order=P85_AUTHOR_SIR_LAGRANGEP_ORDER,
        num_elems=P85_AUTHOR_SIR_LAGRANGEP_NUM_ELEMS,
    )


def _route_payload_with_basis(
    *,
    target_dimension: int,
    order: int,
    num_elems: int,
) -> Mapping[str, Any]:
    spec = p85_author_sir_lagrangep_algebraic_product_basis_spec(
        dimension=int(target_dimension),
        convention=_convention(),
        order=int(order),
        num_elems=int(num_elems),
    )
    payload = spec.manifest_payload()
    axis_specs = payload["axis_specs"]
    is_author_default = (
        int(order) == P85_AUTHOR_SIR_LAGRANGEP_ORDER
        and int(num_elems) == P85_AUTHOR_SIR_LAGRANGEP_NUM_ELEMS
    )
    return {
        "target_id": "zhao_cui_sir_austria_d18",
        "route_class": "fixed_ttsirt_source_route",
        "route_status": (
            "hard_wired_author_lagrangep_algebraic"
            if is_author_default
            else "setup_static_degree_comparator_lagrangep_algebraic"
        ),
        "target_dimension": int(target_dimension),
        "basis_family": "lagrangep",
        "basis_order": int(order),
        "basis_num_elems": int(num_elems),
        "basis_dim_per_dimension": int(num_elems) * int(order) + 1,
        "basis_dim_tuple": payload["basis_dim_tuple"],
        "domain_map": "algebraic",
        "domain_scale": 1.0,
        "density_measure": DensityMeasure.REFERENCE_MEASURE.value,
        "mass_measure": MassMeasure.REFERENCE_MEASURE.value,
        "route_changing_cli": False,
        "source_anchors": payload["source_anchors"],
        "basis_domain_axis0": axis_specs[0],
        "classification": payload["classification"],
        "classification_subtype": payload["classification_subtype"],
        "xla_static_fields": payload["xla_static_fields"],
    }


def build_preflight_payload(
    *,
    output: Path = PREFLIGHT_OUTPUT,
    target_dimension: int = 36,
    fit_rank: int = 4,
    basis_order: int = P85_AUTHOR_SIR_LAGRANGEP_ORDER,
    basis_num_elems: int = P85_AUTHOR_SIR_LAGRANGEP_NUM_ELEMS,
    training_sample_count: int = 364320,
    holdout_sample_count: int = 65536,
    audit_sample_count: int = 65536,
    seed: int = 8605,
    optimizer_batch_size: int = DEFAULT_OPTIMIZER_BATCH_SIZE,
    prefit_steps: int = DEFAULT_PREFIT_STEPS,
    train_steps: int = DEFAULT_TRAIN_STEPS,
    learning_rate: float = DEFAULT_LEARNING_RATE,
    l1_weight: float = DEFAULT_L1_WEIGHT,
    l2_weight: float = DEFAULT_L2_WEIGHT,
    logz_anchor_weight: float = DEFAULT_LOGZ_ANCHOR_WEIGHT,
    max_seconds: int = 14400,
    memory_cap_mib: int = 12288,
    command: str = PREFLIGHT_COMMAND,
    candidate_fit_command: str = FIT_COMMAND,
    expected_output: Path = PREFLIGHT_OUTPUT,
    expected_fit_output: Path = FIT_OUTPUT,
    expected_p_theta: int = 18216,
    status_ready: str = STATUS_PREFLIGHT_READY,
    block_status: str = "BLOCK_P86_PHASE5_PREFLIGHT",
    schema_version: str = "p86_phase5_budget_compliant_fit_preflight.v1",
    phase_name: str = "P86 Phase 5 budget-compliant fit",
    phase_subplan: str = PHASE5_SUBPLAN,
    phase_result: str = PHASE5_RESULT,
    rank_rung: str = "author_basis_rung_F",
    label_prefix: str = "p86-phase5",
    train_prior_seed: int = DEFAULT_TRAIN_PRIOR_SEED,
    train_process_seed: int = DEFAULT_TRAIN_PROCESS_SEED,
    holdout_prior_seed: int = DEFAULT_HOLDOUT_PRIOR_SEED,
    holdout_process_seed: int = DEFAULT_HOLDOUT_PROCESS_SEED,
    audit_prior_seed: int = DEFAULT_AUDIT_PRIOR_SEED,
    audit_process_seed: int = DEFAULT_AUDIT_PROCESS_SEED,
    nonclaims: Sequence[str] = PREFLIGHT_NONCLAIMS,
    lower_rung_artifact: str | None = None,
    allow_explicit_nondefault_basis_preflight_command: bool = False,
) -> Mapping[str, Any]:
    route = _route_payload_with_basis(
        target_dimension=target_dimension,
        order=basis_order,
        num_elems=basis_num_elems,
    )
    ranks = _rank_tuple(target_dimension, fit_rank)
    p_theta = _parameter_count(route["basis_dim_tuple"], ranks)
    minimum_training_samples = max(20 * p_theta, 5000)
    sample_budget_status = (
        "ok" if int(training_sample_count) >= minimum_training_samples else "block"
    )
    clouds = _cloud_manifest(
        training_sample_count=training_sample_count,
        holdout_sample_count=holdout_sample_count,
        audit_sample_count=audit_sample_count,
        label_prefix=label_prefix,
        train_prior_seed=train_prior_seed,
        train_process_seed=train_process_seed,
        holdout_prior_seed=holdout_prior_seed,
        holdout_process_seed=holdout_process_seed,
        audit_prior_seed=audit_prior_seed,
        audit_process_seed=audit_process_seed,
    )
    memory = _memory_forecast(
        training_sample_count=training_sample_count,
        holdout_sample_count=holdout_sample_count,
        optimizer_batch_size=optimizer_batch_size,
        target_dimension=target_dimension,
        basis_dim_tuple=route["basis_dim_tuple"],
        ranks=ranks,
        memory_cap_mib=memory_cap_mib,
    )
    route_manifest_ok = (
        route["basis_family"] == "lagrangep"
        and route["domain_map"] == "algebraic"
        and float(route["domain_scale"]) == 1.0
        and not route["route_changing_cli"]
    )
    route_expected_dim = int(basis_num_elems) * int(basis_order) + 1
    route_expected_default = (
        int(basis_order) == P85_AUTHOR_SIR_LAGRANGEP_ORDER
        and int(basis_num_elems) == P85_AUTHOR_SIR_LAGRANGEP_NUM_ELEMS
    )
    route_manifest_ok = (
        route_manifest_ok
        and route["basis_order"] == int(basis_order)
        and route["basis_num_elems"] == int(basis_num_elems)
        and route["basis_dim_per_dimension"] == route_expected_dim
    )
    known_preflight_command_ok = command in (
        PREFLIGHT_COMMAND,
        PHASE6_RANK_PREFLIGHT_COMMAND,
        PHASE6S_RANK5_ADAPTIVE_PREFLIGHT_COMMAND,
        PHASE6T_L1_TUNING_PREFLIGHT_COMMAND,
        PHASE6V_L1_SELECTION_PREFLIGHT_COMMAND,
        PHASE6W_SAME_POLICY_RANK_PREFLIGHT_COMMAND,
        PHASE6Y_DEGREE_COMPARATOR_PREFLIGHT_COMMAND,
        P88_PHASE2_DEGREE_COMPARATOR_PREFLIGHT_COMMAND,
    )
    explicit_nondefault_basis_preflight_ok = (
        bool(allow_explicit_nondefault_basis_preflight_command)
        and not route_expected_default
        and SCRIPT_RELATIVE in command
        and "--fit" not in command
        and str(expected_output) in command
        and f"--basis-order {int(basis_order)}" in command
        and f"--basis-num-elems {int(basis_num_elems)}" in command
        and SCRIPT_RELATIVE in candidate_fit_command
        and f"--preflight-json {expected_output}" in candidate_fit_command
        and f"--basis-order {int(basis_order)}" in candidate_fit_command
        and f"--basis-num-elems {int(basis_num_elems)}" in candidate_fit_command
    )
    command_fidelity_ok = (
        str(expected_fit_output) in candidate_fit_command
        and str(expected_output) in candidate_fit_command
        and (known_preflight_command_ok or explicit_nondefault_basis_preflight_ok)
    )
    preflight_path_ok = Path(output) == expected_output
    fit_path_ok = str(expected_fit_output) in candidate_fit_command
    cloud_status = _cloud_separation_status(clouds)
    regularization_weights_ok = all(
        _finite_nonnegative_float(value)
        for value in (l1_weight, l2_weight, logz_anchor_weight)
    )
    status_fields = {
        "route_manifest_ok": route_manifest_ok,
        "basis_family": route["basis_family"],
        "basis_order": route["basis_order"],
        "basis_num_elems": route["basis_num_elems"],
        "domain_map": route["domain_map"],
        "domain_scale": route["domain_scale"],
        "basis_dim_per_dimension": route["basis_dim_per_dimension"],
        "basis_expected_dim_per_dimension": route_expected_dim,
        "basis_is_author_default": route_expected_default,
        "route_changing_cli": route["route_changing_cli"],
        "training_backend": TRAINING_BACKEND,
        "historical_als_training_status": HISTORICAL_ALS_TRAINING_STATUS,
        "parameter_count_status": "ok" if p_theta == int(expected_p_theta) else "block",
        "sample_budget_status": sample_budget_status,
        "sample_visit_budget_status": (
            "ok"
            if int(optimizer_batch_size) * int(train_steps)
            >= int(training_sample_count)
            else "block"
        ),
        "cloud_separation_status": cloud_status,
        "command_fidelity_status": "ok" if command_fidelity_ok else "block",
        "reserved_preflight_output_path_status": "ok" if preflight_path_ok else "block",
        "reserved_fit_output_path_status": "ok" if fit_path_ok else "block",
        "planned_runtime_envelope_status": "ok" if int(max_seconds) > 0 else "block",
        "planned_memory_envelope_status": "ok" if memory["planned_under_cap"] else "block",
        "memory_diagnostic_source_status": "ok",
        "regularization_weight_status": "ok" if regularization_weights_ok else "block",
    }
    preflight_ok = (
        route_manifest_ok
        and sample_budget_status == "ok"
        and status_fields["parameter_count_status"] == "ok"
        and status_fields["sample_visit_budget_status"] == "ok"
        and status_fields["cloud_separation_status"] == "ok"
        and status_fields["command_fidelity_status"] == "ok"
        and status_fields["reserved_preflight_output_path_status"] == "ok"
        and status_fields["reserved_fit_output_path_status"] == "ok"
        and status_fields["planned_runtime_envelope_status"] == "ok"
        and status_fields["planned_memory_envelope_status"] == "ok"
        and status_fields["memory_diagnostic_source_status"] == "ok"
        and status_fields["regularization_weight_status"] == "ok"
        and status_fields["training_backend"] == TRAINING_BACKEND
        and status_fields["historical_als_training_status"]
        == HISTORICAL_ALS_TRAINING_STATUS
    )
    return {
        "schema_version": schema_version,
        "status": status_ready if preflight_ok else block_status,
        "phase_name": phase_name,
        "preflight_only": True,
        "fit_executed": False,
        "script": SCRIPT_RELATIVE,
        "output": str(output),
        "command": command,
        "candidate_fit_command": candidate_fit_command,
        "requires_exact_claude_agreement_before_fit": True,
        "training_backend": TRAINING_BACKEND,
        "historical_als_training_status": HISTORICAL_ALS_TRAINING_STATUS,
        "phase_subplan": phase_subplan,
        "phase_result": phase_result,
        "phase5_subplan": PHASE5_SUBPLAN,
        "phase5_result": PHASE5_RESULT,
        "phase6_subplan": PHASE6_SUBPLAN,
        "lower_rung_artifact": lower_rung_artifact,
        "git": _git_state_summary(),
        "environment": {
            "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
            "intentional_gpu_hiding": os.environ.get("CUDA_VISIBLE_DEVICES") == "-1",
            "runtime_posture": "CPU-only/GPU-hidden non-production fit posture",
            "mplconfigdir": os.environ.get("MPLCONFIGDIR"),
            "python": sys.executable,
        },
        "route_manifest": route,
        "rank_budget": {
            "rung": rank_rung,
            "target_dimension": int(target_dimension),
            "fit_rank": int(fit_rank),
            "ranks": ranks,
            "P_theta": p_theta,
            "parameter_count_formula": "sum_axis ranks[axis] * basis_dim[axis] * ranks[axis + 1]",
            "minimum_training_samples_formula": "max(20 * P_theta, 5000)",
            "minimum_training_samples": minimum_training_samples,
            "training_sample_count": int(training_sample_count),
            "training_over_minimum": int(training_sample_count)
            - minimum_training_samples,
        },
        "basis_config": {
            "basis_order": int(basis_order),
            "basis_num_elems": int(basis_num_elems),
            "basis_expected_dim_per_dimension": route_expected_dim,
            "basis_is_author_default": route_expected_default,
        },
        "optimizer_budget": {
            "optimizer": "Adam",
            "training_backend": TRAINING_BACKEND,
            "optimizer_batch_size": int(optimizer_batch_size),
            "prefit_steps": int(prefit_steps),
            "train_steps": int(train_steps),
            "learning_rate": float(learning_rate),
            "minimum_training_sample_visits": int(training_sample_count),
            "planned_training_sample_visits": int(optimizer_batch_size) * int(train_steps),
            "sample_visit_budget_status": (
                "ok"
                if int(optimizer_batch_size) * int(train_steps)
                >= int(training_sample_count)
                else "block"
            ),
            "training_data_reuse_policy": "fixed training cloud cycled by deterministic contiguous optimizer batches",
        },
        "regularization_budget": {
            "l1_weight": float(l1_weight),
            "l2_weight": float(l2_weight),
            "logz_anchor_weight": float(logz_anchor_weight),
            "regularization_weight_status": (
                "ok" if regularization_weights_ok else "block"
            ),
            "regularization_route": "training_base_objective_penalty",
            "audit_tuning_status": "not_used_for_tuning",
        },
        "zhao_cui_regularization_default_policy": (
            _zhao_cui_regularization_default_policy()
        ),
        "clouds": clouds,
        "cloud_policy": {
            "cloud_separation_status": cloud_status,
            "audit_cloud_used_for_tuning": False,
            "replay_cloud_status": "not_used_in_preflight_candidate",
            "validation_holdout_tuning_status": "not_used_for_rank_or_threshold_tuning",
        },
        "runtime_envelope": {
            "max_seconds": int(max_seconds),
            "planned_runtime_envelope_status": status_fields["planned_runtime_envelope_status"],
            "runtime_diagnostic_source": "time.monotonic() wall time in fit runner",
        },
        "memory_envelope": memory,
        "seed": int(seed),
        "cloud_seed_policy": {
            "train_prior_seed": int(train_prior_seed),
            "train_process_seed": int(train_process_seed),
            "holdout_prior_seed": int(holdout_prior_seed),
            "holdout_process_seed": int(holdout_process_seed),
            "audit_prior_seed": int(audit_prior_seed),
            "audit_process_seed": int(audit_process_seed),
        },
        "source_anchors": SOURCE_ANCHORS,
        "author_coordinate_policy": {
            "status": "ok",
            "fit_input": "unclipped local samples_unweighted are mapped through AlgebraicMapping(1) to reference coordinates",
            "target_transform": "sqrt(exp(-(negative_log_physical - log_abs_det_L - sum log|dx/dz|)/2)) on reference coordinates",
            "forbidden_substitute": "legacy bounded Legendre or clipped bounded local coordinates",
            "source_anchor": (
                "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:90-98; "
                "third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/SIRT.m:51-67"
            ),
        },
        "core_status_fields": status_fields,
        "gate_summary": {
            "overall_status": "ready_for_exact_claude_agreed_execution" if preflight_ok else "block",
            **status_fields,
            "fit_executed": False,
            "nonclaims": tuple(nonclaims),
        },
        "nonclaims": tuple(nonclaims),
    }


def build_degree_comparator_preflight_payload(
    *,
    output: Path,
    target_dimension: int,
    fit_rank: int,
    basis_order: int,
    basis_num_elems: int,
    training_sample_count: int,
    holdout_sample_count: int,
    audit_sample_count: int,
    seed: int,
    optimizer_batch_size: int,
    prefit_steps: int,
    train_steps: int,
    learning_rate: float,
    l1_weight: float,
    l2_weight: float,
    logz_anchor_weight: float,
    max_seconds: int,
    memory_cap_mib: int,
    command: str,
    candidate_fit_command: str,
    expected_output: Path,
    expected_fit_output: Path,
    expected_p_theta: int,
    status_ready: str,
    block_status: str,
    schema_version: str,
    phase_name: str,
    phase_subplan: str,
    phase_result: str,
    rank_rung: str,
    label_prefix: str,
    train_prior_seed: int,
    train_process_seed: int,
    holdout_prior_seed: int,
    holdout_process_seed: int,
    audit_prior_seed: int,
    audit_process_seed: int,
    nonclaims: Sequence[str],
    lower_rung_artifact: str | None,
) -> Mapping[str, Any]:
    payload = build_preflight_payload(
        output=output,
        target_dimension=target_dimension,
        fit_rank=fit_rank,
        basis_order=basis_order,
        basis_num_elems=basis_num_elems,
        training_sample_count=training_sample_count,
        holdout_sample_count=holdout_sample_count,
        audit_sample_count=audit_sample_count,
        seed=seed,
        optimizer_batch_size=optimizer_batch_size,
        prefit_steps=prefit_steps,
        train_steps=train_steps,
        learning_rate=learning_rate,
        l1_weight=l1_weight,
        l2_weight=l2_weight,
        logz_anchor_weight=logz_anchor_weight,
        max_seconds=max_seconds,
        memory_cap_mib=memory_cap_mib,
        command=command,
        candidate_fit_command=candidate_fit_command,
        expected_output=expected_output,
        expected_fit_output=expected_fit_output,
        expected_p_theta=expected_p_theta,
        status_ready=status_ready,
        block_status=block_status,
        schema_version=schema_version,
        phase_name=phase_name,
        phase_subplan=phase_subplan,
        phase_result=phase_result,
        rank_rung=rank_rung,
        label_prefix=label_prefix,
        train_prior_seed=train_prior_seed,
        train_process_seed=train_process_seed,
        holdout_prior_seed=holdout_prior_seed,
        holdout_process_seed=holdout_process_seed,
        audit_prior_seed=audit_prior_seed,
        audit_process_seed=audit_process_seed,
        nonclaims=nonclaims,
        lower_rung_artifact=lower_rung_artifact,
        allow_explicit_nondefault_basis_preflight_command=True,
    )
    route = payload["route_manifest"]
    return {
        **payload,
        "route_manifest": route,
        "basis_config": {
            "basis_order": basis_order,
            "basis_num_elems": basis_num_elems,
            "basis_expected_dim_per_dimension": int(basis_num_elems) * int(basis_order) + 1,
            "basis_is_author_default": (
                int(basis_order) == P85_AUTHOR_SIR_LAGRANGEP_ORDER
                and int(basis_num_elems) == P85_AUTHOR_SIR_LAGRANGEP_NUM_ELEMS
            ),
            "degree_comparator_classification": (
                P85_AUTHOR_SIR_CLASSIFICATION
                if int(basis_order) == P85_AUTHOR_SIR_LAGRANGEP_ORDER
                and int(basis_num_elems) == P85_AUTHOR_SIR_LAGRANGEP_NUM_ELEMS
                else P85_AUTHOR_SIR_DEGREE_COMPARATOR_CLASSIFICATION
            ),
            "degree_comparator_subtype": (
                P85_AUTHOR_SIR_SUBTYPE
                if int(basis_order) == P85_AUTHOR_SIR_LAGRANGEP_ORDER
                and int(basis_num_elems) == P85_AUTHOR_SIR_LAGRANGEP_NUM_ELEMS
                else P85_AUTHOR_SIR_DEGREE_COMPARATOR_SUBTYPE
            ),
        },
    }


def validate_phase6y_default_order_reference_artifact(
    payload: Mapping[str, Any],
) -> Mapping[str, Any]:
    route = payload.get("route_manifest", {})
    rank_budget = payload.get("rank_budget", {})
    optimizer_budget = payload.get("optimizer_budget", {})
    statuses = payload.get("post_fit_statuses", {})
    training_protocol = payload.get("training_summary", {}).get(
        "training_protocol", {}
    )
    field_statuses = {
        "artifact_path": payload.get("output") == str(PHASE6W_RANK4_L1_0_OUTPUT),
        "status": payload.get("status") == STATUS_PHASE6W_RANK4_SAME_POLICY_COMPLETED,
        "training_backend": payload.get("training_backend") == TRAINING_BACKEND,
        "fit_rank": rank_budget.get("fit_rank") == PHASE6W_RANK4_FIT_RANK,
        "basis_family": route.get("basis_family") == "lagrangep",
        "basis_order": route.get("basis_order") == P85_AUTHOR_SIR_LAGRANGEP_ORDER,
        "basis_num_elems": (
            route.get("basis_num_elems") == P85_AUTHOR_SIR_LAGRANGEP_NUM_ELEMS
        ),
        "basis_classification": route.get("classification")
        == P85_AUTHOR_SIR_CLASSIFICATION,
        "domain_map": route.get("domain_map") == "algebraic",
        "domain_scale": float(route.get("domain_scale", math.nan)) == 1.0,
        "l1_weight": float(training_protocol.get("l1_weight", math.nan)) == 0.0,
        "learning_rate": (
            float(training_protocol.get("learning_rate", math.nan))
            if "learning_rate" in training_protocol
            else PHASE6W_RANK4_LEARNING_RATE
        )
        == PHASE6W_RANK4_LEARNING_RATE,
        "adaptive_training": training_protocol.get("adaptive_training") is True,
        "serialized_cores": payload.get("trained_core_serialization", {}).get(
            "status"
        )
        == "serialized_with_values",
        "finite_statuses": (
            statuses.get("finite_loss_status") == "ok"
            and statuses.get("finite_fit_residual_status") == "ok"
            and statuses.get("finite_holdout_residual_status") == "ok"
            and statuses.get("finite_normalizer_status") == "ok"
            and statuses.get("finite_sqrt_square_normalizer_status") == "ok"
            and statuses.get("fallback_route_status") == "not_used"
            and statuses.get("audit_cloud_tuning_status") == "not_used_for_tuning"
            and statuses.get("runtime_status") == "within_approved_envelope"
            and statuses.get("memory_status") == "within_approved_envelope"
        ),
        "optimizer_policy": (
            optimizer_budget.get("optimizer_batch_size")
            == DEFAULT_OPTIMIZER_BATCH_SIZE
            and optimizer_budget.get("train_steps") == PHASE6W_RANK4_TRAIN_STEPS
            and optimizer_budget.get("adaptive_training") is True
        ),
    }
    return {
        "status": "ok" if all(field_statuses.values()) else "block",
        "artifact": str(PHASE6W_RANK4_L1_0_OUTPUT),
        "validation_kind": "phase6w_selected_default_order_rank4_reference",
        "field_statuses": field_statuses,
        "reference_holdout_residual": payload.get("holdout_residual"),
        "reference_fit_residual": payload.get("fit_residual"),
    }


def _phase6y_degree_order3_candidate_arms(
    *,
    fit_output: Path = PHASE6Y_DEGREE_ORDER3_RANK4_L1_0_OUTPUT,
    fit_command: str = PHASE6Y_DEGREE_ORDER3_RANK4_L1_0_FIT_COMMAND,
) -> tuple[Mapping[str, Any], ...]:
    return (
        {
            "arm_id": "degree_order3_rank4_lr3e-4_l1_0",
            "role": "lower_degree_zero_l1_comparator",
            "basis_order": PHASE6Y_DEGREE_BASIS_ORDER,
            "basis_num_elems": PHASE6Y_DEGREE_BASIS_NUM_ELEMS,
            "basis_dim_per_dimension": PHASE6Y_DEGREE_BASIS_DIM,
            "l1_weight": PHASE6Y_DEGREE_L1_WEIGHT,
            "execution": "reserved_future_fit_requires_exact_claude_agreed_handoff",
            "output": str(fit_output),
            "candidate_fit_command": fit_command,
        },
    )


def _phase6y_degree_order3_fit_expectations() -> Mapping[Path, Mapping[str, Any]]:
    common = {
        "preflight_json": PHASE6Y_DEGREE_COMPARATOR_PREFLIGHT_OUTPUT,
        "target_dimension": 36,
        "fit_rank": PHASE6Y_DEGREE_FIT_RANK,
        "training_sample_count": PHASE6Y_DEGREE_TRAINING_SAMPLE_COUNT,
        "holdout_sample_count": 65536,
        "audit_sample_count": 65536,
        "seed": PHASE6Y_DEGREE_SEED,
        "optimizer_batch_size": DEFAULT_OPTIMIZER_BATCH_SIZE,
        "prefit_steps": DEFAULT_PREFIT_STEPS,
        "train_steps": PHASE6Y_DEGREE_TRAIN_STEPS,
        "learning_rate": PHASE6Y_DEGREE_LEARNING_RATE,
        "l1_weight": PHASE6Y_DEGREE_L1_WEIGHT,
        "l2_weight": PHASE6Y_DEGREE_L2_WEIGHT,
        "logz_anchor_weight": PHASE6Y_DEGREE_LOGZ_ANCHOR_WEIGHT,
        "max_seconds": PHASE6Y_DEGREE_MAX_SECONDS,
        "memory_cap_mib": 12288,
        "train_prior_seed": PHASE6Y_DEGREE_TRAIN_PRIOR_SEED,
        "train_process_seed": PHASE6Y_DEGREE_TRAIN_PROCESS_SEED,
        "holdout_prior_seed": PHASE6Y_DEGREE_HOLDOUT_PRIOR_SEED,
        "holdout_process_seed": PHASE6Y_DEGREE_HOLDOUT_PROCESS_SEED,
        "audit_prior_seed": PHASE6Y_DEGREE_AUDIT_PRIOR_SEED,
        "audit_process_seed": PHASE6Y_DEGREE_AUDIT_PROCESS_SEED,
        "adaptive_training": True,
        "validation_check_every": PHASE6S_RANK5_ADAPTIVE_VALIDATION_CHECK_EVERY,
        "plateau_patience": PHASE6S_RANK5_ADAPTIVE_PLATEAU_PATIENCE,
        "plateau_min_delta": PHASE6S_RANK5_ADAPTIVE_PLATEAU_MIN_DELTA,
        "lr_reduction_factor": DEFAULT_LR_REDUCTION_FACTOR,
        "min_learning_rate": DEFAULT_MIN_LEARNING_RATE,
        "early_stop_after_lr_drops": PHASE6S_RANK5_ADAPTIVE_EARLY_STOP_AFTER_LR_DROPS,
        "serialize_trained_cores": True,
        "basis_order": PHASE6Y_DEGREE_BASIS_ORDER,
        "basis_num_elems": PHASE6Y_DEGREE_BASIS_NUM_ELEMS,
    }
    return {
        PHASE6Y_DEGREE_ORDER3_RANK4_L1_0_OUTPUT: {
            **common,
            "preflight_json": PHASE6Y_DEGREE_COMPARATOR_PREFLIGHT_OUTPUT,
            "output": PHASE6Y_DEGREE_ORDER3_RANK4_L1_0_OUTPUT,
            "candidate_fit_command": PHASE6Y_DEGREE_ORDER3_RANK4_L1_0_FIT_COMMAND,
        },
        P88_PHASE2_DEGREE_ORDER3_RANK4_L1_0_OUTPUT: {
            **common,
            "preflight_json": P88_PHASE2_DEGREE_COMPARATOR_PREFLIGHT_OUTPUT,
            "output": P88_PHASE2_DEGREE_ORDER3_RANK4_L1_0_OUTPUT,
            "candidate_fit_command": P88_PHASE2_DEGREE_ORDER3_RANK4_L1_0_FIT_COMMAND,
        },
    }


def _build_degree_order3_comparator_preflight_payload(
    *,
    output: Path,
    preflight_output: Path,
    fit_output: Path,
    preflight_command: str,
    fit_command: str,
    status_ready: str,
    block_status: str,
    schema_version: str,
    phase_name: str,
    phase_subplan: str,
    phase_result: str,
    label_prefix: str,
    path_status_suffix: str,
) -> Mapping[str, Any]:
    reference_path = Path(PHASE6W_RANK4_L1_0_OUTPUT)
    reference = json.loads(reference_path.read_text())
    reference_validation = validate_phase6y_default_order_reference_artifact(
        reference
    )
    payload = build_degree_comparator_preflight_payload(
        output=output,
        target_dimension=36,
        fit_rank=PHASE6Y_DEGREE_FIT_RANK,
        basis_order=PHASE6Y_DEGREE_BASIS_ORDER,
        basis_num_elems=PHASE6Y_DEGREE_BASIS_NUM_ELEMS,
        training_sample_count=PHASE6Y_DEGREE_TRAINING_SAMPLE_COUNT,
        holdout_sample_count=65536,
        audit_sample_count=65536,
        seed=PHASE6Y_DEGREE_SEED,
        optimizer_batch_size=DEFAULT_OPTIMIZER_BATCH_SIZE,
        prefit_steps=DEFAULT_PREFIT_STEPS,
        train_steps=PHASE6Y_DEGREE_TRAIN_STEPS,
        learning_rate=PHASE6Y_DEGREE_LEARNING_RATE,
        l1_weight=PHASE6Y_DEGREE_L1_WEIGHT,
        l2_weight=PHASE6Y_DEGREE_L2_WEIGHT,
        logz_anchor_weight=PHASE6Y_DEGREE_LOGZ_ANCHOR_WEIGHT,
        max_seconds=PHASE6Y_DEGREE_MAX_SECONDS,
        memory_cap_mib=12288,
        command=preflight_command,
        candidate_fit_command=fit_command,
        expected_output=preflight_output,
        expected_fit_output=fit_output,
        expected_p_theta=PHASE6Y_DEGREE_P_THETA,
        status_ready=status_ready,
        block_status=block_status,
        schema_version=schema_version,
        phase_name=phase_name,
        phase_subplan=phase_subplan,
        phase_result=phase_result,
        rank_rung="author_basis_rung_F_rank4_degree_order3_comparator",
        label_prefix=label_prefix,
        train_prior_seed=PHASE6Y_DEGREE_TRAIN_PRIOR_SEED,
        train_process_seed=PHASE6Y_DEGREE_TRAIN_PROCESS_SEED,
        holdout_prior_seed=PHASE6Y_DEGREE_HOLDOUT_PRIOR_SEED,
        holdout_process_seed=PHASE6Y_DEGREE_HOLDOUT_PROCESS_SEED,
        audit_prior_seed=PHASE6Y_DEGREE_AUDIT_PRIOR_SEED,
        audit_process_seed=PHASE6Y_DEGREE_AUDIT_PROCESS_SEED,
        nonclaims=PHASE6Y_PREFLIGHT_NONCLAIMS,
        lower_rung_artifact=str(reference_path),
    )
    candidate_arms = _phase6y_degree_order3_candidate_arms(
        fit_output=fit_output,
        fit_command=fit_command,
    )
    adaptive_protocol = {
        "adaptive_training": True,
        "optimizer_identity": TRAINING_BACKEND,
        "optimizer": "Adam",
        "validation_check_every": PHASE6S_RANK5_ADAPTIVE_VALIDATION_CHECK_EVERY,
        "plateau_patience": PHASE6S_RANK5_ADAPTIVE_PLATEAU_PATIENCE,
        "plateau_min_delta": PHASE6S_RANK5_ADAPTIVE_PLATEAU_MIN_DELTA,
        "lr_reduction_factor": DEFAULT_LR_REDUCTION_FACTOR,
        "min_learning_rate": DEFAULT_MIN_LEARNING_RATE,
        "early_stop_after_lr_drops": PHASE6S_RANK5_ADAPTIVE_EARLY_STOP_AFTER_LR_DROPS,
        "serialize_trained_cores": True,
        "validation_holdout_role": "candidate_selection_and_veto_not_audit_not_production",
        "audit_cloud_role": "reserved_final_only_not_tuning",
    }
    degree_comparator_protocol = {
        "degree_comparator": True,
        "reference_artifact": str(reference_path),
        "reference_basis_order": P85_AUTHOR_SIR_LAGRANGEP_ORDER,
        "reference_basis_num_elems": P85_AUTHOR_SIR_LAGRANGEP_NUM_ELEMS,
        "candidate_basis_order": PHASE6Y_DEGREE_BASIS_ORDER,
        "candidate_basis_num_elems": PHASE6Y_DEGREE_BASIS_NUM_ELEMS,
        "candidate_basis_dim_per_dimension": PHASE6Y_DEGREE_BASIS_DIM,
        "classification": P85_AUTHOR_SIR_DEGREE_COMPARATOR_CLASSIFICATION,
        "classification_subtype": P85_AUTHOR_SIR_DEGREE_COMPARATOR_SUBTYPE,
        "execution_status": "not_executed_preflight_only",
        "future_fit_output_path_status": f"reserved_not_created_in_{path_status_suffix}",
        "comparison_status": "blocked_until_exact_degree_fit_claude_agreed_handoff_and_result_review",
    }
    phase6y_status_fields = {
        "reference_artifact_status": reference_validation["status"],
        "candidate_arm_count_status": "ok" if len(candidate_arms) == 1 else "block",
        "degree_comparator_protocol_status": "ok",
        "new_arm_exact_guard_status": "ok",
        "basis_classification_status": (
            "ok"
            if payload["basis_config"]["degree_comparator_classification"]
            == P85_AUTHOR_SIR_DEGREE_COMPARATOR_CLASSIFICATION
            else "block"
        ),
        "future_fit_output_path_status": f"reserved_not_created_in_{path_status_suffix}",
        "fit_execution_status": "not_executed",
        "degree_convergence_interpretation_status": "preflight_only_no_degree_convergence_claim",
        "phase7_status": "blocked_until_degree_gate_reviewed_or_owner_reframed",
        "audit_tuning_status": "not_used_for_tuning",
    }
    overall = payload["gate_summary"]["overall_status"]
    if reference_validation["status"] != "ok":
        overall = "block"
    return {
        **payload,
        "status": (
            status_ready
            if overall == "ready_for_exact_claude_agreed_execution"
            else block_status
        ),
        "candidate_fit_command": fit_command,
        "candidate_arms": candidate_arms,
        "candidate_fit_commands": {
            "degree_order3_rank4_lr3e-4_l1_0": fit_command,
        },
        "reference_artifact_validation": reference_validation,
        "adaptive_training_protocol": adaptive_protocol,
        "degree_comparator_protocol": degree_comparator_protocol,
        "optimizer_budget": {
            **payload["optimizer_budget"],
            "max_train_steps": PHASE6Y_DEGREE_TRAIN_STEPS,
            "adaptive_training": True,
            "validation_check_every": PHASE6S_RANK5_ADAPTIVE_VALIDATION_CHECK_EVERY,
            "plateau_patience": PHASE6S_RANK5_ADAPTIVE_PLATEAU_PATIENCE,
            "plateau_min_delta": PHASE6S_RANK5_ADAPTIVE_PLATEAU_MIN_DELTA,
            "lr_reduction_factor": DEFAULT_LR_REDUCTION_FACTOR,
            "min_learning_rate": DEFAULT_MIN_LEARNING_RATE,
            "early_stop_after_lr_drops": PHASE6S_RANK5_ADAPTIVE_EARLY_STOP_AFTER_LR_DROPS,
            "serialize_trained_cores": True,
            "training_convergence_policy": (
                "scheduler_stop_required_for_degree_candidate_selection; "
                "validation selection is not degree convergence evidence"
            ),
        },
        "phase6y_status_fields": phase6y_status_fields,
        "reviewed_prerequisites": {
            "phase6w_result": (
                "docs/plans/"
                "bayesfilter-highdim-zhao-cui-p86-phase6w-same-policy-rank-degree-convergence-result-2026-06-26.md"
            ),
            "phase6x_result": (
                "docs/plans/"
                "bayesfilter-highdim-zhao-cui-p86-phase6x-configurable-basis-runner-repair-result-2026-06-26.md"
            ),
            "reference_artifact": str(reference_path),
            "reference_artifact_status": reference.get("status"),
            "reference_holdout_residual": reference.get("holdout_residual"),
        },
        "gate_summary": {
            **payload["gate_summary"],
            **phase6y_status_fields,
            "overall_status": (
                "ready_for_exact_claude_agreed_execution"
                if overall == "ready_for_exact_claude_agreed_execution"
                else "block"
            ),
        },
    }


def build_phase6y_degree_comparator_preflight_payload(
    *,
    output: Path = PHASE6Y_DEGREE_COMPARATOR_PREFLIGHT_OUTPUT,
) -> Mapping[str, Any]:
    return _build_degree_order3_comparator_preflight_payload(
        output=output,
        preflight_output=PHASE6Y_DEGREE_COMPARATOR_PREFLIGHT_OUTPUT,
        fit_output=PHASE6Y_DEGREE_ORDER3_RANK4_L1_0_OUTPUT,
        preflight_command=PHASE6Y_DEGREE_COMPARATOR_PREFLIGHT_COMMAND,
        fit_command=PHASE6Y_DEGREE_ORDER3_RANK4_L1_0_FIT_COMMAND,
        status_ready=STATUS_PHASE6Y_DEGREE_COMPARATOR_PREFLIGHT_READY,
        block_status="BLOCK_P86_PHASE6Y_DEGREE_COMPARATOR_PREFLIGHT",
        schema_version="p86_phase6y_degree_comparator_preflight.v1",
        phase_name="P86 Phase 6Y degree comparator preflight",
        phase_subplan=(
            "docs/plans/"
            "bayesfilter-highdim-zhao-cui-p86-phase6y-degree-comparator-preflight-subplan-2026-06-26.md"
        ),
        phase_result=(
            "docs/plans/"
            "bayesfilter-highdim-zhao-cui-p86-phase6y-degree-comparator-preflight-result-2026-06-26.md"
        ),
        label_prefix="p86-phase6y-degree-order3-rank4",
        path_status_suffix="phase6y",
    )


def build_p88_phase2_degree_comparator_preflight_payload(
    *,
    output: Path = P88_PHASE2_DEGREE_COMPARATOR_PREFLIGHT_OUTPUT,
) -> Mapping[str, Any]:
    return _build_degree_order3_comparator_preflight_payload(
        output=output,
        preflight_output=P88_PHASE2_DEGREE_COMPARATOR_PREFLIGHT_OUTPUT,
        fit_output=P88_PHASE2_DEGREE_ORDER3_RANK4_L1_0_OUTPUT,
        preflight_command=P88_PHASE2_DEGREE_COMPARATOR_PREFLIGHT_COMMAND,
        fit_command=P88_PHASE2_DEGREE_ORDER3_RANK4_L1_0_FIT_COMMAND,
        status_ready=STATUS_P88_PHASE2_DEGREE_COMPARATOR_PREFLIGHT_READY,
        block_status="BLOCK_P88_PHASE2_DEGREE_COMPARATOR_PREFLIGHT",
        schema_version="p88_phase2_degree_comparator_preflight.v1",
        phase_name="P88 Phase 2 degree comparator preflight",
        phase_subplan=(
            "docs/plans/"
            "bayesfilter-highdim-zhao-cui-p88-phase2-degree-convergence-execution-subplan-2026-06-27.md"
        ),
        phase_result=(
            "docs/plans/"
            "bayesfilter-highdim-zhao-cui-p88-phase2-degree-convergence-execution-result-2026-06-27.md"
        ),
        label_prefix="p88-phase2-degree-order3-rank4",
        path_status_suffix="p88_phase2",
    )


def build_fit_block_payload(args: argparse.Namespace) -> Mapping[str, Any]:
    return {
        "schema_version": "p86_phase5_budget_compliant_fit.v1",
        "status": STATUS_FIT_BLOCKED,
        "fit_executed": False,
        "command": FIT_COMMAND,
        "output": str(args.output),
        "blockers": (
            "fit_execution_not_performed_by_preflight_package",
            "exact_claude_agreed_handoff_required_after_preflight_review",
        ),
        "nonclaims": PREFLIGHT_NONCLAIMS,
    }


def build_phase6_rank_preflight_payload(
    *,
    output: Path = PHASE6_RANK_PREFLIGHT_OUTPUT,
) -> Mapping[str, Any]:
    lower_path = Path(FIT_OUTPUT)
    lower = json.loads(lower_path.read_text())
    lower_statuses = lower.get("post_fit_statuses", {})
    lower_required_ok = (
        lower.get("status") == STATUS_TRAINING_BASE_COMPLETED
        and lower.get("training_backend") == TRAINING_BACKEND
        and lower.get("rank_budget", {}).get("fit_rank") == 4
        and lower.get("rank_budget", {}).get("P_theta") == 18216
        and lower_statuses.get("finite_normalizer_status") == "ok"
        and lower_statuses.get("finite_sqrt_square_normalizer_status") == "ok"
        and lower_statuses.get("trainable_component_active_status") == "ok"
        and lower_statuses.get("fallback_route_status") == "not_used"
        and lower_statuses.get("audit_cloud_tuning_status") == "not_used_for_tuning"
        and lower_statuses.get("memory_status") == "within_approved_envelope"
        and lower_statuses.get("runtime_status") == "within_approved_envelope"
    )
    payload = build_preflight_payload(
        output=output,
        target_dimension=36,
        fit_rank=PHASE6_RANK5_FIT_RANK,
        training_sample_count=PHASE6_RANK5_TRAINING_SAMPLE_COUNT,
        holdout_sample_count=65536,
        audit_sample_count=65536,
        seed=PHASE6_RANK5_SEED,
        optimizer_batch_size=DEFAULT_OPTIMIZER_BATCH_SIZE,
        prefit_steps=DEFAULT_PREFIT_STEPS,
        train_steps=PHASE6_RANK5_TRAIN_STEPS,
        learning_rate=DEFAULT_LEARNING_RATE,
        max_seconds=14400,
        memory_cap_mib=12288,
        command=PHASE6_RANK_PREFLIGHT_COMMAND,
        candidate_fit_command=PHASE6_RANK5_FIT_COMMAND,
        expected_output=PHASE6_RANK_PREFLIGHT_OUTPUT,
        expected_fit_output=PHASE6_RANK5_FIT_OUTPUT,
        expected_p_theta=28380,
        status_ready=STATUS_PHASE6_RANK_PREFLIGHT_READY,
        block_status="BLOCK_P86_PHASE6_RANK_CONVERGENCE_PREFLIGHT",
        schema_version="p86_phase6_rank_convergence_preflight.v1",
        phase_name="P86 Phase 6 rank convergence comparator preflight",
        phase_subplan=PHASE6_SUBPLAN,
        phase_result=(
            "docs/plans/"
            "bayesfilter-highdim-zhao-cui-p86-phase6-rank-degree-convergence-result-2026-06-24.md"
        ),
        rank_rung="author_basis_rung_F_rank5_comparator",
        label_prefix="p86-phase6-rank5",
        train_prior_seed=PHASE6_RANK5_TRAIN_PRIOR_SEED,
        train_process_seed=PHASE6_RANK5_TRAIN_PROCESS_SEED,
        holdout_prior_seed=PHASE6_RANK5_HOLDOUT_PRIOR_SEED,
        holdout_process_seed=PHASE6_RANK5_HOLDOUT_PROCESS_SEED,
        audit_prior_seed=PHASE6_RANK5_AUDIT_PRIOR_SEED,
        audit_process_seed=PHASE6_RANK5_AUDIT_PROCESS_SEED,
        nonclaims=PHASE6_PREFLIGHT_NONCLAIMS,
        lower_rung_artifact=str(lower_path),
    )
    phase6_status_fields = {
        "lower_rung_status": "ok" if lower_required_ok else "block",
        "lower_rung_training_backend": lower.get("training_backend"),
        "lower_rung_fit_rank": lower.get("rank_budget", {}).get("fit_rank"),
        "lower_rung_p_theta": lower.get("rank_budget", {}).get("P_theta"),
        "lower_rung_status_value": lower.get("status"),
        "rank_comparator_relation": "rank5_vs_rank4_same_route",
        "degree_convergence_status": "blocked_pending_reviewed_configurable_basis_path",
        "lower_rung_core_serialization_status": (
            "summary_only_no_tt_core_payload_for_functional_delta"
        ),
        "convergence_interpretation_status": (
            "preflight_only_no_rank_convergence_claim"
        ),
    }
    overall = payload["gate_summary"]["overall_status"]
    if not lower_required_ok:
        overall = "block"
    return {
        **payload,
        "status": (
            STATUS_PHASE6_RANK_PREFLIGHT_READY
            if overall == "ready_for_exact_claude_agreed_execution"
            else "BLOCK_P86_PHASE6_RANK_CONVERGENCE_PREFLIGHT"
        ),
        "lower_rung_summary": {
            "artifact": str(lower_path),
            "status": lower.get("status"),
            "training_backend": lower.get("training_backend"),
            "fit_rank": lower.get("rank_budget", {}).get("fit_rank"),
            "P_theta": lower.get("rank_budget", {}).get("P_theta"),
            "training_sample_count": lower.get("rank_budget", {}).get("training_sample_count"),
            "normalizer": lower.get("normalizer"),
            "sqrt_square_normalizer": lower.get("sqrt_square_normalizer"),
            "fit_residual": lower.get("fit_residual"),
            "holdout_residual": lower.get("holdout_residual"),
            "post_fit_statuses": lower_statuses,
        },
        "phase6_status_fields": phase6_status_fields,
        "gate_summary": {
            **payload["gate_summary"],
            **phase6_status_fields,
            "overall_status": overall,
        },
        "convergence_artifact_gap": {
            "status": "known_gap_not_preflight_blocker",
            "detail": (
                "The Phase 5 JSON is summary-only and does not serialize trained TT cores; "
                "Phase 6 may preflight a rank-5 comparator, but final convergence "
                "interpretation needs a reviewed convergence ledger/evaluation artifact."
            ),
        },
    }


def build_phase6s_adaptive_rank5_preflight_payload(
    *,
    output: Path = PHASE6S_RANK5_ADAPTIVE_PREFLIGHT_OUTPUT,
) -> Mapping[str, Any]:
    lower_path = Path(FIT_OUTPUT)
    old_rank5_path = Path(PHASE6_RANK5_FIT_OUTPUT)
    smoke_path = Path(PHASE6R_ADAPTIVE_SMOKE_OUTPUT)
    lower = json.loads(lower_path.read_text())
    old_rank5 = json.loads(old_rank5_path.read_text())
    smoke = json.loads(smoke_path.read_text())
    lower_statuses = lower.get("post_fit_statuses", {})
    smoke_statuses = smoke.get("post_fit_statuses", {})
    lower_required_ok = (
        lower.get("status") == STATUS_TRAINING_BASE_COMPLETED
        and lower.get("training_backend") == TRAINING_BACKEND
        and lower.get("rank_budget", {}).get("fit_rank") == 4
        and lower.get("rank_budget", {}).get("P_theta") == 18216
        and lower_statuses.get("finite_normalizer_status") == "ok"
        and lower_statuses.get("finite_sqrt_square_normalizer_status") == "ok"
        and lower_statuses.get("trainable_component_active_status") == "ok"
        and lower_statuses.get("fallback_route_status") == "not_used"
        and lower_statuses.get("audit_cloud_tuning_status") == "not_used_for_tuning"
        and lower_statuses.get("memory_status") == "within_approved_envelope"
        and lower_statuses.get("runtime_status") == "within_approved_envelope"
    )
    smoke_required_ok = (
        smoke.get("status") == STATUS_PHASE6R_ADAPTIVE_SMOKE_COMPLETED
        and smoke.get("training_executed") is True
        and smoke.get("smoke_kind") == "phase6r_adaptive_training_scheduler_smoke"
        and smoke.get("trained_core_serialization", {}).get("status") == "serialized_with_values"
        and len(smoke.get("validation_trace") or ()) > 0
        and smoke_statuses.get("fallback_route_status") == "not_used"
        and smoke_statuses.get("audit_cloud_tuning_status") == "not_used_for_tuning"
    )
    old_rank5_status = old_rank5.get("status")
    payload = build_preflight_payload(
        output=output,
        target_dimension=36,
        fit_rank=PHASE6_RANK5_FIT_RANK,
        training_sample_count=PHASE6_RANK5_TRAINING_SAMPLE_COUNT,
        holdout_sample_count=65536,
        audit_sample_count=65536,
        seed=PHASE6_RANK5_SEED,
        optimizer_batch_size=DEFAULT_OPTIMIZER_BATCH_SIZE,
        prefit_steps=DEFAULT_PREFIT_STEPS,
        train_steps=PHASE6S_RANK5_ADAPTIVE_TRAIN_STEPS,
        learning_rate=DEFAULT_LEARNING_RATE,
        max_seconds=14400,
        memory_cap_mib=12288,
        command=PHASE6S_RANK5_ADAPTIVE_PREFLIGHT_COMMAND,
        candidate_fit_command=PHASE6S_RANK5_ADAPTIVE_FIT_COMMAND,
        expected_output=PHASE6S_RANK5_ADAPTIVE_PREFLIGHT_OUTPUT,
        expected_fit_output=PHASE6S_RANK5_ADAPTIVE_FIT_OUTPUT,
        expected_p_theta=28380,
        status_ready=STATUS_PHASE6S_ADAPTIVE_RANK5_PREFLIGHT_READY,
        block_status="BLOCK_P86_PHASE6S_ADAPTIVE_RANK5_PREFLIGHT",
        schema_version="p86_phase6s_adaptive_rank5_preflight.v1",
        phase_name="P86 Phase 6S adaptive rank-5 preflight and guard",
        phase_subplan=(
            "docs/plans/"
            "bayesfilter-highdim-zhao-cui-p86-phase6s-adaptive-rank5-preflight-guard-subplan-2026-06-25.md"
        ),
        phase_result=(
            "docs/plans/"
            "bayesfilter-highdim-zhao-cui-p86-phase6s-adaptive-rank5-preflight-guard-result-2026-06-25.md"
        ),
        rank_rung="author_basis_rung_F_rank5_adaptive_comparator",
        label_prefix="p86-phase6s-rank5-adaptive",
        train_prior_seed=PHASE6_RANK5_TRAIN_PRIOR_SEED,
        train_process_seed=PHASE6_RANK5_TRAIN_PROCESS_SEED,
        holdout_prior_seed=PHASE6_RANK5_HOLDOUT_PRIOR_SEED,
        holdout_process_seed=PHASE6_RANK5_HOLDOUT_PROCESS_SEED,
        audit_prior_seed=PHASE6_RANK5_AUDIT_PRIOR_SEED,
        audit_process_seed=PHASE6_RANK5_AUDIT_PROCESS_SEED,
        nonclaims=PHASE6S_PREFLIGHT_NONCLAIMS,
        lower_rung_artifact=str(lower_path),
    )
    adaptive_protocol = {
        "adaptive_training": True,
        "optimizer_identity": TRAINING_BACKEND,
        "optimizer": "Adam",
        "validation_check_every": PHASE6S_RANK5_ADAPTIVE_VALIDATION_CHECK_EVERY,
        "plateau_patience": PHASE6S_RANK5_ADAPTIVE_PLATEAU_PATIENCE,
        "plateau_min_delta": PHASE6S_RANK5_ADAPTIVE_PLATEAU_MIN_DELTA,
        "lr_reduction_factor": DEFAULT_LR_REDUCTION_FACTOR,
        "min_learning_rate": DEFAULT_MIN_LEARNING_RATE,
        "early_stop_after_lr_drops": PHASE6S_RANK5_ADAPTIVE_EARLY_STOP_AFTER_LR_DROPS,
        "serialize_trained_cores": True,
        "validation_holdout_role": "scheduler_monitor_and_veto_not_audit_not_production",
        "audit_cloud_role": "reserved_final_only_not_tuning",
    }
    phase6s_status_fields = {
        "lower_rung_status": "ok" if lower_required_ok else "block",
        "phase6r_smoke_status": "ok" if smoke_required_ok else "block",
        "old_rank5_artifact_status": old_rank5_status,
        "old_rank5_interpretation_status": "undertrained_protocol_incomplete_diagnostic_only",
        "rank_comparator_relation": "adaptive_rank5_vs_rank4_same_route",
        "degree_convergence_status": "blocked_pending_reviewed_configurable_basis_path",
        "adaptive_protocol_status": "ok",
        "optimizer_identity_status": "ok",
        "trained_core_serialization_required_status": "ok",
        "validation_holdout_status": "ok",
        "audit_tuning_status": "not_used_for_tuning",
        "convergence_interpretation_status": "preflight_only_no_rank_convergence_claim",
    }
    overall = payload["gate_summary"]["overall_status"]
    if not lower_required_ok or not smoke_required_ok:
        overall = "block"
    return {
        **payload,
        "status": (
            STATUS_PHASE6S_ADAPTIVE_RANK5_PREFLIGHT_READY
            if overall == "ready_for_exact_claude_agreed_execution"
            else "BLOCK_P86_PHASE6S_ADAPTIVE_RANK5_PREFLIGHT"
        ),
        "candidate_fit_command": PHASE6S_RANK5_ADAPTIVE_FIT_COMMAND,
        "adaptive_training_protocol": adaptive_protocol,
        "optimizer_budget": {
            **payload["optimizer_budget"],
            "max_train_steps": PHASE6S_RANK5_ADAPTIVE_TRAIN_STEPS,
            "adaptive_training": True,
            "validation_check_every": PHASE6S_RANK5_ADAPTIVE_VALIDATION_CHECK_EVERY,
            "plateau_patience": PHASE6S_RANK5_ADAPTIVE_PLATEAU_PATIENCE,
            "plateau_min_delta": PHASE6S_RANK5_ADAPTIVE_PLATEAU_MIN_DELTA,
            "lr_reduction_factor": DEFAULT_LR_REDUCTION_FACTOR,
            "min_learning_rate": DEFAULT_MIN_LEARNING_RATE,
            "early_stop_after_lr_drops": PHASE6S_RANK5_ADAPTIVE_EARLY_STOP_AFTER_LR_DROPS,
            "serialize_trained_cores": True,
            "training_convergence_policy": (
                "scheduler_stop_required_for_convergence_claim; "
                "max_step_exhaustion_with_improving_loss_is_nonconverged"
            ),
        },
        "phase6s_status_fields": phase6s_status_fields,
        "reviewed_prerequisites": {
            "phase6r_smoke_artifact": str(smoke_path),
            "phase6r_smoke_status": smoke.get("status"),
            "phase6r_smoke_validation_trace_len": len(smoke.get("validation_trace") or ()),
            "phase6r_smoke_core_serialization_status": smoke.get("trained_core_serialization", {}).get("status"),
            "old_rank5_artifact": str(old_rank5_path),
            "old_rank5_status": old_rank5_status,
            "old_rank5_interpretation_status": "undertrained_protocol_incomplete_diagnostic_only",
        },
        "gate_summary": {
            **payload["gate_summary"],
            **phase6s_status_fields,
            "overall_status": (
                "ready_for_exact_claude_agreed_execution"
                if overall == "ready_for_exact_claude_agreed_execution"
                else "block"
            ),
        },
    }


def build_phase6t_l1_tuning_preflight_payload(
    *,
    output: Path = PHASE6T_L1_TUNING_PREFLIGHT_OUTPUT,
) -> Mapping[str, Any]:
    lower_path = Path(FIT_OUTPUT)
    phase6s_path = Path(PHASE6S_RANK5_ADAPTIVE_FIT_OUTPUT)
    lower = json.loads(lower_path.read_text())
    phase6s = json.loads(phase6s_path.read_text())
    lower_statuses = lower.get("post_fit_statuses", {})
    phase6s_statuses = phase6s.get("post_fit_statuses", {})
    lower_required_ok = (
        lower.get("status") == STATUS_TRAINING_BASE_COMPLETED
        and lower.get("training_backend") == TRAINING_BACKEND
        and lower.get("rank_budget", {}).get("fit_rank") == 4
        and lower_statuses.get("audit_cloud_tuning_status") == "not_used_for_tuning"
    )
    phase6s_required_ok = (
        phase6s.get("training_backend") == TRAINING_BACKEND
        and phase6s.get("rank_budget", {}).get("fit_rank") == PHASE6_RANK5_FIT_RANK
        and phase6s_statuses.get("audit_cloud_tuning_status") == "not_used_for_tuning"
        and phase6s.get("trained_core_serialization", {}).get("status") == "serialized_with_values"
        and len(phase6s.get("validation_trace") or ()) > 0
    )
    payload = build_preflight_payload(
        output=output,
        target_dimension=36,
        fit_rank=PHASE6_RANK5_FIT_RANK,
        training_sample_count=PHASE6_RANK5_TRAINING_SAMPLE_COUNT,
        holdout_sample_count=65536,
        audit_sample_count=65536,
        seed=PHASE6_RANK5_SEED,
        optimizer_batch_size=DEFAULT_OPTIMIZER_BATCH_SIZE,
        prefit_steps=DEFAULT_PREFIT_STEPS,
        train_steps=PHASE6T_L1_TUNING_TRAIN_STEPS,
        learning_rate=PHASE6T_L1_TUNING_LEARNING_RATE,
        l1_weight=PHASE6T_L1_TUNING_L1_WEIGHT,
        l2_weight=PHASE6T_L1_TUNING_L2_WEIGHT,
        logz_anchor_weight=PHASE6T_L1_TUNING_LOGZ_ANCHOR_WEIGHT,
        max_seconds=PHASE6T_L1_TUNING_MAX_SECONDS,
        memory_cap_mib=12288,
        command=PHASE6T_L1_TUNING_PREFLIGHT_COMMAND,
        candidate_fit_command=PHASE6T_L1_TUNING_FIT_COMMAND,
        expected_output=PHASE6T_L1_TUNING_PREFLIGHT_OUTPUT,
        expected_fit_output=PHASE6T_L1_TUNING_DIAGNOSTIC_OUTPUT,
        expected_p_theta=28380,
        status_ready=STATUS_PHASE6T_L1_TUNING_PREFLIGHT_READY,
        block_status="BLOCK_P86_PHASE6T_L1_REGULARIZATION_TUNING_PREFLIGHT",
        schema_version="p86_phase6t_l1_regularization_tuning_preflight.v1",
        phase_name="P86 Phase 6T L1 regularization tuning preflight",
        phase_subplan=(
            "docs/plans/"
            "bayesfilter-highdim-zhao-cui-p86-phase6t-l1-regularization-tuning-subplan-2026-06-25.md"
        ),
        phase_result=(
            "docs/plans/"
            "bayesfilter-highdim-zhao-cui-p86-phase6t-l1-regularization-tuning-result-2026-06-25.md"
        ),
        rank_rung="author_basis_rung_F_rank5_l1_regularization_diagnostic",
        label_prefix="p86-phase6t-rank5-l1",
        train_prior_seed=PHASE6_RANK5_TRAIN_PRIOR_SEED,
        train_process_seed=PHASE6_RANK5_TRAIN_PROCESS_SEED,
        holdout_prior_seed=PHASE6_RANK5_HOLDOUT_PRIOR_SEED,
        holdout_process_seed=PHASE6_RANK5_HOLDOUT_PROCESS_SEED,
        audit_prior_seed=PHASE6_RANK5_AUDIT_PRIOR_SEED,
        audit_process_seed=PHASE6_RANK5_AUDIT_PROCESS_SEED,
        nonclaims=PHASE6T_PREFLIGHT_NONCLAIMS,
        lower_rung_artifact=str(lower_path),
    )
    regularization_protocol = {
        "regularization_tuning": True,
        "default_policy": ZHAO_CUI_L1_TUNING_DEFAULT_POLICY,
        "selection_status": ZHAO_CUI_L1_TUNING_SELECTION_STATUS,
        "l1_weight": PHASE6T_L1_TUNING_L1_WEIGHT,
        "l2_weight": PHASE6T_L1_TUNING_L2_WEIGHT,
        "logz_anchor_weight": PHASE6T_L1_TUNING_LOGZ_ANCHOR_WEIGHT,
        "candidate_l1_grid": (0.0, 1e-10, 3e-10, 1e-9, 3e-9, 1e-8),
        "candidate_learning_rate_grid": (1e-4, 3e-4),
        "grid_execution_status": "metadata_only_not_executed",
        "validation_holdout_role": "candidate_selection_and_veto_not_audit_not_production",
        "audit_cloud_role": "reserved_final_only_not_tuning",
        "normalizer_pathology_source": str(phase6s_path),
    }
    adaptive_protocol = {
        "adaptive_training": True,
        "optimizer_identity": TRAINING_BACKEND,
        "optimizer": "Adam",
        "validation_check_every": PHASE6S_RANK5_ADAPTIVE_VALIDATION_CHECK_EVERY,
        "plateau_patience": PHASE6S_RANK5_ADAPTIVE_PLATEAU_PATIENCE,
        "plateau_min_delta": PHASE6S_RANK5_ADAPTIVE_PLATEAU_MIN_DELTA,
        "lr_reduction_factor": DEFAULT_LR_REDUCTION_FACTOR,
        "min_learning_rate": DEFAULT_MIN_LEARNING_RATE,
        "early_stop_after_lr_drops": PHASE6S_RANK5_ADAPTIVE_EARLY_STOP_AFTER_LR_DROPS,
        "serialize_trained_cores": True,
        "validation_holdout_role": "scheduler_monitor_and_veto_not_audit_not_production",
        "audit_cloud_role": "reserved_final_only_not_tuning",
    }
    phase6t_status_fields = {
        "lower_rung_status": "ok" if lower_required_ok else "block",
        "phase6s_rank5_failure_available_status": "ok" if phase6s_required_ok else "block",
        "regularization_protocol_status": "ok",
        "l1_weight_guard_status": "ok",
        "l2_weight_guard_status": "ok",
        "logz_anchor_weight_guard_status": "ok",
        "audit_tuning_status": "not_used_for_tuning",
        "grid_execution_status": "not_executed",
        "convergence_interpretation_status": "preflight_only_no_rank_convergence_claim",
    }
    overall = payload["gate_summary"]["overall_status"]
    if not lower_required_ok or not phase6s_required_ok:
        overall = "block"
    return {
        **payload,
        "status": (
            STATUS_PHASE6T_L1_TUNING_PREFLIGHT_READY
            if overall == "ready_for_exact_claude_agreed_execution"
            else "BLOCK_P86_PHASE6T_L1_REGULARIZATION_TUNING_PREFLIGHT"
        ),
        "candidate_fit_command": PHASE6T_L1_TUNING_FIT_COMMAND,
        "adaptive_training_protocol": adaptive_protocol,
        "regularization_protocol": regularization_protocol,
        "optimizer_budget": {
            **payload["optimizer_budget"],
            "max_train_steps": PHASE6T_L1_TUNING_TRAIN_STEPS,
            "adaptive_training": True,
            "validation_check_every": PHASE6S_RANK5_ADAPTIVE_VALIDATION_CHECK_EVERY,
            "plateau_patience": PHASE6S_RANK5_ADAPTIVE_PLATEAU_PATIENCE,
            "plateau_min_delta": PHASE6S_RANK5_ADAPTIVE_PLATEAU_MIN_DELTA,
            "lr_reduction_factor": DEFAULT_LR_REDUCTION_FACTOR,
            "min_learning_rate": DEFAULT_MIN_LEARNING_RATE,
            "early_stop_after_lr_drops": PHASE6S_RANK5_ADAPTIVE_EARLY_STOP_AFTER_LR_DROPS,
            "serialize_trained_cores": True,
            "training_convergence_policy": (
                "scheduler_stop_required_for_convergence_claim; "
                "validation tuning is not rank convergence evidence"
            ),
        },
        "phase6t_status_fields": phase6t_status_fields,
        "reviewed_prerequisites": {
            "rank4_lower_rung_artifact": str(lower_path),
            "rank4_lower_rung_status": lower.get("status"),
            "phase6s_rank5_artifact": str(phase6s_path),
            "phase6s_rank5_status": phase6s.get("status"),
            "phase6s_rank5_holdout_residual": phase6s.get("holdout_residual"),
            "phase6s_rank5_normalizer": phase6s.get("normalizer"),
            "phase6s_rank5_validation_trace_len": len(phase6s.get("validation_trace") or ()),
        },
        "gate_summary": {
            **payload["gate_summary"],
            **phase6t_status_fields,
            "overall_status": (
                "ready_for_exact_claude_agreed_execution"
                if overall == "ready_for_exact_claude_agreed_execution"
                else "block"
            ),
        },
    }


def _phase6v_candidate_arms() -> tuple[Mapping[str, Any], ...]:
    return (
        {
            "arm_id": "rank5_lr3e-4_l1_0",
            "role": "zero_l1_comparator",
            "l1_weight": 0.0,
            "execution": "new_fit_requires_exact_claude_agreed_handoff",
            "output": str(PHASE6V_L1_SELECTION_L1_0_OUTPUT),
            "candidate_fit_command": PHASE6V_L1_SELECTION_L1_0_FIT_COMMAND,
        },
        {
            "arm_id": "rank5_lr3e-4_l1_3e-10",
            "role": "positive_l1_candidate",
            "l1_weight": 3e-10,
            "execution": "new_fit_requires_exact_claude_agreed_handoff",
            "output": str(PHASE6V_L1_SELECTION_L1_3E_10_OUTPUT),
            "candidate_fit_command": PHASE6V_L1_SELECTION_L1_3E_10_FIT_COMMAND,
        },
        {
            "arm_id": "rank5_lr3e-4_l1_1e-9",
            "role": "reuse_phase6t_reviewed_candidate",
            "l1_weight": 1e-9,
            "execution": "reuse_reviewed_phase6t_artifact_if_protocol_equivalent",
            "output": str(PHASE6T_L1_TUNING_DIAGNOSTIC_OUTPUT),
            "candidate_fit_command": PHASE6T_L1_TUNING_FIT_COMMAND,
        },
        {
            "arm_id": "rank5_lr3e-4_l1_3e-9",
            "role": "positive_l1_candidate",
            "l1_weight": 3e-9,
            "execution": "new_fit_requires_exact_claude_agreed_handoff",
            "output": str(PHASE6V_L1_SELECTION_L1_3E_9_OUTPUT),
            "candidate_fit_command": PHASE6V_L1_SELECTION_L1_3E_9_FIT_COMMAND,
        },
    )


def _phase6v_new_fit_arm_expectations() -> Mapping[Path, Mapping[str, Any]]:
    common = {
        "preflight_json": PHASE6V_L1_SELECTION_PREFLIGHT_OUTPUT,
        "target_dimension": 36,
        "fit_rank": PHASE6_RANK5_FIT_RANK,
        "training_sample_count": PHASE6_RANK5_TRAINING_SAMPLE_COUNT,
        "holdout_sample_count": 65536,
        "audit_sample_count": 65536,
        "seed": PHASE6_RANK5_SEED,
        "optimizer_batch_size": DEFAULT_OPTIMIZER_BATCH_SIZE,
        "prefit_steps": DEFAULT_PREFIT_STEPS,
        "train_steps": PHASE6V_L1_SELECTION_TRAIN_STEPS,
        "learning_rate": PHASE6V_L1_SELECTION_LEARNING_RATE,
        "l2_weight": PHASE6V_L1_SELECTION_L2_WEIGHT,
        "logz_anchor_weight": PHASE6V_L1_SELECTION_LOGZ_ANCHOR_WEIGHT,
        "max_seconds": PHASE6V_L1_SELECTION_MAX_SECONDS,
        "memory_cap_mib": 12288,
        "train_prior_seed": PHASE6_RANK5_TRAIN_PRIOR_SEED,
        "train_process_seed": PHASE6_RANK5_TRAIN_PROCESS_SEED,
        "holdout_prior_seed": PHASE6_RANK5_HOLDOUT_PRIOR_SEED,
        "holdout_process_seed": PHASE6_RANK5_HOLDOUT_PROCESS_SEED,
        "audit_prior_seed": PHASE6_RANK5_AUDIT_PRIOR_SEED,
        "audit_process_seed": PHASE6_RANK5_AUDIT_PROCESS_SEED,
        "adaptive_training": True,
        "validation_check_every": PHASE6S_RANK5_ADAPTIVE_VALIDATION_CHECK_EVERY,
        "plateau_patience": PHASE6S_RANK5_ADAPTIVE_PLATEAU_PATIENCE,
        "plateau_min_delta": PHASE6S_RANK5_ADAPTIVE_PLATEAU_MIN_DELTA,
        "lr_reduction_factor": DEFAULT_LR_REDUCTION_FACTOR,
        "min_learning_rate": DEFAULT_MIN_LEARNING_RATE,
        "early_stop_after_lr_drops": PHASE6S_RANK5_ADAPTIVE_EARLY_STOP_AFTER_LR_DROPS,
        "serialize_trained_cores": True,
    }
    return {
        PHASE6V_L1_SELECTION_L1_0_OUTPUT: {
            **common,
            "output": PHASE6V_L1_SELECTION_L1_0_OUTPUT,
            "l1_weight": 0.0,
            "candidate_fit_command": PHASE6V_L1_SELECTION_L1_0_FIT_COMMAND,
        },
        PHASE6V_L1_SELECTION_L1_3E_10_OUTPUT: {
            **common,
            "output": PHASE6V_L1_SELECTION_L1_3E_10_OUTPUT,
            "l1_weight": 3e-10,
            "candidate_fit_command": PHASE6V_L1_SELECTION_L1_3E_10_FIT_COMMAND,
        },
        PHASE6V_L1_SELECTION_L1_3E_9_OUTPUT: {
            **common,
            "output": PHASE6V_L1_SELECTION_L1_3E_9_OUTPUT,
            "l1_weight": 3e-9,
            "candidate_fit_command": PHASE6V_L1_SELECTION_L1_3E_9_FIT_COMMAND,
        },
    }


def validate_phase6v_reuse_arm(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    statuses = payload.get("post_fit_statuses", {})
    rank_budget = payload.get("rank_budget", {})
    optimizer_budget = payload.get("optimizer_budget", {})
    route = payload.get("route_manifest", {})
    training_protocol = (
        payload.get("training_summary", {}).get("training_protocol", {})
    )
    training_config = payload.get("training_config", {})
    fit_manifest = payload.get("fit_data_manifest", {})
    nonclaims = tuple(payload.get("nonclaims") or ())
    required_nonclaim_fragments = (
        "no rank convergence claim",
        "no HMC readiness claim",
        "no LEDH comparison claim",
        "no production readiness claim",
        "not a source-faithful author TT-cross proof",
    )
    field_statuses = {
        "status": (
            payload.get("status") == STATUS_PHASE6T_L1_TUNING_COMPLETED
        ),
        "fit_executed": payload.get("fit_executed") is True,
        "training_backend": payload.get("training_backend") == TRAINING_BACKEND,
        "target_dimension": route.get("target_dimension") == 36,
        "fit_rank": rank_budget.get("fit_rank") == PHASE6_RANK5_FIT_RANK,
        "training_sample_count": (
            rank_budget.get("training_sample_count")
            == PHASE6_RANK5_TRAINING_SAMPLE_COUNT
        ),
        "holdout_sample_count": fit_manifest.get("holdout_sample_count") == 65536,
        "learning_rate": (
            float(optimizer_budget.get("learning_rate"))
            == PHASE6V_L1_SELECTION_LEARNING_RATE
        ),
        "l1_weight": (
            float(training_protocol.get("l1_weight"))
            == PHASE6T_L1_TUNING_L1_WEIGHT
            and float(training_config.get("l1_weight"))
            == PHASE6T_L1_TUNING_L1_WEIGHT
        ),
        "l2_weight": (
            float(training_protocol.get("l2_weight"))
            == PHASE6V_L1_SELECTION_L2_WEIGHT
            and float(training_config.get("l2_weight"))
            == PHASE6V_L1_SELECTION_L2_WEIGHT
        ),
        "logz_anchor_weight": (
            float(training_protocol.get("logz_anchor_weight"))
            == PHASE6V_L1_SELECTION_LOGZ_ANCHOR_WEIGHT
            and float(training_config.get("logz_anchor_weight"))
            == PHASE6V_L1_SELECTION_LOGZ_ANCHOR_WEIGHT
        ),
        "adaptive_scheduler": (
            optimizer_budget.get("adaptive_training") is True
            and optimizer_budget.get("validation_check_every")
            == PHASE6S_RANK5_ADAPTIVE_VALIDATION_CHECK_EVERY
            and optimizer_budget.get("plateau_patience")
            == PHASE6S_RANK5_ADAPTIVE_PLATEAU_PATIENCE
            and float(optimizer_budget.get("plateau_min_delta"))
            == PHASE6S_RANK5_ADAPTIVE_PLATEAU_MIN_DELTA
            and float(optimizer_budget.get("lr_reduction_factor"))
            == DEFAULT_LR_REDUCTION_FACTOR
            and float(optimizer_budget.get("min_learning_rate"))
            == DEFAULT_MIN_LEARNING_RATE
            and optimizer_budget.get("early_stop_after_lr_drops")
            == PHASE6S_RANK5_ADAPTIVE_EARLY_STOP_AFTER_LR_DROPS
            and optimizer_budget.get("serialize_trained_cores") is True
        ),
        "train_seeds": (
            fit_manifest.get("train_prior_seed") == PHASE6_RANK5_TRAIN_PRIOR_SEED
            and fit_manifest.get("train_process_seed")
            == PHASE6_RANK5_TRAIN_PROCESS_SEED
        ),
        "holdout_seeds": (
            fit_manifest.get("holdout_prior_seed")
            == PHASE6_RANK5_HOLDOUT_PRIOR_SEED
            and fit_manifest.get("holdout_process_seed")
            == PHASE6_RANK5_HOLDOUT_PROCESS_SEED
        ),
        "route": (
            route.get("target_id") == "zhao_cui_sir_austria_d18"
            and route.get("basis_family") == "lagrangep"
            and route.get("basis_order") == 4
            and route.get("basis_num_elems") == 8
            and route.get("basis_dim_per_dimension") == 33
            and route.get("domain_map") == "algebraic"
            and float(route.get("domain_scale")) == 1.0
            and route.get("density_measure") == DensityMeasure.REFERENCE_MEASURE.value
            and route.get("mass_measure") == MassMeasure.REFERENCE_MEASURE.value
            and isinstance(route.get("xla_static_fields"), list)
            and "basis_family" in route.get("xla_static_fields", ())
        ),
        "serialized_cores": (
            payload.get("trained_core_serialization", {}).get("status")
            == "serialized_with_values"
        ),
        "post_fit_statuses": (
            statuses.get("finite_fit_residual_status") == "ok"
            and statuses.get("finite_holdout_residual_status") == "ok"
            and statuses.get("finite_normalizer_status") == "ok"
            and statuses.get("finite_sqrt_square_normalizer_status") == "ok"
            and statuses.get("fallback_route_status") == "not_used"
            and statuses.get("audit_cloud_tuning_status") == "not_used_for_tuning"
            and statuses.get("runtime_status") == "within_approved_envelope"
            and statuses.get("memory_status") == "within_approved_envelope"
        ),
        "nonclaims": all(
            any(fragment in claim for claim in nonclaims)
            for fragment in required_nonclaim_fragments
        ),
    }
    return {
        "status": "ok" if all(field_statuses.values()) else "block",
        "artifact": str(PHASE6T_L1_TUNING_DIAGNOSTIC_OUTPUT),
        "validation_kind": "manifest_protocol_equivalence_not_command_acceptance",
        "field_statuses": field_statuses,
    }


def build_phase6v_l1_selection_preflight_payload(
    *,
    output: Path = PHASE6V_L1_SELECTION_PREFLIGHT_OUTPUT,
) -> Mapping[str, Any]:
    phase6t_path = Path(PHASE6T_L1_TUNING_DIAGNOSTIC_OUTPUT)
    phase6t = json.loads(phase6t_path.read_text())
    reuse_validation = validate_phase6v_reuse_arm(phase6t)
    payload = build_preflight_payload(
        output=output,
        target_dimension=36,
        fit_rank=PHASE6_RANK5_FIT_RANK,
        training_sample_count=PHASE6_RANK5_TRAINING_SAMPLE_COUNT,
        holdout_sample_count=65536,
        audit_sample_count=65536,
        seed=PHASE6_RANK5_SEED,
        optimizer_batch_size=DEFAULT_OPTIMIZER_BATCH_SIZE,
        prefit_steps=DEFAULT_PREFIT_STEPS,
        train_steps=PHASE6V_L1_SELECTION_TRAIN_STEPS,
        learning_rate=PHASE6V_L1_SELECTION_LEARNING_RATE,
        l1_weight=DEFAULT_L1_WEIGHT,
        l2_weight=PHASE6V_L1_SELECTION_L2_WEIGHT,
        logz_anchor_weight=PHASE6V_L1_SELECTION_LOGZ_ANCHOR_WEIGHT,
        max_seconds=PHASE6V_L1_SELECTION_MAX_SECONDS,
        memory_cap_mib=12288,
        command=PHASE6V_L1_SELECTION_PREFLIGHT_COMMAND,
        candidate_fit_command=PHASE6V_L1_SELECTION_L1_0_FIT_COMMAND,
        expected_output=PHASE6V_L1_SELECTION_PREFLIGHT_OUTPUT,
        expected_fit_output=PHASE6V_L1_SELECTION_L1_0_OUTPUT,
        expected_p_theta=28380,
        status_ready=STATUS_PHASE6V_L1_SELECTION_PREFLIGHT_READY,
        block_status="BLOCK_P86_PHASE6V_L1_SELECTION_PREFLIGHT",
        schema_version="p86_phase6v_l1_selection_preflight.v1",
        phase_name="P86 Phase 6V L1 selection preflight",
        phase_subplan=(
            "docs/plans/"
            "bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-convergence-subplan-2026-06-25.md"
        ),
        phase_result=(
            "docs/plans/"
            "bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-preflight-guard-result-2026-06-25.md"
        ),
        rank_rung="author_basis_rung_F_rank5_l1_selection",
        label_prefix="p86-phase6v-rank5-l1-selection",
        train_prior_seed=PHASE6_RANK5_TRAIN_PRIOR_SEED,
        train_process_seed=PHASE6_RANK5_TRAIN_PROCESS_SEED,
        holdout_prior_seed=PHASE6_RANK5_HOLDOUT_PRIOR_SEED,
        holdout_process_seed=PHASE6_RANK5_HOLDOUT_PROCESS_SEED,
        audit_prior_seed=PHASE6_RANK5_AUDIT_PRIOR_SEED,
        audit_process_seed=PHASE6_RANK5_AUDIT_PROCESS_SEED,
        nonclaims=PHASE6V_PREFLIGHT_NONCLAIMS,
        lower_rung_artifact=str(FIT_OUTPUT),
    )
    candidate_arms = _phase6v_candidate_arms()
    adaptive_protocol = {
        "adaptive_training": True,
        "optimizer_identity": TRAINING_BACKEND,
        "optimizer": "Adam",
        "validation_check_every": PHASE6S_RANK5_ADAPTIVE_VALIDATION_CHECK_EVERY,
        "plateau_patience": PHASE6S_RANK5_ADAPTIVE_PLATEAU_PATIENCE,
        "plateau_min_delta": PHASE6S_RANK5_ADAPTIVE_PLATEAU_MIN_DELTA,
        "lr_reduction_factor": DEFAULT_LR_REDUCTION_FACTOR,
        "min_learning_rate": DEFAULT_MIN_LEARNING_RATE,
        "early_stop_after_lr_drops": PHASE6S_RANK5_ADAPTIVE_EARLY_STOP_AFTER_LR_DROPS,
        "serialize_trained_cores": True,
        "validation_holdout_role": "candidate_selection_and_veto_not_audit_not_production",
        "audit_cloud_role": "reserved_final_only_not_tuning",
    }
    regularization_protocol = {
        "regularization_tuning": True,
        "default_policy": ZHAO_CUI_L1_TUNING_DEFAULT_POLICY,
        "selection_status": ZHAO_CUI_L1_TUNING_SELECTION_STATUS,
        "candidate_l1_grid": tuple(arm["l1_weight"] for arm in candidate_arms),
        "candidate_learning_rate_grid": (PHASE6V_L1_SELECTION_LEARNING_RATE,),
        "l2_weight": PHASE6V_L1_SELECTION_L2_WEIGHT,
        "logz_anchor_weight": PHASE6V_L1_SELECTION_LOGZ_ANCHOR_WEIGHT,
        "grid_execution_status": "not_executed_preflight_only",
        "validation_holdout_role": "candidate_selection_and_veto_not_audit_not_production",
        "audit_cloud_role": "reserved_final_only_not_tuning",
    }
    selection_rule = {
        "veto_first": True,
        "holdout_threshold": PHASE6V_L1_SELECTION_HOLDOUT_THRESHOLD,
        "zero_l1_comparator_required": True,
        "positive_l1_minimum_improvement": "max(0.005, 0.05 * zero_l1_holdout)",
        "tie_policy": (
            "select zero-L1 comparator if no positive-L1 arm clears the "
            "minimum improvement margin and zero-L1 passes all vetoes"
        ),
        "block_policy": "block if no arm passes holdout threshold and vetoes",
    }
    phase6v_status_fields = {
        "regularization_protocol_status": "ok",
        "candidate_arm_count_status": "ok" if len(candidate_arms) == 4 else "block",
        "new_arm_exact_guard_status": "ok",
        "reuse_arm_protocol_equivalence_status": reuse_validation["status"],
        "selection_rule_status": "ok",
        "audit_tuning_status": "not_used_for_tuning",
        "fit_execution_status": "not_executed",
        "convergence_interpretation_status": "preflight_only_no_rank_convergence_claim",
        "phase7_status": "blocked_until_later_same_policy_rank_degree_gate",
    }
    overall = payload["gate_summary"]["overall_status"]
    if reuse_validation["status"] != "ok":
        overall = "block"
    return {
        **payload,
        "status": (
            STATUS_PHASE6V_L1_SELECTION_PREFLIGHT_READY
            if overall == "ready_for_exact_claude_agreed_execution"
            else "BLOCK_P86_PHASE6V_L1_SELECTION_PREFLIGHT"
        ),
        "candidate_fit_command": PHASE6V_L1_SELECTION_L1_0_FIT_COMMAND,
        "candidate_arms": candidate_arms,
        "candidate_fit_commands": {
            "rank5_lr3e-4_l1_0": PHASE6V_L1_SELECTION_L1_0_FIT_COMMAND,
            "rank5_lr3e-4_l1_3e-10": PHASE6V_L1_SELECTION_L1_3E_10_FIT_COMMAND,
            "rank5_lr3e-4_l1_3e-9": PHASE6V_L1_SELECTION_L1_3E_9_FIT_COMMAND,
        },
        "reuse_arm_validation": reuse_validation,
        "adaptive_training_protocol": adaptive_protocol,
        "regularization_protocol": regularization_protocol,
        "selection_rule": selection_rule,
        "optimizer_budget": {
            **payload["optimizer_budget"],
            "max_train_steps": PHASE6V_L1_SELECTION_TRAIN_STEPS,
            "adaptive_training": True,
            "validation_check_every": PHASE6S_RANK5_ADAPTIVE_VALIDATION_CHECK_EVERY,
            "plateau_patience": PHASE6S_RANK5_ADAPTIVE_PLATEAU_PATIENCE,
            "plateau_min_delta": PHASE6S_RANK5_ADAPTIVE_PLATEAU_MIN_DELTA,
            "lr_reduction_factor": DEFAULT_LR_REDUCTION_FACTOR,
            "min_learning_rate": DEFAULT_MIN_LEARNING_RATE,
            "early_stop_after_lr_drops": PHASE6S_RANK5_ADAPTIVE_EARLY_STOP_AFTER_LR_DROPS,
            "serialize_trained_cores": True,
            "training_convergence_policy": (
                "scheduler_stop_required_for_candidate_selection; "
                "validation selection is not rank convergence evidence"
            ),
        },
        "phase6v_status_fields": phase6v_status_fields,
        "reviewed_prerequisites": {
            "phase6t_l1_diagnostic_artifact": str(phase6t_path),
            "phase6t_l1_diagnostic_status": phase6t.get("status"),
            "phase6t_l1_holdout_residual": phase6t.get("holdout_residual"),
            "phase6t_l1_normalizer": phase6t.get("normalizer"),
            "phase6t_l1_validation_trace_len": len(phase6t.get("validation_trace") or ()),
        },
        "gate_summary": {
            **payload["gate_summary"],
            **phase6v_status_fields,
            "overall_status": (
                "ready_for_exact_claude_agreed_execution"
                if overall == "ready_for_exact_claude_agreed_execution"
                else "block"
            ),
        },
    }


def _phase6w_rank4_candidate_arms() -> tuple[Mapping[str, Any], ...]:
    return (
        {
            "arm_id": "rank4_lr3e-4_l1_0",
            "role": "zero_l1_comparator",
            "l1_weight": 0.0,
            "execution": "new_fit_requires_exact_claude_agreed_handoff",
            "output": str(PHASE6W_RANK4_L1_0_OUTPUT),
            "candidate_fit_command": PHASE6W_RANK4_L1_0_FIT_COMMAND,
        },
        {
            "arm_id": "rank4_lr3e-4_l1_3e-10",
            "role": "positive_l1_candidate",
            "l1_weight": 3e-10,
            "execution": "new_fit_requires_exact_claude_agreed_handoff",
            "output": str(PHASE6W_RANK4_L1_3E_10_OUTPUT),
            "candidate_fit_command": PHASE6W_RANK4_L1_3E_10_FIT_COMMAND,
        },
        {
            "arm_id": "rank4_lr3e-4_l1_1e-9",
            "role": "positive_l1_candidate",
            "l1_weight": 1e-9,
            "execution": "new_fit_requires_exact_claude_agreed_handoff",
            "output": str(PHASE6W_RANK4_L1_1E_9_OUTPUT),
            "candidate_fit_command": PHASE6W_RANK4_L1_1E_9_FIT_COMMAND,
        },
        {
            "arm_id": "rank4_lr3e-4_l1_3e-9",
            "role": "positive_l1_candidate",
            "l1_weight": 3e-9,
            "execution": "new_fit_requires_exact_claude_agreed_handoff",
            "output": str(PHASE6W_RANK4_L1_3E_9_OUTPUT),
            "candidate_fit_command": PHASE6W_RANK4_L1_3E_9_FIT_COMMAND,
        },
    )


def _phase6w_rank4_fit_arm_expectations() -> Mapping[Path, Mapping[str, Any]]:
    common = {
        "preflight_json": PHASE6W_SAME_POLICY_RANK_PREFLIGHT_OUTPUT,
        "target_dimension": 36,
        "fit_rank": PHASE6W_RANK4_FIT_RANK,
        "training_sample_count": PHASE6W_RANK4_TRAINING_SAMPLE_COUNT,
        "holdout_sample_count": 65536,
        "audit_sample_count": 65536,
        "seed": PHASE6_RANK5_SEED,
        "optimizer_batch_size": DEFAULT_OPTIMIZER_BATCH_SIZE,
        "prefit_steps": DEFAULT_PREFIT_STEPS,
        "train_steps": PHASE6W_RANK4_TRAIN_STEPS,
        "learning_rate": PHASE6W_RANK4_LEARNING_RATE,
        "l2_weight": PHASE6W_RANK4_L2_WEIGHT,
        "logz_anchor_weight": PHASE6W_RANK4_LOGZ_ANCHOR_WEIGHT,
        "max_seconds": PHASE6W_RANK4_MAX_SECONDS,
        "memory_cap_mib": 12288,
        "train_prior_seed": PHASE6_RANK5_TRAIN_PRIOR_SEED,
        "train_process_seed": PHASE6_RANK5_TRAIN_PROCESS_SEED,
        "holdout_prior_seed": PHASE6_RANK5_HOLDOUT_PRIOR_SEED,
        "holdout_process_seed": PHASE6_RANK5_HOLDOUT_PROCESS_SEED,
        "audit_prior_seed": PHASE6_RANK5_AUDIT_PRIOR_SEED,
        "audit_process_seed": PHASE6_RANK5_AUDIT_PROCESS_SEED,
        "adaptive_training": True,
        "validation_check_every": PHASE6S_RANK5_ADAPTIVE_VALIDATION_CHECK_EVERY,
        "plateau_patience": PHASE6S_RANK5_ADAPTIVE_PLATEAU_PATIENCE,
        "plateau_min_delta": PHASE6S_RANK5_ADAPTIVE_PLATEAU_MIN_DELTA,
        "lr_reduction_factor": DEFAULT_LR_REDUCTION_FACTOR,
        "min_learning_rate": DEFAULT_MIN_LEARNING_RATE,
        "early_stop_after_lr_drops": PHASE6S_RANK5_ADAPTIVE_EARLY_STOP_AFTER_LR_DROPS,
        "serialize_trained_cores": True,
    }
    return {
        PHASE6W_RANK4_L1_0_OUTPUT: {
            **common,
            "output": PHASE6W_RANK4_L1_0_OUTPUT,
            "l1_weight": 0.0,
            "candidate_fit_command": PHASE6W_RANK4_L1_0_FIT_COMMAND,
        },
        PHASE6W_RANK4_L1_3E_10_OUTPUT: {
            **common,
            "output": PHASE6W_RANK4_L1_3E_10_OUTPUT,
            "l1_weight": 3e-10,
            "candidate_fit_command": PHASE6W_RANK4_L1_3E_10_FIT_COMMAND,
        },
        PHASE6W_RANK4_L1_1E_9_OUTPUT: {
            **common,
            "output": PHASE6W_RANK4_L1_1E_9_OUTPUT,
            "l1_weight": 1e-9,
            "candidate_fit_command": PHASE6W_RANK4_L1_1E_9_FIT_COMMAND,
        },
        PHASE6W_RANK4_L1_3E_9_OUTPUT: {
            **common,
            "output": PHASE6W_RANK4_L1_3E_9_OUTPUT,
            "l1_weight": 3e-9,
            "candidate_fit_command": PHASE6W_RANK4_L1_3E_9_FIT_COMMAND,
        },
    }


def validate_phase6w_selected_rank5_reuse_arm(
    payload: Mapping[str, Any],
) -> Mapping[str, Any]:
    statuses = payload.get("post_fit_statuses", {})
    rank_budget = payload.get("rank_budget", {})
    optimizer_budget = payload.get("optimizer_budget", {})
    route = payload.get("route_manifest", {})
    training_protocol = (
        payload.get("training_summary", {}).get("training_protocol", {})
    )
    training_config = payload.get("training_config", {})
    fit_manifest = payload.get("fit_data_manifest", {})
    selection_context = payload.get("phase6v_selection_context", {})
    nonclaims = tuple(payload.get("nonclaims") or ())
    required_nonclaim_fragments = (
        "no rank convergence claim",
        "no HMC readiness claim",
        "no LEDH comparison claim",
        "no production readiness claim",
        "not a source-faithful author TT-cross proof",
    )
    field_statuses = {
        "artifact_path": payload.get("output") == str(PHASE6V_L1_SELECTION_L1_0_OUTPUT),
        "preflight_path": (
            payload.get("preflight_json")
            == str(PHASE6V_L1_SELECTION_PREFLIGHT_OUTPUT)
        ),
        "command": payload.get("command") == PHASE6V_L1_SELECTION_L1_0_FIT_COMMAND,
        "status": payload.get("status") == STATUS_PHASE6V_L1_SELECTION_COMPLETED,
        "fit_executed": payload.get("fit_executed") is True,
        "training_backend": payload.get("training_backend") == TRAINING_BACKEND,
        "target_dimension": route.get("target_dimension") == 36,
        "fit_rank": rank_budget.get("fit_rank") == PHASE6_RANK5_FIT_RANK,
        "training_sample_count": (
            rank_budget.get("training_sample_count")
            == PHASE6_RANK5_TRAINING_SAMPLE_COUNT
        ),
        "holdout_sample_count": fit_manifest.get("holdout_sample_count") == 65536,
        "learning_rate": (
            float(optimizer_budget.get("learning_rate"))
            == PHASE6V_L1_SELECTION_LEARNING_RATE
        ),
        "selected_l1_weight": (
            float(training_protocol.get("l1_weight")) == 0.0
            and float(training_config.get("l1_weight")) == 0.0
        ),
        "l2_weight": (
            float(training_protocol.get("l2_weight"))
            == PHASE6V_L1_SELECTION_L2_WEIGHT
            and float(training_config.get("l2_weight"))
            == PHASE6V_L1_SELECTION_L2_WEIGHT
        ),
        "logz_anchor_weight": (
            float(training_protocol.get("logz_anchor_weight"))
            == PHASE6V_L1_SELECTION_LOGZ_ANCHOR_WEIGHT
            and float(training_config.get("logz_anchor_weight"))
            == PHASE6V_L1_SELECTION_LOGZ_ANCHOR_WEIGHT
        ),
        "adaptive_scheduler": (
            optimizer_budget.get("adaptive_training") is True
            and optimizer_budget.get("validation_check_every")
            == PHASE6S_RANK5_ADAPTIVE_VALIDATION_CHECK_EVERY
            and optimizer_budget.get("plateau_patience")
            == PHASE6S_RANK5_ADAPTIVE_PLATEAU_PATIENCE
            and float(optimizer_budget.get("plateau_min_delta"))
            == PHASE6S_RANK5_ADAPTIVE_PLATEAU_MIN_DELTA
            and float(optimizer_budget.get("lr_reduction_factor"))
            == DEFAULT_LR_REDUCTION_FACTOR
            and float(optimizer_budget.get("min_learning_rate"))
            == DEFAULT_MIN_LEARNING_RATE
            and optimizer_budget.get("early_stop_after_lr_drops")
            == PHASE6S_RANK5_ADAPTIVE_EARLY_STOP_AFTER_LR_DROPS
            and optimizer_budget.get("serialize_trained_cores") is True
        ),
        "train_seeds": (
            fit_manifest.get("train_prior_seed") == PHASE6_RANK5_TRAIN_PRIOR_SEED
            and fit_manifest.get("train_process_seed")
            == PHASE6_RANK5_TRAIN_PROCESS_SEED
        ),
        "holdout_seeds": (
            fit_manifest.get("holdout_prior_seed")
            == PHASE6_RANK5_HOLDOUT_PRIOR_SEED
            and fit_manifest.get("holdout_process_seed")
            == PHASE6_RANK5_HOLDOUT_PROCESS_SEED
        ),
        "route": (
            route.get("target_id") == "zhao_cui_sir_austria_d18"
            and route.get("basis_family") == "lagrangep"
            and route.get("basis_order") == 4
            and route.get("basis_num_elems") == 8
            and route.get("basis_dim_per_dimension") == 33
            and route.get("domain_map") == "algebraic"
            and float(route.get("domain_scale")) == 1.0
            and route.get("density_measure") == DensityMeasure.REFERENCE_MEASURE.value
            and route.get("mass_measure") == MassMeasure.REFERENCE_MEASURE.value
            and isinstance(route.get("xla_static_fields"), list)
            and "basis_family" in route.get("xla_static_fields", ())
        ),
        "phase6v_selection_context": (
            selection_context.get("candidate_fit_commands", {}).get(
                "rank5_lr3e-4_l1_0"
            )
            == PHASE6V_L1_SELECTION_L1_0_FIT_COMMAND
            and selection_context.get("selection_rule", {}).get(
                "zero_l1_comparator_required"
            )
            is True
        ),
        "serialized_cores": (
            payload.get("trained_core_serialization", {}).get("status")
            == "serialized_with_values"
        ),
        "post_fit_statuses": (
            statuses.get("finite_fit_residual_status") == "ok"
            and statuses.get("finite_holdout_residual_status") == "ok"
            and statuses.get("finite_normalizer_status") == "ok"
            and statuses.get("finite_sqrt_square_normalizer_status") == "ok"
            and statuses.get("fallback_route_status") == "not_used"
            and statuses.get("audit_cloud_tuning_status") == "not_used_for_tuning"
            and statuses.get("runtime_status") == "within_approved_envelope"
            and statuses.get("memory_status") == "within_approved_envelope"
        ),
        "nonclaims": all(
            any(fragment in claim for claim in nonclaims)
            for fragment in required_nonclaim_fragments
        ),
    }
    return {
        "status": "ok" if all(field_statuses.values()) else "block",
        "artifact": str(PHASE6V_L1_SELECTION_L1_0_OUTPUT),
        "validation_kind": "selected_phase6v_rank5_protocol_equivalence",
        "field_statuses": field_statuses,
    }


def build_phase6w_same_policy_rank_preflight_payload(
    *,
    output: Path = PHASE6W_SAME_POLICY_RANK_PREFLIGHT_OUTPUT,
) -> Mapping[str, Any]:
    selected_rank5_path = Path(PHASE6V_L1_SELECTION_L1_0_OUTPUT)
    phase6v_ledger_path = Path(
        "docs/plans/"
        "bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-convergence-ledger-2026-06-25.json"
    )
    selected_rank5 = json.loads(selected_rank5_path.read_text())
    phase6v_ledger = json.loads(phase6v_ledger_path.read_text())
    reuse_validation = validate_phase6w_selected_rank5_reuse_arm(selected_rank5)
    phase6v_selection = phase6v_ledger.get("selection_decision", {})
    ledger_field_statuses = {
        "status": (
            phase6v_ledger.get("status")
            == "P86_PHASE6V_L1_SELECTION_CONVERGENCE_REVIEWED"
        ),
        "selected_artifact": (
            phase6v_selection.get("selected_artifact")
            == str(PHASE6V_L1_SELECTION_L1_0_OUTPUT)
        ),
        "selected_l1_weight": float(
            phase6v_selection.get("selected_l1_weight", math.nan)
        )
        == 0.0,
        "positive_l1_margin_pass": (
            phase6v_selection.get("positive_l1_margin_pass") is False
        ),
        "selected_holdout_residual": _finite_nonnegative_float(
            phase6v_selection.get("selected_holdout_residual", math.nan)
        ),
    }
    ledger_validation = {
        "status": "ok" if all(ledger_field_statuses.values()) else "block",
        "artifact": str(phase6v_ledger_path),
        "validation_kind": "reviewed_phase6v_selection_ledger",
        "field_statuses": ledger_field_statuses,
    }
    payload = build_preflight_payload(
        output=output,
        target_dimension=36,
        fit_rank=PHASE6W_RANK4_FIT_RANK,
        training_sample_count=PHASE6W_RANK4_TRAINING_SAMPLE_COUNT,
        holdout_sample_count=65536,
        audit_sample_count=65536,
        seed=PHASE6_RANK5_SEED,
        optimizer_batch_size=DEFAULT_OPTIMIZER_BATCH_SIZE,
        prefit_steps=DEFAULT_PREFIT_STEPS,
        train_steps=PHASE6W_RANK4_TRAIN_STEPS,
        learning_rate=PHASE6W_RANK4_LEARNING_RATE,
        l1_weight=DEFAULT_L1_WEIGHT,
        l2_weight=PHASE6W_RANK4_L2_WEIGHT,
        logz_anchor_weight=PHASE6W_RANK4_LOGZ_ANCHOR_WEIGHT,
        max_seconds=PHASE6W_RANK4_MAX_SECONDS,
        memory_cap_mib=12288,
        command=PHASE6W_SAME_POLICY_RANK_PREFLIGHT_COMMAND,
        candidate_fit_command=PHASE6W_RANK4_L1_0_FIT_COMMAND,
        expected_output=PHASE6W_SAME_POLICY_RANK_PREFLIGHT_OUTPUT,
        expected_fit_output=PHASE6W_RANK4_L1_0_OUTPUT,
        expected_p_theta=18216,
        status_ready=STATUS_PHASE6W_SAME_POLICY_RANK_PREFLIGHT_READY,
        block_status="BLOCK_P86_PHASE6W_SAME_POLICY_RANK_PREFLIGHT",
        schema_version="p86_phase6w_same_policy_rank_convergence_preflight.v1",
        phase_name="P86 Phase 6W same-policy rank convergence preflight",
        phase_subplan=(
            "docs/plans/"
            "bayesfilter-highdim-zhao-cui-p86-phase6w-same-policy-rank-degree-convergence-subplan-2026-06-25.md"
        ),
        phase_result=(
            "docs/plans/"
            "bayesfilter-highdim-zhao-cui-p86-phase6w-same-policy-rank-convergence-preflight-guard-result-2026-06-25.md"
        ),
        rank_rung="author_basis_rung_F_rank4_same_policy_l1_selection",
        label_prefix="p86-phase6w-rank4-l1-selection",
        train_prior_seed=PHASE6_RANK5_TRAIN_PRIOR_SEED,
        train_process_seed=PHASE6_RANK5_TRAIN_PROCESS_SEED,
        holdout_prior_seed=PHASE6_RANK5_HOLDOUT_PRIOR_SEED,
        holdout_process_seed=PHASE6_RANK5_HOLDOUT_PROCESS_SEED,
        audit_prior_seed=PHASE6_RANK5_AUDIT_PRIOR_SEED,
        audit_process_seed=PHASE6_RANK5_AUDIT_PROCESS_SEED,
        nonclaims=PHASE6W_PREFLIGHT_NONCLAIMS,
        lower_rung_artifact=None,
    )
    candidate_arms = _phase6w_rank4_candidate_arms()
    adaptive_protocol = {
        "adaptive_training": True,
        "optimizer_identity": TRAINING_BACKEND,
        "optimizer": "Adam",
        "validation_check_every": PHASE6S_RANK5_ADAPTIVE_VALIDATION_CHECK_EVERY,
        "plateau_patience": PHASE6S_RANK5_ADAPTIVE_PLATEAU_PATIENCE,
        "plateau_min_delta": PHASE6S_RANK5_ADAPTIVE_PLATEAU_MIN_DELTA,
        "lr_reduction_factor": DEFAULT_LR_REDUCTION_FACTOR,
        "min_learning_rate": DEFAULT_MIN_LEARNING_RATE,
        "early_stop_after_lr_drops": PHASE6S_RANK5_ADAPTIVE_EARLY_STOP_AFTER_LR_DROPS,
        "serialize_trained_cores": True,
        "validation_holdout_role": "candidate_selection_and_veto_not_audit_not_production",
        "audit_cloud_role": "reserved_final_only_not_tuning",
    }
    regularization_protocol = {
        "regularization_tuning": True,
        "default_policy": ZHAO_CUI_L1_TUNING_DEFAULT_POLICY,
        "selection_status": ZHAO_CUI_L1_TUNING_SELECTION_STATUS,
        "candidate_l1_grid": tuple(arm["l1_weight"] for arm in candidate_arms),
        "candidate_learning_rate_grid": (PHASE6W_RANK4_LEARNING_RATE,),
        "l2_weight": PHASE6W_RANK4_L2_WEIGHT,
        "logz_anchor_weight": PHASE6W_RANK4_LOGZ_ANCHOR_WEIGHT,
        "grid_execution_status": "not_executed_preflight_only",
        "validation_holdout_role": "candidate_selection_and_veto_not_audit_not_production",
        "audit_cloud_role": "reserved_final_only_not_tuning",
    }
    rank4_selection_rule = {
        "veto_first": True,
        "holdout_threshold": PHASE6V_L1_SELECTION_HOLDOUT_THRESHOLD,
        "zero_l1_comparator_required": True,
        "positive_l1_minimum_improvement": "max(0.005, 0.05 * rank4_zero_l1_holdout)",
        "tie_policy": (
            "select rank-4 zero-L1 comparator if no positive-L1 arm clears "
            "the minimum improvement margin and zero-L1 passes all vetoes"
        ),
        "block_policy": "block if no rank-4 arm passes holdout threshold and vetoes",
        "audit_cloud_selection": "forbidden",
    }
    adjacent_rank_stability_rule = {
        "selected_rank5_artifact": str(PHASE6V_L1_SELECTION_L1_0_OUTPUT),
        "selected_rank5_l1_weight": 0.0,
        "selected_rank5_holdout_residual": selected_rank5.get("holdout_residual"),
        "rank_stability_formula": (
            "abs(rank5_selected_holdout - rank4_selected_holdout) "
            "<= max(0.005, 0.05 * rank4_selected_holdout)"
        ),
        "large_improvement_policy": (
            "larger rank-5 improvement blocks rank convergence rather than "
            "passing it; consider later reviewed rank-6/model-selection diagnostic"
        ),
        "large_regression_policy": "larger rank-5 regression blocks rank convergence",
    }
    phase5_rank4_context = {
        "artifact": str(FIT_OUTPUT),
        "context_status": "historical_only_not_same_policy_lower_rung",
        "reason": (
            "Phase 5 used a different optimizer schedule and did not run the "
            "reviewed L1-selection protocol."
        ),
        "same_policy_lower_rung_status": "not_allowed",
    }
    phase6w_status_fields = {
        "candidate_arm_count_status": "ok" if len(candidate_arms) == 4 else "block",
        "rank4_sample_floor_status": (
            "ok"
            if payload["rank_budget"]["minimum_training_samples"]
            == PHASE6W_RANK4_TRAINING_SAMPLE_COUNT
            else "block"
        ),
        "new_arm_exact_guard_status": "ok",
        "selected_rank5_reuse_status": reuse_validation["status"],
        "phase6v_selection_ledger_status": ledger_validation["status"],
        "phase5_rank4_context_status": "historical_only_not_same_policy_lower_rung",
        "same_policy_rank4_execution_status": "not_executed_requires_exact_claude_agreed_handoff",
        "rank_convergence_interpretation_status": "preflight_only_no_rank_convergence_claim",
        "degree_convergence_status": "blocked_pending_reviewed_configurable_basis_path",
        "phase7_status": "blocked_until_same_policy_rank_degree_gate_passes_or_owner_reframes",
        "audit_tuning_status": "not_used_for_tuning",
    }
    overall = payload["gate_summary"]["overall_status"]
    if reuse_validation["status"] != "ok" or ledger_validation["status"] != "ok":
        overall = "block"
    return {
        **payload,
        "status": (
            STATUS_PHASE6W_SAME_POLICY_RANK_PREFLIGHT_READY
            if overall == "ready_for_exact_claude_agreed_execution"
            else "BLOCK_P86_PHASE6W_SAME_POLICY_RANK_PREFLIGHT"
        ),
        "candidate_fit_command": PHASE6W_RANK4_L1_0_FIT_COMMAND,
        "candidate_arms": candidate_arms,
        "candidate_fit_commands": {
            "rank4_lr3e-4_l1_0": PHASE6W_RANK4_L1_0_FIT_COMMAND,
            "rank4_lr3e-4_l1_3e-10": PHASE6W_RANK4_L1_3E_10_FIT_COMMAND,
            "rank4_lr3e-4_l1_1e-9": PHASE6W_RANK4_L1_1E_9_FIT_COMMAND,
            "rank4_lr3e-4_l1_3e-9": PHASE6W_RANK4_L1_3E_9_FIT_COMMAND,
        },
        "selected_rank5_reuse_validation": reuse_validation,
        "phase6v_selection_ledger_validation": ledger_validation,
        "phase5_rank4_historical_context": phase5_rank4_context,
        "adaptive_training_protocol": adaptive_protocol,
        "regularization_protocol": regularization_protocol,
        "rank4_selection_rule": rank4_selection_rule,
        "adjacent_rank_stability_rule": adjacent_rank_stability_rule,
        "optimizer_budget": {
            **payload["optimizer_budget"],
            "max_train_steps": PHASE6W_RANK4_TRAIN_STEPS,
            "adaptive_training": True,
            "validation_check_every": PHASE6S_RANK5_ADAPTIVE_VALIDATION_CHECK_EVERY,
            "plateau_patience": PHASE6S_RANK5_ADAPTIVE_PLATEAU_PATIENCE,
            "plateau_min_delta": PHASE6S_RANK5_ADAPTIVE_PLATEAU_MIN_DELTA,
            "lr_reduction_factor": DEFAULT_LR_REDUCTION_FACTOR,
            "min_learning_rate": DEFAULT_MIN_LEARNING_RATE,
            "early_stop_after_lr_drops": PHASE6S_RANK5_ADAPTIVE_EARLY_STOP_AFTER_LR_DROPS,
            "serialize_trained_cores": True,
            "training_convergence_policy": (
                "scheduler_stop_required_for_candidate_selection; "
                "validation selection is not rank convergence evidence"
            ),
        },
        "phase6w_status_fields": phase6w_status_fields,
        "reviewed_prerequisites": {
            "phase6v_selected_rank5_artifact": str(selected_rank5_path),
            "phase6v_selected_rank5_status": selected_rank5.get("status"),
            "phase6v_selected_rank5_holdout_residual": selected_rank5.get("holdout_residual"),
            "phase6v_selected_rank5_normalizer": selected_rank5.get("normalizer"),
            "phase6v_selection_ledger": str(phase6v_ledger_path),
            "phase6v_selection_ledger_status": phase6v_ledger.get("status"),
        },
        "gate_summary": {
            **payload["gate_summary"],
            **phase6w_status_fields,
            "overall_status": (
                "ready_for_exact_claude_agreed_execution"
                if overall == "ready_for_exact_claude_agreed_execution"
                else "block"
            ),
        },
    }


def _load_preflight(path: Path) -> Mapping[str, Any]:
    data = json.loads(path.read_text())
    if data.get("status") not in {
        STATUS_PREFLIGHT_READY,
        STATUS_PHASE6_RANK_PREFLIGHT_READY,
        STATUS_PHASE6S_ADAPTIVE_RANK5_PREFLIGHT_READY,
        STATUS_PHASE6T_L1_TUNING_PREFLIGHT_READY,
        STATUS_PHASE6V_L1_SELECTION_PREFLIGHT_READY,
        STATUS_PHASE6W_SAME_POLICY_RANK_PREFLIGHT_READY,
        STATUS_PHASE6Y_DEGREE_COMPARATOR_PREFLIGHT_READY,
        STATUS_P88_PHASE2_DEGREE_COMPARATOR_PREFLIGHT_READY,
    }:
        raise ValueError("fit requires a ready reviewed preflight artifact")
    if data.get("fit_executed") is not False:
        raise ValueError("preflight artifact must be no-fit")
    return data


def _expected_fit_args_for_preflight(preflight: Mapping[str, Any]) -> Mapping[str, Any]:
    basis_order = int(preflight.get("basis_config", {}).get("basis_order", P85_AUTHOR_SIR_LAGRANGEP_ORDER))
    basis_num_elems = int(preflight.get("basis_config", {}).get("basis_num_elems", P85_AUTHOR_SIR_LAGRANGEP_NUM_ELEMS))
    if preflight.get("status") in {
        STATUS_PHASE6Y_DEGREE_COMPARATOR_PREFLIGHT_READY,
        STATUS_P88_PHASE2_DEGREE_COMPARATOR_PREFLIGHT_READY,
    }:
        output = Path(preflight.get("_requested_output", ""))
        expected_by_output = _phase6y_degree_order3_fit_expectations()
        if output not in expected_by_output:
            raise ValueError("Phase 6Y fit output is not a frozen degree candidate")
        return expected_by_output[output]
    if preflight.get("status") == STATUS_PHASE6W_SAME_POLICY_RANK_PREFLIGHT_READY:
        output = Path(preflight.get("_requested_output", ""))
        expected_by_output = _phase6w_rank4_fit_arm_expectations()
        if output not in expected_by_output:
            raise ValueError("Phase 6W fit output is not a frozen rank-4 candidate")
        return {
            **expected_by_output[output],
            "basis_order": basis_order,
            "basis_num_elems": basis_num_elems,
        }
    if preflight.get("status") == STATUS_PHASE6V_L1_SELECTION_PREFLIGHT_READY:
        output = Path(preflight.get("_requested_output", ""))
        expected_by_output = _phase6v_new_fit_arm_expectations()
        if output not in expected_by_output:
            raise ValueError("Phase 6V fit output is not a frozen new-arm candidate")
        return {
            **expected_by_output[output],
            "basis_order": basis_order,
            "basis_num_elems": basis_num_elems,
        }
    if preflight.get("status") == STATUS_PHASE6T_L1_TUNING_PREFLIGHT_READY:
        return {
            "output": PHASE6T_L1_TUNING_DIAGNOSTIC_OUTPUT,
            "preflight_json": PHASE6T_L1_TUNING_PREFLIGHT_OUTPUT,
            "target_dimension": 36,
            "fit_rank": PHASE6_RANK5_FIT_RANK,
            "training_sample_count": PHASE6_RANK5_TRAINING_SAMPLE_COUNT,
            "holdout_sample_count": 65536,
            "audit_sample_count": 65536,
            "seed": PHASE6_RANK5_SEED,
            "optimizer_batch_size": DEFAULT_OPTIMIZER_BATCH_SIZE,
            "prefit_steps": DEFAULT_PREFIT_STEPS,
            "train_steps": PHASE6T_L1_TUNING_TRAIN_STEPS,
            "learning_rate": PHASE6T_L1_TUNING_LEARNING_RATE,
            "l1_weight": PHASE6T_L1_TUNING_L1_WEIGHT,
            "l2_weight": PHASE6T_L1_TUNING_L2_WEIGHT,
            "logz_anchor_weight": PHASE6T_L1_TUNING_LOGZ_ANCHOR_WEIGHT,
            "max_seconds": PHASE6T_L1_TUNING_MAX_SECONDS,
            "memory_cap_mib": 12288,
            "train_prior_seed": PHASE6_RANK5_TRAIN_PRIOR_SEED,
            "train_process_seed": PHASE6_RANK5_TRAIN_PROCESS_SEED,
            "holdout_prior_seed": PHASE6_RANK5_HOLDOUT_PRIOR_SEED,
            "holdout_process_seed": PHASE6_RANK5_HOLDOUT_PROCESS_SEED,
            "audit_prior_seed": PHASE6_RANK5_AUDIT_PRIOR_SEED,
            "audit_process_seed": PHASE6_RANK5_AUDIT_PROCESS_SEED,
            "adaptive_training": True,
            "validation_check_every": PHASE6S_RANK5_ADAPTIVE_VALIDATION_CHECK_EVERY,
            "plateau_patience": PHASE6S_RANK5_ADAPTIVE_PLATEAU_PATIENCE,
            "plateau_min_delta": PHASE6S_RANK5_ADAPTIVE_PLATEAU_MIN_DELTA,
            "lr_reduction_factor": DEFAULT_LR_REDUCTION_FACTOR,
            "min_learning_rate": DEFAULT_MIN_LEARNING_RATE,
            "early_stop_after_lr_drops": PHASE6S_RANK5_ADAPTIVE_EARLY_STOP_AFTER_LR_DROPS,
            "serialize_trained_cores": True,
            "basis_order": basis_order,
            "basis_num_elems": basis_num_elems,
            "candidate_fit_command": PHASE6T_L1_TUNING_FIT_COMMAND,
        }
    if preflight.get("status") == STATUS_PHASE6S_ADAPTIVE_RANK5_PREFLIGHT_READY:
        return {
            "output": PHASE6S_RANK5_ADAPTIVE_FIT_OUTPUT,
            "preflight_json": PHASE6S_RANK5_ADAPTIVE_PREFLIGHT_OUTPUT,
            "target_dimension": 36,
            "fit_rank": PHASE6_RANK5_FIT_RANK,
            "training_sample_count": PHASE6_RANK5_TRAINING_SAMPLE_COUNT,
            "holdout_sample_count": 65536,
            "audit_sample_count": 65536,
            "seed": PHASE6_RANK5_SEED,
            "optimizer_batch_size": DEFAULT_OPTIMIZER_BATCH_SIZE,
            "prefit_steps": DEFAULT_PREFIT_STEPS,
            "train_steps": PHASE6S_RANK5_ADAPTIVE_TRAIN_STEPS,
            "learning_rate": DEFAULT_LEARNING_RATE,
            "l1_weight": DEFAULT_L1_WEIGHT,
            "l2_weight": DEFAULT_L2_WEIGHT,
            "logz_anchor_weight": DEFAULT_LOGZ_ANCHOR_WEIGHT,
            "max_seconds": 14400,
            "memory_cap_mib": 12288,
            "train_prior_seed": PHASE6_RANK5_TRAIN_PRIOR_SEED,
            "train_process_seed": PHASE6_RANK5_TRAIN_PROCESS_SEED,
            "holdout_prior_seed": PHASE6_RANK5_HOLDOUT_PRIOR_SEED,
            "holdout_process_seed": PHASE6_RANK5_HOLDOUT_PROCESS_SEED,
            "audit_prior_seed": PHASE6_RANK5_AUDIT_PRIOR_SEED,
            "audit_process_seed": PHASE6_RANK5_AUDIT_PROCESS_SEED,
            "adaptive_training": True,
            "validation_check_every": PHASE6S_RANK5_ADAPTIVE_VALIDATION_CHECK_EVERY,
            "plateau_patience": PHASE6S_RANK5_ADAPTIVE_PLATEAU_PATIENCE,
            "plateau_min_delta": PHASE6S_RANK5_ADAPTIVE_PLATEAU_MIN_DELTA,
            "lr_reduction_factor": DEFAULT_LR_REDUCTION_FACTOR,
            "min_learning_rate": DEFAULT_MIN_LEARNING_RATE,
            "early_stop_after_lr_drops": PHASE6S_RANK5_ADAPTIVE_EARLY_STOP_AFTER_LR_DROPS,
            "serialize_trained_cores": True,
            "basis_order": basis_order,
            "basis_num_elems": basis_num_elems,
            "candidate_fit_command": PHASE6S_RANK5_ADAPTIVE_FIT_COMMAND,
        }
    if preflight.get("status") == STATUS_PHASE6_RANK_PREFLIGHT_READY:
        return {
            "output": PHASE6_RANK5_FIT_OUTPUT,
            "preflight_json": PHASE6_RANK_PREFLIGHT_OUTPUT,
            "target_dimension": 36,
            "fit_rank": PHASE6_RANK5_FIT_RANK,
            "training_sample_count": PHASE6_RANK5_TRAINING_SAMPLE_COUNT,
            "holdout_sample_count": 65536,
            "audit_sample_count": 65536,
            "seed": PHASE6_RANK5_SEED,
            "optimizer_batch_size": DEFAULT_OPTIMIZER_BATCH_SIZE,
            "prefit_steps": DEFAULT_PREFIT_STEPS,
            "train_steps": PHASE6_RANK5_TRAIN_STEPS,
            "learning_rate": DEFAULT_LEARNING_RATE,
            "l1_weight": DEFAULT_L1_WEIGHT,
            "l2_weight": DEFAULT_L2_WEIGHT,
            "logz_anchor_weight": DEFAULT_LOGZ_ANCHOR_WEIGHT,
            "max_seconds": 14400,
            "memory_cap_mib": 12288,
            "train_prior_seed": PHASE6_RANK5_TRAIN_PRIOR_SEED,
            "train_process_seed": PHASE6_RANK5_TRAIN_PROCESS_SEED,
            "holdout_prior_seed": PHASE6_RANK5_HOLDOUT_PRIOR_SEED,
            "holdout_process_seed": PHASE6_RANK5_HOLDOUT_PROCESS_SEED,
            "audit_prior_seed": PHASE6_RANK5_AUDIT_PRIOR_SEED,
            "audit_process_seed": PHASE6_RANK5_AUDIT_PROCESS_SEED,
            "adaptive_training": DEFAULT_ADAPTIVE_TRAINING,
            "validation_check_every": DEFAULT_VALIDATION_CHECK_EVERY,
            "plateau_patience": DEFAULT_PLATEAU_PATIENCE,
            "plateau_min_delta": DEFAULT_PLATEAU_MIN_DELTA,
            "lr_reduction_factor": DEFAULT_LR_REDUCTION_FACTOR,
            "min_learning_rate": DEFAULT_MIN_LEARNING_RATE,
            "early_stop_after_lr_drops": DEFAULT_EARLY_STOP_AFTER_LR_DROPS,
            "serialize_trained_cores": DEFAULT_SERIALIZE_TRAINED_CORES,
            "basis_order": basis_order,
            "basis_num_elems": basis_num_elems,
            "candidate_fit_command": PHASE6_RANK5_FIT_COMMAND,
        }
    return {
        "output": FIT_OUTPUT,
        "preflight_json": PREFLIGHT_OUTPUT,
        "target_dimension": 36,
        "fit_rank": 4,
        "training_sample_count": 364320,
        "holdout_sample_count": 65536,
        "audit_sample_count": 65536,
        "seed": 8605,
        "optimizer_batch_size": DEFAULT_OPTIMIZER_BATCH_SIZE,
        "prefit_steps": DEFAULT_PREFIT_STEPS,
        "train_steps": DEFAULT_TRAIN_STEPS,
        "learning_rate": DEFAULT_LEARNING_RATE,
        "l1_weight": DEFAULT_L1_WEIGHT,
        "l2_weight": DEFAULT_L2_WEIGHT,
        "logz_anchor_weight": DEFAULT_LOGZ_ANCHOR_WEIGHT,
        "max_seconds": 14400,
        "memory_cap_mib": 12288,
        "train_prior_seed": DEFAULT_TRAIN_PRIOR_SEED,
        "train_process_seed": DEFAULT_TRAIN_PROCESS_SEED,
        "holdout_prior_seed": DEFAULT_HOLDOUT_PRIOR_SEED,
        "holdout_process_seed": DEFAULT_HOLDOUT_PROCESS_SEED,
        "audit_prior_seed": DEFAULT_AUDIT_PRIOR_SEED,
        "audit_process_seed": DEFAULT_AUDIT_PROCESS_SEED,
        "adaptive_training": DEFAULT_ADAPTIVE_TRAINING,
        "validation_check_every": DEFAULT_VALIDATION_CHECK_EVERY,
        "plateau_patience": DEFAULT_PLATEAU_PATIENCE,
        "plateau_min_delta": DEFAULT_PLATEAU_MIN_DELTA,
        "lr_reduction_factor": DEFAULT_LR_REDUCTION_FACTOR,
        "min_learning_rate": DEFAULT_MIN_LEARNING_RATE,
        "early_stop_after_lr_drops": DEFAULT_EARLY_STOP_AFTER_LR_DROPS,
        "serialize_trained_cores": DEFAULT_SERIALIZE_TRAINED_CORES,
        "basis_order": basis_order,
        "basis_num_elems": basis_num_elems,
        "candidate_fit_command": FIT_COMMAND,
    }


def _guard_exact_fit_args(args: argparse.Namespace, preflight: Mapping[str, Any]) -> None:
    expected = _expected_fit_args_for_preflight(
        {**preflight, "_requested_output": str(args.output)}
    )
    if preflight.get("status") in {
        STATUS_PHASE6V_L1_SELECTION_PREFLIGHT_READY,
        STATUS_PHASE6W_SAME_POLICY_RANK_PREFLIGHT_READY,
        STATUS_PHASE6Y_DEGREE_COMPARATOR_PREFLIGHT_READY,
        STATUS_P88_PHASE2_DEGREE_COMPARATOR_PREFLIGHT_READY,
    }:
        candidate_commands = preflight.get("candidate_fit_commands", {})
        if expected["candidate_fit_command"] not in candidate_commands.values():
            raise ValueError("fit command drift from preflight artifact")
    elif preflight.get("candidate_fit_command") != expected["candidate_fit_command"]:
        raise ValueError("fit command drift from preflight artifact")
    for name, expected_value in expected.items():
        if name == "candidate_fit_command":
            continue
        observed = getattr(args, name)
        if isinstance(expected_value, Path):
            if Path(observed) != expected_value:
                raise ValueError(f"fit argument drift: {name}")
        elif observed != expected_value:
            raise ValueError(f"fit argument drift: {name}")
    if preflight["rank_budget"]["training_sample_count"] != expected["training_sample_count"]:
        raise ValueError("training sample count drift from preflight")
    if preflight["rank_budget"]["fit_rank"] != expected["fit_rank"]:
        raise ValueError("fit rank drift from preflight")
    if preflight["route_manifest"]["target_dimension"] != expected["target_dimension"]:
        raise ValueError("target dimension drift from preflight")
    if preflight.get("training_backend") != TRAINING_BACKEND:
        raise ValueError("training backend drift from preflight")
    if (
        preflight.get("historical_als_training_status")
        != HISTORICAL_ALS_TRAINING_STATUS
    ):
        raise ValueError("historical ALS demotion drift from preflight")
    basis_config = preflight.get("basis_config", {})
    if getattr(args, "basis_order", None) != int(
        basis_config.get("basis_order", P85_AUTHOR_SIR_LAGRANGEP_ORDER)
    ):
        raise ValueError("basis_order drift from preflight")
    if getattr(args, "basis_num_elems", None) != int(
        basis_config.get("basis_num_elems", P85_AUTHOR_SIR_LAGRANGEP_NUM_ELEMS)
    ):
        raise ValueError("basis_num_elems drift from preflight")
    optimizer_budget = preflight.get("optimizer_budget", {})
    if optimizer_budget.get("optimizer_batch_size") != expected["optimizer_batch_size"]:
        raise ValueError("optimizer batch size drift from preflight")
    if optimizer_budget.get("prefit_steps") != expected["prefit_steps"]:
        raise ValueError("prefit step drift from preflight")
    if optimizer_budget.get("train_steps") != expected["train_steps"]:
        raise ValueError("train step drift from preflight")
    if float(optimizer_budget.get("learning_rate")) != expected["learning_rate"]:
        raise ValueError("learning rate drift from preflight")
    regularization_budget = preflight.get("regularization_budget", {})
    for name in ("l1_weight", "l2_weight", "logz_anchor_weight"):
        if (
            preflight.get("status")
            in {
                STATUS_PHASE6V_L1_SELECTION_PREFLIGHT_READY,
                STATUS_PHASE6W_SAME_POLICY_RANK_PREFLIGHT_READY,
            }
            and name == "l1_weight"
        ):
            arm_matches = [
                arm
                for arm in preflight.get("candidate_arms", ())
                if arm.get("output") == str(expected["output"])
            ]
            if (
                len(arm_matches) != 1
                or float(arm_matches[0].get("l1_weight")) != expected[name]
            ):
                raise ValueError(f"regularization weight drift from preflight: {name}")
            continue
        if float(regularization_budget.get(name)) != expected[name]:
            raise ValueError(f"regularization weight drift from preflight: {name}")
    cloud_seed_policy = preflight.get("cloud_seed_policy", {})
    for name in (
        "train_prior_seed",
        "train_process_seed",
        "holdout_prior_seed",
        "holdout_process_seed",
        "audit_prior_seed",
        "audit_process_seed",
    ):
        if cloud_seed_policy.get(name) != expected[name]:
            raise ValueError(f"cloud seed drift from preflight: {name}")

def _source_fit_batch(
    *,
    sample_count: int,
    holdout_sample_count: int,
    train_prior_seed: int = DEFAULT_TRAIN_PRIOR_SEED,
    train_process_seed: int = DEFAULT_TRAIN_PROCESS_SEED,
    holdout_prior_seed: int = DEFAULT_HOLDOUT_PRIOR_SEED,
    holdout_process_seed: int = DEFAULT_HOLDOUT_PROCESS_SEED,
) -> Mapping[str, Any]:
    model = zhao_cui_sir_austria_model()
    observations = model.simulate(final_time=1, seed=5901)[1]
    d = model.parameter_dim()
    m = model.state_dim()
    previous_batch = None
    push = _p59_author_sir_source_push_result(
        model=model,
        previous_batch=_p59_author_sir_prior_sample_batch(
            model=model,
            sample_count=int(sample_count),
            seed=int(train_prior_seed),
        ),
        observation=observations[1],
        time_index=1,
        process_noise_seed=int(train_process_seed),
    )
    frame = source_route_recenter(
        samples=push.augmented_batch.samples,
        log_weights=push.augmented_batch.log_weights,
        expansion_factor=P63_AUTHOR_SIR_EXPANSION_FACTOR,
        covariance_jitter=1e-5,
        use_quantile_scale=True,
    )
    resampled, resample_indices = _p59_author_sir_deterministic_weighted_resample(
        samples=push.augmented_batch.samples,
        log_weights=push.augmented_batch.log_weights,
    )
    algebraic_input = tf.linalg.solve(
        frame.matrix,
        resampled - frame.mu[:, tf.newaxis],
    )
    domain_map = product_basis_domain_map()
    reference_points = domain_map.to_reference(tf.transpose(algebraic_input))
    log_dxdz = tf.reduce_sum(
        domain_map.reference_to_domain_log_density(reference_points),
        axis=1,
    )
    basis_points = tf.transpose(algebraic_input)
    physical_fit_points = (
        tf.linalg.matmul(frame.matrix, algebraic_input)
        + frame.mu[:, tf.newaxis]
    )
    prior_log_density, transition_log_density, likelihood_log_density = (
        _p59_author_sir_source_density_callbacks(model, observations[1])
    )
    components = SourceRouteSequentialDensityComponents(
        parameter_dim=d,
        state_dim=m,
        transition_log_density_fn=transition_log_density,
        likelihood_log_density_fn=likelihood_log_density,
        prior_log_density_fn=prior_log_density,
    )
    negative_log_physical = components.negative_log_physical_density(
        physical_points=physical_fit_points,
        time_index=1,
        previous_retained_object=previous_batch,
    )
    local_negative_log = negative_log_physical - frame.log_abs_det()
    shift = tf.reduce_min(local_negative_log)
    reference_negative_log = local_negative_log - log_dxdz
    shift = tf.reduce_min(reference_negative_log)
    shifted = source_route_shifted_negative_log_target(
        negative_log_target=reference_negative_log,
        shift_constant=shift,
    )
    target_values = tf.exp(-0.5 * shifted)
    if holdout_sample_count > 0:
        holdout_prior = _p59_author_sir_prior_sample_batch(
            model=model,
            sample_count=int(holdout_sample_count),
            seed=int(holdout_prior_seed),
        )
        holdout_push = _p59_author_sir_source_push_result(
            model=model,
            previous_batch=holdout_prior,
            observation=observations[1],
            time_index=1,
            process_noise_seed=int(holdout_process_seed),
        )
        holdout_resampled, _ = _p59_author_sir_deterministic_weighted_resample(
            samples=holdout_push.augmented_batch.samples,
            log_weights=holdout_push.augmented_batch.log_weights,
        )
        holdout_algebraic_input = tf.linalg.solve(
            frame.matrix,
            holdout_resampled - frame.mu[:, tf.newaxis],
        )
        holdout_reference = domain_map.to_reference(tf.transpose(holdout_algebraic_input))
        holdout_log_dxdz = tf.reduce_sum(
            domain_map.reference_to_domain_log_density(holdout_reference),
            axis=1,
        )
        holdout_basis_points = tf.transpose(holdout_algebraic_input)
        holdout_physical = (
            tf.linalg.matmul(frame.matrix, holdout_algebraic_input)
            + frame.mu[:, tf.newaxis]
        )
        holdout_negative = components.negative_log_physical_density(
            physical_points=holdout_physical,
            time_index=1,
            previous_retained_object=None,
        ) - frame.log_abs_det()
        holdout_shifted = source_route_shifted_negative_log_target(
            negative_log_target=holdout_negative - holdout_log_dxdz,
            shift_constant=shift,
        )
        holdout_values = tf.exp(-0.5 * holdout_shifted)
    else:
        holdout_basis_points = None
        holdout_values = None
    return {
        "points": basis_points,
        "target_values": target_values,
        "weights": tf.ones([int(sample_count)], dtype=tf.float64),
        "holdout_points": holdout_basis_points,
        "holdout_values": holdout_values,
        "holdout_weights": (
            None
            if holdout_values is None
            else tf.ones([int(holdout_sample_count)], dtype=tf.float64)
        ),
        "fit_data_manifest": {
            "fit_data_mode": "source_pushed_computeL_weighted_augmented_samples",
            "coordinate_policy": "unclipped_author_algebraic_input_coordinates",
            "basis_evaluation_coordinates": "unclipped local algebraic coordinates; ProductBasis applies AlgebraicMapping(1) internally",
            "target_transform": "reference density square-root includes sum log|dx/dz|",
            "basis_points_shape": tuple(int(dim) for dim in basis_points.shape),
            "reference_points_shape": tuple(int(dim) for dim in reference_points.shape),
            "fit_sample_count": int(sample_count),
            "holdout_sample_count": int(holdout_sample_count),
            "resample_index_count": int(resample_indices.shape[0]),
            "coordinate_frame_log_abs_det": frame.log_abs_det(),
            "shift_constant": shift,
            "target_value_min": tf.reduce_min(target_values),
            "target_value_max": tf.reduce_max(target_values),
            "train_prior_seed": int(train_prior_seed),
            "train_process_seed": int(train_process_seed),
            "holdout_prior_seed": int(holdout_prior_seed),
            "holdout_process_seed": int(holdout_process_seed),
        },
}


def product_basis_domain_map():
    product_basis = p85_author_sir_lagrangep_algebraic_product_basis_spec(
        dimension=1,
        convention=_convention(),
    ).build_product_basis()
    return product_basis.bases[0].domain


def _trainer_config(
    *,
    product_basis,
    ranks: Sequence[int],
    seed: int,
    learning_rate: float,
    l1_weight: float = DEFAULT_L1_WEIGHT,
    l2_weight: float = DEFAULT_L2_WEIGHT,
    logz_anchor_weight: float = DEFAULT_LOGZ_ANCHOR_WEIGHT,
) -> P75TrainableTTConfig:
    return P75TrainableTTConfig(
        product_basis=product_basis,
        ranks=tuple(int(rank) for rank in ranks),
        tau=tf.constant(P62_AUTHOR_TTSIRT_EXECUTABLE_DEFAULT_TAU, dtype=tf.float64),
        normalizer_floor=tf.constant(1e-12, dtype=tf.float64),
        denominator_floor=tf.constant(1e-12, dtype=tf.float64),
        l1_weight=tf.constant(float(l1_weight), dtype=tf.float64),
        l2_weight=tf.constant(float(l2_weight), dtype=tf.float64),
        logz_anchor_weight=tf.constant(float(logz_anchor_weight), dtype=tf.float64),
        learning_rate=float(learning_rate),
        gradient_clip_norm=100.0,
        seed=int(seed),
        metadata={
            "route": "p86_author_lagrangep_algebraic",
            "training_backend": TRAINING_BACKEND,
            "historical_als_training_status": HISTORICAL_ALS_TRAINING_STATUS,
            "fixed_branch_adaptation_class": P65_FIXED_BRANCH_ADAPTATION_CLASS,
            "initialization_rule": P70_FIXED_BRANCH_INITIALIZATION_RULE,
        },
    )


def _training_base_initial_cores(
    *,
    product_basis,
    ranks: Sequence[int],
    constant_value: tf.Tensor,
) -> tuple[TTCore, ...]:
    basis_dim = int(product_basis.basis_dim_tuple()[0])
    seeded = _source_route_seeded_channel_initial_cores(
        ranks=tuple(int(rank) for rank in ranks),
        basis_dim=basis_dim,
        constant_value=constant_value,
    )
    cores = []
    for axis, (basis, core) in enumerate(zip(product_basis.bases, seeded)):
        payload = basis.manifest_payload()
        if payload.get("family") != "lagrangep":
            cores.append(core)
            continue
        value = (
            tf.convert_to_tensor(constant_value, dtype=tf.float64)
            if axis == 0
            else tf.constant(1.0, dtype=tf.float64)
        )
        replacement = tf.ones([int(basis.basis_dim)], dtype=tf.float64) * value
        indices = tf.constant(
            [[0, basis_index, 0] for basis_index in range(int(basis.basis_dim))],
            dtype=tf.int64,
        )
        values = tf.tensor_scatter_nd_update(core.values, indices, replacement)
        cores.append(TTCore(values))
    return tuple(cores)


def _objective_batch_from_payload(
    batch_payload: Mapping[str, Any],
    *,
    start: int,
    batch_size: int,
    provenance_label: str,
) -> P75ObjectiveBatch:
    points = tf.convert_to_tensor(batch_payload["points"], dtype=tf.float64)
    targets = tf.convert_to_tensor(batch_payload["target_values"], dtype=tf.float64)
    weights = tf.convert_to_tensor(batch_payload["weights"], dtype=tf.float64)
    n = int(points.shape[0])
    if n <= 0:
        raise ValueError("training cloud must be nonempty")
    indices = tf.math.floormod(
        tf.range(int(start), int(start) + int(batch_size), dtype=tf.int32),
        tf.constant(n, dtype=tf.int32),
    )
    index_values = tuple(int(item) for item in indices.numpy())
    return P75ObjectiveBatch(
        points=tf.gather(points, indices),
        target_values=tf.gather(targets, indices),
        weights=tf.gather(weights, indices),
        point_records=tuple(
            {
                "point_id": f"p86-phase5-train-{index}",
                "cloud_hash": "p86-phase5-train-source-push-t1-prior6301-process6401",
                "role": "fit",
            }
            for index in index_values
        ),
        forbidden_audit_records=(
            {
                "point_id": "p86-phase5-audit-cloud-marker",
                "cloud_hash": "p86-phase5-audit-reserved-source-push-t1-prior7311-process7501",
                "role": "audit",
            },
        ),
        provenance_label=provenance_label,
    )


def _weighted_residual_rms(
    *,
    predictions: tf.Tensor,
    targets: tf.Tensor,
    weights: tf.Tensor,
) -> tf.Tensor:
    residual = tf.convert_to_tensor(predictions, dtype=tf.float64) - tf.convert_to_tensor(
        targets,
        dtype=tf.float64,
    )
    weights_t = tf.convert_to_tensor(weights, dtype=tf.float64)
    numerator = tf.reduce_sum(weights_t * tf.square(residual))
    denominator = tf.reduce_sum(weights_t)
    return tf.sqrt(numerator / denominator)


def _holdout_metric_batch_from_payload(
    batch_payload: Mapping[str, Any],
    *,
    provenance_label: str,
) -> P75ObjectiveBatch | None:
    if batch_payload.get("holdout_points") is None:
        return None
    return P75ObjectiveBatch(
        points=tf.convert_to_tensor(batch_payload["holdout_points"], dtype=tf.float64),
        target_values=tf.convert_to_tensor(batch_payload["holdout_values"], dtype=tf.float64),
        weights=tf.convert_to_tensor(batch_payload["holdout_weights"], dtype=tf.float64),
        point_records=(),
        forbidden_audit_records=(),
        provenance_label=provenance_label,
    )


def _validation_monitor_payload(
    *,
    trainer: TrainableFunctionalTT,
    holdout_batch: P75ObjectiveBatch | None,
    step: int,
    learning_rate: float,
    elapsed_seconds: float,
) -> Mapping[str, Any] | None:
    if holdout_batch is None:
        return None
    terms = trainer.objective(holdout_batch)
    predictions = trainer.evaluate(holdout_batch.points)
    residual = _weighted_residual_rms(
        predictions=predictions,
        targets=holdout_batch.target_values,
        weights=holdout_batch.weights,
    )
    return {
        "step": int(step),
        "learning_rate": float(learning_rate),
        "elapsed_seconds": round(float(elapsed_seconds), 3),
        "holdout_objective": terms_payload(terms),
        "holdout_residual": residual,
        "monitor_value": residual,
        "monitor_metric": "holdout_residual",
        "role": "validation_holdout_for_scheduler_not_audit",
    }


def _adaptive_training_initial_state(*, learning_rate: float) -> Mapping[str, Any]:
    return {
        "best_monitor_value": None,
        "best_step": None,
        "bad_checks": 0,
        "lr_drop_count": 0,
        "current_learning_rate": float(learning_rate),
        "events": [],
        "stop_reason": None,
    }


def _update_adaptive_training_state(
    state: Mapping[str, Any],
    monitor_payload: Mapping[str, Any],
    *,
    plateau_patience: int,
    plateau_min_delta: float,
    lr_reduction_factor: float,
    min_learning_rate: float,
    early_stop_after_lr_drops: int,
) -> Mapping[str, Any]:
    value = float(monitor_payload["monitor_value"])
    best = state["best_monitor_value"]
    improved = best is None or value < float(best) - float(plateau_min_delta)
    bad_checks = 0 if improved else int(state["bad_checks"]) + 1
    best_value = value if improved else best
    best_step = int(monitor_payload["step"]) if improved else state["best_step"]
    current_lr = float(state["current_learning_rate"])
    lr_drop_count = int(state["lr_drop_count"])
    events = list(state["events"])
    stop_reason = state.get("stop_reason")
    if improved:
        events.append(
            {
                "event": "monitor_improved",
                "step": int(monitor_payload["step"]),
                "monitor_value": value,
                "learning_rate": current_lr,
            }
        )
    elif int(plateau_patience) > 0 and bad_checks >= int(plateau_patience):
        proposed_lr = max(float(min_learning_rate), current_lr * float(lr_reduction_factor))
        if proposed_lr < current_lr:
            current_lr = proposed_lr
            lr_drop_count += 1
            bad_checks = 0
            events.append(
                {
                    "event": "learning_rate_reduced_on_plateau",
                    "step": int(monitor_payload["step"]),
                    "monitor_value": value,
                    "learning_rate": current_lr,
                    "lr_drop_count": lr_drop_count,
                }
            )
            if (
                int(early_stop_after_lr_drops) > 0
                and lr_drop_count >= int(early_stop_after_lr_drops)
            ):
                stop_reason = "early_stop_after_plateau_lr_drop_limit"
        else:
            events.append(
                {
                    "event": "plateau_at_min_learning_rate",
                    "step": int(monitor_payload["step"]),
                    "monitor_value": value,
                    "learning_rate": current_lr,
                }
            )
            stop_reason = "early_stop_plateau_at_min_learning_rate"
    return {
        "best_monitor_value": best_value,
        "best_step": best_step,
        "bad_checks": bad_checks,
        "lr_drop_count": lr_drop_count,
        "current_learning_rate": current_lr,
        "events": events,
        "stop_reason": stop_reason,
    }


def _training_convergence_status(
    *,
    requested_steps: int,
    completed_steps: int,
    stop_reason: str,
    adaptive_training: bool,
    trace: Sequence[Mapping[str, Any]],
    plateau_min_delta: float,
) -> Mapping[str, Any]:
    density_trace = [
        record for record in trace
        if record.get("phase") == "density" and "terms" in record
    ]
    final_logged_loss_delta = None
    if len(density_trace) >= 2:
        final_logged_loss_delta = (
            float(density_trace[-1]["terms"]["total_loss"])
            - float(density_trace[-2]["terms"]["total_loss"])
        )
    exhausted = (
        int(completed_steps) >= int(requested_steps)
        and str(stop_reason) == "optimizer_steps_completed"
    )
    still_improving = (
        final_logged_loss_delta is not None
        and final_logged_loss_delta < -abs(float(plateau_min_delta))
    )
    if adaptive_training and stop_reason.startswith("early_stop"):
        status = "scheduler_stopped_after_plateau"
    elif adaptive_training and exhausted and still_improving:
        status = "max_steps_exhausted_while_loss_still_improving"
    elif not adaptive_training and exhausted:
        status = "fixed_budget_exhausted_no_plateau_test"
    else:
        status = "incomplete_or_wall_clock_stopped"
    return {
        "status": status,
        "adaptive_training": bool(adaptive_training),
        "requested_steps": int(requested_steps),
        "completed_steps": int(completed_steps),
        "stop_reason": str(stop_reason),
        "final_logged_loss_delta": final_logged_loss_delta,
        "loss_still_improving_at_stop": bool(still_improving),
        "convergence_claim_allowed": status == "scheduler_stopped_after_plateau",
    }


def _training_protocol_completed(
    training: Mapping[str, Any],
    *,
    requested_prefit_steps: int,
    requested_train_steps: int,
) -> bool:
    prefit_completed = int(training["completed_prefit_steps"]) == int(requested_prefit_steps)
    if not prefit_completed:
        return False
    convergence = training.get("training_convergence") or {}
    if convergence.get("status") == "scheduler_stopped_after_plateau":
        return True
    return int(training["completed_train_steps"]) == int(requested_train_steps)


def _trained_core_serialization_payload(
    cores: Sequence[tf.Tensor],
    *,
    include_values: bool,
) -> Mapping[str, Any]:
    records = []
    digest = hashlib.sha256()
    total_values = 0
    for axis, core in enumerate(cores):
        values = tf.convert_to_tensor(core, dtype=tf.float64).numpy()
        digest.update(values.tobytes())
        total_values += int(values.size)
        record = {
            "axis": int(axis),
            "shape": tuple(int(dim) for dim in values.shape),
            "dtype": "float64",
            "sha256": hashlib.sha256(values.tobytes()).hexdigest(),
            "min": float(values.min()),
            "max": float(values.max()),
            "l2_norm": float(math.sqrt(float((values * values).sum()))),
        }
        if include_values:
            record["values"] = values.tolist()
        records.append(record)
    return {
        "schema_version": "p86_trained_tt_core_serialization.v1",
        "status": "serialized_with_values" if include_values else "metadata_hash_only",
        "include_values": bool(include_values),
        "core_count": len(records),
        "total_values": int(total_values),
        "global_sha256": digest.hexdigest(),
        "cores": tuple(records),
    }


def _finite_positive_scalar(value: tf.Tensor) -> bool:
    scalar = tf.reshape(tf.convert_to_tensor(value, dtype=tf.float64), [])
    return bool(tf.math.is_finite(scalar).numpy() and (scalar > 0.0).numpy())


def _finite_scalar(value: tf.Tensor) -> bool:
    scalar = tf.reshape(tf.convert_to_tensor(value, dtype=tf.float64), [])
    return bool(tf.math.is_finite(scalar).numpy())


def _trainable_component_active(value: tf.Tensor) -> bool:
    scalar = tf.reshape(tf.convert_to_tensor(value, dtype=tf.float64), [])
    floor = tf.constant(P62_AUTHOR_TTSIRT_EXECUTABLE_DEFAULT_TAU, dtype=tf.float64)
    return bool(tf.math.is_finite(scalar).numpy() and (scalar > floor).numpy())


def _core_delta_payload(
    before: Sequence[tf.Tensor],
    after: Sequence[tf.Variable],
) -> Mapping[str, Any]:
    deltas = [
        tf.norm(tf.convert_to_tensor(new, dtype=tf.float64) - old)
        for old, new in zip(before, after)
    ]
    delta_stack = tf.stack(deltas)
    return {
        "delta_norms": deltas,
        "finite": bool(tf.reduce_all(tf.math.is_finite(delta_stack)).numpy()),
        "any_changed": bool(tf.reduce_any(delta_stack > 0.0).numpy()),
        "max_delta_norm": tf.reduce_max(delta_stack),
    }


def _run_training_base(
    *,
    product_basis,
    ranks: Sequence[int],
    batch_payload: Mapping[str, Any],
    seed: int,
    learning_rate: float,
    optimizer_batch_size: int,
    prefit_steps: int,
    train_steps: int,
    max_seconds: float,
    l1_weight: float = DEFAULT_L1_WEIGHT,
    l2_weight: float = DEFAULT_L2_WEIGHT,
    logz_anchor_weight: float = DEFAULT_LOGZ_ANCHOR_WEIGHT,
    adaptive_training: bool = DEFAULT_ADAPTIVE_TRAINING,
    validation_check_every: int = DEFAULT_VALIDATION_CHECK_EVERY,
    plateau_patience: int = DEFAULT_PLATEAU_PATIENCE,
    plateau_min_delta: float = DEFAULT_PLATEAU_MIN_DELTA,
    lr_reduction_factor: float = DEFAULT_LR_REDUCTION_FACTOR,
    min_learning_rate: float = DEFAULT_MIN_LEARNING_RATE,
    early_stop_after_lr_drops: int = DEFAULT_EARLY_STOP_AFTER_LR_DROPS,
    serialize_trained_cores: bool = DEFAULT_SERIALIZE_TRAINED_CORES,
) -> Mapping[str, Any]:
    config = _trainer_config(
        product_basis=product_basis,
        ranks=ranks,
        seed=seed,
        learning_rate=learning_rate,
        l1_weight=l1_weight,
        l2_weight=l2_weight,
        logz_anchor_weight=logz_anchor_weight,
    )
    initial_cores = _training_base_initial_cores(
        product_basis=product_basis,
        ranks=ranks,
        constant_value=_weighted_mean_target_value(
            batch_payload["target_values"],
            batch_payload["weights"],
        ),
    )
    trainer = TrainableFunctionalTT(config, initial_cores=initial_cores)
    optimizer = make_adam_optimizer(config)
    initial_variables = tuple(tf.identity(core) for core in trainer.variables)
    trace = []
    validation_trace = []
    completed_prefit_steps = 0
    completed_train_steps = 0
    stop_reason = "optimizer_steps_completed"
    started = time.monotonic()
    reference_cores = tuple(tf.identity(core) for core in trainer.variables)
    final_prefit_terms = None
    final_train_terms = None
    holdout_metric_batch = _holdout_metric_batch_from_payload(
        batch_payload,
        provenance_label="p86_phase6r_validation_holdout_not_audit",
    )
    adaptive_state = _adaptive_training_initial_state(learning_rate=learning_rate)
    for step in range(int(prefit_steps)):
        if time.monotonic() - started > float(max_seconds):
            stop_reason = "wall_clock_cap_reached_before_prefit_step"
            break
        batch = _objective_batch_from_payload(
            batch_payload,
            start=step * int(optimizer_batch_size),
            batch_size=int(optimizer_batch_size),
            provenance_label=f"p86_phase5_training_base_prefit_batch_{step}",
        )
        terms = trainer.square_root_prefit_step(
            batch,
            optimizer,
            reference_cores=reference_cores,
            reference_l2_weight=tf.constant(0.0, dtype=tf.float64),
        )
        final_prefit_terms = terms
        completed_prefit_steps += 1
        trace.append(
            {
                "phase": "prefit",
                "step": step + 1,
                "terms": prefit_terms_payload(terms),
                "elapsed_seconds": round(time.monotonic() - started, 3),
            }
        )
    for step in range(int(train_steps)):
        if time.monotonic() - started > float(max_seconds):
            stop_reason = "wall_clock_cap_reached_before_train_step"
            break
        current_lr = float(adaptive_state["current_learning_rate"])
        if hasattr(optimizer, "learning_rate"):
            optimizer.learning_rate.assign(current_lr)
        batch = _objective_batch_from_payload(
            batch_payload,
            start=step * int(optimizer_batch_size),
            batch_size=int(optimizer_batch_size),
            provenance_label=f"p86_phase5_training_base_density_batch_{step}",
        )
        terms = trainer.train_step(batch, optimizer)
        final_train_terms = terms
        completed_train_steps += 1
        if step in {0, int(train_steps) - 1} or (step + 1) % 10 == 0:
            trace.append(
                {
                    "phase": "density",
                    "step": step + 1,
                    "learning_rate": current_lr,
                    "terms": terms_payload(terms),
                    "elapsed_seconds": round(time.monotonic() - started, 3),
                }
            )
        should_check_validation = (
            bool(adaptive_training)
            and int(validation_check_every) > 0
            and holdout_metric_batch is not None
            and ((step + 1) % int(validation_check_every) == 0 or step == int(train_steps) - 1)
        )
        if should_check_validation:
            validation_payload = _validation_monitor_payload(
                trainer=trainer,
                holdout_batch=holdout_metric_batch,
                step=step + 1,
                learning_rate=current_lr,
                elapsed_seconds=time.monotonic() - started,
            )
            if validation_payload is not None:
                validation_trace.append(validation_payload)
                adaptive_state = _update_adaptive_training_state(
                    adaptive_state,
                    validation_payload,
                    plateau_patience=int(plateau_patience),
                    plateau_min_delta=float(plateau_min_delta),
                    lr_reduction_factor=float(lr_reduction_factor),
                    min_learning_rate=float(min_learning_rate),
                    early_stop_after_lr_drops=int(early_stop_after_lr_drops),
                )
                if adaptive_state.get("stop_reason") is not None:
                    stop_reason = str(adaptive_state["stop_reason"])
                    break
    if final_train_terms is None and int(train_steps) > 0:
        raise RuntimeError("training-base route produced no density optimizer step")
    train_predictions = trainer.evaluate(batch_payload["points"])
    fit_residual = _weighted_residual_rms(
        predictions=train_predictions,
        targets=batch_payload["target_values"],
        weights=batch_payload["weights"],
    )
    holdout_residual = None
    if batch_payload.get("holdout_points") is not None:
        holdout_predictions = trainer.evaluate(batch_payload["holdout_points"])
        holdout_residual = _weighted_residual_rms(
            predictions=holdout_predictions,
            targets=batch_payload["holdout_values"],
            weights=batch_payload["holdout_weights"],
        )
    sqrt_square_normalizer = trainer.sqrt_square_normalizer()
    normalizer = trainer.normalizer()
    delta_payload = _core_delta_payload(initial_variables, trainer.variables)
    density = trainer.snapshot_density()
    convergence_payload = _training_convergence_status(
        requested_steps=int(train_steps),
        completed_steps=int(completed_train_steps),
        stop_reason=stop_reason,
        adaptive_training=bool(adaptive_training),
        trace=trace,
        plateau_min_delta=float(plateau_min_delta),
    )
    trained_core_payload = _trained_core_serialization_payload(
        trainer.variables,
        include_values=bool(serialize_trained_cores),
    )
    return {
        "trainer": trainer,
        "density": density,
        "config": config,
        "trace": trace,
        "validation_trace": validation_trace,
        "completed_prefit_steps": completed_prefit_steps,
        "completed_train_steps": completed_train_steps,
        "requested_prefit_steps": int(prefit_steps),
        "requested_train_steps": int(train_steps),
        "stop_reason": stop_reason,
        "adaptive_training_summary": {
            **adaptive_state,
            "validation_check_every": int(validation_check_every),
            "plateau_patience": int(plateau_patience),
            "plateau_min_delta": float(plateau_min_delta),
            "lr_reduction_factor": float(lr_reduction_factor),
            "min_learning_rate": float(min_learning_rate),
            "early_stop_after_lr_drops": int(early_stop_after_lr_drops),
        },
        "training_convergence": convergence_payload,
        "final_prefit_terms": (
            None if final_prefit_terms is None else prefit_terms_payload(final_prefit_terms)
        ),
        "final_train_terms": (
            None if final_train_terms is None else terms_payload(final_train_terms)
        ),
        "fit_residual": fit_residual,
        "holdout_residual": holdout_residual,
        "sqrt_square_normalizer": sqrt_square_normalizer,
        "normalizer": normalizer,
        "core_delta": delta_payload,
        "trained_core_serialization": trained_core_payload,
        "branch_hash": density.branch_identity.hash.value,
        "runtime_seconds": time.monotonic() - started,
    }


def run_fit_payload(args: argparse.Namespace) -> Mapping[str, Any]:
    preflight = _load_preflight(args.preflight_json)
    _guard_exact_fit_args(args, preflight)
    expected_fit_args = _expected_fit_args_for_preflight(
        {**preflight, "_requested_output": str(args.output)}
    )
    is_phase6_rank5 = preflight.get("status") == STATUS_PHASE6_RANK_PREFLIGHT_READY
    is_phase6s_adaptive_rank5 = (
        preflight.get("status") == STATUS_PHASE6S_ADAPTIVE_RANK5_PREFLIGHT_READY
    )
    is_phase6t_l1_tuning = (
        preflight.get("status") == STATUS_PHASE6T_L1_TUNING_PREFLIGHT_READY
    )
    is_phase6v_l1_selection = (
        preflight.get("status") == STATUS_PHASE6V_L1_SELECTION_PREFLIGHT_READY
    )
    is_phase6w_same_policy_rank4 = (
        preflight.get("status") == STATUS_PHASE6W_SAME_POLICY_RANK_PREFLIGHT_READY
    )
    is_phase6y_degree_order3 = (
        preflight.get("status")
        in {
            STATUS_PHASE6Y_DEGREE_COMPARATOR_PREFLIGHT_READY,
            STATUS_P88_PHASE2_DEGREE_COMPARATOR_PREFLIGHT_READY,
        }
    )
    is_p88_phase2_degree_order3 = (
        preflight.get("status") == STATUS_P88_PHASE2_DEGREE_COMPARATOR_PREFLIGHT_READY
    )
    started = time.monotonic()
    product_basis = p85_author_sir_lagrangep_algebraic_product_basis_spec(
        dimension=args.target_dimension,
        convention=_convention(),
        order=args.basis_order,
        num_elems=args.basis_num_elems,
    ).build_product_basis()
    ranks = _rank_tuple(args.target_dimension, args.fit_rank)
    batch_payload = _source_fit_batch(
        sample_count=args.training_sample_count,
        holdout_sample_count=args.holdout_sample_count,
        train_prior_seed=args.train_prior_seed,
        train_process_seed=args.train_process_seed,
        holdout_prior_seed=args.holdout_prior_seed,
        holdout_process_seed=args.holdout_process_seed,
    )
    training = _run_training_base(
        product_basis=product_basis,
        ranks=ranks,
        batch_payload=batch_payload,
        seed=args.seed,
        learning_rate=args.learning_rate,
        optimizer_batch_size=args.optimizer_batch_size,
        prefit_steps=args.prefit_steps,
        train_steps=args.train_steps,
        max_seconds=args.max_seconds,
        l1_weight=args.l1_weight,
        l2_weight=args.l2_weight,
        logz_anchor_weight=args.logz_anchor_weight,
        adaptive_training=args.adaptive_training,
        validation_check_every=args.validation_check_every,
        plateau_patience=args.plateau_patience,
        plateau_min_delta=args.plateau_min_delta,
        lr_reduction_factor=args.lr_reduction_factor,
        min_learning_rate=args.min_learning_rate,
        early_stop_after_lr_drops=args.early_stop_after_lr_drops,
        serialize_trained_cores=args.serialize_trained_cores,
    )
    runtime = time.monotonic() - started
    peak_mib = _peak_memory_mib()
    memory_status = (
        "within_approved_envelope"
        if peak_mib <= float(args.memory_cap_mib)
        else "memory_cap_breached"
    )
    completed = _training_protocol_completed(
        training,
        requested_prefit_steps=args.prefit_steps,
        requested_train_steps=args.train_steps,
    )
    fit_residual = float(training["fit_residual"].numpy())
    holdout_residual = (
        None
        if training["holdout_residual"] is None
        else float(training["holdout_residual"].numpy())
    )
    sqrt_square_normalizer = training["sqrt_square_normalizer"]
    normalizer = training["normalizer"]
    finite_normalizer = _finite_positive_scalar(normalizer)
    finite_sqrt_normalizer = _finite_positive_scalar(sqrt_square_normalizer)
    trainable_component_active = _trainable_component_active(sqrt_square_normalizer)
    finite_loss = bool(
        training["final_train_terms"] is not None
        and math.isfinite(float(training["final_train_terms"]["total_loss"]))
    )
    return {
        "schema_version": "p86_phase5_budget_compliant_fit.v1",
        "status": (
            (
                STATUS_PHASE6T_L1_TUNING_COMPLETED
                if is_phase6t_l1_tuning
                else (
                    STATUS_PHASE6W_RANK4_SAME_POLICY_COMPLETED
                    if is_phase6w_same_policy_rank4
                    else (
                        (
                            STATUS_P88_PHASE2_DEGREE_ORDER3_COMPLETED
                            if is_p88_phase2_degree_order3
                            else STATUS_PHASE6Y_DEGREE_ORDER3_COMPLETED
                        )
                        if is_phase6y_degree_order3
                        else (
                            STATUS_PHASE6V_L1_SELECTION_COMPLETED
                            if is_phase6v_l1_selection
                            else (
                                STATUS_PHASE6S_ADAPTIVE_RANK5_COMPLETED
                                if is_phase6s_adaptive_rank5
                                else (
                                    STATUS_PHASE6_RANK5_COMPLETED
                                    if is_phase6_rank5
                                    else STATUS_TRAINING_BASE_COMPLETED
                                )
                            )
                        )
                    )
                )
            )
            if completed and memory_status == "within_approved_envelope"
            and finite_loss
            and finite_normalizer
            and finite_sqrt_normalizer
            and trainable_component_active
            else (
                STATUS_PHASE6T_L1_TUNING_BLOCKED
                if is_phase6t_l1_tuning
                else (
                    STATUS_PHASE6W_RANK4_SAME_POLICY_BLOCKED
                    if is_phase6w_same_policy_rank4
                    else (
                        (
                            STATUS_P88_PHASE2_DEGREE_ORDER3_BLOCKED
                            if is_p88_phase2_degree_order3
                            else STATUS_PHASE6Y_DEGREE_ORDER3_BLOCKED
                        )
                        if is_phase6y_degree_order3
                        else (
                            STATUS_PHASE6V_L1_SELECTION_BLOCKED
                            if is_phase6v_l1_selection
                            else (
                                STATUS_PHASE6S_ADAPTIVE_RANK5_BLOCKED
                                if is_phase6s_adaptive_rank5
                                else (
                                    STATUS_PHASE6_RANK5_BLOCKED
                                    if is_phase6_rank5
                                    else STATUS_TRAINING_BASE_BLOCKED
                                )
                            )
                        )
                    )
                )
            )
        ),
        "phase_name": preflight.get("phase_name"),
        "fit_executed": True,
        "training_backend": TRAINING_BACKEND,
        "historical_als_training_status": HISTORICAL_ALS_TRAINING_STATUS,
        "legacy_als_artifact_status": "superseded_stale_route_diagnostic_only",
        "command": expected_fit_args["candidate_fit_command"],
        "output": str(args.output),
        "preflight_json": str(args.preflight_json),
        "preflight_status": preflight["status"],
        "phase_subplan": preflight.get("phase_subplan"),
        "phase_result": preflight.get("phase_result"),
        "lower_rung_artifact": preflight.get("lower_rung_artifact"),
        "route_manifest": preflight["route_manifest"],
        "rank_budget": preflight["rank_budget"],
        "optimizer_budget": preflight["optimizer_budget"],
        "phase6v_selection_context": (
            {
                "candidate_arms": preflight.get("candidate_arms"),
                "selection_rule": preflight.get("selection_rule"),
                "reuse_arm_validation": preflight.get("reuse_arm_validation"),
                "candidate_fit_commands": preflight.get("candidate_fit_commands"),
            }
            if is_phase6v_l1_selection
            else None
        ),
        "phase6w_same_policy_rank_context": (
            {
                "candidate_arms": preflight.get("candidate_arms"),
                "rank4_selection_rule": preflight.get("rank4_selection_rule"),
                "adjacent_rank_stability_rule": preflight.get(
                    "adjacent_rank_stability_rule"
                ),
                "selected_rank5_reuse_validation": preflight.get(
                    "selected_rank5_reuse_validation"
                ),
                "candidate_fit_commands": preflight.get("candidate_fit_commands"),
            }
            if is_phase6w_same_policy_rank4
            else None
        ),
        "phase6y_degree_context": (
            {
                "candidate_arms": preflight.get("candidate_arms"),
                "candidate_fit_commands": preflight.get("candidate_fit_commands"),
                "reference_artifact_validation": preflight.get(
                    "reference_artifact_validation"
                ),
                "degree_comparator_protocol": preflight.get(
                    "degree_comparator_protocol"
                ),
            }
            if is_phase6y_degree_order3
            else None
        ),
        "fit_data_manifest": batch_payload["fit_data_manifest"],
        "training_config": {
            **config_payload(training["config"]),
            "defensive_tau": P62_AUTHOR_TTSIRT_EXECUTABLE_DEFAULT_TAU,
            "fixed_branch_adaptation_class": P65_FIXED_BRANCH_ADAPTATION_CLASS,
            "initialization_rule": P70_FIXED_BRANCH_INITIALIZATION_RULE,
            "zhao_cui_regularization_default_policy": (
                _zhao_cui_regularization_default_policy()
            ),
        },
        "training_trace": training["trace"],
        "training_summary": {
            "completed_prefit_steps": int(training["completed_prefit_steps"]),
            "requested_prefit_steps": int(training["requested_prefit_steps"]),
            "completed_train_steps": int(training["completed_train_steps"]),
            "requested_train_steps": int(training["requested_train_steps"]),
            "optimizer_batch_size": int(args.optimizer_batch_size),
            "planned_training_sample_visits": int(args.optimizer_batch_size)
            * int(args.train_steps),
            "training_cloud_sample_count": int(args.training_sample_count),
            "stop_reason": training["stop_reason"],
            "training_protocol": {
                **_training_protocol_defaults(),
                "adaptive_training": bool(args.adaptive_training),
                "validation_check_every": int(args.validation_check_every),
                "plateau_patience": int(args.plateau_patience),
                "plateau_min_delta": float(args.plateau_min_delta),
                "lr_reduction_factor": float(args.lr_reduction_factor),
                "min_learning_rate": float(args.min_learning_rate),
                "early_stop_after_lr_drops": int(args.early_stop_after_lr_drops),
                "serialize_trained_cores": bool(args.serialize_trained_cores),
                "l1_weight": float(args.l1_weight),
                "l2_weight": float(args.l2_weight),
                "logz_anchor_weight": float(args.logz_anchor_weight),
            },
            "adaptive_training_summary": training["adaptive_training_summary"],
            "training_convergence": training["training_convergence"],
            "final_prefit_terms": training["final_prefit_terms"],
            "final_train_terms": training["final_train_terms"],
            "core_delta": training["core_delta"],
        },
        "validation_trace": training["validation_trace"],
        "post_fit_statuses": {
            "fit_status": (
                "completed"
                if completed
                else "incomplete_optimizer_steps"
            ),
            "finite_target_status": "ok",
            "finite_loss_status": "ok" if finite_loss else "block",
            "finite_normalizer_status": "ok" if finite_normalizer else "block",
            "finite_sqrt_square_normalizer_status": "ok" if finite_sqrt_normalizer else "block",
            "trainable_component_active_status": "ok" if trainable_component_active else "block",
            "finite_fit_residual_status": "ok" if fit_residual is not None and math.isfinite(fit_residual) else "block",
            "finite_holdout_residual_status": "ok" if holdout_residual is not None and math.isfinite(holdout_residual) else "block",
            "fallback_route_status": "not_used",
            "audit_cloud_tuning_status": "not_used_for_tuning",
            "als_training_status": HISTORICAL_ALS_TRAINING_STATUS,
            "training_backend_status": "ok" if TRAINING_BACKEND == "training_base_optimizer" else "block",
            "runtime_status": (
                "within_approved_envelope"
                if runtime <= float(args.max_seconds)
                else "runtime_cap_breached"
            ),
            "memory_status": memory_status,
        },
        "fit_residual": fit_residual,
        "holdout_residual": holdout_residual,
        "sqrt_square_normalizer": float(sqrt_square_normalizer.numpy()),
        "normalizer": float(normalizer.numpy()),
        "core_update_statuses": (),
        "trained_core_serialization": training["trained_core_serialization"],
        "branch_hash": training["branch_hash"],
        "runtime_seconds": runtime,
        "peak_memory_mib": peak_mib,
        "memory_cap_mib": int(args.memory_cap_mib),
        "environment": {
            "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
            "intentional_gpu_hiding": os.environ.get("CUDA_VISIBLE_DEVICES") == "-1",
            "runtime_posture": "CPU-only/GPU-hidden non-production fit posture",
            "python": sys.executable,
        },
        "nonclaims": (
            PHASE6T_FIT_NONCLAIMS
            if is_phase6t_l1_tuning
            else (
                PHASE6W_FIT_NONCLAIMS
                if is_phase6w_same_policy_rank4
                else (
                    PHASE6Y_FIT_NONCLAIMS
                    if is_phase6y_degree_order3
                    else (
                        PHASE6V_FIT_NONCLAIMS
                        if is_phase6v_l1_selection
                        else (
                            PHASE6S_FIT_NONCLAIMS
                            if is_phase6s_adaptive_rank5
                            else (
                                PHASE6_FIT_NONCLAIMS
                                if is_phase6_rank5
                                else FIT_NONCLAIMS
                            )
                        )
                    )
                )
            )
        ),
    }


def _guard_training_base_smoke_args(args: argparse.Namespace) -> None:
    expected = {
        "output": TRAINING_BASE_RETRY_OUTPUT,
        "target_dimension": 36,
        "fit_rank": 1,
        "training_sample_count": 64,
        "holdout_sample_count": 32,
        "seed": 8615,
        "optimizer_batch_size": 32,
        "prefit_steps": 1,
        "train_steps": 1,
        "learning_rate": DEFAULT_LEARNING_RATE,
        "l1_weight": DEFAULT_L1_WEIGHT,
        "l2_weight": DEFAULT_L2_WEIGHT,
        "logz_anchor_weight": DEFAULT_LOGZ_ANCHOR_WEIGHT,
        "max_seconds": 120,
        "memory_cap_mib": 12288,
    }
    for name, expected_value in expected.items():
        observed = getattr(args, name)
        if isinstance(expected_value, Path):
            if Path(observed) != expected_value:
                raise ValueError(f"training-base smoke argument drift: {name}")
        elif observed != expected_value:
            raise ValueError(f"training-base smoke argument drift: {name}")


def _guard_phase6r_adaptive_smoke_args(args: argparse.Namespace) -> None:
    expected = {
        "output": PHASE6R_ADAPTIVE_SMOKE_OUTPUT,
        "target_dimension": 36,
        "fit_rank": 1,
        "training_sample_count": 64,
        "holdout_sample_count": 32,
        "seed": 8615,
        "optimizer_batch_size": 32,
        "prefit_steps": 1,
        "train_steps": 6,
        "learning_rate": DEFAULT_LEARNING_RATE,
        "l1_weight": DEFAULT_L1_WEIGHT,
        "l2_weight": DEFAULT_L2_WEIGHT,
        "logz_anchor_weight": DEFAULT_LOGZ_ANCHOR_WEIGHT,
        "max_seconds": 120,
        "memory_cap_mib": 12288,
        "adaptive_training": True,
        "validation_check_every": 2,
        "plateau_patience": 1,
        "plateau_min_delta": 0.0,
        "lr_reduction_factor": DEFAULT_LR_REDUCTION_FACTOR,
        "min_learning_rate": DEFAULT_MIN_LEARNING_RATE,
        "early_stop_after_lr_drops": 2,
        "serialize_trained_cores": True,
    }
    for name, expected_value in expected.items():
        observed = getattr(args, name)
        if isinstance(expected_value, Path):
            if Path(observed) != expected_value:
                raise ValueError(f"phase6r adaptive smoke argument drift: {name}")
        elif observed != expected_value:
            raise ValueError(f"phase6r adaptive smoke argument drift: {name}")


def run_training_base_smoke_payload(args: argparse.Namespace) -> Mapping[str, Any]:
    _guard_training_base_smoke_args(args)
    return _run_smoke_payload(
        args,
        command=TRAINING_BASE_SMOKE_COMMAND,
        completed_status=STATUS_TRAINING_BASE_SMOKE_COMPLETED,
        blocked_status=STATUS_TRAINING_BASE_SMOKE_BLOCKED,
        schema_version="p86_phase5_training_base_retry_smoke.v1",
        runtime_posture="CPU-only/GPU-hidden bounded retry smoke",
        smoke_kind="phase5_training_base_retry_smoke",
        nonclaims=SMOKE_NONCLAIMS,
    )


def run_phase6r_adaptive_smoke_payload(args: argparse.Namespace) -> Mapping[str, Any]:
    _guard_phase6r_adaptive_smoke_args(args)
    return _run_smoke_payload(
        args,
        command=PHASE6R_ADAPTIVE_SMOKE_COMMAND,
        completed_status=STATUS_PHASE6R_ADAPTIVE_SMOKE_COMPLETED,
        blocked_status=STATUS_PHASE6R_ADAPTIVE_SMOKE_BLOCKED,
        schema_version="p86_phase6r_adaptive_training_smoke.v1",
        runtime_posture="CPU-only/GPU-hidden bounded Phase 6R adaptive scheduler smoke",
        smoke_kind="phase6r_adaptive_training_scheduler_smoke",
        nonclaims=(
            "Phase 6R adaptive scheduler smoke is not a Phase 6 rank-convergence fit",
            "Phase 6R adaptive scheduler smoke does not close rank or production gates",
        ) + COMMON_NONCLAIMS,
    )


def _run_smoke_payload(
    args: argparse.Namespace,
    *,
    command: str,
    completed_status: str,
    blocked_status: str,
    schema_version: str,
    runtime_posture: str,
    smoke_kind: str,
    nonclaims: Sequence[str],
) -> Mapping[str, Any]:
    started = time.monotonic()
    product_basis = p85_author_sir_lagrangep_algebraic_product_basis_spec(
        dimension=args.target_dimension,
        convention=_convention(),
    ).build_product_basis()
    ranks = _rank_tuple(args.target_dimension, args.fit_rank)
    batch_payload = _source_fit_batch(
        sample_count=args.training_sample_count,
        holdout_sample_count=args.holdout_sample_count,
    )
    training = _run_training_base(
        product_basis=product_basis,
        ranks=ranks,
        batch_payload=batch_payload,
        seed=args.seed,
        learning_rate=args.learning_rate,
        optimizer_batch_size=args.optimizer_batch_size,
        prefit_steps=args.prefit_steps,
        train_steps=args.train_steps,
        max_seconds=args.max_seconds,
        l1_weight=args.l1_weight,
        l2_weight=args.l2_weight,
        logz_anchor_weight=args.logz_anchor_weight,
        adaptive_training=args.adaptive_training,
        validation_check_every=args.validation_check_every,
        plateau_patience=args.plateau_patience,
        plateau_min_delta=args.plateau_min_delta,
        lr_reduction_factor=args.lr_reduction_factor,
        min_learning_rate=args.min_learning_rate,
        early_stop_after_lr_drops=args.early_stop_after_lr_drops,
        serialize_trained_cores=args.serialize_trained_cores,
    )
    runtime = time.monotonic() - started
    peak_mib = _peak_memory_mib()
    memory_status = (
        "within_approved_envelope"
        if peak_mib <= float(args.memory_cap_mib)
        else "memory_cap_breached"
    )
    completed = (
        int(training["completed_train_steps"]) == int(args.train_steps)
        and int(training["completed_prefit_steps"]) == int(args.prefit_steps)
    )
    fit_residual = float(training["fit_residual"].numpy())
    holdout_residual = (
        None
        if training["holdout_residual"] is None
        else float(training["holdout_residual"].numpy())
    )
    sqrt_square_normalizer = training["sqrt_square_normalizer"]
    normalizer = training["normalizer"]
    finite_normalizer = _finite_positive_scalar(normalizer)
    finite_sqrt_normalizer = _finite_positive_scalar(sqrt_square_normalizer)
    trainable_component_active = _trainable_component_active(sqrt_square_normalizer)
    finite_loss = bool(
        training["final_train_terms"] is not None
        and math.isfinite(float(training["final_train_terms"]["total_loss"]))
    )
    finite_fit_residual = math.isfinite(fit_residual)
    finite_holdout_residual = holdout_residual is not None and math.isfinite(holdout_residual)
    core_delta = training["core_delta"]
    changed = bool(core_delta["finite"]) and bool(core_delta["any_changed"])
    status = (
        completed_status
        if completed
        and finite_loss
        and finite_normalizer
        and finite_sqrt_normalizer
        and trainable_component_active
        and finite_fit_residual
        and finite_holdout_residual
        and changed
        and memory_status == "within_approved_envelope"
        and runtime <= float(args.max_seconds)
        else blocked_status
    )
    return {
        "schema_version": schema_version,
        "status": status,
        "fit_executed": False,
        "training_executed": True,
        "training_base_smoke_executed": True,
        "smoke_kind": smoke_kind,
        "training_backend": TRAINING_BACKEND,
        "historical_als_training_status": HISTORICAL_ALS_TRAINING_STATUS,
        "legacy_als_artifact_status": "superseded_stale_route_diagnostic_only",
        "command": command,
        "output": str(args.output),
        "route_manifest": _route_payload(args.target_dimension),
        "rank_budget": {
            "target_dimension": int(args.target_dimension),
            "fit_rank": int(args.fit_rank),
            "ranks": ranks,
            "P_theta": _parameter_count(product_basis.basis_dim_tuple(), ranks),
            "training_sample_count": int(args.training_sample_count),
            "budget_status": "smoke_only_not_phase5_budget_compliant",
        },
        "fit_data_manifest": batch_payload["fit_data_manifest"],
        "training_config": {
            **config_payload(training["config"]),
            "defensive_tau": P62_AUTHOR_TTSIRT_EXECUTABLE_DEFAULT_TAU,
            "fixed_branch_adaptation_class": P65_FIXED_BRANCH_ADAPTATION_CLASS,
            "initialization_rule": P70_FIXED_BRANCH_INITIALIZATION_RULE,
            "zhao_cui_regularization_default_policy": (
                _zhao_cui_regularization_default_policy()
            ),
        },
        "training_trace": training["trace"],
        "training_summary": {
            "completed_prefit_steps": int(training["completed_prefit_steps"]),
            "requested_prefit_steps": int(training["requested_prefit_steps"]),
            "completed_train_steps": int(training["completed_train_steps"]),
            "requested_train_steps": int(training["requested_train_steps"]),
            "optimizer_batch_size": int(args.optimizer_batch_size),
            "training_cloud_sample_count": int(args.training_sample_count),
            "stop_reason": training["stop_reason"],
            "training_protocol": {
                **_training_protocol_defaults(),
                "adaptive_training": bool(args.adaptive_training),
                "validation_check_every": int(args.validation_check_every),
                "plateau_patience": int(args.plateau_patience),
                "plateau_min_delta": float(args.plateau_min_delta),
                "lr_reduction_factor": float(args.lr_reduction_factor),
                "min_learning_rate": float(args.min_learning_rate),
                "early_stop_after_lr_drops": int(args.early_stop_after_lr_drops),
                "serialize_trained_cores": bool(args.serialize_trained_cores),
                "l1_weight": float(args.l1_weight),
                "l2_weight": float(args.l2_weight),
                "logz_anchor_weight": float(args.logz_anchor_weight),
            },
            "adaptive_training_summary": training["adaptive_training_summary"],
            "training_convergence": training["training_convergence"],
            "final_prefit_terms": training["final_prefit_terms"],
            "final_train_terms": training["final_train_terms"],
            "core_delta": core_delta,
        },
        "validation_trace": training["validation_trace"],
        "post_fit_statuses": {
            "fit_status": "smoke_completed" if completed else "incomplete_optimizer_steps",
            "finite_target_status": "ok",
            "finite_loss_status": "ok" if finite_loss else "block",
            "finite_normalizer_status": "ok" if finite_normalizer else "block",
            "finite_sqrt_square_normalizer_status": "ok" if finite_sqrt_normalizer else "block",
            "trainable_component_active_status": "ok" if trainable_component_active else "block",
            "finite_fit_residual_status": "ok" if finite_fit_residual else "block",
            "finite_holdout_residual_status": "ok" if finite_holdout_residual else "block",
            "core_delta_status": "ok" if changed else "block",
            "fallback_route_status": "not_used",
            "audit_cloud_tuning_status": "not_used_for_tuning",
            "als_training_status": HISTORICAL_ALS_TRAINING_STATUS,
            "training_backend_status": "ok",
            "runtime_status": (
                "within_approved_envelope"
                if runtime <= float(args.max_seconds)
                else "runtime_cap_breached"
            ),
            "memory_status": memory_status,
        },
        "fit_residual": fit_residual,
        "holdout_residual": holdout_residual,
        "sqrt_square_normalizer": float(sqrt_square_normalizer.numpy()),
        "normalizer": float(normalizer.numpy()),
        "trained_core_serialization": training["trained_core_serialization"],
        "branch_hash": training["branch_hash"],
        "runtime_seconds": runtime,
        "peak_memory_mib": peak_mib,
        "memory_cap_mib": int(args.memory_cap_mib),
        "environment": {
            "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
            "intentional_gpu_hiding": os.environ.get("CUDA_VISIBLE_DEVICES") == "-1",
            "runtime_posture": runtime_posture,
            "python": sys.executable,
        },
        "nonclaims": nonclaims,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=PREFLIGHT_OUTPUT)
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--phase6-rank-preflight", action="store_true")
    parser.add_argument("--phase6s-adaptive-rank5-preflight", action="store_true")
    parser.add_argument("--phase6t-l1-tuning-preflight", action="store_true")
    parser.add_argument("--phase6v-l1-selection-preflight", action="store_true")
    parser.add_argument("--phase6w-same-policy-rank-preflight", action="store_true")
    parser.add_argument("--phase6y-degree-comparator-preflight", action="store_true")
    parser.add_argument("--p88-phase2-degree-comparator-preflight", action="store_true")
    parser.add_argument("--fit", action="store_true")
    parser.add_argument("--training-base-smoke", action="store_true")
    parser.add_argument("--phase6r-adaptive-smoke", action="store_true")
    parser.add_argument("--preflight-json", type=Path, default=PREFLIGHT_OUTPUT)
    parser.add_argument("--target-dimension", type=int, default=36)
    parser.add_argument("--fit-rank", type=int, default=4)
    parser.add_argument(
        "--basis-order",
        type=int,
        default=P85_AUTHOR_SIR_LAGRANGEP_ORDER,
    )
    parser.add_argument(
        "--basis-num-elems",
        type=int,
        default=P85_AUTHOR_SIR_LAGRANGEP_NUM_ELEMS,
    )
    parser.add_argument("--training-sample-count", type=int, default=364320)
    parser.add_argument("--holdout-sample-count", type=int, default=65536)
    parser.add_argument("--audit-sample-count", type=int, default=65536)
    parser.add_argument("--seed", type=int, default=8605)
    parser.add_argument("--optimizer-batch-size", type=int, default=DEFAULT_OPTIMIZER_BATCH_SIZE)
    parser.add_argument("--prefit-steps", type=int, default=DEFAULT_PREFIT_STEPS)
    parser.add_argument("--train-steps", type=int, default=DEFAULT_TRAIN_STEPS)
    parser.add_argument("--learning-rate", type=float, default=DEFAULT_LEARNING_RATE)
    parser.add_argument("--l1-weight", type=float, default=DEFAULT_L1_WEIGHT)
    parser.add_argument("--l2-weight", type=float, default=DEFAULT_L2_WEIGHT)
    parser.add_argument(
        "--logz-anchor-weight",
        type=float,
        default=DEFAULT_LOGZ_ANCHOR_WEIGHT,
    )
    parser.add_argument("--max-seconds", type=int, default=14400)
    parser.add_argument("--memory-cap-mib", type=int, default=12288)
    parser.add_argument("--adaptive-training", action="store_true")
    parser.add_argument("--validation-check-every", type=int, default=DEFAULT_VALIDATION_CHECK_EVERY)
    parser.add_argument("--plateau-patience", type=int, default=DEFAULT_PLATEAU_PATIENCE)
    parser.add_argument("--plateau-min-delta", type=float, default=DEFAULT_PLATEAU_MIN_DELTA)
    parser.add_argument("--lr-reduction-factor", type=float, default=DEFAULT_LR_REDUCTION_FACTOR)
    parser.add_argument("--min-learning-rate", type=float, default=DEFAULT_MIN_LEARNING_RATE)
    parser.add_argument(
        "--early-stop-after-lr-drops",
        type=int,
        default=DEFAULT_EARLY_STOP_AFTER_LR_DROPS,
    )
    parser.add_argument("--serialize-trained-cores", action="store_true")
    parser.add_argument("--train-prior-seed", type=int, default=DEFAULT_TRAIN_PRIOR_SEED)
    parser.add_argument("--train-process-seed", type=int, default=DEFAULT_TRAIN_PROCESS_SEED)
    parser.add_argument("--holdout-prior-seed", type=int, default=DEFAULT_HOLDOUT_PRIOR_SEED)
    parser.add_argument("--holdout-process-seed", type=int, default=DEFAULT_HOLDOUT_PROCESS_SEED)
    parser.add_argument("--audit-prior-seed", type=int, default=DEFAULT_AUDIT_PRIOR_SEED)
    parser.add_argument("--audit-process-seed", type=int, default=DEFAULT_AUDIT_PROCESS_SEED)
    args = parser.parse_args(argv)
    modes = (
        args.preflight_only,
        args.phase6_rank_preflight,
        args.phase6s_adaptive_rank5_preflight,
        args.phase6t_l1_tuning_preflight,
        args.phase6v_l1_selection_preflight,
        args.phase6w_same_policy_rank_preflight,
        args.phase6y_degree_comparator_preflight,
        args.p88_phase2_degree_comparator_preflight,
        args.fit,
        args.training_base_smoke,
        args.phase6r_adaptive_smoke,
    )
    if sum(bool(mode) for mode in modes) > 1:
        parser.error("--preflight-only, --phase6-rank-preflight, --phase6s-adaptive-rank5-preflight, --phase6t-l1-tuning-preflight, --phase6v-l1-selection-preflight, --phase6w-same-policy-rank-preflight, --phase6y-degree-comparator-preflight, --p88-phase2-degree-comparator-preflight, --fit, --training-base-smoke, and --phase6r-adaptive-smoke are mutually exclusive")
    started = time.monotonic()
    if args.fit:
        payload = run_fit_payload(args)
        _write_payload(args.output, payload)
        print(
            json.dumps(
                {"p86_status": payload["status"], "fit_executed": payload["fit_executed"]},
                sort_keys=True,
            )
        )
        return 0 if _fit_status_succeeded(payload["status"]) else 1
    if args.training_base_smoke:
        payload = run_training_base_smoke_payload(args)
        _write_payload(args.output, payload)
        print(
            json.dumps(
                {
                    "p86_status": payload["status"],
                    "training_executed": payload["training_executed"],
                    "post_fit_statuses": _jsonable(payload["post_fit_statuses"]),
                },
                sort_keys=True,
            )
        )
        return 0 if payload["status"] == STATUS_TRAINING_BASE_SMOKE_COMPLETED else 1
    if args.phase6r_adaptive_smoke:
        payload = run_phase6r_adaptive_smoke_payload(args)
        _write_payload(args.output, payload)
        print(
            json.dumps(
                {
                    "p86_status": payload["status"],
                    "training_executed": payload["training_executed"],
                    "post_fit_statuses": _jsonable(payload["post_fit_statuses"]),
                },
                sort_keys=True,
            )
        )
        return 0 if payload["status"] == STATUS_PHASE6R_ADAPTIVE_SMOKE_COMPLETED else 1
    if args.phase6_rank_preflight:
        payload = build_phase6_rank_preflight_payload(output=args.output)
        payload = {
            **payload,
            "preflight_wall_time_seconds": round(time.monotonic() - started, 3),
        }
        _write_payload(args.output, payload)
        print(
            json.dumps(
                {
                    "p86_status": payload["status"],
                    "gate_summary": _jsonable(payload["gate_summary"]),
                },
                sort_keys=True,
            )
        )
        return 0 if payload["gate_summary"]["overall_status"] == "ready_for_exact_claude_agreed_execution" else 1
    if args.phase6s_adaptive_rank5_preflight:
        payload = build_phase6s_adaptive_rank5_preflight_payload(output=args.output)
        payload = {
            **payload,
            "preflight_wall_time_seconds": round(time.monotonic() - started, 3),
        }
        _write_payload(args.output, payload)
        print(
            json.dumps(
                {
                    "p86_status": payload["status"],
                    "gate_summary": _jsonable(payload["gate_summary"]),
                    "candidate_fit_command": payload["candidate_fit_command"],
                },
                sort_keys=True,
            )
        )
        return 0 if payload["gate_summary"]["overall_status"] == "ready_for_exact_claude_agreed_execution" else 1
    if args.phase6t_l1_tuning_preflight:
        payload = build_phase6t_l1_tuning_preflight_payload(output=args.output)
        payload = {
            **payload,
            "preflight_wall_time_seconds": round(time.monotonic() - started, 3),
        }
        _write_payload(args.output, payload)
        print(
            json.dumps(
                {
                    "p86_status": payload["status"],
                    "gate_summary": _jsonable(payload["gate_summary"]),
                    "candidate_fit_command": payload["candidate_fit_command"],
                },
                sort_keys=True,
            )
        )
        return 0 if payload["gate_summary"]["overall_status"] == "ready_for_exact_claude_agreed_execution" else 1
    if args.phase6v_l1_selection_preflight:
        payload = build_phase6v_l1_selection_preflight_payload(output=args.output)
        payload = {
            **payload,
            "preflight_wall_time_seconds": round(time.monotonic() - started, 3),
        }
        _write_payload(args.output, payload)
        print(
            json.dumps(
                {
                    "p86_status": payload["status"],
                    "gate_summary": _jsonable(payload["gate_summary"]),
                    "candidate_fit_commands": payload["candidate_fit_commands"],
                },
                sort_keys=True,
            )
        )
        return 0 if payload["gate_summary"]["overall_status"] == "ready_for_exact_claude_agreed_execution" else 1
    if args.phase6w_same_policy_rank_preflight:
        payload = build_phase6w_same_policy_rank_preflight_payload(output=args.output)
        payload = {
            **payload,
            "preflight_wall_time_seconds": round(time.monotonic() - started, 3),
        }
        _write_payload(args.output, payload)
        print(
            json.dumps(
                {
                    "p86_status": payload["status"],
                    "gate_summary": _jsonable(payload["gate_summary"]),
                    "candidate_fit_commands": payload["candidate_fit_commands"],
                },
                sort_keys=True,
            )
        )
        return 0 if payload["gate_summary"]["overall_status"] == "ready_for_exact_claude_agreed_execution" else 1
    if args.phase6y_degree_comparator_preflight:
        payload = build_phase6y_degree_comparator_preflight_payload(output=args.output)
        payload = {
            **payload,
            "preflight_wall_time_seconds": round(time.monotonic() - started, 3),
        }
        _write_payload(args.output, payload)
        print(
            json.dumps(
                {
                    "p86_status": payload["status"],
                    "gate_summary": _jsonable(payload["gate_summary"]),
                    "candidate_fit_commands": payload["candidate_fit_commands"],
                },
                sort_keys=True,
            )
        )
        return 0 if payload["gate_summary"]["overall_status"] == "ready_for_exact_claude_agreed_execution" else 1
    if args.p88_phase2_degree_comparator_preflight:
        payload = build_p88_phase2_degree_comparator_preflight_payload(
            output=args.output
        )
        payload = {
            **payload,
            "preflight_wall_time_seconds": round(time.monotonic() - started, 3),
        }
        _write_payload(args.output, payload)
        print(
            json.dumps(
                {
                    "p88_status": payload["status"],
                    "gate_summary": _jsonable(payload["gate_summary"]),
                    "candidate_fit_commands": payload["candidate_fit_commands"],
                },
                sort_keys=True,
            )
        )
        return 0 if payload["gate_summary"]["overall_status"] == "ready_for_exact_claude_agreed_execution" else 1
    payload = build_preflight_payload(
        output=args.output,
        target_dimension=args.target_dimension,
        fit_rank=args.fit_rank,
        training_sample_count=args.training_sample_count,
        holdout_sample_count=args.holdout_sample_count,
        audit_sample_count=args.audit_sample_count,
        seed=args.seed,
        optimizer_batch_size=args.optimizer_batch_size,
        prefit_steps=args.prefit_steps,
        train_steps=args.train_steps,
        learning_rate=args.learning_rate,
        l1_weight=args.l1_weight,
        l2_weight=args.l2_weight,
        logz_anchor_weight=args.logz_anchor_weight,
        max_seconds=args.max_seconds,
        memory_cap_mib=args.memory_cap_mib,
    )
    payload = {
        **payload,
        "preflight_wall_time_seconds": round(time.monotonic() - started, 3),
    }
    _write_payload(args.output, payload)
    print(
        json.dumps(
            {
                "p86_status": payload["status"],
                "gate_summary": _jsonable(payload["gate_summary"]),
            },
            sort_keys=True,
        )
    )
    return 0 if payload["gate_summary"]["overall_status"] == "ready_for_exact_claude_agreed_execution" else 1


if __name__ == "__main__":
    raise SystemExit(main())
