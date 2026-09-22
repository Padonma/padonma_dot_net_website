# Carousel Deep-Link Regression Fix

## Status

Implemented. Repository-wide content and rendered-output checks live in
`scripts/validate-carousel-handoffs.py` and `tests/test_carousel_handoffs.py`.
The renderer continues to emit `link` unchanged, so ordinary fragmentless links
retain their existing navigation behavior.

## Problem

The carousel-unification work made `hero-carousel.html` the renderer for home,
branch, and leaf carousels. A destination carousel can initialize at a selected
slide when the page URL contains a fragment matching that slide's `hash`.

Navigation from the homepage carousel to a topic currently fails to select the
corresponding non-hero slide in most cases. The destination topic loads, but its
carousel opens at the first slide instead of the image selected on the source
page.

For example, the homepage entry currently resembles:

```yaml
- image: /topics/lotus-fiber/companies/loro-piana/loro_pianan_jacket_full.jpg
  hash: loro-piana-jacket-full
  link: /topics/lotus-fiber/companies/loro-piana/
  alt: Loro Piana Lotus Jacket
```

The corresponding destination slide uses:

```yaml
- image: loro_pianan_jacket_full.jpg
  hash: loro-pianan-jacket-full
  alt: Loro Piana
```

The source link contains no fragment, and its `hash` differs from the
destination hash. The destination therefore has no usable slide selection.

The confirmed working URL is:

```text
/topics/lotus-fiber/companies/loro-piana/#loro-pianan-jacket-full
```

## Root Cause

The JavaScript initialization path is functioning as designed:

1. It reads `window.location.hash`.
2. It searches the rendered slides for an exact matching `data-hash`.
3. It passes that slide's index to Swiper as `initialSlide`.
4. If no exact match exists, it selects index zero and allows normal autoplay.

A known-valid deep link to the Bandgrind carousel was verified to initialize at
the requested slide. The regression is therefore not caused by Swiper timing or
index calculation.

The failure is in the source-to-destination content contract:

- `hero-carousel.html` emits a slide's `link` unchanged.
- It does not append the slide's `hash` to that link.
- Most homepage entries use fragmentless links to newly generated leaf
  carousels.
- Most corresponding leaf slides have filename-derived hashes that differ from
  the editorial hashes in the homepage carousel.

The existing contract already requires a carousel-to-carousel handoff link to
name the destination page and fragment explicitly. The source and destination
entries should use the same stable hash for the shared image.

## Required Behavior

When a source carousel slide links to an image represented in a destination
carousel:

1. The source and destination entries must use the same `hash` for that image.
2. The source entry's `link` must include that hash as its fragment.
3. Following the link must initialize the destination carousel at that slide.
4. Arrival through a valid fragment must stop autoplay so the requested slide
   remains selected.
5. The clicked source image and selected destination image must remain eligible
   for the existing carousel handoff view transition.

Ordinary links that are not carousel handoffs must retain their current
behavior. The renderer must not automatically add a fragment to every `link`.

## Implementation

### 1. Normalize shared hashes

For every homepage carousel entry whose image also appears in the linked
destination carousel, choose one stable hash and use it in both carousel files.

Prefer the destination's existing filename-derived hash unless there is a
compatibility reason to preserve a published source hash. This minimizes edits
to generated leaf carousel files and preserves already usable destination URLs.

For the example above, update the homepage entry to:

```yaml
- image: /topics/lotus-fiber/companies/loro-piana/loro_pianan_jacket_full.jpg
  hash: loro-pianan-jacket-full
  link: /topics/lotus-fiber/companies/loro-piana/#loro-pianan-jacket-full
  alt: Loro Piana Lotus Jacket
```

Audit every internal homepage carousel link. Known mismatches found during
diagnosis include:

| Source hash | Destination hash |
| --- | --- |
| `loro-piana-jacket-full` | `loro-pianan-jacket-full` |
| `samatoa-fiber-extraction` | `fiber-extraction` |
| `inle-lotus-weaver` | `weaver-at-loom-in-inle` |
| `loro-piana-jacket-detail` | `loro-pianan-jacket-detail` |
| `ma-su-weaving` | `ma-su` |
| `samatoa-short-dress` | `short-dress-close-up` |
| `hope-lotus-hat` | `hat` |

This table is diagnostic input, not a substitute for a complete audit. Match
entries by resolved image identity and verify the current destination data
before editing.

### 2. Add explicit destination fragments

For each carousel-to-carousel handoff, change the source `link` from:

```yaml
link: /destination/page/
```

to:

```yaml
link: /destination/page/#shared-hash
```

Do not add fragments to links whose destination has no carousel or whose
intended behavior is ordinary page navigation.

### 3. Preserve renderer semantics

Do not change `hero-carousel.html` to concatenate `.link` and `.hash`
automatically.

The `hash` identifies a slide in the current carousel. The `link` defines an
activation destination and may intentionally be an ordinary internal or
external URL. Automatically combining them would conflate these independent
fields, change existing link behavior, and still produce invalid deep links
where source and destination hashes differ.

The existing build-time validation in `carousel-slide-data.html` should
continue to validate same-site links that already contain fragments. Once the
content links have explicit fragments, this validation will reject links whose
fragment is absent from the destination carousel.

## Validation and Regression Coverage

The implementation adds coverage beyond the generator unit tests. The content
validator reports every handoff violation in one run; the integration test builds
Hugo into a temporary destination and validates the rendered anchors and
destination `data-hash` values.

### Content integrity test

The validation script inspects image-preserving carousel-to-carousel links and
asserts that:

- the destination page exists;
- the destination contains `carousel.yaml`;
- the link contains a non-empty fragment;
- exactly one destination entry has a matching `hash`;
- the source and destination entries refer to the same underlying image; and
- the shared image uses the same `hash` in both entries.

Report all violations in one run so content authors can correct the complete
set rather than discovering failures one build at a time.

### Rendered integration test

Build the Hugo site and verify that each carousel-to-carousel source anchor:

- renders an `href` containing the intended destination fragment; and
- has a fragment present in the destination page's rendered `data-hash` set.

### Browser behavior test

At minimum, exercise one non-first destination slide:

1. Load the source page.
2. Activate the source slide link.
3. Confirm that the destination URL retains the fragment.
4. Confirm that `.swiper-slide-active` has the expected `data-hash`.
5. Wait longer than the autoplay delay and confirm that the active hash has not
   changed.

Also retain or add a control case showing that a fragmentless ordinary link
opens the destination at its normal first slide.

## Acceptance Criteria

- Every intended carousel-to-carousel handoff link contains an explicit
  fragment.
- Each handoff fragment exactly matches one destination carousel hash.
- Source and destination entries for the shared image use the same hash.
- Clicking a homepage non-hero image opens its topic with that image active.
- A deep-linked slide remains active rather than advancing automatically.
- Existing first-slide/hero entry behavior remains unchanged.
- Existing external and ordinary fragmentless links remain unchanged.
- Hugo builds without carousel-link validation errors.
- Automated coverage fails if a handoff fragment is removed or renamed on only
  one side.

## Non-Goals

- Replacing Swiper or changing carousel layout.
- Changing URL fragments during unrelated ordinary navigation.
- Automatically deriving activation destinations in the renderer.
- Regenerating all leaf carousels solely to repair this regression.
- Redesigning the carousel YAML schema.

## Likely Files Changed

- `content/carousel.yaml`
- Any destination `carousel.yaml` whose hash is deliberately normalized instead
  of preserving its current value
- A new content-integrity or rendered integration test
- Test documentation if a new validation command is introduced

No JavaScript change should be necessary unless testing uncovers a separate
failure after all links and hashes satisfy this contract.
