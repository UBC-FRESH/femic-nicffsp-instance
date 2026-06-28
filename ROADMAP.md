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
- [x] P3.7 Update the TFL 6 run-profile/model-input contract (`#32`) with
  reviewed design decisions and explicit rejected/deferred assumptions.
  - [x] P3.7a Record the Phase 4 model-input contract field families and
    accepted source artifacts.
  - [x] P3.7b Reconcile `config/run_profile.tfl6.yaml` and
    `config/tipsy/tfl6.yaml` metadata with accepted Phase 3 artifacts.
  - [x] P3.7c Lock rejected/deferred assumptions and Phase 4 entry guardrails.

## Phase 4: Model Inputs and Patchworks Runtime Package (`#14`)

Goal: generate, inspect, and QA the first runnable TFL 6 Patchworks teaching
package only after the reviewed source-layer, THLB, and model-design contracts
exist.

- [x] P4.1 Build the reviewed model-input bundle from accepted TFL 6 source
  layers, THLB outputs, and model-design assumptions (`#17`).
  - [x] P4.1a Confirm the accepted Phase 2/3 prerequisite artifacts and record
    the bundle input manifest.
  - [x] P4.1b Define generated model-input bundle paths and table roles before
    writing bundle outputs.
  - [x] P4.1c Build the first reviewed model-input bundle from the accepted
    THLB, AU, curve, treatment, transition, cedar, and embedded-identity
    contracts.
    - [x] P4.1c.1 Regenerate the final THLB geometry handoff at
      `data/model_input_bundle/input_geometry/thlb_current.feather`, write the
      GeoPackage mirror and checkpoint manifest, and record the inspection
      summary in `planning/tfl6_model_input_bundle_geometry_handoff.md`.
    - [x] P4.1c.2a Repair the GLB-to-AFLB non-forest filter and rerun the
      corrected AFLB/THLB/NTHLB geometry handoffs before bundle CSV generation
      resumes (`#36`).
    - [x] P4.1c.2 Build the first core bundle tables from the AFLB
      resultant-fragment universe, the regenerated THLB/NTHLB managed-share
      state surface, and the accepted Phase 3 model-design contracts.
  - [x] P4.1d Run lightweight bundle QA for readability, required fields,
    missing AU/curve mappings, treatment eligibility flags, and embedded
    K3Z/NICF identity fields.
- [x] P4.2 Generate ForestModel/XML and inspect the semantics that affect
  Patchworks treatment eligibility, curve provenance, products, accounts, and
  targets (`#37`).
- [x] P4.3 Execute Matrix Builder and QA tracks, features, accounts,
  protoaccounts, products, targets, and reports (`#38`).
- [x] P4.4 Complete Patchworks runtime-package build/QA (`#10`) with
  representative launch and scenario-smoke checks.
  - [x] P4.4a Build and inspect runtime block/topology artifacts from the
    accepted P4.2 fragments.
  - [x] P4.4b Add the `analysis/base.pin` launch surface and helper scripts.
  - [x] P4.4c Run direct Patchworks launch smoke and inspect saved-stage
    artifacts.
  - [x] P4.4d Run representative scenario smoke and record Phase 4 closeout
    evidence.

## Phase 5: Publication, Teaching Docs, and Release QA (`#15`)

Goal: make the teaching instance reproducible and usable by students/instructors
after the runtime package has passed direct artifact and launch smoke checks.

- [x] P5.1 Decide which compact runtime artifacts are tracked, annexed,
  published, or regenerated (`#18`).
- [x] P5.2 Publish required data/runtime artifacts through the accepted FEMIC
  public-data workflow and prove fresh-environment materialization (`#39`).
