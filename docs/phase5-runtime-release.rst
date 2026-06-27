Phase 5 Runtime Release
=======================

Purpose
-------

The first TFL 6 teaching release publishes a reviewed Patchworks runtime archive
so students and instructors can launch the accepted Phase 4 model without
rebuilding THLB, yield curves, ForestModel XML, Matrix Builder tracks, or block
topology first.

The archive is not a replacement for the rebuild trail. It is a convenience
artifact for teaching use. Maintainers should still use the planning notes,
lineage registry, and source-controlled configs when changing model logic.

Release Artifacts
-----------------

The release artifacts are annexed files in the instance repository:

.. list-table::
   :header-rows: 1

   * - Artifact
     - Purpose
   * - ``releases/tfl6_patchworks_runtime_p5_2.zip``
     - Ready-to-launch Patchworks runtime archive.
   * - ``releases/tfl6_patchworks_runtime_p5_2_manifest.yaml``
     - Manifest with archive checksum, source commits, Arbutus remote metadata,
       included-file checksums, rebuild command pointers, and validation state.

The runtime archive includes:

- accepted Phase 4 ForestModel XML;
- accepted Patchworks fragments shapefile;
- accepted Matrix Builder track CSVs;
- accepted block shapefile and ``topology_blocks_200r.csv``;
- Patchworks launch scripts and target helpers;
- ``models/tfl6_patchworks_model/README.md``; and
- ``models/tfl6_patchworks_model/lineage_registry.yaml``.

The archive deliberately excludes saved-stage smoke outputs, logs, scratch
directories, source download caches, and model-input build checkpoints.

Materializing The Archive
-------------------------

From a fresh clone of the instance repository:

.. code-block:: powershell

   git clone https://github.com/UBC-FRESH/femic-tfl6-instance.git
   cd femic-tfl6-instance
   git annex init
   git annex enableremote arbutus-s3
   git annex get releases\tfl6_patchworks_runtime_p5_2.zip
   git annex get releases\tfl6_patchworks_runtime_p5_2_manifest.yaml

The ``arbutus-s3`` remote is public. A no-credential clone should be able to
materialize these two files after the remote is enabled.

The published remote metadata is:

.. list-table::
   :header-rows: 1

   * - Field
     - Value
   * - Remote
     - ``arbutus-s3``
   * - Bucket
     - ``ubc-fresh-femic-tfl6-instance``
   * - Public URL
     - ``https://object-arbutus.cloud.computecanada.ca/ubc-fresh-femic-tfl6-instance``
   * - Remote UUID
     - ``861b7dd7-fff0-4637-b0a2-b9b4668dca71``

Validation Evidence
-------------------

P5.2 release validation proved that the archive is publicly materializable:

- a fresh temporary clone of ``feature/p5-publication-release`` was created;
- AWS/S3 credential environment variables were cleared before enabling
  ``arbutus-s3``;
- ``git annex info arbutus-s3`` reported ``creds: not available``,
  ``public: yes``, the expected public URL, and two remote keys;
- ``git annex get`` fetched both release files from ``arbutus-s3`` with
  git-annex checksum ``ok``; and
- a Python standard-library SHA256 check confirmed the archive hash matched the
  manifest.

The accepted archive SHA256 is:

.. code-block:: text

   17f56d11faeba89170fc48e202d1bfe83c2dd40b53e7409d8cdb8c1c487c2f9f

Launch Boundary
---------------

The archive proves materialization of the Phase 4 runtime package, not that
every student's workstation has a complete Patchworks installation. Users still
need a valid Patchworks runtime environment to open and run the package.

The launch surface included in the archive starts at:

.. code-block:: text

   models/tfl6_patchworks_model/analysis/base.pin

The representative Phase 4 scenario smoke used the generic managed clearcut
volume target:

.. code-block:: text

   product.HarvestedVolume.managed.Total.CC

Rebuild Trail
-------------

The main rebuild/provenance anchors are:

- ``planning/tfl6_runtime_artifact_publication_policy.md``;
- ``planning/tfl6_runtime_release_archive_manifest.md``;
- ``planning/tfl6_runtime_package_p44.md``;
- ``planning/tfl6_matrix_builder_p43_smoke.md``;
- ``planning/tfl6_forestmodel_xml_export_bridge.md``;
- ``planning/tfl6_model_input_bundle_core_tables.md``; and
- ``models/tfl6_patchworks_model/lineage_registry.yaml``.

Known Caveats
-------------

- The release archive is the accepted first teaching runtime package, not a
  final research-grade production model.
- Saved-stage scenario outputs are intentionally not part of the canonical
  release archive.
- The base-case treatment surface still uses generic ``CC``; harvest-system
  splits into ground/cable/heli remain a later teaching/model-design refinement.
- Strategic RMZ replacement remains an advanced student challenge rather than a
  base-case requirement.
