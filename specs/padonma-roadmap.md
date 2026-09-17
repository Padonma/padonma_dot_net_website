# Padonma roadmap

This roadmap contains unfinished consumer-site work. Reusable rendering belongs
in Cardhaus; deployment procedures remain in `docs/aws-deployment.md`.

## Content architecture and authoring

- Agree on supporting-image metadata, then migrate representative bundle images
  before any bulk conversion. Keep existing resource filenames stable during
  migration so hero references do not break.
- Add topic, Bandgrind session, and eventual post archetypes once their required
  metadata is settled. Do not invent dates for evergreen research pages.
- Replace deprecated or inconsistent content build settings while preserving
  intended list and render visibility. Document when `list: local`,
  `list: never`, `render: link`, and `render: never` are appropriate.
- Correct stale internal paths or add explicit aliases. Validate ordinary links,
  fragments, static downloads, raw HTML images, and representative QR diagrams.
- Decide whether Bandgrind sessions need an explicit sequence field rather than
  treating display weight as chronology.

## Discovery

- Pilot a small, useful taxonomy vocabulary such as materials and techniques.
  Add places, projects, organizations, or people only when they enable a real
  browsing task; keep workflow status private unless it has public value.
- Tune related-content weights against representative pages, including an
  explicit policy for branch-page introductions. Keep curated topic cards where
  editorial judgment is stronger than similarity matching.
- After the content metadata contract stabilizes, generate a Hugo JSON search
  index and build an accessible client-side search interface. Define which
  branch pages and visibility states are included before implementation.

## Publishing decisions

- Decide the production taxonomy and search URLs before launch, including any
  aliases or redirects needed for historical routes.
- Complete the AWS resources and first credentialed deployment by following
  `docs/aws-deployment.md`; local production validation remains credential-free.