- [x] P5.3 Build full Sphinx teaching documentation (`#21`) modeled on the
  `femic-k3z-instance` and `femic-tsa29-instance` documentation surfaces,
  including quickstart instructions, rebuild workflow, source-data provenance,
  THLB validation notes, scenario teaching workflows, advanced student
  challenges, multi-perspective stakeholder/KPI scenario interpretation, known
  limitations, and warning-clean Sphinx build evidence.
  - [x] P5.3a Publish the current seed docs through a standalone GitHub Pages
    workflow so Phase 2/Phase 3 documentation is visible before the final
    Phase 5 teaching-docs expansion.
    - [x] P5.3a.1 Use the same RTD Sphinx theme pattern as the K3Z and MKRF
      instance documentation.
  - [x] P5.3b Expand final K3Z/TSA29-style teaching docs after Phase 4 runtime
    package evidence exists.
    - [x] P5.3b.1 Add the Phase 5 runtime-release page covering the published
      archive, DataLad/git-annex materialization commands, Arbutus remote
      metadata, no-credential proof, launch boundary, rebuild anchors, and
      caveats.
    - [x] P5.3b.2 Add a student/maintainer runtime quickstart that starts from
      the published archive, materializes it from `arbutus-s3`, unpacks it,
      opens `base.pin`, verifies the core baseline teaching signals, and points
      back to rebuild/provenance docs without requiring students to rebuild
      first.
    - [x] P5.3b.3 Add a maintainer rebuild/provenance guide that maps canonical
      configs, planning notes, generated artifacts, lineage commands, release
      archive metadata, and dependency order from source/THLB through runtime
      publication.
    - [x] P5.3b.4 Add scenario teaching-workflow documentation that orients
      students to the baseline runtime package, stakeholder/KPI families,
      first outputs to inspect, starter exercises, advanced project prompts,
      reporting rules, and first-release scenario limits.
    - [x] P5.3b.5 Add known-limitations and release-readiness documentation
      that consolidates first-release caveats, clarifies what does and does not
      block the teaching release, and defines the P5.4 final QA checklist.
- [x] P5.4 Run final release QA across source materialization, instance rebuild,
  Patchworks launch smoke, and documentation checks (`#40`).
  - [x] P5.4a Create the release-QA child issue and checklist surface before
    running executable QA checks.
  - [x] P5.4b Verify archive, manifest, and public materialization.
  - [x] P5.4c Verify Patchworks launch and baseline signal smoke evidence.
  - [x] P5.4d Verify docs build, docs links, and published Pages surface.
  - [x] P5.4e Close Phase 5 after QA evidence is recorded.

## Phase 6: MP11 Ingestion And Model-Overhaul Planning (`#42`)

Goal: ingest the public TFL 6 Management Plan 11 source package and plan the
MP10-derived teaching model overhaul without changing accepted model inputs
before the MP11 evidence is extracted, reviewed, and crosswalked.

- [ ] P6.1 Archive MP11 source package and extraction manifest (`#43`).
  - [ ] P6.1a Record source URL, access date, document identity, page count,
    and package components.
  - [ ] P6.1b Define source-copy and provenance conventions before accepting
    derived extraction artifacts.
  - [ ] P6.1c Record extraction-manifest requirements for sections, tables,
    figures, assumptions, metadata, and page anchors.
- [ ] P6.2 Extract MP11 tables, figures, sections, assumptions, and metadata
  (`#44`).
  - [ ] P6.2a Inventory section headings, tables, figures, appendices,
    references, assumptions, model-input descriptions, and sensitivity items.
  - [ ] P6.2b Attach every extracted claim to a page/section anchor.
  - [ ] P6.2c Record extraction method, tool versions, failures, and manual
    review flags.
- [ ] P6.3 Compare MP11 land base and THLB assumptions against the Phase 5
  prototype (`#45`).
- [ ] P6.4 Compare MP11 inventory, LiDAR/ITI, yield, operability, and
  harvest-system assumptions (`#46`).
- [ ] P6.5 Compare MP11 model behavior, sensitivities, AAC recommendation, and
  KPI outputs (`#47`).
- [ ] P6.6 Write the Phase 7+ implementation roadmap for the MP11-aligned
  model overhaul (`#48`).

