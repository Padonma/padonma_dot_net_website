# Padoma Scanner product and technical specification

Status: Draft

Product name: **Padoma Scanner**
Internal/working name: **Bandgrinder**

## 1. Purpose

Padoma Scanner is a planned static-browser-first tool for giving a unique hand-woven garment a permanent physical identifier.

The tool generates a UUID locally, encodes that UUID in an rMQR pattern, supports photographing and decoding the hand-woven result, and verifies that the decoded value exactly matches the generated value. After verification, the woven band can be stitched into a garment. The rMQR then carries the garment's UUID as a durable, machine-readable identifier.

The artisan may publish a conventional web page whose content includes the same UUID and information about the garment. Because the scanned UUID is an exact lookup key, people and independent software can use it to find that page on the web.

`bandgrinder/bandgrinder.html` and the scripts under `bandgrinder/` are experiments, not an implementation of the complete workflow specified here. In particular, the current HTML is a minimal client-side reader; it does not establish that generation, comparison, project persistence, publishing, indexing, or production hardening already exist.

## 2. Product principles

1. **Local first.** Generation, rendering, capture, decoding, and exact comparison run in the browser without an application server.
2. **Physical-to-digital fidelity.** Verification succeeds only when the scanned UUID is byte-for-byte equal to the UUID originally generated for the project.
3. **Artisan ownership.** The artisan owns the garment page and, in the proposed GitHub flow, the repository that publishes it.
4. **Open and decentralized.** The identifier and rMQR encoding do not depend on Padoma.net. Padoma.net services are optional conveniences.
5. **Explicit network boundaries.** The interface distinguishes offline/core operations from actions that send data to GitHub, Padoma.net, or another service.
6. **No discovery guarantees.** Publishing can make a page crawlable, but it cannot guarantee or promise when Google or another search engine will index it.

## 3. Goals

- Create a new UUID using a cryptographically strong browser-provided random source.
- Encode the UUID in an rMQR symbol suitable for translation into a hand-weaving pattern.
- Preserve the identifier throughout a potentially long physical making process.
- Decode a photograph or scan of the finished weaving in the same web app.
- Verify the decoded UUID against the generated UUID with an exact comparison.
- Provide clear evidence of match, mismatch, unreadable input, and invalid payload states.
- Allow the artisan to retain or export enough local project data to resume and independently verify the work.
- Offer an optional publishing flow that writes garment content to the artisan's own GitHub repository and publishes it through GitHub Pages.
- Optionally add a successfully published UUID-to-URL association to a public Padoma index after checking the live page.
- Keep non-Padoma publishing, indexing, lookup, and direct page use possible.

## 4. Non-goals

- Acting as a mandatory or authoritative global garment registry.
- Proving who made or owns a garment solely from possession of its UUID.
- Preventing copying, photographing, or re-weaving of a visible rMQR pattern.
- Treating successful decoding as proof of authenticity, provenance, ownership, or legal title.
- Requiring an application server for the core generation and verification workflow.
- Requiring GitHub, GitHub Pages, Padoma.net, Google, or any other specific online provider to use the physical identifier.
- Sending ordinary garment pages to Google's Indexing API. That API is not the general indexing mechanism for this content.
- Promising immediate or guaranteed indexing by Google or any other search engine.
- Defining garment metadata, page design, repository layout, rMQR dimensions, error-correction level, or long-term local storage before the open questions in this document are resolved.
- Claiming that the existing Bandgrinder prototype already provides the planned product workflow.

## 5. Actors

### Artisan

Creates an identifier, weaves its pattern, verifies the finished band, attaches it to a garment, and optionally publishes garment information.

### Scanner/user

Photographs an existing woven rMQR, obtains its UUID, and uses that exact value to look for associated public information. This may be the artisan, owner, buyer, curator, or another interested person.

### Repository owner

Authorizes access to a GitHub repository, reviews the content to publish, and controls the repository and GitHub Pages site. Usually this is the artisan.

### Padoma.net operator

