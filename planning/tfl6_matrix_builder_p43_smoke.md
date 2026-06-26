# TFL 6 P4.3 Matrix Builder Smoke

## Purpose

This note records the first P4.3 Matrix Builder smoke run against the accepted
P4.2 ForestModel XML/fragments pair.

Governing issue: `#38`.

## Runtime Config Repair

The instance-local `config/patchworks.runtime.windows.yaml` initially still
pointed at copied K3Z paths. P4.3 corrected the config to use:

- fragments: `../output/patchworks_tfl6_validated/fragments/fragments.dbf`
- ForestModel XML: `../output/patchworks_tfl6_validated/forestmodel.xml`
- tracks output: `../models/tfl6_patchworks_model/tracks`

`auto_close_window_on_success` was set to `true`, matching the K3Z Windows
Matrix Builder workflow, so the spawned Matrix Builder window does not leave the
agent command hanging after output generation.

## Preflight

Command:

```powershell
..\..\.venv\Scripts\python.exe -m femic patchworks preflight `
  --config config\patchworks.runtime.windows.yaml
```

Result: passed. Patchworks jar, Java launcher, license environment, and
`SPSHOME` were all found.

## First Matrix Builder Attempt

Command:

```powershell
..\..\.venv\Scripts\python.exe -m femic patchworks matrix-build `
  --config config\patchworks.runtime.windows.yaml `
  --run-id tfl6_p43_matrix
```

Result: not accepted.

Although the FEMIC wrapper reported effective return code `0`, direct log and
output inspection showed a hard Matrix Builder failure:

- manifest `raw_returncode`: `1`;
- generated core CSVs were zero bytes except `messages.csv`; and
- Matrix Builder failed while processing Block 1 because pass-through
  succession used `breakup="1000"` and `renew="1000"`.

The relevant Matrix Builder message was:

```text
A succession rule has tried to breakup up a stand at a younger age than when
the stand transferred on to this strata, and this is not allowed.
strata=+treatment()+AU(6000171)+IFM(unmanaged)+ORIGIN(planted)+SILV_STATE(cc_pl)+RETENTION(0.154938618532016)
breakup age=1000
current age=1000
```

## Succession Repair

The generic FEMIC FMG exporter was repaired so default pass-through succession
uses the Patchworks-compatible `breakup="999"` and `renew="0"` pattern already
used by the recovered MKRF legacy contract. The generated TFL 6 XML was then
regenerated from the accepted P4.2 export bridge.

Verification:

- targeted serializer test passed:
  `python -m pytest tests\test_fmg_patchworks.py -k default_pass_through_successions`;
- regenerated XML contains `<succession breakup="999" renew="0" />`; and
- regenerated XML/fragments still report `407` AUs, `24,879` fragments, and
  `373` XML curves.

## Second Matrix Builder Attempt

Command:

```powershell
..\..\.venv\Scripts\python.exe -m femic patchworks matrix-build `
  --config config\patchworks.runtime.windows.yaml `
  --run-id tfl6_p43_matrix_succession999
```

Result: core tracks generated and are readable.

Generated track-table inspection:

| Table | Rows | Status |
| --- | ---: | --- |
| `blocks.csv` | 33,322 | readable |
| `features.csv` | 55,717 | readable |
| `groups.csv` | 17,173 | readable |
| `messages.csv` | 0 | readable |
| `products.csv` | 16,379 | readable |
| `strata.csv` | 18,447 | readable |
| `tracknames.csv` | 9,212 | readable |
| `treatments.csv` | 10,703 | readable |
| `curves.csv` | 0 | empty helper table |
| `packages.csv` | 0 | empty helper table |
| `packageSequences.csv` | 0 | empty helper table |
| `protoaccounts.csv` | missing | P4.3 gap |
| `accounts.csv` | missing | P4.3 gap |

The manifest still records `raw_returncode=1` because the Windows auto-closer
force-stopped the Matrix Builder process after outputs appeared. The generated
core tables are therefore treated as smoke-pass evidence, not full P4.3
closeout evidence.

## Remaining P4.3 Gap

P4.3 remains open because the current FMG XML `<output>` contract does not
request `protoaccounts.csv` or `accounts.csv`, so FEMIC reports
`accounts_sync: skipped_missing_protoaccounts`.

Next bounded repair: add or configure the account/protoaccount output contract
needed by TFL 6, regenerate XML, rerun Matrix Builder, and verify
`protoaccounts.csv -> accounts.csv` promotion before P4.3 closes.
