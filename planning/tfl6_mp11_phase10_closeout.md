# TFL 6 MP11 Phase 10 Closeout

## Purpose

This note closes Phase 10: MP11 AU/yield curve rebuild. Phase 10 launched the
MP11 curve-rebuild issue tree, extracted public-safe managed-yield parameter
evidence, mapped canonical AUs to MP11 curve lanes, repackaged the accepted
public VDYP natural-curve diagnostics, and recorded managed-curve generation
blockers.

Phase 10 did not produce accepted replacement model-input curves. Natural
curves remain Phase 5 public VDYP comparison candidates, and MP11 managed
curves remain blocked until Tables 54, 55, and 57 have reviewed per-AU TIPSY
row parsers.

## Branch And Issue Tree

- Branch: `feature/p10-mp11-au-yield-curve-rebuild`
- Pull request: pending at initial closeout
- Parent issue: `#67`
- Child issues:
  - P10.1 launch MP11 AU/yield rebuild execution plan: `#79`;
  - P10.2 extract MP11 managed-yield parameter library: `#80`;
  - P10.3 refresh MP11 AU and curve-lane crosswalk: `#81`;
  - P10.4 regenerate MP11 natural curve diagnostics: `#82`;
  - P10.5 generate MP11 managed curve diagnostics: `#83`;
  - P10.6 close Phase 10 and hand off curve artifacts: `#84`.

## Tracked Outputs

| Output | Path | Role |
| --- | --- | --- |
| Execution plan | `planning/tfl6_mp11_phase10_execution_plan.md` | Phase 10 issue tree, artifact layout, parameter gates, curve-lane gates, and no-fabrication rules. |
| Managed-yield parameter generator | `scripts/build_p10_mp11_managed_yield_parameter_library.py` | Extracts compact public-safe MP11 parameter evidence from Tables 54-60. |
| Managed-yield parameter library | `planning/tfl6_mp11_managed_yield_parameter_library.md` | Records `48` parameter rows with matching CSV/JSON. |
| AU/curve-lane generator | `scripts/build_p10_mp11_au_curve_lane_crosswalk.py` | Maps canonical AUs to natural, early managed, recent managed, and future managed lanes. |
| AU/curve-lane crosswalk | `planning/tfl6_mp11_au_curve_lane_crosswalk.md` | Records `1,536` AU/lane rows with matching CSV/JSON. |
| Natural-curve diagnostic generator | `scripts/build_p10_mp11_natural_curve_diagnostics.py` | Repackages Phase 5 public VDYP natural-curve evidence for MP11 review. |
| Natural-curve diagnostics | `planning/tfl6_mp11_natural_curve_diagnostics.md` | Records `384` AU rows, including `77` selected curve families and `307` remaps. |
| Managed-curve diagnostic generator | `scripts/build_p10_mp11_managed_curve_diagnostics.py` | Joins MP11 managed-lane gates to Phase 5 managed-curve comparison diagnostics. |
| Managed-curve diagnostics | `planning/tfl6_mp11_managed_curve_diagnostics.md` | Records `1,152` managed AU/lane rows, all blocked pending parser review. |

## Headline Findings

- The stable FEMIC canonical AU universe remains `384` AUs.
- The selected top-area natural curve family set remains `77` AUs, with `307`
  non-selected AU bins remapped to selected curve families.
- P10.2 normalized `48` public-safe MP11 parameter rows from Tables 54-60.
- P10.3 mapped all canonical AUs to four curve lanes: natural unmanaged, early
  managed, recent managed, and future managed.
- P10.5 found `231` selected managed lane rows with Phase 5 comparison curves,
  but `0` MP11 managed curves were generated.
- MP11 managed curve generation remains blocked because Tables 54, 55, and 57
  are large, multi-page, line-wrapped TIPSY tables that require reviewed
  per-AU row parsers before BatchTIPSY handoff.

## Phase 11 Handoff

Phase 11 may use the Phase 10 artifacts as review inputs, but it must not treat
them as accepted model-input curves without explicit promotion.

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