May operate an optional OAuth/token-exchange service and optional public UUID index. The operator is not the mandatory custodian of UUIDs or garment pages.

### External providers

GitHub hosts repositories, authorization/consent screens, APIs, and optionally Pages sites. Search engines may crawl public pages and indexes according to their own policies and schedules.

## 6. Terminology

**UUID**

A 128-bit universally unique identifier. The canonical display form is lowercase hexadecimal in `8-4-4-4-12` groups, for example `97e41923-8681-4f84-a075-dc652cf7d3bc`.

**Identifier bytes**

The 16 raw bytes represented by the UUID. Existing Bandgrinder generator and reader experiments encode and decode this compact binary representation rather than a 36-character UUID string.

**rMQR**

Rectangular Micro QR Code, the two-dimensional symbol used to carry the identifier bytes in the woven band.

**Project**

The local record tying one generated UUID to its rendered weaving pattern, verification state, and optional publication information.

**Verification**

An exact comparison between the 16 decoded identifier bytes and the 16 bytes saved in the active project. Verification does not establish authenticity or ownership.

**Garment page**

A normal public web page containing the canonical UUID and garment information in human-readable and preferably machine-readable form.

**Padoma index**

An optional public mapping from a UUID to a live garment-page URL. It accelerates confirmation and discovery but is neither authoritative nor exclusive.

**Core workflow**

The local generation, rendering, capture/import, decoding, validation, and comparison functions.

**Online workflow**

Optional authentication, publishing, live-page checks, index submission, and web lookup functions.

## 7. Identifier and symbol contract

### 7.1 UUID generation

- A new project MUST generate a fresh UUID locally in the browser.
- Generation MUST use a cryptographically strong browser random-number facility, such as `crypto.randomUUID()` or a standards-correct UUID implementation backed by `crypto.getRandomValues()`.
- The application MUST NOT obtain the UUID from a Padoma.net service or require network access to generate it.
- The application MUST retain the original 16 bytes for comparison and show the canonical textual form to the artisan.
- Reopening or resuming a project MUST NOT silently generate a replacement UUID.

### 7.2 rMQR payload

- Version 1 of the format SHOULD encode exactly the UUID's 16 raw bytes in rMQR byte mode, matching the existing generator/reader experiments.
- A decoded payload MUST be exactly 16 bytes to qualify as a version 1 Padoma garment identifier.
- The canonical UUID string MUST be derived from those bytes; comparison MUST NOT depend on letter case, hyphen formatting, locale, or barcode library text decoding.
- The selected rMQR size and error-correction level MUST be recorded with the project and export.
- The rendered pattern MUST include a sufficient quiet zone and unambiguous module grid. Exact production dimensions and weaving guidance remain an open design decision.
- Future payload versions MUST be distinguishable without allowing an incompatible payload to be misread as a version 1 UUID.

### 7.3 Portability

- The format documentation MUST be sufficient for an independent tool to generate and decode the same UUID/rMQR representation.
- Exported patterns MUST use at least one open, durable representation suitable for printing or weaving without Padoma Scanner.
- A user MUST be able to copy or export the canonical UUID independently of publishing.

## 8. Functional requirements

### 8.1 Core/offline functions

The core application MUST:

1. Load as static web assets and operate without a Padoma application server.
2. Clearly indicate whether required scanner/encoder assets are ready and whether any still need to be fetched.
3. Create a project and generate a UUID locally.
4. Display the canonical UUID and render its rMQR pattern.
5. Provide a pattern view/export appropriate for transferring the module layout to weaving work.
6. Preserve the project UUID while the user navigates between generation, pattern, and scanning steps.
7. Accept a still photo or image file of a woven rMQR. Camera capture MAY use the platform's file/camera input; live video is not required for the first release.
8. Decode only supported rMQR input for verification, using raw decoded bytes rather than a barcode library's text interpretation.
9. Reject missing, malformed, non-rMQR, multiple/ambiguous, or non-16-byte payloads with a clear error.
10. Compare the decoded 16 bytes with the active project's original 16 bytes.
11. Present `match` and `mismatch` as visually and textually distinct results. A mismatch MUST show both canonical UUIDs and MUST NOT advance the project to verified.
12. Retain the original UUID after a failed scan so the user can retry.
13. Allow a verified project to be exported or saved locally without publishing.
14. Decode a woven identifier without an active project in lookup mode, while clearly distinguishing “decoded” from “verified against this project's original UUID.”
15. Avoid sending captured images or UUIDs over the network during core processing unless the user deliberately invokes a disclosed online action.

