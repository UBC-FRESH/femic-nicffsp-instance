# TFL 6 P4.1c THLB Geometry Handoff

## Purpose

This note records the P4.1c handoff from the accepted Phase 2 THLB netdown lane
to the Phase 4 model-input bundle lane. It exists because the regenerated
geometry artifacts under `data/model_input_bundle/` are generated runtime
outputs, while the planning surface needs a tracked audit trail explaining what
was regenerated and how it should be consumed.

Important correction for P4.1c.2: this final THLB geometry is a state surface
for managed-share accounting, not a separate Patchworks stand universe. The
downstream Patchworks model stand universe is the AFLB resultant-fragment
surface produced by the accepted spatial netdown overlays. THLB is a managed
subset of AFLB, and `NTHLB = AFLB - THLB` remains in the model as
unmanaged/full-retention forest. Every AFLB resultant fragment still needs an
untreated VDYP curve so retained forest can grow and report residual inventory
through time.

## Regeneration Command

The final THLB geometry was regenerated from the accepted clipped 2025 TFL 6 R1
VRI input using the reviewed THLB recipe:

```powershell
python -m femic tsr thlb-netdown-run `
  --instance-root external/femic-tfl6-instance `
  --thlb-netdown-recipe-path config/tsr/thlb_netdown.recipe.yaml `
  --checkpoint-path data/input/tfl_6/vri_2025_r1_poly_tfl6.gpkg `
  --output-path data/model_input_bundle/input_geometry/thlb_current.feather `
  --audit-path data/model_input_bundle/input_geometry/thlb_checkpoint_manifest.json `
  --execution-mode reconstructed `
  --parallel-mode serial
```

The GeoPackage mirror was then written from the Feather handoff so downstream
tools that prefer OGR-compatible inputs can inspect the same geometry:

- `data/model_input_bundle/input_geometry/thlb_current.feather`
- `data/model_input_bundle/input_geometry/thlb_current.gpkg`
- `data/model_input_bundle/input_geometry/thlb_checkpoint_manifest.json`

## Direct Inspection

- Generated UTC: `2026-06-26T15:44:37.891352+00:00`
- Source input: `data/input/tfl_6/vri_2025_r1_poly_tfl6.gpkg`
- Recipe: `config/tsr/thlb_netdown.recipe.yaml`
- CRS: `EPSG:3005`
- Rows: `29892`
- Geometry type: `MultiPolygon`
- Feather size: `30963634` bytes
- GeoPackage size: `58990592` bytes
- Manifest size: `53164` bytes
- Total geometry area: `181719.847469 ha`
- Weighted THLB area using `thlb_fact`: `139995.798287 ha`
- Manifest final managed area: `139995.79828729105 ha`

The weighted THLB area is `3508.070 ha` above the scaled current-AOI benchmark
of `136487.728 ha`, a `2.57%` high-side gap. This remains inside the accepted
teaching tolerance and is lower than the earlier invalid-AFLB result. For this
handoff, `thlb_fact` is the authoritative final THLB weighting field. The
positive geometry area alone is not the final THLB area because several
accepted aspatial fallback deductions are represented fractionally.

## Companion Outputs

The THLB runner also wrote companion AFLB and LHLB checkpoint partitions under
`runtime/logs/tsr/lu_partitions/` and reported a corrected AFLB checkpoint area
of `191168.597 ha` in `config/tsr/thlb_reconstructed.status.md`. For P4.1c.2,
the promoted `aflb_current` handoff is the correct resultant-fragment universe.
The THLB checkpoint recorded above should be reconciled against that AFLB
universe to compute managed and retained shares.

If an AFLB or LHLB restart checkpoint is needed as a stable bundle artifact, it
should be regenerated or reconstructed deliberately under
`data/model_input_bundle/input_geometry/` and either added to the accepted
artifact policy or treated as local runtime cache.

## AFLB Resultant-Fragment Handoff

Status: **repaired on 2026-06-26 under `#36`**. The corrected
`aflb_current.*` handoff is the accepted P4.1c.2 stand-universe input for the
next bundle-table pass.

