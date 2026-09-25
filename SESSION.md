# SESSION.md — Truncation-Privilege Class (TPC) buildout

**Session:** 2026-09-25 (buildout of 2026-09-20 seed)
**Seed:** `github.com/sENZ5hFx/truncated-privilege-class-2026-09-20` — single-commit README (2026-09-20T17:50:55Z), entire prior content: *"Autonomous research session 2026-09-20: Truncation-Privilege Class (TPC). Omitted coefficients treated as measured-zero inject information not in the data. Dual of PPC. Research-stage classification — not a physical discovery, not peer review, not a patent. Author: Haley Bird."*
**Author of record:** Haley Bird (seed credits Haley Bird alone; no AI co-credit in the seed).
**Status:** preparatory research + code ONLY. Nothing filed, published, or pushed. Built locally; gh not authenticated.

---

## 1. What the seed declared

The seed README already declares two things: (a) the class definition (omitted coefficients treated as measured-zero inject information not in the data), and (b) the PPC-duality. This buildout's job was to formalize both, not to invent them. The duality formalization is therefore an *elaboration of a declared seed claim*, recorded here so counsel can see the provenance.

## 2. Duality formalization (PPC ↔ TPC)

- **PPC (+DOF):** discredited coordinate + residual → ADD phantom unobservable DOF → pipeline stays intact → coordinate keeps reducing data. Injected: degrees of freedom never measured.
- **TPC (−DOF):** full model + omission event → REMOVE real DOF, set exactly to 0 → downstream treats 0 as measured → remainder privileged. Injected: a measurement (zero) never made.
- **Shared:** both privilege a coordinate by injecting information not in the data; both are closure-failures of the archive.
- **Mirror table:**
  | PPC | TPC |
  |---|---|
  | adds unobservable DOF | zeroes unmeasured coefficients |
  | pipeline intact | pipeline privileged (same pipeline, opposite direction) |
  | majority-lost coordinate | majority-kept remainder |
  | falsifiability blocked by unobservability | falsifiability blocked by zero-certainty |
- **Dual test** (`dual_direction()`): omission kinds in {regularization, truncation, rounding, dropping, thresholding, discretization, bucketing, imputation} → `−DOF` (TPC); {phantom_dof, patch} → `+DOF` (PPC); physical law → `NONE`. G4 kills `+DOF` instances: phantom-addition is PPC, not TPC.
- **Worked dual pair (conceptual, not a proof):** LASSO-zeroing reported as "X has no effect" (TPC) is dual to adding a phantom confounder that absorbs X's signal while keeping X in the model (PPC). Same privilege, opposite direction. *Marked as framing device, not mathematical theorem.*

## 3. Instance sourcing discipline

- 20 real instances + 3 controls. Every real instance cites author-year-venue only (no DOIs/page numbers asserted).
- Citations used: Tibshirani 1996 JRSS-B; Lee, Sun, Sun & Taylor 2016 Ann. Appl. Stat.; Simmons, Nelson & Simonsohn 2011 Psych. Sci.; Harrell 2015 Springer; Altman & Bland 1995 BMJ; Price et al. 2006 Nature Genetics; Choi, Mak & O'Reilly 2020 Nature Protocols; Royston, Altman & Sauerbrei 2006 Stat. Med.; Little & Rubin 2019 Wiley; Borenstein et al. 2009 Wiley; Rosenthal 1979 Psych. Bull.; Burgess 2007 Ann. Rev. Nucl. Part. Sci.; Baker et al. 2016 Geosci. Model Dev.; Deerwester et al. 1990 JASIS; Prechelt 1998 Neural Networks; Sjöberg & Ljung 1995; Codiga 2011 URI/GSO Tech Report (UTide); Górski et al. 2005 ApJ; Usman et al. 2016 CQG; BIS Basel III framework; Gelman 2005 Ann. Statist.; Leamer 1983 AER; ECMWF IFS documentation.
- Where the cited source establishes the *practice* but the *TPC reading* (treated-as-measured-zero) is the session's framing, the instance note says INFERENCE. 8 of 20 carry an INFERENCE flag.
- **Not verified today:** exact volume/page numbers (deliberately not asserted); whether Codiga 2011's UTide report is the best citation for constituent-dropping (it documents the fitted-set machinery; the error-budget reading is inference).
- **Contracted claims:** HEALPix kept as the gate floor (weakest real instance, 44.90) rather than cut — it shows where the class thins. Absence-of-evidence kept with a boundary-case note (omission by underpowered design, G1 weak).

## 4. Gate design and adversarial checks

- G1–G3 are the TPC core (omission by truncation-family op; treated as measured-zero; conclusions affected). G4 is the dual-direction kill. G5 is archive subtraction (20 classes). G6 requires the duality mirror (remainder privileged *because* omitted was zeroed; duality_clarity ≥ 0.5).
- Controls: symmetry-forbidden zero → PENALIZED with G1/G2/G3 failed (flows through gates naturally, demonstrating G1 excludes zero-by-physical-law); PPC dark dimension → KILLED via G4 (dual-direction test works); UCC Katuš → ZEROED (archive control).
- Result: 20 STRUCTURAL_GAP / 1 PENALIZED / 1 KILLED / 1 ZEROED. Primary: PRS_THRESHOLD_ZERO (72.10). Co-primary: LASSO_ZERO_NO_EFFECT (69.25).
- **Adversarial self-check:** is TPC just "post-selection inference as a class"? Partially — the statistical literature owns the *instances* (novelty cap 0.45 reflects this). The class claims the cross-realm named move + duality formalization + archive-subtraction machinery. Whether that delta is inventive is for counsel; the disclosure says so.

## 5. Iterates shipped

1. `zero_privilege_index(n_omitted, n_retained, claim_certainty)` — heuristic certainty-share carried by zeros.
2. `regularization_zero_crossing(coef_path)` — finds the penalty where a coefficient first hits exactly zero on a regularization path.
3. `tail_energy_gap(tail_energy, admitted_uncertainty)` — for series truncation: unadmitted privilege = tail energy − admitted uncertainty.

## 6. Honest weaknesses (carried into the disclosure)

- Alice §101 risk severe: classification heuristics over textbook statistics with hand-set weights.
- Novelty self-capped at 0.45; instances are textbook; external prior-art search (philosophy of science on idealization, statistics of model selection) not done.
- Scores are heuristics; weights (e.g., 0.30 uniqueness) are author judgments.
- The seed's "Author: Haley Bird" vs the sibling repos' "Haley Bird / autonomous Grok research agent" credit lines: inventorship reconstruction needed claim-by-claim; this buildout was agent-executed under Haley's autopilot grant (2026-09-25).
- No new data, no experiments; outputs are ranked lists and iterate specs.

## 7. Files

- `tpc_engine.py` — gates, dual-direction test, 3 iterates, runner
- `tpc_catalog.py` — 23 instances (20 real + 3 controls)
- `tpc_engine_output.json` / `.txt` — run outputs
- `truncated-privilege-class-2026-09-20.md` — invention disclosure (also copied to `~/workspace/ip/disclosures/` and `~/workspace/your_files/ip-protection/`)