A deployed static app MAY cache its HTML, JavaScript, WebAssembly, fonts, and other required assets for reliable offline reuse. “Static-browser-first” does not imply that a first-ever visit can load uncached assets without a network connection; the offline installation/caching promise must be stated accurately.

### 8.2 Optional lookup functions

- After a successful standalone decode, the application SHOULD offer to copy the UUID and perform an exact search.
- Lookup MUST preserve the full UUID as the key; it MUST NOT use prefixes or fuzzy matching as identity matches.
- The interface MAY query the Padoma index, a general search engine, alternate indexes, or user-configured sources.
- Failure to find a page MUST be reported as “not found in the selected source,” not as evidence that the garment or UUID is invalid.
- Direct navigation to a known garment-page URL MUST remain useful without Padoma Scanner or the Padoma index.

### 8.3 Optional GitHub publishing

The proposed publishing flow is:

1. From a verified project, the artisan selects **Publish**.
2. The application explains that publishing is online, identifies the destination owner/repository/branch/path, lists the data to be sent, and requests confirmation.
3. GitHub presents and owns the login and consent UI. Padoma Scanner and Padoma.net MUST NOT request, receive, or handle the artisan's GitHub password.
4. A secure authorization-code/token exchange obtains authorization without embedding a client secret in static HTML.
5. The artisan selects or confirms a repository they own or administer and grants narrowly scoped access.
6. The application creates or updates content through GitHub's API. The intended files and overwrite behavior MUST be previewed before the write.
7. GitHub Pages publishes the repository content, subject to GitHub's build and deployment behavior.
8. The application polls or retries within a bounded period, then checks that the expected public URL is live.
9. The live check MUST confirm that the fetched page associates the exact canonical UUID with the expected URL before the publication is marked successful.
10. Only after that success MAY the artisan opt into, or a previously disclosed workflow perform, submission of the UUID and URL to a public Padoma index.

Additional requirements:

- Publishing MUST be optional and separable from verification.
- Manual repository editing, command-line publishing, and alternate publishing tools MUST remain supported paths.
- The artisan MUST be able to learn what was written, obtain the commit or change reference, and retry safely.
- Repeated publish attempts SHOULD be idempotent and MUST avoid creating duplicate garment records without confirmation.
- Existing content MUST NOT be overwritten silently.
- Repository access MUST be limited to the repositories and operations needed for the chosen action.
- Revoking authorization MUST NOT make the already published page or physical UUID unusable.

### 8.4 Optional Padoma index submission

- The index entry MUST contain at minimum the exact UUID and a public HTTPS URL.
- Submission MUST occur only after the live-page check succeeds.
- The index service SHOULD verify that the target page contains the exact UUID before accepting or activating an entry.
- The service MUST define conflict, update, removal, abuse-reporting, and stale-link behavior before production use.
- The index response MAY provide immediate confirmation that the mapping is discoverable through that index.
- The UI MUST NOT describe index acceptance as Google indexing or as universal registration.
- Public index pages SHOULD expose crawlable links. Sitemap generation and Search Console submission MAY be used where applicable.
- The product MUST state that search engines choose whether and when to crawl and index pages. Google's general Indexing API MUST NOT be presented as an appropriate route for ordinary garment pages.

## 9. Workflow and state transitions

### 9.1 Project state model

