Phase 7 MP11 Figure Extraction Test
===================================

Phase 7 used the public TFL 6 Management Plan 11 PDF as a realistic
``figrecover`` deployment test before any MP10-to-MP11 model upgrade work.

The purpose was not to make recovered figure values model inputs. The purpose
was to identify which published figures can provide auditable comparison
evidence, which figures are useful only as planning context, and which chart
classes should be deferred until the extraction tooling improves.

Source And Artifact Boundary
----------------------------

The source document is the public TFL 6 Management Plan 11 PDF. The tracked
inventory records the source URL, checksum, report page, PDF page, figure
caption, chart-family triage, extraction priority, and Phase 6 alignment for
``61`` figures:

- ``planning/tfl6_mp11_full_figure_inventory.csv``

Generated pages, crops, overlays, raw result JSON, and recovered point CSVs
remain under ignored ``runtime/`` paths. Tracked planning files are compact
summaries intended to preserve provenance without committing generated
artifacts.

Reviewed Evidence Surface
-------------------------

The final closeout files are:

- ``planning/tfl6_mp11_figure_extraction_closeout.md``
- ``planning/tfl6_mp11_figure_extraction_closeout.csv``
- ``planning/tfl6_mp11_figure_extraction_closeout.json``

Phase 7 reviewed all ``36`` high-priority figures. The final status is:

.. list-table::
   :header-rows: 1

   * - Status
     - Figure count
     - Use
   * - ``accepted_for_comparison``
     - ``22``
     - Phase 6 comparison planning only.
   * - ``reviewed_for_planning``
     - ``14``
     - Qualitative or approximate planning context only.
   * - ``deferred_not_extracted``
     - ``20``
     - Medium-priority future extraction/tooling targets.
   * - ``inventory_context_only``
     - ``5``
     - Maps, diagrams, or context images.

No recovered figure row is ``accepted_for_model_input``.

Comparison-accepted figures include the base-case harvest level, growing-stock
charts, timber-supply impact charts, and harvest/scenario line charts:

``2, 3, 20, 21, 22, 23, 24, 25, 26, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38,
39, 40, 57``.

Planning-only figures include cedar inventory, age-class distribution, and
old-seral landscape-unit charts:

``6, 14, 15, 16, 17, 18, 19, 45, 51, 52, 53, 54, 55, 56``.

Validation Pattern
------------------

Accepted comparison rows used deterministic extraction plus at least one
reviewable validation signal, such as:

- overlay inspection against the source crop;
- adjacent table or reference-value cross-check;
- component-sum consistency;
- printed-label extraction and waterfall arithmetic checks; or
- endpoint residual checks.

Planning-only rows are still useful, but their validation is weaker. They are
kept out of comparison-accepted evidence when there is no independent table,
printed value, or strong internal arithmetic check.

Phase 6 Handoff
---------------

Phase 6 may use comparison-accepted figures for MP11 extraction inventory,
scenario comparison, sensitivity interpretation, and MP10-to-MP11 overhaul
planning.

Planning-only figures should be treated as qualitative or approximate context
unless a later task provides stronger independent validation. No recovered
figure table should be copied into a model-input bundle without a new
maintainer review and explicit promotion to ``accepted_for_model_input``.

