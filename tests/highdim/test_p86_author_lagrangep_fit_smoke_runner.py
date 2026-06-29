from __future__ import annotations

import importlib.util
from pathlib import Path
from types import SimpleNamespace


def _load_runner():
    script_path = Path(__file__).resolve().parents[2] / "scripts/p86_author_lagrangep_fit_smoke.py"
    spec = importlib.util.spec_from_file_location("p86_author_lagrangep_fit_smoke", script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_p86_phase4_schema_payload_preserves_author_lagrangep_algebraic_route(tmp_path) -> None:
    runner = _load_runner()
    output = tmp_path / "schema.json"

    payload = runner.schema_payload(
        output,
        "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p86_author_lagrangep_fit_smoke.py --schema-only",
        dimension=2,
        seed=8604,
    )

    route = payload["route_manifest"]
    assert payload["status"] == "P86_PHASE4_SCHEMA_READY_NOT_FIT"
    assert payload["fit_smoke_executed"] is False
    assert payload["gate_summary"]["route_manifest_ok"] is True
    assert route["basis_family"] == "lagrangep"
    assert route["basis_order"] == 4
    assert route["basis_num_elems"] == 8
    assert route["basis_dim_tuple"] == (33, 33)
    assert route["domain_map"] == "algebraic"
    assert route["domain_scale"] == 1.0
    assert route["route_changing_cli"] is False
    assert payload["environment"]["intentional_gpu_hiding"] is True


def test_p86_phase4_exact_fit_command_is_frozen() -> None:
    runner = _load_runner()

    assert runner.EXPECTED_FIT_COMMAND == (
        "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
        "scripts/p86_author_lagrangep_fit_smoke.py --fit-smoke --dimension 2 "
        "--sample-count 8 --optimizer-steps 1 --seed 8604 --max-seconds 60 "
        "--output "
        "docs/plans/bayesfilter-highdim-zhao-cui-p86-phase4-tiny-author-route-fit-smoke-2026-06-24.json"
    )


def test_p86_phase4_fit_mode_records_exact_frozen_command() -> None:
    runner = _load_runner()
    args = SimpleNamespace(
        fit_smoke=True,
        output=runner.FIT_OUTPUT,
        dimension=2,
        sample_count=8,
        optimizer_steps=1,
        seed=8604,
        max_seconds=60.0,
    )

    assert runner._command_for_args(args) == runner.EXPECTED_FIT_COMMAND
