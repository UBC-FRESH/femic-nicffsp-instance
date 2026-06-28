# TFL 6 MP11 Operability, Harvest-System, MHA, And Scenario Contract

## Purpose

This P8.4 contract defines how MP11 physical operability, helicopter economic
operability, harvest-system classification, minimum harvest age, and core
scenario policies should be represented before any transition, XML, or
Patchworks runtime rebuild. It separates stand-level model rules from AU
identity and keeps aggregate MP11 outputs as comparison targets rather than
stand-level assignments.

This contract does not assign harvest systems, regenerate transitions, modify
ForestModel XML, run Patchworks, or promote MP11 behavior values to model
inputs.

## Evidence Inputs

Primary P8.4 evidence inputs:

- `planning/tfl6_mp11_inventory_yield_operability_crosswalk.md`;
- `planning/tfl6_mp11_inventory_yield_operability_crosswalk.csv`;
- `planning/tfl6_mp11_model_behavior_crosswalk.md`;
- `planning/tfl6_mp11_model_behavior_crosswalk.csv`;
- `planning/tfl6_mp11_model_behavior_scenario_endpoints.csv`;
- `planning/tfl6_mp11_baseline_and_promotion_contract.md`;
- `planning/tfl6_mp11_source_layer_thlb_rebuild_contract.md`;
- `planning/tfl6_mp11_au_yield_strategy_contract.md`;
- `planning/tfl6_operability_netdown_proxy.md`.

Relevant reviewed evidence rows:

- `physical_operability_lbb`;
- `economic_operability_helicopter`;
- `minimum_harvest_age`;
- `harvest_system_distribution`;
- `spatial_patchworks_harvest_rules`;
- `alternate_harvest_flows`;
- `policy_and_constraint_sensitivities`;
- `aac_recommendation_bridge`.

Every row remains `reviewed_evidence`, comparison/planning-only downstream use,
and `not_model_input`.

## Rule Separation

Future MP11 implementation must keep these concepts separate:

| Concept | Role | Must not be confused with |
| --- | --- | --- |
| Physical operability | THLB/source-layer or treatment-eligibility surface. | Canonical AU identity. |
| Harvest-system class | Stand-level classifier for ground, cable, and non-conventional/helicopter reporting and eligibility. | MP11 aggregate percentages or AU identity. |
| Economic helicopter operability | Sensitivity or scenario rule using public proxies. | Physical LBB geometry or exact WFP cost model. |
| Minimum harvest age | Treatment/transition eligibility rule attached to curve/AU/stand records. | Yield curve identity or static AU key. |
| Scenario policy | Patchworks objective/constraint/run configuration. | Source-layer THLB netdown or generated model input tables. |

## Physical Operability Strategy

WFP Land Base Blocking remains unavailable unless a public-safe source appears.
The public-data implementation path is therefore a proxy and sensitivity lane:

- build DEM/slope-derived stand metrics from public data;
- combine slope metrics with public inventory volume, height, species, and
  stocking/open-stand signals;
- keep physical operability and economic operability as separate rule fields;
- compare the public proxy against MP11's inoperable THLB-net reduction target
  of `21,193 ha` only as a comparison target; and
- report residual gaps rather than forcing the proxy to reproduce WFP LBB.

The accepted Phase 5 operability proxy notes remain useful design evidence, but
MP11 implementation must document how the MP11 gap differs from the earlier
MP10 teaching proxy.

## Harvest-System Classifier Candidates

A future harvest-system classifier should begin with public stand-level
features:

- DEM-derived slope proportions, including a `30%` ground/cable split candidate
  retained from earlier TFL 6 evidence;
- stand volume per hectare;
- height class or height proxy;
- preferred species shares, especially Cw, Fd, Yc/Cy, hemlock/balsam, pine,
  and deciduous-leading signals;
- road/access or distance-to-road proxies only after public road layers are
  materialized and reviewed; and
- public physical-operability proxy class.

Classifier outputs should be explicit fields such as:

- `harvest_system_candidate`: `ground`, `cable`, `helicopter`,
  `non_conventional`, `excluded`, or `unknown`;
- `harvest_system_basis`: slope, volume, species, access, proxy, manual, or
  unavailable;
- `harvest_system_confidence`: high, medium, low, or review required; and
- `harvest_system_public_private_status`: public, proxy, sensitivity, or
  unavailable.

MP11 aggregate distributions are comparison targets only:

- THLB by harvest system: `57.3%` ground, `39.6%` cable, `3.1%`
  non-conventional;
- base-case harvest-system average: about `57%` ground, `40%` cable, and `3%`
  helicopter.

These percentages must not be backfilled as stand-level assignments.

## Helicopter Economic-Operability Sensitivity

MP11 reports a dedicated economic screen for helicopter/non-conventional
stands. Public implementation should treat this as a sensitivity lane unless
the underlying WFP access/cost model is public-safe.

Candidate public proxy inputs:

