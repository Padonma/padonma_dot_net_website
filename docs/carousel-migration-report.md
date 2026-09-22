# Carousel migration report

The carousel-unification migration was generated from the working tree with
Hugo 0.147.9. A pre-migration render confirmed that Hugo orders compatible page
resources bytewise by filename; the former gallery then promoted the canonical
hero to the first position. The generator reproduces that order.

- Leaf bundles scanned: 47
- Image-bearing leaf bundles: 44
- Generated leaf `carousel.yaml` files: 44
- Generated entries: 165
- Excluded AVIF files: 1 (`backstrap.avif`)
- Existing carousels skipped and retained byte-for-byte: 3 (homepage,
  Bandgrind, and Sport Coat)
- Resolved blockers: the intentionally deleted Samatoa
  `short-dress-close-up.png` removed a collision with the retained
  `short-dress-close-up.jpeg`

The migration standardizes every generated alt to the page title. This changes
two former canonical-image alt values and needs editorial awareness:

- Loro Piana: `A cream lotus-fiber jacket by Loro Piana` → `Loro Piana`
- Burmese attire: `Karen tunic` → `Burmese attire`

All 44 generated files passed generator check mode. The production build and
internal-reference validation completed successfully after the template and
asset migration. Generated coverage and ordering matched the former rendered
gallery exactly for all 43 published image-bearing leaves; the remaining leaf
is a non-rendered draft and follows the same measured deterministic ordering
rule.
