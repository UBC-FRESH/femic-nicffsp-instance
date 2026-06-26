Phase 3 Cedar And NICF Expansion Design
=======================================

Purpose
-------

This page summarizes the Phase 3 cedar-signal and embedded NICF/K3Z identity
contracts. These contracts define what the first TFL 6 teaching model must
carry into Phase 4 for reporting, accounts, targets, and scenario comparison.

This page is documentation only. It does not build model-input tables,
ForestModel XML, Matrix Builder outputs, or a Patchworks runtime package.

Design Boundary
---------------

The cedar and NICF expansion lanes are reporting and scenario-design surfaces.
They do not change canonical AU identity, curve families, or base THLB
netdown.

The accepted AU and curve contract remains:

- BEC zone/subzone/variant/phase, top-two species, and site-index class define
  static AUs.
- Cedar status, K3Z identity, expansion status, treatment eligibility,
  operability, and THLB status remain stand-level attributes.
- The base TFL 6 treatment catalogue remains clearcut-and-plant only for the
  whole TFL 6 base case.
- CT and fertilization hooks are limited to K3Z/NICF core or accepted NICF
  expansion groups once those groups are explicitly activated.

P3.1 Cedar Signals
------------------

P3.1 records the first cedar evidence and locks the source-derived cedar
signals that Phase 4 must carry into the model-input bundle. The design
responds to two teaching needs:

- make cedar cultural and old-cedar availability visible instead of reducing
  cedar to generic harvest volume; and
- let students compare NICF/community cedar interests against broader TFL 6
  and WFP-facing fibre-supply, value-proxy, and delivered-cost-proxy outcomes.

Accepted cedar source signals:

.. list-table::
   :header-rows: 1

   * - Signal
     - First definition
     - First behavior
   * - ``cedar_leading``
     - primary species is western redcedar or yellow-cedar
     - reporting/account signal only
   * - ``western_redcedar_leading``
     - primary species is western redcedar
     - Cw-specific cultural and product reporting
   * - ``yellow_cedar_leading``
     - primary species is yellow-cedar
     - Yc-specific reporting without conflating it with Cw
   * - ``cedar_present``
     - western redcedar plus yellow-cedar component share is at least 20%
     - mixed-stand cedar reporting signal
   * - ``old_cedar``
     - ``cedar_present`` and first or second species age is at least 141 years
     - first old-cedar proxy for reporting
   * - ``large_cedar_proxy``
     - unresolved diameter, height, or grade proxy
     - optional/null until a reviewed threshold exists
   * - ``cedar_cultural_reserve_context``
     - cedar signal in non-THLB, retained, reserve, or unmanaged context
     - report-only base-model signal
   * - ``cedar_harvest_candidate``
     - cedar signal in accepted THLB and managed treatment-eligible area
     - report where cedar may enter scheduled harvest

Gross P3.1 review diagnostics from the accepted stand-to-AU review surface:

.. list-table::
   :header-rows: 1

   * - Signal
     - Rows
     - Gross area
   * - ``western_redcedar_leading``
     - 3868
     - 27980.000 ha
   * - ``yellow_cedar_leading``
     - 659
     - 5446.870 ha
   * - ``cedar_leading``
     - 4527
     - 33426.800 ha
   * - ``cedar_present >= 20%``
     - 8454
     - 62963.700 ha
   * - ``old_cedar``
     - 3838
     - 23058.300 ha
   * - ``cedar_present >= 20%`` inside selected top-90 strata
     - 7255
     - 54734.200 ha

These are review diagnostics, not final Patchworks account values. Phase 4
must recompute them against the final model-input bundle after THLB, retention,
managed/unmanaged treatment eligibility, K3Z/NICF identity, and expansion fields
are present.

Cedar Product And Account Boundary
----------------------------------

The first runtime package should carry product and account hooks for generic
cedar reporting, but it should not invent utility-pole grade, price premiums,
or hard cedar reserve targets.

Accepted first-bundle hooks:

- generic cedar, western redcedar, and yellow-cedar volume reporting;
- cedar-leading, cedar-present, and old-cedar area accounts;
- cultural cedar context in unmanaged, retained, reserve, or non-THLB area;
- scheduled cedar harvest reports by embedded group and harvest system;
- unresolved utility-pole candidate warnings where source fields are
  insufficient; and
- stakeholder comparison reports that show NICF/community cedar outcomes
  alongside WFP-facing fibre-supply, value-proxy, and delivered-cost-proxy
  outcomes.

Deferred cedar decisions:

- utility-pole diameter, height, log-grade, or value thresholds;
- cedar-specific base treatments;
- hard cedar reserve targets;
- cedar-only yield-curve families; and
- automatic THLB exclusions based only on cedar status.

P3.2 Embedded NICF/K3Z Identity
-------------------------------

P3.2 preserves K3Z/NICF identity and expansion opportunity as stand-level or
source-level grouping attributes. These identities are used for accounts,
targets, toggles, and reports. They are not AU fields.

The accepted K3Z/NICF core source is the original K3Z teaching-instance tenure
boundary. Overlay diagnostics showed that the K3Z tenure is 2391.511 ha, but
only 0.072 ha intersects the current FADM-derived TFL 6 AOI. Therefore the
first TFL 6 bundle must not silently label broad current-AOI TFL 6 stands as
``nicf_k3z_core``.

Accepted identity classes:

