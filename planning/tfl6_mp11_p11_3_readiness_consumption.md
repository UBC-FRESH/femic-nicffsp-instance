# TFL 6 MP11 P11.3 Readiness Consumption

## Purpose

This P11.3a note consumes the P11.2 promotion-readiness manifest and records
the entry contract for P11.3 candidate-manifest work. It does not build
model-input tables, ForestModel XML, Matrix Builder outputs, or Patchworks
runtime artifacts.

Companion structured file:

- `planning/tfl6_mp11_p11_3_readiness_consumption.json`

## Consumed Inputs

| Input | Role |
| --- | --- |
| `planning/tfl6_mp11_model_input_promotion_readiness.{csv,json,md}` | Governing readiness manifest. |
| `planning/tfl6_mp11_p11_2_candidate_scaffold_decisions.md` | Candidate-only source/THLB and rule-field decisions. |
| `planning/tfl6_mp11_p11_2_candidate_schema_bridge.{csv,json,md}` | Candidate table-role bridge. |
| `planning/tfl6_mp11_phase11_artifact_layout.{csv,json,md}` | Candidate output roots and baseline-protection rules. |

## Readiness Consumption Result

The P11.2 readiness manifest records:

- gates: `11`;
- blocked hard gates: `0`;
- passing gates: `9`;
- deferred soft gates: `2`;
- missing source artifacts: `0`; and
- P11.3 unlock status: `candidate_manifest_eligible`.

P11.3 may proceed to P11.3b candidate table/schema manifest construction.

## Candidate-Manifest Scope

P11.3b may build
`planning/tfl6_mp11_model_input_candidate_manifest.{csv,json,md}` from the
P11.2 schema bridge. The candidate manifest must record, for each table role:

- bridge action: `reuse`, `replace`, `extend`, or `defer`;
- source artifact;
- candidate output path if later generation is authorized;
- required caveat fields;
- fallback or exclusion policy;
- downstream status; and
- whether the role is eligible for table generation, deferred, or blocked.

## Required Caveats To Preserve

P11.3b must preserve these P11.2 caveats:

- P9RF source/THLB is accepted only for candidate-scaffold roles;
- P9RF current THLB is `122,763.421 ha`, compared with the MP11 target
  `120,099.000 ha`;
- proposed WHA, uneconomic, archaeological, research-site, TUS, big-tree,
  karst, and future stand-level reserve caveats must remain visible;
- MP11 MHA, harvest-system assignment, helicopter economic operability, and
  scenario policy are deferred unless separately promoted;
- Tables 54/55 remain excluded without a public-safe AU-code mapping;
- figure-derived values remain excluded from model-input fields; and
- WFP private dependencies remain unavailable, proxy-only, sensitivity-only, or
  deferred.

## Non-Goals

P11.3a and P11.3b do not authorize:

- generated tables under `data/mp11_model_input_bundle/`;
- ForestModel XML or fragments;
- Matrix Builder;
- Patchworks runtime package assembly;
- release archive work; or
- replacement of the accepted Phase 5 teaching/runtime baseline.

## Next Step

P11.3b should build the candidate table/schema manifest or a blocked stop
report from the consumed readiness and schema-bridge inputs.
