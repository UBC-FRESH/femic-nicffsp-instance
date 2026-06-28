# TFL 6 MP11 KPI, QA, And Reporting Contract

## Purpose

This P8.5 contract defines the MP11 comparison targets, validation-strength
labels, reporting surfaces, and QA expectations needed before future model
outputs can be compared against published MP11 evidence. It keeps
comparison-ready figure evidence separate from planning-only and deferred
figure evidence.

This contract does not build reports from Patchworks outputs, regenerate model
outputs, or promote recovered figure values to model inputs.

## Evidence Inputs

Primary P8.5 evidence inputs:

- `planning/tfl6_mp11_model_behavior_crosswalk.md`;
- `planning/tfl6_mp11_model_behavior_crosswalk.csv`;
- `planning/tfl6_mp11_model_behavior_scenario_endpoints.csv`;
- `planning/tfl6_mp11_figure_extraction_closeout.md`;
- `planning/tfl6_mp11_figure_extraction_closeout.csv`;
- `planning/tfl6_mp11_baseline_and_promotion_contract.md`;
- `planning/tfl6_mp11_operability_harvest_mha_scenario_contract.md`.

Evidence-status summary:

- accepted comparison figures: `22`;
- reviewed planning-only figures: `14`;
- deferred figures: `20`;
- qualitative context figures: `5`;
- model-input status for all figure rows: `not_model_input`.

## Validation-Strength Labels

Future comparison tables and docs must label every MP11 target with one of
these validation strengths:

| Label | Meaning | Examples |
| --- | --- | --- |
| `source_text_or_table_target` | Value is directly available from MP11 text/table evidence or a visible table row. | Current AAC, base-case level, AAC recommendation, some sensitivity endpoints. |
| `accepted_figure_comparison` | Value comes from a reviewed Phase 7 figure extraction accepted for comparison only. | Figures 2, 3, 20-26, 29-40, 57. |
| `planning_only_figure_context` | Figure was reviewed but not accepted as quantitative comparison target. | Age-class, cedar, old-cedar, and old-seral planning figures. |
| `deferred_optional_figure` | Figure was inventoried/cropped but not extracted in Phase 7. | Medium-priority stacked, grouped, and mixed KPI charts. |
| `qualitative_context_only` | Figure is a map, diagram, or context image. | Overview/context figures. |
| `unavailable_non_public` | Target depends on unpublished WFP model internals or source data. | Objective weights, exact private inventory surfaces, full unpublished KPI tables. |

Only `source_text_or_table_target` and `accepted_figure_comparison` values may
be used as quantitative comparison targets without a new review issue.

## Mandatory Scenario Output Groups

A future MP11-aligned runtime should emit comparable outputs for these scenario
families:

| Scenario family | Required outputs | MP11 target strength |
| --- | --- | --- |
| Base case | Harvest flow, THLB growing stock, harvested area, volume per hectare, harvest age, species mix, elevation, harvest-system split, block-size summary. | Source/table plus accepted figures where available. |
| Maintain current AAC | Harvest-flow trajectory and long-term endpoint. | Accepted figure comparison. |
| Maximum short-term | First-decade harvest level, long-term endpoint, and mid-term guardrail metrics. | Accepted figure comparison. |
| Yield sensitivities | Natural +/-10%, managed +/-10%, ITI/LEFI/OAF1 sensitivity endpoints. | Accepted figure comparison, with unavailable-private-data caveats. |
| Policy sensitivities | No genetic gain, full NSOG, MHA +/-10, helicopter excluded, THLB +/-10. | Accepted figure comparison. |
| AAC recommendation | Step-down recommendation trajectory, endpoint, and delta from base case. | Source/table plus accepted figure comparison. |

## KPI Reporting Surfaces

Future reports should define these output schemas before implementation:

