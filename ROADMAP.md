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

- [x] P6.1 Archive MP11 source package and extraction manifest (`#43`).
  - [x] P6.1a Record source URL, access date, document identity, page count,
    and package components.
  - [x] P6.1b Define source-copy and provenance conventions before accepting
    derived extraction artifacts.
  - [x] P6.1c Record extraction-manifest requirements for sections, tables,
    figures, assumptions, metadata, and page anchors.
  - [x] P6.1d State clearly that MP11 analysis informs the Chief Forester's
    AAC determination and is not treated here as a final approved AAC decision.
- [x] P6.2 Extract MP11 tables, figures, sections, assumptions, and metadata
  (`#44`).
  - [x] P6.2a Inventory section headings, tables, figures, appendices,
    references, assumptions, model-input descriptions, and sensitivity items.
  - [x] P6.2b Attach every extracted claim to a page/section anchor.
  - [x] P6.2c Record extraction method, tool versions, failures, and manual
    review flags.
- [x] P6.3 Compare MP11 land base and THLB assumptions against the Phase 5
  prototype (`#45`).
  - [x] P6.3a Crosswalk MP11 total TFL area, productive forest, THLB, NCLB,
    total operable, and long-term land-base values against Phase 5 benchmark
    and bundle surfaces.
  - [x] P6.3b Identify changed netdown categories, source-layer definitions,
    and boundary/tenure assumptions.
  - [x] P6.3c Separate directly reproducible public-layer deltas from
    proxy/sensitivity and model-constraint assumptions.
- [x] P6.4 Compare MP11 inventory, LiDAR/ITI, yield, operability, and
  harvest-system assumptions (`#46`).
  - [x] P6.4a Inspect VRI, LiDAR, ITI, physical operability, economic
    operability, riparian, OGMA/WHA, terrain, karst, and future-retention
    assumptions.
  - [x] P6.4b Inspect analysis-unit, natural-yield, managed-yield, OAF,
    utilization, non-recoverable-loss, forest-cover constraint,
    minimum-harvest-age, harvest-rule, silvicultural-system, and
    harvest-flow-objective assumptions.
  - [x] P6.4c Compare MP11 assumptions against the Phase 5 AU/yield,
    treatment, transition, runtime, and known-limitation surfaces.
  - [x] P6.4d Classify deltas as public-data update, model-parameter update,
    sensitivity candidate, model-constraint update, or unresolved
    proprietary/WFP-model gap.
- [x] P6.5 Compare MP11 model behavior, sensitivities, AAC recommendation, and
  KPI outputs (`#47`).
  - [x] P6.5a Inventory MP11 base case, alternate harvest flows,
    sensitivity analyses, AAC recommendation, and key reported outputs.
  - [x] P6.5b Compare available Phase 5 Patchworks evidence against MP11
    harvest-system, age/volume-class, cedar, old-cedar, elevation-band,
    species-composition, and other KPI surfaces.
  - [x] P6.5c Identify where a public-data prototype can align with MP11 and
    where WFP's model remains non-public and must be approximated or caveated.
  - [x] P6.5d Produce a prioritized gap list for Phase 7+ implementation
    planning.
- [x] P6.6 Write the Phase 7+ implementation roadmap for the MP11-aligned
  model overhaul (`#48`).
  - [x] P6.6a Define follow-on lanes for source layers, THLB, AU/yield,
    Patchworks runtime, scenario/KPI surfaces, docs, QA, and publication.
  - [x] P6.6b Preserve the Phase 5 prototype as the baseline until
    replacement artifacts pass direct inspection and QA.
  - [x] P6.6c Identify required public data, unresolved validation gaps,
    non-public WFP model assumptions, and sequencing dependencies.
  - [x] P6.6d Draft the parent/child issue structure for the next
    implementation phase without beginning the overhaul.

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
- [x] P7.3 Crop, classify, and calibrate MP11 figure candidates (`#52`).
  - [x] P7.3a Crop selected figure candidates under ignored runtime paths.
  - [x] P7.3b Classify extraction method and support status.
  - [x] P7.3c Create calibration specs for high-priority numeric charts.
  - [x] P7.3d Record crop checksums and calibration-review status.
  - [x] P7.3e Update roadmap, changelog, planning notes, and issue comments.
- [x] P7.4 Extract priority MP11 figure tables and QA overlays (`#53`).
  - [x] P7.4a Extract line-chart priority figures.
  - [x] P7.4b Extract bar/stacked/mixed-chart priority figures where feasible.
  - [x] P7.4c Generate QA overlays and diagnostics.
  - [x] P7.4d Register raw extraction outputs with provenance and checksums.
  - [x] P7.4e Update roadmap, changelog, planning notes, and issue comments.
- [x] P7.5 Review recovered outputs and classify downstream use (`#54`).
  - [x] P7.5a Review high-priority extraction overlays.
  - [x] P7.5b Cross-check against related MP11 tables/text when available.
  - [x] P7.5c Assign review status and downstream-use classification.
  - [x] P7.5d Write compact reviewed summary manifests.
  - [x] P7.5e Update roadmap, changelog, planning notes, and Phase 6 handoff
    comments.
- [x] P7.6 Close out docs, validation, and model-upgrade handoff (`#55`).
  - [x] P7.6a Write the phase closeout summary and model-upgrade handoff note.
  - [x] P7.6b Add or update Sphinx docs if the workflow should be user-facing.
  - [x] P7.6c Run final validation checks.
  - [x] P7.6d Open and merge the Phase 7 PR.
  - [x] P7.6e Close parent and child issues with final links.

## Phase 8: MP11-Aligned Public-Data Implementation Foundation (`#58`)

Goal: convert Phase 6/7 MP11 evidence into reviewed public-data contracts and
implementation-ready recipes for the next model rebuild, while preserving the
Phase 5 runtime as the accepted baseline.

- [x] P8.1 Preserve Phase 5 baseline and lock MP11 promotion rules (`#59`).
  - [x] P8.1a Summarize Phase 5 accepted baseline artifacts and QA evidence.
  - [x] P8.1b Define MP11 evidence-promotion states.
  - [x] P8.1c Define promotion requirements for text/table/figure-derived
    evidence.
  - [x] P8.1d Define rollback and non-replacement rules.
- [x] P8.2 Design MP11 public source-layer and THLB rebuild contract (`#60`).
  - [x] P8.2a Classify source-layer categories by public reproducibility.
  - [x] P8.2b Define public proxy candidates and sensitivity lanes.
  - [x] P8.2c Define benchmark checkpoints and tolerances.
  - [x] P8.2d Write the reviewed source-layer/THLB rebuild contract.
- [x] P8.3 Decide MP11 AU/yield and managed-stand parameter strategy (`#61`).
  - [x] P8.3a Decide AU identity strategy.
  - [x] P8.3b Define MP11 managed-yield table extraction requirements.
  - [x] P8.3c Define public/private SI and inventory dependency boundaries.
  - [x] P8.3d Define yield-adjustment parameter surfaces.
- [x] P8.4 Define operability, harvest-system, MHA, and scenario rules (`#62`).
  - [x] P8.4a Define harvest-system classifier candidates and required public
    inputs.
  - [x] P8.4b Define economic-operability sensitivity logic.
  - [x] P8.4c Define MHA extraction and contract requirements.
  - [x] P8.4d Define base-case, max-short-term, AAC recommendation, and
    sensitivity scenario policies.
- [x] P8.5 Define MP11 KPI, QA, and reporting targets (`#63`).
  - [x] P8.5a Define accepted comparison targets and planning-only target
    families.
  - [x] P8.5b Define KPI output schemas and report groups.
  - [x] P8.5c Define comparison tolerances and validation-strength labels.
  - [x] P8.5d Write the KPI/QA/reporting contract.
- [x] P8.6 Close Phase 8 and split rebuild phases (`#64`).
  - [x] P8.6a Audit Phase 8 child issues and artifacts.
  - [x] P8.6b Draft follow-on rebuild phase issue tree.
  - [x] P8.6c Run validation checks.
  - [x] P8.6d Open and merge the Phase 8 PR.
  - [x] P8.6e Close parent and child issues with final links.

## Phase 9: MP11 Source-Layer And THLB Rebuild (`#66`)

Status: closed.

Goal: execute the accepted public-data source-layer and THLB rebuild contract,
materialize/review public sources, implement ordered overlay and proxy logic,
and compare GLB/AFLB/operable/THLB outputs against MP11 and Phase 5
checkpoints without force-fitting.

- [x] P9.1 Launch source-layer THLB rebuild execution plan (`#72`).
  - [x] P9.1a Audit P8.2 contract and existing source-layer notes.
  - [x] P9.1b Define Phase 9 execution plan and artifact layout.
  - [x] P9.1c Define source dependency checklist and current availability
    states.
  - [x] P9.1d Define no-force-fit and promotion gates for generated outputs.
- [x] P9.2 Materialize and verify public source layers (`#73`).
  - [x] P9.2a Verify accepted AOI, VRI/R1, and VDYP source artifacts.
  - [x] P9.2b Verify or materialize hydrography, shoreline, reserve, roads,
    recreation, and DEM/slope candidates.
  - [x] P9.2c Build source-layer schema and geometry QA summaries.
  - [x] P9.2d Record public/private/proxy status for each dependency.
