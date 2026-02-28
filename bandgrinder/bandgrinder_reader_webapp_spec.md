# rMQR Code Reader — Specification

## Overview

A minimal, single-file HTML webpage that allows a user to take a photo using their mobile device's camera, scan it for an rMQR code, and display the decoded UUID on screen. All processing happens client-side with no backend required.

---

## Technology

### zxing-wasm

The page uses [`zxing-wasm`](https://www.npmjs.com/package/zxing-wasm) v1, a WebAssembly build of the ZXing-C++ barcode library. It supports rMQR codes (ISO/IEC 23941).

- Loaded via jsDelivr CDN as an **IIFE script** — no build step or bundler needed
- The IIFE exposes a `ZXingWASM` global with three relevant methods:
  - `setZXingModuleOverrides(overrides)` — configures the WASM module before loading
  - `getZXingModule()` — pre-warms the WASM module (returns a Promise)
  - `readBarcodesFromImageFile(file, options)` — decodes barcodes from a `File` or `Blob`
- Only the reader build is used (`dist/iife/reader/index.js`) since we are decoding only, not generating
- The `.wasm` binary (~919 KB) is fetched separately on first use

#### CDN script tag

```html
<script src="https://cdn.jsdelivr.net/npm/zxing-wasm@1/dist/iife/reader/index.js"></script>
```

#### WASM binary location

The `.wasm` binary is **not** co-located with the JS file — it must be explicitly pointed at using `locateFile` inside `setZXingModuleOverrides`. The correct base path is `dist/reader/` (not `dist/iife/reader/`):

```js
ZXingWASM.setZXingModuleOverrides({
  locateFile: (path, prefix) => {
    if (path.endsWith('.wasm')) return baseUrl + path;
    return prefix + path;
  },
});
```

#### CDN fallback

Two CDN sources are tried in order for the `.wasm` binary:

1. `https://fastly.jsdelivr.net/npm/zxing-wasm@1/dist/reader/`
2. `https://unpkg.com/zxing-wasm@1/dist/reader/`

### No backend

Everything runs in the browser. No server, no API calls, no data leaves the device.

---

## Image Capture

The page uses a standard HTML file input rather than the `getUserMedia` API:

```html
<input type="file" accept="image/*" capture="environment">
```

- On **mobile browsers**, this opens the native camera in still-photo mode pointing at the rear (environment-facing) camera
- On **desktop browsers**, this falls back to a standard file picker
- The captured photo is returned as a `File` object via the input's `change` event
- The button is visible; the file input itself is hidden and triggered programmatically via `fileInput.click()`

This approach avoids the need for a video element, a canvas, a frame-capture loop, and manual camera permission handling. It is lightweight and battery-friendly.

---

## Decoding

The `File` object from the input is passed directly to `readBarcodesFromImageFile()`. The library accepts image files natively — no canvas or pixel-extraction step is needed.

```js
const results = await ZXingWASM.readBarcodesFromImageFile(file, {
  formats: ['rMQRCode'],
  tryHarder: true,
});
```

### Critical: correct format string

The format identifier for rMQR codes in zxing-wasm v1 is **`"rMQRCode"`** (not `"rMQR"`, not `"rmqr"`). Using any other string causes the library to return `{ isValid: false, error: "This is not a valid barcode format: ..." }`.

### Result object

Each entry in the returned array has at minimum:

| Property | Type | Description |
|---|---|---|
| `isValid` | `boolean` | `true` only if a barcode was successfully decoded |
| `text` | `string` | The decoded content, interpreted as Latin-1 — **not reliable for binary content** |
| `bytes` | `Uint8Array` | The raw decoded bytes — use this for binary content |
| `bytesECI` | `Uint8Array` | Raw bytes with ECI prefix bytes prepended |
| `contentType` | `string` | `"Text"` or `"Binary"` |
| `format` | `string` | The detected barcode format (e.g. `"rMQRCode"`) |
| `error` | `string` | Error message if `isValid` is `false` |

Always check `isValid` before reading any content — the library may return a result object with `isValid: false` rather than an empty array when the format string is invalid or no code is found.

---

## UUID Encoding: Binary, Not Text

The rMQR codes in this application store UUIDs as **16 raw binary bytes** (the compact binary UUID representation), not as ASCII/UTF-8 text strings. This is more space-efficient, which matters given the limited data capacity of rMQR codes.

As a result:

- `r.contentType` will be `"Binary"`, not `"Text"`
- `r.text` will be garbled (the 16 bytes misinterpreted as Latin-1 characters) — **do not use `r.text`**
- `r.bytes` will be a `Uint8Array` of exactly 16 bytes representing the UUID

### Decoding binary UUID bytes to string

Convert the 16 bytes to hex and insert dashes in the standard UUID format (`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`):

```js
const b = r.bytes;
const hex = Array.from(b).map(x => x.toString(16).padStart(2, '0')).join('');
const uuidStr = `${hex.slice(0,8)}-${hex.slice(8,12)}-${hex.slice(12,16)}-${hex.slice(16,20)}-${hex.slice(20,32)}`;
```

---

## Initialisation Flow

On page load, the WASM module is pre-warmed so the first scan has no delay:

```js
ZXingWASM.setZXingModuleOverrides({ locateFile: ... });
await ZXingWASM.getZXingModule();
```

The button remains disabled and the status shows "Initialising…" until this resolves. On success the button is enabled and status shows "Ready". On failure the status shows "Failed to load scanner".

---

## Expected Output

The rMQR code encodes a single UUID in compact binary form (16 bytes). The page decodes this to standard UUID string format, e.g. `97e41923-8681-4f84-a075-dc652cf7d3bc`.

---

## User Flow

1. Page loads → WASM binary is fetched and module pre-warms → button disabled, status: "Initialising…"
2. WASM ready → button enabled, status: "Ready"
3. User taps **Take Picture** → native camera (or file picker on desktop) opens
4. User takes or selects a photo
5. Button is disabled, status: "Reading…"
6. `readBarcodesFromImageFile()` processes the image
7. **Success** (`isValid: true`) → 16 raw bytes converted to UUID string and displayed, status: "Decoded successfully"
8. **Failure** (empty results or `isValid: false`) → status: "No rMQR code found"
9. Button re-enabled, file input reset so the same image can be retried

---

## Page Structure

A single self-contained HTML file with no external dependencies beyond the zxing-wasm CDN script and a Google Fonts import.

### Elements

- A hidden `<input type="file">` for camera/file capture
- A visible **Take Picture** button that triggers the file input
- A status row with an animated dot indicator and status text
- A result card (hidden until a successful decode) showing the UUID

### States

| State | Button | Dot | Status text |
|---|---|---|---|
| Initialising | Disabled | Pulsing yellow | "Initialising…" |
| Ready | Enabled | Off | "Ready" |
| Processing | Disabled | Pulsing yellow | "Reading…" |
| Success | Enabled | Solid yellow | "Decoded successfully" |
| Failure | Enabled | Red | "No rMQR code found" |

---

## Styling

Minimal dark theme. IBM Plex Mono for headings, labels, and the UUID display. IBM Plex Sans for body text. Accent colour: `#e8ff47` (yellow-green). No CSS frameworks.

---

## What Is Explicitly Out of Scope

- Live video/viewfinder — still image capture is sufficient and more battery-friendly
- Barcode generation — decoding only
- Any format other than rMQR
- Any content other than a UUID
- A backend or server component
- A build pipeline or bundler
