# TFL 6 MP11 Public Source-Layer And THLB Rebuild Contract

## Purpose

This P8.2 contract translates reviewed MP11 land-base and netdown evidence into
a public-data strategy for a later source-layer and THLB rebuild. It defines
which MP11 land-base categories can be pursued from public spatial sources,
which require public proxies or sensitivity lanes, which are unavailable
because required WFP/LiDAR/LBB assumptions are not public, and which benchmark
checkpoints must be used to evaluate any future rebuild.

This contract does not execute a THLB rebuild, create generated THLB outputs,
materialize new source layers, or promote any MP11 evidence to model input.

## Evidence Inputs

Primary P8.2 evidence inputs:

- `planning/tfl6_mp11_land_base_crosswalk.md`;
- `planning/tfl6_mp11_land_base_crosswalk.csv`;
- `planning/tfl6_mp11_netdown_delta_crosswalk.md`;
- `planning/tfl6_mp11_netdown_delta_crosswalk.csv`;
- `planning/tfl6_mp11_baseline_and_promotion_contract.md`;
- `planning/tfl6_source_layer_dependency_inventory.md`;
- `planning/tfl6_source_layer_recipe_contracts.md`;
- `planning/tfl6_thlb_benchmark_tolerance.md`.

Current evidence status:

- MP11 land-base comparison rows: `8`, all `reviewed_evidence`,
  `phase6_land_base_comparison_only`, and `not_model_input`;
- MP11 netdown/source-layer delta rows: `9`, all `reviewed_evidence`,
  `phase6_land_base_comparison_only`, and `not_model_input`;
- MP11 current THLB comparison target: `120,099 ha`;
- Phase 5 accepted weighted THLB baseline: `139,995.798 ha`;
- delta from Phase 5 accepted baseline to MP11 current THLB:
  `-19,896.798 ha` or `-14.21%`.

## Rebuild Principle

The later MP11 THLB rebuild must be reproducible from public data wherever
possible and explicitly caveated wherever MP11 depends on unavailable WFP
source layers or private model assumptions.

The MP11 current THLB value of `120,099 ha` is a comparison target. It is not a
calibration constant, scale factor, or forced output. A future public-data THLB
rebuild may miss the MP11 target if the miss is explained by a named non-public
dependency, a public-proxy limitation, or a reviewed policy choice.

Disallowed implementation patterns:

- apply unexplained scaling to force public THLB output to `120,099 ha`;
- infer proprietary WFP geometry from aggregate MP11 tables;
- silently substitute public proxies for WFP LBB, ITI, LEFI, or objective
  assumptions;
- mix current THLB, future-road long-term landbase, and Patchworks scenario
  constraints in one area netdown output; or
- overwrite Phase 5 accepted runtime artifacts before replacement QA passes.

## Source-Layer Reproducibility Lanes

Every netdown/source-layer category must be assigned one of these lanes before
implementation:

| Lane | Meaning | May become model contract? |
| --- | --- | --- |
| `public_rebuild` | Public source geometry or public attribute logic can be materialized and directly QAed. | Yes, after source/profile QA. |
| `public_proxy` | A public approximation can be built, but it is not the exact MP11 source. | Yes, as a caveated proxy or sensitivity. |
| `public_proxy_plus_unavailable_gap` | A public proxy can represent part of the logic, while a named WFP/LiDAR/LBB dependency remains unavailable. | Yes, only with explicit caveat and sensitivity bounds. |
| `aspatial_policy` | The best public implementation is a documented area/rate/policy parameter, not a spatial layer. | Yes, if separately reviewed. |
| `model_parameter` | The issue belongs to yield, MHA, treatment eligibility, or curve parameters rather than THLB netdown. | No in the THLB rebuild lane. |
| `model_constraint` | The issue belongs to Patchworks constraints or scenario behavior rather than source-layer THLB. | No in the THLB rebuild lane. |
| `unavailable_non_public` | Required source is not public and no acceptable proxy is defined. | No. |

## MP11 Category Classification

