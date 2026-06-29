Phase 3 Analysis Units and Yield Curves
========================================

Purpose
-------

This page is the student- and maintainer-facing gallery for the Phase 3
TFL 6 analysis-unit and yield-curve work. It gathers the static AU
definition, selected-strata plot, natural VDYP first-growth plots, and
treated BatchTIPSY-vs-VDYP overlays in one place.

The page is a documentation surface, not a model-input bundle. Phase 4
still owns the final Patchworks-facing bundle, XML, Matrix Builder, and
runtime package work.

AU Definition Contract
----------------------

The accepted Phase 3 AU policy is static and K3Z-style:

- BEC zone, subzone, variant, and phase where present;
- top-two VDYP primary-layer species combination;
- stratum-local low/medium/high site-index class; and
- no age, THLB status, operability, treatment eligibility, cedar status,
  NICF identity, or expansion status in the AU key.

The current source review universe contains ``174`` static strata, ``26``
selected top-area strata covering ``90.397%`` of the yieldable review
area, ``384`` source stratum bins, and ``77`` canonical top-N L/M/H AUs.

Canonical review files:

- ``planning/tfl6_au_yield_curve_contract.md``
- ``planning/tfl6_static_au_universe.{csv,json,md}``
- ``planning/tfl6_source_stratum_bin_universe.{csv,json,md}``
- ``planning/tfl6_static_au_top_strata.csv``
- ``planning/tfl6_stand_to_au_review.csv``
- ``planning/tfl6_tipsy_parameter_crosswalk.{csv,json,md}``

Strata Diagnostic
-----------------

The strata diagnostic uses the same FEMIC plot specification as the
other instance examples, widened to a ``0-55`` SI axis for the highly
productive coastal rainforest setting.

.. figure:: ../plots/strata-tfl6.png
   :alt: strata-tfl6.png
   :width: 95%

   TFL 6 selected-strata area and site-index distribution plot.

Yield Curve Artifacts
---------------------

Natural/untreated first-growth curves use the canonical top-N AU set
and the shared FEMIC smoothing lane. Non-AU source stratum bins are imputed to
selected curve families through the lexicographic remap audit.

Treated/managed curves use the reviewed MP10 Tables 27-29 parameter
crosswalk and the BTC/BatchTIPSY output generated from
``data/03_input-tfl6.csv``.

.. list-table::
   :header-rows: 1

   * - Artifact
     - Path
   * - Natural VDYP curves
     - ``planning/tfl6_first_growth_au_curves.csv``
   * - Natural VDYP fit diagnostics
     - ``planning/tfl6_first_growth_shape_diagnostics.{csv,md}``
   * - Non-AU source-bin remap audit
     - ``planning/tfl6_first_growth_au_remap_audit.{csv,md}``
   * - BTC handoff
     - ``data/03_input-tfl6.csv``
   * - BTC output
     - ``data/04_output-tfl6.csv`` and ``data/04_error-tfl6.csv``
   * - Parsed treated curves
     - ``planning/tfl6_tipsy_managed_curves.csv``
   * - Treated-curve diagnostics
     - ``planning/tfl6_tipsy_managed_curve_diagnostics.{csv,md}``

Gallery Counts
--------------

- VDYP L/M/H comparison panels: ``26``
- VDYP fit-diagnostic panels: ``77``
- TIPSY-vs-VDYP treated overlay panels: ``77``

Review Caveats
--------------

- The selected natural VDYP curve set remains a review surface; smoothing,
  tail constraints, and LMH order gates may be revisited before final
  model-input bundle lock.
- Small fallback ``CWHvm1_DR`` treated rows have high treated-to-natural
  ratios. They remain visible in
  ``planning/tfl6_tipsy_managed_curve_diagnostics.{csv,md}`` for later
  bundle QA.
- MP10 legacy AU codes are parameter provenance only. They are not
  canonical Patchworks AU identities.

VDYP L/M/H Comparison Gallery
-----------------------------

