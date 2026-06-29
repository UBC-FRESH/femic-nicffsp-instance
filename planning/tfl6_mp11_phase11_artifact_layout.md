# TFL 6 MP11 Phase 11 Artifact Layout And Hygiene

## Purpose

This P11.1c note defines the Phase 11 artifact layout and generated-output
hygiene rules before any MP11 model-input bundle, ForestModel XML, Matrix
Builder output, Patchworks runtime package, or release archive is generated.

Companion structured files:

- `planning/tfl6_mp11_phase11_artifact_layout.csv`
- `planning/tfl6_mp11_phase11_artifact_layout.json`

## Baseline Protection Rule

The accepted Phase 5 teaching baseline remains protected:

| Phase 5 surface | Accepted path |
| --- | --- |
| model-input rebuild provenance | `data/model_input_bundle/` |
| accepted ForestModel XML/fragments | `output/patchworks_tfl6_validated/` |
| accepted runtime root | `models/tfl6_patchworks_model/` |
| accepted public release archive | `releases/tfl6_patchworks_runtime_p5_2.zip` |

Phase 11 must not overwrite these accepted Phase 5 payloads while building MP11
candidate surfaces. A later replacement decision can only happen after
model-input checks, XML checks, Matrix Builder, Patchworks runtime smoke,
documentation, and release QA pass.

## Tracked Planning Surfaces

Phase 11 planning and manifest surfaces are compact and tracked in Git:

| Surface | Path |
| --- | --- |
| execution plan | `planning/tfl6_mp11_phase11_model_input_xml_execution_plan.md` |
| Phase 5 provenance inventory | `planning/tfl6_mp11_phase11_phase5_provenance_inventory.{csv,json,md}` |
| artifact layout | `planning/tfl6_mp11_phase11_artifact_layout.{csv,json,md}` |
| promotion readiness | `planning/tfl6_mp11_model_input_promotion_readiness.{csv,json,md}` |
| candidate manifest or stop report | `planning/tfl6_mp11_model_input_candidate_manifest.{csv,json,md}` |
| XML readiness or stop report | `planning/tfl6_mp11_forestmodel_xml_readiness.{csv,json,md}` |

Tracked planning files may contain compact row counts, checksums, source paths,
promotion statuses, issue references, and accepted caveats. They must not
contain bulky generated payloads, private-source details, personal local paths,
or unreleasable extracted data.

## Candidate Generated Roots

If P11.2 accepts promotion readiness, Phase 11 candidate outputs must use MP11
namespaced generated paths:

| Surface | Candidate path | Policy |
| --- | --- | --- |
| model-input bundle | `data/mp11_model_input_bundle/` | ignored generated output |
| input geometry handoff | `data/mp11_model_input_bundle/input_geometry/` | ignored generated output |
| bundle QA | `data/mp11_model_input_bundle/qa/` | ignored generated output |
| export compatibility bridge | `data/mp11_model_input_bundle/export_compat/` | ignored generated output |
| ForestModel XML/fragments | `output/patchworks_tfl6_mp11_candidate/` | ignored generated output |
| command logs/manifests | `runtime/mp11_model_input_xml/` | ignored generated output |
| review plots | `plots/mp11_model_input_xml/` | ignored generated output |

Phase 12 candidate runtime surfaces should also use an MP11 namespace:

| Surface | Candidate path | Policy |
| --- | --- | --- |
| candidate runtime root | `models/tfl6_patchworks_model_mp11_candidate/` | mixed later decision |
| Matrix Builder tracks | `models/tfl6_patchworks_model_mp11_candidate/tracks/` | ignored generated output |
| blocks/topology | `models/tfl6_patchworks_model_mp11_candidate/blocks/` | ignored generated output |
| saved-stage smoke output | `models/tfl6_patchworks_model_mp11_candidate/analysis/p*/` | ignored generated output |
| headless runtime output | `models/tfl6_patchworks_model_mp11_candidate/analysis/headless_runs/` | ignored generated output |

Phase 12 may later decide whether compact launch surfaces under the candidate
runtime root should be tracked. Generated tracks, blocks, logs, and saved-stage
outputs remain ignored.

## Write Gates

Before P11.2 finishes, allowed writes are limited to:

- tracked planning notes;
- compact structured planning manifests;
- ignored audit logs under `runtime/mp11_model_input_xml/`; and
- ignored review plots under `plots/mp11_model_input_xml/` if needed.

P11.3 may write `data/mp11_model_input_bundle/` only after P11.2 accepts the
promotion-readiness manifest.

P11.4 may write `data/mp11_model_input_bundle/export_compat/` and
`output/patchworks_tfl6_mp11_candidate/` only after P11.3 emits a candidate
manifest or stop report.

Matrix Builder tracks, blocks/topology, Patchworks runtime surfaces, runtime
smoke outputs, and release archives are Phase 12/13 work unless a child issue
explicitly narrows a parse-only or readiness-only check.

## Required Hygiene Checks

Before any P11 candidate output is accepted:

- candidate paths must include an `mp11` or `mp11_candidate` namespace;
- accepted Phase 5 paths must not be modified by candidate generation;
- generated outputs must remain ignored unless a later publication/release
  decision explicitly annexes or tracks them;
- compact tracked manifests must summarize row counts, checksums, commands,
  source artifacts, and caveats;
- tracked planning artifacts must contain no personal local paths;
- Matrix Builder and runtime outputs must remain out of scope until XML
  readiness passes; and
- Phase 5 remains the accepted teaching baseline until replacement QA passes.

## `.gitignore` Updates

P11.1c adds explicit ignore rules for the MP11 candidate model-input bundle and
candidate Patchworks runtime generated-output subdirectories:

- `data/mp11_model_input_bundle/`
- `models/tfl6_patchworks_model_mp11_candidate/blocks/`
- `models/tfl6_patchworks_model_mp11_candidate/tracks/`
- `models/tfl6_patchworks_model_mp11_candidate/patchworksLog.csv`
- `models/tfl6_patchworks_model_mp11_candidate/analysis/p*/`
- `models/tfl6_patchworks_model_mp11_candidate/analysis/headless_runs/`

The existing repository ignore rules already cover `runtime/`, `output/`,
`plots/`, `releases/`, and `docs/_build/`.

## Next Step

P11.1d should define the promotion gates and stop conditions that decide
whether P11.2 may unlock candidate model-input generation in P11.3.
