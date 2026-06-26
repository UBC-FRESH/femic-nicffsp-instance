Phase 2 THLB Netdown
====================

Purpose
-------

Phase 2 turns the TFL 6 source-layer and THLB planning surfaces into a reviewed
base teaching lane. It does not claim to reproduce the 2011 TSR analysis
exactly, because the active AOI is the current TFL 6 boundary and the official
2011 Management Plan 10 benchmark was built on a smaller historical land base.

The Phase 2 output is a reproducible, inspectable THLB starting point for later
model-design and Patchworks work. It is suitable for teaching because the major
assumptions are explicit, the unresolved source gaps are preserved as caveats,
and the audit trail records both the executable recipe and the resulting area
signals.

Core Inputs
-----------

Phase 2 uses these reviewed instance inputs:

``data/source/tfl_6/aoi/tfl_6_boundary.gpkg``
   Current TFL 6 AOI boundary accepted during P1.6. The AOI area is
   ``217042.718950 ha``.

``data/input/tfl_6/vri_2025_r1_poly_tfl6.gpkg``
   Accepted 2025 R1 polygon accounting surface clipped to the TFL 6 AOI.

``config/tsr/source_layers.recipe.yaml``
   Reviewed source-layer scaffold for materialized hydrology, wildlife, OGMA,
   recreation, roads, landscape-unit, and BEC inputs.

``config/tsr/thlb_netdown.recipe.yaml``
   Ordered THLB recipe scaffold preserving the Management Plan 10 Table 4 row
   order from total landbase through current THLB and long-term landbase.

``planning/tfl6_adjusted_thlb_benchmarks.md``
   Approximate current-AOI validation targets produced by scaling the official
   2011 MP10 Table 4 benchmarks to the current TFL 6 AOI.

Design Rationale
----------------

The official 2011 MP10 Table 4 current THLB benchmark is ``107811 ha`` on a
historical total landbase of ``171441 ha``. The current accepted AOI is larger:
``217042.718950 ha``. Phase 2 therefore does not compare the reconstructed
current-AOI THLB directly against the raw 2011 value.

Instead, Phase 2 uses a scaled current-AOI teaching benchmark. The scaling
contract assumes that the post-2011 extension area has approximately the same
mean THLB netdown rate as the pre-extension MP10 landbase. This is reasonable
for early teaching validation, but it is not verifiable and is almost certainly
not exactly true.

The accepted current-AOI benchmark for current THLB is ``136487.728 ha``. The
P2.4e smoke run produced ``144203.485 ha``. P2.5 accepted the resulting
``+7715.757 ha`` / ``+5.65%`` gap as close enough for the base teaching lane.
This tolerance lock is documented in
``planning/tfl6_thlb_benchmark_tolerance.md``.

Milestone Comparison
--------------------

.. list-table::
   :header-rows: 1

   * - Milestone
     - Scaled benchmark ha
     - P2.4e result ha
     - Delta ha
     - Delta percent
   * - Total landbase
     - ``217042.719``
     - ``217042.719``
     - ``-0.000``
     - ``-0.00%``
   * - Total forested
     - ``194991.692``
     - ``196833.177``
     - ``+1841.485``
     - ``+0.94%``
   * - Total productive forest
     - ``186175.333``
     - ``190515.340``
     - ``+4340.007``
     - ``+2.33%``
   * - Total operable
     - ``170428.940``
     - ``174768.947``
     - ``+4340.007``
     - ``+2.55%``
   * - Reduced landbase
     - ``143686.151``
     - ``151401.908``
     - ``+7715.757``
     - ``+5.37%``
   * - Current THLB
     - ``136487.728``
     - ``144203.485``
     - ``+7715.757``
     - ``+5.65%``

The long-term landbase row is not part of the base current-THLB acceptance
decision because the P2.4e lane does not execute the future-road long-term
adjustment.

Fallbacks and Caveats
---------------------

Phase 2 deliberately distinguishes exact spatial overlays from teaching
fallbacks:

Operational operability
   No accepted public TFL 6-specific historical operability geometry was found.
   The base lane uses a benchmark-aware fallback and preserves DEM/slope and
   VRI/VDYP proxy development as future sensitivity work.

Draft OGMAs
   Current non-legal OGMA geometry is materialized as a review clue, but it is
   not treated as a direct replacement for the 2011 draft OGMA state. The base
   lane keeps a documented fallback.

Cultural heritage resources
   Sensitive TUS/CMT geometry is not expected as public source data. The base
   lane uses a documented proxy/aspatial fallback based on MP10 evidence.

Strategic Resource Management Zones
   Strategic RMZ/LU/BEC stand-level retention is implemented as an aspatial
   MP10 Table 16 fallback. Replacing this with geometry-backed strategic RMZ
   polygons is documented as an advanced student challenge.

These fallbacks are not hidden. They are visible in the recipe, audit JSON,
status report, planning notes, and changelog.

Reproducibility Audit Trail
---------------------------

The Phase 2 audit trail is intentionally split across compact tracked files and
large regenerable runtime products.

Tracked planning and decision surfaces:

``planning/tfl6_source_layer_dependency_inventory.md``
   Source-layer dependency inventory and materialization/review decisions.

``planning/tfl6_operability_netdown_proxy.md``
   Operability evidence, proxy rationale, and sensitivity-design boundary.

``planning/tfl6_r1_vdyp_field_profile.md``
   2025 R1/VDYP7 schema, join, and field-mapping profile.

``planning/tfl6_source_layer_recipe_contracts.md``
   Reviewed source-layer recipe contracts for the first THLB lane.

``planning/tfl6_thlb_smoke_lane_plan.md``
   Smoke-lane command, execution boundary, inspected outputs, and first-run
   signals.

``planning/tfl6_thlb_benchmark_tolerance.md``
   P2.5 tolerance lock and rationale.

Tracked executable/audit surfaces:

``config/tsr/source_layers.recipe.yaml``
   Source-layer recipe scaffold.

``config/tsr/thlb_netdown.recipe.yaml``
   THLB netdown recipe scaffold.

``config/tsr/tfl6_thlb_smoke.audit.json``
   Machine-readable P2.4e smoke-run audit.

``config/tsr/thlb_reconstructed.status.md``
   Human-readable P2.4e status report.

Large generated checkpoint and runtime-log products are not accepted as
ordinary tracked Git content in Phase 2. They are regenerable from the reviewed
inputs and recipe surfaces unless a later publication policy explicitly annexes
or publishes them.

Maintainer Checklist
--------------------

Before using the Phase 2 THLB as a model-input dependency, maintainers should:

1. Confirm the Phase 2 closeout PR was merged.
2. Inspect ``config/tsr/thlb_reconstructed.status.md`` for the final area
   signals and visible fallback rows.
3. Inspect ``planning/tfl6_thlb_benchmark_tolerance.md`` for the accepted
   teaching tolerance and caveats.
4. Confirm that any proposed Phase 3 design change does not silently reopen a
   Phase 2 source-layer or THLB decision.

Student Interpretation
----------------------

Students should treat the Phase 2 THLB as a transparent base-case teaching
landbase, not as a legal TSR reconstruction. The important modeling lesson is
that defensible forest estate models need visible assumptions, reproducible
inputs, and documented tolerances. The base lane is intentionally close enough
to support scenario learning while leaving meaningful sensitivity questions,
such as operability and strategic RMZ replacement, available for advanced work.
