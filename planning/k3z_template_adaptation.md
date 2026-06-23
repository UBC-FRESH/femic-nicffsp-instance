# K3Z Template Adaptation Notes

## Template Reference

Use `external/femic-k3z-instance` in the parent FEMIC checkout as the style and
structure reference for this teaching instance.

Carry forward:

- standalone instance repository layout;
- Patchworks-first teaching package shape;
- rebuild-spec discipline;
- data-package style documentation expectations; and
- student-facing assumptions registry and edit-policy style.

Do not blindly carry forward:

- K3Z tenure boundary;
- K3Z-only variant/subvariant teaching setup;
- K3Z-specific old-growth, seral, product, or treatment thresholds; or
- any generated model-input bundle or Patchworks track artifact.

## NICF FSP Teaching Mission

The first accepted model should support one shared student mission rather than
theme-specific group variants. The mission should expose two linked decision
surfaces:

- cedar: Cw cultural-reserve pressure versus high-value utility-pole production;
- expansion: candidate unallocated areas that can plausibly support an
  approximate 8,000 m3/year AAC uplift.

## First Adaptation Questions

1. What is the authoritative AOI boundary after inspecting the FSP amendment
   spatial payload?
2. Which three Landscape Units are referenced by the FSP, and are they fully or
   partially inside the AOI?
3. Which K3Z assumptions remain pedagogically useful at the larger FSP scale?
4. Which Patchworks products/accounts are needed for cedar cultural and
   utility-pole reporting?
5. What source layer can identify unallocated expansion candidates, and what
   constraints bound the candidate pool?

## P1.3a Template Comparison

Comparison date: 2026-06-23

Reference surfaces inspected:

- K3Z run profile: `external/femic-k3z-instance/config/run_profile.k3z.yaml`
- K3Z rebuild spec: `external/femic-k3z-instance/config/rebuild.spec.yaml`
- K3Z TIPSY rules: `external/femic-k3z-instance/config/tipsy/tsak3z.yaml`
- K3Z seral and silviculture surfaces:
  `external/femic-k3z-instance/config/seral.k3z.yaml` and
  `external/femic-k3z-instance/config/silviculture.k3z.*.yaml`
- K3Z model-input bundle:
  `external/femic-k3z-instance/data/model_input_bundle/`
- K3Z Patchworks package:
  `external/femic-k3z-instance/models/k3z_patchworks_model/`
- NICF current scaffold:
  `config/run_profile.nicffsp.yaml`, `config/rebuild.spec.yaml`,
  `config/tipsy/nicffsp.yaml`, `config/silviculture.nicffsp.yaml`, and
  `config/patchworks.runtime.windows.yaml`

Observed K3Z template state:

- `run_profile.k3z.yaml` uses a custom boundary path
  `data/bc/cfa/k3z/CFA K3Z Tenure.shp`, `boundary_code: k3z`, subzone
  stratification, `vdyp_sampling_mode: all`, two-pass VDYP rebinning, and
  `managed_curve_mode: tipsy`.
- K3Z carries a complete compiled model-input bundle:
  `au_table.csv` has `27` rows, `curve_table.csv` has `451` rows, and
  `curve_points_table.csv` has `8976` rows.
- K3Z carries a full Patchworks teaching package under
  `models/k3z_patchworks_model/`, including `analysis`, `blocks`, `metadata`,
  `yield`, base `tracks`, and treatment/scenario track variants.
- K3Z config has a large variant family: base, CT/fertilization, intensive,
  PCT, overlay, runtime, and variant YAML files.
- K3Z TIPSY rules are FSP-informed for North Island Community Forest context,
  but they are still K3Z/teaching-rule specific and rely on K3Z AU and stratum
  identities.

Observed NICF bootstrap state:

- `run_profile.nicffsp.yaml` now uses the accepted FSP AOI boundary path
  `data/source/nicf_fsp/aoi/nicf_fsp_aoi.shp` and records LU reference context
  at `data/source/nicf_fsp/lu_reference/nicf_lu_reference.shp`.
- NICF does not yet have a compiled `data/model_input_bundle/`.
- NICF does not yet have a `models/` Patchworks package.
- `config/tipsy/nicffsp.yaml` is still a bootstrap placeholder and contains a
  generic softwood rule that is not accepted for the North Island FSP boundary.
- `config/silviculture.nicffsp.yaml` is still a scaffold, not an accepted
  treatment or cedar-signal contract.
- `config/patchworks.runtime.windows.yaml` is still a placeholder copied from
  the K3Z shape and currently points at K3Z output/model paths; it must not be
  treated as runnable NICF runtime configuration until P1.4 opens the runtime
  package build/QA lane.