## Phase 7: MP11 Figure Extraction Test Harness (`#49`)

Goal: run a full, auditable figure-extraction test on the public MP11 PDF
package before recovered figure evidence is used to guide any MP10-to-MP11
model-upgrade work.

- [x] P7.1 Create MP11 source and figure inventory (`#50`).
  - [x] P7.1a Record MP11 source metadata and checksum.
  - [x] P7.1b Build the figure inventory with page anchors and captions.
  - [x] P7.1c Add chart-family and downstream-use candidate fields.
  - [x] P7.1d Identify extraction priority tiers and figures excluded from
    digitization.
  - [x] P7.1e Update roadmap, changelog, planning notes, and issue comments.
- [x] P7.2 Prepare `figrecover` corpus and artifact conventions (`#51`).
  - [x] P7.2a Confirm local optional dependency preflight.
  - [x] P7.2b Prepare ignored runtime corpus paths.
  - [x] P7.2c Render required MP11 figure pages with documented DPI and page
    selection.
  - [x] P7.2d Write corpus source/candidate manifests and record checksums.
  - [x] P7.2e Update roadmap, changelog, planning notes, and issue comments.
- [ ] P7.3 Crop, classify, and calibrate MP11 figure candidates (`#52`).
  - [x] P7.3a Crop selected figure candidates under ignored runtime paths.
  - [x] P7.3b Classify extraction method and support status.
  - [ ] P7.3c Create calibration specs for high-priority numeric charts.
  - [ ] P7.3d Record crop checksums and calibration-review status.
  - [ ] P7.3e Update roadmap, changelog, planning notes, and issue comments.
- [ ] P7.4 Extract priority MP11 figure tables and QA overlays (`#53`).
  - [ ] P7.4a Extract line-chart priority figures.
  - [ ] P7.4b Extract bar/stacked/mixed-chart priority figures where feasible.
  - [ ] P7.4c Generate QA overlays and diagnostics.
  - [ ] P7.4d Register raw extraction outputs with provenance and checksums.
  - [ ] P7.4e Update roadmap, changelog, planning notes, and issue comments.
- [x] P7.5 Review recovered outputs and classify downstream use (`#54`).
  - [x] P7.5a Review high-priority extraction overlays.
  - [x] P7.5b Cross-check against related MP11 tables/text when available.
  - [x] P7.5c Assign review status and downstream-use classification.
  - [x] P7.5d Write compact reviewed summary manifests.
  - [x] P7.5e Update roadmap, changelog, planning notes, and Phase 6 handoff
    comments.
- [ ] P7.6 Close out docs, validation, and model-upgrade handoff (`#55`).
  - [ ] P7.6a Write the phase closeout summary and model-upgrade handoff note.
  - [ ] P7.6b Add or update Sphinx docs if the workflow should be user-facing.
  - [ ] P7.6c Run final validation checks.
  - [ ] P7.6d Open and merge the Phase 7 PR.
  - [ ] P7.6e Close parent and child issues with final links.

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
6. **MP11 ingestion and comparison planning**: Phase 6 (`#42`) starts after the
   Phase 5 teaching release and extracts the MP11 source package before any
   model-upgrade implementation.
7. **MP11 figure extraction test**: Phase 7 (`#49`) is a bounded evidence
   lane upstream of MP10-to-MP11 model upgrades. It may run in parallel with
   Phase 6 extraction planning, but recovered figure values cannot become model
   inputs until reviewed and handed off through the relevant Phase 6 comparison
   lanes.

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

