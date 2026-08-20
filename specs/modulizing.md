# Modularizing Bicyclious as CardHouse

## Purpose

CardHouse is a portable Hugo theme for image-first collections of knowledge.
Its primary content object is a **topic**: a durable, wiki-like page that can
combine a canonical hero image, supporting images, and long-form reference
content. Blog posts can extend and point into that topic collection, but they
do not define the theme's information model.

This work begins with the existing Bicyclious theme, removes its bicycle shop
and build-specific assumptions, and develops the result as the independent
`themes/cardhouse` module. The Padonma site is the first consumer and the
integration test for the module.

## Repository and branch strategy

Development happens in the isolated worktree at `.worktrees/cardhouse` on the
`codex/cardhouse-theme` branch. The worktree starts from commit `df3fd4b`, which
contains the latest committed Bicyclious theme updates. Existing uncommitted
work in the main Padonma worktree is intentionally not copied into this branch.

## Module boundary

The reusable module lives entirely under `themes/cardhouse/`. It owns:

- shared Hugo layouts and partials;
- the focal-aware hero-image renderer;
- topic cards and responsive card grids;
- topic detail presentation and image galleries;
- shared site chrome and CardHouse design tokens;
- theme-provided static assets.

The consuming site continues to own:

- content under `content/`;
- site identity and navigation in `hugo.toml`;
- site-specific images under `assets/` and page bundles;
- homepage hero-carousel data in `data/carousel.yaml`;
- Padonma-specific copy and branding.

CardHouse must not hard-code Padonma, bicycle, build, price, inventory, or
`SOLD` semantics into its reusable templates. A consumer may add those concepts
through content data or later extension points, but they are not part of the
core topic model.

## Topic image contract

Each topic may declare one canonical image:

```yaml
hero:
  image: "filename.jpg"
  focal:
    x: 0.5
    y: 0.35
  alt: "A useful description of the image"
```

- `hero.image` names an image in the topic's page bundle.
- `hero.focal.x` and `hero.focal.y` are optional values from 0 through 1.
- Each missing focal coordinate defaults independently to `0.5`.
- `hero.alt` is optional; the topic title is the fallback.
- Topics without a configured or available image receive a deliberate
  image-missing state rather than a broken image.

During migration, the renderer may fall back to the first page-bundle image so
existing topics remain usable. New and updated content should use explicit
`hero` data because filesystem ordering is not a durable editorial decision.

## Shared rendering model

All topic cards and topic-page heroes use a central
`layouts/_partials/hero-image.html` renderer. It is responsible for resolving
the canonical resource, applying focal cropping, producing responsive image
derivatives where possible, providing stable topic identity attributes, and
rendering the missing-image state.

`layouts/_partials/topic-card.html` provides the shared image-first card. The
card contains the canonical topic image and a restrained glass overlay with the
topic title. Optional secondary labeling must remain subordinate and must not
turn the card into a conventional text-summary box.

The same topic identity is preserved across homepage cards, topic indexes,
taxonomy results, and topic-page heroes. This prepares the theme for a later
View Transitions implementation in which navigation reads as zooming into the
topic rather than replacing one unrelated layout with another.

## Page behavior

### Homepage

The homepage `hero-carousel.html` component is an editorial exception to the
canonical topic-image rule. Each slide may choose any image from the linked
topic's page bundle, with its own focal point and alt text in
`data/carousel.yaml`. Slides display only the image—no title, caption, or glass
overlay. The slide still links to the topic, but it does not claim to be that
topic's canonical visual identity. Homepage topic previews below it use the
shared card grid and canonical topic-card partial.

### Topic indexes and taxonomies

Topic list, generic section, taxonomy, and term pages use the same card markup
and responsive grid. The intended grid is three columns on desktop, two on
tablet, and one on mobile.

### Topic detail

A topic page begins with the canonical topic hero when one is available, with
its title presented as part of the hero treatment. Long-form wiki content
follows. Supporting page-bundle images may continue to appear in the topic
gallery, but the canonical hero remains the topic's stable visual identity.

### Blog posts

Posts are narrative additions to the knowledge base. Their list presentation
may use the same image-first card system and hero contract, but topic semantics
and topic navigation remain distinct. CardHouse should not require posts to
exist.

## Naming migration

The module directory becomes `themes/cardhouse`, the consumer changes to
`theme = "cardhouse"`, and theme metadata identifies the module as CardHouse.
Reusable CSS classes, JavaScript selectors, template names, comments, and
variables are renamed away from `bike`, `build`, and `bicyclious` terminology.
Site-specific legacy parameter names may receive short compatibility fallbacks
only when needed to keep the migration buildable.

The old `themes/bicyclious` directory is removed from this branch after its
contents have been migrated. Git history retains the original source.

## Implementation sequence

1. Copy and rename the theme boundary to `themes/cardhouse`, then point the
   Padonma consumer at it.
2. Introduce CardHouse metadata, neutral design tokens, selectors, and template
   names while preserving current site behavior.
3. Add the canonical focal-aware hero-image partial.
4. Rebuild topic cards, section/taxonomy results, and responsive grids around
   the shared renderer.
5. Add the shared canonical hero to topic detail pages without disrupting
   their long-form content and supporting galleries.
6. Update the former Bicyclious design specification and roadmap to describe
   CardHouse topics rather than bicycles and builds.
7. Run Hugo's production build, inspect warnings and generated routes, and
   review the final branch diff for bicycle-specific remnants.

## Validation criteria

- Hugo builds successfully with `theme = "cardhouse"`.
- `themes/cardhouse` can be understood without Padonma or bicycle domain
  knowledge.
- No active reusable template or style uses bike/build/price/sold concepts.
- A configured hero image and focal point render consistently in cards and on
  topic detail pages.
- Existing topics without explicit hero data continue to render gracefully.
- Homepage, topic lists, taxonomies, and terms share one card system.
- The desktop, tablet, and mobile card layouts remain usable.
- The old Bicyclious theme directory is absent from the completed branch.
