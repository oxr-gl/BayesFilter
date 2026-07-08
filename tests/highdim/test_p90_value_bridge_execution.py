from __future__ import annotations

import importlib.util
from pathlib import Path


_CONTRACT_TEST_PATH = Path(__file__).with_name("test_p90_value_bridge_contract.py")
_SPEC = importlib.util.spec_from_file_location(
    "p90_value_bridge_contract_helpers",
    _CONTRACT_TEST_PATH,
)
assert _SPEC is not None
assert _SPEC.loader is not None
_CONTRACT_MODULE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_CONTRACT_MODULE)


def test_p90_phase3_source_scalar_matches_author_formula_replay() -> None:
    _CONTRACT_MODULE.run_p90_phase3_source_scalar_matches_author_formula_replay()
