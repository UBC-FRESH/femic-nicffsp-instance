Phase 3 Model-Input Contract
============================

Purpose
-------

This page summarizes the P3.7 handoff from reviewed model-design assumptions
to Phase 4 model-input bundle generation. It is a maintainer and student audit
surface, not an executable bundle build.

Phase 4 remains responsible for generating model-input tables, ForestModel XML,
Matrix Builder outputs, and Patchworks runtime packages.

Accepted Contract Sources
-------------------------

The Phase 4 bundle build should start from these reviewed sources:

- ``config/run_profile.tfl6.yaml``;
- ``planning/tfl6_model_input_contract.md``;
- ``planning/tfl6_au_yield_curve_contract.md``;
- ``planning/tfl6_static_au_universe.{csv,json,md}``;
- ``planning/tfl6_stand_to_au_review.csv``;
- ``planning/tfl6_first_growth_au_curves.csv``;
- ``planning/tfl6_first_growth_shape_diagnostics.{csv,md}``;
- ``planning/tfl6_first_growth_au_remap_audit.{csv,md}``;
- ``planning/tfl6_mp10_tipsy_parameter_library.{csv,json,md}``;
- ``planning/tfl6_tipsy_parameter_crosswalk.{csv,json,md}``;
- ``data/03_input-tfl6.csv``;
- ``data/04_output-tfl6.csv`` and ``data/04_error-tfl6.csv``;
- ``planning/tfl6_tipsy_managed_curves.csv``;
- ``planning/tfl6_tipsy_managed_curve_diagnostics.{csv,md}``;
- ``planning/tfl6_treatment_option_contract.md``;
- ``config/silviculture.tfl6.yaml``;
- ``planning/tfl6_state_transition_contract.md``;
- ``planning/tfl6_cedar_signal_design.md``; and
- ``planning/tfl6_nicf_embedded_identity.md``.

Required Field Families
-----------------------

P4.1 should produce or preserve these semantic field families:

.. list-table::
   :header-rows: 1

   * - Field family
     - Purpose
   * - Stand identity
     - stable source and fragment keys for joins and QA
   * - Area accounting
     - hectares and current-AOI membership
   * - THLB / IFM
     - THLB status, managed treatment eligibility, retention, reserve, and
       unmanaged context
   * - Curve provenance
     - natural/untreated and treated/managed curve IDs without conflating them
       with managed/unmanaged eligibility
   * - Static AU
     - BEC/species/site-index class identity
   * - AU remap
     - selected top-area curve-family remap for non-selected AU bins
   * - Yield curves
     - natural and treated curve table keys and diagnostics
   * - Treatment options
     - clearcut-and-plant base treatment plus CT/fertilization hooks
   * - Transitions
     - grow, retained, harvested, regenerated, and deferred/special states
   * - Harvest system
     - ground-based, cable, and heli classes for eligibility and cost proxies
   * - Cedar
     - cedar-leading, cedar-present, cedar percentage, old-cedar, and unresolved
       large/pole proxy signals
   * - Embedded identity
     - TFL 6 remainder, K3Z reference, outside-AOI expansion, and rejected or
       unreviewed expansion pools
   * - Reporting groups
     - group splits for Patchworks accounts, targets, toggles, and reports

Guardrails
----------

P4.1 must preserve these Phase 3 boundaries:

- current-AOI TFL 6 area must not include outside-AOI expansion source lands;
- rejected and unreviewed expansion pools are report/audit surfaces only;
- embedded identity and cedar status are not AU keys or curve-family keys;
- managed/unmanaged treatment eligibility remains separate from natural/treated
  curve provenance;
- harvest-system classes are eligibility and reporting fields, not AU identity;
- base scheduled treatment remains ``clearcut_and_plant`` for the whole TFL 6
  base case;
- CT and fertilization remain gated to reviewed K3Z/NICF and accepted expansion
  groups; and
- cedar cultural reserve, utility-pole grade, cedar hard targets, and
  cedar-only curve families remain deferred unless a later reviewed scenario
  lane activates them.

Reproducibility Trail
---------------------

The canonical detailed contract is
``planning/tfl6_model_input_contract.md``. The active config metadata is in
``config/run_profile.tfl6.yaml`` and ``config/tipsy/tfl6.yaml``. Issue ``#32``
tracks the P3.7 reconciliation lane under the Phase 3 parent ``#13``.
