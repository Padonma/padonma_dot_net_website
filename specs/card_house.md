# CardHouse image-first knowledge theme

## Purpose and design intent

CardHouse is a cinematic, image-first Hugo theme for topic-centered knowledge
sites. A topic is a persistent wiki-like object rather than a product or a
marketing card. Its canonical image gives it a stable visual identity; its
title, optional classification, supporting gallery, and long-form reference
content provide the surrounding context.

The topic index, taxonomy results, and topic detail page are different views of
the same object:

- Topic and taxonomy lists: responsive topic-card grid.
- Topic detail: expanded canonical hero followed by wiki content.

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

During migration, `social_image` and then the first compatible page-bundle
image may be used as fallbacks. A missing image produces an intentional neutral
placeholder, never a broken image.

All cards and topic heroes render through
`layouts/_partials/hero-image.html`. That partial resolves the canonical
resource, generates responsive derivatives, applies the focal point with
`object-position`, and emits the same `data-topic-id` wherever the topic
appears.

## Shared topic card

`layouts/_partials/topic-card.html` is the only topic-list card. It contains:

- the canonical topic image or missing-image state;
- the topic title in a restrained dark glass overlay;
- an optional short `topic_type` label.

It does not contain a description body, commerce state, price, inventory,
purchase control, or other product metadata. The image remains the primary
presentation.

```gohtml
{{ partial "topic-card.html" . }}
```

## Page patterns

### Homepage

The hero carousel reads `data/carousel.yaml`. Each slide resolves `slug` to a
topic destination and may choose any image from that topic's page bundle using
`image`. It also supports an independent `focal` and accessible `alt` text. If
`image` is omitted, the canonical topic hero is used as a fallback. Slides are
plain images with no visible title, caption, or glass overlay.

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

### Topic detail

An image-bearing topic begins with an expanded rendering of its canonical hero.
The title and optional date sit in the same dark glass language as the card.
Long-form wiki content follows. When multiple page-bundle images exist, the
supporting gallery follows the content.

A text-only topic begins with a conventional page heading and content; hero
imagery is encouraged but not required.

### Blog posts

Posts are narrative additions to the knowledge base. A post may adopt the same
hero contract and card renderer when listed. CardHouse does not require a blog,
and post presentation must not distort the topic model.

## Visual continuity

Every canonical image receives a stable `data-topic-id` derived from its page
permalink. The hook is shared by cards and detail renderings and is the basis
for a later View Transitions implementation. Arbitrary homepage hero-carousel
slides remain outside this identity system. Transition names are not assigned
until duplicate representations on the same document can be disambiguated
safely.

## Glass and image treatment

Image overlays use one subtle dark glass treatment: translucent charcoal,
moderate blur and saturation, a fine light border, and restrained shadow. Text
must maintain useful contrast over both light and dark imagery.

Card images use a consistent `4 / 3` crop. Topic detail heroes use a responsive
`16 / 9` presentation. Canonical source identity and focal coordinates remain
the same even where the responsive crop changes.

## Module boundary

Reusable behavior and presentation live under `themes/cardhouse/`. The theme
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
3. Route shared topic imagery through `hero-image.html`.
4. Keep topic cards image-first and overlay metadata minimal.
5. Do not introduce commerce or inventory assumptions into CardHouse.
6. Keep focal cropping predictable and missing images graceful.
7. Keep the theme independent of any one consuming site.
