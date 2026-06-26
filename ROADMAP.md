# Roadmap

## Phase 1: Bootstrap Repository and Build Plan (`#4`)

- [x] P1.1 Create the standalone `femic-tfl6-instance` repository scaffold.
  - [x] P1.1a Initialize the FEMIC instance skeleton.
  - [x] P1.1b Add modelwright-style workflow surfaces:
    `AGENTS.md`, `ROADMAP.md`, `CHANGE_LOG.md`, and `planning/`.
  - [x] P1.1c Add the uploaded AOI, LU, and FSP source payloads under stable
    lowercase tracked paths.
- [x] P1.2 Inspect and normalize source payloads (`#1`).
  - [x] P1.2a Unzip and inspect the NICF FSP amendment spatial payload.
  - [x] P1.2b Identify the authoritative AOI layer, geometry type, CRS, and
    expected area.
  - [x] P1.2c Inspect the LU clip payload and identify the three relevant LU
    boundaries referenced by the FSP.
  - [x] P1.2d Decide which extracted layers become tracked canonical source
    files and which remain regenerated scratch.
- [x] P1.3 Define the first K3Z-to-NICF adaptation contract (`#3`).
  - [x] P1.3a Compare K3Z config, model-input bundle, docs, and Patchworks
    package structure against the NICF FSP requirements.
  - [x] P1.3b Define the first `run_profile.tfl6.yaml` boundary after AOI
    extraction.
  - [x] P1.3c Identify which K3Z teaching assumptions can carry forward and
    which need explicit FRST 558 review.
  - [x] P1.3d Identify the minimum source-derived model-input surfaces needed
    before Patchworks runtime-package work.
  - [x] P1.3e Record the accepted adaptation boundary and keep implementation
    in follow-on tasks.
- [x] P1.4 Split model-design work into follow-on issues (`#2`).
  - [x] P1.4a Open a cedar-signal design issue covering Cw cultural reserve,
    utility-pole-grade products, treatments, yield curves, accounts, and
    reporting outputs (`#8`).
  - [x] P1.4b Open a K3Z expansion candidate-area issue covering unallocated
    candidate-area pool construction, productivity screening, and AAC uplift
    constraints (`#9`).
  - [x] P1.4c Open a Patchworks runtime-package issue once source normalization
    and model-design boundaries are accepted (`#10`).
- [x] P1.5 Materialize 2025 VRI source datasets for NICF base inventory (`#5`).
  - [x] P1.5a Record official 2025 R1 and VDYP7 polygon/layer package metadata.
  - [x] P1.5b Materialize the 2025 provincial source packages under the
    accepted `external/femic-public-data/data/bc/vri/2025/` convention.
  - [x] P1.5c Record file size, checksum, read-smoke, CRS, and layer-name
    evidence for both materialized packages.
  - [x] P1.5d Record DataLad/git-annex/public-data publication status and the
    downstream extraction handoff to the accepted active AOI issue, then publish
    any missing remote keys before closing P1.5.
- [x] P1.6 Pivot active AOI to TFL 6 and clip 2025 VRI inputs (`#6`).
  - [x] P1.6a Fetch and normalize the authoritative TFL 6 boundary from
    `WHSE_ADMIN_BOUNDARIES.FADM_TFL`.
  - [x] P1.6b Clip the 2025 VRI R1 polygon source to TFL 6 and record geometry
    QA.
  - [x] P1.6c Filter the 2025 VDYP7 polygon and layer tables to the TFL 6
    feature-id set and verify key integrity.
  - [x] P1.6d Record the accepted TFL 6 input-layer manifest and mark the
    original FDU 1/2/3 AOI as superseded for active model extraction.
- [x] P1.7 Plan TFL 6 source-layer and THLB netdown recipes from 2011 documents
  (`#7`).
  - [x] P1.7a Add/verify local source copies of the TFL 6 Management Plan 10 and
    information package PDFs, plus the broader TFL 6 reference corpus index.
  - [x] P1.7b Review the 2011 documents for land-base, source-layer, yield, and
    THLB netdown assumptions.
  - [x] P1.7b1 Record the ordered Management Plan 10 Table 4 THLB netdown
    backbone in `planning/tfl6_thlb_netdown_steps.md`, including tentative
    `GLB -> AFLB -> LHLB -> THLB` mapping, cumulative benchmarks, and
    per-step input-layer/GIS-operation readiness notes.
  - [x] P1.7b2 Scrape post-2011 TFL 6 instrument links and record boundary
    reconciliation evidence in
    `planning/tfl6_instrument_boundary_reconciliation.md`.
  - [x] P1.7b3 Scale MP10 Table 4 values to provisional current-AOI validation
    targets in `planning/tfl6_adjusted_thlb_benchmarks.md` and
    `planning/tfl6_adjusted_thlb_benchmarks.json`.
  - [x] P1.7c Separate TSA29 workflow carry-forward assumptions from
    TFL/general-FMU adaptation gaps.
  - [x] P1.7d Draft source-layer and THLB netdown recipe skeletons or planning
    tables without executing recipes.
