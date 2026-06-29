# TFL 6 MP11 P11.2 Candidate-Scaffold Decisions

## Purpose

This P11.2 note resolves the hard promotion-readiness blockers for a
candidate-only MP11 model-input scaffold. It does not accept the scaffold as a
runtime model, release payload, or MP11-equivalent forecast.

The pre-resolution P11.2a dry run reported `11` gates, `3` blocked hard gates,
`2` deferred soft gates, `6` passing gates, and `0` missing source artifacts.
This note records the decisions that allow P11.3 to build only a candidate
manifest, not model-input tables, ForestModel XML, Matrix Builder outputs, or
Patchworks runtime artifacts.

## Source And THLB Candidate Contract

P11.3 may use the P9RF resultant-fragment lane as the candidate source/THLB
contract for manifest planning only.

Candidate roles:

| Candidate role | P11.3 source |
| --- | --- |
| stand universe | P9RF resultant-fragment checkpoint geometry |
| THLB/NTHLB state | P9RF retained/excluded status by resultant fragment |
| retained area | P9RF net retained area after ordered MP11 Table 12 steps |
| managed/unmanaged area | P9RF THLB/NTHLB classification with caveat fields |
| group-field source | P9RF step/status labels and public proxy context |

Required P11.3 caveats:

- the P9RF current THLB checkpoint is `122,763.421 ha`, while the MP11 current
  THLB comparison target is `120,099.000 ha`;
- proposed WHA and uneconomic deductions remain review-required or unavailable;
- archaeological sites, research sites, and TUS-zone cultural features remain
  sensitive-source exclusions;
- big-tree reserves and karst remain deferred pending public source review;
- future stand-level reserves remain a reviewed proxy candidate, not final
  WFP model equivalence; and
- P11.3 must keep these caveats as explicit candidate manifest fields or QA
  notes rather than hiding them in generated tables.

This resolves `p11_gate_02_source_thlb` only for candidate-manifest work.
Runtime, release, and final MP11 replacement acceptance remain later gates.

## Rule-Field Candidate Contract

P11.3 may use a conservative rule scaffold that keeps MP11 rule gaps explicit:

| Rule family | Candidate treatment |
| --- | --- |
| treatment defaults | reuse Phase 5 treatment defaults where MP11 rule contracts are not accepted |
| transition defaults | reuse Phase 5 transition defaults where MP11 transitions are not accepted |
| minimum harvest age | defer as null, comparison, or QA metadata until a reviewed MHA library exists |
| harvest system | defer stand-level assignments; aggregate MP11 percentages remain comparison targets only |
| helicopter economic operability | defer to sensitivity/proxy design; do not infer WFP cost/access model |
| scenario policy | defer to runtime/scenario phases; do not encode Patchworks objective weights |

P11.3 may include rule-status fields only when they are explicitly marked as
`reuse_phase5_default`, `deferred`, `comparison_target`, `proxy_candidate`, or
`unavailable_non_public`. Those fields do not become accepted model inputs.

This resolves `p11_gate_06_rule_contracts` only for candidate-manifest work.
No MP11 MHA, harvest-system, helicopter economic-operability, or scenario rule
is accepted for runtime use by this decision.

## P11.3 Unlock Boundary

P11.3 may build `planning/tfl6_mp11_model_input_candidate_manifest.{csv,json,md}`
and may inspect the candidate output roots named in
`planning/tfl6_mp11_phase11_artifact_layout.md`.

P11.3 must still not write:

- `data/mp11_model_input_bundle/` generated tables unless its own issue
  explicitly moves from manifest to generated scaffold;
- ForestModel XML or fragments;
- Matrix Builder tracks;
- Patchworks runtime blocks, topology, saved stages, or release archives.

Phase 5 remains the accepted teaching/runtime baseline until a future MP11
candidate passes model-input, XML, Matrix Builder, Patchworks runtime,
scenario, documentation, and release QA.
