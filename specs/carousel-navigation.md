# Hero carousel navigation

## Scope

The carousel began as a homepage-only feature backed by one shared data file.
It is now a shared partial: each branch bundle may provide a sibling
`carousel.yaml`, while the root bundle uses `content/carousel.yaml`. The
navigation code must therefore work for every carousel instance, including
short, centered, mixed-width slide sets.

## What to avoid

- Do not combine Swiper Navigation with separate button handlers. Each control
  must have exactly one movement path.
- Do not enable Swiper's default navigation icons or control A11y rewriting:
  Cardhaus supplies the arrow shapes and button labels itself.
- Do not use `rewind` for the centered mixed-width carousel. Its end-to-start
  jump can expose an empty track.
- Do not use Swiper's loop reordering for this layout. It can leave an empty
  side or choose the wrong physical direction with these slide widths.

## Navigation contract

Clone the last slide before the originals and the first slide after them, then
start on the first original. Each arrow makes one physical move:

```js
previous: swiper.slidePrev()
next:     swiper.slideNext()
```

Render a complete clone set on each side of the originals. A single cloned
neighbour is not sufficient when variable-width slides leave more than one
slide's width visible on a large viewport. After entering either clone set,
reset to its matching original with a zero-duration `slideTo`. Read the logical
index from `data-carousel-index`, so pagination and preloading ignore the clones.

The handlers should stop autoplay and mark navigation manual before moving.
The same routines serve the keyboard arrows. Cardhaus CSS draws the arrow
icons and intentionally suppresses focus outlines on the previous/next
controls.

## Verification checklist

- Run `hugo --minify --noBuildLock` and `git diff --check`.
- In a browser, click Next across the last slide and confirm it reaches the
  first slide; click Previous from the first slide and confirm it reaches the
  last slide.
- Confirm both controls move exactly one logical slide in their labeled
  direction, without a blank boundary jump.
- Confirm the controls still show only the Cardhaus arrows, with no injected
  Swiper SVGs or focus outline.