| State | Entry condition | Allowed next states | Notes |
|---|---|---|---|
| `no-project` | App opened without a project | `generated`, `lookup` | No identifier exists yet. |
| `generated` | UUID created and saved locally | `pattern-ready`, `abandoned` | Original bytes become immutable for this project. |
| `pattern-ready` | rMQR rendered/exportable | `awaiting-scan`, `abandoned` | Artisan can begin or continue weaving. |
| `awaiting-scan` | Pattern has been presented for making | `scan-failed`, `mismatch`, `verified` | Physical work happens outside the app. |
| `scan-failed` | No valid supported payload decoded | `awaiting-scan` | Original identifier is preserved. |
| `mismatch` | Valid UUID decoded but bytes differ | `awaiting-scan` | Never treated as verification. |
| `verified` | Decoded bytes exactly equal original bytes | `publish-draft`, `complete-local` | Band may now be recorded as verified and stitched into the garment. |
| `complete-local` | User finishes without online publishing | `publish-draft` | Export/manual publishing remains possible. |
| `publish-draft` | Garment content prepared | `authorization`, `complete-local` | Preview destination and changes. |
| `authorization` | GitHub flow started | `publishing`, `publish-failed`, `publish-draft` | Login/consent occurs on GitHub. |
| `publishing` | Authorized API write/build in progress | `live-check`, `publish-failed` | Network-dependent. |
| `live-check` | GitHub change accepted | `published`, `publish-failed` | Exact UUID and expected URL are checked. |
| `published` | Public page passes live check | `index-submission`, `complete` | Publication does not imply search-engine indexing. |
| `index-submission` | Optional index action in progress | `indexed-by-padoma`, `index-failed`, `complete` | Does not block the garment page. |
| `indexed-by-padoma` | Padoma index accepted mapping | `complete` | Confirms only Padoma index availability. |
| `complete` | User finishes workflow | — | Local record/export remains usable. |

`lookup` is independent of project verification: a scanner can decode a UUID and search for it, but the UI MUST NOT label that result “verified” unless it was compared with the immutable original UUID of an active project.

### 9.2 Physical workflow

1. The artisan generates a UUID and rMQR pattern.
2. The artisan hand-weaves the pattern into a band.
3. The artisan photographs or scans the finished weaving with Padoma Scanner.
4. Padoma Scanner decodes the identifier and performs the exact comparison.
5. If it matches, the artisan stitches the band into the unique hand-woven garment.
6. The UUID remains the garment's permanent physical identifier.
7. The artisan may publish and maintain a web page keyed by that UUID.

The app cannot enforce the ordering of physical actions. Its records and language should make the intended order clear without claiming to observe stitching or garment construction.

## 10. Architecture and components

### 10.1 Static client

The static client contains:

- **Project manager:** creates, resumes, exports, and abandons local projects.
- **UUID module:** generates UUIDs and converts between canonical strings and 16-byte values.
- **rMQR encoder:** converts the 16-byte payload to a selected rMQR module matrix and image/pattern representation.
- **Capture/import UI:** obtains still images from a camera or file picker.
- **rMQR decoder:** detects rMQR and returns raw bytes. The existing experiment uses `zxing-wasm` and the format name `rMQRCode`; the production dependency and pinned version require validation.
- **Verifier:** validates the payload contract and performs a constant, exact byte comparison with the active project UUID. Timing-attack resistance is not material here, but comparison semantics must be unambiguous.
- **Local persistence/export:** stores or exports project state without requiring an account.
- **Publishing client:** prepares content and, after explicit authorization, calls GitHub APIs using short-lived credentials.
- **Lookup client:** copies/searches a decoded UUID using optional online sources.

Production deployment SHOULD bundle or self-host core runtime dependencies rather than rely solely on unpinned third-party CDN URLs. If dependencies are fetched, versions and integrity policy must be defined and the UI must not overstate offline readiness.

### 10.2 Minimal authorization service

A fully static client must not embed a confidential OAuth client secret. Padoma.net may therefore provide a minimal service solely for secure authorization and token handling. The preferred design SHOULD evaluate a GitHub App because it can use narrowly scoped repository permissions and short-lived installation access tokens.

The service should:

