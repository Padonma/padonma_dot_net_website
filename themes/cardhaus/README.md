# Cardhaus

Cardhaus is an image-first Hugo theme for topic-centered knowledge sites. It
treats each topic as a durable wiki-like page with one canonical image across
list cards and the first image in its detail gallery. Homepage carousel slides
are an editorial exception and may select a different bundle image.

## Use in a Hugo site

Place this directory at `themes/cardhaus` and select it in the consuming
site's configuration:

```toml
theme = "cardhaus"
```

The directory is self-contained and can be moved into a standalone repository
later. A Hugo Module import path should be added only after that repository has
a stable public or private module URL.

## Topic contract

Topics are page bundles under `content/topics/`. A topic may select its
canonical bundle image and crop:

```yaml
hero:
  image: "filename.jpg"
  focal:
    x: 0.5
    y: 0.35
  alt: "Description of the image"
```

If `hero.image` is absent, Cardhaus falls back to the first compatible bundle
image. Explicit hero data is recommended.

The shared card renderer and canonical first gallery image apply `hero.focal`
and `hero.alt`. Supporting gallery images may use entries in the page's
`images` frontmatter array for individual focal points. Per-image focal
coordinates take precedence; a missing coordinate on the canonical image falls
back independently to its topic hero coordinate.

An optional `topic_type` value appears as a small secondary card label. Hugo's
page summary appears beneath the title when one is available.

## Topic-card shortcodes

Use `topic-card` to place the existing canonical card in Markdown content:

```go-html-template
{{</* topic-card ref="/topics/example-topic" */>}}
```

Use the paired `topic-card-grid` shortcode for a curated responsive group. Its
optional `heading` appears first. Markdown before the first nested card is
rendered below the heading and above the cards:

```go-html-template
{{</* topic-card-grid heading="Related topics" */>}}

These topics provide useful context for this page.

{{</* topic-card ref="/topics/example-topic" */>}}
{{</* topic-card ref="/topics/another-topic" */>}}

{{</* /topic-card-grid */>}}
```

Use absolute content references beginning with `/`. Missing `ref` values and
references that do not resolve fail the build. Do not repeat the same topic on
one rendered page: canonical cards carry named View Transitions, whose names
must be unique within a document. A grid requires at least one nested card;
place all introductory Markdown before the first card.

## Bundle hero carousel

Place a `carousel.yaml` beside a bundle's `_index.md` to show the carousel on
that bundle's page. The root bundle uses `content/carousel.yaml`; branch
bundles use the same filename in their own directory. Bundles without this
file simply omit the carousel.

Each file contains slides in this form:

```yaml
- slug: example-topic
  image: supporting-image.jpg
  alt: Description of the selected image
  focal:
    x: 0.4
    y: 0.6
```

`image` may select any image from the linked topic's page bundle. The focal
point and alt text belong to that slide and do not change the topic's canonical
hero. Slides contain no visible title or caption. If `image` is omitted,
Cardhaus falls back to the canonical topic image.

## Consumer parameters

All parameters are optional unless the consuming layout depends on them:

```toml
[params]
  description = "Site description"
  subtitle = "Site subtitle"
  logo = "brand/wordmark.png"
  billboardImage = "brand/background.jpg"
  billboardLogo = "brand/mark.png"
  billboardTitle = ["Site", "Name"]
  topicsHeading = "Topics"
  footerImage = "brand/footer.jpg"
```

Image values resolve through Hugo's global `assets/` directory.

## Styling and brand overrides

Cardhaus keeps its CSS in four responsibility-based source files:

- `assets/css/tokens.css` provides neutral semantic defaults.
- `assets/css/base.css` provides the reset and global document behavior.
- `assets/css/layout.css` arranges the site shell and major page regions.
- `assets/css/components.css` styles cards, prose, galleries, and controls.

The base template concatenates those sources, in that order, into the
fingerprinted `css/main.css` served to browsers.

A consuming site can add an optional site-owned stylesheet under its global
`assets/` directory:

```toml
[params.cardhaus]
  customStylesheet = "css/brand.css"
```

Cardhaus processes and links that stylesheet after its own bundle. Define
brand values there as ordinary CSS custom-property overrides:

```css
:root {
  --accent: #8b1e3f;
  --primary: var(--accent);
  --font-display: Georgia, serif;
}
```

The configuration contains only the optional stylesheet path; colors, fonts,
and other design values remain in CSS and follow the normal cascade.

## Reusable source

- `layouts/_partials/hero-resource.html` resolves canonical images.
- `layouts/_partials/hero-image.html` renders focal-aware responsive imagery.
- `layouts/_partials/gallery-image-meta.html` applies per-image focal data and
  canonical hero fallbacks consistently across gallery views.
- `layouts/_partials/topic-card.html` renders the shared card.
- `layouts/shortcodes/topic-card.html` embeds one shared card in Markdown.
- `layouts/shortcodes/topic-card-grid.html` renders curated cards with optional
  introductory Markdown.
- `layouts/topics/single.html` renders the topic detail hero and wiki content.
- `assets/css/` contains the shared, bundled responsive design system.

Cardhaus intentionally has no product, price, inventory, or purchasing model.

## Current validation status

The Padonma consumer builds successfully with Hugo. The remaining cleanup queue
is documented in `specs/roadmap.md`: removal of one legacy header asset lookup
and an in-content shortcode fixture for validation.
