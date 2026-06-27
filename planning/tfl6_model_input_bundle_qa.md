# TFL 6 Model-Input Bundle QA

## Purpose

This note records the P4.1d lightweight QA pass for the first generated
TFL 6 model-input bundle. It verifies that the ignored generated bundle tables
under `data/model_input_bundle/` are internally readable and coherent enough to
start P4.2 ForestModel/XML generation, with explicit warning gates carried
forward.

Governing issue: `#17`.

This QA pass did not generate ForestModel XML, run Matrix Builder, assemble a
Patchworks runtime package, publish artifacts, or start runtime smoke testing.

## QA Inputs

The QA pass read these generated tables:

- `data/model_input_bundle/stand_table.csv`
- `data/model_input_bundle/au_table.csv`
- `data/model_input_bundle/curve_table.csv`
- `data/model_input_bundle/curve_points_table.csv`
- `data/model_input_bundle/stand_au_assignment.csv`
- `data/model_input_bundle/stand_origin_assignment.csv`
- `data/model_input_bundle/treatment_table.csv`
- `data/model_input_bundle/transition_table.csv`
- `data/model_input_bundle/group_table.csv`
- `data/model_input_bundle/cedar_signal_table.csv`
- `data/model_input_bundle/embedded_identity_table.csv`
- `data/model_input_bundle/harvest_system_table.csv`
- `data/model_input_bundle/bundle_manifest.json`
- `data/model_input_bundle/qa/area_reconciliation.csv`
- `data/model_input_bundle/qa/missing_mapping_report.csv`
- `data/model_input_bundle/qa/bundle_qa_summary.json`
- `data/model_input_bundle/qa/curve_assignment_summary.csv`

## QA Results

| Check | Status | Detail |
| --- | --- | --- |
| Stand rows | Pass | `25019` rows. |
| Manifest record counts | Pass | Manifest stand count matches `stand_table.csv`. |
| Unique stand IDs | Pass | No duplicate `stand_id` values. |
| Managed-share bounds | Pass | `managed_share` ranges from `0.0` to `0.8450613814688143`. |
| Area reconciliation | Pass | `191168.597386 ha` AFLB, `139995.798287 ha` THLB, `51172.799099 ha` NTHLB. |
| Missing AU IDs | Pass | `0` missing `au_id` values. |
| Missing natural curve IDs | Pass | `0` missing `natural_curve_id` values. |
| Missing treated curve IDs | Pass | `0` missing `treated_curve_id` values. |
| Stand curves in curve table | Pass | Every stand-level curve ID exists in `curve_table.csv`. |
| Curve points | Pass | Every curve in `curve_table.csv` has rows in `curve_points_table.csv`. |
| Treatment rows | Pass | `4` treatment rows. |
| Transition rows | Pass | `5` transition rows. |
| Group membership | Pass | `125095` rows, equal to five memberships per stand. |
| Cedar rows | Pass | `25019` rows, matching stand count. |
| Embedded identity rows | Pass | `25019` rows, matching stand count. |
| Harvest-system rows | Pass | `25019` rows, matching stand count. |
| Harvest-system assignment | Warn | All rows are `unassigned_review_required`. |
| Clearcut eligibility | Warn | All rows have `clearcut_and_plant_eligible == False`. |
| Embedded identity | Pass | `embedded_area_class` is non-null in stand and embedded identity tables. |
| Fatal missing curve rows | Pass | `0` fatal missing curve rows. |
| Sparse treated-curve fallback | Warn | `136` rows use warning-only sparse TIPSY fallback. |

## Accepted Warnings

Two warning classes remain intentionally unresolved after P4.1d:

1. **Harvest-system assignment is deferred.** The bundle carries explicit
   `unassigned_review_required` harvest-system placeholders for all stands
   until reviewed ground/cable/heli logic is implemented from the operability
   proxy lane.
2. **Sparse treated-curve fallback remains reviewable.** The bundle maps all
   stands to concrete treated TIPSY curves, but `136` rows / `749.396 ha` use a
   lexicographic sparse-stratum fallback instead of a direct Phase 3
   future-managed curve match.

These warnings do not block P4.2 ForestModel/XML generation if the XML exporter
preserves the warning state and does not silently convert deferred
harvest-system rows into eligible operational treatments. They do block any
claim that the model has accepted ground/cable/heli assignment or final
clearcut-and-plant scheduling eligibility.

## Handoff

P4.1 is complete. P4.2 may start by generating ForestModel XML from the
reviewed bundle tables. P4.2 must preserve the following semantics:

- the Patchworks stand universe is the AFLB resultant-fragment table;
- THLB is the managed share and NTHLB remains unmanaged/full-retention forest;
- every AFLB stand has an untreated VDYP curve so retained/NTHLB forest can
  grow;
- treated TIPSY curve fallback rows are warning-only and auditable; and
- harvest-system placeholders must not be interpreted as accepted operational
  harvest systems or final treatment eligibility.