- initiate or complete an authorization-code flow with PKCE where supported and appropriate;
- keep client secrets and GitHub App private keys server-side;
- validate `state`, redirect URI, and other anti-forgery controls;
- request the minimum repository permissions required to create/update the chosen content;
- issue or relay short-lived, narrowly scoped credentials rather than long-lived broad personal access tokens;
- avoid persistent token storage unless a separately specified feature requires it;
- redact authorization codes, tokens, and secrets from logs;
- expose no endpoint that accepts a GitHub password;
- return actionable, non-sensitive errors to the static client.

The exact GitHub authorization mechanism, token custody model, and browser-to-service session design remain open decisions and require a threat-model review.

### 10.3 GitHub repository and Pages

The artisan's repository is the source of truth for published content in this workflow. A publisher adapter creates or updates the agreed file(s), records the canonical UUID, and observes GitHub's deployment status or checks the resulting Pages URL.

Repository schema, branch strategy, content format, commit authorship, Pages configuration, and support for existing site generators are intentionally unspecified pending the open questions below.

### 10.4 Optional Padoma services

Padoma.net may host:

- the minimal authorization/token-exchange service;
- a public UUID-to-URL index and its submission/validation API;
- crawlable index pages and sitemaps;
- static copies of Padoma Scanner assets.

Core identification and verification MUST continue to work if all these services are unavailable.

## 11. Security and privacy

### 11.1 Local data

- UUIDs are public identifiers once woven or published; they MUST NOT be presented as secrets or authentication factors.
- Captured images may reveal a garment, workspace, people, location metadata, or other sensitive context. Core scanning SHOULD process them locally and SHOULD discard image buffers after processing unless the user explicitly saves them.
- The application SHOULD avoid retaining original photo metadata by default.
- Local project storage and export behavior MUST be disclosed, including how to delete a project.
- The app MUST not claim that “no data leaves the device” while online publishing, lookup, remote fonts, telemetry, or dependency fetching is occurring.

### 11.2 Publishing authorization

- GitHub MUST own the login and consent surfaces.
- Padoma components MUST never collect GitHub passwords.
- No client secret or GitHub App private key may appear in static assets.
- Tokens MUST be scoped narrowly, transmitted only over HTTPS, kept out of URLs and logs, and cleared when no longer needed.
- Cross-site request forgery, authorization-code interception, malicious redirects, token replay, and confused-deputy risks MUST be addressed in the selected flow.
- Repository owner, repository, branch, path, and exact proposed changes MUST be visible before a write.
- Content derived from user input MUST be escaped or sanitized for its target format to prevent script injection in published pages.

### 11.3 Identifier integrity and claims

- A match proves only that the scanned payload equals the project's generated payload.
- A public page's inclusion of a UUID does not by itself prove authorship, ownership, or authenticity.
- The public index must anticipate duplicate claims and malicious URLs. It MUST NOT silently choose one claimant as authentic without a separately defined trust model.
- Scanned URLs, if any future format permits them, MUST NOT be opened automatically. Version 1 accepts only a 16-byte UUID payload.

## 12. Failure handling

| Failure | Required behavior |
|---|---|
| Random UUID generation unavailable | Block creation, explain that secure generation is unavailable, and do not fall back to weak randomness. |
| Encoder unavailable or rejects configuration | Preserve the UUID/project, report the error, and allow retry/export of the UUID. |
| Required static/WASM asset unavailable | Distinguish “not downloaded” from a scan failure; offer retry when online. |
| Camera permission denied or camera absent | Offer file selection and instructions; do not lose project state. |
| No rMQR detected | Report unreadable/no symbol, retain original UUID, and allow another image. |
| Multiple rMQR symbols detected | Require the user to choose or retake; never guess which one is the garment identifier. |
| Payload length or format invalid | Report unsupported/invalid identifier; do not compare or verify. |
| Valid decoded UUID mismatches | Show both UUIDs, mark mismatch, prohibit verified transition, and allow retry. |
| Browser/project data lost | Explain recovery limits; imports/exports should restore the original UUID where supported. Never recreate it silently. |
| Authorization denied/cancelled | Return to publish draft without affecting local verification or existing pages. |
| Authorization service unavailable | Preserve the draft and offer retry or manual/alternate publishing instructions. |
| GitHub API permission or rate-limit error | Explain the affected operation, preserve the draft, and avoid blind repeated writes. |
| Destination file already exists | Preview a merge/update or require a new destination; never overwrite silently. |
| Commit succeeds but Pages build fails | Report partial success, link to the repository/change where possible, and do not mark published. |
| Pages deployment is delayed | Use bounded polling and a resumable pending state; do not report failure as a rollback of a successful commit. |
| Live page lacks or misstates UUID | Mark live check failed and withhold automatic index submission. |
| Padoma index submission fails | Keep the garment page marked published; allow retry or alternate indexing. |
| Search engine has not indexed the page | Explain that crawling is external and asynchronous; provide the direct URL and crawlability guidance. |

