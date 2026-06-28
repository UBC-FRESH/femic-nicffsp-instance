# TFL 6 MP11 Public DEM Steep-Slope Execution Plan

## Purpose

Phase 9D repairs an avoidable P9RF THLB gap: MP11 Table 12 Step 220
`Terrain Stability - LiDAR 90% + Slope` is currently carried as a
zero-deduction placeholder even though a public DEM source has already been
identified. This plan defines a bounded public DEM steep-slope proxy workflow
that can be executed before the P9RF THLB surface is treated as promotion-ready
for model-input work.

The intent is not to reproduce WFP's private LiDAR/DTSM/Patchworks analysis.
The intent is to test the best currently available public DEM route, quantify
what it can explain, and either lock a defensible public proxy for Step 220 or
record a precise blocker.

## Source Boundary

Immediate public DEM source:

- Source name: `Digital Elevation Model for British Columbia - CDED - 1:250,000`
- Existing FEMIC resolver alias: `digital elevation model` / `DEM`
- Existing FEMIC direct-root note: `https://pub.data.gov.bc.ca/datasets/175624/`
- Status: public coarse fallback and raster-pipeline smoke-test source
- Expected role: prove materialization, clipping, slope derivation, and
  zonal-stat mechanics; assess whether a coarse DEM proxy is useful enough for
  Step 220 review.

Future high-resolution source:

- Source family: LidarBC / open LiDAR
- Status: preferred future high-resolution route, not yet materialized
- Expected role: parent FEMIC Phase 79 will add reusable open LiDAR discovery,
  tile materialization, DTM/DEM, slope, and terrain-derived hydrography
  workflows.

Rejected immediate shortcuts:

- No private WFP LiDAR, DTSM, terrain, LBB, ITI, or LEFI data.
- No benchmark-only tuning without terrain/slope evidence.
- No use of RESULTS opening slope/aspect/elevation as a continuous DEM
  substitute.
- No claim that CDED 1:250,000 is stand-level LiDAR equivalence.

## Artifact Layout

Generated or large raster artifacts stay out of normal source tracking unless
explicitly promoted.

- DEM downloads:
  `runtime/dem/p9d_public_dem/source/`
- DEM clip/mosaic:
  `runtime/dem/p9d_public_dem/processed/tfl6_cded_dem.tif`
- Percent-slope raster:
  `runtime/dem/p9d_public_dem/processed/tfl6_cded_slope_pct.tif`
- Raster QA summaries:
  `planning/tfl6_mp11_p9d_public_dem_source_manifest.{md,csv,json}`
- Zonal/stat summaries:
  `planning/tfl6_mp11_p9d_public_dem_slope_zonal_stats.{md,csv,json}`
- Step 220 scenario summaries:
  `planning/tfl6_mp11_p9d_step220_dem_slope_scenarios.{md,csv,json}`
- If accepted into P9RF:
  refreshed `planning/tfl6_mp11_p9rf_table12_step_220.*` through
  `planning/tfl6_mp11_p9rf_table12_step_310.*`.

## Implementation Sequence

### P9D.2 DEM Materialization

1. Resolve the CDED package through FEMIC's BCDC resolver.
2. Identify required DEM archives or tiles for the TFL 6 AOI.
3. Download archives under `runtime/dem/p9d_public_dem/source/`.
4. Record URL, archive names, sizes, checksums, licence, and command
   provenance.
5. Build an AOI DEM clip or mosaic in EPSG:3005 where feasible.
6. Emit DEM QA summaries covering CRS, resolution, extent, nodata, coverage,
   and obvious voids.

### P9D.3 Slope Raster And Zonal Statistics

1. Derive percent slope from the DEM clip/mosaic.
2. Clip/mask the slope raster to TFL 6 and the relevant P9RF active surface.
3. Compute zonal statistics for current Step 210/220 candidate fragments.
4. Include at minimum:
   - median slope percent;
   - mean slope percent;
   - maximum slope percent;
   - proportion of valid pixels above candidate thresholds;
   - valid-pixel and nodata counts;
   - area represented by valid pixels.
5. Emit QA summaries and record coarse-resolution limitations.

### P9D.4 Step 220 Scenario Comparison

Candidate rules should test both slope threshold and within-fragment steep-area
proportion. Initial scenario grid:

- slope thresholds: `60%`, `70%`, `80%`, `90%`
- minimum steep-pixel proportions: `25%`, `50%`, `75%`, `90%`
- optional whole-fragment versus partial-area accounting diagnostics

Each scenario must report:

- Step 220 deduction area;
- delta to MP11 Step 220 target `1,820 ha`;
- retained area after Step 220;
- propagated Current THLB and Long-term Land Base deltas if applied;
- valid/nodata coverage diagnostics;
- caveat text about CDED resolution and non-equivalence to LiDAR.

### P9D.5 Lock Or Defer

A Step 220 public DEM proxy can be locked only if:

- source coverage is sufficient for the TFL 6 AOI;
- raster and zonal-stat QA pass;
- the selected rule has an interpretable terrain rationale;
- the selected rule is not merely a benchmark-fit artifact;
- area balance remains valid in the P9RF resultant-fragment rebuild; and
- the report clearly states CDED/public DEM limitations.