- stand volume per hectare;
- Cw, Fd, and Yc/Cy component share;
- slope/terrain class;
- distance-to-road or distance-to-access proxy after road-source review;
- approximate flight-distance/access zones only if a public method is
  documented; and
- harvest-system candidate class.

Required scenario switches:

- include helicopter stands with no additional economic screen;
- exclude helicopter/non-conventional stands;
- include helicopter stands only if public volume/species/access thresholds
  pass; and
- compare against MP11's helicopter-excluded sensitivity endpoint
  `1,021,900 m3/year`.

The MP11 statement that only `20 ha` were netted down as non-conventional
uneconomic is a comparison clue, not enough information to infer WFP's
stand-level economic screen.

## Minimum Harvest Age Contract

MP11 MHA must be represented as a treatment/transition eligibility rule, not an
AU identity dimension.

Implementation requirements for a later issue:

- extract MP11 Tables 71-72 and surrounding text into a reviewed MHA library;
- represent `95%` CMAI age and `350 m3/ha` minimum volume as separate rule
  fields;
- attach the accepted rule to AU/curve/stand records through stable keys;
- preserve future-stand weighted-average MHA `64 years` and average volume
  `586 m3/ha` as comparison targets only until extracted and reviewed;
- define whether MHA applies to all harvest systems or varies by curve lane;
  and
- define how MHA interacts with managed-stand yield curves, utilization, and
  NRL.

Sensitivity targets:

- MHA +10 endpoint: `956,000 m3/year`;
- MHA -10 endpoint: `1,074,300 m3/year`.

These endpoints are scenario comparison targets, not model-input parameters.

## Scenario Policy Contract

The first MP11-aligned runtime should define scenario policy before
interpreting outputs. At minimum it should distinguish:

| Scenario family | MP11 evidence | P8.4 contract |
| --- | --- | --- |
| Base case | `1,061,600 m3/year` even-flow target over 300 years, net of NRL. | Future QA target after source-layer, AU/yield, MHA, and constraint rebuilds. |
| Maintain current AAC | Long-term endpoint `1,055,200 m3/year`. | Explicit harvest-flow scenario, not the base-case default. |
| Maximum short-term | First-decade `1,147,700 m3/year`; long-term endpoint `1,095,500 m3/year`. | Separate objective/run policy with mid-term guardrails. |
| AAC recommendation | `1,252,700 m3/year`, linked to LiDAR/ITI/LEFI/OAF1 assumptions. | High-level target gated on unavailable private-data sensitivity handling. |
| THLB +/- 10% | `1,118,200` and `953,500 m3/year`. | Landbase sensitivity after THLB source-layer rebuild. |
| Genetic gain removed | `1,004,000 m3/year`. | Yield-parameter sensitivity linked to P8.3. |
| Helicopter excluded | `1,021,900 m3/year`. | Harvest-system/economic-operability sensitivity. |

Scenario definitions must identify:

- objective function or run mode;
- planning horizon;
- flow period and even-flow/step-down semantics;
- active source-layer, yield, MHA, harvest-system, and constraint variants;
- output KPIs required for comparison; and
- whether the scenario is base, sensitivity, recommendation, or teaching-only.

## Patchworks Constraint Boundary

P8.4 records the scenario-rule boundary but does not implement Patchworks
constraints. The later runtime rebuild must separately review:

- green-up and adjacency;
- patch-size/block-size targets;
- VQO constraints;
- ECA/watershed constraints;
- biodiversity, old-growth, and NSOG constraints;
- objective weights; and
- any private WFP model-control assumptions.

Public constraints may be rebuilt only where source layers and rule semantics
are public-safe. WFP objective weights and exact internal controls remain
unavailable unless explicitly supplied and reviewed.

## Acceptance Checks For Later Implementation

A future implementation phase must pass these checks before treating outputs as
MP11-comparable:

- physical operability, harvest-system class, economic operability, MHA, and
  AU identity are stored as separate fields/contracts;
- aggregate MP11 harvest-system percentages are used only as comparison
  targets;
- every harvest-system assignment has a public source/proxy basis;
- every MHA rule has source table/text provenance;
- every scenario has a named run policy and active variant set;
- no WFP LBB geometry, private access layer, or proprietary objective weight is
  embedded in public artifacts; and
- output comparisons state whether they are direct, proxy, sensitivity, or
  unavailable-non-public comparisons.

## Handoff To P8.5

P8.5 should use this contract to define KPI and reporting targets, including:

- harvest-system KPI tables;
- harvested area, volume per hectare, harvest age, block size, and elevation;
- growing stock by age class;
- cedar, old cedar, and old-seral reporting;
- scenario endpoint comparison tables; and
- validation-strength labels for each target.

## P8.4 Acceptance

P8.4 is complete when:

- this contract is tracked in `planning/`;
- `ROADMAP.md` marks P8.4 complete;
- `CHANGE_LOG.md` records the contract;
- issue `#62` is closed with validation evidence;
- no runtime/XML/transition artifacts are modified; and
- no MP11 behavior value has been promoted to model-input status.