- [x] P9.3 Profile inventory and proxy inputs (`#74`).
  - [x] P9.3a Profile inventory/productivity fields and candidate MP11
    mappings.
  - [x] P9.3b Profile DEM/slope and road/access proxy inputs.
  - [x] P9.3c Profile hydrography and legal/proposed reserve overlay
    attributes.
  - [x] P9.3d Define operability and low-site proxy variables with caveats.
- [x] P9.4 Implement ordered overlay THLB recipe scaffold (`#75`).
  - [x] P9.4a Define ordered overlay recipe/config from accepted P9.2/P9.3
    evidence.
  - [x] P9.4b Implement or wire bounded smoke-lane execution logic.
  - [x] P9.4c Emit checkpoint, overlap, diagnostic, and provenance outputs.
  - [x] P9.4d Run bounded smoke tests after source/profile gates pass.
- [x] P9.5 Execute and compare public-data THLB rebuild (`#76`).
  - [x] P9.5a Execute accepted THLB rebuild lane.
  - [x] P9.5b Build checkpoint and residual comparison summaries.
  - [x] P9.5c Build provenance and diagnostic manifests.
  - [x] P9.5d Classify residual gaps and candidate outputs.
- [x] P9.6 Close Phase 9 and hand off rebuild outputs (`#77`).
  - [x] P9.6a Audit Phase 9 artifacts and generated-output hygiene.
  - [x] P9.6b Write Phase 9 closeout and Phase 10/11 handoff note.
  - [x] P9.6c Run final validation and THLB QA checks.
  - [x] P9.6d Open and merge Phase 9 PR.
  - [x] P9.6e Close parent and child issues with final links.
  - [x] P9.6f Add user-facing Sphinx documentation for the accepted P9RF MP11
    THLB netdown logic, public data sources, skipped/deferred rows, and MP11
    cumulative deltas.

## Phase 10: MP11 AU/Yield Readiness And Curve-Rebuild Scoping (`#67`)

Status: closed.

Goal: extract reviewed MP11 managed-yield parameter evidence, refresh AU/yield
crosswalk surfaces, repackage existing natural and managed curve diagnostics,
and isolate the blockers that prevent an actual MP11 curve rebuild.

Phase 10 did **not** rebuild AU/yield curves or update curve plots. It produced
readiness evidence and blocker diagnostics. The actual curve rebuild is Phase
10R.

- [x] P10.1 Launch MP11 AU/yield readiness execution plan (`#79`).
  - [x] P10.1a Audit governing contracts and existing curve artifacts.
  - [x] P10.1b Define Phase 10 artifact layout and generated-output hygiene.
  - [x] P10.1c Define curve-lane and parameter-library gates.
  - [x] P10.1d Define validation commands for Phase 10 implementation tasks.
- [x] P10.2 Extract MP11 managed-yield parameter library (`#80`).
  - [x] P10.2a Identify source-page anchors and extraction scope for MP11
    parameter tables/text.
  - [x] P10.2b Build reviewed MP11 managed-yield parameter library generator.
  - [x] P10.2c Emit Markdown/CSV/JSON parameter-library outputs.
  - [x] P10.2d Classify row confidence and public/private dependency status.
- [x] P10.3 Refresh MP11 AU and curve-lane crosswalk (`#81`).
  - [x] P10.3a Audit existing Phase 3 static AU and curve crosswalk artifacts.
  - [x] P10.3b Build MP11 AU/curve-lane crosswalk generator.
  - [x] P10.3c Emit crosswalk Markdown/CSV/JSON and fallback diagnostics.
  - [x] P10.3d Flag unsupported and non-public dependency mappings.
- [x] P10.4 Repackage MP11 natural curve diagnostics (`#82`).
  - [x] P10.4a Review VDYP source/version and existing natural curve scripts.
  - [x] P10.4b Repackage existing public VDYP evidence for MP11 review.
  - [x] P10.4c Emit natural curve diagnostics, existing plot references, and comparison
    summaries.
  - [x] P10.4d Flag sparse-support, fallback, or unsupported curve families.
- [x] P10.5 Record MP11 managed curve blocker diagnostics (`#83`).
  - [x] P10.5a Join managed-lane gates to existing Phase 5 comparison
    diagnostics.
  - [x] P10.5b Record parser-review blockers for Tables 54, 55, and 57.
  - [x] P10.5c Emit diagnostics, existing comparison references, and fallback
    reports.
  - [x] P10.5d Classify unsupported and unavailable-dependency rows.
- [x] P10.6 Close Phase 10 and hand off curve-readiness artifacts (`#84`).
  - [x] P10.6a Audit Phase 10 artifacts and generated-output hygiene.
  - [x] P10.6b Write Phase 10 closeout and Phase 11 handoff note.
  - [x] P10.6c Run final validation and readiness QA checks.
  - [x] P10.6d Open and merge Phase 10 PR.
  - [x] P10.6e Close parent and child issues with final links.

## Phase 10R: MP11 Curve Parser And Curve Rebuild (`#92`)

Status: complete.

Goal: execute the actual MP11 curve rebuild that Phase 10 scoped but did not
complete. This phase owns reviewed parsing of MP11 Tables 54, 55, and 57,
BatchTIPSY/TIPSY handoff inputs, managed-curve execution/parsing, and refreshed
natural/managed curve plots or a maintainer-reviewable blocker package.

- [x] P10R.1 Launch MP11 curve-rebuild execution plan (`#93`).
  - [x] P10R.1a Amend Phase 10 wording to readiness/scoping rather than
    completed curve rebuild.
  - [x] P10R.1b Add Phase 10R roadmap and issue references.
  - [x] P10R.1c Add the Phase 10R execution plan.
  - [x] P10R.1d Mark Phase 11 blocked pending accepted Phase 10R outputs.
- [x] P10R.2 Parse MP11 Tables 54, 55, and 57 per-AU TIPSY rows (`#94`).
  - [x] P10R.2a Locate source pages and table boundaries for Tables 54, 55,
    and 57.
  - [x] P10R.2b Implement parser/extraction script.
  - [x] P10R.2c Emit public-safe row tables with page/table provenance.
  - [x] P10R.2d Add QA summaries for missing, wrapped, or ambiguous rows.
  - [x] P10R.2e Review row counts and representative rows manually.
- [x] P10R.3 QA managed-yield rows and build BatchTIPSY handoff inputs (`#95`).
  - [x] P10R.3a Join parsed rows to the AU/curve-lane crosswalk.
  - [x] P10R.3b Validate density, regeneration delay, genetic gain, VRAF,
    utilization, and site assumptions.
  - [x] P10R.3c Emit handoff CSV/JSON/Markdown manifests.
  - [x] P10R.3d Record unsupported rows and maintainer decisions required.
- [x] P10R.4 Run and parse MP11 managed curve generation (`#96`) - Windows
  BatchTIPSY/TIPSY execution, output parsing, inspection, and Phase 5 fallback
  comparison complete for all `27` Table 57 future-managed candidates: `25`
  rows are BTC-generated and `2` FMH rows reuse the valid canonical
  `cwhvm2_hw_ba_l` future-managed TIPSY curve. Every review artifact remains
  `not_model_input`; the curve-generation recipe is locked to target canonical
  top-N AU VRI BEC and median SI inputs.
  - [x] P10R.4a Run accepted BatchTIPSY/TIPSY or local-equivalent commands.
  - [x] P10R.4b Capture tool versions, commands, inputs, outputs, and failures.
  - [x] P10R.4c Parse output curves to normalized tables.
  - [x] P10R.4d Emit diagnostics for failed or unsupported rows.
  - [x] P10R.4e Compare candidate outputs against Phase 5 fallback curves.
- [x] P10R.5 Regenerate natural and managed curve plots and overlays (`#97`) -
  managed Phase 10R-vs-Phase 5 overlays, public VDYP curve slices, and
  AU-wise MP11 TIPSY-vs-VDYP diagnostic plots complete for all `27` accepted
  Table 57 handoff curves. All review artifacts remain `not_model_input` until
  Phase 11 writes model-input tables.
  - [x] P10R.5a Inventory existing curve plot locations.
  - [x] P10R.5b Generate updated VDYP/natural curves and AU-wise
    TIPSY-vs-VDYP diagnostic plots where inputs support it.
  - [x] P10R.5c Generate rebuilt managed curve plots from P10R.4 outputs.
  - [x] P10R.5d Emit plot manifests with source/provenance links.
  - [x] P10R.5e Update review/planning references to the new plot library.
- [x] P10R.6 Close curve-rebuild phase and hand off accepted curve candidates
  (`#98`).
  - [x] P10R.6a Audit Phase 10R artifacts, rejected-curve parameters, and
    generated-output hygiene.
  - [x] P10R.6a1 Lock the reproducible MP11 managed curve-generation recipe.
  - [x] P10R.6b Write Phase 10R closeout.
  - [x] P10R.6c Update roadmap, changelog, and issue statuses.
  - [x] P10R.6d Run final validation.
  - [x] P10R.6e Unblock or explicitly defer Phase 11 based on accepted outputs.