.. list-table::
   :header-rows: 1

   * - Class
     - Meaning
     - First behavior
   * - ``wfp_tfl6_remainder``
     - current-AOI TFL 6 stands outside the near-zero K3Z overlap
     - default current-AOI TFL 6 base class
   * - ``nicf_k3z_core_reference``
     - original K3Z tenure identity carried as external/reference provenance
     - report/reference class unless a later broadened-geometry lane activates it
   * - ``nicf_expansion_candidate``
     - proximal or adjacent public forested land outside the current TFL 6 AOI
       that passes a reviewed expansion screen
     - external expansion scenario/reporting class
   * - ``nicf_expansion_rejected``
     - outside-AOI public forest land considered but rejected by screen rules
     - rejected-pool audit/reporting class
   * - ``nicf_expansion_pool_unreviewed``
     - outside-AOI public forest land inside a candidate search envelope before
       screening
     - temporary QA status only, not active in the first runtime package

Expansion candidates come from outside the current TFL 6 AOI. They should be
proximal or adjacent to the K3Z/NICF context, drawn from public forested land,
and screened for THLB-equivalent eligibility, operability, productivity,
tenure/public-land availability, constraint context, source quality, and
maintainer review. Exact geometry and screening execution belong to Phase 4 or
a later explicitly scoped implementation lane.

Patchworks Comparison Surfaces
------------------------------

P3.2d defines the Patchworks comparison surfaces needed to make the stakeholder
tradeoffs visible.

Required group dimensions:

- ``embedded_area_class``;
- ``embedded_area_id``;
- ``inside_tfl6_aoi``;
- ``outside_tfl6_aoi_expansion_source``;
- ``expansion_candidate_set``;
- ``expansion_scenario_group``;
- ``expansion_screen_status``; and
- ``core_overlay_status``.

Required account families:

- gross and schedulable area by embedded class and AOI membership;
- managed/unmanaged area by THLB or THLB-equivalent status;
- harvest area and harvest volume by embedded class, treatment, AU, product
  group, and harvest system;
- residual inventory by embedded class, AU, cedar signal, age class, and harvest
  system;
- delivered-cost proxy accounts using ground/cable/heli harvest-system classes;
- cedar signal accounts by embedded group; and
- rejected-pool diagnostics by rejection reason, source quality, and
  tenure/public-land availability.

Required matching targets and reports:

- whole TFL 6 versus WFP remainder;
- K3Z reference versus accepted expansion candidates;
- accepted expansion candidates versus rejected candidate pools;
- expansion scenario uplift in area, THLB-equivalent area, harvest area, and
  harvest volume;
- WFP-facing fibre-supply and value-proxy impacts;
- delivered-cost proxy shifts by harvest system;
- cedar/community outcomes; and
- K3Z continuity reports linking the TFL 6 teaching model back to the original
  K3Z instance.

Scenario Toggles
----------------

The first Patchworks-facing design should support these scenario controls:

.. list-table::
   :header-rows: 1

   * - Toggle
     - Effect
     - Guardrail
   * - ``base_tfl6_only``
     - use current-AOI TFL 6 stands and report K3Z as reference/provenance
     - default first-runtime behavior
   * - ``include_nicf_expansion_candidates``
     - activate reviewed outside-AOI accepted candidates for scenario comparison
     - never includes rejected or unreviewed pools
   * - ``report_rejected_expansion_pool``
     - expose rejected-pool area and rejection reasons
     - report-only, not schedulable
   * - ``k3z_reference_reporting``
     - report original K3Z tenure continuity alongside TFL 6 outputs
     - report-only unless later broadened geometry is accepted
   * - ``nicf_ct_fert_eligible_groups``
     - gate CT/fertilization hooks to K3Z reference/core and accepted expansion
       candidates
     - no CT/fert activation outside reviewed NICF groups

P3.2e Handoff To P3.7 And P4.1
------------------------------

P3.2e closes the embedded identity design lane by defining what later contract
and implementation lanes must carry forward. The handoff remains design-only:
it does not materialize outside-AOI expansion geometry, run candidate screening,
generate model-input tables, emit ForestModel XML, run Matrix Builder, or build
a Patchworks runtime package.

Required model-input contract fields:

- ``embedded_area_class``;
- ``embedded_area_id``;
- ``inside_tfl6_aoi``;
- ``outside_tfl6_aoi_expansion_source``;
- ``is_nicf_k3z_core``;
- ``nicf_k3z_core_external_reference``;
- ``core_overlay_status``;
- ``is_nicf_expansion_candidate``;
- ``is_nicf_expansion_rejected``;
- ``expansion_candidate_set``;
- ``expansion_screen_status``;
- ``expansion_screen_reason``; and
- ``expansion_scenario_group``.

Phase 4 model-input generation must keep current-AOI TFL 6 base stands
separate from external expansion source geography. Rejected and unreviewed
expansion pools are report/audit surfaces only. Embedded-area fields may split
accounts, targets, toggles, reports, treatment eligibility, harvest-system
summaries, cedar outputs, and THLB-equivalent summaries, but they must not
become AU keys, curve-family keys, or hidden THLB deductions.

Reproducibility Trail
---------------------

Canonical planning sources:

- ``planning/tfl6_cedar_signal_design.md``
- ``planning/tfl6_nicf_embedded_identity.md``
- ``planning/tfl6_stakeholder_context.md``
- ``planning/tfl6_treatment_option_contract.md``
- ``planning/tfl6_state_transition_contract.md``

Roadmap and issue anchors:

- P3.1 cedar design: issue ``#8``.
- P3.2 embedded NICF/K3Z and expansion design: issue ``#9``.
- Phase 3 parent: issue ``#13``.

Phase 4 must carry these fields into the model-input contract before building
ForestModel XML or Matrix Builder outputs. Any final runtime account names may
be refined in P3.7/P4.1, but the reporting content above is the accepted Phase
3 design intent.