- [x] P1.8 Plan next roadmap phases and issue tree (`#11`).
  - [x] P1.8a Draft proposed Phase 2 through at least Phase 5 sections in this
    roadmap.
  - [x] P1.8b Create one GitHub parent issue per proposed phase.
  - [x] P1.8c Create linked child task issues for the first executable tasks in
    each proposed phase.
  - [x] P1.8d Record dependency order across source-layer/THLB work, cedar
    design, expansion design, model-input generation, Patchworks runtime build,
    QA/publication, and teaching docs.
  - [x] P1.8e Place existing follow-on issues `#8`, `#9`, and `#10` into the
    planned phase structure or explicitly defer them.

## Phase 2: Reviewed Source Layers and THLB Netdown (`#12`)

Goal: turn the TFL 6 source-layer and THLB planning surfaces into reviewed,
executable FEMIC source-layer and netdown recipes before model-input generation
starts.

- [x] P2.1 Resolve and materialize public/reference source layers needed by the
  TFL 6 THLB skeleton (`#16`).
- [x] P2.1a Design operability netdown proxy and sensitivity lane (`#20`).
- [x] P2.2 Profile accepted 2025 R1 and VDYP7 fields for non-forest,
  non-productive, deciduous-leading, productivity, and join-key assumptions
  (`#22`).
  - [x] P2.2a Record accepted input schema profile, area surface, and
    R1/VDYP7 join coverage in `planning/tfl6_r1_vdyp_field_profile.md`.
  - [x] P2.2b Draft candidate field mappings and gross-area diagnostics for
    non-forest, non-productive, deciduous-leading, productivity, and
    operability-proxy review without accepting executable recipe logic.
  - [x] P2.2c Review/accept or revise the candidate mappings and record the
    short field-mapping handoff contract for P2.3.
- [x] P2.3 Define reviewed current-AOI source-layer recipe contracts under the
  future TFL/general-FMU recipe path (`#23`).
  - [x] P2.3a Open and link the child issue under Phase 2 parent `#12`.
  - [x] P2.3b Draft the first source-layer recipe-contract table in
    `planning/tfl6_source_layer_recipe_contracts.md` without creating
    executable recipe YAML.
  - [x] P2.3c Review and revise the contract table into the accepted P2.4
    handoff.
- [x] P2.4 Implement and smoke-test the first executable THLB netdown recipe
  lane against the accepted TFL 6 input surfaces (`#24`).
  - [x] P2.4a Open and link the child issue under Phase 2 parent `#12`.
  - [x] P2.4b Draft the first smoke-lane plan in
    `planning/tfl6_thlb_smoke_lane_plan.md` without creating recipe YAML or
    executing THLB netdown.
  - [x] P2.4c Create the first recipe YAML scaffold under the accepted
    `config/tsr/` convention without executing it.
  - [x] P2.4d Validate the scaffold and record the exact bounded smoke-run
    command, stop-line, outputs, and acceptance checks.
  - [x] P2.4e Execute the first bounded smoke run and inspect checkpoint, audit,
    status, and benchmark/tolerance artifacts.
- [x] P2.5 Compare GLB/AFLB/LHLB/THLB milestones against the adjusted
  current-AOI benchmark targets and record accepted teaching tolerances (`#25`).
  The accepted tolerance lock is recorded in
  `planning/tfl6_thlb_benchmark_tolerance.md`.
- [x] P2.6 Close out the Phase 2 branch/PR lifecycle before starting Phase 3
  implementation (`#26`).
  - [x] P2.6a Add Phase 2 THLB Sphinx documentation covering design rationale,
    caveats, benchmark tolerance, and reproducibility audit trail.
  - [x] P2.6b Reconcile and merge the Phase 2 closeout PR.

## Phase 3: Model Design Assumptions (`#13`)

Goal: define the reviewed model-design assumptions that depend on the accepted
source-layer and THLB surfaces, without compiling a Patchworks package.

