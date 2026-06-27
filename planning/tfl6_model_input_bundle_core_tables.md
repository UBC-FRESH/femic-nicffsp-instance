# TFL 6 Model-Input Bundle Core Tables

## Purpose

This note records the P4.1c.2 core bundle-table generation pass for the TFL 6
instance. It is the tracked audit surface for generated files under
`data/model_input_bundle/`, which remain generated/ignored output unless a later
artifact-publication policy decides otherwise.

Governing issue: `#17`.

This pass generated bundle tables only. It did not generate ForestModel XML, run
Matrix Builder, assemble a Patchworks runtime package, publish data, or start
runtime QA.

## Source Handoffs

The bundle tables were generated from the corrected P4.1c.2a geometry handoffs:

| Handoff | Path | Role |
| --- | --- | --- |
| AFLB resultant-fragment universe | `data/model_input_bundle/input_geometry/aflb_current.feather` | Patchworks stand universe. Every AFLB row needs a growth curve, including NTHLB/full-retention forest. |
| THLB state surface | `data/model_input_bundle/input_geometry/thlb_current.feather` | Managed THLB share overlay used to compute `managed_share`, `thlb_area_ha`, and `nthlb_area_ha` on the AFLB universe. |

The THLB state was intersected back to the AFLB resultant-fragment universe so
managed area is expressed as a share of each AFLB stand row. THLB is not treated
as a separate stand universe.

## Generated Tables

The generated bundle root is `data/model_input_bundle/`.

| Table | Rows | Notes |
| --- | ---: | --- |
| `stand_table.csv` | 25,019 | One row per AFLB resultant fragment with area, THLB/NTHLB share, AU, curves, treatment gates, cedar signals, embedded identity, and harvest-system placeholders. |
| `stand_au_assignment.csv` | 25,019 | Stand-to-AU and curve-remap audit surface. |
| `stand_origin_assignment.csv` | 25,019 | Natural-origin baseline assignment surface. |
| `au_table.csv` | 407 | AU audit table for direct Phase 3 assignments plus computed/sparse rows required by the corrected AFLB universe. |
| `curve_table.csv` | 507 | Natural/untreated VDYP and treated/managed TIPSY curve metadata. |
| `curve_points_table.csv` | 90,840 | Age-by-curve yield points. |
| `treatment_table.csv` | 4 | Base and NICF-gated treatment definitions from Phase 3. |
| `transition_table.csv` | 5 | State-transition definitions from Phase 3. |
| `cedar_signal_table.csv` | 25,019 | Cedar reporting and hook fields. |
| `embedded_identity_table.csv` | 25,019 | Current TFL 6, K3Z/NICF reference, and expansion identity fields. |
| `harvest_system_table.csv` | 25,019 | Deferred harvest-system placeholders pending reviewed operability/DEM-slope assignment. |
| `group_table.csv` | 125,095 | Reporting group membership rows. |

## Area Reconciliation

| Metric | Area (ha) | Status |
| --- | ---: | --- |
| AFLB stand universe | 191,168.597386 | Pass |
| THLB managed share | 139,995.798287 | Pass |
| NTHLB/full-retention forest | 51,172.799099 | Pass |
| Area-weighted managed share | 0.732316 | Informational |

The corrected THLB result remains within the accepted teaching tolerance from
P2.5/P4.1c.2a. NTHLB remains in the model as unmanaged/full-retention forest and
therefore still receives untreated VDYP growth curves.

## AU and Curve Mapping

The corrected AFLB handoff contains rows that were not present in the earlier
Phase 3 AU review table. P4.1c.2 used the accepted Phase 3 assignment where
available and computed the same static AU key from AFLB fields for the remaining
rows.

| Mapping family | Rows | Area (ha) | Status |
| --- | ---: | ---: | --- |
| Phase 3 reviewed AU assignment | 16,774 | Not separately materialized | Accepted |
| Computed from corrected AFLB fields | 8,245 | Not separately materialized | Accepted for first bundle QA |
| P4 lexicographic selected-AU fallback | 176 | 1,110.969717 | Warning/review item |
| Treated TIPSY curve fallback | 136 | 749.395971 | Warning/review item |

All rows have non-null natural and treated curve IDs. The generated
`curve_table.csv` includes `77` `future_managed` TIPSY curves, and every
stand row maps to one of them through either the Phase 3 future-curve map or the
P4 lexicographic treated-curve fallback.

The sparse fallback rows are not fatal for this first bundle, but P4.1d should
inspect them before ForestModel/XML generation. They are small-area, sparse
strata where the canonical static AU did not have a direct future-managed TIPSY
curve. The fallback preserves a concrete TIPSY curve assignment instead of
leaving rows unmapped.

## Harvest-System Warning

Harvest-system assignment is deliberately unresolved in this bundle. The
generated table uses `unassigned_review_required` for all `25,019` stand rows
and records `deferred_operability_proxy` as the assignment status.

This means:

- `clearcut_and_plant_candidate` can identify rows that are otherwise plausible
  candidates;
- `clearcut_and_plant_eligible` remains false until ground/cable/heli assignment
  is reviewed; and
- P4.1d/P4.2 must not interpret the first bundle as having accepted operational
  harvest-system classes.

The next bounded task is P4.1d bundle QA. It should validate required fields,
readability, AU/curve mappings, sparse fallbacks, embedded identity, cedar
signals, and the deferred harvest-system warning before ForestModel XML work
starts.
