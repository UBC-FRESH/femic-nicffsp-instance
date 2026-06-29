# TFL 6 MP11 Phase 15 Archive Publication QA

This report records the P15.2 local archive/manifest build and the P15.3 publication status for the Phase 14 MP11 harvest-system candidate runtime. It does not prove clean-checkout materialization.

## Summary

- archive_status: `published_materialization_pending`
- archive_path: `releases/tfl6_mp11_harvest_system_candidate_runtime_p15_2.zip`
- manifest_path: `releases/tfl6_mp11_harvest_system_candidate_runtime_p15_2_manifest.yaml`
- archive_size_bytes: `33806073`
- archive_sha256: `fcf8d3615f8bba65419d1a401d818c5eb87e7d75d3aa6007cfa6ada773536362`
- included_file_count: `46`
- source_runtime_phase: `phase14_harvest_system_candidate`
- phase5_relationship: `phase5_remains_accepted_baseline_pending_replacement_acceptance`

## QA Rows

| ID | Status | Value | Evidence | Replacement implication |
| --- | --- | --- | --- | --- |
| `archive_status` | `published_materialization_pending` | `releases/tfl6_mp11_harvest_system_candidate_runtime_p15_2.zip` | `archive_built_and_zip_integrity_checked` | candidate_archive_published_pending_materialization |
| `archive_sha256` | `recorded` | `fcf8d3615f8bba65419d1a401d818c5eb87e7d75d3aa6007cfa6ada773536362` | `releases/tfl6_mp11_harvest_system_candidate_runtime_p15_2_manifest.yaml` | supports_publication_and_materialization_checks |
| `archive_size_bytes` | `recorded` | `33806073` | `releases/tfl6_mp11_harvest_system_candidate_runtime_p15_2_manifest.yaml` | supports_publication_and_materialization_checks |
| `phase5_relationship` | `baseline_preserved` | `phase5_remains_accepted_baseline_pending_replacement_acceptance` | `releases/tfl6_mp11_harvest_system_candidate_runtime_p15_2_manifest.yaml` | p15_is_replacement_candidate_review_not_silent_replacement |
| `p14_5_forestmodel_xml_fragments` | `included` | `6 files` | `releases/tfl6_mp11_harvest_system_candidate_runtime_p15_2_manifest.yaml` | public_safe_runtime_payload_candidate |
| `p14_6_blocks_topology` | `included` | `6 files` | `releases/tfl6_mp11_harvest_system_candidate_runtime_p15_2_manifest.yaml` | public_safe_runtime_payload_candidate |
| `p14_6_matrix_builder_tracks` | `included` | `13 files` | `releases/tfl6_mp11_harvest_system_candidate_runtime_p15_2_manifest.yaml` | public_safe_runtime_payload_candidate |
| `p14_7_no_heli_tracks` | `included` | `13 files` | `releases/tfl6_mp11_harvest_system_candidate_runtime_p15_2_manifest.yaml` | public_safe_runtime_payload_candidate |
| `p14_runtime_config` | `included` | `1 files` | `releases/tfl6_mp11_harvest_system_candidate_runtime_p15_2_manifest.yaml` | public_safe_runtime_payload_candidate |
| `p14_runtime_launch_surfaces` | `included` | `5 files` | `releases/tfl6_mp11_harvest_system_candidate_runtime_p15_2_manifest.yaml` | public_safe_runtime_payload_candidate |
| `p14_runtime_metadata` | `included` | `2 files` | `releases/tfl6_mp11_harvest_system_candidate_runtime_p15_2_manifest.yaml` | public_safe_runtime_payload_candidate |

## Included Runtime Inputs