Selected Strata L/M/H Panels
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: ../plots/vdyp_lmh_tfl6-cwhvh1_cw_hw.png
   :alt: vdyp_lmh_tfl6-cwhvh1_cw_hw.png
   :width: 95%

   Natural VDYP L/M/H comparison panel for stratum ``cwhvh1_cw_hw``.

.. figure:: ../plots/vdyp_lmh_tfl6-cwhvh1_hw_ba.png
   :alt: vdyp_lmh_tfl6-cwhvh1_hw_ba.png
   :width: 95%

   Natural VDYP L/M/H comparison panel for stratum ``cwhvh1_hw_ba``.

.. figure:: ../plots/vdyp_lmh_tfl6-cwhvh1_hw_cw.png
   :alt: vdyp_lmh_tfl6-cwhvh1_hw_cw.png
   :width: 95%

   Natural VDYP L/M/H comparison panel for stratum ``cwhvh1_hw_cw``.

.. figure:: ../plots/vdyp_lmh_tfl6-cwhvh1_hw_ss.png
   :alt: vdyp_lmh_tfl6-cwhvh1_hw_ss.png
   :width: 95%

   Natural VDYP L/M/H comparison panel for stratum ``cwhvh1_hw_ss``.

.. figure:: ../plots/vdyp_lmh_tfl6-cwhvm1_ba_hw.png
   :alt: vdyp_lmh_tfl6-cwhvm1_ba_hw.png
   :width: 95%

   Natural VDYP L/M/H comparison panel for stratum ``cwhvm1_ba_hw``.

.. figure:: ../plots/vdyp_lmh_tfl6-cwhvm1_cw.png
   :alt: vdyp_lmh_tfl6-cwhvm1_cw.png
   :width: 95%

   Natural VDYP L/M/H comparison panel for stratum ``cwhvm1_cw``.

.. figure:: ../plots/vdyp_lmh_tfl6-cwhvm1_cw_hw.png
   :alt: vdyp_lmh_tfl6-cwhvm1_cw_hw.png
   :width: 95%

   Natural VDYP L/M/H comparison panel for stratum ``cwhvm1_cw_hw``.

.. figure:: ../plots/vdyp_lmh_tfl6-cwhvm1_cw_yc.png
   :alt: vdyp_lmh_tfl6-cwhvm1_cw_yc.png
   :width: 95%

   Natural VDYP L/M/H comparison panel for stratum ``cwhvm1_cw_yc``.

.. figure:: ../plots/vdyp_lmh_tfl6-cwhvm1_dr.png
   :alt: vdyp_lmh_tfl6-cwhvm1_dr.png
   :width: 95%

   Natural VDYP L/M/H comparison panel for stratum ``cwhvm1_dr``.

.. figure:: ../plots/vdyp_lmh_tfl6-cwhvm1_dr_hw.png
   :alt: vdyp_lmh_tfl6-cwhvm1_dr_hw.png
   :width: 95%

   Natural VDYP L/M/H comparison panel for stratum ``cwhvm1_dr_hw``.

.. figure:: ../plots/vdyp_lmh_tfl6-cwhvm1_hw.png
   :alt: vdyp_lmh_tfl6-cwhvm1_hw.png
   :width: 95%

   Natural VDYP L/M/H comparison panel for stratum ``cwhvm1_hw``.

.. figure:: ../plots/vdyp_lmh_tfl6-cwhvm1_hw_ba.png
   :alt: vdyp_lmh_tfl6-cwhvm1_hw_ba.png
   :width: 95%

   Natural VDYP L/M/H comparison panel for stratum ``cwhvm1_hw_ba``.

.. figure:: ../plots/vdyp_lmh_tfl6-cwhvm1_hw_cw.png
   :alt: vdyp_lmh_tfl6-cwhvm1_hw_cw.png
   :width: 95%

   Natural VDYP L/M/H comparison panel for stratum ``cwhvm1_hw_cw``.

.. figure:: ../plots/vdyp_lmh_tfl6-cwhvm1_hw_dr.png
   :alt: vdyp_lmh_tfl6-cwhvm1_hw_dr.png
   :width: 95%

   Natural VDYP L/M/H comparison panel for stratum ``cwhvm1_hw_dr``.