| MP11 category | P6.3 class | P8.2 lane | Future treatment |
| --- | --- | --- | --- |
| Legal/proposed OGMAs and WHAs | `partially_public_spatial_layer_rebuild` | `public_rebuild` plus `public_proxy_plus_unavailable_gap` | Use public legal OGMA, non-legal OGMA, approved WHA, and approved UWR layers where applicable. Proposed or locally negotiated conservation areas remain version-sensitive and may require proxy or unavailable status. |
| Additional values: research, PSPs, big trees, karst | `mixed_public_proxy_or_confidential` | `public_proxy_plus_unavailable_gap` | Use public karst and big-tree candidates only if a public layer is identified and reviewed. Treat PSP/research locations as unavailable unless public-safe geometry exists. |
| Non-productive and low sites | `public_inventory_and_lidar_proxy` | `public_proxy_plus_unavailable_gap` | Rebuild public VRI/R1/VDYP productivity logic and add public DEM or public LiDAR proxy only if reproducible. Name any missing LEFI/ITI-style dependency. |
| Inoperable | `public_dem_proxy_plus_wfp_operability_gap` | `public_proxy_plus_unavailable_gap` | Build a public DEM/slope/terrain proxy and keep WFP LBB physical/economic operability geometry as unavailable unless supplied through a public-safe path. |
| Riparian management | `public_hydrography_lidar_proxy` | `public_rebuild` plus `public_proxy` | Use public FWA streams, lakes, wetlands, and shoreline candidates with reviewed buffer/order rules. Any LiDAR stream-class or operational overlap treatment remains caveated. |
| Terrain stability and LiDAR 90%+ slope | `public_dem_proxy_plus_lidar_gap` | `public_proxy_plus_unavailable_gap` | Build a public DEM slope proxy for 90%+ slope and terrain-screen sensitivity. Do not claim equivalence to WFP LiDAR unless source proof exists. |
| Existing and future WTRAs | `partly_aspatial_policy_parameter` | `aspatial_policy` plus `public_proxy` | Treat future WTRAs as policy/aspatial assumptions. Existing spatial WTRAs require a public source or reviewed proxy; otherwise they remain parameterized. |
| 95% CMAI MHA plus 350 m3/ha minimum volume | `model_parameter_rebuild` | `model_parameter` | Exclude from THLB area netdown. Hand off to P8.3/P8.4 AU/yield/MHA contracts. |
| VQO, ECA, adjacency, green-up, Patchworks spatial modelling | `model_constraint_rebuild` | `model_constraint` | Exclude from THLB area netdown. Hand off to P8.4/P8.5 scenario, constraint, and KPI contracts. |

## Public Source Candidates

The first implementation issue should start from already reviewed public-source
candidates where they exist:

| Dependency family | Candidate public source | Contract use |
| --- | --- | --- |
| TFL 6 AOI | FADM TFL boundary, accepted current-AOI layer | Keep as rebuild universe unless a later MP11 boundary issue shows a material boundary change. |
| Inventory/productivity | Accepted 2025 VRI R1 and VDYP7 TFL 6 extracts | Re-profile for MP11 non-forest, non-productive, low-site, deciduous-leading, and productivity logic. |
| Existing roads | Digital Road Atlas MPAR, with CEF Integrated Roads as reference | Existing-road overlay candidate only after road-class and width rules are reviewed. |
| Hydrology | FWA streams, lakes, wetlands | Riparian rebuild candidate after stream/lake/wetland class and buffer/order rules are accepted. |
| Shoreline | NTS BC coastline candidates | Coarse teaching candidate only; precision limitations must be recorded. |
| OGMA | Legal Current and Non-Legal Current OGMA public layers | Legal OGMA candidate and non-legal/proposed proxy candidate; current-vintage risk must be reported. |
| WHA/UWR | Approved WHA and approved UWR layers | Approved legal-overlay candidates; proposed layers excluded unless separately justified. |
| Recreation and reserves | Public recreation polygons/trails/sites, strategic/RMZ clues where available | Use only after field and rule review; otherwise keep prior aspatial/proxy treatment. |
| DEM/slope | Public DEM-derived slope surface | Public proxy for operability and 90%+ slope; not WFP LBB/LiDAR equivalence. |

## Unavailable Or Non-Public Dependencies

The following dependencies must be named as gaps unless public-safe source data
are later supplied and reviewed:

- WFP Land Base Blocking physical/economic operability geometry;
- WFP LiDAR-derived ITI and LEFI attributes;
- exact WFP operational stream/riparian interpretation if it depends on
  unavailable LiDAR or local operational mapping;
- exact WFP existing-WTRA spatial inventory if not public;
- private PSP/research-site geometries;
- WFP Patchworks objective weights, constraint internals, and model-control
  assumptions.

These gaps can be represented as `unavailable_non_public`, public proxy lanes,
or sensitivity lanes. They must not be hidden inside scripts, static tables, or
generated geometry.

## Benchmark Checkpoints

