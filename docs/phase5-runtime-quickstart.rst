Phase 5 Runtime Quickstart
==========================

This quickstart is for students and instructors who want to open the first TFL
6 teaching runtime package before learning how to rebuild it. It starts from
the published Phase 5 archive, not from the source-layer or Matrix Builder
workflows.

Prerequisites
-------------

You need:

- Git;
- git-annex;
- a Patchworks runtime installation; and
- a local clone of ``UBC-FRESH/femic-tfl6-instance``.

The release archive is stored in the public ``arbutus-s3`` git-annex remote.
No Arbutus credentials are required for normal teaching users.

Materialize The Runtime Archive
-------------------------------

From a fresh clone:

.. code-block:: powershell

   git clone https://github.com/UBC-FRESH/femic-tfl6-instance.git
   cd femic-tfl6-instance
   git annex init
   git annex enableremote arbutus-s3
   git annex get releases\tfl6_patchworks_runtime_p5_2.zip
   git annex get releases\tfl6_patchworks_runtime_p5_2_manifest.yaml

Confirm the archive file exists locally:

.. code-block:: powershell

   git annex whereis releases\tfl6_patchworks_runtime_p5_2.zip

The output should include the local repository and ``arbutus-s3``.

Unpack The Runtime Package
--------------------------

Unpack the archive from the repository root:

.. code-block:: powershell

   Expand-Archive releases\tfl6_patchworks_runtime_p5_2.zip -DestinationPath runtime\tfl6_patchworks_runtime_p5_2

The archive preserves the model-root layout. The launch file is:

.. code-block:: text

   runtime/tfl6_patchworks_runtime_p5_2/models/tfl6_patchworks_model/analysis/base.pin

The runtime package also includes the Matrix Builder tracks, blocks, topology,
ForestModel XML, launch helpers, package README, and lineage registry needed by
that ``base.pin`` file.

Open Patchworks
---------------

Open the extracted ``base.pin`` file in Patchworks:

.. code-block:: text

   runtime/tfl6_patchworks_runtime_p5_2/models/tfl6_patchworks_model/analysis/base.pin

The accepted Phase 5 launch boundary is a baseline model launch. Students
should not need to run THLB netdown, yield-curve generation, ForestModel XML
export, Matrix Builder, or block topology generation before opening this first
teaching package.

Baseline Smoke Signals
----------------------

After the package opens, use the model surfaces to confirm that the core
teaching signals are present:

.. list-table::
   :header-rows: 1

   * - Signal
     - Why It Matters
   * - ``product.HarvestedVolume.managed.Total.CC``
     - Representative managed clearcut volume product used for the Phase 4
       harvest-smoke target.
   * - ``product.Treated.managed.CC``
     - Confirms the generic base-case clearcut treatment lane is visible.
   * - ``feature.Area.managed`` and ``feature.Area.unmanaged``
     - Confirms the Patchworks managed/unmanaged split is available.
   * - ``feature.Yield.managed.Total`` and ``feature.Yield.unmanaged.Total``
     - Confirms both THLB and retained AFLB areas carry growth signal.

Remember that the stand universe is the AFLB. THLB is the managed subset of
that AFLB universe. NTHLB is still forested AFLB area, so it remains in the
model as unmanaged retention area with untreated growth.

Teaching Interpretation
-----------------------

The first runtime package is intended to support discussion of tradeoffs before
students learn the full rebuild pipeline. Useful first questions include:

- how much harvest flow can the generic clearcut lane support;
- how managed and unmanaged area are represented differently;
- why NTHLB remains in the model even though it is not eligible for scheduled
  harvest;
- how TFL 6, the embedded K3Z/NICF area, and future NICF expansion candidates
  should be tracked separately; and
- which outputs are useful proxy KPIs for WFP fibre supply, NICF interests,
  ecosystem retention, cedar stewardship, and student-defined scenario goals.

Rebuild Boundary
----------------

The runtime archive is the teaching-consumption path. Rebuild work belongs in
the source-controlled FEMIC workflows and planning notes. Use the rebuild trail
when a project changes source data, THLB netdown rules, AU definitions, yield
curves, treatment options, state transitions, XML semantics, Matrix Builder
tracks, block topology, or Patchworks targets.

The main rebuild anchors are:

- :doc:`phase2-thlb-netdown`;
- :doc:`phase3-au-yield-curves`;
- :doc:`phase3-cedar-nicf-expansion`;
- :doc:`phase3-model-input-contract`; and
- :doc:`phase5-runtime-release`.

Known Limits For First Use
--------------------------

- The base-case treatment lane is generic ``CC``. Ground, cable, and heli
  harvest-system splits are deferred.
- Cedar and NICF expansion scenario details are teaching-design surfaces, not
  fully enumerated operational prescriptions in this first runtime package.
- Strategic RMZ replacement is documented as an advanced student challenge.
- Saved-stage outputs are not canonical release artifacts; rerun scenarios from
  the published runtime package when producing new teaching results.