## Phase 9D: Public DEM Steep-Slope Proxy Repair (`#100`)

Status: active and urgent.

Goal: implement a public DEM steep-slope proxy for MP11 Table 12 Step 220 so
the P9RF THLB lane no longer leaves an avoidable zero-deduction placeholder
where a known public DEM source can at least support a reviewed proxy.

This phase is a P9RF residual-repair lane. It does not claim equivalence to
WFP's private LiDAR/DTSM/Patchworks implementation, but it must test the best
available public DEM route before the MP11 THLB surface is promoted into
model-input work.

- [x] P9D.1 Launch public DEM steep-slope execution plan (`#101`).
  - [x] P9D.1a Audit existing DEM/LiDAR/CDED/source-discovery notes.
  - [x] P9D.1b Write
    `planning/tfl6_mp11_public_dem_steep_slope_execution_plan.md`.
  - [x] P9D.1c Define artifact paths for DEM, slope raster, zonal stats, and
    Step 220 reports.
  - [x] P9D.1d Define lock/defer criteria for Step 220.
- [x] P9D.2 Materialize public DEM smoke-test source for TFL 6 (`#102`).
  - [x] P9D.2a Resolve CDED source metadata and direct download root.
  - [x] P9D.2b Determine AOI tile/archive requirements.
  - [x] P9D.2c Materialize source archives under ignored/generated paths.
  - [x] P9D.2d Build a DEM clip or mosaic for the TFL 6 AOI.
  - [x] P9D.2e Write DEM QA summary Markdown/CSV/JSON.
- [x] P9D.3 Derive percent-slope raster and zonal statistics (`#103`).
  - [x] P9D.3a Implement or adapt a slope-raster derivation script.
  - [x] P9D.3b Compute documented percent-slope raster outputs.
  - [x] P9D.3c Compute zonal summaries and steep-area proportions.
  - [x] P9D.3d Emit QA summaries for slope distributions and nodata coverage.
- [x] P9D.4 Implement and compare Step 220 steep-slope scenarios (`#104`).
  - [x] P9D.4a Implement Step 220 scenario runner.
  - [x] P9D.4b Test multiple slope/proportion thresholds.
  - [x] P9D.4c Compare results against MP11 Step 220 and Current THLB
    residuals.
  - [x] P9D.4d Emit Markdown/CSV/JSON scenario reports.
  - [x] P9D.4e Recommend lock/defer with rationale.
- [x] P9D.5 Lock or defer Step 220 and refresh P9RF outputs (`#105`).
  - [x] P9D.5a Decide lock/defer for Step 220 with maintainer rationale.
  - [x] P9D.5b Patch P9RF rebuild and contract if accepted.
  - [x] P9D.5c Rerun P9RF and compare Steps 220, 280, 290, and 310.
  - [x] P9D.5d Update generated reports, roadmap, changelog, and planning
    notes.
  - [x] P9D.5e Run validation and close the phase.

## Phase 9E: Public TSM Terrain-Stability Step 210 Repair (`#106`)

Status: complete.

Goal: correct the Step 210 source gap after identifying the public BC Terrain
Stability Mapping detailed polygon layer as a real candidate source for MP11
Table 12 Step 210.

This phase applies the public TSM source transparently but does not claim WFP
DTSM/Patchworks equivalence. The result proves that the public layer exists and
should not be skipped, while also showing that strict public Class V terrain
coverage explains only a very small portion of the MP11 Step 210 netdown.

- [x] P9E.1 Materialize public TSM source and evaluate Step 210 scenarios
  (`#107`).
  - [x] P9E.1a Fetch public TSM polygons from the BC ArcGIS REST layer.
  - [x] P9E.1b Clip to TFL 6 and write
    `data/source/tfl_6/terrain/tsm_detailed_polygons_tfl6.gpkg`.
  - [x] P9E.1c Write source manifest Markdown/CSV/JSON.
  - [x] P9E.1d Test strict Class V and broader diagnostic rules against the
    Step 200 active P9RF surface.
  - [x] P9E.1e Select strict `slope_stability_class_w_roads == "V"` as the
    accepted public proxy.
- [x] P9E.2 Apply public TSM Step 210 proxy and rerun P9RF (`#108`).
  - [x] P9E.2a Patch Table 12 recipe and P9RF rebuild.
  - [x] P9E.2b Add guard against stale Step 220 zonal tables after Step 210
    geometry changes.
  - [x] P9E.2c Regenerate Step 220 CDED zonal/scenario evidence on the
    TSM-adjusted Step 210 surface.
  - [x] P9E.2d Rerun P9RF through Step 310.
  - [x] P9E.2e Record final endpoint deltas.

## Phase 11: MP11 Model-Input Bundle And ForestModel XML Rebuild (`#68`)

Status: active for model-input/XML rebuild from accepted Phase 10R curves.

Goal: build the MP11-aligned model-input bundle and ForestModel XML from
accepted source-layer, THLB, AU/yield, treatment, transition, MHA,
harvest-system, and reporting contracts.

Build boundary: Phase 11 may build or stop-report the MP11 candidate
model-input bundle, export bridge, and ForestModel XML/fragments. Phase 11 does
not assemble the Patchworks runtime bundle. The first roadmap phase that
actually runs Matrix Builder and builds the Patchworks runtime package is
Phase 12 (`#69`).

Phase 10R is closed with all `27` MP11 Table 57 future-managed curves accepted
for the Phase 11 curve handoff. The locked recipe emits TIPSY BEC and SI from
the target canonical top-N AU VRI record. Phase 11 can proceed to explicit
model-input table and ForestModel XML work from that surface. Tables 54/55
remain deferred unless a later public-safe existing or recent managed AU-code
mapping is supplied. Phase 9D is complete and Step 220 now has an accepted
public CDED steep-slope proxy in the P9RF THLB surface.

- [x] P11.1 Launch MP11 model-input/XML rebuild execution plan (`#86`).
  - [x] P11.1a Audit governing contracts and handoff blockers.
  - [x] P11.1b Inventory existing Phase 5 model-input/XML provenance surfaces.
  - [x] P11.1c Define Phase 11 artifact layout and generated-output hygiene.
  - [x] P11.1d Define promotion gates and stop conditions.
- [x] P11.2 Audit MP11 model-input promotion readiness (`#87`).
  - [x] P11.2a Build promotion-readiness audit generator.
  - [x] P11.2b Emit readiness Markdown/CSV/JSON outputs.
  - [x] P11.2c Classify blockers and required maintainer decisions.
  - [x] P11.2d Decide whether P11.3 may build a candidate scaffold or must
    remain blocked.
- [x] P11.3 Build MP11 model-input candidate manifest or stop report (`#88`).
  - [x] P11.3a Consume P11.2 readiness manifest.
  - [x] P11.3b Build candidate table/schema manifest or blocked stop report.
  - [x] P11.3c Record provenance and fallback policy for each candidate table.
- [x] P11.4 Generate MP11 ForestModel XML candidate or stop report (`#89`).
  - [x] P11.4a Audit existing Phase 5 XML provenance and bridge notes.
  - [x] P11.4b Build XML readiness manifest or stop report.
  - [x] P11.4c Build generated MP11 candidate model-input bundle and export
    compatibility bridge under `data/mp11_model_input_bundle/`.
  - [x] P11.4d Rerun XML readiness against generated MP11 candidate outputs.
  - [x] P11.4e Generate candidate `forestmodel.xml` and fragments under
    `output/patchworks_tfl6_mp11_candidate/` if readiness passes.
  - [x] P11.4f Parse/check generated XML and record XML readiness QA.
- [x] P11.5 Define Phase 12 runtime handoff or blocker package (`#90`).
  - [x] P11.5a Build Phase 12 handoff or blocker summary.
  - [x] P11.5b Post/update Phase 12 issue handoff.
- [x] P11.6 Close Phase 11 and hand off model-input/XML status (`#91`).
  - [x] P11.6a Audit Phase 11 artifacts and generated-output hygiene.
  - [x] P11.6b Write Phase 11 closeout and Phase 12/13 handoff note.
  - [x] P11.6c Run final validation and model-input/XML checks.
  - [x] P11.6d Open and merge Phase 11 PR.
  - [x] P11.6e Close parent and child issues with final links.

## Phase 12: MP11 Patchworks Runtime And Scenario Smoke (`#69`)

Status: complete. P12.1 launched the runtime-build issue tree and added the
MP11 candidate Matrix Builder config. P12.2 generated and inspected Matrix
Builder tracks. P12.3 assembled the candidate runtime package. P12.4 passed
direct launch smoke. P12.5 passed representative scenario smoke. P12.6 closed
the runtime-smoke lane and handed the candidate runtime to Phase 13.

Goal: run Matrix Builder, assemble an MP11-aligned Patchworks runtime package,
and smoke-test direct launch plus representative base and sensitivity
scenarios before any release claim.

Build ownership: Phase 12 is the runtime-build phase. It consumes the accepted
Phase 11 model-input/XML handoff and produces Matrix Builder tracks, blocks,
topology, launch surfaces, scenario smoke outputs, runtime manifests, and a
candidate runtime package.

