# TFL 6 MP11 Phase 14 No-Heli Tracks

This P14.7 helper builds a generated no-heli track variant by copying the P14.6 harvest-system Matrix Builder tracks and removing `CC_HELI` treatment/product rows. It does not change the all-system tracks.

## Summary

- generated_at_utc: `2026-06-29T06:51:28+00:00`
- source_tracks_root: `models/tfl6_patchworks_model_mp11_harvest_system_candidate/tracks`
- no_heli_tracks_root: `models/tfl6_patchworks_model_mp11_harvest_system_candidate/tracks_no_heli`
- treatment_rows_removed: `892`
- product_rows_removed: `2230`
- account_rows_removed: `2`
- protoaccount_rows_removed: `2`
- treatments_rows: `17750`
- products_rows: `44375`
- accounts_rows: `827`
- protoaccounts_rows: `827`
- accounts_proto_equal: `True`
- cc_heli_treatment_rows: `0`
- cc_heli_product_rows: `0`
- cc_heli_account_rows: `0`
- cc_heli_protoaccount_rows: `0`
- aggregate_cc_product_rows: `17750`

## Boundary

- The no-heli variant is a smoke-test track variant, not a new source model.
- The all-system tracks remain under `tracks/`.
- The no-heli tracks are generated under ignored `tracks_no_heli/`.