Adaptation boundary from this comparison:

- Carry forward the K3Z repository shape, rebuild-spec discipline, run-profile
  boundary-mode pattern, model-input bundle table contract, Patchworks package
  directory pattern, and issue/roadmap/changelog workflow.
- Do not carry forward K3Z generated bundle tables, Patchworks tracks, scenario
  variants, treatment YAMLs, seral assumptions, TIPSY AU rules, product/account
  targets, or Patchworks runtime paths as accepted NICF semantics.
- Treat the NICF accepted source boundary as decision-complete for starting
  model-input design: AOI is FDU 1 Holberg, FDU 2 Keogh, and FDU 3 Marble; LU
  reference context is the matching Holberg/Keogh/Marble BCGW subset.
- Treat cedar-signal design, expansion candidate-area construction, and
  Patchworks runtime packaging as separate follow-on task lanes under P1.4, not
  as part of the K3Z template comparison.

Immediate next P1.3 work:

- Define the first NICF run-profile boundary beyond source paths: which K3Z
  stratification, VDYP sampling, two-pass rebinning, and managed-curve settings
  are acceptable defaults for the FSP AOI.
- Separate K3Z assumptions into explicit carry-forward versus FRST 558 review
  lists before any model-input bundle generation starts.

## P1.3b First NICF Run-Profile Boundary

Decision date: 2026-06-23

Accepted first-boundary settings in `config/run_profile.nicffsp.yaml`:

| Field | Accepted value | Rationale |
| --- | --- | --- |
| `selection.boundary_path` | `data/source/nicf_fsp/aoi/nicf_fsp_aoi.shp` | Accepted FDU 1-3 FSP AOI from P1.2. |
| `selection.boundary_code` | `nicffsp` | Case code for the custom-boundary lane. |
| `selection.stratification.bec_grouping` | `subzone` | Carries forward the K3Z teaching-template structure and keeps the first AU design inspectable. |
| `selection.stratification.species_combo_count` | `2` | Carries forward the K3Z two-species teaching simplification for the first bundle. |
| `selection.stratification.include_tm_species2_for_single` | `true` | Carries forward K3Z's fallback species-pairing behavior for sparse/single-species records. |
| `selection.stratification.top_area_coverage` | `0.90` | Carries forward K3Z's compact-strata teaching boundary. |
| `modes.resume` | `false` | First NICF compile should build from a clean boundary rather than resuming stale bootstrap artifacts. |
| `modes.vdyp_sampling_mode` | `all` | First accepted source-derived baseline should be complete; performance tuning can follow after evidence exists. |
| `modes.vdyp_two_pass_rebin` | `true` | Carries forward K3Z's more stable low-count strata handling. |
| `modes.vdyp_min_stands_per_si_bin` | `10` | Carries forward K3Z's teaching-scale minimum until NICF area/strata diagnostics justify a change. |
| `modes.managed_curve_mode` | `tipsy` | Keeps the K3Z teaching-model contract that managed-origin curves use BatchTIPSY-style synthesis. |

Boundary interpretation:

- These settings accept K3Z's run-profile mechanics as the first NICF compile
  boundary.
- These settings do not accept K3Z AU identities, generated bundle tables,
  TIPSY rule content, silviculture treatments, seral thresholds, products,
  accounts, or Patchworks runtime paths as NICF semantics.
- `config/tipsy/nicffsp.yaml` remains provisional; the `managed_curve_mode:
  tipsy` decision means the first bundle will need NICF-reviewed TIPSY rules
  before managed-curve outputs are treated as accepted teaching evidence.
- The first bundle should still be blocked until P1.3c separates
  carry-forward assumptions from FRST 558 review-required assumptions.

Validation performed:

- `load_pipeline_run_profile()` parsed the accepted boundary defaults from
  `config/run_profile.nicffsp.yaml`.

Immediate next P1.3 work:

- Complete the carry-forward versus FRST 558 review-required assumption list.
- Identify the minimum source-derived model-input surfaces needed before P1.4
  runtime-package issue bodies can be finalized.

## P1.3c Carry-Forward and Review Assumptions

Decision date: 2026-06-23

Accepted carry-forward assumptions:

