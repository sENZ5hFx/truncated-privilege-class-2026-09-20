#!/usr/bin/env python3
"""
Truncation-Privilege Class (TPC) scoring engine
Session: 2026-09-25 (buildout of 2026-09-20 seed)
Author: Haley Bird (seed README credits Haley Bird alone)

Research-stage classification heuristic. NOT a measurement of nature,
NOT a physical discovery, NOT peer review, NOT a patent.

TPC definition
--------------
A coefficient-omission event (truncation of a series, regularization
zeroing, rounding, covariate dropping, thresholding, discretization,
bucketing, zero-imputation) followed by downstream treatment of the
omitted coefficients as MEASURED ZERO rather than unmeasured. The exact
zero enters subsequent mathematics -- confidence intervals, predictions,
causal claims, decisions -- injecting information not present in the data.

TPC is the DUAL of PPC (Patch-Proliferation Class, 2026-09-08):
  PPC: discredited coordinate + residual -> ADD phantom unobservable DOF
       -> pipeline stays intact -> coordinate keeps reducing data.
       Injected information: degrees of freedom never measured. (+DOF)
  TPC: full model + omission event -> REMOVE real DOF, set exactly to 0
       -> downstream treats 0 as measured -> remainder privileged.
       Injected information: a measurement (zero) never made. (-DOF)
Both privilege a coordinate by injecting information not in the data,
from opposite directions.

Gates (all must pass for STRUCTURAL_GAP)
----------------------------------------
G1  Coefficients were omitted by truncation / regularization / rounding /
    dropping / thresholding / discretization / bucketing / zero-imputation
    -- NOT by measurement, NOT by physical law (symmetry-forbidden terms
    are measured-by-theory, not TPC).
G2  Downstream analysis treats omitted coefficients as measured-zero: the
    exact 0 enters subsequent mathematics (CIs, predictions, causal
    claims, decisions) rather than being carried as unmeasured/uncertain.
G3  The zero-treatment affects conclusions: a published claim, decision,
    or downstream computation differs from the honest-unknown treatment.
G4  Not PPC: the dual-direction test. The move must be DOF-REMOVAL
    (privilege flows to the remainder). Phantom-DOF-addition is PPC
    -> KILLED.
G5  Not another archived class (archive subtraction over 20 classes).
G6  Duality mirror: the instance exhibits the mirror image of a PPC
    signature -- a coordinate REMAINDER is retained/trusted BECAUSE the
    omitted part was zeroed (parallels PPC's coordinate retained because
    residuals were patched).

Scores are classification heuristics, not measurements of nature.
Novelty is capped: the statistical literature owns the instances
(post-selection inference, Harrell, Little & Rubin, ...); the class is
the cross-realm named move plus the PPC-duality formalization, after
archive subtraction.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import json
import sys


ARCHIVED_CLASSES = [
    "Dark Biosphere Hypothesis",
    "Cosmic-Bio Resonance",
    "Undersampling",
    "Deep-biosphere-as-space-prior",
    "Ritual Nyquist Law",
    "Transducer-Absence Class (TAC)",
    "Cadence Mismatch",
    "Named-Cause Residual (NCR)",
    "Failed-Adjudication Class (FAC)",
    "Clock-Incommensurability Class (CIC)",
    "Join-Absence Class (JAC)",
    "Interscale-Operator Absence Class (IOA)",
    "Destructive-Inquiry Class (DIC)",
    "Patch-Proliferation Class (PPC)",
    "Channel-Monopoly Class (CMC)",
    "Observable-Aliasing Class (OAC)",
    "Unrecorded-Cessation Class (UCC)",
    "Unclosed-Redox-Column (UPRC)",
    "Coupling-Incompleteness (CIP)",
    "Exchangeability-Failure Class (EFC)",
]

ZEROED_CONTROLS = [
    "dark dimension DE x DM coupling",   # PPC primary -> G4 kill
    "katus shortfall",                    # UCC primary -> G5 kill
    # NOTE: the symmetry-forbidden control is deliberately NOT in this list:
    # it must flow through the gates and fail G1 naturally, demonstrating
    # that zero-by-physical-law is excluded by the gate, not by the list.
]

NOVELTY_CAP = 0.45  # instances are textbook statistics; class = named move + duality
COHERENCE_PRIOR = 0.74

# Omission kinds that count as DOF-REMOVAL (TPC direction)
TPC_DIRECTIONS = {
    "regularization", "truncation", "rounding", "dropping",
    "thresholding", "discretization", "bucketing", "imputation",
}
# Kinds that count as DOF-ADDITION (PPC direction)
PPC_DIRECTIONS = {"phantom_dof", "patch"}


def dual_direction(omission_kind: str) -> str:
    """Return the duality direction of an omission kind.

    '-DOF' = TPC direction (removal, privilege to the remainder).
    '+DOF' = PPC direction (phantom addition, privilege to the coordinate).
    'NONE' = neither (e.g. physical law).
    """
    k = (omission_kind or "").lower().strip()
    if k in TPC_DIRECTIONS:
        return "-DOF"
    if k in PPC_DIRECTIONS:
        return "+DOF"
    return "NONE"


@dataclass
class TPCInstance:
    id: str
    realm: str
    name: str
    source: str
    source_date: str
    omission_kind: str  # one of TPC_DIRECTIONS / PPC_DIRECTIONS / other
    omitted: str        # what was omitted
    zero_treatment: str # how downstream treats the omitted as measured-zero
    known_fact: str
    gap_statement: str
    omission_by_truncation: bool   # G1
    treated_as_measured_zero: bool # G2
    conclusion_affected: bool      # G3
    prior_class_overlap: str       # empty or class acronym
    consequence: float   # 0-1 severity of downstream consequence
    freshness: float     # 0-1, 1 = 2026 lock
    uniqueness: float    # 0-1, inverse saturation of THIS framing
    g2_strength: float   # 0-1 how strongly zero enters downstream math
    duality_clarity: float  # 0-1 how cleanly it mirrors a PPC signature
    notes: str = ""


def _clip(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def score_tpc_instance(inst: TPCInstance) -> dict[str, Any]:
    """Score one candidate against TPC gates.

    Edge cases:
    - ZEROED controls always return score 0, status ZEROED
    - PPC-direction instances -> KILLED via G4 (dual-direction test)
    - prior_class_overlap in archive -> KILLED (hard) or PENALIZED (soft)
    - G1/G2/G3 failures -> PENALIZED (omission real but privilege weak)
    """
    reasons: list[str] = []
    failed: list[str] = []

    name_l = (inst.name + " " + inst.id).lower()
    for z in ZEROED_CONTROLS:
        if z.lower() in name_l:
            return {
                "id": inst.id, "name": inst.name, "realm": inst.realm,
                "status": "ZEROED", "score": 0.0,
                "failed_gates": ["ZEROED_CONTROL"],
                "reasons": [f"Archive-zeroed control: {z}"],
                "gates": {},
            }

    direction = dual_direction(inst.omission_kind)

    g1 = bool(inst.omission_by_truncation) and direction == "-DOF"
    g2 = bool(inst.treated_as_measured_zero)
    g3 = bool(inst.conclusion_affected)
    if not g1:
        failed.append("G1")
        reasons.append("Omission not by truncation/regularization/rounding/dropping (or by physical law)")
    if not g2:
        failed.append("G2")
        reasons.append("Downstream does not treat omitted as measured-zero")
    if not g3:
        failed.append("G3")
        reasons.append("Zero-treatment does not affect conclusions")

    overlap = (inst.prior_class_overlap or "").upper().strip()
    hard_kill = {
        "PPC": "G4", "DIC": "G5", "TAC": "G5", "CIC": "G5",
        "UCC": "G5", "OAC": "G5", "EFC": "G5", "CMC": "G5",
        "CBR": "G5", "DBH": "G5", "UPRC": "G5", "CIP": "G5",
    }
    penalize = {
        "UND": "G5", "UNDERSAMPLING": "G5", "NCR": "G5", "FAC": "G5",
        "JAC": "G5", "IOA": "G5", "INSTITUTIONAL": "G3",
    }

    # G4: dual-direction test — phantom addition is PPC, not TPC
    g4 = direction == "-DOF" and overlap != "PPC"
    # G5: archive subtraction
    g5 = overlap not in hard_kill and overlap not in penalize
    # G6: duality mirror — remainder privileged because omitted was zeroed
    g6 = bool(inst.duality_clarity >= 0.5)

    status = "STRUCTURAL_GAP"
    if direction == "+DOF" or overlap == "PPC":
        failed.append("G4")
        reasons.append("Dual-direction test: phantom-DOF addition is PPC, not TPC -> KILLED")
        status = "KILLED"
    elif overlap in hard_kill:
        failed.append(hard_kill[overlap])
        reasons.append(f"Hard archive overlap: {overlap}")
        status = "KILLED"
    elif overlap in penalize:
        failed.append(penalize[overlap])
        reasons.append(f"Soft archive overlap: {overlap} — penalized, not promoted")
        status = "PENALIZED"

    if status == "STRUCTURAL_GAP" and failed:
        status = "PENALIZED"
    if status == "STRUCTURAL_GAP" and not g6:
        failed.append("G6")
        reasons.append("Duality mirror weak: remainder-privilege not evidenced")
        status = "PENALIZED"

    base = (
        0.30 * _clip(inst.uniqueness)
        + 0.25 * _clip(inst.freshness)
        + 0.20 * _clip(inst.consequence)
        + 0.15 * _clip(inst.g2_strength)
        + 0.10 * _clip(inst.duality_clarity)
    )
    if status == "STRUCTURAL_GAP":
        score = 100.0 * _clip(base)
    elif status == "PENALIZED":
        score = 100.0 * _clip(base * 0.45)
    else:
        score = 0.0

    return {
        "id": inst.id, "name": inst.name, "realm": inst.realm,
        "status": status, "score": round(score, 2),
        "failed_gates": failed, "reasons": reasons,
        "source": inst.source, "source_date": inst.source_date,
        "omission_kind": inst.omission_kind, "dual_direction": direction,
        "omitted": inst.omitted, "zero_treatment": inst.zero_treatment,
        "known_fact": inst.known_fact, "gap_statement": inst.gap_statement,
        "notes": inst.notes,
        "gates": {"G1": g1, "G2": g2, "G3": g3, "G4": g4, "G5": g5, "G6": g6},
        "prior_class_overlap": overlap,
    }


# ---------------------------------------------------------------------------
# Iterates
# ---------------------------------------------------------------------------

def zero_privilege_index(n_omitted: int, n_retained: int,
                         claim_certainty: float) -> dict[str, Any]:
    """Iterate #1 — Zero-Privilege Index (ZPI).

    Heuristic for how much of a downstream claim's certainty is carried by
    the zero-treatment rather than the data: certainty * omitted share.
    All inputs are author judgments, not measurements.
    """
    if n_omitted < 0 or n_retained < 0:
        raise ValueError("counts cannot be negative")
    if n_omitted + n_retained == 0:
        return {"status": "NO_COEFFICIENTS", "privilege_index": 0.0}
    share = n_omitted / (n_omitted + n_retained)
    pi = _clip(claim_certainty) * share
    return {
        "n_omitted": n_omitted, "n_retained": n_retained,
        "claim_certainty": _clip(claim_certainty),
        "privilege_index": round(pi, 4),
        "status": "PRIVILEGED" if pi >= 0.25 else "LOW_PRIVILEGE",
        "note": "Heuristic: certainty attributed to zeros vs data. Not a measurement.",
    }


def regularization_zero_crossing(coef_path: list[tuple[float, float]]) -> dict[str, Any]:
    """Iterate #2 — Regularization zero-crossing.

    Given a coefficient path as (penalty, coef) pairs in increasing penalty
    order, find the penalty at which the coefficient first hits exactly zero.
    Downstream use of the post-crossing model as 'no effect' is the TPC move.
    """
    if not coef_path:
        raise ValueError("empty coefficient path")
    crossing = None
    for penalty, coef in coef_path:
        if coef == 0.0:
            crossing = penalty
            break
    return {
        "n_points": len(coef_path),
        "zero_crossing_penalty": crossing,
        "status": "CROSSED_TO_ZERO" if crossing is not None else "NEVER_ZEROED",
        "tpc_reading": (
            "Coefficient omitted by regularization at penalty "
            f"{crossing}; any downstream 'no effect' claim treats this "
            "omission as a measurement."
            if crossing is not None else
            "Coefficient never zeroed on this path; no TPC event."
        ),
    }


def tail_energy_gap(tail_energy: float, admitted_uncertainty: float) -> dict[str, Any]:
    """Iterate #3 — Tail-energy gap (series-truncation privilege).

    For a truncated series with known omitted tail energy E_tail and a
    downstream-admitted uncertainty U: gap = E_tail - U. Positive gap means
    the truncation privilege is unadmitted -- the zeroed tail carries more
    energy than the analysis admits as uncertain.
    """
    gap = tail_energy - admitted_uncertainty
    return {
        "tail_energy": tail_energy,
        "admitted_uncertainty": admitted_uncertainty,
        "gap": round(gap, 6),
        "status": "UNADMITTED_PRIVILEGE" if gap > 0 else "PRIVILEGE_ADMITTED",
        "note": "Heuristic on author-supplied energies. Not a measurement of nature.",
    }

# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------


def run_engine() -> dict[str, Any]:
    from tpc_catalog import build_catalog
    catalog = build_catalog()
    scored = [score_tpc_instance(i) for i in catalog]
    scored.sort(key=lambda r: (-r["score"], r["name"]))

    by_status: dict[str, int] = {}
    for r in scored:
        by_status[r["status"]] = by_status.get(r["status"], 0) + 1

    gaps = [r for r in scored if r["status"] == "STRUCTURAL_GAP"]
    primary = gaps[0] if gaps else None

    # Iterate 1: Zero-Privilege Index on representative (omitted, retained, certainty)
    zpi = [
        zero_privilege_index(8, 4, 0.95),    # LASSO-like: 8 zeroed, 4 kept, high certainty
        zero_privilege_index(1, 1, 0.90),    # fixed-effect tau^2: 1 variance zeroed
        zero_privilege_index(3, 400, 0.80),  # GWAS PCs: 3 kept of 403
    ]

    # Iterate 2: regularization zero-crossing on a synthetic LASSO path
    path = [(0.01 * k, max(0.0, 0.42 - 0.05 * k)) for k in range(12)]
    rzc = regularization_zero_crossing(path)

    # Iterate 3: tail-energy gap on a synthetic truncated series
    teg = tail_energy_gap(tail_energy=0.18, admitted_uncertainty=0.05)

    winning = "Truncation-Privilege Class" if primary else "NONE"
    novelty = NOVELTY_CAP if primary else 0.0
    coherence = COHERENCE_PRIOR if primary else 0.0

    return {
        "session_id": "2026-09-25-tpc-truncation-privilege",
        "timestamp": "2026-09-25T08:15:00-04:00",
        "seed": "github.com/sENZ5hFx/truncated-privilege-class-2026-09-20 (single-commit README, 2026-09-20)",
        "winning_class": winning,
        "novelty_cap": novelty,
        "coherence": coherence,
        "primary": primary,
        "status_counts": by_status,
        "ranked": scored,
        "iterate_zero_privilege_index": zpi,
        "iterate_regularization_zero_crossing": rzc,
        "iterate_tail_energy_gap": teg,
        "archived_classes_subtracted": ARCHIVED_CLASSES,
        "zeroed_controls": ZEROED_CONTROLS,
        "duality": {
            "ppc": "+DOF: add phantom unobservable DOF; pipeline intact; coordinate keeps reducing data",
            "tpc": "-DOF: remove real DOF, set exactly 0; downstream treats 0 as measured; remainder privileged",
            "shared": "both inject information not in the data; both privilege a coordinate",
        },
        "claim_hygiene": (
            "Research-stage classification. Not a physical discovery, not peer review, "
            "not a patent. Scores are a classification heuristic, not measurements of nature. "
            "Instances are textbook statistics; the class is the cross-realm named move plus "
            "the PPC-duality formalization, after archive subtraction. "
            "The seed README (2026-09-20) already declares TPC the dual of PPC; this buildout "
            "formalizes that declaration."
        ),
    }


def render_text(result: dict[str, Any]) -> str:
    lines = []
    lines.append("=" * 72)
    lines.append(f"WINNING CLASS: {result['winning_class']}")
    lines.append(f"novelty_cap {result['novelty_cap']} | coherence {result['coherence']}")
    sc = result["status_counts"]
    lines.append(
        f"STRUCTURAL_GAP {sc.get('STRUCTURAL_GAP', 0)} | "
        f"PENALIZED {sc.get('PENALIZED', 0)} | "
        f"KILLED {sc.get('KILLED', 0)} | "
        f"ZEROED {sc.get('ZEROED', 0)}"
    )
    if result["primary"]:
        p = result["primary"]
        lines.append(f"primary {p['id']} {p['score']}")
    lines.append("=" * 72)
    lines.append("")
    lines.append(f"{'score':>7}  {'status':<16}  {'realm':<12}  name")
    lines.append("-" * 72)
    for r in result["ranked"]:
        lines.append(f"{r['score']:7.2f}  {r['status']:<16}  {r['realm']:<12}  {r['name']}")
    lines.append("")
    lines.append("DUALITY (PPC <-> TPC)")
    lines.append(f"  PPC (+DOF): {result['duality']['ppc']}")
    lines.append(f"  TPC (-DOF): {result['duality']['tpc']}")
    lines.append("")
    lines.append("ITERATE 1 — Zero-Privilege Index")
    for w in result["iterate_zero_privilege_index"]:
        lines.append(f"  omitted={w['n_omitted']} retained={w['n_retained']} "
                     f"certainty={w['claim_certainty']} -> PI={w['privilege_index']} {w['status']}")
    lines.append("")
    lines.append("ITERATE 2 — Regularization zero-crossing")
    rzc = result["iterate_regularization_zero_crossing"]
    lines.append(f"  {rzc['status']} at penalty={rzc['zero_crossing_penalty']}")
    lines.append(f"  {rzc['tpc_reading']}")
    lines.append("")
    lines.append("ITERATE 3 — Tail-energy gap")
    teg = result["iterate_tail_energy_gap"]
    lines.append(f"  tail={teg['tail_energy']} admitted={teg['admitted_uncertainty']} "
                 f"gap={teg['gap']} {teg['status']}")
    lines.append("")
    lines.append(result["claim_hygiene"])
    return "\n".join(lines)


def main() -> int:
    result = run_engine()
    text = render_text(result)
    print(text)
    out_json = "tpc_engine_output.json"
    out_txt = "tpc_engine_output.txt"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write(text + "\n")
    print(f"\nWrote {out_json}")
    print(f"Wrote {out_txt}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