P4.1c.2a reran the THLB recipe from the raw clipped TFL 6 R1 source after
repairing the GLB-to-AFLB non-forest rule, then promoted the corrected AFLB
checkpoint into the canonical generated input-geometry handoff:

- `data/model_input_bundle/input_geometry/aflb_current.feather`
- `data/model_input_bundle/input_geometry/aflb_current.gpkg`
- `data/model_input_bundle/input_geometry/aflb_checkpoint_manifest.json`

The handoff concatenates the 13 LU partition Feather files under
`runtime/logs/tsr/lu_partitions/aflb_checkpoint.6a351f3a223a/`, preserves the
runner-supplied identifiers, and adds:

- `aflb_fragment_id`: stable generated row key for the AFLB resultant-fragment
  universe;
- `lu_partition`: source LU partition name; and
- `aflb_area_ha`: geometry area in hectares.

Direct inspection after the `#36` repair:

- Generated UTC: `2026-06-26T15:45:13.450633+00:00`
- CRS: `EPSG:3005`
- Rows: `25019`
- Geometry type: `MultiPolygon`
- Total AFLB resultant-fragment area: `191168.597386 ha`
- Unique `FEATURE_ID`: `25019`
- Duplicate `FEATURE_ID` rows: `0`
- Empty geometry: `0`
- Null geometry: `0`
- Invalid geometry: `0`
- `bclcs_level_1 in {N, U}` rows: `0`
- `bclcs_level_1 in {N, U}` area: `0.000000 ha`
- Gap against scaled AFLB benchmark `186175.333 ha`: `4993.264 ha`
  high-side, or `2.68%`.

Duplicate source identifiers are expected because the LU-partitioned,
resultant-fragment surface can split one source polygon into multiple
Patchworks fragments. The generated `aflb_fragment_id` is therefore the stable
P4.1c row key for bundle-table construction.

### Repair Finding

The earlier generated handoff was removed after direct inspection showed that
the runner-labeled `aflb_checkpoint.6a351f3a223a` still contained non-treed and
non-forested BCLCS rows. Examples in the invalid checkpoint included:

- `N/L/U` with `for_mgmt_land_base_ind=N`: `2850.573 ha`;
- `N/L/U/EL/ES` with `for_mgmt_land_base_ind=N`: `2382.025 ha`; and
- additional `N/L/U` rows with `for_mgmt_land_base_ind=Y`: `212.358 ha`.

By definition, AFLB must be GLB net of non-treed, non-forested, and
non-productive stands. Therefore the GLB-to-AFLB filter in the reviewed
THLB recipe/runner output is too permissive for this model-building handoff.
The immediate repair is to correct and rerun the GLB-to-AFLB lane before any
bundle CSV generation resumes. The corrected non-forest rule must remove
BCLCS level 1 non-treed/unclassified rows and BCLCS level 2 non-vegetated,
water, or unreported rows, while keeping `for_mgmt_land_base_ind == N` as
QA evidence rather than the base executable rule because it also captures
explicit non-productive rows.

The `#36` repair changed `tfl6_nd_010_non_forest` to apply
`checkpoint_attribute_mode: any` over `bclcs_level_1 in {N, U}` and
`bclcs_level_2 in {N, W}` or null. The corrected AFLB handoff passed the
direct contamination check and is accepted for the next P4.1c.2 bundle-table
slice.

## Scope Boundary

This pass regenerated the corrected AFLB resultant-fragment handoff and the
downstream THLB/NTHLB state handoff. It did not build bundle CSV tables,
ForestModel XML, Matrix Builder outputs, a Patchworks runtime package, or
Phase 5 publication policy work.

The next P4.1c move is to resume P4.1c.2: build core model-input bundle tables
from the corrected AFLB resultant-fragment universe, the corrected THLB/NTHLB
managed-share state surface, and the accepted AU, curve, treatment,
transition, cedar, and embedded-identity contracts.
