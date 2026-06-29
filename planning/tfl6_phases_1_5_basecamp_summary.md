# TFL 6 FEMIC Teaching Instance: Phases 1-5 Progress Summary

We have completed the first end-to-end build and release cycle for the new `femic-tfl6-instance` teaching model. The project started as a small NICF/FSP oriented instance but was deliberately pivoted to a broader Tree Farm Licence 6 teaching model so students can work with a larger, realistic forest estate context that embeds NICF/K3Z interests inside the surrounding WFP-managed TFL 6 landbase.

The first teaching release is now public, documented, materializable, launch-smoked, and explicitly bounded by known limitations and follow-on work.

## Phase 1: Bootstrap, AOI Pivot, and Build Plan

We created the standalone `femic-tfl6-instance` repository and added the standard project control surfaces: roadmap, changelog, planning notes, agent contract, issue hierarchy, and release workflow expectations.

The original working area was based on NICF/FSP source material, including FDU 1/2/3 boundaries. Early source inspection confirmed those data were useful provenance, but the active model area was later pivoted to Tree Farm Licence 6. We normalized that pivot in the project documentation and planning notes so the FDU/FSP material is retained only as historical/provenance context.

We materialized and indexed the key input data needed for the TFL 6 build:

- authoritative TFL 6 boundary from the provincial FADM TFL layer;
- 2025 VRI R1 polygon inventory;
- 2025 VDYP7 polygon/layer packages;
- the TFL 6 Management Plan 10 and 2011 information package PDFs;
- additional TFL 6 reference and instrument documents.

We also built a searchable local reference-document index and extracted key THLB/netdown planning evidence from the 2011 TSR/management-plan material. Instrument 101 and related boundary-change notes were used to explain much of the difference between the historical 2011 gross landbase and the current FADM-derived TFL 6 AOI.

Phase 1 ended with a proper issue-tree and roadmap structure for Phases 2-5, rather than ad hoc "next slice" work.

## Phase 2: Reviewed Source Layers and THLB Netdown

Phase 2 turned the source-layer planning into an executable THLB netdown lane.

We resolved and reviewed public/reference source layers for the THLB recipe, including:

- forest inventory fields from 2025 R1/VDYP;
- non-forest and non-productive indicators;
- deciduous-leading and productivity filters;
- OGMA and other spatial/static exclusions where available;
- strategic RMZ and other assumptions where spatial data were incomplete;
- operability as a separate proxy/sensitivity lane rather than a hard-coded one-off assumption.

A key methodological decision was to document unresolved source-layer gaps explicitly rather than pretending we had perfect historical geometry. For example:

- strategic RMZ was treated as an aspatial fallback unless geometry is later recovered;
- cultural/sensitive heritage geometry was not pursued directly;
- operability was given its own planning lane because it is both technically fuzzy and pedagogically useful for student sensitivity analysis.

We built and smoke-tested the first executable THLB netdown recipe. During Phase 4 we later found and repaired an AFLB filtering problem, but Phase 2 established the core GLB/AFLB/LHLB/THLB logic and benchmark framework.

The accepted teaching tolerance was locked after comparing reconstructed current-AOI netdown results against scaled historical MP10 benchmark values. The final corrected THLB result was within the accepted teaching tolerance, recognizing that the scaled benchmark depends on the reasonable but unverifiable assumption that the post-2011 extension area has roughly similar THLB rate to the earlier MP10 landbase.

Phase 2 also produced Sphinx documentation explaining the THLB design rationale, benchmark tolerance, caveats, and reproducibility trail.

## Phase 3: Model Design Assumptions, AUs, Yield Curves, Treatments, Transitions

Phase 3 defined the model semantics needed before building Patchworks inputs.

The most important design decision was to prioritize analysis units and yield curves before cedar/NICF details. We locked a static AU scheme based on the K3Z-style pattern:

- BEC/subzone/variant/phase;
- leading species pair;
- low/medium/high site index class;
- top-area stratum selection;
- lexicographic remapping of non-dominant strata to selected dominant strata.

We explicitly rejected the 2011 MP10 age-at-time-zero AU split as the canonical Patchworks AU identity because stand age is dynamic while AU identity should remain stable. The 2011 MP10 AU/TIPSY tables were instead scraped and used as parameter evidence for treated/managed curve generation.

We built both yield-curve lanes:

- natural/untreated VDYP curves using the shared FEMIC smoothing approach and selected top-area AUs;
- treated/managed BatchTIPSY curves using a reviewed crosswalk from the MP10 TIPSY parameter tables.

We generated AU/stratum plots, curve diagnostics, TIPSY parameter libraries, and crosswalk metadata. Some VDYP smoothing/tail behavior was flagged as potentially worth revisiting later, but it was judged good enough to proceed for the first teaching release.

We defined first-release treatment logic:

- base TFL 6 treatment is generic clearcut-and-plant (`CC`);
- CT/fertilization are conceptually reserved for K3Z/NICF and future expansion areas, not the base TFL 6 release;
- ground/cable/heli harvest-system splits are deferred until the DEM/slope/inventory operability signal is reviewed.

We also locked the Patchworks semantic distinction between:

- managed/unmanaged = treatment eligibility;
- natural/treated = curve provenance.

This matters because NTHLB is not "outside the model." The Patchworks stand universe is AFLB. THLB is the managed subset, and NTHLB is the AFLB complement that remains unmanaged/full-retention but still needs VDYP growth curves.

Cedar and NICF/K3Z expansion design were also recorded:

- cedar signals and reporting hooks are present for future scenario work;
- K3Z/NICF identity is preserved as a distinct embedded/reference identity;
- expansion candidates are defined as outside the current TFL 6 AOI, coming from proximal/adjacent public forested land;
- the model is framed for student exploration of tradeoffs between NICF/community objectives and WFP-style fibre supply/value/cost objectives.

Phase 3 Sphinx docs were expanded to cover AU definitions, yield-curve design, cedar/NICF expansion context, and teaching challenges.

## Phase 4: Model Inputs, XML, Matrix Builder, and Patchworks Runtime Package

Phase 4 built the actual Patchworks-facing model package.

We generated the model-input bundle from the reviewed Phase 2/3 artifacts. During this work we caught an important landbase issue: the original GLB-to-AFLB filter had allowed non-treed/non-forested BCLCS rows to survive into AFLB. We created and resolved a Phase 4 blocker to repair this before continuing.

The corrected AFLB/THLB/NTHLB handoff now treats:

- AFLB as the Patchworks fragment universe;
- THLB as the managed subset;
- NTHLB as unmanaged/full-retention forest that still grows on untreated curves.

The corrected core bundle contained:

- about 25,019 AFLB stand rows;
- about 191,169 ha AFLB;
- about 139,996 ha THLB;
- about 51,173 ha NTHLB;
- no missing natural or treated curve assignments;
- sparse TIPSY fallback only as a documented warning;
- harvest-system assignment explicitly deferred as `unassigned_review_required`.

We then generated ForestModel XML and fragments. The initial generic FEMIC exporter expected an older numeric bundle schema, so we built an exporter-compatible bridge mapping the reviewed TFL6 string AU/curve IDs to deterministic numeric IDs. This allowed the generic export path to produce usable XML/fragments while preserving the reviewed TFL6 metadata.

Matrix Builder was then run and QA'd. We repaired a generic succession/export issue and a Windows Matrix Builder settle-time issue before accepting the Matrix Builder outputs. Final track/account surfaces were readable and included the expected generic `CC` product and harvested-volume account surfaces.

The Patchworks runtime package was then assembled:

- block/topology artifacts built from accepted fragments;
- `analysis/base.pin` launch surface added;
- shared headless launch helpers added;
- flow-target helper scripts added;
- direct Patchworks launch smoke passed;
- representative scenario smoke against `product.HarvestedVolume.managed.Total.CC` passed.

