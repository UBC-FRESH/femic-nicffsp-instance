# TFL 6 MP11 Phase 10 Readiness And Blocker Review Closeout

## Purpose

This note closes Phase 10: MP11 AU/yield readiness and curve-rebuild scoping.
Phase 10 extracted public-safe managed-yield parameter evidence, mapped
canonical AUs to MP11 curve lanes, repackaged the accepted public VDYP
natural-curve diagnostics, and recorded managed-curve generation blockers.

Phase 10 did **not** rebuild all AUs/yield curves, did **not** regenerate
managed curves, and did **not** update curve plots. Natural curves remain Phase
5 public VDYP comparison candidates, and MP11 managed curves remain blocked
until Tables 54, 55, and 57 have reviewed per-AU TIPSY row parsers.

The actual curve rebuild is Phase 10R (`#92`).

## Branch And Issue Tree

- Branch: `feature/p10-mp11-au-yield-curve-rebuild`
- Pull request: `#85`
- Parent issue: `#67`
- Child issues:
  - P10.1 launch MP11 AU/yield readiness execution plan: `#79`;
  - P10.2 extract MP11 managed-yield parameter library: `#80`;
  - P10.3 refresh MP11 AU and curve-lane crosswalk: `#81`;
  - P10.4 repackage MP11 natural curve diagnostics: `#82`;
  - P10.5 record MP11 managed curve blocker diagnostics: `#83`;
  - P10.6 close Phase 10 and hand off curve-readiness artifacts: `#84`.

## Tracked Outputs

| Output | Path | Role |
| --- | --- | --- |
| Execution plan | `planning/tfl6_mp11_phase10_execution_plan.md` | Phase 10 issue tree, artifact layout, parameter gates, curve-lane gates, and no-fabrication rules. |
| Managed-yield parameter generator | `scripts/build_p10_mp11_managed_yield_parameter_library.py` | Extracts compact public-safe MP11 parameter evidence from Tables 54-60. |
| Managed-yield parameter library | `planning/tfl6_mp11_managed_yield_parameter_library.md` | Records `48` parameter rows with matching CSV/JSON. |
| AU/curve-lane generator | `scripts/build_p10_mp11_au_curve_lane_crosswalk.py` | Maps canonical AUs to natural, early managed, recent managed, and future managed lanes. |
| AU/curve-lane crosswalk | `planning/tfl6_mp11_au_curve_lane_crosswalk.md` | Records `1,536` AU/lane rows with matching CSV/JSON. |
| Natural-curve diagnostic generator | `scripts/build_p10_mp11_natural_curve_diagnostics.py` | Repackages Phase 5 public VDYP natural-curve evidence for MP11 review. |
| Natural-curve diagnostics | `planning/tfl6_mp11_natural_curve_diagnostics.md` | Records `77` canonical top-N AU curve families plus source-bin remap provenance. |
| Managed-curve diagnostic generator | `scripts/build_p10_mp11_managed_curve_diagnostics.py` | Joins MP11 managed-lane gates to Phase 5 managed-curve comparison diagnostics. |
| Managed-curve diagnostics | `planning/tfl6_mp11_managed_curve_diagnostics.md` | Records `1,152` managed AU/lane rows, all blocked pending parser review. |

## What Was Not Done

Phase 10 did not:

- rebuild AU/yield curves;
- run BatchTIPSY/TIPSY for MP11 managed rows;
- parse MP11 Tables 54, 55, and 57 into reviewed per-AU curve-generation
  inputs;
- regenerate natural curve plots;
- regenerate managed curve plots;
- update the curve plot library; or
- promote any curve artifact to `accepted_model_input`.

Those tasks are assigned to Phase 10R.

## Headline Findings

- The stable FEMIC canonical AU universe is the `77` top-N L/M/H AU set.
- The selected top-area natural curve family set remains `77` AUs, with `307`
  non-AU source stratum bins remapped to selected curve families.
- P10.2 normalized `48` public-safe MP11 parameter rows from Tables 54-60.
- P10.3 mapped all canonical AUs to four curve lanes: natural unmanaged, early
  managed, recent managed, and future managed.
- P10.5 found `231` selected managed lane rows with Phase 5 comparison curves,
  but `0` MP11 managed curves were generated.
- MP11 managed curve generation remains blocked because Tables 54, 55, and 57
  are large, multi-page, line-wrapped TIPSY tables that require reviewed
  per-AU row parsers before BatchTIPSY handoff.

## Actual Curve-Rebuild Reference

The actual curve rebuild is now tracked as Phase 10R: MP11 curve parser and
curve rebuild (`#92`).

- P10R.1 launch MP11 curve-rebuild execution plan: `#93`;
- P10R.2 parse MP11 Tables 54, 55, and 57 per-AU TIPSY rows: `#94`;
- P10R.3 QA managed-yield rows and build BatchTIPSY handoff inputs: `#95`;
- P10R.4 run and parse MP11 managed curve generation: `#96`;
- P10R.5 regenerate natural and managed curve plots and overlays: `#97`;
- P10R.6 close curve-rebuild phase and hand off accepted curve candidates:
  `#98`.

Phase 11 is blocked until Phase 10R closes with accepted curve candidates or a
maintainer-approved blocker path.

## Phase 10R And Phase 11 Handoff

Phase 10R may use Phase 10 artifacts as review inputs, but it must not treat
them as rebuilt curves. Phase 11 must not treat them as accepted model-input
curves without explicit promotion after Phase 10R closeout.

Ready as comparison or review evidence:

- `planning/tfl6_mp11_managed_yield_parameter_library.*`;
- `planning/tfl6_mp11_au_curve_lane_crosswalk.*`;
- `planning/tfl6_mp11_natural_curve_diagnostics.*`;
- `planning/tfl6_mp11_managed_curve_diagnostics.*`.

Blocked before model-input/XML promotion:

- MP11 per-AU managed TIPSY rows from Tables 54, 55, and 57 need reviewed
  parsers, QA diagnostics, and BatchTIPSY handoff surfaces.
- VRAF rows from Table 58 are harvest-time yield-impact parameters, not base
  curve edits.
- LEFI/ITI/LiDAR productivity assumptions remain unavailable or sensitivity
  evidence unless public-safe inputs are supplied and reviewed.
- No Phase 10 row is `accepted_model_input`.

The Phase 5 teaching runtime remains the accepted baseline.

## Validation

Phase 10 closeout validation:

```bash
python scripts/build_p10_mp11_managed_yield_parameter_library.py
python scripts/build_p10_mp11_au_curve_lane_crosswalk.py
python scripts/build_p10_mp11_natural_curve_diagnostics.py
python scripts/build_p10_mp11_managed_curve_diagnostics.py
python -m ruff check .
sphinx-build -b html docs docs/_build/html -W
```

All commands passed before closeout.

## Private-Data Hygiene

Phase 10 used public MP11 text/table evidence, public FEMIC source surfaces,
and existing public-safe Phase 5 curve diagnostics only. It did not track
private WFP curves, unpublished parameter tables, proprietary LEFI/ITI/LiDAR
attributes, private prompt logs, model-input bundles, ForestModel XML, Matrix
Builder outputs, Patchworks runtime artifacts, or generated scratch outputs
outside accepted paths.
