# TFL 6 MP11 Figrecover Corpus Summary

## Purpose

This compact public-safe summary records the P7.2 runtime corpus preparation
for the full MP11 figure-extraction test. Generated pages and runtime manifests
remain ignored under `runtime/`.

## Source

- Source URL:
  `https://www.westernforest.com/wp-content/uploads/2026/06/TFL6_MP_11_202606_w_Appendices_Web-compressed.pdf`
- Source SHA256:
  `44591c1024254e36d8989df45a2b489a624d5669c5ae01a6ebfd961b50a7321b`
- PDF page count:
  `475`
- Figure inventory:
  `planning/tfl6_mp11_full_figure_inventory.csv`
- Figure inventory rows:
  `61`

## Runtime Corpus

- Corpus ID:
  `tfl6-mp11-full-figures`
- Runtime root:
  `runtime/document_ingestion/tfl6-mp11-full-figures`
- Runtime source manifest:
  `runtime/document_ingestion/tfl6-mp11-full-figures/source_manifest.yaml`
- Runtime pages directory:
  `runtime/document_ingestion/tfl6-mp11-full-figures/pages`
- Rendered page count:
  `58`
- Unique figure PDF pages:
  `58`
- Page selection:
  `66,82-93,95,97-101,103-104,107,109-110,112,115-117,120,122-124,126,129,131-133,136,143-158,172-175`
- DPI:
  `150`
- Image format:
  `png`
- `figrecover` version:
  `0.1.0a1`
- PyMuPDF renderer version:
  `1.27.2.3`

## Commands

Run these from the instance repository with a Python environment that can import
FEMIC and `figrecover`.

Preflight:

```bash
python -m femic doc figures preflight
```

Corpus render:

```bash
python -m femic doc figures prepare-corpus tfl6-mp11-full-figures \
  --pdf <local-public-mp11-source-copy> \
  --pages 66,82-93,95,97-101,103-104,107,109-110,112,115-117,120,122-124,126,129,131-133,136,143-158,172-175 \
  --dpi 150 \
  --output-root runtime/document_ingestion/tfl6-mp11-full-figures \
  --overwrite
```

## Artifact Policy

Generated runtime pages, crops, overlays, prompt logs, raw recovered tables, and
review bundles remain ignored. Tracked Phase 7 files should stay compact and
public-safe until specific reviewed artifacts are approved.
