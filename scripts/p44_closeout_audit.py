from __future__ import annotations

import json
import sys
from pathlib import Path


RUN_ID = "p44-codex-supervised-20260608-013203"
PHASE_SLUGS = {
    "P44-M0": "target-governance",
    "P44-M1": "lgssm",
    "P44-M2": "cubic-additive-gaussian",
    "P44-M3": "quadratic-observation",
    "P44-M4": "nonlinear-transition",
    "P44-M5": "spatial-sir-diagnostic",
    "P44-M6": "predator-prey-diagnostic",
    "P44-M7": "generalized-sv-target",
}
CLAIM_CLASSES = {
    "P44-M0": "governance",
    "P44-M1": "exact same-target",
    "P44-M2": "same-target approximation gap",
    "P44-M3": "same-target stress diagnostic",
    "P44-M4": "same-target approximation gap with Zhao-Cui T4 nonclaim",
    "P44-M5": "diagnostic-only no equality",
    "P44-M6": "diagnostic-only no equality",
    "P44-M7": "P42 Class D diagnostic-only target definition",
}
CLAIM_EVIDENCE_TERMS = {
    "P44-M0": {
        "result": ("target-governance", "M1 may claim exact same-target", "M5--M6 may run finite closure diagnostics"),
        "review": ("M1", "exact Kalman same-target", "M5--M6", "diagnostic-only"),
        "manifest": ("target-governance labels", "diagnostic-only"),
    },
    "P44-M1": {
        "result": ("exact linear Gaussian", "exact Kalman", "same declared"),
        "review": ("score coverage", "Zhao--Cui artifact-lane nonclaim"),
        "manifest": ("exact LGSSM", "explicit nonclaim"),
    },
    "P44-M2": {
        "result": ("same-target approximation", "no exact CUT4 nonlinear likelihood claim"),
        "review": ("same-target approximation", "No exactness overclaim"),
        "manifest": ("same-target approximation", "Zhao--Cui/fixed-design scalar TT"),
    },
    "P44-M3": {
        "result": ("stress diagnostic", "CUT4 is finite", "large bounded stress gap"),
        "review": ("stress-gap diagnostic", "same-target"),
        "manifest": ("same-target stress gap", "Zhao--Cui/fixed-design scalar TT"),
    },
    "P44-M4": {
        "result": ("same-target", "no Zhao--Cui T=4 accumulation result"),
        "review": ("no Zhao--Cui `T=4` accumulation claim", "nonclaim"),
        "manifest": ("Zhao--Cui T=4 is an explicit executable nonclaim",),
    },
    "P44-M5": {
        "result": ("diagnostic-only", "no matched Zhao--Cui SIR equality target"),
        "review": ("diagnostic-only", "no-Zhao--Cui equality"),
        "manifest": ("diagnostic-only", "no Zhao--Cui equality row is run"),
    },
    "P44-M6": {
        "result": ("diagnostic-only", "no matched non-scalar predator-prey equality target"),
        "review": ("Diagnostic-only", "no CUT4-vs-Zhao--Cui", "equality"),
        "manifest": ("diagnostic-only", "no Zhao--Cui equality row is run"),
    },
    "P44-M7": {
        "result": ("P42 Class D diagnostic only", "no same-target value/gradient equality test is run"),
        "review": ("P42 Class D diagnostic-only", "No CUT4-vs-Zhao--Cui same-target equality"),
        "manifest": ("P42 Class D diagnostic only", "no same-target value/gradient equality test is run"),
    },
}
COMMON_NONCLAIM_TERMS = (
    "no HMC readiness",
    "no paper-scale",
)
COMMON_UNSUPPORTED_CLAIM_TERMS = (
    "HMC readiness",
    "paper-scale",
)
GLOBAL_CLOSEOUT_NONCLAIM_TERMS = (
    "no production analytic score API",
    "no stable public API",
)
EXACT_BLOCKER_CLASSES = {
    "target-definition",
    "implementation",
    "numerical-reference",
    "scientific-evidence",
}


def _artifact_paths(root: Path, phase: str) -> tuple[Path, Path, Path]:
    phase_num = phase.split("M", 1)[1]
    slug = PHASE_SLUGS[phase]
    stem = f"bayesfilter-highdim-zhao-cui-p44-phase{phase_num}-{slug}"
    docs = root / "docs" / "plans"
    return (
        docs / f"{stem}-result-2026-06-07.md",
        docs / f"{stem}-claude-review-ledger-2026-06-07.md",
        docs / f"{stem}-evidence-manifest-{RUN_ID}.json",
    )


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _contains_all(text: str, terms: tuple[str, ...]) -> bool:
    lower_text = text.lower()
    return all(term.lower() in lower_text for term in terms)


def _require_terms(text: str, terms: tuple[str, ...], label: str) -> None:
    for term in terms:
        _require(term.lower() in text.lower(), f"{label} missing term: {term!r}")


