# Cardhaus image-first knowledge theme

## Purpose and design intent

Cardhaus is a cinematic, image-first Hugo theme for topic-centered knowledge
sites. A topic is a persistent wiki-like object rather than a product or a
marketing card. Its canonical image gives it a stable visual identity; its
title, optional short summary and classification, supporting gallery, and
long-form reference content provide the surrounding context.

The topic index, taxonomy results, and topic detail page are different views of
the same object:

- Topic and taxonomy lists: responsive topic-card grid.
- Topic detail: full image gallery, canonical hero first, followed by wiki
  content.

The homepage hero carousel is a deliberate editorial exception: it may present
arbitrary images from topic page bundles rather than canonical topic heroes.

Navigation should feel like moving closer to a topic rather than replacing one
unrelated page with another.

## Canonical topic image

Each topic may select one canonical page-bundle image through frontmatter:

```yaml
hero:
  image: "filename.jpg"
  focal:
    x: 0.5
    y: 0.35
  alt: "Optional accessible description"
```

`hero.image` is the durable editorial choice. Each focal coordinate is optional,
accepts a value from 0 through 1, and defaults independently to `0.5`.
`hero.alt` defaults to the topic title.

When `hero.image` is absent, the first compatible page-bundle image may be
used as a fallback. A missing image produces an intentional neutral placeholder,
never a broken image.

All cards render through `layouts/_partials/hero-image.html`. That partial
resolves the canonical resource, generates responsive derivatives, applies the
focal point with `object-position`, and emits the topic identity. Topic detail
galleries use the same `hero-resource.html` resolver to place that canonical
resource first, then assign its matching transition name through
`view-transition-name.html`.

## Shared topic card

`layouts/_partials/topic-card.html` is the only topic-list card. It contains:

- the canonical topic image or missing-image state;
- the topic title and optional summary in a restrained dark glass overlay;
- an optional short `topic_type` label.

The summary is short supporting context sourced from Hugo's page summary. It
does not turn the card into a general description body. Cards do not contain
commerce state, price, inventory, purchase controls, or other product metadata.
The image remains the primary presentation.

```gohtml
{{ partial "topic-card.html" . }}
```

## Embedded topic-card shortcodes

Markdown content may reuse the canonical card renderer through two shortcodes.
The single-card shortcode resolves an absolute content reference and delegates
directly to `topic-card.html`:

```go-html-template
{{</* topic-card ref="/topics/example-topic" */>}}
```

The paired grid shortcode groups curated cards and may add a heading. Markdown
placed before the first card is rendered below that heading and spans the grid:

```go-html-template
{{</* topic-card-grid heading="Related topics" */>}}

These topics provide useful context for the discussion above.

{{</* topic-card ref="/topics/example-topic" */>}}
{{</* topic-card ref="/topics/another-topic" */>}}

{{</* /topic-card-grid */>}}
```

`ref` is required and unresolved references fail the Hugo build. Each referenced
topic should appear at most once on a rendered page so its canonical View
Transition name remains unique in that document. The grid does not provide
image, title, summary, or styling overrides; those remain properties of the
referenced topic and the shared card renderer. A grid requires at least one
nested card, and any introductory Markdown must precede all of its cards.

## Page patterns

### Homepage

The homepage hero carousel reads `content/carousel.yaml`, the root branch
bundle's page resource. A topics branch may provide its own `carousel.yaml`
beside `_index.md`. Each slide resolves `slug` to a topic destination and may
choose any image from that topic's page bundle using `image`. It also supports
an independent `focal` and accessible `alt` text. If `image` is omitted, the
canonical topic hero is used as a fallback. Slides are plain images with no
visible title, caption, or glass overlay.

```yaml
- slug: example-topic
  image: supporting-image.jpg
  alt: Description of the selected image
  focal:
    x: 0.4
    y: 0.6
```

Because an arbitrary carousel image is not the topic's canonical identity, it
does not receive the canonical `data-topic-id` transition hook.

Homepage topic previews use the same `topic-card.html` partial and `card-grid`
as every other topic list.

### Topic, section, taxonomy, and term lists

All generated lists use the shared topic card. The authoritative responsive
grid uses three columns on desktop, two on tablet, and one on mobile.

