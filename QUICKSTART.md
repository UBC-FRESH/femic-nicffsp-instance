# NICF FSP FEMIC Instance Quickstart

1. Validate CLI install:
   `femic --help`
2. Validate the rebuild-spec scaffold:
   `femic instance validate-spec --spec config/rebuild.spec.yaml`
3. Review the pre-pivot FDU source provenance in
   `planning/source_inventory.md`.
4. Confirm `config/run_profile.nicffsp.yaml` still points at the temporary
   pre-pivot FDU boundary path. Do not switch it to the TFL 6 boundary until
   `P1.6a` materializes `data/source/tfl_6/aoi/tfl_6_boundary.gpkg`.
5. Validate geospatial runtime dependencies:
   `femic prep geospatial-preflight`
6. Validate case paths:
   `femic prep validate-case --run-config config/run_profile.nicffsp.yaml --tipsy-config-dir config/tipsy`
7. Run compile workflow from this instance root only after the roadmap accepts
   the TFL 6 boundary, input-layer, and model-design contracts.