0. Phase 7 is active on branch `feature/p7-mp11-figure-extraction-test`.
   Parent issue `#49` and child issues `#50` through `#55` define the full MP11
   figure-extraction test upstream of any MP10-to-MP11 model upgrade. P7.1 is
   complete: `planning/tfl6_mp11_figure_extraction_test_plan.md` defines the
   extraction-test boundary,
   `planning/tfl6_mp11_full_figure_inventory.csv` records the first 61-figure
   inventory from Appendix A's list of figures, and
   `planning/tfl6_mp11_figrecover_corpus_summary.md` /
   `planning/tfl6_mp11_figrecover_corpus_summary.json` record the ignored
   runtime corpus preparation, and
   `planning/tfl6_mp11_priority_figure_crop_queue.csv` records the first 36
   high-priority preliminary crop queue. A first Figure 2 raw extraction pilot
   is recorded in `planning/tfl6_mp11_figure2_extraction_pilot.md` and
   `planning/tfl6_mp11_figure2_extraction_pilot.json`; it produced 161 raw
   points from the base-case harvest-level chart and remains unaccepted
   `raw_extraction` evidence pending overlay/value review. The first repeatable
   crop-proposal pass is now recorded in
   `planning/tfl6_mp11_priority_crop_proposals.md`,
   `planning/tfl6_mp11_priority_crop_proposals.csv`, and
   `planning/tfl6_mp11_priority_crop_proposals.json`, with 36 proposed crops
   still marked `needs_manual_crop_review`. The first repeatable six-figure
   harvest-sensitivity extraction batch is recorded in
   `planning/tfl6_mp11_harvest_sensitivity_extraction_summary.md` and related
   CSV/JSON summaries. The reviewed manifest
   `planning/tfl6_mp11_reviewed_extraction_manifest.md` promotes Figures `29`,
   `30`, `31`, `35`, `36`, and `39` to `accepted_for_comparison` with
   downstream use `phase6_mp11_comparison_only`; all rows remain
   `not_model_input`. The next P7.4 chart class is also started:
   `planning/tfl6_mp11_growing_stock_extraction_summary.md` records raw
   extraction of Figures `3` and `40`, with component-sum residuals below `1%`.
   The reviewed manifest `planning/tfl6_mp11_growing_stock_review_manifest.md`
   promotes those two growing-stock figures to `accepted_for_comparison` with
   downstream use `phase6_mp11_comparison_only`; both remain `not_model_input`.
   The active edge remains P7.4 for the next chart classes: cedar inventory,
   age-class, waterfall, and remaining hybrid figures.
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
9. P3.7 / `#32` is complete. The TFL 6 run-profile and model-input contract
   now point at the reviewed Phase 2/3 artifacts, required field families, and
   explicit Phase 4 entry guardrails. YAML parsing, warning-clean Sphinx, and
   `femic prep validate-case` all passed after loading the local Arbutus
   environment and materializing/unlocking the public-data `FADM_TSA.gdb`
   payload.
10. Phase 3 closeout is complete. PR `#33` was merged to instance `main`, the
    parent FEMIC submodule pointer was updated, and the standalone docs are
    published with the RTD theme.
11. P4.1a / `#17` is complete. The accepted Phase 2/3 prerequisite manifest is
    recorded in `planning/tfl6_model_input_bundle_prerequisite_manifest.md` and
    `planning/tfl6_model_input_bundle_prerequisite_manifest.json`. The manifest
    confirms the accepted run profile, source-input layer manifest, AU/curve
    tables, TIPSY/BTC outputs, treatment/transition contracts, cedar contract,
    and embedded-identity contract are present. It also records that the
    generated `data/tsr/*checkpoint*` THLB checkpoint files referenced by the
    Phase 2 status report are missing from the current clean checkout and must
    be rematerialized, regenerated, or explicitly waived before P4.1c consumes
    final THLB geometry.
12. P4.1b / `#17` is complete. The generated bundle path and table-role
    contract is recorded in `planning/tfl6_model_input_bundle_path_contract.md`
    and `planning/tfl6_model_input_bundle_path_contract.json`. The canonical
    generated bundle root is `data/model_input_bundle/`, with final THLB
    geometry staged as
    `data/model_input_bundle/input_geometry/thlb_current.feather` plus a
    readable GeoPackage mirror and checkpoint manifest. P4.1b did not create
    the bundle root or write generated outputs.
