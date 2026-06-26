# TFL 6 ForestModel XML Export Bridge

## Purpose

This note records the P4.2 exporter-compatible schema bridge and the second
semantic blocker found after ForestModel XML/fragments generation succeeded.

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

## Semantic Blocker

The XML currently emits `814` `CC` treatment nodes even though P4.1d accepted
that final clearcut-and-plant eligibility remains blocked until reviewed
ground/cable/heli harvest-system assignment exists. The generated XML does not
include `unassigned_review_required` or `clearcut_blocker` conditions in select
statements.

This means the compatibility bridge solves the numeric-schema blocker, but P4.2
is not yet semantically ready for Matrix Builder. The next repair must ensure
the ForestModel exporter preserves the P4.1d warning state and does not
silently convert deferred harvest-system rows into accepted operational
treatment eligibility.

Possible bounded repairs:

1. add an exporter option/config hook that disables base CC treatment emission
   for this first TFL6 XML until harvest-system eligibility is reviewed; or
2. extend the exporter to include a treatment-eligibility field in fragments and
   constrain managed treatment selects to eligible rows.

P4.2 remains open. Matrix Builder, runtime packaging, publication, and runtime
smoke remain blocked.
