# TFL 6 Cedar Signal Design

## Purpose

This note starts P3.1 by translating TFL 6 cedar evidence into model-design
requirements for the teaching instance.

Governing issue: `#8`.

This is a design note only. It does not generate model inputs, Patchworks XML,
Matrix Builder outputs, or a runtime package.

## Source Evidence

### Cultural Cedar Need

The 2012 AAC rationale records First Nations concerns about monumental and
old-growth cedar. KFN raised potential overharvest concerns, while MQFN and TFN
identified continued access to monumental cedar for cultural purposes. MQFN,
NFN, QFN, and TFN also raised archaeological-feature protection concerns.

The same rationale records WFP's position that a significant volume of
old-growth cedar exists in TFL 6, with a large portion outside the THLB, and
that non-contributing land may contain larger cedar trees suitable for canoes,
buildings, and poles. WFP also offered further engagement to discuss cultural
cedar needs and potential inventory of those needs.

Design implication: cultural cedar must not be represented only as harvested
volume. The model needs visible cedar availability and reserve/reporting
signals that can distinguish old/large cedar and non-THLB reserve context from
scheduled timber production.

### Cedar Composition

The 2011 information package forest-cover summary records western redcedar as
the second-largest forest component after western hemlock:

- western hemlock: `102664 ha` / `67.5%`;
- western redcedar: `28608 ha` / `18.8%`; and
- yellow-cedar: `8212 ha` / `5.4%`.

Design implication: cedar is large enough to justify dedicated account/report
signals, but most forested area is not cedar-leading. The first design should
separate cedar-leading, cedar-present, yellow-cedar, and old/large cedar
signals rather than treating all conifer volume as equivalent.

### Productivity and Yield Evidence

The 2011 information package includes TFL 6-specific site-index conversion
evidence for Cw and other target species. Table 42 estimates Cw site index by
productivity group:

- PG1: `27.0 m`;
- PG2: `24.5 m`;
- PG3: `23.7 m`;
- PG2+3: `23.8 m`;
- PG4: `19.2 m`.

The AAC rationale records that fertilization effects for hemlock, spruce, and
redcedar were modeled using the next higher productivity group, with support
from Salal-Cedar-Hemlock Integrated Research Program work near Port McNeill.
It also records that genetically improved select seed was used for Douglas-fir,
western hemlock, western redcedar, and yellow-cedar plantations.

Design implication: cedar yield behavior belongs in model-design assumptions,
not in THLB netdown. The first model-input bundle should preserve enough cedar
species, productivity-group, site-index, managed-origin, and treatment
attribution to support later cedar-specific curve/account decisions.

### K3Z Carry-Forward Boundary

The K3Z template provides useful structural patterns but not accepted TFL 6
cedar semantics. Existing planning already rejects carrying forward K3Z product
or account targets as TFL 6 cedar logic.

Design implication: P3.1 may borrow the shape of K3Z-style account/product and
reporting surfaces, but cedar thresholds, treatments, products, and targets
must be TFL 6-specific or explicitly marked as teaching approximations.

## First Cedar Signal Set

The first P3.1 design lane should define these source-derived signals for later
model-input generation:

| Signal | First definition | Purpose | Status |
| --- | --- | --- | --- |
| `cedar_leading` | Primary species is western redcedar (`Cw` / source code `C`) or yellow-cedar (`Yc` / source code `Cy`) depending on accepted R1/VDYP species coding. | Separate cedar-dominant stands for reporting, products, and treatment review. | Draft; verify exact R1/VDYP species columns and code values in P3.1b. |
| `western_redcedar_leading` | Primary species is western redcedar. | Preserve Cw-specific cultural and utility-pole signals. | Draft. |
| `yellow_cedar_leading` | Primary species is yellow-cedar/cypress. | Keep yellow-cedar visible without conflating it with Cw cultural cedar. | Draft. |
| `cedar_present` | Any accepted species component includes Cw or Cy above a reviewed percent threshold. | Catch mixed stands where cedar is not leading but may matter for products or culture. | Review required; first candidate threshold should be `>= 20%` component share. |
| `old_cedar` | Cedar-leading or cedar-present stand above a reviewed age threshold. | Approximate old-growth cedar reporting where direct monumental cedar inventory is unavailable. | Review required; first candidate threshold should use age class 8 / `>= 141 years` to align with MP10 age-class reporting. |
| `large_cedar_proxy` | Cedar-leading or cedar-present stand above reviewed diameter/height proxy thresholds if source fields are available. | Proxy for monumental/pole-quality candidates and cultural-cedar availability. | Review required; do not accept until field availability is confirmed. |
| `cedar_cultural_reserve_context` | Cedar signal intersecting non-THLB, reserve, or otherwise unmanaged landbase context. | Report likely cultural cedar availability outside scheduled timber production. | Draft; should be reporting/accounting first, not a new THLB exclusion. |
| `cedar_harvest_candidate` | Cedar signal inside accepted THLB and eligible managed area. | Report where cedar supply may enter harvest scheduling. | Draft; depends on Phase 4 managed/unmanaged/origin assignment. |

