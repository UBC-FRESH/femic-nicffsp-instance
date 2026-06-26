# TFL 6 Treatment Option Contract

## Purpose

This note defines the Phase 3 treatment-option vocabulary for the first TFL 6
Patchworks teaching model. It is a design contract for P3.5 only. It does not
define state transitions, build model-input tables, generate ForestModel XML,
run Matrix Builder, or assemble a Patchworks runtime package.

P3.6 must consume this vocabulary when transition logic is designed. Treatment
semantics should not be redefined in the transition lane.

## Accepted Base Treatment Catalogue

| Treatment ID | Label | Status | Role |
| --- | --- | --- | --- |
| `grow` | Grow/no scheduled treatment | Accepted implicit state behavior | Represents stands that remain unscheduled in a period. This is a model state path, not a harvest action. |
| `cc` | Clearcut/final harvest | Accepted base scheduled treatment | Primary timber-harvest treatment for eligible managed THLB stands. |
| `regen_plant` | Planted regeneration | Accepted post-harvest transition target | Assigns harvested managed stands to the reviewed treated/managed TIPSY curve lane. Transition timing is P3.6 work. |
| `regen_natural` | Natural regeneration | Deferred/fallback transition target | Reserved for cases where source evidence or scenario design requires natural regeneration after harvest. Not a base scheduling action in this slice. |

The first model should stay deliberately small: one base harvest action and
explicit regeneration targets. Commercial thinning, pre-commercial thinning,
fertilization, cedar-specific treatments, and NICF expansion scenario actions
are not accepted base treatments yet.

## Eligibility Filters

`cc` is eligible only where all of the following are true in the future
model-input bundle:

- the stand is inside the accepted TFL 6 AOI;
- the stand is in the active THLB after the reviewed Phase 2 netdown;
- the stand is assigned `managed` treatment eligibility;
- the stand is not in a full-retention, reserve, non-THLB, or otherwise
  unschedulable status;
- the stand passes the accepted operability/yarding/slope eligibility filter
  for the selected scenario;
- the stand has a valid static AU assignment and a usable yield curve;
- the stand has reached the minimum harvest-age / merchantability rule that
  P3.6 will define; and
- any group-level constraints for NICF core, expansion candidates, WFP
  remainder, cedar signals, visual quality, or other reporting groups allow
  the treatment in that scenario.

`grow` is available to all stands with a valid state and curve assignment. It
does not change treatment eligibility or curve provenance.

`regen_plant` and `regen_natural` are not independent scheduled treatments.
They are transition targets after harvest. P3.6 must define the timing,
origin/provenance assignment, and curve-family selection rules.

## Curve and Eligibility Semantics

The treatment catalogue preserves FEMIC/Patchworks semantics:

- `managed` / `unmanaged` means treatment eligibility only;
- `natural` / `treated` means curve provenance only;
- a natural-origin stand can still be treatment eligible if it is in managed
  THLB;
- an unmanaged stand can still carry a treated-origin curve if the source
  history supports it; and
- retention, operability, cedar signals, NICF identity, and expansion status
  are stand/group/scenario attributes, not AU identity fields and not curve
  provenance fields.

The post-harvest default for managed harvested stands is `regen_plant`, which
uses the reviewed TFL 6 treated/managed BatchTIPSY curve lane. That does not
mean all `managed` stands are already `treated`; it only defines the curve lane
after a managed regeneration transition.

## Product Hooks

The first P4 model-input bundle should expose the product hooks needed for
basic scheduling and teaching reports:

- total merchantable volume;
- available species or species-group volume where supported by the accepted
  curve tables;
- cedar volume/reporting hooks where cedar signal design has accepted fields;
- optional log-grade or utility-pole hooks only after P3.1 cedar product design
  resolves their source fields and confidence level; and
- harvested area by treatment, AU, source group, and stakeholder/reporting
  group.

P3.5 does not assign product equations or Patchworks account names. It defines
the treatment-side requirements P4 must satisfy when tables/XML are generated.

## Account and Reporting Hooks

The base catalogue must support reporting by:

- whole TFL 6;
- THLB and non-THLB;
- managed and unmanaged treatment eligibility;
- natural and treated curve provenance;
- NICF/K3Z core area;
- NICF expansion candidates and rejected candidates;
- WFP/TFL 6 remainder;
- cedar signal classes; and
- operability or slope-proxy sensitivity classes.

Those hooks let student projects compare stakeholder perspectives without
making cedar or NICF expansion treatments part of the first base treatment
vocabulary.

## Deferred Treatments

The following remain explicit deferred design items:

| Treatment | Reason deferred | Required before activation |
| --- | --- | --- |
| Pre-commercial thinning | Not needed for the first runnable base model and not yet linked to reviewed TFL 6 response curves. | Stand-age/stocking eligibility, response curve logic, and teaching scenario purpose. |
| Commercial thinning | Potentially useful for advanced scenarios but not part of the MP10 base-case implementation target. | Merchantability thresholds, removal fractions, residual-stand transitions, and products. |
| Fertilization | Historically important in TFL 6 and already embedded in MP10 TIPSY parameter evidence, but not yet a standalone scheduling action. | Clear separation between yield-curve assumptions already baked into TIPSY and optional scheduled fertilization scenarios. |
| Cedar retention or cedar-product treatments | Stakeholder relevant but belongs to the cedar design lane. | P3.1 cedar signal, product, cultural reserve, treatment, and reporting decisions. |
| NICF expansion scenario actions | Stakeholder relevant but belongs to embedded identity and scenario-design lanes. | P3.2 identity fields and later scenario/account/target design. |

Deferred treatment entries are not rejected forever. They are blocked from the
base catalogue until their eligibility, response, product, account, and
teaching-purpose contracts are explicit.

## P3.6 Handoff

P3.6 should define:

- initial state classes;
- minimum harvest-age or merchantability rules for `cc`;
- transitions from eligible pre-harvest state to harvested/regenerated state;
- whether `regen_plant` or `regen_natural` applies after each harvest context;
- how managed/unmanaged eligibility changes, if at all, after retention or
  scenario filters;
- how operability sensitivity moves stands in or out of `cc` eligibility
  without redefining AUs; and
- where cedar and NICF expansion hook points enter state, account, and report
  logic without becoming base treatment semantics.

## Acceptance Checks

- No accepted treatment ID encodes AU identity, stand age at time 0, THLB
  status, operability class, cedar status, or NICF expansion status.
- No accepted treatment rule infers `managed = treated` or
  `unmanaged = natural`.
- The base scheduled treatment set is small enough to implement and inspect in
  the first Patchworks package.
- Every deferred treatment has a documented blocker or review need.
