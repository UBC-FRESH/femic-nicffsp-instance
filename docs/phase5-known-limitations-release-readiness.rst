Phase 5 Known Limitations And Release Readiness
===============================================

This page consolidates the known limitations of the first TFL 6 teaching
runtime package and defines what must be checked before Phase 5 can close.

The release is intended for FRST 558 teaching use. It is not a claim that every
modeling question for TFL 6 has been resolved.

Release Status
--------------

The first teaching release is ready to use when:

- the runtime archive and manifest are publicly materializable;
- the archive opens from the documented ``base.pin`` launch surface in a valid
  Patchworks environment;
- the core managed/unmanaged area and yield signals are present;
- the representative managed ``CC`` harvest product is present;
- the documentation builds without Sphinx warnings; and
- the remaining caveats below are documented rather than hidden.

The accepted public release artifacts are:

.. list-table::
   :header-rows: 1

   * - Artifact
     - Role
   * - ``releases/tfl6_patchworks_runtime_p5_2.zip``
     - Ready-to-launch teaching runtime package.
   * - ``releases/tfl6_patchworks_runtime_p5_2_manifest.yaml``
     - Archive checksum, included-file inventory, source commits, Arbutus
       metadata, and validation record.

The release archive was proven materializable from a no-credential clone through
the public ``arbutus-s3`` special remote.

What The First Release Is
-------------------------

The first release is:

- a reviewed teaching runtime package;
- a reproducible FEMIC/Patchworks build with an audit trail;
- a baseline for scenario exercises;
- a vehicle for stakeholder-style tradeoff interpretation; and
- a starting point for student extensions.

The first release is not:

- a final research-grade TFL 6 production model;
- a complete operational planning model;
- a legal or consultation record;
- a definitive economic model of delivered cost or product value; or
- a substitute for reviewing the rebuild trail before changing model logic.

Modeling Caveats
----------------

Treatment Surface
~~~~~~~~~~~~~~~~~

The base treatment surface uses generic ``CC`` as the first-pass
clearcut-and-plant lane. It does not yet split treatments or costs by ground,
cable, and heli harvest systems.

Implication:
  Students may use the first runtime package for baseline harvest-flow and
  tradeoff exercises, but any interpretation involving delivered cost or
  harvesting system should be framed as a proxy until the harvest-system
  classifier is reviewed.

Harvest-System Assignment
~~~~~~~~~~~~~~~~~~~~~~~~~

Ground/cable/heli assignment is deferred. The intended future refinement is to
combine stand inventory, DEM/slope evidence, and reviewed operability logic.

Implication:
  Harvest-system splits are an advanced model improvement, not a blocker for
  the first teaching release.

Strategic RMZ
~~~~~~~~~~~~~

The base teaching lane keeps the MP10 Table 16 strategic RMZ / stand-level
retention effect as an aspatial fallback. The current public-data discovery
work did not locate an accepted materializable strategic Resource Management
Zone geometry for the base model.

Implication:
  Replacing the fallback with geometry-backed RMZ polygons is an advanced
  student challenge and sensitivity-analysis opportunity.

NICF Expansion
~~~~~~~~~~~~~~

NICF expansion candidates are expected to come from proximal or adjacent public
forested land outside the current TFL 6 AOI. They are not active base-case
geography inside the published runtime package.

Implication:
  Scenario reports must keep current-AOI TFL 6 geography separate from any
  future outside-AOI expansion candidate pools.

Cedar Stewardship
~~~~~~~~~~~~~~~~~

The first release carries cedar signals for teaching and reporting, but it does
not impose hard cedar reserve targets, utility-pole grade thresholds, or
cedar-specific treatment lanes.

Implication:
  Cedar-focused exercises should state whether they use existing report signals
  or add new student-defined assumptions.

VDYP And TIPSY Curves
~~~~~~~~~~~~~~~~~~~~~

The first release uses accepted VDYP first-growth curves and reviewed TIPSY
managed-curve inputs. Some curve smoothing and sparse-bin choices are
documented as acceptable for proceeding, but may be revisited if a project
needs a more detailed curve sensitivity exercise.

Implication:
  Curve review is a valid extension project, but it is not required before
  using the first runtime package.

Saved-Stage Outputs
~~~~~~~~~~~~~~~~~~~

Saved-stage smoke outputs are validation evidence. They are not canonical
release inputs and should not be treated as the source of truth for new
scenario results.

Implication:
  New teaching results should be generated from the published runtime package
  or from a documented rebuilt package.

Data And Rebuild Caveats
------------------------

The release archive is designed to let students launch the model without
rebuilding. Maintainers who change model logic must work through the rebuild
trail:

- source and THLB contracts;
- AU and yield-curve contracts;
- model-input bundle generation;
- ForestModel XML and fragments;
- Matrix Builder tracks/accounts;
- blocks and topology;
- launch smoke and representative scenario smoke; and
- archive/manifest publication.

The maintainer map is documented in :doc:`phase5-rebuild-provenance`.

P5.4 Release-QA Checklist
-------------------------

Before Phase 5 closeout, run and record the final QA checks:

.. list-table::
   :header-rows: 1

   * - Check
     - Acceptance Signal
   * - Sphinx documentation build
     - ``sphinx-build -b html docs docs/_build/html -W`` passes.
   * - Public archive materialization
     - Fresh no-credential clone can fetch archive and manifest from
       ``arbutus-s3``.
   * - Archive manifest consistency
     - ZIP contents and SHA256 match the release manifest.
   * - Patchworks launch smoke
     - ``base.pin`` opens in the accepted runtime environment.
   * - Baseline signal smoke
     - Managed/unmanaged area and yield signals plus managed ``CC`` harvest
       product are present.
   * - Documentation link audit
     - Runtime release, quickstart, rebuild provenance, scenario workflow,
       teaching challenges, and known-limitations pages are reachable.
   * - Roadmap and issue hygiene
     - P5.3 is closed, P5.4 records final QA, and issue comments match the repo
       state.

Release-Readiness Boundary
--------------------------

Phase 5 can close when the first teaching release is public, documented,
materializable, launch-smoked, and honest about its limitations.

Phase 5 should not be held open for:

- ground/cable/heli harvest-system modeling;
- geometry-backed strategic RMZ replacement;
- outside-AOI NICF expansion implementation;
- cedar-specific reserve or utility-pole-grade policy design;
- VDYP/TIPSY sensitivity projects; or
- production-grade economic modeling.

Those are legitimate follow-on teaching or research tasks, not prerequisites
for this first runtime release.