- [x] P12.1 Launch runtime-build execution plan and child issues (`#114`).
  - [x] P12.1a Create P12 child issues and link the issue tree.
  - [x] P12.1b Add
    `planning/tfl6_mp11_phase12_runtime_build_execution_plan.md`.
  - [x] P12.1c Add
    `config/patchworks.runtime.mp11_candidate.windows.yaml` for the P12.2
    Matrix Builder run.
  - [x] P12.1d Confirm Phase 11 handoff inputs exist and runtime roots are
    absent before P12.2.
- [x] P12.2 Run Matrix Builder from the accepted MP11 ForestModel XML (`#115`).
  - [x] P12.2a Generate Matrix Builder tracks under
    `models/tfl6_patchworks_model_mp11_candidate/tracks/`.
  - [x] P12.2b Inspect accounts, protoaccounts, features, products, curves,
    groups, strata, treatments, and block references.
  - [x] P12.2c Record Matrix Builder QA in
    `planning/tfl6_mp11_matrix_builder_tracks_qa.{csv,json,md}`.
- [x] P12.3 Assemble MP11 candidate Patchworks runtime package (`#116`).
  - [x] P12.3a Build blocks/topology and launch surfaces under
    `models/tfl6_patchworks_model_mp11_candidate/`.
  - [x] P12.3b Record runtime lineage and candidate package manifest.
- [x] P12.4 Smoke-test direct Patchworks launch (`#117`).
  - [x] P12.4a Run headless direct launch from
    `models/tfl6_patchworks_model_mp11_candidate/analysis/base.pin`.
  - [x] P12.4b Inspect headless manifest, trace marker, saved-stage output,
    and warning/error surfaces.
  - [x] P12.4c Record launch QA in
    `planning/tfl6_mp11_direct_launch_qa.{csv,json,md}`.
- [x] P12.5 Smoke-test representative base and sensitivity scenarios (`#118`).
  - [x] P12.5a Patch candidate scenario helper to prime harvested volume before
    even-flow activation.
  - [x] P12.5b Run 200,000-iteration max-even-flow scenario smoke.
  - [x] P12.5c Inspect target status, target summary, schedule, trace, and log
    surfaces.
  - [x] P12.5d Record scenario QA in
    `planning/tfl6_mp11_scenario_smoke_qa.{csv,json,md}`.
- [x] P12.6 Close runtime smoke phase and hand off Phase 13 release/docs QA
  (`#119`).
  - [x] P12.6a Build
    `planning/tfl6_mp11_phase12_runtime_closeout.{csv,json,md}`.
  - [x] P12.6b Confirm Matrix Builder tracks, blocks/topology, direct launch
    smoke, and representative scenario smoke outputs exist.
  - [x] P12.6c Update runtime lineage and candidate-package README with the
    Phase 12 smoke-pass status and Phase 13 boundary.

## Phase 13: MP11 Comparison Documentation And Release QA (`#70`)

Status: complete. Phase 13 started from the P12.6 closeout package and decided
that the smoke-tested MP11 candidate runtime supplements the completed Phase 5
baseline. The MP11 candidate is a labelled comparison and advanced teaching
surface, not a replacement public release baseline. P13.1 recorded the initial
candidate-runtime positioning: the local interactive MP11 candidate run is
plausibly in the same model family as the WFP MP11 base-case evidence, but
remains above WFP's base case for explainable public-data/scaffold reasons and
is not WFP model equivalence or approved AAC evidence.

Goal: publish MP11 comparison documentation, teaching updates, release archive
QA, and replacement/supplement decision evidence after a rebuilt runtime passes
direct source, model-input, XML, Matrix Builder, Patchworks, scenario, docs,
archive, and manifest checks.

Execution plan:
`planning/tfl6_mp11_phase13_comparison_release_qa_plan.md`.

- [x] P13.1 Document candidate runtime positioning and comparison starting
  assumptions (`#70`).
  - [x] P13.1a Record the maintainer screenshot interpretation and MP11 Figure
    2 context in
    `planning/tfl6_mp11_phase13_candidate_runtime_positioning.md`.
  - [x] P13.1b Convert screenshot-informed positioning into reproducible
    tracked scenario comparison tables (`#127`).
- [x] P13.2 Build MP11 KPI and caveat comparison report (`#128`).
  - [x] P13.2a Compare land base, THLB, source-layer caveats, yield/curve
    caveats, growing stock, age/seral context, cedar/old-cedar evidence,
    harvest-system caveats, and selected MP11 sensitivity evidence where
    tracked sources already exist.
  - [x] P13.2b Label each comparison row by evidence strength and
    release-decision implication.
- [x] P13.3 Update MP11 Sphinx docs and teaching guidance (`#129`).
  - [x] P13.3a Document Phase 5 baseline status, MP11 candidate status, public
    data reconstruction limits, comparison evidence, and teaching workflows.
  - [x] P13.3b Run Sphinx warning-clean.
- [x] P13.4 Prepare MP11 candidate runtime archive and materialization QA
  (`#130`).
  - [x] P13.4a Decide which generated tracks, blocks, launch surfaces,
    manifests, and logs are public-safe and publishable.
  - [x] P13.4b Build archive manifest, checksums, and clean-checkout
    materialization or blocker evidence.
- [x] P13.5 Decide MP11 release status and Phase 5 baseline relationship
  (`#131`).
  - [x] P13.5a Decide `replace_phase5`, `supplement_phase5`, or
    `experimental_only`.
  - [x] P13.5b Close Phase 13 only after docs, release QA, archive/materialization,
    roadmap, changelog, and issue comments are synchronized.

## Phase 14: MP11 Harvest-System Operability Integration (`#138`)

Status: complete. Phase 14 converted the deferred MP11 harvest-system caveat
into a runtime-visible public-proxy implementation lane. It starts from the
Phase 13 `supplement_phase5` decision: Phase 5 remains the accepted public
teaching/runtime baseline, while the smoke-tested MP11 harvest-system candidate
is a working supplement for comparison and advanced teaching.

Evidence basis:

- WFP's Land Base Blocking (LBB) physical-operability dataset is not public or
  queryable from the MP11 package.
- MP11 assigns ground, cable, and non-conventional/helicopter systems from WFP's
  LBB process using LiDAR, professional review, future block/road planning, and
  post-harvest updates. FEMIC must not claim WFP LBB equivalence.
- Public FEMIC assignments must therefore be explicit public proxies with
  source, confidence, and caveat fields.
- MP11 Table 20 and Table 73 harvest-system area/volume distributions are
  comparison targets, not stand-level source truth.
- MP11 helicopter economic-operability criteria from Tables 27-29 are usable
  only where public age, volume, species-share, and access/flight-distance proxy
  fields exist.

Planning note:
`planning/tfl6_mp11_phase14_harvest_system_operability_plan.md`.

- [x] P14.1 Launch MP11 harvest-system operability execution plan (`#139`).
  - [x] P14.1a Create and link the Phase 14 parent/child issue tree.
  - [x] P14.1b Record source anchors, generated-output boundaries, and
    non-goals in the Phase 14 planning note.
  - [x] P14.1c Update `ROADMAP.md` and `CHANGE_LOG.md` without generating
    model-input tables, XML, Matrix Builder outputs, or runtime artifacts.
- [x] P14.2 Mine MP11 and public-source evidence for harvest-system criteria
  (`#140`).
  - [x] P14.2a Build
    `planning/tfl6_mp11_phase14_harvest_system_evidence.{csv,json,md}`.
  - [x] P14.2b Classify MP11 LBB as an unavailable private source, MP11 Table
    20/Table 73 as aggregate comparison targets, P9D/VRI as public proxy
    inputs, DRA roads as an access candidate, and MP11 helicopter economics as
    candidate rules after metric build.
- [x] P14.3 Build public proxy metrics for ground, cable, and heli assignment
  (`#141`).
  - [x] P14.3a Add `scripts/build_p14_public_proxy_metrics.py`.
  - [x] P14.3b Generate
    `planning/tfl6_mp11_phase14_public_proxy_metrics.{csv,json,md}` with
    stand-level public proxy metrics for age, volume, Cw/Fd/Yc species share,
    P9D CDED slope context, nearest-DRA-road access distance, and helicopter
    economic-operability threshold testing.
  - [x] P14.3c Record that P14.3 does not classify stands, does not accept
    WFP LBB equivalence, and does not generate model-input tables, ForestModel
    XML, Matrix Builder outputs, Patchworks runtime artifacts, or scenarios.
- [x] P14.4 Classify MP11 candidate stands by harvest system and QA against
  MP11 targets (`#142`).
  - [x] P14.4a Add `scripts/build_p14_harvest_system_classification.py`.
  - [x] P14.4b Generate
    `planning/tfl6_mp11_phase14_harvest_system_classification.{csv,json,md}`
    and
    `planning/tfl6_mp11_phase14_harvest_system_classification_qa.csv`.
  - [x] P14.4c Classify managed current THLB into public-proxy `ground`,
    `cable`, and `heli` lanes while keeping non-managed-current-THLB rows
    `not_applicable`.
  - [x] P14.4d Compare aggregate candidate area/volume against MP11 Table 73
    direct targets and normalized area/volume shares, preserving the caveat
    that WFP LBB geometry is unavailable.
