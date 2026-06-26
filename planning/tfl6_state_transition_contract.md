# TFL 6 State-Transition Contract

## Purpose

This note defines the Phase 3 state-transition contract for the first TFL 6
Patchworks teaching model. P3.6a defines the state classes and semantic fields
that P3.6b transition rules must consume. It does not build the model-input
bundle, generate ForestModel XML, run Matrix Builder, or assemble a Patchworks
runtime package.

The governing treatment vocabulary is
`planning/tfl6_treatment_option_contract.md`. Transition logic must consume
that vocabulary without redefining treatment semantics.

## Core State Fields

The first model-input bundle should keep these state dimensions separate:

| Field | Meaning | Examples |
| --- | --- | --- |
| `IFM` | Treatment eligibility only. | `managed`, `unmanaged` |
| `ORIGIN` | Curve provenance only. | `natural`, `treated` |
| `SILV_STATE` | Silviculture / state-path label. | `baseline`, `cc_planted`, `ct_candidate`, `fert_candidate`, `retained` |
| `RETENTION` | Retention fraction or retention class. | numeric fraction or reviewed class |
| `HARVEST_SYSTEM` | Operational harvest-system class. | `ground_based`, `cable`, `heli` |
| `TFL6_GROUP` | Spatial/reporting group identity. | `nicf_k3z_core`, `nicf_expansion_candidate`, `wfp_tfl6_remainder` |

These fields are not AU identity fields. AUs remain static BEC/phase/species/SI
families. Treatment eligibility, origin, harvest system, retention, cedar
signals, and NICF/expansion groups are stand attributes or scenario/reporting
attributes.

## Required State Classes

| State ID | Field expression | Meaning | Treatment eligibility |
| --- | --- | --- | --- |
| `initial_managed_natural` | `IFM=managed`, `ORIGIN=natural`, `SILV_STATE=baseline` | Existing natural-origin stand in managed THLB. | Eligible for `clearcut_and_plant` when age/merchantability, operability, harvest system, retention, and group constraints pass. |
| `initial_managed_treated` | `IFM=managed`, `ORIGIN=treated`, `SILV_STATE=baseline` | Existing treated-origin stand in managed THLB. | Eligible for `clearcut_and_plant`; CT/fertilization only where K3Z/NICF group gates and future response rules pass. |
| `initial_unmanaged_natural` | `IFM=unmanaged`, `ORIGIN=natural`, `SILV_STATE=baseline` | Natural-origin stand outside treatment eligibility. | Not eligible for scheduled treatments. |
| `initial_unmanaged_treated` | `IFM=unmanaged`, `ORIGIN=treated`, `SILV_STATE=baseline` | Treated-origin stand outside treatment eligibility. | Not eligible for scheduled treatments, but keeps treated curve provenance if source history supports it. |
| `retained_unmanaged` | `IFM=unmanaged`, `SILV_STATE=retained` | Area moved or held outside scheduling by retention/reserve/non-THLB rules. | Not eligible for scheduled treatments. |
| `post_clearcut_planted` | `IFM=managed`, `ORIGIN=treated`, `SILV_STATE=cc_planted` | Post-`clearcut_and_plant` regenerated stand on the treated/managed curve lane. | Future eligibility depends on age/merchantability and scenario rules. |
| `ct_candidate` | `IFM=managed`, `SILV_STATE=ct_candidate` | Optional candidate state for NICF-focused CT scenario logic. | Only inside `nicf_k3z_core` or accepted future `nicf_expansion_candidate` groups after reviewed CT rules exist. |
| `fert_candidate` | `IFM=managed`, `SILV_STATE=fert_candidate` | Optional candidate state for NICF-focused fertilization scenario logic. | Only inside `nicf_k3z_core` or accepted future `nicf_expansion_candidate` groups after reviewed fertilization rules exist. |
| `deferred_special` | explicit reviewed value | Placeholder for future cedar or expansion special states. | Not schedulable until a later reviewed lane defines the treatment/transition semantics. |

The table defines stable state IDs for planning. Phase 4 may encode the same
contract with separate Patchworks track fields rather than one concatenated
state string, but the semantics must remain equivalent.

## Semantic Rules

- `managed` / `unmanaged` is treatment eligibility only.
- `natural` / `treated` is curve provenance only.
- `SILV_STATE` records the state path, not the AU identity.
- `HARVEST_SYSTEM` is a TFL-wide operational attribute, not an AU or curve
  identity.
- A natural-origin managed stand can be harvested and transition to a
  treated-origin planted state.
