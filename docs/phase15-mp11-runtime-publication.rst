Phase 15 MP11 Runtime Publication
=================================

Phase 15 publishes and validates the Phase 14 MP11 harvest-system candidate
runtime. The goal is practical: prove that a clean checkout can materialize the
published archive from ``arbutus-s3``, unpack it, launch Patchworks, and run the
same all-system and no-heli smoke scenarios from the archive payload.

Phase 15 does not silently replace Phase 5. The completed Phase 5 runtime
remains the accepted public teaching/runtime baseline until a later explicit
replacement acceptance decision is made.

Status Boundary
---------------

The Phase 15 runtime is a published and materialized replacement candidate. It
is still not Western Forest Products' unpublished internal Patchworks model,
not a reconstruction of WFP's private Land Base Blocking layer, and not an
approved AAC result.

Recommended wording:

   The MP11 harvest-system candidate runtime is public-data based, archive
   materializable, and smoke-tested from the materialized archive. It is ready
   for replacement review if Phase 15 decision gates pass, but Phase 5 remains
   the accepted public baseline until that replacement is explicitly accepted.

Avoid describing the candidate as WFP-equivalent. The harvest-system lanes are
public proxies, even though the runtime now exposes ground, cable, and heli
clearcut treatment lanes and has passed archive-derived scenario smoke.

Published Artifacts
-------------------

The P15 publication payload is:

.. list-table::
   :header-rows: 1

   * - Artifact
     - Purpose
   * - ``releases/tfl6_mp11_harvest_system_candidate_runtime_p15_2.zip``
     - Ready-to-launch Patchworks runtime archive.
   * - ``releases/tfl6_mp11_harvest_system_candidate_runtime_p15_2_manifest.yaml``
     - Tracked manifest with archive checksum, member count, and per-file
       checksums.

The archive SHA256 is
``fcf8d3615f8bba65419d1a401d818c5eb87e7d75d3aa6007cfa6ada773536362``. The
manifest records ``46`` included files. The archive includes:

- the Phase 14 harvest-system runtime config;
- ForestModel XML and fragments;
- all-system ``tracks/`` outputs;
- no-heli ``tracks_no_heli/`` outputs;
- block and topology surfaces;
- ``analysis/base.pin`` and ``analysis/no_heli.pin``;
- shared Patchworks analysis helpers; and
- runtime README and lineage registry.

The archive intentionally excludes saved stages, runtime logs, generated
model-input bundles, downloads, caches, docs builds, and local machine paths.

Materialization
---------------

The clean-checkout materialization test used a shallow checkout of the P15
branch, then enabled ``arbutus-s3`` without credentials. The essential command
sequence is:

.. code-block:: powershell

   git clone --depth 1 --single-branch --no-tags --branch feature/tfl6-mp11-p15-runtime-publication https://github.com/UBC-FRESH/femic-tfl6-instance.git femic-tfl6-instance
   cd femic-tfl6-instance
   git fetch origin git-annex:refs/remotes/origin/git-annex
   git update-ref refs/heads/git-annex refs/remotes/origin/git-annex
   git annex init
   git annex enableremote arbutus-s3
   git annex get releases/tfl6_mp11_harvest_system_candidate_runtime_p15_2.zip
   git annex get releases/tfl6_mp11_harvest_system_candidate_runtime_p15_2_manifest.yaml

The P15 materialization QA recorded:

- ``arbutus-s3`` was enabled with credentials cleared;
- ``git annex info arbutus-s3`` reported ``creds: not available`` and
  ``public: yes``;
- archive and manifest fetches completed with checksum ``ok``;
- archive SHA256 matched the tracked manifest; and
- the unpacked archive contained expected ``base.pin``, ``no_heli.pin``,
  all-system track, and no-heli track files.

See ``planning/tfl6_mp11_phase15_materialization_qa.md`` for the tracked QA
record.

Archive-Derived Smoke Tests
---------------------------

P15.5 launched Patchworks from the unpacked materialized archive, not from the
source working tree. The tracked QA report is:

- ``planning/tfl6_mp11_phase15_materialized_runtime_smoke_qa.md``;
- ``planning/tfl6_mp11_phase15_materialized_runtime_smoke_qa.csv``; and
- ``planning/tfl6_mp11_phase15_materialized_runtime_smoke_qa.json``.

The smoke-test results were:

.. list-table::
   :header-rows: 1

   * - Run
     - Result
     - Schedule rows
     - Treatment lanes
   * - Direct launch
     - Pass
     - ``0``
     - none
   * - All-system 200k smoke
     - Pass
     - ``76,693``
     - ``CC_CABLE``, ``CC_GROUND``, ``CC_HELI``
   * - No-heli 200k smoke
     - Pass
     - ``75,023``
     - ``CC_CABLE``, ``CC_GROUND``

Both scenario-smoke runs used the Phase 14 harvest-target setup:

- base harvested-volume target
  ``product.HarvestedVolume.managed.Total.CC``;
- minimum value ``20,000,000`` per period;
- linear base target penalty shape;
- base target priming before even-flow activation;
- even-flow target ``flow.even.product.HarvestedVolume.managed.Total.CC``;
- default non-linear even-flow penalty shape; and
- even-flow min/max weights of ``10,000``.

The no-heli run had no forbidden ``CC_HELI`` treatment in the saved schedule.
This directly checks the prior Patchworks startup issue where a no-heli
scenario attempted to create targets against missing ``CC_HELI`` accounts.

Caveats
-------

The publication and smoke-test evidence is strong enough for replacement
review, but it does not erase the model caveats:

- WFP LBB remains unavailable and private.
- Ground, cable, and heli assignments remain public proxies.
- Public CDED slope, DRA road distance, and VRI-derived age, volume, and
  species-share signals are not WFP LiDAR, access, ITI, or LEFI truth.
- MP11 delivered-cost behavior, detailed scenario-policy rules, and several
  operational KPI surfaces remain incomplete unless later promoted.
- The published candidate is not an approved Chief Forester AAC decision.

Teaching Use
------------

The P15 candidate is suitable for advanced teaching workflows that require a
materializable harvest-system runtime:

- compare Phase 5 and MP11 candidate release boundaries;
- materialize a public git-annex runtime archive from a clean checkout;
- inspect all-system versus no-heli treatment schedules;
- explain why public-proxy harvest-system classification is useful but not
  WFP-model equivalence; and
- draft a replacement-review checklist before accepting a new baseline.

Students should treat Phase 15 as a publication and validation case study, not
as proof that the public FEMIC model is WFP's operational model.

Maintainer Workflow
-------------------

Maintainers should read the Phase 15 evidence in this order:

1. ``planning/tfl6_mp11_phase15_publication_replacement_candidate_plan.md`` for
   the publication boundary.
2. ``planning/tfl6_mp11_phase15_archive_publication_qa.md`` for archive
   contents, SHA256, and publication status.
3. ``planning/tfl6_mp11_phase15_materialization_qa.md`` for clean-checkout
   no-credential materialization evidence.
4. ``planning/tfl6_mp11_phase15_materialized_runtime_smoke_qa.md`` for
   archive-derived launch and scenario-smoke evidence.
5. ``planning/tfl6_mp11_phase15_replacement_candidate_decision.md`` once P15.7
   emits the final replacement-candidate decision.

The final Phase 15 decision vocabulary is:

- ``replacement_candidate_ready_for_review`` when all hard gates pass; or
- ``replacement_candidate_blocked`` when publication, materialization,
  checksum, launch, scenario, or documentation gates fail.

Neither status automatically replaces Phase 5. Replacement still requires a
separate explicit acceptance decision.
