# TFL 6 Runtime Release Archive Manifest Contract

## Purpose

P5.2b locks the publication decision for the first TFL 6 teaching release:
publish a reviewed ready-to-launch Patchworks runtime archive and keep the
rebuild workflow documented. This contract defines the archive contents and the
manifest fields that must exist before any payload is copied to `arbutus-s3`.

This is a planning/metadata slice only. It does not build, annex, copy, or
publish the archive.

## Release Mode

Accepted release mode:

- publish rebuild instructions and source provenance in Git/Sphinx docs; and
- publish one reviewed ready-to-launch Patchworks runtime archive through the
  instance-local `arbutus-s3` git-annex special remote.

Reasoning:

- instructors and students should be able to launch the accepted Phase 4 model
  without rebuilding THLB, yield curves, XML, Matrix Builder tracks, or blocks;
- maintainers still need the source-controlled rebuild trail for audit and
  future changes; and
- putting generated runtime directories directly in Git would create avoidable
  churn and make ordinary source review noisy.

## Archive Naming

Canonical archive path:

```text
releases/tfl6_patchworks_runtime_p5_2.zip
```

Canonical manifest path:

```text
releases/tfl6_patchworks_runtime_p5_2_manifest.yaml
```

The archive and manifest are expected to be annexed files. They are not ordinary
Git source files.

## Included Paths

The archive must preserve repo-relative paths for these release inputs:

| Path | Required | Notes |
| --- | --- | --- |
| `output/patchworks_tfl6_validated/forestmodel.xml` | yes | accepted P4.2 ForestModel XML |
| `output/patchworks_tfl6_validated/fragments/fragments.cpg` | yes | fragments sidecar |
| `output/patchworks_tfl6_validated/fragments/fragments.dbf` | yes | fragments sidecar |
| `output/patchworks_tfl6_validated/fragments/fragments.prj` | yes | fragments sidecar |
| `output/patchworks_tfl6_validated/fragments/fragments.shp` | yes | fragments geometry |
| `output/patchworks_tfl6_validated/fragments/fragments.shx` | yes | fragments sidecar |
| `models/tfl6_patchworks_model/tracks/*.csv` | yes | accepted P4.3 Matrix Builder tracks |
| `models/tfl6_patchworks_model/blocks/blocks.cpg` | yes | block sidecar |
| `models/tfl6_patchworks_model/blocks/blocks.dbf` | yes | block sidecar |
| `models/tfl6_patchworks_model/blocks/blocks.prj` | yes | block sidecar |
| `models/tfl6_patchworks_model/blocks/blocks.shp` | yes | accepted P4.4a block geometry |
| `models/tfl6_patchworks_model/blocks/blocks.shx` | yes | block sidecar |
| `models/tfl6_patchworks_model/blocks/topology_blocks_200r.csv` | yes | accepted P4.4a topology |
| `models/tfl6_patchworks_model/analysis/base.pin` | yes | launch surface |
| `models/tfl6_patchworks_model/analysis/base_variant_common.bsh` | yes | launch helper |
| `models/tfl6_patchworks_model/analysis/headless_runtime_common.bsh` | yes | launch helper |
| `models/tfl6_patchworks_model/scripts/targets/flowtargets.bsh` | yes | target helper |
| `models/tfl6_patchworks_model/README.md` | yes | package readme |
| `models/tfl6_patchworks_model/lineage_registry.yaml` | yes | package lineage |

## Excluded Paths

The archive must not include:

- `models/tfl6_patchworks_model/analysis/p44*/`;
- `models/tfl6_patchworks_model/analysis/headless_runs/`;
- `models/tfl6_patchworks_model/patchworksLog.csv`;
- `runtime/`;
- `docs/_build/`;
- `data/model_input_bundle/`;
- source download caches; or
- local git-annex/dbdir/cache paths.

Saved-stage smoke outputs are evidence, not canonical runtime inputs.

## Manifest Schema

The YAML manifest must include:

```yaml
schema_version: 1
artifact_id: tfl6_patchworks_runtime_p5_2
archive_path: releases/tfl6_patchworks_runtime_p5_2.zip
archive_sha256: null
archive_size_bytes: null
instance_repo: UBC-FRESH/femic-tfl6-instance
instance_branch: feature/p5-publication-release
instance_commit: null
parent_repo: UBC-FRESH/femic
parent_branch: feature/tfl6-p5-publication-pointer
parent_commit: null
annex_remote:
  name: arbutus-s3
  bucket: ubc-fresh-femic-tfl6-instance
  publicurl: https://object-arbutus.cloud.computecanada.ca/ubc-fresh-femic-tfl6-instance
  uuid: 861b7dd7-fff0-4637-b0a2-b9b4668dca71
included_files: []
excluded_patterns: []
source_rebuild_commands:
  model_input_bundle: null
  forestmodel_export: null
  matrix_builder: null
  blocks_topology: null
validation:
  p4_4d_smoke_run_id: tfl6_p44d_harvest_smoke200
  direct_launch_smoke: accepted
  scenario_smoke: accepted
  fresh_clone_smoke: pending
```

Each `included_files` entry must include:

```yaml
- path: models/tfl6_patchworks_model/tracks/accounts.csv
  size_bytes: null
  sha256: null
  source_step: p4_3_matrix_builder
```

## Publication Commands

P5.2c should build the archive and manifest, then annex them:

```powershell
git annex add -f releases\tfl6_patchworks_runtime_p5_2.zip `
  releases\tfl6_patchworks_runtime_p5_2_manifest.yaml
git commit -m "P5.2 publish TFL6 runtime archive manifest"
git annex copy --to arbutus-s3 -- releases\tfl6_patchworks_runtime_p5_2.zip `
  releases\tfl6_patchworks_runtime_p5_2_manifest.yaml
git push
git push origin git-annex
```

The exact commit message may change, but the copy and `git-annex` branch push
are required.

## Fresh-Clone Proof

P5.2d must run a no-credential materialization smoke from a new clone. The smoke
must clear local S3 credentials before enabling the remote:

```powershell
Remove-Item Env:AWS_ACCESS_KEY_ID -ErrorAction SilentlyContinue
Remove-Item Env:AWS_SECRET_ACCESS_KEY -ErrorAction SilentlyContinue
Remove-Item Env:AWS_SESSION_TOKEN -ErrorAction SilentlyContinue
git clone https://github.com/UBC-FRESH/femic-tfl6-instance.git
cd femic-tfl6-instance
git annex init
git annex enableremote arbutus-s3
git annex get releases\tfl6_patchworks_runtime_p5_2.zip
git annex get releases\tfl6_patchworks_runtime_p5_2_manifest.yaml
```

The proof must record:

- clone path class, not a personal absolute path;
- `git annex info arbutus-s3` with `creds: not available`, `public: yes`, and a
  populated `publicurl`;
- successful `git annex get` for both release files; and
- SHA256 match against the manifest.
