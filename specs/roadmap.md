# Cardhaus roadmap

## Goal

Turn the former Bicyclious implementation into a reusable Cardhaus Hugo theme
for wiki-like topics and supporting blog posts. Unify topic lists, taxonomy
results, and topic detail pages around one focal-aware image identity and one
image-first card system, while retaining a separate editorial homepage hero
carousel that can select arbitrary page-bundle images.

## Current implementation status

The initial modularization, gallery, shortcode, and View Transition work is
integrated on `master`. The Padonma repository is the first consumer and build
fixture, and the module lives at `themes/cardhaus/`. A production build passes;
the remaining work is a small conformance pass plus intentionally deferred blog
and extraction work.

Primary implementation locations:

- `themes/cardhaus/layouts/_partials/hero-resource.html` — canonical resource
  resolution and migration fallbacks.
- `themes/cardhaus/layouts/_partials/hero-image.html` — focal-aware responsive
  image renderer and stable identity hook.
- `themes/cardhaus/layouts/_partials/view-transition-name.html` — matching,
  filename-safe CSS transition identifiers.
- `themes/cardhaus/layouts/_partials/topic-card.html` — shared image-first card.
- `themes/cardhaus/layouts/_partials/hero-carousel.html` — homepage editorial
  carousel with per-slide image and focal selection.
- `themes/cardhaus/layouts/_partials/topic-gallery.html` — full topic image
  carousel, canonical transition destination, thumbnails, and lightbox.
- `themes/cardhaus/layouts/topics/single.html` — full topic gallery followed
  by the topic heading and wiki content.
- `themes/cardhaus/assets/css/` — responsibility-based card, hero, glass,
  gallery, and responsive rules bundled by the base template.
- `themes/cardhaus/layouts/home.html` — parameterized consumer homepage.
- `themes/cardhaus/layouts/section.html`, `taxonomy.html`, and `term.html` —
  generated shared-card lists.

## Phase 1 — module and language migration

1. Rename `themes/bicyclious` to `themes/cardhaus` and update the consumer's
   Hugo configuration.
2. Remove bicycle, build, price, sold-state, inventory, and purchase concepts
   from active templates and styles.
3. Replace project-specific CSS tokens and selectors with semantic Cardhaus
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
2. Limit overlays to a title, optional short summary, and optional topic
   classification.
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

**Exit criterion:** the blog can visually participate in Cardhaus while topics
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

## Phase 7 — embedded topic cards (complete)

1. Add a `topic-card` shortcode that resolves an absolute content reference
   and delegates to the shared card partial.
2. Add a paired `topic-card-grid` shortcode with an optional heading and
   Markdown introduction.
3. Keep shortcode cards on the canonical image, summary, metadata, and View
   Transition contract without adding per-embed overrides.
4. Make embedded grids responsive to their content width and isolate card
   presentation from broad Markdown prose styles.
5. Fail the Hugo build for missing or unresolved topic references.

**Exit criterion:** authors can place one canonical topic card or a curated,
responsive group in Markdown without creating a second card implementation.

## Phase 8 — standalone extraction (optional future work)

1. Add module installation documentation once the eventual standalone Git
   repository path is known.
2. Extract or subtree the `themes/cardhaus` directory into that repository,
   then consume it from Padonma as a Hugo Module or Git submodule.

**Exit criterion:** Cardhaus can be versioned and consumed independently
without copying Padonma-specific files.

## Phase 9 — conformance cleanup (in progress)

1. [x] Apply `hero.focal` to the canonical first gallery image and use
   `hero.alt` for its alternative text.
2. [x] Preserve optional focal metadata for supporting gallery images without
   creating a second canonical-image contract. Explicit per-image coordinates
   take precedence; missing canonical coordinates fall back independently to
   the topic hero values.
3. Remove the hard-coded `brand/checkerboard.png` lookup from `baseof.html` and
   ensure the header element is always opened and closed correctly.
4. Add a representative shortcode use to content or a build fixture so Hugo's
   unused-template report exercises both shortcode templates.
5. [x] Re-run the production build and verify the generated canonical crop on a
   topic whose `hero.focal` is not centered.

**Exit criterion:** the implementation fully matches the documented hero and
module-boundary contracts, and the build exercises the author-facing shortcode
surface.

## Recommended plan

Do not reopen the migration or prioritize standalone extraction yet. Complete
Phase 9 as a narrow hardening pass. Then choose between content work and Phase
5 based on whether posts have become a real editorial need. Extract Cardhaus
only after its repository path, versioning policy, and consumption mechanism
are known.

## Implementation checklist

- [x] Cardhaus modularization plan documented before source changes.
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
- [x] Hugo production build passes with the current implementation.
- [x] Generated homepage, topic list, and representative topic pages receive
      visual review at desktop and mobile widths.
- [ ] Final module-boundary audit is clean; the remaining hard-coded
      `brand/checkerboard.png` lookup must be removed.
- [x] Markdown content can embed shared topic cards individually or in a
      curated responsive grid with introductory prose.
- [x] Canonical gallery imagery consumes the same `hero.focal` and `hero.alt`
      values as cards.
- [ ] A content fixture exercises both topic-card shortcodes during validation.