| KPI family | Required fields | Validation boundary |
| --- | --- | --- |
| Harvest flow | scenario, period/year, volume, delta vs base, validation strength. | Quantitative comparison accepted for listed scenario endpoints. |
| Growing stock | scenario, period/year, age-class group, volume, THLB/NTHLB where applicable. | Base and AAC min/max targets are comparison targets; full trajectories require curve/output QA. |
| Harvest system | scenario, period/year, system class, volume, area, percent. | Aggregate MP11 percentages are comparison targets only; stand-level class must come from public proxy. |
| Harvested area and volume per hectare | scenario, period/year, area, volume, volume/ha. | Required for MP11-style reporting after runtime rebuild. |
| Harvest age | scenario, period/year, age statistic, harvest system or stand family where available. | Report design required before MHA comparisons. |
| Block size | scenario, period/year, block-size statistic, harvest system where available. | Average block size `19.1 ha` is comparison evidence, not model input. |
| Species composition | scenario, period/year, species group, volume and percent. | Required for MP11-style reporting; exact source target strength varies. |
| Elevation band | scenario, period/year, elevation band, area and volume. | Required for MP11-style reporting; may need public DEM bin contract. |
| Age class | scenario, period/year, age class, productive forest/THLB area. | Figure 6 remains planning-only until independently accepted. |
| Cedar and old cedar | scenario, period/year, cedar family, age/stock class, area and volume where available. | Figures 14-19 and 51-56 remain planning-only. |
| Old seral | scenario, period/year, BEC/LU/seral target family, area and target status. | Planning-only unless later promoted through source/table review. |

## Accepted Comparison Targets

The first comparison table should include at minimum:

- current AAC: `1,362,000 m3/year`;
- MP11 Base Case: `1,061,600 m3/year`;
- MP11 AAC recommendation: `1,252,700 m3/year`;
- maintain-current-AAC endpoint: `1,055,200 m3/year`;
- maximum-short-term first decade: `1,147,700 m3/year`;
- maximum-short-term long-term endpoint: `1,095,500 m3/year`;
- natural yield +10/-10 endpoints: `1,075,300` and `1,036,600 m3/year`;
- managed yield +10/-10 endpoints: `1,138,800` and `970,900 m3/year`;
- no genetic gain endpoint: `1,004,000 m3/year`;
- full NSOG endpoint: `1,049,400 m3/year`;
- MHA +10/-10 endpoints: `956,000` and `1,074,300 m3/year`;
- helicopter excluded endpoint: `1,021,900 m3/year`;
- THLB +10/-10 endpoints: `1,118,200` and `953,500 m3/year`; and
- base-case harvest-system average: about `57%` ground, `40%` cable, and `3%`
  helicopter.

All targets remain `not_model_input`.

## Planning-Only And Deferred Figure Families

Planning-only reviewed figures may guide report design, but not quantitative
acceptance:

- age-class planning: Figure 6;
- cedar and old-cedar planning: Figures 14-19 and 51-56;
- old-seral planning: Figures 45 and related reviewed planning figures.

Deferred optional figures should be extracted later only if they become needed
for QA or documentation:

- base-case harvest by stand era and seral stages;
- harvest-system, block-size, harvest-age, harvested-area, volume-per-hectare,
  species, and elevation medium-priority charts;
- other stacked, grouped, or mixed KPI figures that were out of scope for
  Phase 7.

Deferred figures are good future `figrecover` stress tests, but they are not
required to close Phase 8.

## Tolerance Guidance

Tolerance should be tied to target strength:

- Source text/table values: exact value match after rounding to the published
  unit, with any model-output difference reported in absolute and percent
  terms.
- Accepted figure comparison endpoints: use the recorded extraction endpoint
  error as QA context and report model-vs-target differences to the published
  precision.
- Approximate trajectory comparisons: compare shape, endpoint, and broad
  magnitude separately; do not require pointwise equality for recovered chart
  trajectories.
- Planning-only figures: report qualitative alignment only unless a later
  issue promotes the figure with stronger review.
- Unavailable-private-data scenarios: report residual gap and caveat rather
  than treating mismatch as implementation failure.

## Required QA Outputs

A future MP11 comparison report should include:

- scenario endpoint comparison table;
- land-base checkpoint comparison table;
- yield/curve sensitivity comparison table;
- harvest-system proxy comparison table;
- growing-stock summary;
- MHA and helicopter-exclusion sensitivity comparison;
- figure-target provenance table with validation-strength labels;
- model-output provenance manifest; and
- explicit caveat section for WFP private-data gaps.

## P8.5 Acceptance

P8.5 is complete when:

- this contract is tracked in `planning/`;
- `ROADMAP.md` marks P8.5 complete;
- `CHANGE_LOG.md` records the contract;
- issue `#63` is closed with validation evidence;
- no new runtime reports are generated; and
- no planning-only figure evidence has been promoted to comparison target or
  model-input status.
