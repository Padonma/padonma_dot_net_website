# Padonma content and authoring

Padonma is a consumer of Cardhaus. This document records the site's current
content organization and editorial conventions; it does not redefine theme
rendering contracts.

## Site structure

- `content/_index.md` is the editorial homepage. It introduces Padonma's fiber,
  network, and atelier strands and uses curated `topic-card-grid` groups.
- `content/topics/` contains the durable knowledge hierarchy. Branch bundles use
  `_index.md`; leaf bundles use `index.md`. Branch prose is rendered and may use
  `topic-card-children` for an explicit immediate-child listing.
- `content/posts/` is reserved for dated narrative work. Topics remain the
  durable reference model even if posts later become substantive.
- Main navigation and site identity are configured in `hugo.toml`. Cardhaus
  highlights a menu entry on its descendants and derives breadcrumbs from the
  Hugo page tree.

## Editorial metadata

Give each page a clear title and a short summary suitable for cards and metadata.
Use `hero.image`, `hero.focal`, and `hero.alt` for a canonical image when the page
has one. Quote the `"y"` focal key in YAML. Text-only topics are valid.

Use a bundle's `carousel.yaml` only for a deliberately selected visual sequence.
Sibling images alone do not render a carousel. Carousel images may differ from
canonical heroes. Use curated `topic-card` and
`topic-card-grid` embeds when editorial selection matters; use
`topic-card-children` for structural immediate-child navigation.

To opt an existing leaf bundle into its migrated image sequence, run:

```sh
python3 scripts/generate-carousel.py content/topics/example-topic
python3 scripts/generate-carousel.py content/topics/example-topic --check
```

The default directory is the current working directory. Preview exact output
without writing with `--dry-run`. The generator refuses to overwrite an
existing file; resolve reported filenames, focal metadata, or hash collisions
instead of editing identifiers automatically.

When one carousel links to the same image in another carousel, give both slides
the same `hash` and include it explicitly in the destination URL fragment. Check
all such handoffs, and optionally a rendered Hugo output directory, with:

```sh
python3 scripts/validate-carousel-handoffs.py
python3 scripts/validate-carousel-handoffs.py --rendered-dir public
```

Padonma's detailed shortcode, image, social-preview, and consumer-parameter
syntax is documented in `themes/cardhaus/README.md`. Stable rendering behavior
is defined by `themes/cardhaus/SPEC.md`.

## Ownership and publishing

Padonma owns its hierarchy, prose, taxonomy vocabulary, search inclusion,
aliases, canonical production URL, brand assets, and deployment. Cardhaus owns
how supported metadata and components render. New site-specific vocabulary must
not be added to theme templates.

Local production checks and AWS publication are separate. Follow
`docs/aws-deployment.md`; do not require cloud credentials for ordinary builds.