Cardhaus has two configurable build-time structural breakpoints under
`[params.cardhaus.breakpoints]`: `tablet` defaults to `1200px` and `mobile`
defaults to `850px`. The grid has three columns above the tablet breakpoint,
two columns at and below tablet until mobile, and one column at mobile. A
consuming site may override either value; Hugo compiles the values into the
theme's media queries. Narrower component-level rules may adjust typography or
spacing for fit, but do not alter this structural grid contract.

### Topic detail

An image-bearing topic begins with a full carousel of its page-bundle images.
The canonical hero is ordered first, starts active, and carries the matching
View Transition name. Explicit per-image focal coordinates take precedence;
each missing coordinate on the canonical image falls back independently to its
`hero.focal` value and then to `0.5`. Its alternative text uses `hero.alt`, with
the topic title as fallback. Supporting images follow in the same carousel. The
topic title, optional date, and long-form wiki content appear below the gallery.

The main gallery shows a centered 2.5-slide composition and loops continuously.
Its thumbnail strip remains synchronized. Clicking any visible image opens that
specific image in a single-image lightbox, which also loops continuously in
both directions.

A text-only topic begins with a conventional page heading and content; hero
imagery is encouraged but not required.

### Blog posts

Posts are narrative additions to the knowledge base. A post may adopt the same
hero contract and card renderer when listed. Cardhaus does not require a blog,
and post presentation must not distort the topic model.

## Visual continuity

Every canonical image receives a stable `data-topic-id` derived from its page
permalink. Cards and the canonical first image in the topic gallery also
receive the same filename-safe `view-transition-name`, generated by
`layouts/_partials/view-transition-name.html`.

Cardhaus opts into cross-document View Transitions with
`@view-transition { navigation: auto; }`. The named image expands for 750ms
while the outgoing and incoming page roots fade. Under
`prefers-reduced-motion: reduce`, the named transition is shortened to 0.01s
and root fades are disabled.

Arbitrary homepage hero-carousel slides remain outside this identity system;
the canonical topic cards below the carousel continue to participate.

## Glass and image treatment

Image overlays use one subtle dark glass treatment: translucent charcoal,
moderate blur and saturation, a fine light border, and restrained shadow. Text
must maintain useful contrast over both light and dark imagery.

Card images use a consistent `3 / 4` portrait crop. Topic-gallery slides
preserve each source image's aspect ratio within the centered carousel.
Canonical source identity and focal coordinates remain stable across the card
and gallery even where their responsive presentation differs.

## Module boundary

Reusable behavior and presentation live under `themes/cardhaus/`. The theme
must not hard-code a consumer name, logo, content asset, or subject domain.
Consumers provide identity, navigation, billboard content, featured topics,
and page bundles through Hugo configuration and content data.

Semantic CSS custom properties provide defaults and may be overridden by a
consumer. Reusable selectors use topic, card, hero, gallery, carousel, post, or
site terminology rather than project-specific names.

## Non-negotiable rules

1. One topic has one canonical image identity across list cards and detail
   views; the homepage hero carousel is an explicit editorial exception.
2. Do not create separate card and detail image contracts.
3. Route canonical image selection through `hero-resource.html`, and route all
   topic cards through `hero-image.html`.
4. Keep topic cards image-first and overlay metadata limited to the title,
   optional short summary, and optional classification.
5. Do not introduce commerce or inventory assumptions into Cardhaus.
6. Keep focal cropping predictable and missing images graceful.
7. Keep the theme independent of any one consuming site.
8. Preserve matching View Transition names between canonical cards and the
   canonical first topic-gallery image.

## Current conformance notes

The implementation conforms to the central image identity, shared-card,
responsive-grid, bundle-carousel, gallery/lightbox, shortcode, and View
Transition contracts. A production Hugo build succeeds.

One implementation gap remains and is tracked in the roadmap rather than being
accepted as a change to this specification:

- `baseof.html` still conditionally looks up `brand/checkerboard.png` while
  opening the site header. The theme must render valid header markup without
  relying on that consumer asset or path.

The topic-detail gallery now gives per-image focal coordinates precedence and
falls back to `hero.focal` and `hero.alt` for its canonical first image,
matching the shared hero contract.
