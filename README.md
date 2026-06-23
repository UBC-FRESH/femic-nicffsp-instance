# femic-nicffsp-instance

Standalone FEMIC teaching instance for the FRST 558 North Island Community
Forest / Forest Stewardship Plan case.

## Purpose

This repository will host the Patchworks model package and rebuild workflow for
the expanded NICF / TFL 6 student case. The case starts from the existing K3Z
teaching model style, but the active target area of interest has pivoted to
Tree Farm Licence 6.

The teaching mission is being designed around two active management questions:

- cedar allocation and value: represent cedar cultural-reserve and utility-pole
  production signals clearly enough for student scenario design; and
- K3Z expansion: provide a bounded pool of candidate unallocated areas from
  which student groups can recommend an expansion package that supports an
  approximate 8,000 m3/year AAC increase.

## Current Status

This is a bootstrap snapshot. It contains source payload inventory, FEMIC
instance scaffolding, and the first TFL 6 boundary artifact. It is not yet a
compiled or runnable Patchworks model package. The original FDU 1/2/3 boundary
is retained as provenance, but TFL 6 is the active target AOI for the next input
layer build.

## Source Payloads

Initial source files are tracked under `data/source/nicf_fsp/`:

- `nicf_fsp_amendment_3_spatial.zip`
- `bcgw_lu_clip_2026_06.zip`
- `nicf_forest_stewardship_plan_2020.pdf`

See `planning/source_inventory.md` for original filenames, hashes, and the
first interpretation boundary.

Pre-pivot extracted source paths retained as provenance:

- FDU 1/2/3 bootstrap boundary: `data/source/nicf_fsp/aoi/nicf_fsp_aoi.shp`
- LU reference context:
  `data/source/nicf_fsp/lu_reference/nicf_lu_reference.shp`

Active TFL 6 boundary:

- `data/source/tfl_6/aoi/tfl_6_boundary.gpkg`
- layer: `tfl_6_boundary`

## Workflow

This repository uses the same control-surface pattern as recent FRESH agent-led
projects:

- `AGENTS.md` is the working contract for coding agents.
- `ROADMAP.md` is the active plan and next-step tracker.
- `CHANGE_LOG.md` is the append-only project narrative.
- `planning/` contains focused design and provenance notes.
- GitHub Issues carry active workflow state and should be kept synchronized with
  roadmap and changelog entries.

## FEMIC Rebuild Entry Points

The initial scaffold is present but not yet accepted as runnable:

```bash
femic instance validate-spec --spec config/rebuild.spec.yaml
```

Case preflight now points at the TFL 6 boundary but remains a bootstrap
source-path check until the TFL 6-clipped input layers are materialized under
Phase 1. Full rebuild commands should wait until the TFL 6 input-layer and
model-design contracts are accepted.
