# TFL 6 MP11 Phase 15 Materialization QA

This P15.4 report records no-credential clean-checkout materialization for the
published Phase 15 MP11 harvest-system runtime archive. It proves that the
archive and manifest can be fetched from `arbutus-s3`, verifies the archive
checksum against the manifest, and unpacks the archive for P15.5 smoke testing.

## Summary

- materialization_status: `materialized_smoke_pending`
- clone_path_class: `temp_clean_checkout`
- clone_mode: `shallow_single_branch_no_tags`
- branch: `feature/tfl6-mp11-p15-runtime-publication`
- archive: `releases/tfl6_mp11_harvest_system_candidate_runtime_p15_2.zip`
- manifest: `releases/tfl6_mp11_harvest_system_candidate_runtime_p15_2_manifest.yaml`
- archive_sha256: `fcf8d3615f8bba65419d1a401d818c5eb87e7d75d3aa6007cfa6ada773536362`
- expected_files_present: `true`
- next_status: `p15_5_archive_derived_smoke_pending`

## QA Rows

| ID | Status | Value | Evidence | Replacement implication |
| --- | --- | --- | --- | --- |
| `clone_mode` | `pass` | `shallow_single_branch_no_tags` | `manual_p15_4_clean_checkout` | clean_checkout_materialization_exercised |
| `git_annex_metadata` | `pass` | `origin_git_annex_fetched_before_enableremote` | `manual_p15_4_clean_checkout` | documents_required_fresh_clone_annex_metadata_step |
| `remote_public_access` | `pass` | `creds_not_available_public_yes_remote_keys_5` | `git_annex_info_arbutus_s3` | no_credential_public_read_confirmed |
| `archive_get` | `pass` | `releases/tfl6_mp11_harvest_system_candidate_runtime_p15_2.zip` | `git_annex_get_checksum_ok` | archive_materialized_from_arbutus_s3 |
| `manifest_get` | `pass` | `releases/tfl6_mp11_harvest_system_candidate_runtime_p15_2_manifest.yaml` | `git_annex_get_checksum_ok` | manifest_materialized_from_arbutus_s3 |
| `archive_sha256` | `pass` | `fcf8d3615f8bba65419d1a401d818c5eb87e7d75d3aa6007cfa6ada773536362` | `manifest_sha256_comparison` | materialized_archive_matches_manifest |
| `archive_unpack` | `pass` | `temp_clean_checkout_runtime_p15_materialized_archive` | `expand_archive_expected_files_present` | archive_layout_ready_for_p15_5_smoke |
| `phase5_relationship` | `baseline_preserved` | `phase5_remains_accepted_baseline_pending_replacement_acceptance` | `p15_4_materialization_boundary` | p15_does_not_silently_replace_phase5 |

## Fresh-Clone Annex Metadata Note

The fresh clone needed the `git-annex` branch metadata before `arbutus-s3`
could be enabled. The robust sequence for this repository is:

```powershell
git clone --depth 1 --single-branch --no-tags --branch feature/tfl6-mp11-p15-runtime-publication https://github.com/UBC-FRESH/femic-tfl6-instance.git
cd femic-tfl6-instance
git fetch origin git-annex:refs/remotes/origin/git-annex
git update-ref refs/heads/git-annex refs/remotes/origin/git-annex
git annex init
git annex enableremote arbutus-s3
git annex get releases\tfl6_mp11_harvest_system_candidate_runtime_p15_2.zip releases\tfl6_mp11_harvest_system_candidate_runtime_p15_2_manifest.yaml
```

After the metadata step, `git annex info arbutus-s3` reported `creds: not
available`, `public: yes`, the expected public URL, and `5` remote keys.

## Boundary

- P15.4 proves public materialization and archive unpacking.
- P15.4 does not run Patchworks.
- Direct launch and all-system/no-heli archive-derived smoke remain P15.5.
- Phase 5 remains the accepted public baseline until a later replacement
  acceptance decision.