## Cultural Reserve Design

The base teaching model should not create a new hidden THLB exclusion for
cultural cedar. Phase 2 already applies the MP10 cultural heritage resources
fallback as part of THLB netdown.

For P3.1, cultural cedar should be represented as:

- a reporting/accounting signal for old/large cedar context;
- a scenario constraint candidate that can limit or reserve portions of
  cedar-relevant managed area; and
- a discussion surface for students to compare timber value against cultural
  availability.

Accepted first behavior:

- no additional base-case THLB deduction;
- no automatic exclusion of all old cedar from harvest eligibility;
- report cedar availability both inside and outside THLB; and
- leave scenario-specific cedar reserve targets for later model-design review.

## Utility-Pole Product Design

Utility-pole-grade cedar should be treated as a product/reporting design lane,
not as a source-layer extraction step.

Minimum first-bundle requirements:

- cedar species signal;
- old/large proxy or explicit diameter/height fields if available;
- managed/unmanaged treatment eligibility;
- natural/treated curve provenance;
- cedar volume by analysis unit or curve group; and
- a product/account surface that can distinguish generic cedar volume from
  candidate high-value utility-pole potential.

Open review questions for P3.1b/P3.1c:

- Which diameter, height, age, or volume thresholds are defensible as a first
  utility-pole proxy?
- Should utility-pole potential be reported as a product, a feature/account, or
  both?
- Should the first base model constrain harvest of utility-pole candidates, or
  only report their scheduled and residual quantities?

## Treatment and Yield Implications

Treatment assumptions should stay separate from source extraction:

- fertilization response for redcedar was modeled historically through
  productivity-group uplift, but the first teaching model should not silently
  hard-code that as a new cedar treatment without review;
- genetically improved cedar stock is relevant for managed-origin curve
  assumptions, but managed-origin and treated-origin semantics must remain
  distinct; and
- cedar-specific treatment variants should be explicit scenario alternatives,
  not implicit edits to base THLB or source-layer status.

P3.1c should define whether the first bundle needs:

- cedar-specific products only;
- cedar-specific accounts/reports only;
- cedar-specific treatment eligibility;
- cedar-specific yield-curve groupings; or
- all of the above.

## Patchworks-Facing Requirements

The first model-input bundle should preserve enough fields to build these
Patchworks-facing surfaces later:

| Surface | Minimum requirement |
| --- | --- |
| Feature/account | Area by cedar-leading, Cw-leading, Cy-leading, cedar-present, old cedar, and cedar cultural reserve context. |
| Product | Generic harvested cedar volume plus a provisional utility-pole candidate product or reporting class if reviewed thresholds are available. |
| Target/report | Residual old/large cedar context, scheduled cedar volume, and cedar harvest versus reserve tradeoff reports. |
| Treatment hook | Optional cedar-oriented treatment family, only after P3.1c accepts a teaching treatment design. |
| QA | Source species-area shares must be compared against MP10 forest-cover shares before accepting the first bundle. |

## P3.1a Decision Boundary

P3.1a accepts only the evidence base and first design questions. It does not
lock source fields, thresholds, products, targets, or treatments.

P3.1b should verify the exact R1/VDYP fields and candidate thresholds for the
cedar signals. P3.1c should turn the accepted signals into explicit
Patchworks-facing product/account/report requirements.
