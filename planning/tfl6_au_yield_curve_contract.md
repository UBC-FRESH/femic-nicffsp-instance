# TFL 6 AU and Yield-Curve Assignment Contract

## Purpose

This note defines the Phase 3 contract for TFL 6 analysis units (AUs), yield
curve assignment, TIPSY parameter extraction, and treatment/operability
eligibility boundaries. It is a planning/design surface only: it does not build
the model-input bundle, ForestModel XML, Matrix Builder outputs, or Patchworks
runtime package.

## Source Evidence

- K3Z teaching baseline: uses BEC subzone grouping, ordered top-two species
  combinations, `top_area_coverage = 0.90`, and L/M/H SI classes to build
  stable AU/curve IDs.
- FEMIC parent issue `UBC-FRESH/femic#187`: promoted MKRF's
  `smoothed_bin_pchip` AU-level first-growth method into the official shared
  default for AU-level first-growth / unmanaged VDYP synthesis.
- FEMIC parent issue `UBC-FRESH/femic#188`: adopted the shared default on the
  TSA29 instance, locking a `54`-row TSA29 smoothed curve library with no
  `insufficient_source_stands` rows in the accepted selection summary.
- FEMIC parent issue `UBC-FRESH/femic#177`: recorded the MKRF curve-quality
  gate that led to the promoted method, including AU-local first-growth
  publication, explicit insufficient-support handling, and rejection of hidden
  whole-curve borrowing in the canonical bundle.
- MKRF yield-curve lane: adds a selected canonical AU set, explicit
  raw-to-canonical AU aggregation, runtime AU remapping, managed-only runtime
  policy for unsupported first-growth AUs, and first-growth support
  diagnostics.
- TFL 6 MP10 information package section 7.2 defines legacy AUs from ecosite
  group, age class, leading species or regeneration method, and silviculture
  treatment.
- TFL 6 MP10 Tables 27, 28, and 29 provide BatchTIPSY parameter evidence for
  existing managed stands aged 11-50, existing managed stands aged 1-10, and
  future managed stands.

The TFL 6 implementation should use K3Z/MKRF/TSA29 FEMIC mechanics for the new
model contract and use the 2011 TFL 6 AU tables as parameter evidence, not as
the canonical Patchworks AU identity scheme. For first-growth smoothing,
`UBC-FRESH/femic#187` is the governing default-method decision; MKRF is the
evidence basis and TSA29 is the downstream adoption example.

## AU Identity

Canonical TFL 6 AUs should be static stand-family identifiers. They must not
encode time-dynamic or scenario-dynamic attributes.

Accepted AU identity dimensions:

- BEC/subzone grouping, following the current TFL 6 run-profile/K3Z profile.
- Ordered top-two leading species combination.
- `top_area_coverage = 0.90` for selecting the main stratum set.
- L/M/H SI class after accepted VDYP/SiteProd field review.

Rejected AU identity dimensions:

- stand age at time 0;
- MP10 age-band class;
- THLB status;
- managed/unmanaged treatment eligibility;
- natural/treated curve provenance;
- operability, yarding class, or slope-proxy class;
- retention status;
- cedar-cultural, cedar-product, or cedar-treatment signals; and
- expansion-candidate status.

Those rejected fields remain valid stand attributes or scenario filters. They
are intentionally outside AU identity so that age updates, treatment choices,
operability sensitivities, and expansion scenarios can change without
redefining the AU universe.

## Legacy MP10 AU Treatment

The 2011 MP10 AU code system is not the canonical FEMIC/Patchworks AU identity
for this instance.

Reason:

- MP10 encodes age class in the AU code for existing stands.
- Patchworks age is time-dynamic, while AU assignment is effectively a static
  stand-family identifier in the model-input bundle.
- Carrying MP10 age-at-time-0 AU splits into the canonical AU key would make
  stand identity depend on a state variable that changes through the run.

Accepted use:

- Preserve MP10 AU codes as provenance and TIPSY parameter keys.
- Scrape Tables 27, 28, and 29 into a structured parameter library.
- Crosswalk new static TFL 6 AUs to the best available MP10 TIPSY parameter row
  using ecology/productivity/species/regeneration-method/treatment similarity.
