# TFL 6 MP11 Phase 11 Promotion Gates And Stop Conditions

## Purpose

This P11.1d note defines the gates that P11.2 must evaluate before any MP11
model-input bundle, export bridge, ForestModel XML, Matrix Builder output, or
Patchworks runtime artifact is generated.

This is a planning and audit contract only. It does not promote any MP11
surface to model input.

Companion structured files:

- `planning/tfl6_mp11_phase11_promotion_gates.csv`
- `planning/tfl6_mp11_phase11_promotion_gates.json`

## Required P11.2 Decision

P11.2 must emit `planning/tfl6_mp11_model_input_promotion_readiness.{csv,json,md}`
with one row per gate below. Each row must record:

- gate ID;
- target model-input or XML role;
- source artifact path;
- required promotion state;
- actual promotion state;
- required QA evidence;
- decision: `pass`, `blocked`, or `deferred`;
- blocker or caveat text; and
- issue or planning note that owns the next action.

P11.3 may build candidate model-input manifests only if all hard gates pass.
Soft gates may remain deferred only when the readiness manifest says which
later phase owns them and why they do not affect model-input table generation.

## Hard Gates

| Gate | Target role | Required condition | Stop condition |
| --- | --- | --- | --- |
| `p11_gate_01_baseline_protection` | all generated outputs | Candidate paths use the MP11 namespace from `planning/tfl6_mp11_phase11_artifact_layout.md`. | Any generated output would overwrite Phase 5 `data/model_input_bundle/`, `output/patchworks_tfl6_validated/`, `models/tfl6_patchworks_model/`, or the Phase 5 release archive. |
| `p11_gate_02_source_thlb` | stand universe and THLB/NTHLB state | P9RF resultant-fragment THLB is explicitly accepted, caveated, or blocked for each model-input table role. | P11.2 cannot identify which P9RF THLB/source-layer outputs feed geometry, managed share, unmanaged share, area, and group fields. |
| `p11_gate_03_curve_handoff` | natural and managed curves | Accepted Phase 10R curve handoff maps deterministically to model-input curve IDs, with all 27 Table 57 curves accounted for. | Any accepted curve lacks feature ID, curve ID, source row, canonical AU target, or review status. |
| `p11_gate_04_deferred_tables_54_55` | early/recent managed curves | Tables 54/55 remain excluded unless a public-safe AU-code mapping is reviewed and accepted. | Any model-input table consumes Tables 54/55 directly without that mapping. |
| `p11_gate_05_figure_evidence` | all numeric model fields | Figure-derived values are excluded unless separately promoted to an accepted model contract. | Any figure-recovered value enters model-input tables from `comparison_target`, `reviewed_for_planning`, or raw extraction status. |
| `p11_gate_06_rule_contracts` | treatments, transitions, MHA, harvest system, operability, scenarios | Phase 8/10 rule contracts identify which MP11 rules are accepted, proxy-only, sensitivity-only, unavailable, or deferred. | P11.3 would need to invent treatment, transition, MHA, harvest-system, operability, or scenario fields not covered by reviewed contracts. |
| `p11_gate_07_schema_bridge` | model-input tables and export compatibility | P11.2 names the candidate table roles and whether they reuse, replace, or extend the Phase 5 schema/export bridge. | P11.3 cannot define required tables, keys, field names, and export-compatibility needs before writing generated outputs. |
| `p11_gate_08_private_data` | all promoted fields | Non-public WFP ITI/LEFI/LBB/objective-weight dependencies are marked unavailable, proxied, sensitivity-only, or deferred. | Any generated model input implies private WFP stand-level data or unpublished model internals from public summaries. |

## Soft Gates

| Gate | Target role | Required condition | Deferral rule |
| --- | --- | --- | --- |
| `p11_gate_09_kpi_reporting` | reporting and QA fields | KPI/reporting targets from `planning/tfl6_mp11_kpi_qa_reporting_contract.md` are classified as model-input, XML/report, runtime, docs, or comparison-only. | May defer runtime-only and docs-only outputs to Phases 12/13 if model-input table generation does not require them. |
| `p11_gate_10_xml_readiness` | ForestModel XML | P11.2 identifies whether enough model-input metadata exists to attempt P11.4 XML readiness. | May defer XML generation with a stop report if P11.3 cannot produce a candidate manifest. |
| `p11_gate_11_runtime_boundary` | Matrix Builder and Patchworks runtime | Runtime checks are assigned to Phase 12 unless P11.4 defines a parse-only XML check. | Must not run Matrix Builder or Patchworks runtime in P11.2/P11.3. |

## P11.2 Stop Report Requirements

If any hard gate is blocked, P11.2 must write a stop report instead of
unlocking candidate generation. The stop report must:

- name each blocked gate;
- cite the missing source, contract, mapping, or QA evidence;
- state whether the issue is a public-data gap, private-data gap, parser gap,
  model-contract gap, or implementation gap;
- identify the child issue or later phase that can resolve it; and
- explicitly keep P11.3 model-input generation blocked.

## P11.3 Unlock Requirements

P11.3 may start only after the P11.2 readiness manifest records:

- all hard gates as `pass`;
- any soft-gate deferrals as non-blocking with rationale;
- the MP11 candidate output roots from
  `planning/tfl6_mp11_phase11_artifact_layout.md`;
- the Phase 5 baseline paths that must remain untouched; and
- the exact candidate manifest paths P11.3 may write.

## Current Status

P11.2 emitted
`planning/tfl6_mp11_model_input_promotion_readiness.{csv,json,md}` and resolved
the three former hard blockers through candidate-only scaffold decisions. P11.3
may now consume the readiness manifest to build a candidate manifest, but this
does not authorize generated model-input tables, ForestModel XML, Matrix
Builder outputs, or Patchworks runtime artifacts.