.. figure:: ../plots/vdyp_lmh_tfl6-cwhvm1_hw_fd.png
   :alt: vdyp_lmh_tfl6-cwhvm1_hw_fd.png
   :width: 95%

   Natural VDYP L/M/H comparison panel for stratum ``cwhvm1_hw_fd``.

.. figure:: ../plots/vdyp_lmh_tfl6-cwhvm1_hw_fdc.png
   :alt: vdyp_lmh_tfl6-cwhvm1_hw_fdc.png
   :width: 95%

   Natural VDYP L/M/H comparison panel for stratum ``cwhvm1_hw_fdc``.

.. figure:: ../plots/vdyp_lmh_tfl6-cwhvm1_hw_ss.png
   :alt: vdyp_lmh_tfl6-cwhvm1_hw_ss.png
   :width: 95%

   Natural VDYP L/M/H comparison panel for stratum ``cwhvm1_hw_ss``.

.. figure:: ../plots/vdyp_lmh_tfl6-cwhvm1_ss_hw.png
   :alt: vdyp_lmh_tfl6-cwhvm1_ss_hw.png
   :width: 95%

   Natural VDYP L/M/H comparison panel for stratum ``cwhvm1_ss_hw``.

.. figure:: ../plots/vdyp_lmh_tfl6-cwhvm1_yc_cw.png
   :alt: vdyp_lmh_tfl6-cwhvm1_yc_cw.png
   :width: 95%

   Natural VDYP L/M/H comparison panel for stratum ``cwhvm1_yc_cw``.

.. figure:: ../plots/vdyp_lmh_tfl6-cwhvm1_yc_hw.png
   :alt: vdyp_lmh_tfl6-cwhvm1_yc_hw.png
   :width: 95%

   Natural VDYP L/M/H comparison panel for stratum ``cwhvm1_yc_hw``.

.. figure:: ../plots/vdyp_lmh_tfl6-cwhvm2_ba_hw.png
   :alt: vdyp_lmh_tfl6-cwhvm2_ba_hw.png
   :width: 95%

   Natural VDYP L/M/H comparison panel for stratum ``cwhvm2_ba_hw``.

.. figure:: ../plots/vdyp_lmh_tfl6-cwhvm2_cw_hw.png
   :alt: vdyp_lmh_tfl6-cwhvm2_cw_hw.png
   :width: 95%

   Natural VDYP L/M/H comparison panel for stratum ``cwhvm2_cw_hw``.

.. figure:: ../plots/vdyp_lmh_tfl6-cwhvm2_hw_ba.png
   :alt: vdyp_lmh_tfl6-cwhvm2_hw_ba.png
   :width: 95%

   Natural VDYP L/M/H comparison panel for stratum ``cwhvm2_hw_ba``.

.. figure:: ../plots/vdyp_lmh_tfl6-cwhvm2_hw_cw.png
   :alt: vdyp_lmh_tfl6-cwhvm2_hw_cw.png
   :width: 95%

   Natural VDYP L/M/H comparison panel for stratum ``cwhvm2_hw_cw``.

.. figure:: ../plots/vdyp_lmh_tfl6-cwhvm2_hw_yc.png
   :alt: vdyp_lmh_tfl6-cwhvm2_hw_yc.png
   :width: 95%

   Natural VDYP L/M/H comparison panel for stratum ``cwhvm2_hw_yc``.

.. figure:: ../plots/vdyp_lmh_tfl6-cwhvm2_yc_hw.png
   :alt: vdyp_lmh_tfl6-cwhvm2_yc_hw.png
   :width: 95%

   Natural VDYP L/M/H comparison panel for stratum ``cwhvm2_yc_hw``.

VDYP Fit-Diagnostic Gallery
---------------------------