- [x] P14.5 Rebuild MP11 model-input tables and ForestModel XML with split CC
  lanes (`#143`).
  - [x] P14.5a Add generated-root ignores for the harvest-system candidate
    bundle and future runtime package.
  - [x] P14.5b Add `scripts/build_p14_harvest_system_model_input_xml.py`.
  - [x] P14.5c Build the ignored
    `data/mp11_harvest_system_model_input_bundle/` candidate bundle by applying
    P14.4 public-proxy harvest-system assignments to stand, harvest-system,
    group, treatment, transition, and export-compat checkpoint surfaces.
  - [x] P14.5d Generate ignored ForestModel XML/fragments under
    `output/patchworks_tfl6_mp11_harvest_system_candidate/`.
  - [x] P14.5e Split generic managed `CC` tracks and product selects into
    `CC_GROUND`, `CC_CABLE`, and `CC_HELI` lanes keyed by the fragment `HVSYS`
    field while retaining aggregate `.CC` product labels for all-system
    reporting.
  - [x] P14.5f Emit
    `planning/tfl6_mp11_phase14_model_input_xml_build_summary.{csv,json,md}`.
- [x] P14.6 Run Matrix Builder and assemble harvest-system candidate runtime
  (`#144`).
  - [x] P14.6a Add
    `config/patchworks.runtime.mp11_harvest_system_candidate.windows.yaml`.
  - [x] P14.6b Run Matrix Builder with run ID
    `tfl6_mp11_harvest_system_p14_6_matrix_build`.
  - [x] P14.6c Inspect track outputs directly and verify nonzero split
    treatment/product surfaces, zero message rows, synced accounts, and managed
    area restored after binding XML `HVSYS` to the fragment `HVSYS` column.
  - [x] P14.6d Run `femic patchworks build-blocks` with topology radius `200`.
  - [x] P14.6e Assemble tracked runtime launch surfaces under
    `models/tfl6_patchworks_model_mp11_harvest_system_candidate/`.
  - [x] P14.6f Emit
    `planning/tfl6_mp11_phase14_matrix_runtime_qa.{csv,json,md}`.
- [x] P14.7 Smoke-test all-system and no-heli harvest scenarios (`#145`).
  - [x] P14.7a Add a no-heli PIN wrapper and generated ignored
    `tracks_no_heli/` track variant.
  - [x] P14.7b Remove `CC_HELI` treatment, product, account, and protoaccount
    rows from the no-heli track variant while preserving aggregate `.CC`
    harvested-volume products.
  - [x] P14.7c Run direct launch smoke, all-system 200,000-iteration harvest
    smoke, and no-heli 200,000-iteration harvest smoke.
  - [x] P14.7d Emit
    `planning/tfl6_mp11_phase14_no_heli_tracks.{csv,json,md}` and
    `planning/tfl6_mp11_phase14_scenario_smoke_qa.{csv,json,md}`.
- [x] P14.8 Document Phase 14 caveats, comparison results, and closeout status
  (`#146`).
  - [x] P14.8a Add
    `planning/tfl6_mp11_phase14_closeout.md`.
  - [x] P14.8b Add
    `docs/phase14-mp11-harvest-system-operability.rst` and link it from the
    Sphinx index.
  - [x] P14.8c Preserve Phase 5 as the accepted public teaching/runtime
    baseline and describe Phase 14 as a caveated MP11 candidate supplement.

## Phase 15: MP11 Harvest-System Runtime Publication And Replacement-Candidate QA (`#147`)

Status: active. Phase 15 publishes and validates the Phase 14 MP11
harvest-system candidate runtime as a replacement-candidate QA lane. It uses
the existing TFL 6 `arbutus-s3` git-annex publication workflow, proves
no-credential clean-checkout materialization, unpacks the materialized archive,
reruns direct launch plus all-system and no-heli scenario smoke from the archive
payload, and records whether the runtime is ready for replacement review.

Phase 15 does not silently replace Phase 5. Passing P15 means
`replacement_candidate_ready_for_review`; Phase 5 remains the accepted public
teaching/runtime baseline until a later explicit replacement acceptance
decision.

Planning note:
`planning/tfl6_mp11_phase15_publication_replacement_candidate_plan.md`.

Publication artifacts:

- `releases/tfl6_mp11_harvest_system_candidate_runtime_p15_2.zip`;
- `releases/tfl6_mp11_harvest_system_candidate_runtime_p15_2_manifest.yaml`.

- [x] P15.1 Launch MP11 harvest-system publication and replacement-candidate
  plan (`#148`).
  - [x] P15.1a Create and link the Phase 15 parent/child issue tree.
  - [x] P15.1b Record that P15 consumes the Phase 14 harvest-system runtime,
    not the older P13 archive.
  - [x] P15.1c Record artifact names, status vocabulary, WFP LBB caveats, and
    Phase 5 baseline boundary.
- [x] P15.2 Build MP11 harvest-system runtime archive and manifest (`#149`).
  - [x] P15.2a Add
    `scripts/build_p15_harvest_system_archive_publication_qa.py`.
  - [x] P15.2b Build local archive
    `releases/tfl6_mp11_harvest_system_candidate_runtime_p15_2.zip`.
  - [x] P15.2c Emit tracked manifest
    `releases/tfl6_mp11_harvest_system_candidate_runtime_p15_2_manifest.yaml`.
  - [x] P15.2d Emit
    `planning/tfl6_mp11_phase15_archive_publication_qa.{csv,json,md}` with
    status `local_archive_built_not_published`.
- [x] P15.3 Annex and publish archive through `arbutus-s3` (`#150`).
  - [x] P15.3a Annex the P15 archive and manifest.
  - [x] P15.3b Copy both artifacts to `arbutus-s3`.
  - [x] P15.3c Verify `git annex whereis` reports local and `arbutus-s3`
    copies for both artifacts.
  - [x] P15.3d Update archive QA status to
    `published_materialization_pending`.
- [ ] P15.4 Prove no-credential clean-checkout materialization (`#151`).
- [ ] P15.5 Run direct launch and scenario smoke from materialized archive
  (`#152`).
- [ ] P15.6 Document publication, caveats, and replacement-candidate status
  (`#153`).
- [ ] P15.7 Decide replacement-candidate readiness and close Phase 15 (`#154`).

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
8. **MP11 implementation foundation**: Phase 8 (`#58`) locks public-data
   contracts and promotion rules before any source-layer, yield, model-input,
   XML, Matrix Builder, or runtime rebuild begins.
9. **MP11 source-layer and THLB rebuild**: Phase 9 (`#66`) executes the
   accepted source-layer and THLB contract.
10. **MP11 AU/yield readiness and blocker scoping**: Phase 10 (`#67`) extracts
    managed-yield parameter evidence, refreshes crosswalks, and records the
    blockers that prevent immediate curve rebuilding.
11. **MP11 curve parser and curve rebuild**: Phase 10R (`#92`) parses MP11
    Tables 54, 55, and 57, builds BatchTIPSY/TIPSY handoff inputs, runs/parses
    managed curves where supported, and refreshes curve plots or records a
    blocker package.
12. **Public DEM steep-slope proxy repair**: Phase 9D (`#100`) materializes a
    public DEM route, derives slope evidence, and locks or defers MP11 Table 12
    Step 220 before THLB promotion.
13. **MP11 model-input/XML rebuild**: Phase 11 (`#68`) promotes accepted
    source, curve, rule, and reporting contracts into model-input and
    ForestModel XML artifacts.
14. **MP11 runtime smoke**: Phase 12 (`#69`) builds and smoke-tests Matrix
    Builder and Patchworks runtime artifacts.
15. **MP11 comparison/release QA**: Phase 13 (`#70`) documents comparisons,
    release readiness, and whether an MP11-aligned package replaces or
    supplements the Phase 5 teaching baseline.
16. **MP11 harvest-system operability integration**: Phase 14 (`#138`) builds a
    public-proxy ground/cable/heli classifier, then rebuilds candidate
    model-input, XML, Matrix Builder, runtime, and scenario-smoke surfaces only
    after P14.1 records the plan and output boundaries.
17. **MP11 harvest-system runtime publication and replacement-candidate QA**:
    Phase 15 (`#147`) publishes the Phase 14 harvest-system runtime archive,
    proves no-credential clean-checkout materialization, reruns direct launch
    and all-system/no-heli scenario smoke from the materialized archive, and
    records whether the candidate is ready for replacement review without
    silently replacing Phase 5.

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

