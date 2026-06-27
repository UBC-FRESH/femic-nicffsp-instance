Phase 5 Scenario Teaching Workflows
===================================

This page turns the first TFL 6 runtime package into a classroom workflow. It
assumes students have already materialized the archive and opened the
Patchworks package described in :doc:`phase5-runtime-quickstart`.

The goal is not to identify one correct scenario. The teaching goal is to make
tradeoffs visible across stakeholder-style perspectives.

Starting Point
--------------

The first teaching runtime package is a base TFL 6 model with:

- AFLB as the stand universe;
- THLB as the managed treatment-eligible subset;
- NTHLB retained in the model as unmanaged forest with untreated growth;
- generic ``CC`` as the first clearcut-and-plant treatment lane;
- embedded K3Z/NICF and expansion identity fields carried for reporting; and
- cedar signals available for reporting and scenario interpretation.

Students should start by launching:

.. code-block:: text

   models/tfl6_patchworks_model/analysis/base.pin

The Phase 4 scenario smoke used this representative harvest target:

.. code-block:: text

   product.HarvestedVolume.managed.Total.CC

First Accounts And Outputs To Inspect
-------------------------------------

Before changing a scenario, inspect the baseline signals that confirm the
runtime package is behaving as expected.

.. list-table::
   :header-rows: 1

   * - Output Surface
     - Teaching Use
   * - ``feature.Area.managed``
     - Managed THLB area available for scheduled treatment.
   * - ``feature.Area.unmanaged``
     - Retained AFLB / NTHLB area kept in the model but excluded from scheduled
       treatment.
   * - ``feature.Yield.managed.Total``
     - Growth signal for the managed portion of the AFLB universe.
   * - ``feature.Yield.unmanaged.Total``
     - Growth signal for retained forest area.
   * - ``product.HarvestedVolume.managed.Total.CC``
     - Main first-release harvest-volume product for the generic clearcut lane.
   * - ``flow.even.product.HarvestedVolume.managed.Total.CC``
     - Even-flow helper target used in the Phase 4 smoke run.
   * - ``product.Treated.managed.CC``
     - Area or treatment signal for scheduled generic clearcut activity.

If students use the saved Phase 4 smoke outputs for orientation, the relevant
directory in the development repository is:

.. code-block:: text

   models/tfl6_patchworks_model/analysis/p44d_harvest_smoke200/

Those saved-stage outputs are useful evidence, but they are not canonical
release inputs. New teaching results should be generated from the published
runtime package.

Stakeholder-Style KPI Families
------------------------------

The instance should be interpreted through several KPI families. These are
proxies for values different groups may care about; they are not claims that
every stakeholder values every metric equally.

.. list-table::
   :header-rows: 1

   * - Perspective
     - Useful Proxy KPIs
   * - WFP / TFL 6 fibre supply
     - Harvest flow, managed growing stock, scheduled ``CC`` area, long-run
       fibre stability, and whole-TFL impacts of constraints.
   * - WFP delivered-cost pressure
     - Operability or harvest-system proxy fields when available, future
       ground/cable/heli splits, and any scenario that shifts harvest into
       harder or more expensive stands.
   * - NICF / K3Z continuity
     - K3Z reference identity, accepted expansion candidate area, expansion
       scenario uplift, and differences between NICF groups and the TFL 6
       remainder.
   * - Cedar stewardship
     - Cedar-leading area, cedar-present area, old-cedar proxy area, cedar
       harvest candidate area, and cedar retained in unmanaged or reserve-like
       contexts.
   * - Retention / ecosystem proxy
     - Unmanaged area, NTHLB share, old-growth or BEC-stratum area accounts,
       strategic RMZ fallback effects, and changes to retained growth signal.
   * - Teaching-model transparency
     - Difference between base-case results and sensitivity results, plus clear
       separation of accepted model logic from student-proposed extensions.

Starter Exercises
-----------------

Exercise 1: Read The Baseline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Open the runtime package and inspect the managed and unmanaged area/yield
surfaces. Students should explain why unmanaged forest remains in the model and
why it still needs a growth curve.

Expected discussion points:

- AFLB is broader than THLB.
- NTHLB is not deleted from the model.
- Patchworks ``managed`` and ``unmanaged`` are treatment-eligibility states,
  not curve-origin labels.

Exercise 2: Generic Clearcut Flow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use ``product.HarvestedVolume.managed.Total.CC`` as the first harvest-flow
signal. Ask students to compare even-flow pressure against inventory outcomes.

Expected discussion points:

- the first release uses generic ``CC`` rather than ground/cable/heli-specific
  treatments;
- a flat harvest target can hide shifts in stand type, age, cedar content, or
  future operability; and
- successful flow does not mean every stakeholder objective is satisfied.

Exercise 3: Managed Versus Retained Forest
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Compare ``feature.Area.managed``, ``feature.Area.unmanaged``,
``feature.Yield.managed.Total``, and ``feature.Yield.unmanaged.Total``.

Expected discussion points:

- retained forest still contributes to non-harvest inventory metrics;
- unmanaged forest can matter for biodiversity, old-forest, cedar, and visual
  scenario interpretation; and
- changing THLB rules changes both managed opportunity and retained geography.

Exercise 4: Cedar Signals
~~~~~~~~~~~~~~~~~~~~~~~~~

Use the cedar design page and available cedar accounts to frame a scenario
question about old cedar, cedar-present stands, or cedar harvest candidates.

Expected discussion points:

- cedar should not be reduced to generic volume alone;
- cedar retained in NTHLB and cedar scheduled for harvest answer different
  questions; and
- hard cedar-reserve targets are not part of the first runtime package unless a
  class exercise adds them explicitly.

Exercise 5: NICF Expansion Framing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Review the embedded identity design before proposing expansion scenarios.
Students should distinguish current-AOI TFL 6 stands from outside-AOI proximal
or adjacent public forested land that may become NICF expansion candidates in a
future scenario.

Expected discussion points:

- expansion candidates are outside the current TFL 6 AOI;
- rejected or unreviewed expansion pools are audit/reporting surfaces, not
  automatically schedulable area; and
- NICF-preferred expansion or cedar scenarios may affect WFP-facing fibre
  supply, value proxies, or delivered-cost pressure.

Advanced Project Prompts
------------------------

The following prompts are suitable for longer student projects:

- Replace the strategic RMZ aspatial fallback with credible geometry, rerun the
  affected netdown step, rebuild the runtime package, and compare scenario
  outcomes.
- Develop a reviewed slope/DEM and inventory-based harvest-system classifier
  that separates ground, cable, and heli opportunities, then compare delivered
  cost proxy changes.
- Add a cedar stewardship target and test how harvest flow, old-cedar
  retention, and WFP-facing fibre-supply proxies respond.
- Screen outside-AOI public forested land for NICF expansion candidates, keep
  accepted/rejected/unreviewed pools separate, and compare expansion scenarios
  against the base TFL 6-only model.
- Revisit VDYP smoothing or TIPSY parameter crosswalk assumptions for a small
  set of influential AUs and test whether the scenario ranking changes.

Scenario Reporting Rules
------------------------

Student reports should make these boundaries explicit:

- identify whether results came from the published runtime package or a rebuilt
  model;
- report the scenario target, major constraints, and any new assumptions;
- keep TFL 6 whole-area, WFP remainder, K3Z/NICF reference, and expansion
  candidate results separate where those groups are available;
- distinguish managed THLB activity from retained NTHLB growth;
- state when a KPI is a proxy rather than an observed economic, cultural, or
  ecological value; and
- disclose whether harvest-system, cedar, RMZ, or expansion logic is base-case,
  deferred, or student-proposed.

First-Release Limits
--------------------

The first teaching package is intentionally simple in several places:

- generic ``CC`` is the only active base treatment lane;
- ground/cable/heli harvest-system assignment remains deferred;
- CT and fertilization hooks are limited to K3Z/NICF core or accepted expansion
  groups once those groups are explicitly activated;
- outside-AOI NICF expansion geometry is not part of the current TFL 6 base
  AOI; and
- saved-stage smoke output is evidence, not the source of truth for new
  scenario results.