Selected AU Fit-Diagnostic Panels
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvh1_cw_hw_h.png
   :alt: vdyp_fitdiag_tfl6-cwhvh1_cw_hw_h.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvh1_cw_hw_h``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvh1_cw_hw_l.png
   :alt: vdyp_fitdiag_tfl6-cwhvh1_cw_hw_l.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvh1_cw_hw_l``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvh1_cw_hw_m.png
   :alt: vdyp_fitdiag_tfl6-cwhvh1_cw_hw_m.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvh1_cw_hw_m``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvh1_hw_ba_h.png
   :alt: vdyp_fitdiag_tfl6-cwhvh1_hw_ba_h.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvh1_hw_ba_h``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvh1_hw_ba_l.png
   :alt: vdyp_fitdiag_tfl6-cwhvh1_hw_ba_l.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvh1_hw_ba_l``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvh1_hw_ba_m.png
   :alt: vdyp_fitdiag_tfl6-cwhvh1_hw_ba_m.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvh1_hw_ba_m``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvh1_hw_cw_h.png
   :alt: vdyp_fitdiag_tfl6-cwhvh1_hw_cw_h.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvh1_hw_cw_h``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvh1_hw_cw_l.png
   :alt: vdyp_fitdiag_tfl6-cwhvh1_hw_cw_l.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvh1_hw_cw_l``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvh1_hw_cw_m.png
   :alt: vdyp_fitdiag_tfl6-cwhvh1_hw_cw_m.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvh1_hw_cw_m``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvh1_hw_ss_h.png
   :alt: vdyp_fitdiag_tfl6-cwhvh1_hw_ss_h.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvh1_hw_ss_h``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvh1_hw_ss_l.png
   :alt: vdyp_fitdiag_tfl6-cwhvh1_hw_ss_l.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvh1_hw_ss_l``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvh1_hw_ss_m.png
   :alt: vdyp_fitdiag_tfl6-cwhvh1_hw_ss_m.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvh1_hw_ss_m``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_ba_hw_h.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_ba_hw_h.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_ba_hw_h``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_ba_hw_l.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_ba_hw_l.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_ba_hw_l``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_ba_hw_m.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_ba_hw_m.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_ba_hw_m``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_cw_h.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_cw_h.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_cw_h``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_cw_hw_h.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_cw_hw_h.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_cw_hw_h``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_cw_hw_l.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_cw_hw_l.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_cw_hw_l``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_cw_hw_m.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_cw_hw_m.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_cw_hw_m``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_cw_l.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_cw_l.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_cw_l``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_cw_m.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_cw_m.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_cw_m``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_cw_yc_h.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_cw_yc_h.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_cw_yc_h``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_cw_yc_l.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_cw_yc_l.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_cw_yc_l``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_cw_yc_m.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_cw_yc_m.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_cw_yc_m``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_dr_h.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_dr_h.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_dr_h``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_dr_hw_h.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_dr_hw_h.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_dr_hw_h``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_dr_hw_l.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_dr_hw_l.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_dr_hw_l``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_dr_hw_m.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_dr_hw_m.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_dr_hw_m``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_dr_l.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_dr_l.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_dr_l``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_dr_m.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_dr_m.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_dr_m``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_hw_ba_h.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_hw_ba_h.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_hw_ba_h``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_hw_ba_l.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_hw_ba_l.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_hw_ba_l``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_hw_ba_m.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_hw_ba_m.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_hw_ba_m``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_hw_cw_h.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_hw_cw_h.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_hw_cw_h``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_hw_cw_l.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_hw_cw_l.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_hw_cw_l``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_hw_cw_m.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_hw_cw_m.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_hw_cw_m``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_hw_dr_h.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_hw_dr_h.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_hw_dr_h``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_hw_dr_l.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_hw_dr_l.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_hw_dr_l``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_hw_dr_m.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_hw_dr_m.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_hw_dr_m``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_hw_fd_h.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_hw_fd_h.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_hw_fd_h``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_hw_fd_l.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_hw_fd_l.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_hw_fd_l``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_hw_fd_m.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_hw_fd_m.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_hw_fd_m``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_hw_fdc_h.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_hw_fdc_h.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_hw_fdc_h``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_hw_fdc_l.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_hw_fdc_l.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_hw_fdc_l``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_hw_h.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_hw_h.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_hw_h``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_hw_l.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_hw_l.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_hw_l``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_hw_m.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_hw_m.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_hw_m``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_hw_ss_h.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_hw_ss_h.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_hw_ss_h``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_hw_ss_l.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_hw_ss_l.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_hw_ss_l``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_hw_ss_m.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_hw_ss_m.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_hw_ss_m``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_ss_hw_h.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_ss_hw_h.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_ss_hw_h``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_ss_hw_l.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_ss_hw_l.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_ss_hw_l``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_ss_hw_m.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_ss_hw_m.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_ss_hw_m``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_yc_cw_h.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_yc_cw_h.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_yc_cw_h``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_yc_cw_l.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_yc_cw_l.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_yc_cw_l``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_yc_cw_m.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_yc_cw_m.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_yc_cw_m``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_yc_hw_h.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_yc_hw_h.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_yc_hw_h``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_yc_hw_l.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_yc_hw_l.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_yc_hw_l``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm1_yc_hw_m.png
   :alt: vdyp_fitdiag_tfl6-cwhvm1_yc_hw_m.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm1_yc_hw_m``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm2_ba_hw_h.png
   :alt: vdyp_fitdiag_tfl6-cwhvm2_ba_hw_h.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm2_ba_hw_h``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm2_ba_hw_l.png
   :alt: vdyp_fitdiag_tfl6-cwhvm2_ba_hw_l.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm2_ba_hw_l``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm2_ba_hw_m.png
   :alt: vdyp_fitdiag_tfl6-cwhvm2_ba_hw_m.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm2_ba_hw_m``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm2_cw_hw_h.png
   :alt: vdyp_fitdiag_tfl6-cwhvm2_cw_hw_h.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm2_cw_hw_h``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm2_cw_hw_l.png
   :alt: vdyp_fitdiag_tfl6-cwhvm2_cw_hw_l.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm2_cw_hw_l``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm2_cw_hw_m.png
   :alt: vdyp_fitdiag_tfl6-cwhvm2_cw_hw_m.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm2_cw_hw_m``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm2_hw_ba_h.png
   :alt: vdyp_fitdiag_tfl6-cwhvm2_hw_ba_h.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm2_hw_ba_h``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm2_hw_ba_l.png
   :alt: vdyp_fitdiag_tfl6-cwhvm2_hw_ba_l.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm2_hw_ba_l``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm2_hw_ba_m.png
   :alt: vdyp_fitdiag_tfl6-cwhvm2_hw_ba_m.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm2_hw_ba_m``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm2_hw_cw_h.png
   :alt: vdyp_fitdiag_tfl6-cwhvm2_hw_cw_h.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm2_hw_cw_h``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm2_hw_cw_l.png
   :alt: vdyp_fitdiag_tfl6-cwhvm2_hw_cw_l.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm2_hw_cw_l``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm2_hw_cw_m.png
   :alt: vdyp_fitdiag_tfl6-cwhvm2_hw_cw_m.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm2_hw_cw_m``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm2_hw_yc_h.png
   :alt: vdyp_fitdiag_tfl6-cwhvm2_hw_yc_h.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm2_hw_yc_h``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm2_hw_yc_l.png
   :alt: vdyp_fitdiag_tfl6-cwhvm2_hw_yc_l.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm2_hw_yc_l``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm2_hw_yc_m.png
   :alt: vdyp_fitdiag_tfl6-cwhvm2_hw_yc_m.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm2_hw_yc_m``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm2_yc_hw_h.png
   :alt: vdyp_fitdiag_tfl6-cwhvm2_yc_hw_h.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm2_yc_hw_h``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm2_yc_hw_l.png
   :alt: vdyp_fitdiag_tfl6-cwhvm2_yc_hw_l.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm2_yc_hw_l``.

