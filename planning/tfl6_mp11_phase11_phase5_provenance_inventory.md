# TFL 6 MP11 Phase 11 Phase 5 Provenance Inventory

## Purpose

This P11.1b inventory records the existing Phase 5 model-input, ForestModel
XML, Matrix Builder, runtime, and release provenance surfaces before Phase 11
defines MP11 candidate artifact layout or promotion-readiness checks.

This is a read-only inventory. It does not generate model-input tables,
ForestModel XML, Matrix Builder outputs, Patchworks runtime outputs, or release
artifacts.

Companion structured files:

- `planning/tfl6_mp11_phase11_phase5_provenance_inventory.csv`
- `planning/tfl6_mp11_phase11_phase5_provenance_inventory.json`

## Phase 5 Baseline Boundary

The accepted Phase 5 teaching baseline remains:

- runtime archive: `releases/tfl6_patchworks_runtime_p5_2.zip`
- archive SHA-256:
  `17f56d11faeba89170fc48e202d1bfe83c2dd40b53e7409d8cdb8c1c487c2f9f`
- archive size: `28,000,736` bytes
- runtime manifest: `releases/tfl6_patchworks_runtime_p5_2_manifest.yaml`
- public annex remote: `arbutus-s3`

The release archive contains the accepted Phase 4 runtime ingredients:

- `output/patchworks_tfl6_validated/forestmodel.xml`
- `output/patchworks_tfl6_validated/fragments/fragments.*`
- `models/tfl6_patchworks_model/tracks/*.csv`
- `models/tfl6_patchworks_model/blocks/*`
- `models/tfl6_patchworks_model/analysis/base.pin`
- launch helper scripts, package README, and lineage registry.

The release archive intentionally excludes `data/model_input_bundle/`. The
bundle is rebuild provenance and should inform Phase 11 replacement planning,
but the Phase 5 public user-facing payload is the ready-to-launch runtime
archive.

## Model-Input Bundle Inventory

The Phase 5 model-input bundle lives under `data/model_input_bundle/`.

| Table | Rows | Phase 11 role |
| --- | ---: | --- |
| `stand_table.csv` | `25,019` | replace with MP11 candidate stand table. |
| `au_table.csv` | `407` | replace with MP11 candidate AU/curve-family table. |
| `curve_table.csv` | `507` | replace with MP11 candidate curve metadata. |
| `curve_points_table.csv` | `90,840` | replace with MP11 candidate curve points. |
| `stand_au_assignment.csv` | `25,019` | replace with MP11 AU assignment and provenance. |
| `stand_origin_assignment.csv` | `25,019` | replace or preserve after MP11 source review. |
| `treatment_table.csv` | `4` | replace or supplement with MP11 treatment/rule contract. |
| `transition_table.csv` | `5` | replace or supplement with MP11 transition contract. |
| `harvest_system_table.csv` | `25,019` | replace; Phase 5 rows are all deferred placeholders. |
| `group_table.csv` | `125,095` | replace or supplement with MP11 reporting groups. |
| `cedar_signal_table.csv` | `25,019` | replace or supplement with MP11 cedar/reporting signals. |
| `embedded_identity_table.csv` | `25,019` | preserve or supplement; keeps K3Z/NICF identity. |

Phase 5 bundle area summary:

| Metric | Area |
| --- | ---: |
| AFLB | `191,168.597386 ha` |
| THLB | `139,995.798287 ha` |
| NTHLB | `51,172.799099 ha` |
| area-weighted managed share | `0.732315873` |

Phase 5 warning states that matter for replacement planning:

- fatal missing curve rows: `0`;
- sparse treated-curve fallback rows: `136` / `749.396 ha`;
- harvest-system placeholder rows: `25,019`;
- clearcut eligibility remained blocked by deferred harvest-system assignment
  in the bundle, even though the first XML/runtime accepted a generic `CC`
  treatment lane.

## Export Compatibility Bridge

The Phase 5 generic exporter used an intermediate compatibility bridge:

- `data/model_input_bundle/export_compat/bridge_manifest.json`
- `data/model_input_bundle/export_compat/au_table.csv`
- `data/model_input_bundle/export_compat/curve_table.csv`
- `data/model_input_bundle/export_compat/curve_points_table.csv`
- `data/model_input_bundle/export_compat/id_crosswalk.csv`
- `data/model_input_bundle/export_compat/aflb_current_export_compat.feather`

Bridge counts:

| Surface | Count |
| --- | ---: |
| numeric AU rows | `407` |
| referenced numeric curve rows | `170` |
| curve point rows | `30,579` |
| compatibility AFLB checkpoint rows | `25,019` |
| missing checkpoint AU rows | `0` |
| missing unmanaged curve rows | `0` |
| missing managed curve rows | `0` |

Phase 11 should assume a new MP11 candidate bridge is required if it uses the
same generic exporter path. The Phase 5 bridge must not be silently reused
after MP11 source, AU, curve, or THLB promotion changes.

## ForestModel XML And Fragments

Accepted Phase 5 XML/fragments:

| Surface | Path | Evidence |
| --- | --- | --- |
| ForestModel XML | `output/patchworks_tfl6_validated/forestmodel.xml` | `2,662,799` bytes; SHA-256 `f95a7e29b95a9fcfabdd77036e3ac19611041e704a0aeef6257def190b2ff6a4`. |
| fragments | `output/patchworks_tfl6_validated/fragments/fragments.*` | `24,879` rows; `191,168.566 ha`; SHP SHA-256 `ad9552a5bd34ca0b95c0b9406695a5b3520609fd1c17d7cd303f2207f44dee5f`. |

The accepted export command is recorded in
`models/tfl6_patchworks_model/lineage_registry.yaml` and
`planning/tfl6_forestmodel_xml_export_bridge.md`.

Phase 11 replacement rule: generate any MP11 XML/fragments under an explicit
candidate namespace and do not overwrite the Phase 5 accepted payload before
model-input, XML, Matrix Builder, and runtime QA pass.

## Matrix Builder Tracks

Accepted Matrix Builder run:

- run ID: `tfl6_p43_matrix_accounts_wait20`
- manifest:
  `runtime/logs/patchworks_matrixbuilder_manifest-tfl6_p43_matrix_accounts_wait20.json`
- return code: `0`
- accounts sync: `synced`

Track counts:

| Track | Rows |
| --- | ---: |
| `accounts.csv` | `211` |
| `protoaccounts.csv` | `211` |
| `features.csv` | `86,574` |
| `products.csv` | `26,085` |
| `curves.csv` | `991,672` |
| `blocks.csv` | `47,218` |
| `groups.csv` | `24,879` |
| `strata.csv` | `28,858` |
| `treatments.csv` | `17,390` |

Phase 11 replacement rule: Matrix Builder outputs are downstream of candidate
XML/fragments. They should not be regenerated until model-input/XML readiness
is accepted.

## Runtime Package And Smoke Evidence

Accepted runtime package surfaces:

| Surface | Path | Evidence |
| --- | --- | --- |
| blocks | `models/tfl6_patchworks_model/blocks/blocks.*` | `24,879` rows; `191,168.566 ha`; SHP checksum matches fragments. |
| topology | `models/tfl6_patchworks_model/blocks/topology_blocks_200r.csv` | `170,759` rows. |
| baseline launch | `models/tfl6_patchworks_model/analysis/base.pin` | accepted P4.4b launch surface. |
| lineage | `models/tfl6_patchworks_model/lineage_registry.yaml` | primary Phase 5 runtime provenance registry. |
| direct launch smoke | `runtime/logs/patchworks_headless_manifest-tfl6_p44b_launch0.json` | return code `0`; saved-stage evidence accepted. |
| scenario smoke | `runtime/logs/patchworks_headless_manifest-tfl6_p44d_harvest_smoke200.json` | return code `0`; `801` managed `CC` rows scheduled; nonzero managed `CC` harvested volume. |

Phase 11 replacement rule: runtime package and smoke evidence are Phase 12
work. Phase 11 should only produce a Phase 12 handoff or blocker package after
model-input and XML readiness are resolved.

## Phase 11 Decisions Carried Forward

- Preserve Phase 5 as the accepted teaching baseline until a rebuilt MP11
  runtime passes downstream QA.
- Write MP11 candidate outputs separately from the Phase 5 accepted runtime
  payload.
- Treat `data/model_input_bundle/` as rebuild provenance, not as the public
  Phase 5 release payload.
- Build a new MP11 candidate model-input bundle and export bridge if P11.2
  accepts promotion readiness.
- Defer Matrix Builder, blocks/topology, Patchworks launch, scenario smoke, and
  release archive work to later Phase 11/12 gates.

## Next Step

P11.1c should define the Phase 11 artifact layout and generated-output hygiene
rules using this inventory as the baseline. The layout must make it impossible
to confuse Phase 5 accepted payloads with MP11 candidate rebuild outputs.