13. Continue Phase 4 on branch `feature/p4-model-input-bundle`. P4.1c.1 /
    `#17` regenerated the final THLB geometry handoff at
    `data/model_input_bundle/input_geometry/thlb_current.feather`, wrote the
    GeoPackage mirror and manifest. P4.1c.2a / `#36` then repaired the
    GLB-to-AFLB non-forest filter after the attempted AFLB handoff from
    `aflb_checkpoint.6a351f3a223a` was invalidated. The corrected AFLB handoff
    has `25019` rows, `191168.597 ha`, and `0.000 ha` of
    `bclcs_level_1 in {N, U}` contamination. The corrected weighted
    `thlb_fact` THLB area is `139995.798 ha`, `2.57%` above the scaled current
    benchmark and inside the accepted teaching tolerance. P4.1c.2 must not
    treat THLB area alone as the full Patchworks stand universe. The stand
    universe is the AFLB resultant-fragment surface; THLB is the managed
    subset, and `NTHLB = AFLB - THLB` remains unmanaged/full-retention forest
    that still needs untreated VDYP curves.
14. P4.1c.2 / `#17` is complete. The first generated core bundle tables are
    written under ignored `data/model_input_bundle/` output space and audited in
    `planning/tfl6_model_input_bundle_core_tables.md`. The bundle contains
    `25019` AFLB stand rows, `191168.597 ha` AFLB, `139995.798 ha` THLB,
    `51172.799 ha` NTHLB, no missing natural or treated curve assignments, and
    warning-only sparse TIPSY fallback for `136` rows / `749.396 ha`. All
    harvest-system classes remain explicit `unassigned_review_required`
    placeholders pending reviewed operability/ground-cable-heli assignment. The
    first Phase 4 ForestModel may still use a generic `CC` treatment across
    eligible managed area; ground/cable/heli splitting is a later refinement
    for costs, operability reporting, and scenario interpretation. The current
    executable edge is P4.1d lightweight bundle QA; do not start ForestModel
    XML, Matrix Builder, or Patchworks runtime work until P4.1d passes or the
    maintainer explicitly narrows the gate.
15. P4.1d / `#17` is complete. Lightweight bundle QA is recorded in
    `planning/tfl6_model_input_bundle_qa.md`. Required generated tables are
    readable; area reconciliation passes; stand IDs are unique; all AU,
    natural-curve, and treated-curve mappings are non-null; all stand-level
    curve IDs exist in the curve metadata table; every curve has point rows;
    and cedar/embedded/harvest-system support tables match the stand count. The
    accepted warning gates are `136` sparse treated-curve fallback rows and
    harvest-system assignment deferred as `unassigned_review_required` for all
    rows. P4.2 may start ForestModel/XML generation from the reviewed bundle.
    Generic `CC` treatment emission is acceptable for the first ForestModel
    package; reviewed ground/cable/heli harvest-system assignment is deferred
    to a later operability and delivered-cost refinement.
16. P4.2 / `#37` is complete. It generated ForestModel XML from the refreshed
    P4.1 bundle tables and corrected AFLB checkpoint, then inspected XML
    semantics before Matrix Builder. The direct first attempt used
    `femic export patchworks --tsa tfl6` with `data/model_input_bundle/` as the
    bundle directory,
    `data/model_input_bundle/input_geometry/aflb_current.feather` as the
    checkpoint, and `output/patchworks_tfl6_validated/` as the output
    directory. That attempt exposed the schema mismatch recorded below.
17. The first P4.2 export attempt failed before writing a usable XML package
    because the reviewed TFL6 bundle uses string AU/curve IDs and audit-oriented
    columns, while the current generic FMG Patchworks exporter still expects the
    legacy numeric bundle schema with `tsa`, integer `au_id`,
    `managed_curve_id`, `unmanaged_curve_id`, `si_level`, and curve point
    columns `x`/`y`. The blocker is recorded in
    `planning/tfl6_forestmodel_xml_export_blocker.md`. That numeric-schema
    blocker was repaired by the exporter-compatible bridge recorded in item 18.