- [x] P3.3 Define TFL 6 AU, yield-curve, and treatment-eligibility contract
  (`#28`) before model-input bundle generation.
  Priority note: P3.3 is listed first because the AU/yield contract is now the
  top Phase 3 dependency. The `P3.3` identifier is retained to preserve the
  existing issue/comment/commit audit trail.
  - [x] P3.3a Add the first AU/yield-curve planning contract in
    `planning/tfl6_au_yield_curve_contract.md`.
  - [x] P3.3b Review and lock the static AU identity, legacy MP10 TIPSY
    parameter extraction boundary, curve-lane assumptions, and
    operability/treatment-eligibility interaction.
- [x] P3.4 Build and QA actual TFL 6 yield curves (`#29`) before Phase 4
  model-input bundle generation.
  - [x] P3.4a Scrape MP10 Tables 27, 28, and 29 into a reviewed TIPSY
    parameter library.
  - [x] P3.4b Compile the first static TFL 6 AU/stratum universe and review
    plots from accepted R1/VDYP source inputs, without writing the model-input
    bundle.
  - [x] P3.4c Crosswalk static TFL 6 AUs to reviewed TIPSY parameter rows or
    explicit fallbacks.
  - [x] P3.4d Generate and QA natural/untreated VDYP curves for the selected
    top-area AU set using the shared `smoothed_bin_pchip` first-growth
    selector, with selected-AU L/M/H comparison plots, fit-diagnostic plots,
    and a lexicographic remap audit for non-selected AU bins.
  - [x] P3.4e Generate and QA treated/managed BatchTIPSY curves from the
    reviewed TIPSY parameter crosswalk.
    - [x] P3.4e1 Emit the selected-AU BTC handoff as `data/03_input-tfl6.csv`
      with curve-ID mapping and translation-policy manifest.
    - [x] P3.4e2 Run BTC/BatchTIPSY from the `tfl6` handoff, parse
      `04_output-tfl6.csv`, and build treated/managed curve QA overlays.
  - [x] P3.4f Review selected-set natural-curve shape diagnostics and document
    that the current VDYP smoothing/tail behavior is good enough to proceed
    with the rest of Phase 3, while reserving a later optional revisit before
    final model-input bundle lock.
- [x] P3.5 Define TFL 6 treatment options (`#30`) before transition logic and
  Phase 4 model-input bundle generation.
  - [x] P3.5a Define treatment IDs, labels, eligibility filters, products,
    accounts, and reporting hooks.
  - [x] P3.5b Verify natural/treated curve provenance remains separate from
    managed/unmanaged treatment eligibility.
  - [x] P3.5c Lock any deferred treatment semantics with explicit blockers or
    review needs.
- [x] P3.6 Define TFL 6 state-transition logic (`#31`) before Phase 4
  model-input bundle generation.
  - [x] P3.6a Define stand-state classes for initial, managed, unmanaged,
    retained, regenerated, and deferred/special teaching states.
  - [x] P3.6b Define transitions for base harvest, managed regeneration,
    retention/unmanaged movement, existing managed/natural origin handling,
    and operability-driven eligibility changes.
  - [x] P3.6c Verify transitions consume reviewed treatment options from P3.5
    without redefining treatment semantics.
  - [x] P3.6d Record cedar and expansion hook points without completing those
    detail lanes.
  - [x] P3.6e Lock deferred transition semantics with explicit blockers or
    review needs.
- [x] P3.1 Complete cedar-signal design (`#8`) for Cw cultural reserve,
  utility-pole-grade products, treatments, yield implications, accounts, and
  reporting outputs.
  Priority note: P3.1 remains open with P3.1a already completed, but cedar
  details now sit downstream of AU, yield-curve, treatment-option, and
  transition-logic locks.
  - [x] P3.1a Record the first cedar evidence/design note in
    `planning/tfl6_cedar_signal_design.md` without generating model inputs.
  - [x] P3.1b Review and lock cedar source fields, derived signals, and
    provisional unresolved assumptions.
  - [x] P3.1c Define Patchworks-facing cedar products, accounts, treatment
    hooks, stakeholder-comparison signals, and report requirements for the
    first model-input bundle, including student-facing KPI families for
    comparing cedar/community outcomes against broader TFL 6 fibre supply,
    value, and delivered-cost proxies.
