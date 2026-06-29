# TFL 6 MP11 Phase 14 Closeout

Phase 14 converted the deferred MP11 harvest-system caveat into a public-proxy
ground/cable/heli runtime lane for the MP11 candidate model. It did not replace
the accepted Phase 5 teaching/runtime baseline, reconstruct WFP's private Land
Base Blocking (LBB) layer, claim WFP-model equivalence, or make an approved AAC
claim.

## Status

Phase 14 status: `complete`.

Closeout decision: the harvest-system candidate runtime is suitable for labelled
MP11 comparison and advanced teaching workflows. It remains a public-data
candidate supplement to the Phase 5 baseline.

Governing issue tree:

- `#138`: Phase 14 parent issue.
- `#139`: P14.1 launch execution plan.
- `#140`: P14.2 harvest-system evidence mining.
- `#141`: P14.3 public proxy metrics.
- `#142`: P14.4 harvest-system classification and QA.
- `#143`: P14.5 split-lane model input and ForestModel XML.
- `#144`: P14.6 Matrix Builder and runtime assembly.
- `#145`: P14.7 all-system and no-heli smoke tests.
- `#146`: P14.8 documentation and closeout.

## Evidence Basis

The governing MP11 harvest-system source is WFP's LBB process, but that layer is
not public or queryable from the MP11 package. Phase 14 therefore implemented a
public proxy, using MP11 text/table anchors only as criteria and aggregate
comparison evidence.

The public proxy uses:

- MP11 Table 20 / Table 73 area and volume distributions as comparison targets;
- MP11 Tables 27-29 helicopter economic-operability criteria where public
  inventory and access proxies exist;
- P9D public CDED slope context;
- public VRI age, volume, and species-share proxies; and
- nearest-DRA-road distance as an access-distance proxy.

The public proxy does not use private WFP LBB geometry, WFP LiDAR/ITI/LEFI
assignment surfaces, future block/road planning, or post-harvest internal review
layers.

## Classification Result

P14.4 classified `22,614` managed current THLB rows across `139,995.798 ha` of
the candidate scaffold:

| System | Candidate Rows | Candidate Area (ha) | Candidate Volume (m3) | Area Share (%) | MP11 Table 73 Area Share (%) | Area Residual (pp) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Ground | 12,905 | 80,241.389 | 22,778,489.535 | 57.317 | 57.300 | 0.017 |
| Cable | 9,055 | 56,677.061 | 20,342,940.218 | 40.485 | 39.600 | 0.885 |
| Heli | 654 | 3,077.349 | 1,921,687.622 | 2.198 | 3.100 | -0.902 |

Direct area/volume residuals are not WFP LBB stand-level errors. The candidate
scaffold total is larger than MP11 Table 73 and public VRI volume proxies are
not WFP inventory truth. Normalized shares are the useful comparison surface for
Phase 14 closeout.

## Model-Input And XML Result

P14.5 generated ignored candidate model-input and ForestModel XML roots:

- `data/mp11_harvest_system_model_input_bundle/`;
- `output/patchworks_tfl6_mp11_harvest_system_candidate/`.

The XML retains aggregate `.CC` harvested-volume products for all-system
reporting and splits managed clearcut treatment lanes by fragment `HVSYS`:

- `814` `CC_GROUND` treatment nodes;
- `814` `CC_CABLE` treatment nodes;
- `814` `CC_HELI` treatment nodes;
- `2,442` `HVSYS` split managed selects; and
- `2,442` split product selects.

P14.5 did not run Matrix Builder or Patchworks scenarios. Those checks were
completed in P14.6 and P14.7.

## Runtime And Smoke Result

P14.6 ran Matrix Builder and assembled the harvest-system candidate runtime:

- Matrix Builder run ID:
  `tfl6_mp11_harvest_system_p14_6_matrix_build`;
- `13` generated track files;
- `93,330` feature rows;
- `829` account rows and `829` protoaccount rows;
- `46,605` product rows;
- `18,642` treatment rows;
- `0` message rows;
- `10,790` `CC_GROUND`, `6,960` `CC_CABLE`, and `892` `CC_HELI` treatment
  rows;
- `24,879` block rows;
- `191,168.566447 ha` block area;
- valid `EPSG:3005` block geometry; and
- `170,759` topology rows.

P14.7 direct launch and scenario smoke passed:

| Run | Result | Schedule Rows | Treatments |
| --- | --- | ---: | --- |
| Direct launch | Pass | 0 | none |
| All-system 200k smoke | Pass | 76,635 | `CC_CABLE`, `CC_GROUND`, `CC_HELI` |
| No-heli 200k smoke | Pass | 75,086 | `CC_CABLE`, `CC_GROUND` |

The no-heli track variant is generated under ignored `tracks_no_heli/`. The
variant removes `CC_HELI` treatment, product, account, and protoaccount rows
while leaving the all-system `tracks/` outputs intact.

## Caveats

Phase 14 removes the generic-CC-only limitation for the MP11 candidate runtime,
but the result is still caveated:

- WFP LBB is unavailable and was not reconstructed.
- Ground/cable/heli classes are public proxy assignments, not operational
  assignments approved by WFP.
- The slope input is public CDED context, not WFP LiDAR terrain analysis.
- Nearest-DRA-road distance is a rough public access proxy, not a flight
  distance or WFP road-planning surface.
- Public VRI age, volume, and species-share fields are not WFP ITI/LEFI truth.
- MP11 MHA, scenario-policy, delivered-cost, block-size, and harvest-age KPI
  surfaces remain future work unless separately promoted.
- The runtime is smoke-tested, not release-archive materialized in a clean
  checkout.

## Closeout Interpretation

Phase 14 is a real runtime upgrade, not just a documentation note. It added a
public-proxy harvest-system classifier, rebuilt model-input and XML surfaces,
ran Matrix Builder, assembled the candidate runtime, and passed direct launch,
all-system, and no-heli scenario smoke.

The correct release language remains careful:

- Phase 5 remains the accepted public teaching/runtime baseline.
- The MP11 harvest-system candidate supplements Phase 5 for MP11 comparison and
  advanced teaching.
- The candidate is plausibly useful for exploring harvest-system effects, but
  it is not WFP-model equivalent.
- The candidate is not an approved AAC model.
- Future work should open a new phase or issue if the harvest-system candidate
  is to be archive-published, clean-checkout materialized, calibrated against a
  broader MP11 KPI suite, or promoted toward replacing Phase 5.

