# CardHouse roadmap

## Goal

Turn the former Bicyclious implementation into a reusable CardHouse Hugo theme
for wiki-like topics and supporting blog posts. Unify topic lists, taxonomy
results, and topic detail pages around one focal-aware image identity and one
image-first card system, while retaining a separate editorial homepage hero
carousel that can select arbitrary page-bundle images.

## Current implementation status

The initial modularization and View Transition implementation are complete in
`.worktrees/cardhouse` on the `codex/cardhouse-theme` branch. The Padonma
repository is the first consumer and build fixture. The module lives at
`themes/cardhouse/`.

Primary implementation locations:

- `themes/cardhouse/layouts/_partials/hero-resource.html` — canonical resource
  resolution and migration fallbacks.
- `themes/cardhouse/layouts/_partials/hero-image.html` — focal-aware responsive
  image renderer and stable identity hook.
- `themes/cardhouse/layouts/_partials/view-transition-name.html` — matching,
  filename-safe CSS transition identifiers.
- `themes/cardhouse/layouts/_partials/topic-card.html` — shared image-first card.
- `themes/cardhouse/layouts/_partials/hero-carousel.html` — homepage editorial
  carousel with per-slide image and focal selection.
- `themes/cardhouse/layouts/_partials/topic-gallery.html` — full topic image
  carousel, canonical transition destination, thumbnails, and lightbox.
- `themes/cardhouse/layouts/topics/single.html` — full topic gallery followed
  by the topic heading and wiki content.
- `themes/cardhouse/assets/css/main.css` — card, hero, glass, gallery, and
  responsive rules.
- `themes/cardhouse/layouts/home.html` — parameterized consumer homepage.
- `themes/cardhouse/layouts/section.html`, `taxonomy.html`, and `term.html` —
  generated shared-card lists.

## Phase 1 — module and language migration

1. Rename `themes/bicyclious` to `themes/cardhouse` and update the consumer's
   Hugo configuration.
2. Remove bicycle, build, price, sold-state, inventory, and purchase concepts
   from active templates and styles.
3. Replace project-specific CSS tokens and selectors with semantic CardHouse
   names.
4. Parameterize Padonma-specific homepage identity so the theme does not
   contain consumer names or asset paths.
5. Remove obsolete branded assets that are not part of the reusable module.

**Exit criterion:** the theme directory and active source are understandable
without bicycle-commerce or Padonma context.

## Phase 2 — canonical topic image foundation

1. Implement the `hero` frontmatter contract.
2. Resolve explicit `hero.image`, then a first-image fallback.
3. Apply independently defaulted focal coordinates and accessible alt text.
4. Generate responsive WebP derivatives without enlarging source images.
5. Emit the same stable `data-topic-id` in every topic-image context.

**Exit criterion:** one topic image and focal decision render predictably in
cards and as the canonical first image in topic galleries.

## Phase 3 — shared cards and list migration

1. Rebuild `topic-card.html` around `hero-image.html`.
2. Limit overlays to a title and optional short topic classification.
3. Standardize the dark glass treatment.
4. Route section, topic, taxonomy, and term results through the shared card.
5. Validate the authoritative three/two/one-column responsive grid.

**Exit criterion:** all topic-like lists share one card structure and one CSS
system, including useful missing-image behavior.

## Phase 4 — topic detail and full image gallery

1. Start image-bearing topic pages with a full gallery whose first active image
   is the same canonical image used by their cards.
2. Preserve long-form Markdown as the topic's primary knowledge content.
3. Keep supporting images in the same gallery after the canonical image.
4. Open the exact clicked gallery image in the lightbox.
5. Loop the main gallery and lightbox continuously without endpoint jumps or
   blank regions.
6. Avoid requiring images for text-first topics.

**Exit criterion:** a topic begins on its canonical image, supports stable
continuous browsing through every image, and then reveals the wiki content.

## Phase 5 — blog integration

1. Add a dedicated post list layout when substantive posts exist.
2. Allow posts to opt into the shared hero contract and card renderer.
3. Keep post dates and narrative metadata subordinate to imagery on list views.
4. Establish explicit links from posts into the topic knowledge base without
   conflating the two content types.

**Exit criterion:** the blog can visually participate in CardHouse while topics
remain the durable information architecture.

## Phase 6 — cross-document View Transitions (complete)

1. Generate one matching, filename-safe `view-transition-name` for each
   canonical topic card and canonical first topic-gallery image.
2. Opt into cross-document navigation with `@view-transition`.
3. Animate named groups over 750ms while fading page roots.
4. Honor `prefers-reduced-motion` with an effectively instant transition and no
   root fades.
5. Keep arbitrary homepage hero-carousel slides outside the canonical
   transition identity.
6. Validate the served HTML, generated names, animation rules, and live
   card-to-topic behavior.

**Exit criterion:** canonical card-to-topic navigation expands the matching
image with progressive enhancement and reduced-motion support.

## Phase 7 — standalone extraction (optional future work)

1. Add module installation documentation once the eventual standalone Git
   repository path is known.
2. Extract or subtree the `themes/cardhouse` directory into that repository,
   then consume it from Padonma as a Hugo Module or Git submodule.

**Exit criterion:** CardHouse can be versioned and consumed independently
without copying Padonma-specific files.

## Completion checklist for this branch

- [x] CardHouse modularization plan documented before source changes.
- [x] Theme renamed and consumer configuration updated.
- [x] Commerce and bicycle assumptions removed from active theme source.
- [x] Canonical hero resolver and renderer added.
- [x] Homepage hero carousel supports arbitrary page-bundle images and focal
      points independently of canonical topic heroes.
- [x] Section, taxonomy, and term lists use the shared topic card.
- [x] Topic detail pages use canonical heroes when images exist.
- [x] Topic pages restore the full image gallery with the canonical hero first.
- [x] Main topic galleries and lightboxes loop continuously and open the exact
      clicked image.
- [x] Canonical cards and topic galleries use matching View Transition names.
- [x] Cross-document transition animation and reduced-motion behavior are
      implemented and browser-verified.
- [x] Padonma homepage identity moved to consumer parameters.
- [x] Hugo production build passes after final cleanup.
- [x] Generated homepage, topic list, and representative topic pages receive
      visual review at desktop and mobile widths.
- [x] Final active-source audit finds no old theme/domain vocabulary.