The representative smoke run scheduled 801 managed `CC` rows and produced nonzero harvested-volume signal across 30 periods.

Phase 4 was closed after the runtime package had refreshed XML, Matrix Builder tracks/accounts, block/topology artifacts, direct launch smoke, and representative scenario-smoke evidence.

## Phase 5: Publication, Teaching Docs, Release QA

Phase 5 made the runtime usable outside the development environment.

We decided the publication policy:

- compact launch/control surfaces are tracked in Git;
- large/generated runtime artifacts remain ignored by default;
- a reviewed ready-to-launch runtime archive is published through git-annex/DataLad using the instance-local `arbutus-s3` special remote.

We initialized the instance Arbutus special remote and published:

- `releases/tfl6_patchworks_runtime_p5_2.zip`;
- `releases/tfl6_patchworks_runtime_p5_2_manifest.yaml`.

The archive contains the accepted Phase 4 runtime ingredients, including launch scripts, XML/fragments, Matrix Builder tracks, block/topology artifacts, package README, and lineage registry. The manifest records checksums, size, source commits, and included-file metadata.

We proved fresh-environment materialization:

- cloned the instance fresh;
- cleared AWS/S3 credential environment variables;
- enabled `arbutus-s3`;
- fetched the archive and manifest without credentials;
- verified git-annex checksums;
- verified archive SHA256 against the manifest.

We then built full Sphinx teaching documentation in the same style as the other FEMIC teaching instances. The docs now include:

- runtime release overview;
- runtime quickstart for students/instructors;
- rebuild/provenance guide for maintainers;
- scenario teaching workflows;
- known limitations and release-readiness notes;
- Phase 2/3 technical background pages.

The docs were published with the RTD theme at the public GitHub Pages site. During final QA we found that the Pages site was stale because deployment was still `main`-only, so we repaired the workflow to allow explicit manual release-branch deploys while preserving automatic deploys only from `main`. We then verified the public site served the Phase 5 content correctly.

Final release QA passed:

- public archive materialization;
- manifest/SHA verification;
- Patchworks launch and baseline signal smoke evidence;
- warning-clean Sphinx build;
- public Pages checks;
- explicit deferred-scope documentation.

Phase 5 child issue and parent issue were closed, then the instance Phase 5 branch was merged to `main`. The parent FEMIC repository submodule pointer was also updated and merged.

## Current Status

The first TFL 6 FEMIC teaching runtime release is complete.

Students/instructors can now:

- access the public documentation;
- materialize the ready-to-launch runtime archive;
- open the Patchworks package from `base.pin`;
- inspect baseline managed/unmanaged area and yield signals;
- inspect generic managed `CC` harvest-volume outputs;
- use the package as the starting point for scenario exercises.

Maintainers can:

- trace the build through roadmap/changelog/planning notes;
- inspect THLB, AU/yield, treatment, transition, XML, Matrix Builder, and runtime-package provenance;
- rebuild or extend the model using the documented surfaces.

## Known Follow-On Work

The first release is deliberately a teaching-ready baseline, not a final production-grade TFL 6 forest estate model. Follow-on work should be opened as new issues/phases rather than reopening Phase 5.

Key follow-ons:

- split generic `CC` into ground/cable/heli harvest systems after DEM/slope/inventory operability logic is reviewed;
- replace strategic RMZ aspatial fallback with geometry-backed RMZ netdown if spatial polygons are recovered;
- implement outside-AOI NICF expansion candidate areas;
- develop cedar-specific reserve, utility-pole-grade, product/account, and treatment logic;
- revisit VDYP/TIPSY smoothing and sensitivity scenarios;
- add more advanced economic/cost/value signals for stakeholder tradeoff work.

The release is strong enough for course planning and early teaching use. It gives students a realistic, inspectable forest estate model with documented compromises and several meaningful project directions.
