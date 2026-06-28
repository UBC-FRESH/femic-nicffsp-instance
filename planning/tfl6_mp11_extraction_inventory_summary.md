# TFL 6 MP11 Extraction Inventory

## Purpose

This P6.2 inventory is the first structured extraction pass over the MP11
PDF. It records raw heading, table, figure, and high-priority claim
candidates with source SHA256, document component, one-based PDF page,
review status, downstream use, and model-input status.

This is an inventory surface only. Rows are `raw_extraction`, downstream
use is `phase6_inventory_triage_only`, and model-input status is
`not_model_input`.

## Files

- CSV: `planning/tfl6_mp11_extraction_inventory.csv`
- JSON summary: `planning/tfl6_mp11_extraction_inventory_summary.json`
- Markdown summary: `planning/tfl6_mp11_extraction_inventory_summary.md`

## Counts

- Row count: `1870`
- Object type counts: `{'claim_candidate': 1094, 'figure': 244, 'heading': 245, 'table': 287}`
- Comparison topic counts: `{'aac': 131, 'inventory_yield': 815, 'land_base': 225, 'metadata': 458, 'model_behavior': 241}`
- Document component counts: `{'appendix_a_timber_supply_analysis': 935, 'appendix_b_acceptance_letter': 2, 'appendix_b_information_package': 827, 'management_plan_main': 106}`
- Review status counts: `{'raw_extraction': 1870}`
- Model-input status counts: `{'not_model_input': 1870}`

## Interpretation

Use this file as the extraction queue for detailed P6.2 review. It is not
a reviewed source of model assumptions. Phase 7 figure closeout evidence
should be linked where relevant instead of duplicating recovered figure
tables into this raw inventory.

## Next Step

Review and normalize the highest-priority table and claim rows into
P6.3-P6.5 comparison crosswalks. Keep raw extraction separate from
reviewed evidence and accepted model contracts.
