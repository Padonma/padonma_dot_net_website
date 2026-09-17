# Modularizing Bicyclious as Cardhaus

## Purpose

Cardhaus is a portable Hugo theme for image-first collections of knowledge.
Its primary content object is a **topic**: a durable, wiki-like page that can
combine a canonical hero image, supporting images, and long-form reference
content. Blog posts can extend and point into that topic collection, but they
do not define the theme's information model.

This work began with the existing Bicyclious theme, removed its bicycle shop
and build-specific assumptions, and produced the independent
`themes/cardhaus` module. The Padonma site remains the first consumer and the
integration test for the module.


## Module boundary

The reusable module lives entirely under `themes/cardhaus/`. It owns:

- shared Hugo layouts and partials;
- the focal-aware hero-image renderer;
- topic cards and responsive card grids;
- Markdown shortcodes for individual and curated topic cards;
- topic detail presentation and image galleries;
- shared site chrome and Cardhaus design tokens;
- theme-provided static assets.

The consuming site continues to own:

- content under `content/`;
- site identity and navigation in `hugo.toml`;
- site-specific images under `assets/` and page bundles;
- bundle-owned hero-carousel data in `content/.../carousel.yaml`;
- Padonma-specific copy and branding.


## Topic image contract

Each topic may declare one canonical image:

```yaml
hero:
  image: "filename.jpg"
  focal:
    x: 0.5
    "y": 0.35
  alt: "A useful description of the image"
```

- `hero.image` names an image in the topic's page bundle.
- `hero.focal.x` and `hero.focal.y` are optional values from 0 through 1.
- Each missing focal coordinate defaults independently to `0.5`.
- `hero.alt` is optional; the topic title is the fallback.
- Topics without a configured or available image receive a deliberate
  image-missing state rather than a broken image.


## Shared rendering model

All topic cards and topic-page heroes use a central
`layouts/_partials/hero-image.html` renderer. It is responsible for resolving
the canonical resource, applying focal cropping, producing responsive image
derivatives where possible, providing stable topic identity attributes, and
rendering the missing-image state.

`layouts/_partials/topic-card.html` provides the shared image-first card. The
card contains the canonical topic image and a restrained glass overlay with the
topic title, optional short summary, and optional secondary label. Supporting
copy must remain subordinate and must not turn the card into a conventional
text-summary box.

Markdown authors may reuse that exact renderer through the `topic-card`
shortcode or group references in a paired `topic-card-grid` shortcode. The grid
may provide a heading and introductory Markdown but does not override a topic's
canonical image or card metadata.

The same topic identity is preserved across homepage cards, topic indexes,
taxonomy results, and the canonical image at the start of each topic gallery.
Cardhaus assigns a matching, filename-safe `view-transition-name` to those
images and opts into cross-document navigation with `@view-transition`. The
named image expands over 750ms while the old and new page roots fade. Reduced
motion preferences reduce that animation to effectively instantaneous.

Arbitrary homepage hero-carousel slides remain outside the named transition
identity. Homepage topic cards still participate because they use the canonical
topic hero.

## Page behavior

### Homepage

The homepage `hero-carousel.html` component is an editorial exception to the
canonical topic-image rule. Each slide may choose any image from the linked
topic's page bundle, with its own focal point and alt text in the current
branch bundle's `carousel.yaml` page resource (`content/carousel.yaml` for the
homepage). Slides display only the image—no title, caption, or glass overlay.
The slide still links to the topic, but it does not claim to be that topic's
canonical visual identity. Homepage topic previews below it use the shared card
grid and canonical topic-card partial.

### Topic indexes and taxonomies

Topic list, generic section, taxonomy, and term pages use the same card markup
and responsive grid. The intended grid is three columns on desktop, two on
tablet, and one on mobile.

### Topic detail

An image-bearing topic begins with the full page-bundle image gallery. The
canonical hero is ordered first, starts active, and carries the transition name
that matches the topic card. Per-image focal coordinates take precedence; each
missing coordinate on the canonical image falls back independently to
`hero.focal` and then to the centered default. Its alt text likewise uses
`hero.alt` before the topic title. Supporting images follow in the same
carousel. Clicking any visible slide opens that exact image in the lightbox;
the main gallery and lightbox loop continuously in both directions. The
conventional topic title and long-form wiki content follow the gallery.

### Blog posts

Posts are narrative additions to the knowledge base. Their list presentation
may use the same image-first card system and hero contract, but topic semantics
and topic navigation remain distinct. Cardhaus should not require posts to
exist.

## Naming migration

The module directory becomes `themes/cardhaus`, the consumer changes to
`theme = "cardhaus"`, and theme metadata identifies the module as Cardhaus.
Reusable CSS classes, JavaScript selectors, template names, comments, and
variables are renamed away from `bike`, `build`, and `bicyclious` terminology.
Site-specific legacy parameter names may receive short compatibility fallbacks
only when needed to keep the migration buildable.

The old `themes/bicyclious` directory is removed from this branch after its
contents have been migrated. Git history retains the original source.

## Implementation sequence

1. Copy and rename the theme boundary to `themes/cardhaus`, then point the
   Padonma consumer at it.
2. Introduce Cardhaus metadata, neutral design tokens, selectors, and template
   names while preserving current site behavior.
3. Add the canonical focal-aware hero-image partial.
4. Rebuild topic cards, section/taxonomy results, and responsive grids around
   the shared renderer.
5. Place the shared canonical hero first in each full topic gallery without
   disrupting long-form content or supporting images.
6. Assign matching cross-document View Transition names to canonical card and
   topic-gallery images, including reduced-motion behavior.
7. Restore the full topic image carousel with the canonical hero first and
   preserve exact-image lightbox targeting and continuous looping.
8. Update the former Bicyclious design specification and roadmap to describe
   Cardhaus topics rather than bicycles and builds.
9. Run Hugo's production build, inspect warnings and generated routes, and
   review the final branch diff for bicycle-specific remnants.

## Validation criteria

- Hugo builds successfully with `theme = "cardhaus"`.
- `themes/cardhaus` can be understood without Padonma or bicycle domain
  knowledge.
- No active reusable template or style uses bike/build/price/sold concepts.
- A configured hero image and focal point render consistently in cards and on
  topic detail pages.
- Existing topics without explicit hero data continue to render gracefully.
- Homepage, topic lists, taxonomies, and terms share one card system.
- The desktop, tablet, and mobile card layouts remain usable.
- Canonical topic cards and the first topic-gallery image receive identical,
  valid `view-transition-name` values.
- Cross-document transitions use the implemented 750ms animation and honor
  `prefers-reduced-motion`.
- Topic galleries start on the canonical image, open the exact clicked image,
  and loop continuously without blank gaps.
- The old Bicyclious theme directory is absent from the completed branch.

## Post-migration status

Phases 1–4 and 6–7 are implemented, and the production build currently
succeeds. Phase 5 remains intentionally deferred until the site has a
substantive post collection. Standalone extraction also remains optional.

The final module-boundary and hero-contract audit identified two cleanup items.
The gallery item is now complete:

- [x] Make the canonical gallery image consume `hero.focal` and `hero.alt`,
  while retaining per-supporting-image focal data where needed.
- [ ] Remove the hard-coded `brand/checkerboard.png` lookup from `baseof.html` and
  make the header markup unconditional and structurally valid.

These are focused conformance fixes, not reasons to reopen the completed
migration or change the topic-centered plan.