18. P4.2 / `#37` is complete. The exporter-compatible schema bridge is
    generated under ignored
    `data/model_input_bundle/export_compat/` output space and audited in
    `planning/tfl6_forestmodel_xml_export_bridge.md`. It maps reviewed TFL6
    string AU/curve IDs to deterministic numeric IDs and allowed
    `femic export patchworks --tsa tfl6` to produce XML/fragments under ignored
    `output/patchworks_tfl6_validated/`. Structural inspection found
    `373` XML curves, `2442` selects, `24879` fragments, `191168.566 ha`
    exported fragment area, and `407` exported AUs. The `814` emitted `CC`
    treatment nodes are accepted as a generic Phase 4 clearcut-and-plant
    approximation. Harvest-system assignment remains deferred and will later
    split generic `CC` into ground/cable/heli classes after the DEM and
    inventory parsing logic is reviewed.
19. P4.3 / `#38` was the Phase 4 Matrix Builder lane. It ran Matrix Builder
    from the accepted P4.2 XML/fragments pair under
    `output/patchworks_tfl6_validated/`, then inspect generated tracks,
    features, accounts, protoaccounts, products, targets, and report surfaces.
    P4.3 must confirm that AFLB remains the fragment universe, THLB remains a
    managed-share state, NTHLB remains unmanaged/full-retention forest with
    untreated growth, and generic `CC` remains the accepted first-pass
    clearcut-and-plant lane. Runtime-package assembly remains downstream in
    P4.4.
20. P4.3 / `#38` is complete and recorded in
    `planning/tfl6_matrix_builder_p43_smoke.md`. The instance runtime config
    was repaired from copied K3Z paths to TFL6 XML/fragments/tracks paths, and
    Patchworks preflight passed. The first Matrix Builder attempt exposed a
    generic FEMIC FMG pass-through succession problem (`1000 -> 1000`); the
    exporter was repaired to emit `999 -> 0`, the XML/fragments were
    regenerated, and the second Matrix Builder attempt produced readable core
    tracks: `33322` block rows, `55717` feature rows, `17173` group rows,
    `16379` product rows, `18447` strata rows, `9212` trackname rows, and
    `10703` treatment rows. The missing `protoaccounts.csv` / `accounts.csv`
    gap was repaired by increasing the Windows Matrix Builder settle window to
    `20.0` seconds and rerunning. The accepted `tfl6_p43_matrix_accounts_wait20`
    run produced readable final track tables: `47218` block rows, `86574`
    feature rows, `24879` group rows, `26085` product rows, `28858` strata
    rows, `14429` trackname rows, `17390` treatment rows, `211`
    protoaccount rows, and `211` promoted account rows. Generic `CC` product
    and harvested-volume account surfaces are present. Runtime-package
    assembly, Patchworks launch smoke, scenario targets, and final report
    surfaces remain downstream in P4.4/P5.
21. P4.4 / `#10` was the final Phase 4 runtime-package lane. It assembled the
    first TFL6 Patchworks runtime package from the accepted P4.3 tracks and
    P4.2 XML/fragments, then ran representative launch/scenario smoke before
    Phase 4 closeout. Do not move to final publication until runtime-package
    smoke evidence exists. P4.4a is complete: `femic patchworks build-blocks`
    generated `models/tfl6_patchworks_model/blocks/blocks.*` and
    `topology_blocks_200r.csv`; inspection found `24879` valid EPSG:3005 block
    rows, `191168.566 ha`, and `170759` topology edges. Generated blocks,
    tracks, and `patchworksLog.csv` remain ignored until Phase 5 decides the
    publication policy. P4.4b is the next bounded step: add
    `models/tfl6_patchworks_model/analysis/base.pin` and its helper scripts so
    direct launch smoke can run. P4.4b and P4.4c are now complete: the TFL6
    runtime package has a baseline `analysis/base.pin`, shared headless helper,
    and `flowtargets.bsh` keyed to `product.HarvestedVolume.managed.*`; direct
    headless launch run `tfl6_p44b_launch0` returned `0`, detected
    `[FEMIC headless] saveStage completed`, and wrote `903` saved-stage files.
    P4.4d is the next bounded step: run representative scenario smoke against
    `product.HarvestedVolume.managed.Total.CC` and inspect target/schedule
    outputs. P4.4d is now complete: representative scenario smoke run
    `tfl6_p44d_harvest_smoke200` returned `0`, detected
    `[FEMIC headless] saveStage completed`, wrote `903` saved-stage files,
    activated both `product.HarvestedVolume.managed.Total.CC` and
    `flow.even.product.HarvestedVolume.managed.Total.CC`, produced `801`
    scheduled managed `CC` rows, and generated nonzero harvested-volume current
    in `30` periods. P4.4 child `#10` and Phase 4 parent `#14` are closed.
