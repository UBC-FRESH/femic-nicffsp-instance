# TFL 6 MP11 Phase 13 Archive And Materialization QA

This note records P13.4 archive/materialization QA for the MP11 candidate runtime. It builds a local ignored candidate archive and a tracked manifest so P13.5 can decide whether the candidate supplements Phase 5, replaces Phase 5 after stronger QA, or remains experimental.

## Summary

- archive_status: `local_archive_built_not_published`
- archive_path: `releases/tfl6_mp11_candidate_runtime_p13_4.zip`
- manifest_path: `releases/tfl6_mp11_candidate_runtime_p13_4_manifest.yaml`
- archive_size_bytes: `28053959`
- archive_sha256: `ec6377ce6e887ab18882e3b4c0dbb282be4a1aae5435e186913f720e36f5cb75`
- included_file_count: `32`
- local_archive_integrity: `pass`
- clean_checkout_materialization: `pending_publication_or_p13_5_decision`
- release_decision: `pending_p13_5`
- phase5_relationship: `phase5_remains_accepted_baseline_pending_p13_5`

## QA Rows

| ID | Status | Value | Evidence | Release implication |
| --- | --- | --- | --- | --- |
| `archive_status` | `local_archive_built_not_published` | `releases/tfl6_mp11_candidate_runtime_p13_4.zip` | `archive_built_and_zip_integrity_checked` | candidate_archive_available_for_p13_5_decision |
| `archive_sha256` | `recorded` | `ec6377ce6e887ab18882e3b4c0dbb282be4a1aae5435e186913f720e36f5cb75` | `releases/tfl6_mp11_candidate_runtime_p13_4_manifest.yaml` | supports_later_annex_or_publication_check |
| `archive_size_bytes` | `recorded` | `28053959` | `releases/tfl6_mp11_candidate_runtime_p13_4_manifest.yaml` | supports_later_annex_or_publication_check |
| `clean_checkout_materialization` | `pending_publication_or_p13_5_decision` | `not_run` | `archive_is_local_ignored_candidate_payload` | blocks_replacement_release_but_not_candidate_supplement_decision |
| `p11_4_forestmodel_xml_fragments` | `included` | `6 files` | `releases/tfl6_mp11_candidate_runtime_p13_4_manifest.yaml` | public_safe_runtime_input_candidate |
| `p12_1_runtime_config` | `included` | `1 files` | `releases/tfl6_mp11_candidate_runtime_p13_4_manifest.yaml` | public_safe_runtime_input_candidate |
| `p12_2_matrix_builder` | `included` | `13 files` | `releases/tfl6_mp11_candidate_runtime_p13_4_manifest.yaml` | public_safe_runtime_input_candidate |
| `p12_3_blocks_topology` | `included` | `6 files` | `releases/tfl6_mp11_candidate_runtime_p13_4_manifest.yaml` | public_safe_runtime_input_candidate |
| `p12_3_launch_and_metadata` | `included` | `6 files` | `releases/tfl6_mp11_candidate_runtime_p13_4_manifest.yaml` | public_safe_runtime_input_candidate |

## Included Runtime Inputs

