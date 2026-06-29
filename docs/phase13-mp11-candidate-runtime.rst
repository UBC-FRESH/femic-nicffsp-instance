Phase 13 MP11 Candidate Runtime
================================

Phase 13 documents how the MP11 candidate runtime should be interpreted after
the Phase 12 Matrix Builder, direct-launch, and scenario-smoke checks. The
candidate runtime is useful teaching and comparison evidence. It is not yet the
accepted release baseline, and it is not a claim that FEMIC has reproduced
Western Forest Products' unpublished internal model.

Status Boundary
---------------

The completed Phase 5 runtime remains the accepted teaching/runtime baseline.
The MP11 runtime is a smoke-tested candidate built from public data, reviewed
MP11 extraction work, and the Phase 5 Patchworks scaffold. It should be used as
an MP11 comparison and teaching surface while Phase 13 finishes archive QA and
the release-status decision.

The recommended wording is:

   The MP11 candidate runtime is a plausible public-data reconstruction of the
   MP11 model structure and produces harvest-flow behavior in the same broad
   range as the MP11 base-case evidence. It remains a candidate model until
   Phase 13 comparison documentation, release QA, archive materialization, and
   baseline replacement or supplement decisions pass.

Avoid stronger claims. In particular, do not describe the candidate as a
replica of WFP's model, as an approved AAC result, or as a Phase 5 replacement
until the remaining Phase 13 gates have passed.

Comparison Evidence
-------------------

Phase 13 separates four evidence classes:

.. list-table::
   :header-rows: 1

   * - Evidence
     - Current use
     - Main caveat
   * - MP11 base-case text and Figure 2 context
     - Comparison target.
     - Published evidence only; not a model input.
   * - Reviewed MP11 figure recovery
     - Comparison planning and classroom interpretation.
     - Approximate figure-derived values remain review evidence.
   * - Tracked Phase 12 runtime smoke outputs
     - Proof that the candidate runtime builds, launches, schedules, and writes
       Patchworks outputs.
     - The smoke run used a high harvested-volume target and is not the same
       basic interactive scenario reviewed by the maintainer.
   * - Maintainer interactive Patchworks context
     - Practical interpretation of the candidate model's behavior.
     - Screenshot/context evidence only until exported through a reproducible
       scenario table.

The tracked scenario comparison tables are:

- ``planning/tfl6_mp11_phase13_scenario_comparison.md``;
- ``planning/tfl6_mp11_phase13_scenario_comparison.csv``;
- ``planning/tfl6_mp11_phase13_scenario_comparison.json``; and
- ``planning/tfl6_mp11_phase13_scenario_period_comparison.csv``.

Those tables record the MP11 base-case level as ``1,061,600 m3/year``, the MP11
adjusted LRSY context as ``1,182,900 m3/year``, and the maintainer interactive
candidate context as approximately ``1,150,000 m3/year``. The candidate context
is about ``8.33%`` above the MP11 base-case anchor. That is plausible because
the public-data candidate does not yet include every WFP constraint and its
Phase 9RF THLB scaffold is slightly larger than the MP11 declared THLB.

Why The Candidate Can Be Higher
-------------------------------

A candidate result that is somewhat above WFP's MP11 base case does not, by
itself, mean the model is off-track. The current public-data reconstruction has
two important differences from WFP's internal analysis:

- the accepted P9RF current THLB is ``122,763.421 ha`` versus the MP11 declared
  ``120,099 ha``; and
- several WFP or sensitive constraints are unavailable or deliberately excluded
  from the public teaching instance.

The P9RF THLB difference is about ``2.2%``. Some unavailable or deferred
constraints could also reduce harvest in WFP's full base case. The Phase 13
interpretation is therefore that the candidate model is plausibly in the same
model family, but still caveated.

KPI And Caveat Report
---------------------

The KPI/caveat report is the main release-decision surface:

- ``planning/tfl6_mp11_phase13_kpi_caveat_report.md``;
- ``planning/tfl6_mp11_phase13_kpi_caveat_report.csv``; and
- ``planning/tfl6_mp11_phase13_kpi_caveat_report.json``.

It records ``42`` comparison rows covering harvest flow, land base, source/THLB
constraints, selected sensitivities, runtime-build evidence, and reviewed
figure evidence. The report keeps non-blocking caveats separate from release
caveats and explicitly labels rows that still need archive/materialization QA
or reproducible base-scenario export.

High-signal caveats for students and maintainers are:

- the maintainer's approximate ``1.15 million m3/year`` scenario context needs
  a reproducible export before it becomes release QA evidence;
- the P12.5 tracked scenario smoke proves runtime behavior, not a calibrated
  MP11 base case;
- karst, big-tree reserves, sensitive cultural or archaeological features,
  some research-site information, and private WFP operability inputs remain
  unresolved or intentionally excluded;
- harvest-system assignment, minimum-harvest-age policy, and scenario-policy
  details are not yet accepted as final MP11 runtime equivalence; and
- archive and materialization QA are still Phase 13 work.

Teaching Workflows
------------------

The MP11 candidate runtime supports teaching exercises that compare evidence
strength, model structure, and public-data limits. Good student workflows
include:

- compare MP11 Figure 2 and the tracked Phase 13 scenario table, then explain
  why the candidate result can be above the WFP base case without being
  dismissed;
- use the Phase 9 THLB page and the P13 KPI/caveat report to classify public
  proxy, sensitive-source exclusion, private-source gap, and accepted endpoint
  rows;
- inspect the Phase 12 runtime closeout to distinguish launch smoke,
  scenario-smoke output, and release QA;
- identify which caveats would matter most before using the candidate as a
  decision-support model; and
- propose a reproducible scenario-export checklist for turning the maintainer
  interactive context into tracked evidence.

These workflows should treat the candidate as an advanced teaching surface.
They should not ask students to treat the current candidate result as an AAC
recommendation or as the published WFP model.

Maintainer Workflow
-------------------

Maintainers should use the P13 evidence in this order:

1. Read ``planning/tfl6_mp11_phase12_runtime_closeout.md`` to confirm the
   candidate runtime build and smoke-test boundary.
2. Read ``planning/tfl6_mp11_phase13_scenario_comparison.md`` to separate MP11
   base-case evidence, runtime-smoke output, and maintainer context.
3. Read ``planning/tfl6_mp11_phase13_kpi_caveat_report.md`` before making any
   release-positioning claim.
4. Complete Phase 13 archive/materialization QA before publishing or describing
   the candidate as materializable.
5. Decide in P13.5 whether the candidate ``replaces_phase5``,
   ``supplements_phase5``, or remains ``experimental_only``.

Phase 13 documentation does not rebuild model inputs, regenerate XML, rerun
Matrix Builder, or produce a release archive. Those boundaries keep the docs
lane focused on interpretation, teaching use, and release-readiness evidence.