.. figure:: ../plots/vdyp_fitdiag_tfl6-cwhvm2_yc_hw_m.png
   :alt: vdyp_fitdiag_tfl6-cwhvm2_yc_hw_m.png
   :width: 95%

   Natural VDYP fit-diagnostic panel for AU ``cwhvm2_yc_hw_m``.

TIPSY-vs-VDYP Treated Overlay Gallery
-------------------------------------

Selected AU Treated Overlay Panels
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvh1_cw_hw_h.png
   :alt: tipsy_vdyp_tfl6-cwhvh1_cw_hw_h.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvh1_cw_hw_h``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvh1_cw_hw_l.png
   :alt: tipsy_vdyp_tfl6-cwhvh1_cw_hw_l.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvh1_cw_hw_l``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvh1_cw_hw_m.png
   :alt: tipsy_vdyp_tfl6-cwhvh1_cw_hw_m.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvh1_cw_hw_m``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvh1_hw_ba_h.png
   :alt: tipsy_vdyp_tfl6-cwhvh1_hw_ba_h.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvh1_hw_ba_h``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvh1_hw_ba_l.png
   :alt: tipsy_vdyp_tfl6-cwhvh1_hw_ba_l.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvh1_hw_ba_l``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvh1_hw_ba_m.png
   :alt: tipsy_vdyp_tfl6-cwhvh1_hw_ba_m.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvh1_hw_ba_m``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvh1_hw_cw_h.png
   :alt: tipsy_vdyp_tfl6-cwhvh1_hw_cw_h.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvh1_hw_cw_h``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvh1_hw_cw_l.png
   :alt: tipsy_vdyp_tfl6-cwhvh1_hw_cw_l.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvh1_hw_cw_l``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvh1_hw_cw_m.png
   :alt: tipsy_vdyp_tfl6-cwhvh1_hw_cw_m.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvh1_hw_cw_m``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvh1_hw_ss_h.png
   :alt: tipsy_vdyp_tfl6-cwhvh1_hw_ss_h.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvh1_hw_ss_h``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvh1_hw_ss_l.png
   :alt: tipsy_vdyp_tfl6-cwhvh1_hw_ss_l.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvh1_hw_ss_l``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvh1_hw_ss_m.png
   :alt: tipsy_vdyp_tfl6-cwhvh1_hw_ss_m.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvh1_hw_ss_m``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_ba_hw_h.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_ba_hw_h.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_ba_hw_h``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_ba_hw_l.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_ba_hw_l.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_ba_hw_l``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_ba_hw_m.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_ba_hw_m.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_ba_hw_m``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_cw_h.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_cw_h.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_cw_h``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_cw_hw_h.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_cw_hw_h.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_cw_hw_h``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_cw_hw_l.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_cw_hw_l.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_cw_hw_l``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_cw_hw_m.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_cw_hw_m.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_cw_hw_m``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_cw_l.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_cw_l.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_cw_l``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_cw_m.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_cw_m.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_cw_m``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_cw_yc_h.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_cw_yc_h.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_cw_yc_h``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_cw_yc_l.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_cw_yc_l.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_cw_yc_l``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_cw_yc_m.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_cw_yc_m.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_cw_yc_m``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_dr_h.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_dr_h.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_dr_h``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_dr_hw_h.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_dr_hw_h.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_dr_hw_h``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_dr_hw_l.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_dr_hw_l.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_dr_hw_l``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_dr_hw_m.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_dr_hw_m.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_dr_hw_m``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_dr_l.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_dr_l.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_dr_l``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_dr_m.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_dr_m.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_dr_m``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_hw_ba_h.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_hw_ba_h.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_hw_ba_h``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_hw_ba_l.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_hw_ba_l.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_hw_ba_l``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_hw_ba_m.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_hw_ba_m.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_hw_ba_m``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_hw_cw_h.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_hw_cw_h.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_hw_cw_h``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_hw_cw_l.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_hw_cw_l.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_hw_cw_l``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_hw_cw_m.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_hw_cw_m.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_hw_cw_m``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_hw_dr_h.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_hw_dr_h.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_hw_dr_h``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_hw_dr_l.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_hw_dr_l.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_hw_dr_l``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_hw_dr_m.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_hw_dr_m.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_hw_dr_m``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_hw_fd_h.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_hw_fd_h.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_hw_fd_h``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_hw_fd_l.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_hw_fd_l.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_hw_fd_l``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_hw_fd_m.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_hw_fd_m.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_hw_fd_m``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_hw_fdc_h.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_hw_fdc_h.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_hw_fdc_h``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_hw_fdc_l.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_hw_fdc_l.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_hw_fdc_l``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_hw_h.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_hw_h.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_hw_h``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_hw_l.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_hw_l.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_hw_l``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_hw_m.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_hw_m.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_hw_m``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_hw_ss_h.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_hw_ss_h.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_hw_ss_h``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_hw_ss_l.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_hw_ss_l.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_hw_ss_l``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_hw_ss_m.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_hw_ss_m.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_hw_ss_m``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_ss_hw_h.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_ss_hw_h.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_ss_hw_h``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_ss_hw_l.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_ss_hw_l.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_ss_hw_l``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_ss_hw_m.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_ss_hw_m.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_ss_hw_m``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_yc_cw_h.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_yc_cw_h.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_yc_cw_h``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_yc_cw_l.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_yc_cw_l.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_yc_cw_l``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_yc_cw_m.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_yc_cw_m.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_yc_cw_m``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_yc_hw_h.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_yc_hw_h.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_yc_hw_h``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_yc_hw_l.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_yc_hw_l.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_yc_hw_l``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm1_yc_hw_m.png
   :alt: tipsy_vdyp_tfl6-cwhvm1_yc_hw_m.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm1_yc_hw_m``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm2_ba_hw_h.png
   :alt: tipsy_vdyp_tfl6-cwhvm2_ba_hw_h.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm2_ba_hw_h``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm2_ba_hw_l.png
   :alt: tipsy_vdyp_tfl6-cwhvm2_ba_hw_l.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm2_ba_hw_l``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm2_ba_hw_m.png
   :alt: tipsy_vdyp_tfl6-cwhvm2_ba_hw_m.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm2_ba_hw_m``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm2_cw_hw_h.png
   :alt: tipsy_vdyp_tfl6-cwhvm2_cw_hw_h.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm2_cw_hw_h``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm2_cw_hw_l.png
   :alt: tipsy_vdyp_tfl6-cwhvm2_cw_hw_l.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm2_cw_hw_l``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm2_cw_hw_m.png
   :alt: tipsy_vdyp_tfl6-cwhvm2_cw_hw_m.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm2_cw_hw_m``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm2_hw_ba_h.png
   :alt: tipsy_vdyp_tfl6-cwhvm2_hw_ba_h.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm2_hw_ba_h``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm2_hw_ba_l.png
   :alt: tipsy_vdyp_tfl6-cwhvm2_hw_ba_l.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm2_hw_ba_l``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm2_hw_ba_m.png
   :alt: tipsy_vdyp_tfl6-cwhvm2_hw_ba_m.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm2_hw_ba_m``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm2_hw_cw_h.png
   :alt: tipsy_vdyp_tfl6-cwhvm2_hw_cw_h.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm2_hw_cw_h``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm2_hw_cw_l.png
   :alt: tipsy_vdyp_tfl6-cwhvm2_hw_cw_l.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm2_hw_cw_l``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm2_hw_cw_m.png
   :alt: tipsy_vdyp_tfl6-cwhvm2_hw_cw_m.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm2_hw_cw_m``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm2_hw_yc_h.png
   :alt: tipsy_vdyp_tfl6-cwhvm2_hw_yc_h.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm2_hw_yc_h``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm2_hw_yc_l.png
   :alt: tipsy_vdyp_tfl6-cwhvm2_hw_yc_l.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm2_hw_yc_l``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm2_hw_yc_m.png
   :alt: tipsy_vdyp_tfl6-cwhvm2_hw_yc_m.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm2_hw_yc_m``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm2_yc_hw_h.png
   :alt: tipsy_vdyp_tfl6-cwhvm2_yc_hw_h.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm2_yc_hw_h``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm2_yc_hw_l.png
   :alt: tipsy_vdyp_tfl6-cwhvm2_yc_hw_l.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm2_yc_hw_l``.

.. figure:: ../plots/tipsy_vdyp_tfl6-cwhvm2_yc_hw_m.png
   :alt: tipsy_vdyp_tfl6-cwhvm2_yc_hw_m.png
   :width: 95%

   Treated BatchTIPSY-vs-natural VDYP overlay for AU ``cwhvm2_yc_hw_m``.