| Path | Bytes | Source step | SHA256 |
| --- | ---: | --- | --- |
| `config/patchworks.runtime.mp11_candidate.windows.yaml` | `620` | `p12_1_runtime_config` | `d9328bc97700dc58efbb38e67b9c9388ad7e3765db80db8d5612c44f98b8e6ce` |
| `models/tfl6_patchworks_model_mp11_candidate/analysis/base.pin` | `157` | `p12_3_launch_and_metadata` | `279ed1c4b5fad324fe3b9dd036e872211fc9f567947c428727409db0a1b4d0ff` |
| `models/tfl6_patchworks_model_mp11_candidate/analysis/base_variant_common.bsh` | `3785` | `p12_3_launch_and_metadata` | `c17e67d6a021813bf5a829ce548df3a0af513d9c1dd088432f789a99b8c24d6b` |
| `models/tfl6_patchworks_model_mp11_candidate/analysis/headless_runtime_common.bsh` | `10831` | `p12_3_launch_and_metadata` | `63f944120fcd78c8cb4b632dd16669ce9ca5bfdda40f088f2ce270813b0f52a4` |
| `models/tfl6_patchworks_model_mp11_candidate/blocks/blocks.cpg` | `5` | `p12_3_blocks_topology` | `3ad3031f5503a4404af825262ee8232cc04d4ea6683d42c5dd0a2f2a27ac9824` |
| `models/tfl6_patchworks_model_mp11_candidate/blocks/blocks.dbf` | `10971993` | `p12_3_blocks_topology` | `6127a52e27c848a7a06e1bc196f33a92b4fd824165a9d5672456f75616bf3a96` |
| `models/tfl6_patchworks_model_mp11_candidate/blocks/blocks.prj` | `466` | `p12_3_blocks_topology` | `4dc6a252b4e1e9468f9489c04fc559230f6d8b3f6ad8a79f02ba365a593636f5` |
| `models/tfl6_patchworks_model_mp11_candidate/blocks/blocks.shp` | `19040188` | `p12_3_blocks_topology` | `ad9552a5bd34ca0b95c0b9406695a5b3520609fd1c17d7cd303f2207f44dee5f` |
| `models/tfl6_patchworks_model_mp11_candidate/blocks/blocks.shx` | `199132` | `p12_3_blocks_topology` | `8e53d7ba8b7933db4bd2b1dcde38698ee623f8c3049c97baab96fd7bcf3a6ea1` |
| `models/tfl6_patchworks_model_mp11_candidate/blocks/topology_blocks_200r.csv` | `4394747` | `p12_3_blocks_topology` | `2709734f92c0c3bb6bdcbefee7ef4d9c6c9e1b539c28a2f70984320a37bba179` |
| `models/tfl6_patchworks_model_mp11_candidate/lineage_registry.yaml` | `8294` | `p12_3_launch_and_metadata` | `9cc7bed1255a49515d6d452913a3b4528cadf15c4f2b21ba8ccb78085e9e01cc` |
| `models/tfl6_patchworks_model_mp11_candidate/README.md` | `1439` | `p12_3_launch_and_metadata` | `ff16db172c0fbf31e7d9062471070a91634bcca61169126e15009e2588752947` |
| `models/tfl6_patchworks_model_mp11_candidate/scripts/targets/flowtargets.bsh` | `2187` | `p12_3_launch_and_metadata` | `7282f221530db247242c0f3b7d37d698f59f16e0e81953f6f4f4b278ae46afc2` |
| `models/tfl6_patchworks_model_mp11_candidate/tracks/accounts.csv` | `60204` | `p12_2_matrix_builder` | `5c451419ee006830dbdf93fd692bfe41e6ba0ca5a1447a419c7515591b3ec99b` |
| `models/tfl6_patchworks_model_mp11_candidate/tracks/blocks.csv` | `1467082` | `p12_2_matrix_builder` | `2df28bad63de6ed92aacfb49bc4ba62bc017eaf5e0dc52dff18bfee00b1cf74d` |
| `models/tfl6_patchworks_model_mp11_candidate/tracks/curves.csv` | `15720364` | `p12_2_matrix_builder` | `cf04cc879933e7c001c5db2e57f4e623c678c4c0f5f0f0cb03abf02d69dcb73d` |
| `models/tfl6_patchworks_model_mp11_candidate/tracks/features.csv` | `3188444` | `p12_2_matrix_builder` | `ffd89366362551f68988aac6fcd84cb0127ba16ebc976973c9e2658876bb5a78` |
| `models/tfl6_patchworks_model_mp11_candidate/tracks/groups.csv` | `337266` | `p12_2_matrix_builder` | `a1e990ed463cc5cd791ae1eac81044451284bbad8438d5ab8f96a9ba125d18cf` |
| `models/tfl6_patchworks_model_mp11_candidate/tracks/messages.csv` | `60` | `p12_2_matrix_builder` | `ed43bd5f78304f72dee9ebcb3a9f1c8afea3a3888a7016802ad3e6f7fcf0373a` |
| `models/tfl6_patchworks_model_mp11_candidate/tracks/packages.csv` | `61` | `p12_2_matrix_builder` | `49d15b75d8d0286e7bb2ffe81de1b8d35fe1e02520a10b8edabbf72a1e3a0162` |
| `models/tfl6_patchworks_model_mp11_candidate/tracks/packageSequences.csv` | `25` | `p12_2_matrix_builder` | `f5fc343b5c4868e72048fa30176f52bf56cd21c95b77bd1c9cddca4a7cd63cb7` |
| `models/tfl6_patchworks_model_mp11_candidate/tracks/products.csv` | `1321561` | `p12_2_matrix_builder` | `e65032d250e20da1995472617653e3699fea1d247b9a026140bae43535a50bbe` |
| `models/tfl6_patchworks_model_mp11_candidate/tracks/protoaccounts.csv` | `60204` | `p12_2_matrix_builder` | `5c451419ee006830dbdf93fd692bfe41e6ba0ca5a1447a419c7515591b3ec99b` |
| `models/tfl6_patchworks_model_mp11_candidate/tracks/strata.csv` | `1819983` | `p12_2_matrix_builder` | `87740533524fa62e872264b222b86abfe42305b7fcb025c6573ac5bb12195205` |
| `models/tfl6_patchworks_model_mp11_candidate/tracks/tracknames.csv` | `1674711` | `p12_2_matrix_builder` | `7e5e92625567b114cb9762ef1b30da42cf1213dd3ea2e203f6e836dcffb83da8` |
| `models/tfl6_patchworks_model_mp11_candidate/tracks/treatments.csv` | `678650` | `p12_2_matrix_builder` | `8acbdfe33233d1c766f1408d71ab6696cfb3b0cdd6ed0cde7e36a0ee5b632470` |
| `output/patchworks_tfl6_mp11_candidate/forestmodel.xml` | `2668892` | `p11_4_forestmodel_xml_fragments` | `390e7e5a68469c0d008f68e4823944cb00da150953c42f9e96d1207414c1975c` |
| `output/patchworks_tfl6_mp11_candidate/fragments/fragments.cpg` | `5` | `p11_4_forestmodel_xml_fragments` | `3ad3031f5503a4404af825262ee8232cc04d4ea6683d42c5dd0a2f2a27ac9824` |
| `output/patchworks_tfl6_mp11_candidate/fragments/fragments.dbf` | `10971993` | `p11_4_forestmodel_xml_fragments` | `6127a52e27c848a7a06e1bc196f33a92b4fd824165a9d5672456f75616bf3a96` |
| `output/patchworks_tfl6_mp11_candidate/fragments/fragments.prj` | `466` | `p11_4_forestmodel_xml_fragments` | `4dc6a252b4e1e9468f9489c04fc559230f6d8b3f6ad8a79f02ba365a593636f5` |
| `output/patchworks_tfl6_mp11_candidate/fragments/fragments.shp` | `19040188` | `p11_4_forestmodel_xml_fragments` | `ad9552a5bd34ca0b95c0b9406695a5b3520609fd1c17d7cd303f2207f44dee5f` |
| `output/patchworks_tfl6_mp11_candidate/fragments/fragments.shx` | `199132` | `p11_4_forestmodel_xml_fragments` | `8e53d7ba8b7933db4bd2b1dcde38698ee623f8c3049c97baab96fd7bcf3a6ea1` |

## Excluded Runtime Outputs

- `models/tfl6_patchworks_model_mp11_candidate/analysis/p*/`
- `models/tfl6_patchworks_model_mp11_candidate/analysis/headless_runs/`
- `models/tfl6_patchworks_model_mp11_candidate/patchworksLog.csv`
- `runtime/`
- `docs/_build/`
- `data/mp11_model_input_bundle/`
- `data/downloads/`
- `data/bc/`

Saved-stage outputs, runtime logs, generated model-input tables, and source download caches are excluded from the archive. They remain QA or rebuild evidence, not canonical runtime launch inputs.

## Materialization Boundary

The archive exists locally under the ignored `releases/` root and passed ZIP integrity checks. It has not been annexed, copied to `arbutus-s3`, or proven from a no-credential clean checkout. That prevents a `replace_phase5` release decision in P13.5, but it is enough evidence for P13.5 to decide whether the candidate can supplement Phase 5 as a documented MP11 candidate surface.

The Phase 5 release archive remains the accepted public runtime package until P13.5 makes an explicit decision.