- [x] P3.2 Complete embedded NICF/K3Z identity and expansion candidate-area
  design (`#9`) for group accounts, matching targets, reports, unallocated
  candidate pools, productivity screening, and AAC uplift constraints.
  Priority note: P3.2 remains open but sits downstream of the base AU, yield,
  treatment, and transition contract lanes. It must preserve the embedded
  K3Z/NICF core identity and outside-AOI expansion-candidate identities inside
  the larger teaching model without redefining AUs.
  - [x] P3.2a Record the embedded identity contract in
    `planning/tfl6_nicf_embedded_identity.md`.
  - [x] P3.2b Define accepted K3Z/NICF core AOI overlay identity inside the
    TFL 6 model area.
  - [x] P3.2c Define outside-AOI expansion candidate, rejected-candidate, and
    current-AOI TFL 6 remainder identity classes and source/provenance fields.
  - [x] P3.2d Define Patchworks group accounts, matching targets, scenario
    toggles, and reports needed to track K3Z/NICF core and expansion
    candidates separately, including WFP-facing fibre supply, value, and
    delivered-cost tradeoff signals where available and multi-perspective KPI
    outputs for student scenario projects.
  - [x] P3.2e Lock dependency handoff to P3.7/P4.1 so embedded identity fields
    appear in the model-input bundle without changing AU identity.
- [ ] P3.7 Update the TFL 6 run-profile/model-input contract with reviewed
  design decisions and explicit rejected/deferred assumptions.

## Proposed Phase 4: Model Inputs and Patchworks Runtime Package (`#14`)

Goal: generate, inspect, and QA the first runnable TFL 6 Patchworks teaching
package only after the reviewed source-layer, THLB, and model-design contracts
exist.

- [ ] P4.1 Build the reviewed model-input bundle from accepted TFL 6 source
  layers, THLB outputs, and model-design assumptions (`#17`).
- [ ] P4.2 Generate ForestModel/XML and inspect the semantics that affect
  Patchworks treatment eligibility, curve provenance, products, accounts, and
  targets.
- [ ] P4.3 Execute Matrix Builder and QA tracks, features, accounts,
  protoaccounts, products, targets, and reports.
- [ ] P4.4 Complete Patchworks runtime-package build/QA (`#10`) with
  representative launch and scenario-smoke checks.

## Proposed Phase 5: Publication, Teaching Docs, and Release QA (`#15`)

Goal: make the teaching instance reproducible and usable by students/instructors
after the runtime package has passed direct artifact and launch smoke checks.

- [ ] P5.1 Decide which compact runtime artifacts are tracked, annexed,
  published, or regenerated (`#18`).
- [ ] P5.2 Publish required data/runtime artifacts through the accepted FEMIC
  public-data workflow and prove fresh-environment materialization.
- [ ] P5.3 Build full Sphinx teaching documentation (`#21`) modeled on the
  `femic-k3z-instance` and `femic-tsa29-instance` documentation surfaces,
  including quickstart instructions, rebuild workflow, source-data provenance,
  THLB validation notes, scenario teaching workflows, advanced student
  challenges, multi-perspective stakeholder/KPI scenario interpretation, known
  limitations, and warning-clean Sphinx build evidence.
- [ ] P5.4 Run final release QA across source materialization, instance rebuild,
  Patchworks launch smoke, and documentation checks.

## Dependency Order

The next phases must proceed in this order unless the maintainer explicitly
approves a narrower independent slice:

1. **Source-layer and THLB foundation**: Phase 2 (`#12`) resolves/materializes
   source layers, profiles accepted 2025 VRI and VDYP7 fields, defines reviewed
   source-layer recipe contracts, executes the first THLB netdown lane, and
   records GLB/AFLB/LHLB/THLB benchmark tolerances before any model-input
   generation starts.
2. **Model-design assumptions**: Phase 3 (`#13`) depends on the accepted Phase 2
   source-layer/THLB contracts. Cedar design (`#8`) and expansion candidate-area
   design (`#9`) belong in this phase because they decide modeling semantics,
   treatment/product/account/reporting behavior, and AAC-uplift assumptions
   rather than source extraction mechanics.
3. **Model-input generation**: Phase 4 (`#14`) starts only after Phase 2 source
   and THLB outputs plus Phase 3 model-design assumptions are reviewed. Phase
   3 must explicitly lock the AU/yield contract (`#28`), actual yield-curve
   build and QA (`#29`), treatment options (`#30`), and state-transition logic
   (`#31`) before P4.1 (`#17`) builds the model-input bundle from those
   accepted contracts.
4. **Patchworks runtime build and QA**: ForestModel/XML generation, Matrix
   Builder execution, runtime-package assembly, and runtime-package QA remain
   Phase 4 work after P4.1. Runtime-package follow-on `#10` is downstream of
   accepted source layers, THLB outputs, cedar design, expansion design, and
   model-input bundle construction.
5. **Publication and teaching release**: Phase 5 (`#15`) starts after the
   runtime package passes direct artifact and launch smoke. P5.1 (`#18`) first
   decides artifact publication policy, then later Phase 5 tasks publish
   materializable artifacts, build full K3Z/TSA29-style Sphinx teaching docs,
   and run final release QA.

