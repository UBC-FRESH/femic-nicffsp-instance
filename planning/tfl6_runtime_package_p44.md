# TFL 6 P4.4 Runtime Package Build and QA

## Scope

P4.4 assembles and smokes the first runnable TFL 6 Patchworks package after
P4.2 ForestModel/XML export and P4.3 Matrix Builder track QA.

The active runtime package root is:

- `models/tfl6_patchworks_model/`

Generated `blocks/`, `tracks/`, and `patchworksLog.csv` remain ignored until
Phase 5 decides which runtime artifacts are tracked, annexed, published, or
regenerated.

## Accepted Inputs

- ForestModel XML: `output/patchworks_tfl6_validated/forestmodel.xml`
- Fragments: `output/patchworks_tfl6_validated/fragments/fragments.*`
- Tracks: `models/tfl6_patchworks_model/tracks/*.csv`
- Runtime config: `config/patchworks.runtime.windows.yaml`

P4.3 accepted Matrix Builder run:

- run id: `tfl6_p43_matrix_accounts_wait20`
- `protoaccounts.csv`: 211 rows
- `accounts.csv`: 211 rows
- generic `CC` product and harvested-volume account surfaces present

## P4.4a Block and Topology Build

Command:

```powershell
..\..\.venv\Scripts\python.exe -m femic patchworks build-blocks `
  --config config\patchworks.runtime.windows.yaml `
  --topology-radius 200
```

The command exceeded the initial 120 second agent tool timeout but continued in
the background and completed. The process was allowed to finish rather than
being killed mid-topology.

Validation:

| Artifact | Result |
| --- | --- |
| `blocks.shp` rows | 24,879 |
| CRS | EPSG:3005 |
| Geometry validity | all valid |
| Area | 191,168.566 ha |
| Columns | `FRAGMENT_I`, `BLOCK`, `AREA_HA`, `F_AGE`, `AU`, `IFM`, `ORIGIN`, `SILV_STATE`, `RETENTION`, `TSA`, `geometry` |
| `topology_blocks_200r.csv` rows | 170,759 |
| Topology columns | `BLOCK1`, `BLOCK2`, `DISTANCE`, `LENGTH` |

P4.4a is accepted.

## Remaining P4.4 Steps

## P4.4b Launch Surface

P4.4b added the baseline launch surface:

- `models/tfl6_patchworks_model/analysis/base.pin`
- `models/tfl6_patchworks_model/analysis/base_variant_common.bsh`
- `models/tfl6_patchworks_model/analysis/headless_runtime_common.bsh`
- `models/tfl6_patchworks_model/scripts/targets/flowtargets.bsh`

The TFL 6 flow target helper uses the generated account label family
`product.HarvestedVolume.managed.*`, with
`product.HarvestedVolume.managed.Total.CC` as the default scenario-smoke target.

P4.4b is accepted.

## P4.4c Direct Launch Smoke

Command:

```powershell
..\..\.venv\Scripts\python.exe -m femic patchworks run-headless `
  models\tfl6_patchworks_model\analysis\base.pin `
  --config config\patchworks.runtime.windows.yaml `
  --run-id tfl6_p44b_launch0 `
  --iterations 0 `
  --stage-label p44b_launch0
```

Result: accepted.

Manifest evidence:

| Field | Value |
| --- | --- |
| run id | `tfl6_p44b_launch0` |
| raw return code | `0` |
| effective return code | `0` |
| terminal state | `success` |
| detected marker | `[FEMIC headless] saveStage completed` |
| saved files | `903` |
| scenario mode | `none` |
| stage directory | `models/tfl6_patchworks_model/analysis/p44b_launch0` |

Trace evidence confirms Patchworks loaded the PIN, initialized, skipped
scheduler iterations as requested, and completed `saveStage`.

P4.4c is accepted for direct launch smoke. The saved stage is generated output
and remains ignored in Git.

## Remaining P4.4 Steps

P4.4d must run a representative scenario smoke:

- activate an appropriate generic managed-volume target surface;
- confirm target status / target summary are written; and
- confirm schedule evidence is non-empty if a scheduling scenario is claimed.

## P4.4d Representative Scenario Smoke

Command:

```powershell
..\..\.venv\Scripts\python.exe -m femic patchworks run-headless `
  models\tfl6_patchworks_model\analysis\base.pin `
  --config config\patchworks.runtime.windows.yaml `
  --run-id tfl6_p44d_harvest_smoke200 `
  --stage-label p44d_harvest_smoke200 `
  --scenario-mode max-even-flow-smoke `
  --scenario-target product.HarvestedVolume.managed.Total.CC `
  --scenario-min-annual 1000 `
  --iterations 200
```

Result: accepted.

Manifest evidence:

| Field | Value |
| --- | --- |
| run id | `tfl6_p44d_harvest_smoke200` |
| raw return code | `0` |
| effective return code | `0` |
| terminal state | `success` |
| detected marker | `[FEMIC headless] saveStage completed` |
| saved files | `903` |
| scenario mode | `max-even-flow-smoke` |
| scenario target | `product.HarvestedVolume.managed.Total.CC` |
| scenario minimum annual | `1000` |
| iterations | `200` |
| stage directory | `models/tfl6_patchworks_model/analysis/p44d_harvest_smoke200` |

Target/schedule inspection:

| Check | Result |
| --- | --- |
| `scenario/targetStatus.csv` rows | `213` |
| `product.HarvestedVolume.managed.Total.CC` active | yes |
| `flow.even.product.HarvestedVolume.managed.Total.CC` active | yes |
| `scenario/targetSummary.csv` rows | `6573` |
| product current nonzero periods | `30` |
| product current sum | `1674405.726562` |
| `scenario/schedule.csv` rows | `801` |
| scheduled type | `MANAGED` |
| scheduled treatment | `CC` |

P4.4d is accepted. The saved stage is generated output and remains ignored in
Git. Phase 4 closeout can now proceed.
