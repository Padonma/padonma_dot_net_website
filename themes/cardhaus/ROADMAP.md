# Cardhaus roadmap

Only unfinished reusable-theme work belongs here. Stable behavior is specified
in `SPEC.md`; current installation and authoring instructions are in `README.md`.

## Conformance cleanup

- Remove the hard-coded `brand/checkerboard.png` lookup from `baseof.html` and
  make the header open and close unconditionally with no consumer asset path.
- Make an explicitly configured but missing hero image fail with actionable page
  context instead of silently falling back to a different bundle image.

## Reusable image and content rendering

- Define and implement page-resource metadata precedence for supporting-image
  alt text, captions, credits, focal points, ordering, and gallery exclusion.
- Add Markdown image and internal-link render hooks after behavior for raster
  images, SVG, animation, QR diagrams, remote URLs, fragments, and downloads is
  settled. Preserve linked-image semantics and do not download remote resources.
- Add focused validation for focal ranges, carousel targets, and image types.

## Maintainability

- Move the inline carousel and gallery JavaScript from `baseof.html` into a
  fingerprinted Hugo Pipes asset without changing navigation, synchronization,
  decoding, or lightbox behavior. Load it only on pages that need it once
  component presence has one reliable definition.
- Add dedicated post-list presentation if a consumer develops a substantive
  post collection. Posts may opt into the hero and card contracts without
  changing topic semantics.
- Extract Cardhaus to a standalone versioned repository only when a second
  consumer or distribution requirement establishes the module URL and release
  policy. Add Hugo Module installation instructions at that time.