def _require_common_boundaries(phase: str, result_text: str, manifest: dict) -> None:
    nonclaims = " ".join(str(item) for item in manifest.get("evidence_contract", {}).get("nonclaims", []))
    combined_nonclaims = f"{result_text}\n{nonclaims}"
    _require_terms(combined_nonclaims, COMMON_NONCLAIM_TERMS, f"{phase} nonclaim boundary")
    if phase in {"P44-M1", "P44-M2", "P44-M3", "P44-M4", "P44-M5", "P44-M6", "P44-M7"}:
        for unsupported in COMMON_UNSUPPORTED_CLAIM_TERMS:
            result_claim = f"No {unsupported}"
            _require(
                result_claim.lower() in combined_nonclaims.lower()
                or f"no {unsupported}".lower() in combined_nonclaims.lower(),
                f"{phase} unsupported claim boundary not negated: {unsupported!r}",
            )


def _require_claim_class_support(phase: str, result_text: str, review_text: str, manifest: dict) -> None:
    support = CLAIM_EVIDENCE_TERMS[phase]
    manifest_text = json.dumps(manifest, sort_keys=True)
    _require_terms(result_text, support["result"], f"{phase} result claim-class support")
    _require_terms(review_text, support["review"], f"{phase} review claim-class support")
    _require_terms(manifest_text, support["manifest"], f"{phase} manifest claim-class support")


def _require_closeout_global_boundaries(root: Path) -> None:
    docs = root / "docs" / "plans"
    result = docs / "bayesfilter-highdim-zhao-cui-p44-phase8-integration-closeout-result-2026-06-07.md"
    manifest = docs / f"bayesfilter-highdim-zhao-cui-p44-phase8-integration-closeout-evidence-manifest-{RUN_ID}.json"
    _require(result.exists(), f"missing P44-M8 result for global closeout boundary audit: {result}")
    _require(manifest.exists(), f"missing P44-M8 manifest for global closeout boundary audit: {manifest}")
    manifest_data = json.loads(manifest.read_text(encoding="utf-8"))
    manifest_text = json.dumps(manifest_data, sort_keys=True)
    combined = f"{result.read_text(encoding='utf-8')}\n{manifest_text}"
    _require_terms(combined, GLOBAL_CLOSEOUT_NONCLAIM_TERMS, "P44-M8 global closeout nonclaim boundary")


def _main() -> int:
    root = Path(__file__).resolve().parents[1]
    rows = []
    for phase in PHASE_SLUGS:
        token = f"PASS_{phase.replace('-', '_')}_CODE_GOVERNANCE"
        result, review, manifest_path = _artifact_paths(root, phase)
        for label, path in (("result", result), ("review", review), ("manifest", manifest_path)):
            _require(path.exists(), f"missing {phase} {label}: {path}")
        result_text = result.read_text(encoding="utf-8")
        review_text = review.read_text(encoding="utf-8")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

        _require(f"Status: `{token}`" in result_text, f"{phase} result missing pass token")
        _require(f"p44_claude_code_governance_verdict: `{token}`" in review_text, f"{phase} review missing pass verdict")
        _require(manifest["status"] == token, f"{phase} manifest status mismatch")
        _require(manifest["pass_token"] == token, f"{phase} manifest token mismatch")
        _require(manifest["evidence_chain"]["PHASE_PASS"] is True, f"{phase} manifest phase pass false")
        _require(
            manifest["evidence_chain"]["TRACEABILITY_UPDATED_OR_NONCLAIM_RECORDED"] is True,
            f"{phase} traceability/nonclaim false",
        )
        commands = manifest["commands"]
        _require(len(commands) == 2, f"{phase} expected exactly two commands")
        for index, command in enumerate(commands):
            log_path = root / command["log_path"]
            _require(log_path.exists(), f"{phase} command {index} missing log")
            log_text = log_path.read_text(encoding="utf-8")
            _require(f"p44_run_id: `{RUN_ID}`" in log_text, f"{phase} log {index} missing run id")
            _require(f"p44_phase: `{phase}`" in log_text, f"{phase} log {index} missing phase marker")
            _require(f"p44_command_index: `{index}`" in log_text, f"{phase} log {index} missing command index")
            _require("p44_command_exit_code: `0`" in log_text, f"{phase} log {index} missing zero exit")

        _require_claim_class_support(phase, result_text, review_text, manifest)
        _require_common_boundaries(phase, result_text, manifest)

        rows.append(
            {
                "phase": phase,
                "claim_class": CLAIM_CLASSES[phase],
                "claim_class_supported_by_artifacts": True,
                "token": token,
                "result": result.relative_to(root).as_posix(),
                "manifest": manifest_path.relative_to(root).as_posix(),
                "veto_status": manifest["diagnostics"]["veto_status"],
            }
        )

    _require_closeout_global_boundaries(root)

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "phase_count": len(rows),
                "blocker_classes": sorted(EXACT_BLOCKER_CLASSES),
                "content_veto_audit": "claim-class and common nonclaim terms verified from prior artifacts; global score/public API nonclaims verified from M8 closeout artifacts",
                "rows": rows,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(_main())
    except Exception as exc:
        print(f"P44 closeout audit failed: {exc}", file=sys.stderr)
        raise
