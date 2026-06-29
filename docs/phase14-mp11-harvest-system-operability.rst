Phase 14 MP11 Harvest-System Operability
========================================

Phase 14 adds public-proxy ground, cable, and heli harvest-system lanes to the
MP11 candidate runtime. This closes the generic-clearcut-only limitation for the
candidate model, while keeping the release language careful: Phase 5 remains the
accepted public teaching/runtime baseline, and the Phase 14 runtime is a
candidate supplement for MP11 comparison and advanced teaching.

Status Boundary
---------------

The Phase 14 runtime is a smoke-tested public-data candidate. It is not a
reconstruction of Western Forest Products' unpublished Land Base Blocking
(LBB) layer, not a replica of WFP's internal Patchworks model, and not an
approved AAC result.

Recommended wording:

   The Phase 14 MP11 candidate runtime includes public-proxy ground, cable, and
   heli harvest-system lanes. It is useful for labelled MP11 comparison and
   teaching workflows, but the harvest-system assignment is a public proxy
   because WFP's LBB layer is not public or queryable.

Avoid describing the candidate as WFP-equivalent. The correct interpretation is
that Phase 14 makes the candidate more operationally expressive while preserving
the public-data caveats.

Evidence Basis
--------------

MP11 describes harvest-system assignment through WFP's LBB process. That
process uses inputs that are not available as a public stand-level FEMIC source,
including WFP internal operability review and planning surfaces. Phase 14
therefore uses public proxies and treats MP11 aggregate tables as comparison
targets rather than stand-level truth.

The Phase 14 proxy uses:

.. list-table::
   :header-rows: 1

   * - Evidence
     - Phase 14 use
     - Caveat
   * - MP11 Table 20 / Table 73
     - Aggregate area and volume comparison target.
     - Not stand-level source truth.
   * - MP11 Tables 27-29
     - Helicopter economic-operability threshold context.
     - Used only where public age, volume, species-share, and access proxies
       exist.
   * - P9D CDED slope
     - Public slope context for ground/cable/heli proxy assignment.
     - Not WFP LiDAR terrain analysis.
   * - Public VRI attributes
     - Age, volume, and species-share proxy fields.
     - Not WFP ITI/LEFI inventory truth.
   * - Nearest DRA road distance
     - Access-distance proxy.
     - Not flight distance or WFP road-planning data.

Classification Result
---------------------

The P14.4 classifier assigned ``22,614`` managed current THLB rows across
``139,995.798 ha`` of the candidate scaffold:

.. list-table::
   :header-rows: 1

   * - System
     - Candidate rows
     - Candidate area
     - Candidate volume
     - Area share
     - MP11 Table 73 area share
     - Residual
   * - Ground
     - ``12,905``
     - ``80,241.389 ha``
     - ``22,778,489.535 m3``
     - ``57.317%``
     - ``57.300%``
     - ``+0.017 pp``
   * - Cable
     - ``9,055``
     - ``56,677.061 ha``
     - ``20,342,940.218 m3``
     - ``40.485%``
     - ``39.600%``
     - ``+0.885 pp``
   * - Heli
     - ``654``
     - ``3,077.349 ha``
     - ``1,921,687.622 m3``
     - ``2.198%``
     - ``3.100%``
     - ``-0.902 pp``

The normalized area shares are close to the MP11 Table 73 distribution. Direct
area and volume residuals are still caveated because the candidate scaffold
total is larger than the MP11 Table 73 total and the public volume fields are
not WFP inventory truth.

Runtime Evidence
----------------

Phase 14 generated a new candidate model-input and XML lane, then built the
Patchworks runtime:

- ignored model-input root:
  ``data/mp11_harvest_system_model_input_bundle/``;
- ignored ForestModel XML/fragments root:
  ``output/patchworks_tfl6_mp11_harvest_system_candidate/``;
- runtime root:
  ``models/tfl6_patchworks_model_mp11_harvest_system_candidate/``;