0. Phase 15 is active on branch
   `feature/tfl6-mp11-p15-runtime-publication`. P15.1 (`#148`) is complete:
   the parent issue `#147` and child issues `#148` through `#154` are open,
   `planning/tfl6_mp11_phase15_publication_replacement_candidate_plan.md`
   records the Phase 14 source-runtime boundary, publication artifact names,
   release-status vocabulary, hard validation gates, WFP LBB caveats, and Phase
   5 baseline boundary. P15 consumes the completed Phase 14 harvest-system
   runtime, not the older P13 candidate archive. P15.2 (`#149`) is complete:
   `scripts/build_p15_harvest_system_archive_publication_qa.py` built local
   archive `releases/tfl6_mp11_harvest_system_candidate_runtime_p15_2.zip`,
   emitted manifest
   `releases/tfl6_mp11_harvest_system_candidate_runtime_p15_2_manifest.yaml`,
   and wrote `planning/tfl6_mp11_phase15_archive_publication_qa.{csv,json,md}`.
   The archive contains `46` files, includes both all-system `tracks/` and
   no-heli `tracks_no_heli/`, passed ZIP integrity/member-count checks, and has
   SHA256 `fcf8d3615f8bba65419d1a401d818c5eb87e7d75d3aa6007cfa6ada773536362`.
   P15.3 (`#150`) is complete: the archive and manifest were annexed, copied
   to `arbutus-s3`, verified with `git annex whereis` as present both locally
   and on `arbutus-s3`, and the archive QA status was updated to
   `published_materialization_pending`. `git annex info arbutus-s3` reports
   public remote metadata and `5` remote keys. The next bounded task is P15.4
   (`#151`): prove no-credential clean-checkout materialization.

Historical leading-edge notes below are retained for audit context only; the
active next step is P15.4.

0. Phase 14 is active on branch
   `feature/tfl6-mp11-harvest-system-operability`. P14.1 (`#139`) is complete:
   the parent issue `#138` and child issues `#139` through `#146` are open,
   `planning/tfl6_mp11_phase14_harvest_system_operability_plan.md` records the
   MP11 source anchors, WFP LBB/public-proxy boundaries, generated-output roots,
   and non-goals, and no model-input tables, ForestModel XML, Matrix Builder
   outputs, Patchworks runtime artifacts, or scenario outputs were generated.
   P14.2 (`#140`) is complete:
   `scripts/build_p14_harvest_system_evidence.py` emits
   `planning/tfl6_mp11_phase14_harvest_system_evidence.{csv,json,md}` with
   `16` evidence rows. The inventory records WFP LBB as unavailable/private,
   MP11 Table 20 and Table 73 as aggregate comparison targets, P9D CDED slope
   and VRI/VDYP inventory attributes as public proxy inputs, DRA roads as an
   access-distance candidate needing review, and MP11 helicopter economic
   thresholds as candidate rules after metric build. P14.3 (`#141`) is
   complete:
   `scripts/build_p14_public_proxy_metrics.py` emits
   `planning/tfl6_mp11_phase14_public_proxy_metrics.{csv,json,md}` with
   `25,019` stand-level metric rows, `22,614` managed-current-THLB rows,
   `17,395` rows with P9D slope joins, all rows with nearest-DRA-road distance,
   and `3,326` rows passing the public-proxy helicopter economic test. These
   metrics are inputs to P14.4 only; they are not accepted harvest-system
   classifications and they do not generate model-input tables, XML, Matrix
   Builder outputs, Patchworks runtime artifacts, or scenarios. P14.4 (`#142`)
   is complete:
   `scripts/build_p14_harvest_system_classification.py` emits
   `planning/tfl6_mp11_phase14_harvest_system_classification.{csv,json,md}` and
   `planning/tfl6_mp11_phase14_harvest_system_classification_qa.csv`. The
   public-proxy classifier assigns `80,241.389 ha` to ground, `56,677.061 ha`
   to cable, and `3,077.349 ha` to heli over `139,995.798 ha` of managed
   current THLB in the candidate scaffold. Normalized area-share residuals
   against MP11 Table 73 are `+0.017` percentage points for ground, `+0.885`
   for cable, and `-0.902` for heli; direct residuals remain caveated because
   the candidate scaffold total is larger than the MP11 Table 73 total and WFP
   LBB geometry is unavailable. P14.5 (`#143`) is complete:
   `scripts/build_p14_harvest_system_model_input_xml.py` creates the ignored
   `data/mp11_harvest_system_model_input_bundle/` candidate bundle, generates
   ignored ForestModel XML/fragments under
   `output/patchworks_tfl6_mp11_harvest_system_candidate/`, and emits
   `planning/tfl6_mp11_phase14_model_input_xml_build_summary.{csv,json,md}`.
   The generated XML has `814` `CC_GROUND`, `814` `CC_CABLE`, and `814`
   `CC_HELI` treatment nodes, `2,442` `HVSYS` split managed selects, `2,442`
   split product selects, and zero remaining `treatment eq 'CC'` product
   selects. Matrix Builder, runtime assembly, and scenarios remain
   `not_performed`. P14.6 (`#144`) is complete:
   `config/patchworks.runtime.mp11_harvest_system_candidate.windows.yaml`
   points Matrix Builder to the harvest-system XML/fragments and tracks root.
   Matrix Builder run `tfl6_mp11_harvest_system_p14_6_matrix_build` returned
   `0`, generated `13` track files, `93,330` feature rows, `829` account rows,
   `46,605` product rows, `18,642` treatment rows, `0` message rows, and
   restored managed area to `139,995.785 ha` after the XML `HVSYS` field was
   bound to the fragment `HVSYS` column. Split track evidence includes `10,790`
   `CC_GROUND`, `6,960` `CC_CABLE`, and `892` `CC_HELI` treatment rows.
   Runtime blocks/topology were assembled under
   `models/tfl6_patchworks_model_mp11_harvest_system_candidate/` with `24,879`
   block rows, `191,168.566447 ha`, valid `EPSG:3005` geometry, and `170,759`
   topology rows. P14.7 (`#145`) is complete:
   `scripts/build_p14_no_heli_tracks.py` creates an ignored `tracks_no_heli/`
   variant that removes `CC_HELI` treatment, product, account, and protoaccount
   rows. The no-heli repair fixed the Patchworks startup failure where stale
   account rows caused `flow.even.product.HarvestedVolume.managed.Total.CC_HELI`
   to be defined after the matching product account was removed. Direct launch
   smoke, all-system 200,000-iteration harvest smoke, and no-heli
   200,000-iteration harvest smoke all passed. The all-system schedule recorded
   `76,635` rows across `CC_CABLE`, `CC_GROUND`, and `CC_HELI`; the no-heli
   schedule recorded `75,086` rows across `CC_CABLE` and `CC_GROUND`, with no
   `CC_HELI` scheduled treatments. P14.8 (`#146`) is complete:
   `planning/tfl6_mp11_phase14_closeout.md` and
   `docs/phase14-mp11-harvest-system-operability.rst` document the Phase 14
   caveats, comparison evidence, runtime status, teaching use, and closeout
   boundary. Phase 14 is complete. Phase 5 remains the accepted public
   teaching/runtime baseline; the MP11 harvest-system runtime is a caveated
   candidate supplement. Future archive publication, clean-checkout
   materialization, broader KPI calibration, or Phase 5 replacement work should
   open a new issue or phase.

Historical leading-edge notes below are retained for audit context only; the
Phase 14 lane has no active next step.