- Record a confidence flag and fallback reason for every crosswalked row.

## Curve Lanes

Natural/untreated lane:

- Use accepted TFL 6 VDYP outputs.
- Use the shared FEMIC `smoothed_bin_pchip` first-growth curve family as the
  default, governed by `UBC-FRESH/femic#187`.
- Carry the accepted selector contract forward unless TFL 6 diagnostics justify
  an explicit reviewed override: minimum trusted source-bin age `60`, maximum
  trusted source-bin age `300`, seven-point / four-pass smoothing, local
  early-window left-bin censoring, and legacy exponential toe splice blended
  into the smoothed PCHIP body.
- Carry curve-selection diagnostics, sparse-bin/support diagnostics, and fit
  figures forward into Phase 4 QA.
- If a static AU lacks enough source support, prefer explicit audit/fallback
  handling over silent curve fabrication.

Treated/managed lane:

- Generate BatchTIPSY curves from a reviewed TFL 6 parameter crosswalk.
- Use MP10 Tables 27, 28, and 29 as the initial parameter source library.
- Preserve TIPSY input dimensions: SPH, species percentages, species-specific
  SI, genetic worth, regeneration delay, OAF/utilization assumptions,
  fertilization/treatment notes, and THLB-area evidence.
- Assign treated curves by stand origin/treatment state and AU family, not by
  MP10 age-band AU identity.

Bundle semantics:

- `au_table.csv` must keep separate `untreated_curve_id` / `treated_curve_id`
  and `unmanaged_curve_id` / `managed_curve_id` fields.
- `managed` and `unmanaged` remain treatment-eligibility semantics.
- `natural` and `treated` remain curve-provenance semantics.
- Retention, operability, and cedar/expansion signals may change treatment
  eligibility, products, accounts, or scenario membership, but not AU identity.

## TIPSY Parameter Extraction and Crosswalk

The MP10 TIPSY parameter scrape should produce one reviewed structured table
with at least:

- `source_table`: `mp10_table_27`, `mp10_table_28`, or `mp10_table_29`;
- `legacy_au_code`;
- `legacy_age_band_context`;
- `legacy_ecosite_group`;
- `legacy_species_or_regen_method`;
- `legacy_treatment_code`;
- `initial_sph` and `spaced_sph` where available;
- species percentages for Ba, Cw, Cy, Fd, Hw, Ss, and Other;
- species-specific SI values;
- genetic worth values where available;
- regeneration-delay/OAF/utilization assumptions;
- fertilization and natural-regeneration notes; and
- MP10 THLB-area evidence.

The crosswalk from new static AUs to MP10 parameter rows should record:

- static TFL 6 AU ID and stratum code;
- matched MP10 row;
- match basis;
- confidence class;
- fallback reason where no strong match exists; and
- whether the row is intended for existing managed, future planted, future
  natural, fertilized, or other managed-curve use.

## Treatment and Operability Interaction

Operability is a stand-level eligibility/scenario attribute, not an AU key.

The first model-input bundle should carry enough fields to support:

- base THLB inclusion/exclusion;
- managed/unmanaged treatment eligibility;
- operability or yarding/slope-proxy class;
- cedar-cultural and cedar-product signals;
- stand-level retention assignment;
- expansion-candidate membership; and
- origin/provenance assignment for natural versus treated curve lanes.

This keeps operability sensitivity work teachable. Students can vary slope,
yarding, or operability thresholds and move stands in/out of the managed THLB
set without rebuilding static AU identities.

## Downstream Artifacts

Phase 4 should not start until the following contract surfaces are ready:

- static AU definition and selected stratum universe;
- stand-to-AU assignment table with raw and canonical AU fields;
- stand origin/provenance assignment table;
- MP10 TIPSY parameter library;
- TFL6 AU to MP10 parameter crosswalk;
- VDYP curve-selection and support diagnostics;
- TIPSY/VDYP overlay diagnostics;
- missing AU/curve mapping report; and
- species-share consistency report for natural and treated lanes.

