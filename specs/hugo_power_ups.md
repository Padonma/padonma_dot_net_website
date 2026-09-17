# Hugo power-ups for Padonma

Reviewed: 2026-09-14. Status: proposal; implementation has not started.

## Direction

Use more of Hugo's content and resource machinery to improve navigation,
authoring, image presentation, and publishing reliability. Preserve Cardhaus's
shared card and canonical hero design. Build speed is already sufficient;
optimization and theme extraction are secondary.

This review refines the initial suggestions. In particular, section content
visibility and image metadata should be addressed before adding search or broad
classification. Related content is metadata-based matching, not an automatically
constructed knowledge graph.

## Current baseline

- The audit found 55 Markdown files: 44 leaf bundles and 11 branch bundles.
- Page bundles, resource lookup, responsive image derivatives, CSS concatenation,
  minification, fingerprints, menus using `pageRef`, and editorial carousel YAML
  are already in use.
- Hugo already generates RSS, a sitemap, robots.txt, and two aliases. These are
  existing capabilities to refine, not missing features to add.
- The installed Hugo is 0.147.9; Cardhaus declares a minimum of 0.146.0. Current
  online documentation may describe later behavior. Verify APIs and template
  lookup against the supported version before implementing; make any version
  increase explicit and align development and deployment versions.
- The earlier in-memory builds completed in approximately 0.4–1.3 seconds. These
  are local observations, not cold-build benchmarks. Image transformations are
  already cached by Hugo.
- The build reports deprecated `_build` fields in `content/topics/fluff/index.md`
  and `content/topics/peoples/_index.md`, plus unused topic-card shortcodes,
  `page.html`, and `term.html`. Unused templates are not necessarily defects.
- No project archetypes or taxonomy assignments were found. Most pages have a
  summary, but no explicit description; only one had an explicit date.

## Recommended implementation sequence

### 1. Restore section prose and strengthen navigation

`themes/cardhaus/layouts/topics/section.html` renders child cards when `.Pages`
is nonempty, but renders `.Content` only in the other branch. Consequently,
substantial branch-page prose, including the Padonma Network introduction, has
no place in the HTML when that section has children.

Allow section pages to combine introductory Markdown, optional carousel/gallery,
and child cards. Agree on their visual order using the existing section designs.
Extract the repeated article markup only where that simplifies the templates.

Use Hugo's page tree for breadcrumbs, filtering ancestors that are deliberately
not published. Use `HasMenuCurrent` alongside `IsMenuCurrent` to keep TOPICS
active on descendant pages. For Bandgrind, consider generated session navigation
with an explicit sequence field; its weights currently encode display order and
should not be assumed to be chronological dates.

Acceptance: sections with children retain their prose, children remain reachable,
hidden ancestors produce no dead breadcrumb links, and session ordering is clear.