| Path | Bytes | Source step | SHA256 |
| --- | ---: | --- | --- |
| `config/patchworks.runtime.mp11_harvest_system_candidate.windows.yaml` | `650` | `p14_runtime_config` | `0d10bfd5ae03ded89789eca7fd4008e8fe0cceeb2ff32d012508bd85dce7825c` |
| `models/tfl6_patchworks_model_mp11_harvest_system_candidate/analysis/base.pin` | `157` | `p14_runtime_launch_surfaces` | `279ed1c4b5fad324fe3b9dd036e872211fc9f567947c428727409db0a1b4d0ff` |
| `models/tfl6_patchworks_model_mp11_harvest_system_candidate/analysis/base_variant_common.bsh` | `3785` | `p14_runtime_launch_surfaces` | `c17e67d6a021813bf5a829ce548df3a0af513d9c1dd088432f789a99b8c24d6b` |
| `models/tfl6_patchworks_model_mp11_harvest_system_candidate/analysis/headless_runtime_common.bsh` | `10831` | `p14_runtime_launch_surfaces` | `63f944120fcd78c8cb4b632dd16669ce9ca5bfdda40f088f2ce270813b0f52a4` |
| `models/tfl6_patchworks_model_mp11_harvest_system_candidate/analysis/no_heli.pin` | `172` | `p14_runtime_launch_surfaces` | `563d1e7741b7c8fcb0edc928e61fc2a5601281b91ff01a118b9672adbe7056dd` |
| `models/tfl6_patchworks_model_mp11_harvest_system_candidate/blocks/blocks.cpg` | `5` | `p14_6_blocks_topology` | `3ad3031f5503a4404af825262ee8232cc04d4ea6683d42c5dd0a2f2a27ac9824` |
| `models/tfl6_patchworks_model_mp11_harvest_system_candidate/blocks/blocks.dbf` | `12962345` | `p14_6_blocks_topology` | `dc15a041eb3eed85b06e121c438516c86301c8e4d839b6e1916020430b7f4f7d` |
| `models/tfl6_patchworks_model_mp11_harvest_system_candidate/blocks/blocks.prj` | `466` | `p14_6_blocks_topology` | `4dc6a252b4e1e9468f9489c04fc559230f6d8b3f6ad8a79f02ba365a593636f5` |
| `models/tfl6_patchworks_model_mp11_harvest_system_candidate/blocks/blocks.shp` | `19040188` | `p14_6_blocks_topology` | `ad9552a5bd34ca0b95c0b9406695a5b3520609fd1c17d7cd303f2207f44dee5f` |
| `models/tfl6_patchworks_model_mp11_harvest_system_candidate/blocks/blocks.shx` | `199132` | `p14_6_blocks_topology` | `8e53d7ba8b7933db4bd2b1dcde38698ee623f8c3049c97baab96fd7bcf3a6ea1` |
| `models/tfl6_patchworks_model_mp11_harvest_system_candidate/blocks/topology_blocks_200r.csv` | `4394747` | `p14_6_blocks_topology` | `2709734f92c0c3bb6bdcbefee7ef4d9c6c9e1b539c28a2f70984320a37bba179` |
| `models/tfl6_patchworks_model_mp11_harvest_system_candidate/lineage_registry.yaml` | `3894` | `p14_runtime_metadata` | `e5a0e5751f7fdd00f81cd20021d033afe7614a2fb182838b5df159c25cf26ff8` |
| `models/tfl6_patchworks_model_mp11_harvest_system_candidate/README.md` | `1386` | `p14_runtime_metadata` | `a4a2f62f05bea8b65115fb4f18ce53b8445a2a3a7596e4cd57a48a78041858d3` |
| `models/tfl6_patchworks_model_mp11_harvest_system_candidate/scripts/targets/flowtargets.bsh` | `2187` | `p14_runtime_launch_surfaces` | `7282f221530db247242c0f3b7d37d698f59f16e0e81953f6f4f4b278ae46afc2` |
| `models/tfl6_patchworks_model_mp11_harvest_system_candidate/tracks/accounts.csv` | `60762` | `p14_6_matrix_builder_tracks` | `34c3b7c2c4e5e21f68bb6e6cbd0d99431143e653585f83b8875f15f0b8f3dbbb` |
| `models/tfl6_patchworks_model_mp11_harvest_system_candidate/tracks/blocks.csv` | `1477233` | `p14_6_matrix_builder_tracks` | `e2607720ae6e9f0b9fb4287ecd9e6075def2bdf8ba19334c651074db2a79b2af` |
| `models/tfl6_patchworks_model_mp11_harvest_system_candidate/tracks/curves.csv` | `17033244` | `p14_6_matrix_builder_tracks` | `d0892553b6e100edfd599d1d448855aedc7fb04995f0b97b5ac3dcb12f63693b` |
| `models/tfl6_patchworks_model_mp11_harvest_system_candidate/tracks/features.csv` | `3444497` | `p14_6_matrix_builder_tracks` | `7fcaf6f604b6b4c5713b2d063f082e77207e6bcb7631cf39cda86ec38c7c3982` |
| `models/tfl6_patchworks_model_mp11_harvest_system_candidate/tracks/groups.csv` | `337266` | `p14_6_matrix_builder_tracks` | `a1e990ed463cc5cd791ae1eac81044451284bbad8438d5ab8f96a9ba125d18cf` |
| `models/tfl6_patchworks_model_mp11_harvest_system_candidate/tracks/messages.csv` | `66` | `p14_6_matrix_builder_tracks` | `dc63c922915d439fe5ea75e3e69a6f07581fa2a705b289b9780c865f40582182` |
| `models/tfl6_patchworks_model_mp11_harvest_system_candidate/tracks/packages.csv` | `61` | `p14_6_matrix_builder_tracks` | `49d15b75d8d0286e7bb2ffe81de1b8d35fe1e02520a10b8edabbf72a1e3a0162` |
| `models/tfl6_patchworks_model_mp11_harvest_system_candidate/tracks/packageSequences.csv` | `25` | `p14_6_matrix_builder_tracks` | `f5fc343b5c4868e72048fa30176f52bf56cd21c95b77bd1c9cddca4a7cd63cb7` |
| `models/tfl6_patchworks_model_mp11_harvest_system_candidate/tracks/products.csv` | `2821608` | `p14_6_matrix_builder_tracks` | `8572fe8a884e94c1444dd123a7544c1a2cb67ff50d99b8204acd81badcb40900` |
| `models/tfl6_patchworks_model_mp11_harvest_system_candidate/tracks/protoaccounts.csv` | `60762` | `p14_6_matrix_builder_tracks` | `34c3b7c2c4e5e21f68bb6e6cbd0d99431143e653585f83b8875f15f0b8f3dbbb` |
| `models/tfl6_patchworks_model_mp11_harvest_system_candidate/tracks/strata.csv` | `2170533` | `p14_6_matrix_builder_tracks` | `1362d5d2dfd3bed0bb679708365f82875aab56f6a3dd0b56e59830fdf6d1e3b1` |
| `models/tfl6_patchworks_model_mp11_harvest_system_candidate/tracks/tracknames.csv` | `2018546` | `p14_6_matrix_builder_tracks` | `4fc8778f7885c560b83e5e9ee09d71e3d0c1163a2f83b69c174e2e47d190171f` |
| `models/tfl6_patchworks_model_mp11_harvest_system_candidate/tracks/treatments.csv` | `851273` | `p14_6_matrix_builder_tracks` | `03dc081ae44430bd3fdea6026f099e71293254fcf32a5e7f94cc656bf69a6c38` |
| `models/tfl6_patchworks_model_mp11_harvest_system_candidate/tracks_no_heli/accounts.csv` | `60580` | `p14_7_no_heli_tracks` | `2a4afa1ec1db62a5d0d20deb226993d88519684f6222f4178ea2fef95280bf37` |
| `models/tfl6_patchworks_model_mp11_harvest_system_candidate/tracks_no_heli/blocks.csv` | `1477233` | `p14_7_no_heli_tracks` | `e2607720ae6e9f0b9fb4287ecd9e6075def2bdf8ba19334c651074db2a79b2af` |
| `models/tfl6_patchworks_model_mp11_harvest_system_candidate/tracks_no_heli/curves.csv` | `17033244` | `p14_7_no_heli_tracks` | `d0892553b6e100edfd599d1d448855aedc7fb04995f0b97b5ac3dcb12f63693b` |
| `models/tfl6_patchworks_model_mp11_harvest_system_candidate/tracks_no_heli/features.csv` | `3444497` | `p14_7_no_heli_tracks` | `7fcaf6f604b6b4c5713b2d063f082e77207e6bcb7631cf39cda86ec38c7c3982` |
| `models/tfl6_patchworks_model_mp11_harvest_system_candidate/tracks_no_heli/groups.csv` | `337266` | `p14_7_no_heli_tracks` | `a1e990ed463cc5cd791ae1eac81044451284bbad8438d5ab8f96a9ba125d18cf` |
| `models/tfl6_patchworks_model_mp11_harvest_system_candidate/tracks_no_heli/messages.csv` | `66` | `p14_7_no_heli_tracks` | `dc63c922915d439fe5ea75e3e69a6f07581fa2a705b289b9780c865f40582182` |
| `models/tfl6_patchworks_model_mp11_harvest_system_candidate/tracks_no_heli/packages.csv` | `61` | `p14_7_no_heli_tracks` | `49d15b75d8d0286e7bb2ffe81de1b8d35fe1e02520a10b8edabbf72a1e3a0162` |
| `models/tfl6_patchworks_model_mp11_harvest_system_candidate/tracks_no_heli/packageSequences.csv` | `25` | `p14_7_no_heli_tracks` | `f5fc343b5c4868e72048fa30176f52bf56cd21c95b77bd1c9cddca4a7cd63cb7` |
| `models/tfl6_patchworks_model_mp11_harvest_system_candidate/tracks_no_heli/products.csv` | `2691593` | `p14_7_no_heli_tracks` | `21510b5b34e393255ed8d7280ac9388b15346994aa41a2e26191b7439b9074cf` |
| `models/tfl6_patchworks_model_mp11_harvest_system_candidate/tracks_no_heli/protoaccounts.csv` | `60580` | `p14_7_no_heli_tracks` | `2a4afa1ec1db62a5d0d20deb226993d88519684f6222f4178ea2fef95280bf37` |
| `models/tfl6_patchworks_model_mp11_harvest_system_candidate/tracks_no_heli/strata.csv` | `2170533` | `p14_7_no_heli_tracks` | `1362d5d2dfd3bed0bb679708365f82875aab56f6a3dd0b56e59830fdf6d1e3b1` |
| `models/tfl6_patchworks_model_mp11_harvest_system_candidate/tracks_no_heli/tracknames.csv` | `2018546` | `p14_7_no_heli_tracks` | `4fc8778f7885c560b83e5e9ee09d71e3d0c1163a2f83b69c174e2e47d190171f` |
| `models/tfl6_patchworks_model_mp11_harvest_system_candidate/tracks_no_heli/treatments.csv` | `812075` | `p14_7_no_heli_tracks` | `655e7bd742c7d4a35f298f2719ad50b8e1bbd6a1f1bb0b1885ee21c855584150` |
| `output/patchworks_tfl6_mp11_harvest_system_candidate/forestmodel.xml` | `6633605` | `p14_5_forestmodel_xml_fragments` | `d895703182219ff70ff6b35f140fa03ac650805b6b871c09d5763690cdd93f2e` |
| `output/patchworks_tfl6_mp11_harvest_system_candidate/fragments/fragments.cpg` | `5` | `p14_5_forestmodel_xml_fragments` | `3ad3031f5503a4404af825262ee8232cc04d4ea6683d42c5dd0a2f2a27ac9824` |
| `output/patchworks_tfl6_mp11_harvest_system_candidate/fragments/fragments.dbf` | `12962345` | `p14_5_forestmodel_xml_fragments` | `dc15a041eb3eed85b06e121c438516c86301c8e4d839b6e1916020430b7f4f7d` |
| `output/patchworks_tfl6_mp11_harvest_system_candidate/fragments/fragments.prj` | `466` | `p14_5_forestmodel_xml_fragments` | `4dc6a252b4e1e9468f9489c04fc559230f6d8b3f6ad8a79f02ba365a593636f5` |
| `output/patchworks_tfl6_mp11_harvest_system_candidate/fragments/fragments.shp` | `19040188` | `p14_5_forestmodel_xml_fragments` | `ad9552a5bd34ca0b95c0b9406695a5b3520609fd1c17d7cd303f2207f44dee5f` |
| `output/patchworks_tfl6_mp11_harvest_system_candidate/fragments/fragments.shx` | `199132` | `p14_5_forestmodel_xml_fragments` | `8e53d7ba8b7933db4bd2b1dcde38698ee623f8c3049c97baab96fd7bcf3a6ea1` |

## Excluded Runtime Outputs

- `models/tfl6_patchworks_model_mp11_harvest_system_candidate/analysis/p*/`
- `models/tfl6_patchworks_model_mp11_harvest_system_candidate/analysis/headless_runs/`
- `models/tfl6_patchworks_model_mp11_harvest_system_candidate/patchworksLog.csv`
- `runtime/`
- `docs/_build/`
- `data/mp11_harvest_system_model_input_bundle/`
- `data/mp11_model_input_bundle/`
- `data/downloads/`
- `data/bc/`

## Publication Evidence

- annex_remote: `arbutus-s3`
- remote_bucket: `ubc-fresh-femic-tfl6-instance`
- publicurl: `https://object-arbutus.cloud.computecanada.ca/ubc-fresh-femic-tfl6-instance`
- publication_status: `published_materialization_pending`
- clean_checkout_materialization: `pending_p15_4`

## Boundary

- P15.2 built the local archive and tracked manifest.
- P15.3 annexed and copied the archive and manifest to `arbutus-s3`.
- No-credential materialization remains P15.4.
- Archive-derived launch and scenario smoke remain P15.5.
- The archive is a replacement candidate input, not an automatic Phase 5 replacement.
