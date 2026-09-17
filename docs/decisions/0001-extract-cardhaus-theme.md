# Decision 0001: extract Cardhaus from the former Bicyclious theme

Status: accepted

## Context

The original theme mixed reusable image-first presentation with bicycle-shop,
build, commerce, and Padonma-specific assumptions. Padonma needed a topic-centered
knowledge model whose durable objects could combine a canonical image, supporting
gallery, and long-form reference content.

## Decision

The reusable implementation was renamed and moved to `themes/cardhaus/`.
Bicycle, build, price, inventory, purchase, and consumer-brand assumptions were
removed from active theme source. Padonma became the first consumer and its
content, navigation, assets, and identity remained outside the theme.

One focal-aware canonical hero resolver and one topic-card renderer now serve
lists, embedded cards, and topic detail. Topic galleries place the canonical
image first; matching named View Transitions preserve visual identity. The
homepage/branch hero carousel remains an editorial exception and may select a
different image. Supporting galleries, continuous lightboxes, shared responsive
grids, and author-facing card shortcodes were retained as reusable features.

## Consequences

Theme contracts are now maintained in `themes/cardhaus/SPEC.md`, while Padonma
decides which features to use. The old Bicyclious source and duplicate migration
plans are unnecessary; Git history preserves them. A standalone Cardhaus
repository remains optional until another consumer or versioning need justifies
the distribution overhead.