## 13. Decentralization invariants

The following are release-blocking invariants, not aspirational features:

1. A UUID is generated in the browser and is valid without registration.
2. The UUID/rMQR payload format is openly documented and implementable by third parties.
3. Core rendering, decoding, and verification do not call a Padoma.net application API.
4. An artisan can export the UUID and pattern and continue without Padoma Scanner.
5. An artisan can publish manually or with a different tool and host the garment page anywhere.
6. GitHub and GitHub Pages are one proposed adapter, not part of the identifier format.
7. The artisan, not Padoma.net, owns the repository and published page in the proposed GitHub flow.
8. A garment page remains directly usable and linkable without an entry in the Padoma index.
9. Alternate public or private indexes can map the same exact UUID to pages.
10. Padoma index failure, removal, or shutdown does not invalidate the UUID, woven band, exported project, or garment page.
11. No Padoma service is the sole holder of information needed to decode or compare the identifier.
12. Search-engine visibility is additive discovery, never the definition of validity.

## 14. Acceptance criteria

### 14.1 Core workflow

- With network requests blocked after the required static assets are locally available, a supported browser can generate a fresh UUID, render its rMQR, import/capture a test image, decode it, and verify an exact match.
- A conformance fixture generated from a known UUID decodes to exactly the same 16 bytes and canonical UUID.
- A fixture containing a different valid UUID yields `mismatch`, never `verified`.
- A non-rMQR image, an unreadable woven sample, a non-16-byte rMQR payload, and an image containing multiple candidate symbols each produce distinct non-success outcomes.
- Retrying any failed scan preserves the original UUID.
- Standalone lookup mode can decode and copy a UUID but does not claim project verification.
- Network inspection confirms that capture and core decoding do not upload the image or UUID.
- Project export contains the UUID, payload/format version, rMQR configuration, and sufficient pattern data or representation for independent use.
- An independent implementation can reproduce and decode at least one published format test vector.

### 14.2 Publishing

- Selecting Publish identifies it as an online operation and previews the target and outgoing garment data.
- The user authenticates and consents on GitHub-controlled UI; no Padoma page contains a GitHub password field.
- Inspection of deployed static assets finds no OAuth client secret, GitHub App private key, or long-lived access token.
- The granted installation/repository permissions are limited to the selected publishing use case.
- On approval, the workflow creates or updates the previewed content in the selected artisan-owned repository and exposes the resulting change reference.
- Cancelled consent or failed authorization leaves local verification and the publish draft intact.
- Existing destination content is not overwritten without explicit confirmation.
- A publish is marked successful only after the public URL responds and its content associates the exact UUID with that page.
- Repeating a successful publish updates or confirms the same garment record rather than silently creating a duplicate.

### 14.3 Indexing and discovery

- Padoma index submission cannot precede a successful live-page check.
- A successful submission makes the exact UUID-to-URL mapping queryable in the Padoma index and clearly labels that result as Padoma-index discovery.
- Index failure does not change the published status of the garment page.
- Product copy makes no promise of immediate or guaranteed Google indexing and does not direct ordinary garment pages to Google's general Indexing API.
- A published garment page is accessible directly and includes crawlable navigation or is referenced by an appropriate sitemap/index path where the chosen site structure supports it.