Reference: [Hugo page methods](https://gohugo.io/methods/page/).

### 2. Establish shared image metadata and Markdown render hooks

Keep `hero.image` as the page's canonical image selection. Introduce Hugo's
`resources` front matter for per-image alt text, caption, credit/source, focal
coordinates, and optional gallery ordering or exclusion. These custom parameters
need theme code to consume them; Hugo does not automatically render captions or
sort a gallery by a custom weight.

Avoid changing resource `name` during this migration: Hugo lookup uses the new
name after a resource is renamed, which could break existing hero references.
Document precedence between resource metadata, existing `hero` metadata, and
carousel-specific overrides. Preserve existing content through a migration
period. Moving metadata alone does not fix YAML's interpretation of an unquoted
`y`; quote that key or adopt unambiguous coordinate names consistently.

Add an image render hook that resolves bundle resources and reuses the responsive
image helper. Preserve Markdown alt text and linked images. Define handling for
SVG, animated images, small originals, and remote URLs without assuming every
resource supports the same raster operations. Do not silently download remote
images. Review QR diagrams separately: lossy derivatives and resampling may be
unsuitable where exact modules or scannability matter.

Migrate raw HTML figures gradually. Render hooks apply to Markdown, not raw
`<img>` elements. Keep `unsafe = true` until the remaining HTML and embeds have
been audited and migrated; disabling it is an optional outcome, not a prerequisite.

Add a link render hook or use explicit Hugo references for internal links.
Resolve content references to `.RelPermalink`, preserving fragments and queries.
Handle static downloads, external URLs, mail links, and anchors separately.
Existing stale paths need correction or an explicit redirect map: hooks cannot
infer where moved pages went. Preserve useful historical URLs through aliases.

Acceptance: representative prose images, linked images, figures, QR diagrams,
and gallery images render correctly; missing explicit local references produce
actionable diagnostics; legacy URLs and fragment links receive targeted checks.

References: [page resource metadata](https://gohugo.io/content-management/page-resources/),
[image hooks](https://gohugo.io/render-hooks/images/),
[link hooks](https://gohugo.io/render-hooks/links/).

### 3. Add authoring defaults and focused validation

Create topic, session, and eventual post archetypes after agreeing on the image
contract. Include title, summary, draft state, and suitable content prompts.
Dates should reflect real editorial information; do not invent dates for existing
research pages. Use branch `cascade` for shared defaults only where inheritance
is semantically correct, with individual pages able to override them.

Use small validation partials with `errorf` for broken explicit references or
invalid values, and `warnf` for editorial omissions during migration. Validate
hero/carousel targets, image types, focal ranges, and controlled vocabulary
values. Missing images remain valid for text-only topics, and intentionally
decorative images may have empty alt text. Validation is custom template logic,
not a built-in Hugo schema system.

An explicitly configured but missing hero currently falls back to another image
in `hero-resource.html`; distinguish that mistake from intentionally omitting a
hero. Exercise both existing card shortcodes in a suitable fixture or actual
content. Fix `_build` to `build`, preserving the existing visibility intent:
`list: never` does not make a page private or necessarily stop it being rendered.

Acceptance: new bundles are easy to create, deliberately broken references fail
with a file/context message, optional metadata stays optional, and visibility
behavior is checked on the affected pages and descendants.

References: [archetypes](https://gohugo.io/content-management/archetypes/),
[cascade](https://gohugo.io/configuration/cascade/),
[build options](https://gohugo.io/content-management/build-options/).

### 4. Improve descriptions, sharing previews, and feed discovery

`baseof.html` currently falls back from `.Description` directly to the site-wide
description, bypassing the existing page summaries. Introduce a plain-text
description fallback, canonical links, and Open Graph/social-card metadata.
Reuse the canonical hero for sharing, with an intentional social crop or override
when appropriate. Add RSS discovery links using the page's output formats.

Hugo's embedded metadata templates are useful starting points, but verify their
invocation and image expectations on the supported Hugo version. The theme's
existing `images` array contains metadata maps, whereas embedded social templates
expect image paths; resolve that conflict before using those templates directly.
Do not assume the embedded schema template emits the desired JSON-LD. Add explicit
structured data only for information the page actually supplies, using a suitable
type and JSON serialization.

Acceptance: a topic, a section, and the homepage have correct absolute canonical
and social image URLs, useful descriptions, and no conflicting metadata. Feeds
contain intentional content and dates rather than fabricated chronology.

Reference: [embedded metadata templates](https://gohugo.io/templates/embedded/).

### 5. Pilot taxonomies and related content

Start with a small vocabulary, such as materials and techniques, on a representative
set of pages. Add places, projects, organizations, or people only when they support
a useful browsing task. Workflow status can remain a parameter rather than become
a public taxonomy. Avoid creating many sparse indexes at once.

Configure explicit related-content indices and tune the weights against actual
examples. Evergreen topics should be able to relate to newer pages; date matching
is unlikely to be useful here. The usual `site.RegularPages.Related` collection
excludes branch pages, so deliberately decide how important section introductions
participate. Filter recommendations to pages visitors can reach and should see.

Keep curated links and embedded topic cards where editorial judgment is stronger
than similarity scoring. Term pages should use the shared card design, with
intentional text or imagery for the terms themselves.

Acceptance: sample related lists connect useful material across directory branches,
avoid irrelevant matches, and lead to meaningful taxonomy landing pages.

Reference: [related content](https://gohugo.io/content-management/related-content/).

### 6. Generate a search index when the content contract is settled

Add a home JSON output containing title, summary, permalink, selected terms,
plain-text body, and optionally a small hero thumbnail. Generate JSON with Hugo's
serialization functions, not hand-escaped strings. Include useful section pages
as well as regular pages; explicitly exclude drafts and intentionally undiscoverable
or unrendered pages according to the publication policy.

Hugo generates the index; a separate client-side interface performs searches.
Keep that interface accessible, load the index on demand, and evaluate its size
before choosing a search dependency. Search does not require taxonomies, but the
metadata work above gives it better inputs.

Acceptance: distinctive body text finds the expected topic, titles rank sensibly,
all results lead to published pages, and hidden content is absent from the index.

Reference: [output formats](https://gohugo.io/configuration/output-formats/).

### 7. Move carousel JavaScript into Hugo Pipes

Move the large inline implementation from `baseof.html` into theme assets and use
`js.Build` plus fingerprints. Preserve current behavior, including manual-navigation
autoplay stopping, gallery synchronization, lightbox behavior, and image decoding.
Use development source maps where helpful. Fingerprinting enables independent
browser caching and removes the need for a manually maintained version query.

This can be an independent maintenance change earlier in the sequence. It requires
no new npm dependency if existing vendored code is retained. Loading scripts only
where needed can follow once carousel/gallery presence has one reliable definition.
Externalizing JavaScript alone does not establish a strict CSP; inline styles and
third-party embeds would need separate consideration.

Acceptance: the existing interactive behavior passes a focused browser check,
JavaScript is emitted as a fingerprinted asset, and pages without interactive
components still render correctly.

Reference: [js.Build](https://gohugo.io/functions/js/build/).

## Defer until there is a concrete need

- Broad partial caching or segmented builds: first measure a real bottleneck.
  The image helper runs repeatedly, but Hugo already caches transformations.
  Cached partials need correct resource/context variant keys and must not suppress
  validation or mix page-specific output.
- Content adapters: useful if supplier or garment records acquire a structured
  source of truth. Keep the current editorial pages as bundles for now.
- Multilingual publishing: adopt when translators, target languages, and a content
  maintenance process exist.
- Standalone Hugo Module extraction: follow the existing Cardhaus roadmap once
  a second consumer or versioning requirement justifies it.

## Scope and next implementation slice

These notes authorize no deployment or bulk content conversion. A practical first
implementation slice is section prose/navigation and the existing roadmap's narrow
conformance cleanup, followed by a representative image metadata/render-hook pilot.
Keep generic rendering in Cardhaus and Padonma's vocabulary, editorial choices,
and site identity in project content/configuration.

For each slice, use the supported Hugo version, inspect relevant build diagnostics,
and review representative generated HTML. Use visual checks for layout/image changes
and browser checks for interaction changes. A passing Hugo build alone does not
prove that ordinary Markdown links work or that section content is visible.
