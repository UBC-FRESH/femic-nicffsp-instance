Phase 5 Rebuild Provenance
==========================

This page is the maintainer-facing rebuild map for the first TFL 6 teaching
runtime package. It complements the runtime quickstart by explaining where the
published archive came from and which source-controlled surfaces should be
consulted before changing model logic.

The published archive is convenient for teaching use. The rebuild trail is the
authority for development work.

Canonical Versus Generated Surfaces
-----------------------------------

The TFL 6 repository separates reviewed model contracts from generated runtime
outputs.

.. list-table::
   :header-rows: 1

   * - Surface
     - Status
     - Notes
   * - ``config/``
     - canonical
     - Reviewed recipe, runtime, TIPSY, and Patchworks configuration.
   * - ``planning/``
     - canonical audit trail
     - Reviewed decisions, extraction notes, diagnostics, and milestone QA.
   * - ``docs/``
     - canonical teaching and maintainer documentation
     - Sphinx source for the public teaching docs.
   * - ``models/tfl6_patchworks_model/README.md``
     - canonical package note
     - Human-readable runtime-package boundary.
   * - ``models/tfl6_patchworks_model/lineage_registry.yaml``
     - canonical runtime lineage registry
     - Commands, accepted artifact paths, QA status, and publication policy.
   * - ``data/model_input_bundle/``
     - generated
     - Bundle tables and handoff geometry regenerated from Phase 2/3 contracts.
   * - ``output/patchworks_tfl6_validated/``
     - generated
     - ForestModel XML and fragments from the Patchworks export.
   * - ``models/tfl6_patchworks_model/tracks/``
     - generated
     - Matrix Builder CSV surfaces.
   * - ``models/tfl6_patchworks_model/blocks/``
     - generated
     - Runtime block and topology inputs.
   * - ``models/tfl6_patchworks_model/analysis/p44*/``
     - smoke output
     - Saved-stage launch/scenario evidence, not canonical release input.
   * - ``releases/``
     - published artifact surface
     - Annexed runtime archive and manifest for teaching users.

Source And THLB Foundation
--------------------------

The Phase 2 foundation resolves the TFL 6 AOI, 2025 VRI/VDYP source inputs,
THLB netdown rules, and benchmark tolerance. The main reviewed anchors are:

- ``planning/tfl6_aoi_pivot_and_input_layers.md``;
- ``planning/tfl6_source_layer_dependency_inventory.md``;
- ``planning/tfl6_source_layer_recipe_contracts.md``;
- ``planning/tfl6_r1_vdyp_field_profile.md``;
- ``planning/tfl6_thlb_netdown_steps.md``;
- ``planning/tfl6_thlb_smoke_lane_plan.md``;
- ``planning/tfl6_adjusted_thlb_benchmarks.md``; and
- ``planning/tfl6_thlb_benchmark_tolerance.md``.

The corrected Phase 4 bundle is built from the AFLB universe. THLB is a managed
share inside that universe, and NTHLB remains forested AFLB area that carries
untreated growth but is not eligible for scheduled management.

AU, Yield-Curve, And Treatment Foundation
-----------------------------------------

Phase 3 defines the model-design contract that feeds the bundle. The key
anchors are:

- ``planning/tfl6_au_yield_curve_contract.md``;
- ``planning/tfl6_static_au_universe.md``;
- ``planning/tfl6_first_growth_vdyp_run_summary.md``;
- ``planning/tfl6_first_growth_au_remap_audit.md``;
- ``planning/tfl6_first_growth_shape_diagnostics.md``;
- ``planning/tfl6_mp10_tipsy_parameter_library.md``;
- ``planning/tfl6_tipsy_parameter_crosswalk.md``;
- ``planning/tfl6_tipsy_managed_curve_diagnostics.md``;
- ``planning/tfl6_tipsy_vdyp_overlay_manifest.md``;
- ``planning/tfl6_treatment_option_contract.md``; and
- ``planning/tfl6_state_transition_contract.md``.

The accepted first release uses:

- static AU identity;
- top-strata VDYP first-growth curves with remapping for non-dominant strata;
- reviewed MP10 TIPSY parameter evidence for managed curves;
- generic ``CC`` as the first-pass clearcut-and-plant treatment lane; and
- deferred ground/cable/heli harvest-system assignment.

Cedar, NICF, And Stakeholder Context
------------------------------------

The first runtime package embeds the K3Z/NICF identity surfaces inside the
larger TFL 6 model, but detailed cedar and NICF expansion scenario work remains
teaching-design and future-modeling scope. The main anchors are:

- ``planning/tfl6_cedar_signal_design.md``;
- ``planning/tfl6_nicf_embedded_identity.md``;
- ``planning/tfl6_stakeholder_context.md``; and
- :doc:`phase3-cedar-nicf-expansion`.

Future NICF expansion areas are outside the TFL 6 AOI and should be modeled as
proximal or adjacent public forested land, not as new area inside the current
TFL 6 boundary.

Model-Input Bundle
------------------