- An unmanaged stand may carry a treated-origin curve if source history
  supports it, but it remains unavailable for scheduled treatments.
- Retention, non-THLB, reserves, and scenario exclusions should move or hold
  area in an unmanaged/retained state without changing the static AU.
- Operability or slope sensitivity can change eligibility for scheduling, but
  should not alter AU identity or curve provenance.

## Harvest-System Boundary

P3.6b/P4 must carry `HARVEST_SYSTEM` throughout TFL 6 with these accepted
classes:

- `ground_based`;
- `cable`; and
- `heli`.

The field should be available for:

- `clearcut_and_plant` eligibility;
- CT/fertilization eligibility where those treatments are group-gated;
- delivered-cost and harvest-system proxy accounts;
- harvest volume and area reports by system;
- operability sensitivity runs; and
- student scenario comparisons.

The field should not create separate AU IDs or separate yield-curve families by
itself.

## Transition Rows

This P3.6b table defines the reviewed transition rows for the first transition
contract. These are design rows for the Phase 4 model-input/XML builders to
consume later; they are not executable runtime outputs in this slice.

| Transition ID | Treatment / trigger | Source state | Destination state | Field changes | Eligibility gates | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `tr_grow_managed_natural` | `grow` | `initial_managed_natural` | `initial_managed_natural` | age advances; `IFM`, `ORIGIN`, `SILV_STATE`, `HARVEST_SYSTEM`, and AU unchanged | valid state and curve | No scheduled action. Natural curve provenance persists. |
| `tr_grow_managed_treated` | `grow` | `initial_managed_treated` or `post_clearcut_planted` | same source state | age advances; `IFM`, `ORIGIN`, `SILV_STATE`, `HARVEST_SYSTEM`, and AU unchanged | valid state and curve | Treated curve provenance persists. |
| `tr_grow_unmanaged` | `grow` | `initial_unmanaged_natural`, `initial_unmanaged_treated`, or `retained_unmanaged` | same source state | age advances; `IFM=unmanaged`; `ORIGIN`, `SILV_STATE`, `HARVEST_SYSTEM`, and AU unchanged | valid state and curve | No scheduled treatment eligibility is introduced. |
| `tr_clearcut_plant_natural` | `clearcut_and_plant` | `initial_managed_natural` | `post_clearcut_planted` | `ORIGIN=treated`; `SILV_STATE=cc_planted`; `IFM=managed`; age reset/regeneration delay handled in P4 implementation; AU family maps to treated curve lane | active THLB, `IFM=managed`, not retained/reserve/non-THLB, operable under scenario, assigned `HARVEST_SYSTEM`, valid AU/curve, age/merchantability rule passes, group constraints allow | Base whole-TFL 6 harvest transition. Natural-origin source can become treated-origin after planted regeneration. |
| `tr_clearcut_plant_treated` | `clearcut_and_plant` | `initial_managed_treated` or `post_clearcut_planted` | `post_clearcut_planted` | `ORIGIN=treated`; `SILV_STATE=cc_planted`; `IFM=managed`; age reset/regeneration delay handled in P4 implementation; AU family maps to treated curve lane | active THLB, `IFM=managed`, not retained/reserve/non-THLB, operable under scenario, assigned `HARVEST_SYSTEM`, valid AU/curve, age/merchantability rule passes, group constraints allow | Reharvest or harvest of existing treated-origin stands stays on treated/managed curve lane. |
| `tr_reserve_to_retained` | reserve, non-THLB, full retention, or scenario exclusion | any initial or post-treatment state | `retained_unmanaged` | `IFM=unmanaged`; `SILV_STATE=retained`; `RETENTION` set or preserved; `ORIGIN`, `HARVEST_SYSTEM`, and AU unchanged | retained/reserve/non-THLB/scenario-excluded area | Retention affects scheduling eligibility, not curve provenance or AU identity. |
| `tr_operability_mask_out` | operability or harvest-system sensitivity excludes scheduling | any managed source state | same source state with scheduling mask disabled, or `retained_unmanaged` only if the scenario explicitly models exclusion as unmanaged | no AU or `ORIGIN` change; treatment eligibility mask changes; optional `IFM=unmanaged` only under reviewed scenario rule | scenario-specific operability, slope, yarding, or heli/cable/ground availability rule | Default behavior is eligibility masking, not identity change. |
| `tr_ct_candidate_hold` | `commercial_thinning` hook | `initial_managed_treated`, `post_clearcut_planted`, or reviewed managed source state | `ct_candidate` or source state until CT rules are reviewed | no AU or `ORIGIN` change in this base contract | inside `nicf_k3z_core` or accepted future `nicf_expansion_candidate`; active THLB; `IFM=managed`; valid harvest system; reviewed CT response rules | Hook only. CT residual-state and curve behavior remain deferred. |
| `tr_fert_candidate_hold` | `fertilization` hook | `initial_managed_treated`, `post_clearcut_planted`, or reviewed managed source state | `fert_candidate` or source state until fertilization rules are reviewed | no AU or `ORIGIN` change in this base contract | inside `nicf_k3z_core` or accepted future `nicf_expansion_candidate`; active THLB; `IFM=managed`; valid harvest system; reviewed fertilization response rules | Hook only. Must not double-count fertilization already embedded in TIPSY curves. |
| `tr_cedar_expansion_hook` | cedar or NICF expansion detail lane | any applicable state | same source state or `deferred_special` only after reviewed lane defines it | no base-contract AU, `IFM`, or `ORIGIN` change | P3.1/P3.2 reviewed hook fields present | Carries future account/report hooks without implementing cedar or expansion treatment semantics. |

