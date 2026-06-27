# TFL 6 ForestModel XML Export Bridge

## Purpose

This note records the P4.2 exporter-compatible schema bridge, the generated
ForestModel XML/fragments, and the accepted interim generic-clearcut treatment
assumption for the first Phase 4 model package.

Governing issue: `#37`.

## Bridge Generation

The reviewed P4.1 TFL6 bundle remains unchanged under `data/model_input_bundle/`.
For the existing generic FMG Patchworks exporter, P4.2 generated a compatibility
view under ignored output space:

- `data/model_input_bundle/export_compat/au_table.csv`
- `data/model_input_bundle/export_compat/curve_table.csv`
- `data/model_input_bundle/export_compat/curve_points_table.csv`
- `data/model_input_bundle/export_compat/id_crosswalk.csv`
- `data/model_input_bundle/export_compat/aflb_current_export_compat.feather`
- `data/model_input_bundle/export_compat/bridge_manifest.json`

The bridge maps reviewed TFL6 string IDs to deterministic numeric IDs required
by the current exporter:

| Surface | Count |
| --- | ---: |
| Numeric AU rows | 407 |
| Referenced numeric curve rows | 170 |
| Curve point rows | 30,579 |
| Compatibility AFLB checkpoint rows | 25,019 |
| Missing checkpoint AU rows | 0 |
| Missing unmanaged curve rows | 0 |
| Missing managed curve rows | 0 |
| Managed-share range | 0.0 to 0.8450613814688143 |
| Age-zero rows | 157 |

The compatibility checkpoint overwrites `thlb_fact` with the reviewed
`managed_share` from `stand_table.csv` so proportional IFM/retention export uses
the corrected P4.1d THLB/NTHLB state.

## Export Command

The successful structural export command was:

```powershell
python -m femic export patchworks `
  --instance-root . `
  --tsa tfl6 `
  --bundle-dir data\model_input_bundle\export_compat `
  --checkpoint data\model_input_bundle\export_compat\aflb_current_export_compat.feather `
  --output-dir output\patchworks_tfl6_validated `
  --start-year 2026 `
  --horizon-years 300 `
  --ifm-mode proportional
```

Generated ignored outputs:

- `output/patchworks_tfl6_validated/forestmodel.xml`
- `output/patchworks_tfl6_validated/fragments/fragments.shp`
- `output/patchworks_tfl6_validated/fragments/fragments.dbf`
- `output/patchworks_tfl6_validated/fragments/fragments.shx`
- `output/patchworks_tfl6_validated/fragments/fragments.prj`
- `output/patchworks_tfl6_validated/fragments/fragments.cpg`

## Structural Inspection

| Check | Result |
| --- | --- |
| XML root | `ForestModel` |
| XML year / horizon | `2026` / `300` |
| XML curves | 373 |
| XML selects | 2,442 |
| XML inputs / outputs | 1 / 1 |
| CC treatment nodes | 814 |
| Fragment rows | 24,879 |
| Fragment area | 191,168.566447 ha |
| Fragment IFM counts | 22,403 managed; 2,476 unmanaged |
| Fragment RETENTION range | 0.0 to 0.999924322418445 |
| Fragment AU count | 407 |
| Fragment age-zero rows | 155 |

The fragment row count is lower than the compatibility checkpoint row count
because the exporter drops zero/subprecision positive-area fragments. The area
gap is `0.030939 ha`, which is negligible for the current P4.2 structural
export check.

## Treatment Semantics Decision

The XML emits `814` generic `CC` treatment nodes. This is accepted for the
first Phase 4 ForestModel package. Ground/cable/heli harvest-system assignment
remains explicitly deferred because the stand-inventory and DEM-derived
operability signal has not yet been reviewed, but that deferral should not block
the generic clearcut-and-plant treatment lane.

The intended interpretation is:

- `CC` is a generic Phase 4 base treatment, not a final harvest-system class;
- harvest-system splitting into ground, cable, and heli remains a later
  operability/cost/reporting refinement;
- deferred harvest-system fields in the model-input bundle remain useful QA and
  metadata, but they are not treatment blockers for this first XML package; and
- Matrix Builder may proceed from this XML/fragments pair.

P4.2 is complete. Runtime packaging and publication remain downstream, but the
next executable Phase 4 lane is P4.3 Matrix Builder and track/account QA.
