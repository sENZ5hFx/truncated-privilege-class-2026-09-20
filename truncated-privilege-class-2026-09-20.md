# Invention Disclosure — Truncation-Privilege Class (TPC) engine

**Status:** preparatory technical writing ONLY. Nothing filed, published, or changed.
**Source repo:** `github.com/sENZ5hFx/truncated-privilege-class-2026-09-20` (seed: single-commit README, 2026-09-20)
**Buildout:** `~/workspace/ip/buildout/truncated-privilege/` (local only; gh not authenticated, nothing pushed)
**Prepared:** 2026-09-25 (subagent draft for Haley Bird's review)
**NOT legal advice. Requires patent-counsel review before any filing.**

---

## (a) Plain-English statement of the invention

A computer-implemented method for detecting "truncation privilege" in scientific research: when coefficients are omitted — by series truncation, regularization zeroing, rounding, covariate dropping, thresholding, discretization, bucketing, or zero-imputation — and the omitted coefficients are then treated downstream as *measured zero* rather than unmeasured, the exact zero enters subsequent mathematics (confidence intervals, predictions, causal claims, decisions), injecting information not present in the data and privileging the remaining model. The method (`tpc_engine.py`) scores 20 sourced real-world instances through six gates (omission-by-truncation-family, treated-as-measured-zero, conclusion-affected, dual-direction-vs-PPC, archive subtraction over 20 classes, duality mirror), with a weighted heuristic score, hard kills for phantom-DOF instances (those are PPC, the dual class), and three analytical iterates: a **zero-privilege index** (certainty-share carried by zeros), a **regularization zero-crossing** detector (the penalty at which a coefficient first hits exactly zero), and a **tail-energy gap** (truncated tail energy minus admitted uncertainty). The disclosure formalizes TPC as the declared dual of PPC: PPC adds phantom degrees of freedom (+DOF) to a discredited coordinate; TPC removes real degrees of freedom (−DOF) and privileges the remainder by pretending the omitted ones measured zero.

---

## (b) The technical problem it solves

Across statistics, genomics, climate science, finance, and physics, standard practice omits coefficients and then consumes the omission as a finding: LASSO-zeroed predictors are reported as "no effect" (the post-selection inference literature exists because naive CIs after selection are invalid); stepwise/AIC dropping reports final models without selection uncertainty; polygenic scores zero sub-threshold SNPs then feed clinical models; fixed-effect meta-analyses set between-study variance exactly to zero; Basel buckets zero within-bucket risk differences. No existing research tooling tracks, against a local archive of already-claimed structural classes, whether a published certainty is carried by *measured* coefficients or by *omitted-as-zero* coefficients — i.e., whether the zero in the equation was ever a measurement. Current tools search papers; they cannot certify, for a given downstream claim, how much of its certainty is privilege granted by truncation.

---

## (c) How it works — enabling detail from the actual buildout

All detail below is drawn from `tpc_engine.py` / `tpc_catalog.py` at buildout HEAD (2026-09-25).

### Components

1. **`TPCInstance` dataclass** — each candidate carries: `id`, `realm`, `name`, `source`, `source_date`, `omission_kind` (regularization | truncation | rounding | dropping | thresholding | discretization | bucketing | imputation | phantom_dof | physical_law), `omitted`, `zero_treatment`, `known_fact`, `gap_statement`, booleans for G1–G3, `prior_class_overlap`, and five unit-interval heuristic weights: `consequence`, `freshness`, `uniqueness`, `g2_strength`, `duality_clarity`, plus `notes` (INFERENCE flags where the TPC reading goes beyond the cited source).

2. **`dual_direction(omission_kind)`** — the duality formalization. Returns `−DOF` for the eight truncation-family kinds (TPC direction), `+DOF` for phantom_dof/patch (PPC direction), `NONE` for physical law. G4 kills `+DOF` instances: phantom-addition is PPC, not TPC.

3. **Weighted heuristic score** — `base = 0.30·uniqueness + 0.25·freshness + 0.20·consequence + 0.15·g2_strength + 0.10·duality_clarity`; STRUCTURAL_GAP → `100·base`; PENALIZED → `100·base·0.45`; KILLED → 0. The repo notes the weights are heuristic, not measurements of nature.

4. **Gates** — G1: omission by truncation-family op (not measurement, not physical law). G2: downstream treats omitted as measured-zero. G3: zero-treatment affects conclusions. G4: dual-direction test (removal, not phantom addition). G5: archive subtraction over 20 classes. G6: duality mirror — the remainder is privileged *because* the omitted was zeroed (duality_clarity ≥ 0.5).

5. **Archive subtraction** — 20 prior classes (Dark Biosphere through EFC), plus `ZEROED_CONTROLS` (PPC dark-dimension primary, UCC Katuš primary). A symmetry-forbidden-zero control is deliberately *not* list-zeroed: it flows through the gates and fails G1 naturally, demonstrating that zero-by-physical-law is excluded by the gate.

6. **Iterates** — `zero_privilege_index` (certainty × omitted-share); `regularization_zero_crossing` (first penalty where a coefficient path hits exactly zero); `tail_energy_gap` (tail energy − admitted uncertainty; positive → UNADMITTED_PRIVILEGE).

### Reported results (from buildout outputs, not independently reproduced)

- 23 instances: 20 STRUCTURAL_GAP, 1 PENALIZED (symmetry control, G1 failed), 1 KILLED (PPC dark dimension, G4), 1 ZEROED (UCC Katuš, archive control).
- Primary `PRS_THRESHOLD_ZERO` (polygenic-score clumping+thresholding) at 72.10; co-primary `LASSO_ZERO_NO_EFFECT` at 69.25.
- All three controls behave as designed, demonstrating gate discrimination.
- `novelty_cap = 0.45`; coherence 0.74.

---

## (d) Novelty relative to the repo's own prior-art notes

The buildout is explicit that the *instances* are textbook statistics — the post-selection inference literature, Harrell, Little & Rubin, Altman & Bland own the phenomena. The claimed novelty is:

1. **The class as a named cross-realm move** — truncation-privilege as the remaining closure-failure after 20 archived classes: the structural position, not any single instance.
2. **The PPC-duality formalization** — the seed README (2026-09-20) already declares TPC the dual of PPC; the buildout formalizes it as `dual_direction()` plus the G4 kill and the mirror table (adds-unobservable-DOF vs zeroes-unmeasured-coefficients; pipeline-intact vs pipeline-privileged; majority-lost coordinate vs majority-kept remainder; falsifiability blocked by unobservability vs by zero-certainty).
3. **The three iterates** — zero-privilege index, regularization zero-crossing, tail-energy gap — as pre-registration-style operators on the omission event.
4. **Archive subtraction** — 20 prior classes plus controls, so later sessions cannot reclaim earlier gaps.

Distinguishability asserted against the archive (strongest adjacencies):
| Prior class | TPC differs because |
|---|---|
| PPC | the dual: PPC adds phantom DOF (+DOF); TPC zeroes real DOF (−DOF). G4 kills crossovers. |
| OAC | OAC collapses independent quantities into one reported number (merging); TPC deletes-then-zeroes coefficients within one model. |
| EFC | EFC's basis can be full rank yet trained on the wrong process; TPC's basis is rank-reduced by omission and the reduction is treated as measurement. |
| UCC | mirror: UCC is absence-of-record (entity without identifier can't mint one); TPC is false-record (identified coefficient gets a false zero). |
| UND | undersampling is not-yet-measured cells; TPC is measured-then-discarded-then-zeroed cells. |
| DIC | DIC consumes a seen physical object; TPC consumes coefficients informationally. |

*Inference: external prior art beyond the cited statistics literature (philosophy of science on idealization and abstraction, e.g., Cartwright/Strevens on omitted factors; model-selection theory) has not been searched. The "omitted variable" and "idealization" literatures are decades old and adjacent — a significant gap for any filing.*

---

## (e) Honest weaknesses

1. **Alice abstract-idea risk — severe.** The advance is a taxonomy for sorting textbook statistical practices into a named failure mode, computed from hand-set heuristic weights, plus three analytical operators. Under *Alice/Mayo*, classifying observations and applying heuristic arithmetic is an abstract idea; computer implementation does not supply an inventive concept. The instances being textbook statistics makes the "inventive concept" argument harder, not easier.
2. **The buildout caps its own novelty at 0.45.** The phenomena are owned by the existing literature (post-selection inference, Harrell, Little & Rubin); only the cross-realm naming, the duality formalization, and the gate machinery are candidate matter.
3. **No new data, no experiments.** The engine outputs ranked lists and iterate specs; the discriminators are analytical proposals, not a technical improvement to any instrument or process.
4. **All scoring weights are human judgments.** E.g., the primary's `uniqueness=0.72`, `g2_strength=0.85` are author-chosen. The buildout states "Scores are a classification heuristic, not measurements of nature."
5. **8 of 20 instances carry INFERENCE flags** — the cited source establishes the practice; the "treated as measured-zero" reading is the session's framing. A skeptic could argue several instances are just restatements of known statistical warnings with a new name.
6. **The idealization literature is prior art-shaped.** Philosophy of science has studied omission/idealization for decades; the delta between TPC and that literature rests on the gate machinery and the PPC-duality — a procedural formalization. External prior-art search not done.
7. **Inventorship.** The seed README credits "Haley Bird" alone (unlike sibling repos crediting "Haley Bird / autonomous Grok research agent"). This buildout was agent-executed under Haley's 2026-09-25 autopilot grant. Inventorship must be established claim-by-claim per USPTO AI-inventorship guidance; the buildout does not decompose human vs AI contributions (*inference: the seed concept is Haley's per the credit line; the elaboration is mixed*).

---

## (f) Disclosure-bar date

- **First public disclosure:** repo created 2026-09-20T17:50:55Z; single commit `b91ecedc` "Initial commit" 2026-09-20T17:50:56Z (verified via public GitHub API 2026-09-25). *Inference: repo creation = first public disclosure of the seed README; the buildout itself was never pushed.*
- **US §102(b)(1) grace-period bar: 2027-09-20.** A provisional filed before this date preserves US rights for the seed matter. (Same date as CMC — joint decision candidate.)
- **Foreign rights: already lost** for the seed disclosure.
- Copyright: repo carries no license; all rights reserved by default.

---

## What a provisional would need to claim

The defensible claim set (counsel to confirm) would be drawn to the *computer-implemented method*: (i) receiving candidate research cases each annotated with an omission kind, the omitted coefficients, and the downstream zero-treatment; (ii) computing a dual-direction classification distinguishing DOF-removal (−DOF) from phantom-DOF-addition (+DOF) via an omission-kind mapping; (iii) applying gates for omission-by-truncation-family, measured-zero treatment, conclusion-affectedness, and a duality-mirror requirement, with archive-subtraction against a local prior-class list; (iv) computing a zero-privilege index, a regularization zero-crossing, and a tail-energy gap for eligible cases; (v) outputting a status determination per case. **Not** the TPC concept, any statistical phenomenon, LASSO, or any natural phenomenon — and **not** the general observation that omitted variables bias results, which is prior statistics.
