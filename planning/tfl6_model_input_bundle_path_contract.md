# TFL 6 Model-Input Bundle Path Contract

## Purpose

This P4.1b contract defines generated model-input bundle paths and table roles
before any bundle outputs are written. It keeps the existing FEMIC instance
convention of using `data/model_input_bundle/` as the generated bundle root and
records the stable handoff paths that later P4.1c/P4.1d/P4.2 work must use.

Machine-readable companion:
`planning/tfl6_model_input_bundle_path_contract.json`.

Governing issue: `#17`.

This contract does not create `data/model_input_bundle/`, regenerate THLB
geometry, write CSVs, generate ForestModel XML, run Matrix Builder, or assemble
a Patchworks runtime package.

## Bundle Root

Canonical generated bundle root:

- `data/model_input_bundle/`

This follows the K3Z, TSA29, and MKRF instance convention. The directory is
generated-output space. It should stay absent or ignored until P4.1c writes the
first reviewed bundle and Phase 5 decides what is tracked, annexed, published,
or regenerated.

## Input Geometry Handoff

P4.1a found that the generated `data/tsr/*checkpoint*` files referenced by the
Phase 2 THLB status report are not present in the clean checkout. P4.1b defines
stable P4 input locations for the regenerated or rematerialized AFLB resultant
fragment universe and final THLB/NTHLB state geometry:

| Artifact | Path | Role |
| --- | --- | --- |
| Canonical AFLB resultant-fragment universe | `data/model_input_bundle/input_geometry/aflb_current.feather` | P4.1c stand-table source for the forested model universe after accepted spatial netdown/resultant processing. Every row needs an untreated VDYP curve so retained/NTHLB forest can grow. |
| Readable AFLB mirror | `data/model_input_bundle/input_geometry/aflb_current.gpkg` | GeoPackage mirror for GIS QA and maintainer inspection of the model resultant-fragment universe. |
| Final THLB state checkpoint | `data/model_input_bundle/input_geometry/thlb_current.feather` | P4.1c source for managed THLB share, unmanaged/NTHLB retention share, and final THLB area reconciliation on AFLB resultant fragments. It is not a separate stand-table universe. |
| Readable final THLB mirror | `data/model_input_bundle/input_geometry/thlb_current.gpkg` | GeoPackage mirror for GIS QA and maintainer inspection of THLB/NTHLB state on resultant fragments. |
| Checkpoint manifest | `data/model_input_bundle/input_geometry/thlb_checkpoint_manifest.json` | Records source command, source audit, area metrics, checksums, and regeneration/rematerialization status. |

The AFLB Feather checkpoint is the canonical resultant-fragment restart/read
path. The THLB Feather checkpoint is a downstream state surface used to compute
`managed_share`, `thlb_fact`, `thlb_area_ha`, and `retention_share`.
`NTHLB = AFLB - THLB` remains in the model as unmanaged/full-retention forest
and still requires an untreated VDYP growth curve. P4.1c must create or
rematerialize the AFLB surface before it writes stand-level bundle tables.

## Core Generated Tables

P4.1c should write these core tables under `data/model_input_bundle/`:

| Table | Role |
| --- | --- |
| `bundle_manifest.json` | Bundle provenance, run metadata, source paths, row counts, checksums, and accepted caveats. |
| `stand_table.csv` | One row per AFLB resultant fragment with stable keys, area, THLB/NTHLB share, IFM, ORIGIN, AU, curve, treatment, transition, cedar, harvest-system, and embedded-identity fields. |
| `au_table.csv` | Canonical Patchworks-facing AU table: static AU identity, selected top-area status, SI class, curve IDs, and remap family. |
| `curve_table.csv` | Curve metadata for natural/untreated and treated/managed curve IDs. |
| `curve_points_table.csv` | Age-by-curve yield points for Patchworks ForestModel export. |
| `stand_au_assignment.csv` | Stand-to-AU and AU-remap audit table. |
| `stand_origin_assignment.csv` | Stand-level natural/treated ORIGIN and curve-provenance assignment audit. |
| `treatment_table.csv` | Accepted treatment IDs and eligibility gates for base and NICF-gated scenario hooks. |
| `transition_table.csv` | Accepted state-transition rows and source/destination state semantics. |
| `group_table.csv` | Reporting and scenario group membership for TFL 6 base, WFP remainder, K3Z reference, expansion pools, cedar signals, harvest systems, and THLB/IFM classes. |
| `cedar_signal_table.csv` | Cedar-leading, Cw/Yc, cedar-present, old-cedar, unresolved utility-pole, reserve-context, and harvest-candidate signals. |
| `embedded_identity_table.csv` | K3Z/NICF reference, outside-AOI expansion candidate/rejected/unreviewed, and WFP/TFL 6 remainder identity fields. |
| `harvest_system_table.csv` | Ground-based, cable, heli, and operability/slope proxy assignments and reporting classes. |

`au_table.csv`, `curve_table.csv`, and `curve_points_table.csv` keep the
cross-instance FEMIC/Patchworks naming convention. TFL 6 adds explicit
stand/group/cedar/embedded/harvest-system support tables so the first XML and
Matrix Builder lanes can inspect semantics directly instead of burying them in
one opaque table.

## QA Tables

P4.1d should write these QA surfaces:

| Table | Role |
| --- | --- |
| `qa/bundle_qa_summary.json` | Readability, row counts, required fields, and fatal/warn QA results. |
| `qa/area_reconciliation.csv` | Area checks across source input, THLB audit, final bundle, IFM, embedded identity, and reporting groups. |
| `qa/missing_mapping_report.csv` | Missing AU, curve, treatment, transition, harvest-system, cedar, and embedded-identity mappings. |
| `qa/curve_assignment_summary.csv` | Natural/treated curve coverage and AU remap diagnostics. |
| `qa/treatment_eligibility_summary.csv` | IFM, THLB, harvest-system, K3Z/NICF, expansion, and deferred treatment eligibility checks. |
| `qa/cedar_signal_summary.csv` | Cedar signal area/volume checks against P3.1b gross diagnostics and final THLB/IFM filtering. |
| `qa/embedded_identity_summary.csv` | K3Z reference, current-AOI TFL 6, WFP remainder, outside-AOI expansion candidate, rejected, and unreviewed pool checks. |

## Downstream Phase 4 Paths

These paths are reserved for later Phase 4 work and must not be written in
P4.1b:

| Surface | Path |
| --- | --- |
| ForestModel output directory | `output/patchworks_tfl6_validated/` |
| ForestModel XML | `output/patchworks_tfl6_validated/forestmodel.xml` |
| ForestModel fragments | `output/patchworks_tfl6_validated/fragments/` |
| Patchworks model root | `models/tfl6_patchworks_model/` |
| Patchworks blocks | `models/tfl6_patchworks_model/blocks/` |
| Patchworks tracks | `models/tfl6_patchworks_model/tracks/` |
| Patchworks analysis | `models/tfl6_patchworks_model/analysis/` |

P4.2 owns XML/fragments. P4.3 owns Matrix Builder tracks/accounts/products.
P4.4 owns runtime-package QA and launch smoke.

## P4.1c Handoff

P4.1c may start only after it has a concrete plan for creating or
rematerializing `data/model_input_bundle/input_geometry/aflb_current.feather`
as the resultant-fragment universe and
`data/model_input_bundle/input_geometry/thlb_current.feather` as the managed
share state surface. The first bundle build should then write the core generated
tables and stop before ForestModel XML generation unless the maintainer
explicitly broadens the scope.