| Surface | Carry-forward assumption | Boundary |
| --- | --- | --- |
| Instance workflow | Use the K3Z standalone instance shape: repo-local `config/`, `data/`, `models/`, `planning/`, `runbooks/`, roadmap, changelog, and issue trail. | Structural only; filenames and case IDs must be NICF-specific and lowercase where FEMIC controls paths. |
| Run profile | Use custom-boundary mode with `selection.boundary_path`, `selection.boundary_code`, and explicit stratification/mode defaults. | Source boundary is NICF FSP FDU 1-3, not K3Z tenure. |
| Stratification | Start with K3Z-style subzone plus two leading species combinations and 90 percent top-area coverage. | Accepted as first compile boundary only; revise after NICF AU/strata diagnostics exist. |
| VDYP handling | Start with complete VDYP sampling, two-pass rebinning, and minimum 10 stands per SI bin. | Performance tuning and alternate thresholds wait for first NICF diagnostics. |
| Managed curve lane | Use the K3Z teaching convention that managed-origin curves are BatchTIPSY-style, with `managed_curve_mode: tipsy`. | TIPSY rule content is not carried forward; NICF rules need review before accepted outputs. |
| Model-input bundle contract | Preserve the K3Z bundle table shape: AU table, curve table, and curve-points table as the pre-Patchworks handoff. | Bundle contents must be regenerated from NICF source data. |
| Patchworks package shape | Preserve the K3Z directory/package concept: analysis scripts, blocks, metadata, yield surface, tracks, accounts, products, treatments, and runtime QA. | Package implementation is deferred to P1.4 runtime-package issue work. |
| Documentation/control surfaces | Preserve K3Z-style assumptions registry, operator/runbook, rebuild spec, validation narrative, and append-only changelog behavior. | NICF documents must identify provisional versus accepted teaching assumptions. |

FRST 558 review-required assumptions:

| Surface | Review question | Why review is required before implementation |
| --- | --- | --- |
| TIPSY managed rules | Which species mixes, densities, utilization DBH, regeneration delays, OAFs, and site-index fallbacks represent managed-origin NICF stands? | K3Z `tsak3z.yaml` rules are AU/stratum-specific and not valid for the larger FSP AOI. |
| Cedar cultural reserve signal | How should Cw cultural-reserve pressure be represented as area, eligibility, account, target, constraint, or scenario signal? | This is one of the core teaching questions and cannot be inferred from K3Z. |
| Utility-pole production signal | Which cedar product/account definitions and utilization assumptions distinguish high-value utility-pole potential from generic harvested volume? | K3Z product/account targets do not encode the requested NICF value signal. |
| Expansion candidate pool | Which source layers define unallocated candidate areas, tenure status, exclusions, productivity screening, and the AAC-uplift envelope? | The uploaded FSP AOI/LU files do not by themselves identify expansion eligibility. |
| Seral/old-growth objectives | Which LU/FDU-level seral or old-growth objectives apply to Holberg, Keogh, and Marble for the teaching model? | K3Z thresholds are local teaching assumptions and the FSP/LU context must be reviewed. |
| Treatment portfolio | Which base, cedar, thinning, fertilization, or intensive-management treatments should students be allowed to schedule? | K3Z variant families are examples, not accepted NICF treatments. |
| Managed/unmanaged and origin assignment | How should Patchworks treatment eligibility and curve provenance be assigned across the FSP AOI? | FEMIC semantics require managed/unmanaged and natural/treated origin to remain distinct. |
| Account and reporting package | Which accounts, products, targets, and summary reports are required for FRST 558 decision review? | K3Z reports are teaching examples and do not cover the new cedar/expansion mission. |
| Baseline acceptance metrics | What minimum area, volume, account, and sanity checks make a first NICF bundle acceptable? | K3Z invariants use K3Z scale and cannot be reused numerically. |

Rejected carry-forward assumptions for Phase 1:

| Surface | Rejected assumption |
| --- | --- |
| K3Z boundary | Do not reuse the K3Z tenure boundary or its AOI semantics. |
| K3Z generated bundle | Do not copy `data/model_input_bundle/*` into NICF. |
| K3Z Patchworks tracks | Do not copy K3Z `tracks*`, `blocks`, `analysis`, or validated output artifacts as NICF runtime evidence. |
| K3Z treatment variants | Do not treat K3Z CT/fertilization, intensive, PCT, or overlay variants as accepted NICF scenarios. |
| K3Z TIPSY rules | Do not treat K3Z AU IDs, species-pair rules, or fallback pathways as accepted NICF managed-curve assumptions. |
| K3Z product/account targets | Do not reuse K3Z product/account expectations as NICF cedar or expansion reporting semantics. |
| K3Z runtime paths | Do not treat K3Z-shaped paths in `config/patchworks.runtime.windows.yaml` as runnable NICF runtime configuration. |

Implementation gate:

- Model-input bundle generation must not start until the review-required
  TIPSY/managed-curve and baseline acceptance assumptions are either accepted
  or explicitly bracketed as provisional.
- P1.4 issue bodies must carry the review-required cedar-signal,
  expansion-candidate, and runtime-package terms into separate follow-on lanes.