0. Phase 11 is active on branch
   `feature/p11-model-input-xml-rebuild-plan`. P11.1 and P11.2 are complete.
   `planning/tfl6_mp11_phase11_model_input_xml_execution_plan.md` audits the
   governing MP11 promotion contracts, the repaired P9RF THLB endpoint, the
   accepted 27-curve Phase 10R handoff, the deferred Tables 54/55 boundary, and
   the stop conditions that governed candidate-only readiness resolution.
   `planning/tfl6_mp11_phase11_phase5_provenance_inventory.{csv,json,md}`
   inventories the Phase 5 model-input bundle, export bridge, ForestModel XML,
   fragments, Matrix Builder tracks, runtime package, smoke evidence, and public
   release archive. `planning/tfl6_mp11_phase11_artifact_layout.{csv,json,md}`
   defines MP11 candidate generated roots, write gates, `.gitignore` rules, and
   the Phase 5 baseline protection rule.
   `planning/tfl6_mp11_phase11_promotion_gates.{csv,json,md}` defines the
   hard and soft gates P11.2 must evaluate before P11.3 can write candidate
   model-input tables or P11.4 can attempt XML readiness.
   `scripts/build_p11_mp11_promotion_readiness.py` emits
   `planning/tfl6_mp11_model_input_promotion_readiness.{csv,json,md}`. P11.2
   resolves the three former hard blockers through candidate-only source/THLB,
   rule-field, and schema-bridge decisions in
   `planning/tfl6_mp11_p11_2_candidate_scaffold_decisions.md` and
   `planning/tfl6_mp11_p11_2_candidate_schema_bridge.{csv,json,md}`. The
   readiness manifest reports `11` gates, `0` blocked hard gates, `2`
   deferred soft gates, `9` passing gates, and P11.3 unlock status
   `candidate_manifest_eligible`.
   `planning/tfl6_mp11_p11_3_readiness_consumption.{json,md}` records P11.3a
   consumption of the readiness manifest and preserves the candidate-only
   caveats. `scripts/build_p11_mp11_candidate_manifest.py` emits
   `planning/tfl6_mp11_model_input_candidate_manifest.{csv,json,md}` with `13`
   table roles: `12` eligible for a later generated scaffold and `1` deferred
   not eligible role (`harvest_system_table`).
   `scripts/build_p11_mp11_candidate_provenance_review.py` emits
   `planning/tfl6_mp11_model_input_candidate_provenance_review.{csv,json,md}`;
   the P11.3c review records `12` passing candidate-scaffold roles, `1`
   non-blocking deferred comparison-metadata role, `0` blocked roles, and
   P11.4a unlock status `p11_4a_audit_eligible`. P11.3 is complete.
   `scripts/build_p11_mp11_xml_provenance_audit.py` emits
   `planning/tfl6_mp11_phase11_xml_provenance_audit.{csv,json,md}`. The P11.4a
   audit records `8` XML/component families, `7` families requiring P11.4b
   readiness decisions, `1` non-blocking deferred harvest-system family, `0`
   missing required Phase 5 notes, and P11.4b unlock status
   `p11_4b_readiness_eligible`.
   `scripts/build_p11_mp11_xml_readiness.py` emits
   `planning/tfl6_mp11_forestmodel_xml_readiness.{csv,json,md}`. The first
   P11.4b output is a stop report: `8` component families evaluated, `0` ready,
   `7` blocked on missing MP11 candidate bundle/export-bridge outputs, `1`
   non-blocking deferred harvest-system family, and P11.4c generation status
   `blocked_missing_candidate_outputs`. That stop report is evidence of the
   missing build input, not the endpoint. Issue `#89` is reopened. The next
   bounded move is P11.4c: build the generated MP11 candidate model-input
   bundle and export compatibility bridge under `data/mp11_model_input_bundle/`.
   P11.4c is complete: `scripts/build_p11_mp11_candidate_bundle.py` builds the
   generated MP11 candidate scaffold under `data/mp11_model_input_bundle/` and
   emits `planning/tfl6_mp11_candidate_bundle_build_summary.{csv,json,md}`.
   The scaffold injects `18` active Phase 10R MP11 Table 57 managed curves
   across `648` curve-point rows, affects `8,957` stand rows, defers `9`
   duplicate Table 57 rows that map to already-selected canonical AU identities,
   and regenerates the export compatibility bridge with `172` curve rows and
   `30,651` curve-point rows. P11.4d reran XML readiness and now reports `7`
   ready component families, `0` blocked, `1` non-blocking deferred
   harvest-system family, and P11.4c generation status `eligible`. P11.4e
   generated `output/patchworks_tfl6_mp11_candidate/forestmodel.xml` and
   fragments from the MP11 candidate bridge. P11.4f records QA in
   `planning/tfl6_mp11_forestmodel_xml_generation_qa.{csv,json,md}`: XML root
   `ForestModel`, `13,197` curve nodes, `2,442` select nodes, `814` treatment
   nodes, `24,879` fragment rows, and `191,168.566447 ha` fragment area. P11.4
   is complete. The next bounded move is P11.5: define the Phase 12 runtime
   handoff package for Matrix Builder/runtime work without running it in Phase
   11.
   P11.5 is complete: `scripts/build_p11_mp11_phase12_runtime_handoff.py`
   emits `planning/tfl6_mp11_phase12_runtime_handoff.{csv,json,md}` with
   handoff status `phase12_runtime_handoff_ready`. The handoff points P12.2 to
   `output/patchworks_tfl6_mp11_candidate/forestmodel.xml` and fragments,
   records the generated candidate bundle/export bridge inputs, preserves the
   candidate-scaffold caveats, and keeps Matrix Builder, runtime assembly,
   scenario smoke, and release QA marked `not_performed`. The next bounded move
   is P11.6: close Phase 11 and hand off model-input/XML status.
   P11.6 is complete: `scripts/build_p11_mp11_phase11_closeout.py` emits
   `planning/tfl6_mp11_phase11_closeout.{csv,json,md}` with status
   `complete_model_input_xml_handoff`. Phase 11 built
   `data/mp11_model_input_bundle/`,
   `output/patchworks_tfl6_mp11_candidate/forestmodel.xml`, and
   `output/patchworks_tfl6_mp11_candidate/fragments/fragments.shp`, preserved
   the Phase 5 teaching/runtime baseline, and left Matrix Builder/runtime
   outputs uncreated. The next bounded move is P12.1/P12.2: launch the runtime
   build issues and run Matrix Builder from the candidate XML/fragments.
   P12.1 is complete on branch `feature/p12-mp11-runtime-build`: child issues
   `#114` through `#119` now define the Phase 12 runtime-build sequence,
   `planning/tfl6_mp11_phase12_runtime_build_execution_plan.md` records the
   execution plan, and `config/patchworks.runtime.mp11_candidate.windows.yaml`
   points Matrix Builder at the MP11 candidate XML/fragments and candidate
   tracks root. The next bounded move is P12.2: run
   `python -m femic patchworks matrix-build --instance-root
   external/femic-tfl6-instance --config
   config/patchworks.runtime.mp11_candidate.windows.yaml --run-id
   tfl6_mp11_candidate_p12_2_matrix_build`, then inspect the generated
   `tracks/` surfaces before any runtime success claim.
   P12.2 is complete on branch `feature/p12-2-mp11-matrix-builder`: Matrix
   Builder generated 13 expected track CSV files under
   `models/tfl6_patchworks_model_mp11_candidate/tracks/`, and
   `scripts/build_p12_mp11_matrix_builder_tracks_qa.py` recorded
   `planning/tfl6_mp11_matrix_builder_tracks_qa.{csv,json,md}` with status
   `matrix_builder_tracks_generated_inspection_pass`. The QA records `86,574`
   feature rows, `823` account/protoaccount rows with account sync equality,
   `1,004,368` curve rows, `47,218` block rows, `0` message rows, no manifest
   failures, and block area `191,168.565448 ha` versus Phase 11 fragment area
   `191,168.566447 ha`. The next bounded move is P12.3: assemble the candidate
   runtime package from the generated tracks without claiming release
   readiness.
   P12.3 is complete on branch `feature/p12-3-mp11-runtime-package`: block and
   topology build generated `24,879` block rows and `170,759` topology rows
   under `models/tfl6_patchworks_model_mp11_candidate/blocks/`; compact launch
   surfaces, README, and lineage registry were assembled under
   `models/tfl6_patchworks_model_mp11_candidate/`; and
   `scripts/build_p12_mp11_runtime_package_manifest.py` recorded
   `planning/tfl6_mp11_runtime_package_manifest.{csv,json,md}` with status
   `candidate_runtime_package_assembled_pending_launch_smoke`. The next
   bounded move is P12.4: direct launch smoke from
   `models/tfl6_patchworks_model_mp11_candidate/analysis/base.pin`.
   P12.4 is complete on branch `feature/p12-4-mp11-direct-launch`: direct
   headless launch run `tfl6_mp11_candidate_p12_4_launch0` returned code `0`,
   saved `3,359` stage files under
   `models/tfl6_patchworks_model_mp11_candidate/analysis/p12_4_launch0`, and
   recorded `planning/tfl6_mp11_direct_launch_qa.{csv,json,md}` with status
   `direct_launch_smoke_pass`. The QA records terminal state `success`,
   detected marker `[FEMIC headless] saveStage completed`, `824`
   `targetStatus.csv` rows, `25,544` `targetSummary.csv` rows, `0`
   `schedule.csv` rows for the no-iteration launch, and no stdout/stderr
   warning or error matches. The next bounded move is P12.5: representative
   base/sensitivity scenario smoke.
   P12.5 is complete on branch `feature/p12-5-mp11-scenario-smoke`: the
   candidate headless scenario helper now activates the base harvested-volume
   target with a linear `20,000,000` per-period minimum, runs 1,000 seed
   iterations plus a 5-second active dwell before even-flow activation, then
   runs the even-flow target with default non-linear penalty shape and
   min/max weights `10,000` for `200,000` iterations. Scenario run
   `tfl6_mp11_candidate_p12_5_harvest_smoke200k` returned code `0`, saved
   `3,359` files, wrote `76,726` managed `CC` schedule rows, retained nonzero
   final-period base harvested volume `14,104,784`, and recorded
   `planning/tfl6_mp11_scenario_smoke_qa.{csv,json,md}` with status
   `scenario_smoke_pass`. P12.6 then closed the runtime-smoke lane with
   `planning/tfl6_mp11_phase12_runtime_closeout.{csv,json,md}`, verified the
   generated runtime outputs are present, updated candidate runtime lineage,
   and handed Phase 13 a candidate runtime smoke-pass package. P13.1 records
   the initial candidate-runtime positioning: the local interactive MP11
   candidate run produced approximately `1.15 million m3/year`, which is
   plausibly close to the MP11 base-case/LRSY evidence given a slightly larger
   public-data THLB and missing WFP constraints, but remains candidate evidence
   rather than release QA or WFP model equivalence. Phase 13 now has an
   explicit execution plan in
   `planning/tfl6_mp11_phase13_comparison_release_qa_plan.md` and child issues
   `#127` through `#131`. P13.1b (`#127`) produced
   `planning/tfl6_mp11_phase13_scenario_comparison.{csv,json,md}` and
   `planning/tfl6_mp11_phase13_scenario_period_comparison.csv`, separating the
   MP11 base-case target, adjusted-LRSY context, P12.5 tracked smoke output,
   and maintainer interactive context. P13.2 (`#128`) produced
   `planning/tfl6_mp11_phase13_kpi_caveat_report.{csv,json,md}` with `42`
   comparison rows, evidence labels, blocker/caveat counts, and release
   implications. P13.3 (`#129`) added the public Sphinx page
   `docs/phase13-mp11-candidate-runtime.rst`, clarifying that Phase 5 remains
   the accepted teaching/runtime baseline while the MP11 candidate is a
   smoke-tested comparison and advanced teaching surface pending archive QA and
   release-status decision. P13.4 (`#130`) built a local ignored MP11 candidate
   archive, tracked the archive/materialization QA in
   `planning/tfl6_mp11_phase13_archive_materialization_qa.{csv,json,md}`, and
   recorded the archive manifest at
   `releases/tfl6_mp11_candidate_runtime_p13_4_manifest.yaml`. The candidate
   archive passed local ZIP integrity and checksum checks but remains
   unpublished, so clean-checkout materialization is pending publication or the
   P13.5 release decision. P13.5 (`#131`) recorded
   `planning/tfl6_mp11_phase13_release_decision.{csv,json,md}` and selected
   `supplement_phase5`: the MP11 candidate runtime is a documented,
   smoke-tested supplement for MP11 comparison and advanced teaching, while
   Phase 5 remains the accepted public runtime baseline. Phase 13 is complete.
   Future work should open a new issue/phase if the candidate archive is to be
   annexed/published, no-credential materialization-tested, or promoted toward
   replacing Phase 5.