### 14.4 Decentralization

- A documented manual path can publish an equivalent garment page without the Padoma authorization service.
- A page hosted outside GitHub Pages can represent the same UUID and be used directly.
- Disabling all Padoma.net endpoints does not prevent local generation, pattern export, decoding, comparison, or access to already published third-party pages.
- A third-party scanner/index can use the open UUID/rMQR contract without a Padoma account or API key.

## 15. Open questions

These decisions require validation; this specification does not invent answers for them.

### Physical format and decoding

- Which rMQR sizes, aspect ratios, and error-correction levels are practical for the intended band widths, yarns, weave structures, and camera conditions?
- Should the first release select one fixed symbol configuration or allow a constrained set?
- What quiet-zone, contrast, orientation, scale, and module-shape guidance produces reliable hand-woven scans?
- What physical test corpus and minimum decode success rate define production readiness?
- Should verification accept only a newly captured image or also imported files, and how should each be labeled?
- Is raw 16-byte UUID payload sufficient for long-term versioning, or is an explicit envelope/version marker required before format freeze?
- Which UUID version should be normative? UUIDv4 matches the current experiments, but the product decision should be explicit.

### Local projects and portability

- Should projects live in IndexedDB, downloadable files, both, or another browser storage model?
- What is the export file format, and should it include scan evidence, timestamps, notes, and checksums?
- How should users move a project between phone and desktop without creating a mandatory account or cloud service?
- What accessibility requirements apply to the pattern display and match/mismatch cues?
- Which browsers and device versions are supported, and what offline caching/install behavior is promised?

### Garment content and publishing

- What minimum garment metadata is required, optional, or prohibited?
- What repository layout and content format should the default GitHub adapter use?
- Should Padoma Scanner create a new repository, use an existing repository, or support both?
- How are existing static-site generators, default branches, pull requests, protected branches, and Pages configurations handled?
- Does publishing write directly, create a branch and pull request, or offer both modes?
- What stable public URL structure maps UUIDs to pages?
- What machine-readable metadata should a garment page expose so live checks and independent indexes can verify the UUID association?

### Authentication and token handling

- Is a GitHub App the final choice, and what exact permissions and installation flow are required?
- Can the selected GitHub flow use PKCE end to end, or must the minimal service hold an app secret and exchange codes?
- Does the browser ever receive an installation token, or should the service proxy narrowly defined repository operations?
- What session lifetime, token revocation, audit logging, rate limiting, and abuse controls are required?
- Who operates the minimal service, and what availability and privacy commitments apply?

### Index governance and discovery

- Is Padoma index submission explicit opt-in per publish, a remembered preference, or an inseparable disclosed step in a particular publish mode?
- How does the public index resolve multiple URLs or conflicting claims for one UUID without presenting itself as an authenticity authority?
- How are entries updated, removed, appealed, rate-limited, and protected from malicious links?
- What proof, if any, beyond presence of the UUID on the live page is required to add or update a mapping?
- What crawlable index-page and sitemap structures balance discovery, privacy, and scale?

## 16. Prototype notes and implementation caution

The repository currently supplies useful experiments:

- `bandgrinder/bandgrinder.html` captures or selects a still image and attempts client-side rMQR decoding with `zxing-wasm`.
- `bandgrinder/bandgrinder_reader_webapp_spec.md` documents that prototype's reader API and its raw-byte UUID conversion.
- `bandgrinder/bandgrinder.py` and `bandgrinder/generate_uuid_rmqr_variants.py` experiment with encoding 16 UUID bytes into rMQR symbols and generating size/error-correction variants.

These files ground the version 1 payload proposal but do not settle production library choice, dependency delivery, supported symbol configuration, offline packaging, browser support, physical scan reliability, security controls, or any publishing/index service design. Implementation should begin only after the relevant open questions have explicit decisions and test fixtures.