22. Phase 4 is complete. The accepted runtime package has refreshed
    ForestModel/XML, Matrix Builder tracks/accounts, block/topology artifacts,
    direct launch smoke, and representative scenario-smoke evidence. Generated
    blocks, tracks, and saved-stage outputs remain ignored locally until Phase
    5 decides publication policy.
23. P5.1 / `#18` is complete. The runtime artifact publication policy is
    recorded in `planning/tfl6_runtime_artifact_publication_policy.md`. Compact
    contract and launch surfaces stay tracked in Git; generated model-input
    bundles, XML/fragments, Matrix Builder tracks, blocks/topology, logs, and
    saved-stage outputs remain ignored by default; and P5.2 must decide whether
    to publish only source data plus rebuild instructions or also a reviewed
    runtime archive. Any published runtime archive must be annexed or otherwise
    released through an explicit public mechanism and proven materializable in a
    fresh environment.
24. P5.3a / `#21` publication plumbing is complete for the current seed docs,
    but P5.3 stays open for final teaching-docs expansion after Phase 4 runtime
    package evidence exists.
25. P5.2 / `#39` is the next bounded lane: implement the accepted publication
    path from P5.1 and prove required fresh-environment materialization before
    claiming release readiness. The first P5.2 decision is whether this release
    publishes only source data plus rebuild instructions or also publishes a
    reviewed ready-to-launch runtime archive for teaching users.
    P5.2a is complete: the instance-local `arbutus-s3` git-annex special remote
    has been initialized against bucket `ubc-fresh-femic-tfl6-instance`, the
    remote metadata has been pushed on the `git-annex` branch, and the remote is
    currently empty pending the artifact-set decision.
    P5.2b is complete: the release mode is a reviewed ready-to-launch
    Patchworks runtime archive plus rebuild instructions, and
    `planning/tfl6_runtime_release_archive_manifest.md` defines the archive
    contents, manifest schema, annex publication commands, and no-credential
    fresh-clone proof.
    P5.2c is complete: `releases/tfl6_patchworks_runtime_p5_2.zip`
    and `releases/tfl6_patchworks_runtime_p5_2_manifest.yaml` were generated
    from the accepted Phase 4 runtime inputs, annexed, and copied to
    `arbutus-s3`; `git annex whereis` reports both the local repository and the
    remote, and `git annex info arbutus-s3` reports `2` remote keys / `28.01`
    MB. The next verification edge is the no-credential fresh-clone
    materialization proof.
    P5.2d is complete: a fresh temp clone of `feature/p5-publication-release`
    with AWS/S3 environment variables cleared enabled `arbutus-s3` with
    `creds: not available`, fetched both release files from the public remote,
    and verified the archive SHA256 against the manifest. P5.2 child `#39` is
    closed. The next bounded Phase 5 lane is P5.3b / `#21`: expand the final
    K3Z/TSA29-style teaching docs now that the runtime archive exists and is
    publicly materializable.
    P5.3b.1 is complete: `docs/phase5-runtime-release.rst` now documents the
    published runtime archive, `arbutus-s3` materialization commands and remote
    metadata, no-credential proof, launch boundary, rebuild anchors, and known
    caveats; `docs/index.rst` links the page and no longer describes the package
    as not runnable.
    P5.3b.2 is complete: `docs/phase5-runtime-quickstart.rst` now gives
    teaching users a runtime-first path from public archive materialization to
    `base.pin` launch and baseline signal checks, while keeping rebuild work
    pointed at the provenance and model-building documentation.
    P5.3b.3 is complete: `docs/phase5-rebuild-provenance.rst` now maps the
    canonical planning/config/docs surfaces, generated artifact boundaries,
    accepted Phase 2-5 rebuild anchors, lineage-registry commands, release
    archive/manifest surfaces, and maintainer rebuild checklist.
    P5.3b.4 is complete: `docs/phase5-scenario-teaching-workflows.rst` now
    documents the baseline scenario orientation, stakeholder-style KPI
    families, first Patchworks outputs to inspect, starter exercises, advanced
    project prompts, reporting rules, and first-release limits for generic
    `CC`, deferred harvest-system splits, and outside-AOI NICF expansion.
    P5.3b.5 is complete: `docs/phase5-known-limitations-release-readiness.rst`
    now consolidates first-release caveats, release-readiness boundaries, and
    the P5.4 final QA checklist. P5.3 / `#21` is complete and the next bounded
    Phase 5 lane is P5.4 release QA.
    P5.4a is complete: P5.4 child issue `#40` is open and
    `planning/tfl6_phase5_release_qa.md` records the final release-QA checklist.
    The next bounded QA slice is P5.4b archive, manifest, and public
    materialization verification.
    P5.4b is complete: a fresh no-credential clone on
    `feature/p5-publication-release` enabled `arbutus-s3` with
    `creds: not available`, fetched the runtime archive and manifest, passed
    git-annex checksum verification, matched archive SHA256
    `17f56d11faeba89170fc48e202d1bfe83c2dd40b53e7409d8cdb8c1c487c2f9f` and
    size `28000736` against the manifest, and confirmed required ZIP members
    are present. The next bounded QA slice is P5.4c Patchworks launch and
    baseline signal smoke evidence.
    P5.4c is complete: accepted lineage evidence records direct launch smoke
    `tfl6_p44b_launch0` and scenario smoke `tfl6_p44d_harvest_smoke200`, both
    with return code `0`, `[FEMIC headless] saveStage completed`, and `903`
    saved-stage files. The scenario schedule has `801` managed `CC` rows, and
    saved target CSVs carry nonzero managed `CC` harvested-volume,
    managed `CC` treated-area, managed/unmanaged area, and managed/unmanaged
    yield signals. Release ZIP inspection confirmed required launch helpers,
    ForestModel XML, track tables, and baseline signal names are included. The
    next bounded QA slice is P5.4d docs build, docs links, and published Pages
    verification.
    P5.4d is complete: local Sphinx built warning-clean, generated HTML uses
    the RTD theme and links the Phase 5 pages, and public Pages now serves the
    Phase 5 release docs. The first public check exposed stale Pages content
    because deployment was still `main`-only; the workflow now permits manual
    `workflow_dispatch` deployment while keeping automatic deployment restricted
    to `main`, and the `github-pages` environment has a narrow branch policy for
    `feature/p5-publication-release`. The manual deploy succeeded, the public
    root returns `200` with Phase 5 content, and the five Phase 5 pages return
    `200`.
    P5.4e and Phase 5 are complete: the release-QA checklist records archive
    materialization, manifest/SHA verification, Patchworks launch and baseline
    signal smoke evidence, warning-clean Sphinx build, public Pages checks, and
    explicit deferred follow-on scope. The P5.4 child issue `#40` and Phase 5
    parent `#15` are closed. Future work should be opened as new follow-on
    phase/task issues rather than reopening this first teaching-release
    closeout.