0. Phase 9D and Phase 9E are complete. Step 210 now applies the public TSM
   strict Class V proxy, deducting `1.425 ha` against the MP11 Step 210 target
   `1,993.000 ha`; this is an explicit public-source coverage/semantic gap, not
   a skipped row. Step 220 applies the public CDED proxy, deducting
   `1,801.705 ha` against the MP11 Step 220 target `1,820.000 ha`. After the
   full P9RF rerun, Step 290 Current THLB is `122,763.421 ha` (`+2,664.421 ha`
   versus MP11), and Step 310 Long-term Land Base is `121,336.593 ha`
   (`+2,664.593 ha` versus MP11).
1. Phase 10R is closed on branch
   `feature/p10r-curve-rebuild-roadmap-correction`.
   `planning/tfl6_mp11_phase10r_curve_rebuild_execution_plan.md` records the
   actual curve-rebuild issue tree, artifact layout, parser gates,
   curve-generation gates, plot refresh expectations, and Phase 11 handoff.
   P10R.2 parsed MP11 Tables 54, 55, and 57 into
   `planning/tfl6_mp11_tipsy_row_parse.{csv,json,md}`: `141` rows total
   (`79` Table 54, `34` Table 55, `28` Table 57), with `132`
   high-confidence parser candidates and `9` rows retained as
   review-required. P10R.3 now emits
   `planning/tfl6_mp11_tipsy_handoff.{csv,json,md}` plus
   `planning/tfl6_mp11_tipsy_handoff_map.csv` from the canonical top-N AU
   universe: all `27` Table 57 future-managed candidate rows are
   handoff-ready, `105` existing/recent rows are deferred pending a public MP11
   AU-code to BEC/site-series mapping, and `9` rows remain parser
   review-required. `FMH01` and `FMH22` are accepted through target AU
   `cwhvm2_hw_ba_l`, so their emitted TIPSY BEC is `CWH/vm` and their emitted
   TIPSY SI is the target AU VRI median SI `14.0`; they reuse the valid
   canonical `cwhvm2_hw_ba_l` future-managed TIPSY curve instead of generating
   duplicate FMH row-derived BTC curves. The locked recipe is
   `scripts/run_p10r_mp11_curve_generation_recipe.py` and
   `planning/tfl6_mp11_curve_generation_recipe.md`. It uses FEMIC's existing
   `python -m femic tipsy run-btc ...` surface and writes
   `planning/tfl6_mp11_curve_generation_recipe_lock.json` with command
   provenance, validation results, and SHA-256 hashes. The recipe uses the
   target canonical top-N AU VRI BEC and median SI as TIPSY inputs for every
   candidate row; parsed MP11 per-species SI is retained only as provenance.
   The current BTC rerun returns manifest status `ok`, exit code `0`, `25`
   output rows, and `0` error rows under ignored
   `runtime/mp11_yield/`. The parsed review surfaces are
   `planning/tfl6_mp11_managed_curves.{csv,json}` with `972` age-by-curve rows
   and regenerated `planning/tfl6_mp11_managed_curve_rebuild.{csv,json,md}`
   with `generated_curve_output_inspected`. P10R.4e emits
   `planning/tfl6_mp11_managed_curve_comparison.{csv,json,md}`: all `27`
   candidates match comparison references and are accepted for Phase 11 handoff.
   P10R.5 emits
   `planning/tfl6_mp11_vdyp_natural_curve_slice.{csv,json}` and
   `planning/tfl6_mp11_tipsy_vdyp_diagnostic_manifest.{csv,json,md}` with
   `27` AU-wise MP11 TIPSY-vs-public-VDYP diagnostic plots under ignored
   `plots/mp11_tipsy_vdyp_diagnostics/`. The diagnostic validation finds no
   handoff `MH/mm` candidates, no plotted BEC mismatches, no target AU BEC
   mismatches, no positive SI column differing from `tipsy_input_si`, and no
   missing/empty plots. The accepted handoff has `25` BTC-generated curves and
   `2` canonical-curve reuse rows. Every generated row remains
   `not_model_input` until Phase 11 writes model-input tables. The obsolete
   rejected-curve audit generated
   before the canonical-top-N / VRI-median-SI repair has been removed from the
   active artifact set. The Phase 10R closeout is
   `planning/tfl6_mp11_phase10r_curve_rebuild_closeout.md`. P10R.6d final
   validation passed: the locked recipe reran, Ruff passed on active
   recipe/generator scripts, Sphinx built warning-clean, and stale-state /
   personal-path hygiene searches were clean. P10R.6e records the accepted
   27-curve Phase 11 handoff: P11.1 should now launch the model-input/XML
   rebuild from that locked curve surface. Tables 54/55 remain deferred unless
   a later public-safe existing/recent AU-code mapping is supplied.
2. Phase 7 is closed. PR `#56` merged the MP11 figure-extraction test
   closeout into `main`. The final closeout surface is
   `planning/tfl6_mp11_figure_extraction_closeout.md` with matching CSV/JSON.
   Phase 7 inventoried `61` figures, reviewed all `36` high-priority figures,
   promoted `22` figures to `accepted_for_comparison`, assigned `14` figures
   to `reviewed_for_planning`, deferred `20` medium-priority figures, and kept
   `5` context figures as inventory-only. Every row remains
   `not_model_input`. The next active edge is Phase 6 MP11 extraction and
   model-overhaul planning from the reviewed figure evidence.
3. Phase 2 is closed. The instance `main` branch contains the Phase 2
   source-layer, THLB smoke, benchmark-tolerance, and Sphinx audit-trail
   surfaces; the parent FEMIC submodule pointer has been updated to the merged
   closeout commit.
4. Continue Phase 3 on branch `feature/p3-model-design-assumptions`. P3.3
   through P3.6 are complete: AU identity, untreated VDYP curves, treated
   BatchTIPSY curves, treatment options, and state-transition logic are locked
   for current design purposes. P3.4 still carries a non-blocking deferred
   option to revisit VDYP smoothing/tail constraints before the final Phase 4
   model-input bundle lock.
4. P3.1b is complete. Cedar source fields and derived signal definitions are
   locked in `planning/tfl6_cedar_signal_design.md` using the accepted
   `planning/tfl6_stand_to_au_review.csv` surface. P3.1b accepts `CW`/`YC`
   leading and component signals, the `>= 20%` cedar-present threshold, and the
   `>= 141` age proxy for `old_cedar`. It leaves `large_cedar_proxy`,
   utility-pole thresholds, cedar-specific treatments, and cedar-specific
   products/accounts to P3.1c.
5. P3.1c and P3.1 are complete. The cedar design lane now defines
   Patchworks-facing product hooks, feature/account families, report/target
   families, treatment-hook boundaries, yield-curve boundaries, and Phase 4
   handoff fields in `planning/tfl6_cedar_signal_design.md`. The first bundle
   should carry cedar reporting surfaces, but it must not create cedar-specific
   base treatments, hard cedar reserve targets, utility-pole grade claims, or
   cedar-only yield-curve families.
6. P3.2b is complete. The accepted K3Z/NICF core source is the original K3Z
   tenure boundary from `external/femic-k3z-instance`, but non-mutating overlay
   diagnostics show that the current FADM-derived TFL 6 AOI intersects only
   `0.072 ha` of that `2391.511 ha` K3Z tenure. The first bundle must not
   silently relabel the broader FDU 1/2/3 planning context as
   `nicf_k3z_core`; K3Z core should be treated as a source/provenance identity
   and likely external/reference carve-out under the current TFL 6 boundary.
7. P3.2c is complete and corrected after maintainer clarification. Expansion
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