Guardrail: source extraction, THLB execution, cedar/expansion implementation,
model-input generation, XML/Matrix Builder work, runtime packaging,
publication, and teaching documentation should not be bundled into one
"next slice" unless the maintainer explicitly broadens scope.

## Follow-on Issue Placement

The Phase 1 follow-on issues are placed into the future roadmap as follows:

- Cedar-signal design `#8` is Phase 3 model-design work and is listed as P3.1
  under Phase 3 parent `#13`.
- Expansion candidate-area design `#9` is Phase 3 model-design work and is
  listed as P3.2 under Phase 3 parent `#13`.
- Patchworks runtime-package build/QA `#10` is Phase 4 runtime-package work and
  is listed as P4.4 under Phase 4 parent `#14`, downstream of P4.1 model-input
  bundle construction `#17`.

## Current Next Steps

1. Phase 2 is closed. The instance `main` branch contains the Phase 2
   source-layer, THLB smoke, benchmark-tolerance, and Sphinx audit-trail
   surfaces; the parent FEMIC submodule pointer has been updated to the merged
   closeout commit.
2. Continue Phase 3 on branch `feature/p3-model-design-assumptions`. P3.3
   through P3.6 are complete: AU identity, untreated VDYP curves, treated
   BatchTIPSY curves, treatment options, and state-transition logic are locked
   for current design purposes. P3.4 still carries a non-blocking deferred
   option to revisit VDYP smoothing/tail constraints before the final Phase 4
   model-input bundle lock.
3. P3.1b is complete. Cedar source fields and derived signal definitions are
   locked in `planning/tfl6_cedar_signal_design.md` using the accepted
   `planning/tfl6_stand_to_au_review.csv` surface. P3.1b accepts `CW`/`YC`
   leading and component signals, the `>= 20%` cedar-present threshold, and the
   `>= 141` age proxy for `old_cedar`. It leaves `large_cedar_proxy`,
   utility-pole thresholds, cedar-specific treatments, and cedar-specific
   products/accounts to P3.1c.
4. P3.1c and P3.1 are complete. The cedar design lane now defines
   Patchworks-facing product hooks, feature/account families, report/target
   families, treatment-hook boundaries, yield-curve boundaries, and Phase 4
   handoff fields in `planning/tfl6_cedar_signal_design.md`. The first bundle
   should carry cedar reporting surfaces, but it must not create cedar-specific
   base treatments, hard cedar reserve targets, utility-pole grade claims, or
   cedar-only yield-curve families.
5. P3.2b is complete. The accepted K3Z/NICF core source is the original K3Z
   tenure boundary from `external/femic-k3z-instance`, but non-mutating overlay
   diagnostics show that the current FADM-derived TFL 6 AOI intersects only
   `0.072 ha` of that `2391.511 ha` K3Z tenure. The first bundle must not
   silently relabel the broader FDU 1/2/3 planning context as
   `nicf_k3z_core`; K3Z core should be treated as a source/provenance identity
   and likely external/reference carve-out under the current TFL 6 boundary.
6. P3.2c is complete and corrected after maintainer clarification. Expansion
   candidates are not selected from current-AOI TFL 6 stands; they come from
   proximal/adjacent public forested land outside the current TFL 6 AOI. The
   embedded identity contract now defines `wfp_tfl6_remainder`,
   `nicf_expansion_candidate`, `nicf_expansion_rejected`,
   `nicf_expansion_pool_unreviewed`, and `nicf_k3z_core_reference`, plus the
   outside-AOI source/provenance fields and first `expansion_screen_status`
   vocabulary needed for Phase 4 handoff.
7. P3.2d is complete. The embedded identity contract now lists the Patchworks
   group dimensions, account families, matching targets, scenario toggles, and
   reports needed to compare K3Z/NICF reference identity, outside-AOI expansion
   candidates, rejected/unreviewed pools, WFP TFL 6 remainder, and whole-model
   teaching outcomes without changing AU identity.
8. P3.2e and P3.2 are complete. The embedded identity contract now hands
   required field families and dependency boundaries to P3.7/P4.1 so
   current-AOI TFL 6 base geography, K3Z reference identity, outside-AOI
   expansion candidates, rejected/unreviewed pools, and Patchworks comparison
   surfaces can enter the model-input contract without changing AU identity.
9. The next bounded tranche is P3.7: reconcile the TFL 6 run-profile and
   model-input contract with all reviewed Phase 3 design decisions. Phase 4
   remains blocked until P3.7 is complete or explicitly narrowed by the
   maintainer.