Phase 4 starts by turning the accepted THLB and model-design contracts into
Patchworks-facing bundle tables. The primary anchors are:

- ``planning/tfl6_model_input_bundle_prerequisite_manifest.md``;
- ``planning/tfl6_model_input_bundle_path_contract.md``;
- ``planning/tfl6_model_input_bundle_geometry_handoff.md``;
- ``planning/tfl6_model_input_bundle_core_tables.md``;
- ``planning/tfl6_model_input_bundle_qa.md``; and
- :doc:`phase3-model-input-contract`.

The accepted bundle evidence records:

- ``25,019`` AFLB stand rows;
- ``191,168.597 ha`` AFLB;
- ``139,995.798 ha`` THLB;
- ``51,172.799 ha`` NTHLB;
- no missing AU, natural-curve, or treated-curve assignments; and
- warning-only sparse TIPSY fallback for ``136`` rows / ``749.396 ha``.

ForestModel XML And Fragments
-----------------------------

The accepted Patchworks export is recorded in:

- ``planning/tfl6_forestmodel_xml_export_blocker.md``;
- ``planning/tfl6_forestmodel_xml_export_bridge.md``; and
- ``models/tfl6_patchworks_model/lineage_registry.yaml``.

The accepted command recorded in the lineage registry is:

.. code-block:: powershell

   python -m femic export patchworks --instance-root . `
     --tsa tfl6 --bundle-dir data/model_input_bundle/export_compat `
     --checkpoint data/model_input_bundle/export_compat/aflb_current_export_compat.feather `
     --output-dir output/patchworks_tfl6_validated --start-year 2026 `
     --horizon-years 300 --ifm-mode proportional

The accepted outputs are:

- ``output/patchworks_tfl6_validated/forestmodel.xml``; and
- ``output/patchworks_tfl6_validated/fragments/fragments.*``.

Matrix Builder
--------------

The accepted Matrix Builder lane is recorded in:

- ``planning/tfl6_matrix_builder_p43_smoke.md``; and
- ``models/tfl6_patchworks_model/lineage_registry.yaml``.

The accepted command recorded in the lineage registry is:

.. code-block:: powershell

   python -m femic patchworks matrix-build `
     --config config/patchworks.runtime.windows.yaml `
     --run-id tfl6_p43_matrix_accounts_wait20

Accepted evidence includes synced accounts/protoaccounts, ``211`` account rows,
and repaired TFL 6 runtime paths. Matrix Builder output is generated under:

.. code-block:: text

   models/tfl6_patchworks_model/tracks/

Blocks, Topology, And Launch Surfaces
-------------------------------------

The accepted runtime-package lane is recorded in:

- ``planning/tfl6_runtime_package_p44.md``; and
- ``models/tfl6_patchworks_model/lineage_registry.yaml``.

The accepted block/topology command is:

.. code-block:: powershell

   python -m femic patchworks build-blocks `
     --config config/patchworks.runtime.windows.yaml `
     --topology-radius 200

Accepted block evidence includes ``24,879`` valid EPSG:3005 block rows,
``191,168.566 ha``, and ``170,759`` topology edges.

The accepted baseline launch surface is:

.. code-block:: text

   models/tfl6_patchworks_model/analysis/base.pin

The accepted direct launch smoke command is:

.. code-block:: powershell

   python -m femic patchworks run-headless `
     models/tfl6_patchworks_model/analysis/base.pin `
     --config config/patchworks.runtime.windows.yaml `
     --run-id tfl6_p44b_launch0 --iterations 0 `
     --stage-label p44b_launch0

The accepted representative scenario smoke uses:

.. code-block:: text

   product.HarvestedVolume.managed.Total.CC

with generic managed ``CC`` scheduling.

Release Archive And Manifest
----------------------------

Phase 5 publication is recorded in:

- ``planning/tfl6_runtime_artifact_publication_policy.md``;
- ``planning/tfl6_runtime_release_archive_manifest.md``;
- ``releases/tfl6_patchworks_runtime_p5_2.zip``; and
- ``releases/tfl6_patchworks_runtime_p5_2_manifest.yaml``.

The manifest is the release-time inventory of included files, checksums,
source commits, Arbutus remote metadata, and validation status. The archive is
publicly materialized through ``arbutus-s3`` and verified in
:doc:`phase5-runtime-release`.

Maintainer Checklist
--------------------

Before rebuilding or republishing, maintainers should confirm:

- the intended change is recorded in ``ROADMAP.md`` under the active phase;
- the governing issue has been updated;
- the source contract or config being changed is canonical, not a generated
  smoke output;
- generated bundle/XML/fragments/tracks/blocks are rebuilt in dependency order;
- the lineage registry is updated when commands, accepted artifacts, or QA
  status change;
- Sphinx docs are rebuilt with warnings as errors after documentation changes;
  and
- published release files are annexed, copied to ``arbutus-s3``, and proven
  materializable from a fresh no-credential clone before release readiness is
  claimed.