## Origin and Eligibility Handling

Initial `ORIGIN` is carried from source evidence into the model-input bundle.
`grow`, retention movement, operability masks, harvest-system class changes,
and reporting-group membership do not change `ORIGIN`. The only accepted base
transition that changes `ORIGIN` is `clearcut_and_plant`, which moves the
destination stand to `ORIGIN=treated` because planted regeneration uses the
reviewed treated/managed BatchTIPSY curve lane.

Initial `IFM` is derived from the accepted Phase 2 THLB/scheduling-eligibility
contract and later scenario masks. `clearcut_and_plant`, CT hooks, and
fertilization hooks require `IFM=managed`. Retention, reserves, non-THLB, and
reviewed scenario exclusions can move or hold stands in `IFM=unmanaged`.

`HARVEST_SYSTEM` must be present for scheduled treatment eligibility and should
remain available for account/reporting outputs. Changing `HARVEST_SYSTEM`
thresholds in a scenario changes eligibility and cost/reporting signals; it
does not redefine AU identity or curve provenance.

## P3.6c Treatment-Semantics Verification

This verification compares the P3.6 transition rows against the P3.5 treatment
vocabulary in `planning/tfl6_treatment_option_contract.md`.

| Check | Result | Evidence |
| --- | --- | --- |
| Transition rows use only accepted P3.5 treatment IDs/triggers. | Pass | Rows use `grow`, `clearcut_and_plant`, `commercial_thinning`, and `fertilization`. Reserve/operability/cedar-expansion rows are triggers or hook rows, not new scheduled treatment IDs. |
| `clearcut_and_plant` remains the only whole-TFL 6 base scheduled treatment. | Pass | Only `tr_clearcut_plant_natural` and `tr_clearcut_plant_treated` implement base harvest/regeneration; CT/fertilization rows are hooks only. |
| CT/fertilization remain K3Z/NICF-gated. | Pass | CT/fert hook rows require `nicf_k3z_core` or accepted future `nicf_expansion_candidate` group membership and reviewed response rules before activation. |
| Transition rows preserve `managed` / `unmanaged` as treatment eligibility. | Pass | `IFM=managed` is required for scheduled treatment rows; reserve/non-THLB/retention rows move or hold stands as `IFM=unmanaged`. |
| Transition rows preserve `natural` / `treated` as curve provenance. | Pass | `grow`, retention, operability masks, reporting groups, and harvest-system classes do not change `ORIGIN`. `clearcut_and_plant` is the only accepted base transition that changes `ORIGIN` to `treated`. |
| Harvest system remains operational/reporting context. | Pass | `HARVEST_SYSTEM` is an eligibility/account/reporting field and does not alter AU identity or curve provenance. |
| Cedar and expansion details remain deferred. | Pass | `tr_cedar_expansion_hook` carries future hook points only and does not implement cedar or expansion treatment semantics. |

P3.6c therefore accepts the transition rows as consuming the P3.5 treatment
contract without redefining treatment semantics.

## P3.6d Cedar and Expansion Hook Points

P3.6d records hook points only. It does not complete cedar design, expansion
candidate design, products, accounts, targets, or scenario toggles.

### Cedar Hooks

P3.1 owns cedar signal design. The transition contract must carry cedar fields
without making cedar a base treatment or an AU identity dimension.

Required cedar hook fields for P4 handoff:

| Hook field | Source design lane | Transition behavior |
| --- | --- | --- |
| `cedar_leading` | P3.1 | Preserve through `grow`, retention, operability masks, and `clearcut_and_plant`; may support reports/accounts. |
| `western_redcedar_leading` | P3.1 | Preserve as a reporting/product signal; no base transition semantics. |
| `yellow_cedar_leading` | P3.1 | Preserve as a reporting/product signal; no base transition semantics. |
| `cedar_present` | P3.1 | Preserve as a reporting/product signal; no base transition semantics. |
| `old_cedar` | P3.1 | Preserve for residual, reserve, and scheduled-harvest reporting; no automatic base exclusion. |
| `large_cedar_proxy` | P3.1 | Preserve only after P3.1 accepts source fields/thresholds. |
| `cedar_cultural_reserve_context` | P3.1 | Can inform reports or later scenario constraints; does not create a hidden THLB exclusion in this contract. |
| `cedar_harvest_candidate` | P3.1 | Can inform scheduled cedar reports; does not define a cedar-specific treatment here. |

Cedar hooks may affect Phase 4 accounts, products, reports, or later scenario
constraints. They must not:

- redefine static AU identity;
- change `ORIGIN` except through accepted treatment transitions;
- change `IFM` unless a later reviewed cedar scenario explicitly does so; or
- introduce cedar-specific treatments before P3.1c accepts them.

### Embedded NICF/K3Z and Expansion Hooks

P3.2 owns embedded NICF/K3Z identity and expansion-candidate design. The
transition contract must carry those identities as reporting/scenario fields,
not AU fields.

Required embedded-identity hook fields for P4 handoff:

| Hook field | Source design lane | Transition behavior |
| --- | --- | --- |
| `embedded_area_class` | P3.2 | Preserve through all base transitions; drives group reports and scenario filters. |
| `embedded_area_id` | P3.2 | Preserve for provenance and group/account traceability. |
| `is_nicf_k3z_core` | P3.2 | Gates CT/fertilization hooks with `nicf_k3z_core`; supports separate reports. |
| `is_nicf_expansion_candidate` | P3.2 | Gates future accepted expansion candidate CT/fertilization hooks; supports scenario toggles. |
| `is_nicf_expansion_rejected` | P3.2 | Preserve for rejected-pool audit/reporting; not schedulable as expansion by default. |
| `expansion_candidate_set` | P3.2 | Preserve for candidate-pool comparisons. |
| `expansion_screen_status` | P3.2 | Preserve for scenario filtering and audit. |
| `expansion_screen_reason` | P3.2 | Preserve for rejected/accepted candidate audit. |
| `expansion_scenario_group` | P3.2 | Preserve for future scenario toggles; no base transition semantics. |

Embedded identity hooks may affect group accounts, matching targets, reports,
and CT/fertilization eligibility gates. They must not:

- redefine static AU identity;
- duplicate yield curves by group membership alone;
- make NICF expansion a base treatment; or
- complete expansion-candidate scenario logic before P3.2 accepts it.

### Hook Handoff Rule

`tr_cedar_expansion_hook` remains a placeholder row. Its purpose is to ensure
Phase 4 carries the fields needed by P3.1/P3.2, while keeping the base
transition contract unchanged:

- `grow` preserves cedar and embedded-identity fields;
- `clearcut_and_plant` preserves cedar and embedded-identity fields for
  scheduled/residual reporting and moves only accepted state fields;
- retention and operability masks preserve cedar and embedded-identity fields;
- CT/fertilization hooks can use `nicf_k3z_core` and accepted future
  `nicf_expansion_candidate` fields as gates; and
- cedar/expansion treatment or scenario semantics remain deferred.

## Deferred Transition Semantics

| Deferred item | Blocker |
| --- | --- |
| CT residual-state transition | Needs reviewed age/volume eligibility, removal fraction, residual curve behavior, products, and accounts. |
| Fertilization response transition | Needs clear separation between TIPSY yield assumptions already embedded in curves and optional scheduled fertilization response logic. |
| Cedar-specific state transitions | Depends on P3.1 cedar product/cultural reserve/treatment design. |
| NICF expansion scenario transitions | Depends on P3.2 accepted expansion identity fields and later scenario design. |
| Harvest-system reassignment over time | Needs explicit scenario rule; base model treats harvest system as an initial stand-level operational attribute. |

## Acceptance Checks

- No state class redefines the P3.5 treatment vocabulary.
- No state class infers `managed = treated` or `unmanaged = natural`.
- State classes carry ground/cable/heli harvest systems as operational fields.
- State classes preserve static AU identity under age, operability, retention,
  and scenario changes.
- Transition rows are defined without starting Phase 4 model-input generation.
