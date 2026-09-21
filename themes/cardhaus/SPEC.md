# Cardhaus specification

## Purpose and boundary

Cardhaus is a reusable, image-first Hugo theme for topic-centered knowledge
sites. A topic is a durable reference page, not a product. The theme owns the
rendering contracts, components, design tokens, responsive behavior, navigation
chrome, metadata, and progressive enhancement shared by its consumers.

A consuming site owns its content hierarchy, vocabulary, editorial policy,
navigation entries, brand assets, deployment, URLs, redirects, and the choice of
which Cardhaus features to use. Cardhaus must not hard-code a consumer name,
subject domain, asset path, commerce state, inventory, or purchasing behavior.

Reusable source lives under `themes/cardhaus/`. Consumer content, configuration,
and assets live outside the theme.

## Canonical topic image

A page may select one canonical page-bundle image:

```yaml
hero:
  image: "filename.jpg"
  focal:
    x: 0.5
    "y": 0.35
  alt: "Accessible description"
```

`hero.image` is the durable editorial identity. Each focal coordinate is
optional, ranges from 0 through 1, and defaults independently to `0.5`.
`hero.alt` defaults to the page title. Quote `"y"` in YAML 1.1 front matter.

When `hero.image` is absent, the first compatible bundle image may be used.
A page without an image receives an intentional placeholder, not a broken image.
Explicit image names that cannot be resolved should fail validation rather than
quietly choose another image; this stricter behavior remains roadmap work.

`layouts/_partials/hero-resource.html` is the canonical resolver.
`hero-image.html` renders responsive derivatives, focal cropping, accessible
text, and stable topic identity. Gallery code uses the same resolver and places
the canonical resource first. Do not create a second card or detail-image
contract.

## Cards, grids, and child listings

`layouts/_partials/topic-card.html` is the only topic-list card. It contains the
canonical image or missing-image state and a restrained dark glass overlay with
the title, optional Hugo summary, and optional `topic_type`. The image remains
primary.

Cardhaus provides three author-facing shortcodes:

- `topic-card` embeds one card resolved from an absolute content reference.
- Paired `topic-card-grid` groups curated cards and may add a heading and
  introductory Markdown. Introductory content must precede all nested cards.
- `topic-card-children` lists a branch's immediate authored children in weight
  order. It defaults to the current branch and may accept an absolute branch
  reference and heading.

Unresolved references and structurally invalid shortcode use fail the build.
Shortcodes delegate to shared partials and cannot override a referenced topic's
image or card metadata. A canonical topic should appear only once per document,
because named View Transitions must be unique.

Generated section, taxonomy, and term lists use the same card. The structural
grid has three columns above the tablet breakpoint, two through tablet widths,
and one at mobile widths. Consumers may override `tablet` and `mobile` under
`params.cardhaus.breakpoints`; defaults are `1200px` and `850px`.

## Carousels and galleries

A branch bundle may supply `carousel.yaml`; the root bundle uses
`content/carousel.yaml`. Every slide requires an explicit `image`, stable
`hash`, and accessible `alt`. A relative image path resolves from the bundle
containing `carousel.yaml`; a site-root-relative image path resolves from the
page bundle named by that path. Both local forms use Hugo's responsive image
pipeline. Fully qualified HTTP(S) images remain remote and may supply `width`
and `height` to reserve their aspect ratio.
Slide-specific `focal` values control the crop. Slides contain no visible title
or caption.

An optional `link` navigates normally. A same-site carousel URL with a fragment
matching a destination hash focuses that slide and gives only the clicked and
destination images a coordinated view transition. The source and destination
carousel entries use the same `image` and `hash`; the source `link` names the
destination carousel URL plus that shared hash. Slides without `link` open the
complete image in a modal lightbox. Legacy `slug` input is a build error.

Carousel navigation uses complete clone sets before and after the originals so
centered, variable-width layouts do not expose an empty track. Previous and next
controls make one physical move; after entering a clone set, the implementation
resets without animation to the matching original. Logical state comes from
`data-carousel-index`. Manual pointer or keyboard navigation stops autoplay,
as does arriving with a fragment that selects a slide; a deep-linked image must
remain focused rather than advancing on the autoplay timer.
Cardhaus supplies control labels and arrow presentation rather than Swiper's
navigation or accessibility rewriting. The URL fragment tracks the focused
slide and initializes a matching slide on arrival.

An image-bearing topic starts with all compatible bundle images. The canonical
image is first and active. Per-image focal metadata takes precedence; missing
canonical coordinates fall back independently to `hero.focal`, then center.
Canonical alt text falls back through `hero.alt` to the title. The main gallery,
thumbnail strip, and single-image lightbox stay synchronized; clicking a slide
opens that exact image, and the main gallery and lightbox loop continuously.
A text-only topic remains valid.

## View Transitions

Canonical cards and the canonical first gallery image receive the same stable,
filename-safe `view-transition-name`, derived by
`layouts/_partials/view-transition-name.html`. Cardhaus opts into cross-document
transitions. The named image expands over 750ms while page roots fade.
`prefers-reduced-motion: reduce` makes the named transition effectively
instantaneous and disables root fades.

## Descriptions and social metadata

Cardhaus emits a canonical URL, description, Open Graph data, Twitter card data,
and RSS discovery where that output exists. Description precedence is page
description, explicit summary, generated summary, then site description.

Social image precedence is `social.image`, canonical hero, site social image,
then none. Focal coordinates and alt text inherit only from metadata belonging
to the selected resource; otherwise they fall back to center and page title.
Processable images use the largest in-bounds 40:21 crop around the focal point
and are reduced, never enlarged, toward 1200 by 630 pixels. Other formats are
linked without an attempted crop.

## Design and extension contracts

Image overlays share a subtle dark glass treatment with useful contrast. Topic
cards use a consistent `3 / 4` portrait crop; gallery images preserve their
source proportions within the carousel.

Theme CSS is divided into neutral tokens, document base, layout, and components,
then concatenated, minified, and fingerprinted. Consumers may override semantic
custom properties through a site-owned stylesheet configured as
`params.cardhaus.customStylesheet`. Structural breakpoint values are build-time
Hugo parameters because CSS custom properties cannot define media-query limits.

The theme may provide generic header, menu, breadcrumb, footer, page, section,
taxonomy, topic, carousel, gallery, and card rendering. Consumer configuration
provides navigation and identity. Header markup must be valid without any
consumer asset; the current exception is tracked in `ROADMAP.md`.

## Conformance

A conforming change preserves canonical image identity, shared cards, graceful
text-only pages, responsive grids, accessible metadata, reduced motion, exact
gallery targeting, and continuous carousel navigation. Validate with a
production Hugo build, generated-page inspection, interaction checks for changed
UI behavior, and `git diff --check`.
