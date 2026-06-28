# TFL 6 MP11 Phase 9 Closeout

## Purpose

This note closes Phase 9: MP11 source-layer and THLB rebuild. Phase 9 turned
the accepted Phase 8 public-data source-layer contract into verified source
manifests, public proxy profiles, an ordered overlay scaffold, and a compact
diagnostic THLB rebuild summary.

Phase 9 did not produce an accepted replacement THLB surface. The final P9.5
run is a bounded diagnostic that deliberately avoids force-fitting to the MP11
current THLB target.

## Branch And Issue Tree

- Branch: `feature/p9-mp11-source-layer-thlb-rebuild`
- Pull request: `#78`
- Parent issue: `#66`
- Child issues:
  - P9.1 launch source-layer THLB rebuild execution plan: `#72`;
  - P9.2 materialize and verify public source layers: `#73`;
  - P9.3 profile inventory and proxy inputs: `#74`;
  - P9.4 implement ordered overlay THLB recipe scaffold: `#75`;
  - P9.5 execute and compare public-data THLB rebuild: `#76`;
  - P9.6 close Phase 9 and hand off rebuild outputs: `#77`.

## Tracked Outputs

| Output | Path | Role |
| --- | --- | --- |
| Execution plan | `planning/tfl6_mp11_phase9_execution_plan.md` | Phase 9 branch, issue, artifact, source-dependency, no-force-fit, and promotion-gate plan. |
| Source-layer verifier | `scripts/build_p9_mp11_source_layer_manifest.py` | Generates public source-layer dependency status and read-smoke evidence. |
| Source-layer manifest | `planning/tfl6_mp11_phase9_source_layer_manifest.md` | Public-safe summary of `21` source dependencies with matching CSV/JSON. |
| Input/proxy profiler | `scripts/build_p9_mp11_input_proxy_profile.py` | Profiles inventory, VDYP, road, hydrology, and reserve candidates for later overlay use. |
| Input/proxy profile | `planning/tfl6_mp11_phase9_input_proxy_profile.md` | Public-safe summary of `51` candidate/profile/QA rows with matching CSV/JSON. |
| Ordered overlay recipe | `config/tsr/mp11_thlb_rebuild.recipe.yaml` | Public-data ordered-overlay scaffold and checkpoint sequence. |
| Scaffold verifier | `scripts/build_p9_mp11_ordered_overlay_scaffold.py` | Validates source and candidate references in the ordered-overlay scaffold. |
| Ordered overlay scaffold | `planning/tfl6_mp11_phase9_ordered_overlay_scaffold.md` | Public-safe summary of `13` ordered scaffold rows with matching CSV/JSON. |
| Diagnostic rebuild runner | `scripts/run_p9_mp11_public_thlb_rebuild.py` | Runs the compact public-data THLB diagnostic summary calculation. |
| Diagnostic rebuild summary | `planning/tfl6_mp11_phase9_thlb_rebuild_summary.md` | Public-safe summary of the P9.5 diagnostic rebuild with matching CSV/JSON. |

## Headline Result

The P9.5 diagnostic current THLB is `24,762.768 ha`, compared with the MP11
current THLB comparison target of `120,099.000 ha`.

This is not a valid model-input replacement. The large negative residual is
expected from the intentionally conservative diagnostic design:

- full-stand intersection diagnostics for DRA road buffers and FWA hydrology
  buffers overstate partial road and riparian deductions;
- shoreline and DEM/slope public proxies are not yet materialized;
- WFP LBB, ITI, LEFI, proposed/local reserve, and some LiDAR-derived
  assumptions remain unavailable as public data;
- WTRA and stand-level retention policy deductions remain deferred; and
- no step scales or force-fits the output to MP11 Table values.

The Phase 5 teaching runtime therefore remains the accepted baseline.

## Phase 10 Handoff

Phase 10 can proceed with AU/yield work without treating the Phase 9 diagnostic
THLB as accepted model input. The useful Phase 9 inputs for Phase 10 are:

- the verified public VRI/R1 and VDYP source paths;
- the inventory/profile evidence for candidate AU and productivity fields; and
- the explicit unavailable-dependency list for LEFI/ITI/LiDAR-related MP11
  managed-stand assumptions.

Phase 10 should keep yield and managed-stand parameter work separated from
source-layer promotion decisions.

## Phase 11 Handoff

Phase 11 must not consume the P9.5 diagnostic THLB as an accepted replacement
surface. Before model-input/XML promotion, a later slice must either:

- replace the full-stand intersection diagnostics with reviewed partial-area
  overlay geometry or another accepted area-accounting implementation;
- materialize or formally defer shoreline and DEM/slope public proxies;
- document treatment of unavailable WFP LBB/ITI/LEFI dependencies and local
  reserve assumptions; and
- pass the Phase 8 evidence-promotion gates for any candidate source-layer or
  THLB output.

Until those gates pass, MP11 `120,099 ha` remains a comparison target and the
Phase 5 teaching runtime remains the accepted baseline.

## Validation

Phase 9 closeout validation:

```bash
python scripts/build_p9_mp11_source_layer_manifest.py
python scripts/build_p9_mp11_input_proxy_profile.py
python scripts/build_p9_mp11_ordered_overlay_scaffold.py
python scripts/run_p9_mp11_public_thlb_rebuild.py
python -m ruff check .
sphinx-build -b html docs docs/_build/html -W
```

All commands passed before closeout.

## Private-Data Hygiene

Phase 9 used public source layers, public-safe summaries, and generated
planning outputs only. It did not track private WFP layers, unpublished source
tables, private prompt logs, generated scratch outputs outside accepted paths,
or proprietary model assumptions.
