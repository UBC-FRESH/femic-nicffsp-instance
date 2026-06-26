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

## Account-Output Repair

The missing account files were caused by premature Windows auto-close, not by
the XML `<output>` contract. Existing K3Z/TSA29 XML examples also omit explicit
`protoaccounts` / `accounts` output attributes; Matrix Builder writes those
tables after the core track tables when it is allowed to settle long enough.

P4.3 changed `config/patchworks.runtime.windows.yaml` from a `2.0` second
settle window to `20.0` seconds, cleared the generated tracks directory, and
reran Matrix Builder.

Command:

```powershell
..\..\.venv\Scripts\python.exe -m femic patchworks matrix-build `
  --config config\patchworks.runtime.windows.yaml `
  --run-id tfl6_p43_matrix_accounts_wait20
```

Result: accepted.

The manifest reports:

- `accounts_sync.status`: `synced`
- `protoaccounts_path`:
  `models/tfl6_patchworks_model/tracks/protoaccounts.csv`
- `accounts_path`: `models/tfl6_patchworks_model/tracks/accounts.csv`
- warning: `Processing completed. Review warnings and exit when finished.`

The raw Java return code remains nonzero because FEMIC force-stops the
Matrix Builder window after the configured settle period, but the output tables
and account promotion are complete. This is the same Windows automation seam
used for other instance Matrix Builder smoke runs.

Final generated track-table inspection:

| Table | Rows | Status |
| --- | ---: | --- |
| `blocks.csv` | 47,218 | readable |
| `features.csv` | 86,574 | readable |
| `groups.csv` | 24,879 | readable |
| `messages.csv` | 0 | readable |
| `products.csv` | 26,085 | readable |
| `strata.csv` | 28,858 | readable |
| `tracknames.csv` | 14,429 | readable |
| `treatments.csv` | 17,390 | readable |
| `protoaccounts.csv` | 211 | readable |
| `accounts.csv` | 211 | readable |

Account samples confirmed expected first-pass surfaces:

- managed area account rows exist;
- unmanaged area account rows exist;
- generic `product.Treated.managed.CC` exists;
- generic `product.HarvestedVolume.managed.Total.CC` exists; and
- no standalone seral account rows were emitted in this first Matrix Builder
  track package.

## P4.3 Closeout

P4.3 is complete for Matrix Builder and track/account QA. Runtime-package
assembly, Patchworks launch smoke, scenario targets, and final report surfaces
remain downstream in P4.4/P5.
