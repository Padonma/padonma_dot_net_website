# CardHouse

CardHouse is an image-first Hugo theme for topic-centered knowledge sites. It
treats each topic as a durable wiki-like page with one canonical image across
featured slides, list cards, and detail heroes.

## Use in a Hugo site

Place this directory at `themes/cardhouse` and select it in the consuming
site's configuration:

```toml
theme = "cardhouse"
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

If `hero.image` is absent, CardHouse temporarily falls back to `social_image`
and then the first compatible bundle image. Explicit hero data is recommended.

An optional `topic_type` value appears as a small secondary card label.

## Homepage hero carousel

The homepage carousel reads `data/carousel.yaml`:

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
CardHouse falls back to the canonical topic image.

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

CardHouse keeps its CSS in four responsibility-based source files:

- `assets/css/tokens.css` provides neutral semantic defaults.
- `assets/css/base.css` provides the reset and global document behavior.
- `assets/css/layout.css` arranges the site shell and major page regions.
- `assets/css/components.css` styles cards, prose, galleries, and controls.

The base template concatenates those sources, in that order, into the
fingerprinted `css/main.css` served to browsers.

A consuming site can add an optional site-owned stylesheet under its global
`assets/` directory:

```toml
[params.cardhouse]
  customStylesheet = "css/brand.css"
```

CardHouse processes and links that stylesheet after its own bundle. Define
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
- `layouts/_partials/topic-card.html` renders the shared card.
- `layouts/topics/single.html` renders the topic detail hero and wiki content.
- `assets/css/` contains the shared, bundled responsive design system.

CardHouse intentionally has no product, price, inventory, or purchasing model.
