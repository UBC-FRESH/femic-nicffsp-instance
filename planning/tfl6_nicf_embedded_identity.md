# TFL 6 Embedded NICF/K3Z Identity Contract

## Purpose

The TFL 6 teaching model must embed the original NICF/K3Z teaching area inside
the larger TFL 6 model while preserving distinct identities for:

- the broader TFL 6 model area;
- the K3Z/NICF core teaching AOI; and
- expansion candidate areas considered for NICF-style teaching scenarios.

This is a Phase 3 design contract for P3.2 / `#9`. It does not build geometry,
model-input tables, ForestModel XML, Matrix Builder outputs, or Patchworks
runtime files.

Related stakeholder framing is recorded in
`planning/tfl6_stakeholder_context.md`. The embedded identity contract should
support NICF-facing community/expansion reporting and WFP-facing
fibre-supply/value/cost comparison in the same runtime.

## Design Principle

NICF/K3Z and expansion identity must be represented as stand-level or
block-level grouping attributes, not as AU identity.

Reason:

- AUs define yield-curve families and should remain focused on stable
  ecological/species/SI strata.
- NICF/K3Z membership and expansion-candidate membership are planning/reporting
  identities and scenario groupings.
- Patchworks needs these identities for group accounts, matching targets, and
  reports, but they should not force duplicate AU families or duplicate yield
  curves.

## Required Identity Classes

The first reviewed contract should define at least these mutually auditable
classes:

| Identity | Meaning | Expected use |
| --- | --- | --- |
| `tfl6_base` | Area inside the accepted TFL 6 AOI but outside the embedded NICF/K3Z core and outside active expansion-candidate classes. | Whole-TFL accounting, comparison reports, broader teaching context. |
| `nicf_k3z_core` | Original K3Z/NICF teaching AOI embedded inside the TFL 6 model. | Separate area/yield/account reporting, matching targets, continuity with the K3Z teaching instance. |
| `nicf_expansion_candidate` | Area outside `nicf_k3z_core` that is eligible for candidate expansion scenarios. | Scenario toggles, candidate pool accounting, AAC-uplift comparisons, matching targets. |
| `nicf_expansion_rejected` | Area considered but screened out by productivity, THLB, operability, constraint, or review criteria. | Audit trail, teaching comparison, rejected-pool reporting. |

The implementation can use a more compact coded field, but it must preserve
these distinctions in auditable form.

## Candidate Stand Attributes

Phase 4 model-input generation should receive explicit fields such as:

- `embedded_area_class`;
- `embedded_area_id`;
- `is_nicf_k3z_core`;
- `is_nicf_expansion_candidate`;
- `is_nicf_expansion_rejected`;
- `expansion_candidate_set`;
- `expansion_screen_status`;
- `expansion_screen_reason`;
- `expansion_scenario_group`; and
- optional source geometry/provenance fields for K3Z/NICF and expansion
  overlays.

Exact field names can be finalized in P3.7 / the model-input contract, but the
identity content must be available before P4.1 starts.

## Patchworks-Facing Requirements

The embedded identity contract must support:

- group accounts for the whole TFL 6 area, NICF/K3Z core, expansion candidates,
  rejected candidates, and TFL 6 remainder;
- matching targets that can compare NICF/K3Z core behavior against expansion
  candidate behavior;
- matching targets and reports that compare NICF-preferred expansion outcomes
  against broader TFL 6 and WFP-facing fibre-supply, value, and delivered-cost
  signals where available;
- area/yield/product reports split by embedded area class;
- scenario toggles that add or exclude expansion candidates without altering
  base AU identity;
- AAC-uplift reporting for expansion scenarios; and
- continuity reports that help students compare the former K3Z teaching model
  with the embedded TFL 6 model.

The reporting design should make tradeoffs visible. Expansion candidates that
increase NICF opportunity may still affect WFP fibre supply, fibre value, or
delivered unit cost in the TFL 6 remainder; those effects should be reportable
rather than hidden inside a single whole-model total.

## Dependencies

- P3.3 / `#28` owns AU identity and curve-lane semantics.
- P3.4 / `#29` owns actual yield-curve build and QA.
- P3.5 / `#30` owns treatment options.
- P3.6 / `#31` owns base state-transition logic and should expose hook points
  for embedded-area groups without completing expansion details.
- P3.2 / `#9` owns the embedded NICF/K3Z and expansion-candidate identity
  design.
- P3.7 owns final run-profile/model-input field naming after P3.2 is reviewed.

## Acceptance Checks

- A stand inside the K3Z/NICF core can be identified after clipping to the
  TFL 6 AOI.
- A stand in an expansion-candidate pool can be identified separately from the
  K3Z/NICF core and from the TFL 6 remainder.
- Group-account, matching-target, and report requirements are listed before
  P4.1 starts.
- Embedded identity fields do not change AU assignment or curve family.
- Expansion scenarios can change inclusion/eligibility/reporting without
  redefining AUs.