If these conditions fail, Step 220 remains deferred, but the deferral must
state exactly whether the blocker is source coverage, resolution, nodata,
workflow implementation, or proxy semantics.

## Validation Commands

Expected command families, subject to exact script names in P9D.2-P9D.4:

```bash
python scripts/run_p9d_public_dem_materialization.py
python scripts/run_p9d_public_dem_slope_zonal.py
python scripts/run_p9d_step220_dem_slope_scenarios.py
python scripts/run_p9rf_mp11_table12_resultant_rebuild.py
python -m ruff check scripts/run_p9d_*.py scripts/run_p9rf_mp11_table12_resultant_rebuild.py
```

Raster validation must include explicit readback of generated GeoTIFF metadata.
P9RF validation must include JSON/Markdown consistency checks for Steps 220,
280, 290, and 310.

## Promotion Boundary

Phase 11 model-input/XML work must not treat the current P9RF THLB surface as
final until Phase 9D closes with one of:

- `locked_p9rf_step220_public_dem_steep_slope_proxy`; or
- `deferred_p9rf_step220_public_dem_proxy_rejected_with_evidence`.

The second status is acceptable only if the execution evidence makes clear why
the public DEM route is unsuitable.

## Parent FEMIC Package Handoff

Parent FEMIC Phase 79 is the long-term package solution. It should provide:

- open LiDAR tile discovery and materialization;
- DTM/DEM and slope product pipelines;
- terrain-derived stream evidence workflows;
- optional dependency isolation;
- reusable APIs and CLI commands for future instances.

The TFL 6 Phase 9D work should remain a bounded public DEM repair lane and feed
lessons learned into FEMIC Phase 79 rather than becoming permanent duplicated
package functionality.

## Execution Evidence

P9D.2-P9D.4 produced a usable public DEM evidence lane:

- Materialized `44` CDED archives from the public root
  `https://pub.data.gov.bc.ca/datasets/175624/` for letterblocks `092L` and
  `102I`.
- Verified `44` remote MD5 checksums and `44` readable extracted DEM files.
- Built `runtime/dem/p9d_public_dem/processed/tfl6_cded_dem.tif`, clipped to
  the TFL 6 boundary in `EPSG:3005`.
- Built `runtime/dem/p9d_public_dem/processed/tfl6_cded_slope_pct.tif`.
- Computed zonal statistics for `43,530` P9RF Step 210 active fragments.
- Found valid DEM pixels for `39,239` fragments covering `129,142.501 ha`;
  the remaining `67.602 ha` has no valid DEM pixels in this public CDED
  mosaic.

The current recommended whole-fragment Step 220 review candidate is:

- scenario: `slope_ge_70_prop_ge_0.75_whole_fragment`;
- rule: deduct Step 210 resultant fragments where at least `75%` of valid CDED
  pixels are `>=70%` slope;
- deduction: `1,801.705 ha`;
- MP11 Step 220 benchmark: `1,820.000 ha`;
- delta: `-18.295 ha` (`-1.005%`).

Rationale for review: CDED is coarser and smoother than LiDAR, so a lower
public-DEM slope threshold can be semantically defensible as a public proxy for
LiDAR-derived `90%+` slope terrain. The rule should still be recorded as a
public CDED proxy, not as WFP LiDAR equivalence.

Generated evidence:

- `planning/tfl6_mp11_p9d_public_dem_source_manifest.{md,csv,json}`
- `planning/tfl6_mp11_p9d_public_dem_slope_zonal_stats.{md,csv,json}`
- `planning/tfl6_mp11_p9d_step220_dem_slope_scenarios.{md,csv,json}`

## Closeout Result

The recommended public CDED proxy was accepted and locked into the P9RF Table
12 rebuild.

Accepted rule:

- Step: `mp11_t12_220`
- Status: `locked_p9rf_step220_public_cded_steep_slope_proxy`
- Rule: deduct Step 210 resultant fragments where at least `75%` of valid
  CDED pixels are `>=70%` slope.
- Deducted area: `1,801.705 ha`
- MP11 Step 220 benchmark: `1,820.000 ha`
- Delta: `-18.295 ha` (`-1.005%`)

Full P9RF rerun endpoint after locking Step 220:

- Step 290 Current THLB: `122,764.836 ha`
- MP11 Step 290 benchmark: `120,099.000 ha`
- Step 290 delta: `+2,665.836 ha` (`+2.2197%`)
- Step 310 Long-term Land Base: `121,338.039 ha`
- MP11 Step 310 benchmark: `118,672.000 ha`
- Step 310 delta: `+2,666.039 ha` (`+2.2466%`)

Interpretation: the public DEM repair materially improved the final endpoint
delta while preserving an explicit non-equivalence caveat relative to WFP
LiDAR. Remaining residual is dominated by still-unavailable public-source rows,
especially terrain-stability Class 5, karst, big-tree reserves, and sensitive
cultural/TUS features.