- ``814`` ``CC_GROUND`` treatment nodes;
- ``814`` ``CC_CABLE`` treatment nodes;
- ``814`` ``CC_HELI`` treatment nodes;
- ``2,442`` ``HVSYS`` split managed selects;
- ``13`` Matrix Builder track files;
- ``93,330`` feature rows;
- ``46,605`` product rows;
- ``18,642`` treatment rows;
- ``0`` message rows;
- ``24,879`` block rows; and
- valid ``EPSG:3005`` block geometry.

The runtime keeps aggregate ``.CC`` harvested-volume products for all-system
reporting while exposing split ``CC_GROUND``, ``CC_CABLE``, and ``CC_HELI``
treatment lanes.

Smoke Tests
-----------

Phase 14 direct launch and scenario smoke passed:

.. list-table::
   :header-rows: 1

   * - Run
     - Result
     - Schedule rows
     - Scheduled treatments
   * - Direct launch
     - Pass
     - ``0``
     - none
   * - All-system 200k smoke
     - Pass
     - ``76,635``
     - ``CC_CABLE``, ``CC_GROUND``, ``CC_HELI``
   * - No-heli 200k smoke
     - Pass
     - ``75,086``
     - ``CC_CABLE``, ``CC_GROUND``

The no-heli run uses an ignored generated ``tracks_no_heli/`` variant. That
variant removes ``CC_HELI`` treatment, product, account, and protoaccount rows
while leaving the all-system ``tracks/`` outputs intact.

Caveats
-------

Phase 14 makes the MP11 candidate more useful, but it does not remove all MP11
runtime caveats:

- WFP LBB is unavailable and was not reconstructed.
- Ground/cable/heli assignments are public proxies, not WFP operational
  assignments.
- Public CDED slope is not WFP LiDAR slope or terrain-operability analysis.
- Nearest-DRA-road distance is not a flight-distance or WFP road-development
  model.
- Public VRI age, volume, and species-share fields are not WFP ITI/LEFI truth.
- MP11 minimum-harvest-age policy, delivered-cost behavior, block-size
  behavior, harvest-age KPIs, and scenario-policy rules remain future work
  unless separately promoted.
- Phase 14 smoke tests are runtime feasibility evidence, not release-archive
  materialization evidence.

Teaching Workflows
------------------

Useful teaching exercises now include:

- compare MP11 Table 73 area shares against the Phase 14 public-proxy
  classifier and identify why normalized shares are more meaningful than direct
  area residuals;
- run or inspect all-system versus no-heli harvest scenarios and explain the
  operational interpretation of removing heli lanes;
- distinguish treatment eligibility, curve provenance, harvest-system class,
  and reporting products in the Patchworks runtime;
- classify each Phase 14 input as public proxy, MP11 aggregate comparison
  target, private-source gap, or generated runtime artifact; and
- write a release-readiness checklist for what would be required before using
  the harvest-system candidate as a replacement baseline.

Students should not be asked to treat the Phase 14 candidate as WFP's model or
as an AAC recommendation.

Maintainer Workflow
-------------------

Maintainers should read the Phase 14 evidence in this order:

1. ``planning/tfl6_mp11_phase14_harvest_system_operability_plan.md`` for the
   execution boundary.
2. ``planning/tfl6_mp11_phase14_harvest_system_evidence.md`` for source anchors
   and public/private boundaries.
3. ``planning/tfl6_mp11_phase14_public_proxy_metrics.md`` for metric inputs.
4. ``planning/tfl6_mp11_phase14_harvest_system_classification.md`` for
   classifier and MP11 Table 73 comparison evidence.
5. ``planning/tfl6_mp11_phase14_model_input_xml_build_summary.md`` for XML
   split-lane evidence.
6. ``planning/tfl6_mp11_phase14_matrix_runtime_qa.md`` for Matrix Builder and
   runtime package evidence.
7. ``planning/tfl6_mp11_phase14_scenario_smoke_qa.md`` for direct launch,
   all-system, and no-heli smoke evidence.
8. ``planning/tfl6_mp11_phase14_closeout.md`` for the final closeout boundary.

Future work should open a new issue or phase if the candidate is to be
archive-published, clean-checkout materialized, calibrated against more MP11
KPIs, or promoted toward replacing Phase 5.