Future THLB implementation must report these checkpoints at minimum:

| Checkpoint | MP11 comparison target ha | Phase 5 reference ha | Required interpretation |
| --- | ---: | ---: | --- |
| Total land base | `217,197` | `217,042.719` | Boundary/AOI alignment check. Difference is currently small enough for planning comparison. |
| Total forested | `196,233` | `196,833.177` | Forested-area check after inventory class rules. |
| Productive forest / PFLB / AFLB | `187,425` | `191,168.597` | Productivity/low-site and forest-class check. |
| Total operable | `156,305` | `174,768.947` | Operability and economic-operability proxy check. |
| Current THLB | `120,099` | `139,995.798` | Central MP11 comparison target, not a forced output. |
| NCLB / productive forest unavailable for harvest | `67,326` | `51,172.799` | Complement check against accepted THLB/NTHLB surfaces. |
| Long-term land base after future roads | `118,672` | `134,598.870` | Long-term context only; keep separate from current THLB. |
| Previous-MP current AAC-supporting THLB | `133,665` | `136,487.728` | Historical/current-AAC-supporting context target, not replacement THLB. |

## Tolerances

Tolerance decisions must be explicit by checkpoint class:

- Total land base: target tolerance should be tight, because public FADM AOI is
  already within `0.1%` of the MP11 total land-base value.
- Forested/productive forest: report absolute and percent deltas; investigate
  differences above `2%` or any systematic category mismatch.
- Operable/current THLB: report absolute and percent deltas, but do not treat a
  large miss as failure if the miss is explained by unavailable WFP LBB,
  LiDAR/ITI/LEFI, or economic-operability dependencies.
- Long-term land base: report separately from current THLB because it includes
  future-road assumptions not executed in the Phase 5 base lane.
- Category netdowns: never validate by summing independent category areas
  without ordered overlay accounting, because MP11 reports overlap-sensitive
  reductions.

The first executable rebuild issue must define concrete pass/warn/fail bands
before running the recipe. Until then, all MP11 targets remain
`comparison_target`, not `accepted_model_contract`.

## Ordered Overlay Requirements

The next THLB recipe issue must define an ordered overlay sequence before
implementation. At minimum it must specify:

- AOI and base inventory universe;
- forested, productive, and low-site attribute exclusions;
- existing-road handling and whether road buffers are current-THLB or
  long-term context;
- legal reserve overlays and whether proposed/non-legal layers are accepted,
  proxied, or deferred;
- riparian buffer classes, shoreline handling, and overlap order;
- operability, slope, and terrain proxy order;
- WTRA/stand-level-retention policy treatment;
- whether any aspatial deductions are applied after spatial overlays; and
- area accounting fields for gross area, productive area, THLB-net reduction,
  overlap-adjusted reduction, and final current THLB.

## Handoff To Later Phase 8 Tasks

This P8.2 contract intentionally excludes several MP11 changes from the THLB
source-layer lane:

- AU identity, SI, VDYP/TIPSY, OAF, VRAF, NRL, genetic gain, fertilization,
  and managed-yield assumptions belong to P8.3.
- Harvest-system classification, helicopter/economic operability,
  minimum-harvest-age rules, `95%` CMAI, and `350 m3/ha` treatment eligibility
  belong to P8.4.
- VQO, ECA, adjacency, green-up, harvest-flow, AAC recommendation,
  sensitivity-scenario interpretation, and KPI reporting targets belong to
  P8.4/P8.5.

## Next Executable THLB Recipe Plan

A later implementation phase may execute a public-data MP11 THLB recipe only
after it has accepted this contract and opened a dedicated implementation
issue. That issue must:

1. identify each input layer and source authority;
2. materialize or verify source-layer artifacts with checksums/schema profiles;
3. define ordered overlay and aspatial deduction rules;
4. define checkpoint tolerances before running the recipe;
5. emit reproducible commands and a run manifest;
6. write generated outputs only under tracked/ignored paths according to repo
   policy;
7. compare results against MP11 checkpoints and Phase 5 accepted surfaces; and
8. explicitly state which rows, if any, move from `implementation_candidate`
   to `accepted_model_contract` or `accepted_model_input`.

## P8.2 Acceptance

P8.2 is complete when:

- this contract is tracked in `planning/`;
- `ROADMAP.md` marks P8.2 complete;
- `CHANGE_LOG.md` records the contract;
- issue `#60` is closed with validation evidence;
- no generated THLB outputs are tracked; and
- no MP11 value has been promoted to model-input status.
