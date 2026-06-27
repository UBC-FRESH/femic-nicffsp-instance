# TFL 6 Phase 5 Release QA

## Purpose

This checklist records final release QA for the first TFL 6 teaching runtime
package. It is the Phase 5 closeout evidence surface for issue `#40` under
Phase 5 parent `#15`.

The goal is to prove that the release is public, documented, materializable,
launch-smoked, and honest about its first-release limitations. This checklist
does not reopen model design, THLB netdown, yield curves, Matrix Builder, or
runtime-package construction unless QA exposes a release-blocking defect.

## Release Inputs

- Runtime archive: `releases/tfl6_patchworks_runtime_p5_2.zip`
- Runtime manifest: `releases/tfl6_patchworks_runtime_p5_2_manifest.yaml`
- Public annex remote: `arbutus-s3`
- Runtime launch file inside package:
  `models/tfl6_patchworks_model/analysis/base.pin`
- Representative harvest product:
  `product.HarvestedVolume.managed.Total.CC`
- Release docs:
  - `docs/phase5-runtime-release.rst`
  - `docs/phase5-runtime-quickstart.rst`
  - `docs/phase5-rebuild-provenance.rst`
  - `docs/phase5-scenario-teaching-workflows.rst`
  - `docs/phase5-known-limitations-release-readiness.rst`

## QA Checklist

| ID | Check | Evidence | Result | Notes |
| --- | --- | --- | --- | --- |
| P5.4a | Create release-QA issue and checklist surface. | Issue `#40`; this file; Phase 5 parent `#15` body updated. | Pass | Created before executable QA checks. |
| P5.4b | Verify archive, manifest, and public materialization. | Fresh no-credential clone on `feature/p5-publication-release`; `git annex enableremote arbutus-s3`; `git annex info arbutus-s3`; `git annex get` archive and manifest; `git annex fsck`; Python SHA/size/ZIP-member validation. | Pass | `creds: not available`; `public: yes`; `remote annex keys: 2`; archive SHA256 `17f56d11faeba89170fc48e202d1bfe83c2dd40b53e7409d8cdb8c1c487c2f9f`; size `28000736`; ZIP members `31`; required launch/XML/tracks/block members present. |
| P5.4c | Verify Patchworks launch and baseline signal smoke evidence. | `lineage_registry.yaml`; saved-stage target CSVs under `models/tfl6_patchworks_model/analysis/p44d_harvest_smoke200/`; release ZIP member/track-table inspection. | Pass | Accepted launch run `tfl6_p44b_launch0` returned `0` and wrote `903` saved-stage files; scenario smoke `tfl6_p44d_harvest_smoke200` returned `0`, wrote `903` saved-stage files, scheduled `801` managed `CC` rows, and produced nonzero managed `CC` harvested-volume, treated-area, managed/unmanaged area, and managed/unmanaged yield signals. The release ZIP contains the launch helpers, ForestModel XML, and track tables carrying the required baseline signal names. |
| P5.4d | Verify docs build, docs links, and published Pages surface. | Local `sphinx-build -b html docs docs/_build/html -W`; generated HTML checks for RTD theme and Phase 5 links; manual GitHub Actions `docs-pages` deploy from `feature/p5-publication-release`; public Pages HTTP checks. | Pass | Local Sphinx build passed warning-clean. Generated index uses RTD theme and links Phase 5 pages. Public root returned `200`, showed Phase 5 content and RTD theme markup, and all five Phase 5 pages returned `200`. Quickstart public page contains archive, `arbutus-s3`, `base.pin`, and `product.HarvestedVolume.managed.Total.CC` references. A narrow `github-pages` environment branch policy for `feature/p5-publication-release` was required before the manual deploy could publish the release-branch docs. |
| P5.4e | Close Phase 5 after QA evidence is recorded. | This checklist; `ROADMAP.md`; `CHANGE_LOG.md`; final closeout comments on issues `#40` and `#15`; issue closure for `#40` and `#15`. | Pass | Final QA evidence is recorded, deferred follow-on scope is explicit, and Phase 5 issue closeout is complete. |

## Deferred Follow-On Scope

The following items are documented follow-on work and do not block the first
teaching release:

- ground/cable/heli harvest-system modeling;
- geometry-backed strategic RMZ replacement;
- outside-AOI NICF expansion implementation;
- cedar-specific reserve or utility-pole-grade policy design;
- VDYP/TIPSY sensitivity projects; and
- production-grade economic modeling.

## Current Status

P5.4e is complete. The first TFL 6 teaching runtime release has passed final
release QA: public archive materialization, manifest/SHA checks, Patchworks
launch and baseline signal smoke evidence, warning-clean Sphinx build, and
public Pages checks are all recorded above. Deferred modeling improvements
remain documented follow-on scope and do not block the first teaching release.
Issues `#40` and `#15` are ready to close after the final closeout comments are
posted.