MKRF's selected-AU/remap audit pattern is a useful reference if TFL 6 has many
small source strata. The first TFL 6 design preference is to keep the static AU
universe interpretable; if the full source universe is too fragmented, use an
audited raw-to-canonical aggregation or selected-AU remap rather than allowing
unreviewed one-off curve families to proliferate. If first-growth support is
weak for some canonical AUs, follow the parent `#187` / MKRF `#177` governance
pattern: make unsupported rows explicit and reviewed rather than hiding them
behind untracked borrowed or synthetic curves.

## Acceptance Checks for Implementation

- Changing stand age must not change canonical AU identity.
- Changing operability or THLB scenario assumptions must not change canonical
  AU identity.
- Every published AU must have an untreated curve or an explicit missing-curve
  rationale.
- Every managed/treated curve must trace to a reviewed TIPSY parameter row or a
  reviewed fallback.
- Sparse VDYP support and TIPSY crosswalk fallbacks must be visible in tracked
  diagnostics before Patchworks runtime-package QA starts.

## P3.3b Accepted Contract Lock

This section records the reviewed P3.3b lock. It closes the AU/yield contract
design lane and hands implementation to P3.4 without building model inputs in
this slice.

Accepted static AU identity:

- BEC/subzone grouping.
- Ordered top-two leading species combination.
- `top_area_coverage = 0.90`.
- L/M/H SI class after accepted VDYP/SiteProd field review.

Rejected canonical AU identity fields:

- stand age at time 0 or MP10 age-band class;
- THLB status, operability, yarding, slope-proxy class, or treatment
  eligibility;
- natural/treated curve provenance;
- managed/unmanaged treatment eligibility;
- retention, cedar, cultural cedar, product-quality, or treatment-signal
  fields; and
- K3Z/NICF core, expansion-candidate, rejected-candidate, or TFL 6 remainder
  identity.

Accepted MP10 TIPSY boundary:

- MP10 Tables 27, 28, and 29 are accepted as the initial TFL 6 TIPSY parameter
  evidence library.
- Legacy MP10 AU codes are preserved as provenance and parameter keys only.
- MP10 age-at-time-0 AU splits are rejected as canonical Patchworks AU
  identity.
- P3.4 must scrape the tables into a structured parameter library before
  generating treated/managed BatchTIPSY curves.

Accepted curve-lane boundary:

- Natural/untreated curves use accepted TFL 6 VDYP outputs and the shared
  FEMIC `smoothed_bin_pchip` first-growth selector by default.
- Parent FEMIC issue `UBC-FRESH/femic#187` is the governing shared/default
  smoothing-method decision. MKRF issue `UBC-FRESH/femic#177` is the evidence
  basis and TSA29 issue `UBC-FRESH/femic#188` is the adoption example.
- Treated/managed curves use BatchTIPSY curves generated from the reviewed
  TFL 6 TIPSY parameter crosswalk.
- Unsupported or sparse curve families must be visible in tracked diagnostics;
  silent curve borrowing or hidden fabrication is rejected.

Accepted eligibility interaction:

- Operability is a stand-level eligibility and scenario attribute, not an AU
  key.
- Managed/unmanaged treatment eligibility is separate from natural/treated
  curve provenance.
- Retention, cedar signals, expansion status, and stakeholder/KPI reporting
  fields are stand/group/scenario attributes. They may affect treatment
  eligibility, products, accounts, reports, or scenario membership, but not AU
  identity.

P3.4 implementation handoff:

- scrape MP10 Tables 27-29 into a reviewed parameter library;
- construct the static TFL 6 AU universe and stand-to-AU assignment surface;
- generate and QA natural/untreated VDYP curves using the accepted smoothing
  default;
- generate and QA treated/managed BatchTIPSY curves from the reviewed
  parameter crosswalk; and
- emit curve-selection, sparse-support, missing-mapping, fallback-row,
  TIPSY/VDYP overlay, and species-share diagnostics before Phase 4 starts.
