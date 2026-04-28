---
name: adobe-resize-photos-and-videos
description: >
  Resize photos and videos to exact pixel dimensions or aspect ratios using Adobe tools.
  Use this skill whenever a user wants to resize, scale, or change the dimensions of an image
  or video file — including phrases like "resize this to 1920x1080", "make this 4K", "scale
  to 800x600", "change the aspect ratio to 16:9", "resize my video", "make the image smaller",
  "crop to square", "fit this to a specific size", "resize for print", "resize for web",
  "make it 300 DPI ready", "change canvas size", "resize a batch of photos", or any request
  specifying target dimensions (W×H, ratio, or named size like "4K", "HD", "A4").
  Also triggers for: "make this fit a specific size", "resize to [any dimension]",
  "I need this at [WxH]", "scale my video down", "change resolution", "downscale", "upscale".
  NOT for social media platform sets (use adobe-create-social-variations for that).
  Uses image_crop_and_resize for photos, video_resize for videos.
license: Apache-2.0
metadata:
  version: 1.0.0
  visibility: public
---

# Adobe Resize Photos and Videos

Resizes images or videos to user-specified dimensions, aspect ratio, or named size.
For social media platform sets (Instagram, TikTok, etc.) → use the `adobe-create-social-variations` skill instead.

---

## Step 0 - prereq: Initialize Adobe Tools
Call `adobe_mandatory_init` first. This returns file handling rules and tool routing guidance required for the rest of the workflow.

```json
{ "skill_name": "adobe-resize-photos-and-videos", "skill_version": "1.0.0" }
```

---

## IMMEDIATE ACTION REQUIRED

**Step 1:** If parameters are missing or ambiguous → run the multi-step intake (Step 0 below).
**Step 2:** If no file uploaded, call `asset_add_file({})`.
**Step 3:** Detect image vs. video → route to the correct workflow.

---

## Step 0 — Multi-Step Intake

Run this when the user hasn't provided complete parameters (type + dimensions + fit mode).
Skip entirely if the user's message already contains all three.

Use `AskUserQuestion` to collect parameters step by step.

### Step 0a — Type

```
AskUserQuestion([{
  question: "Photo or video?",
  type: "single_select",
  options: ["Photo", "Video"]
}])
```

### Step 0b — Dimensions

**If Photo** (`multi_select` — user can pick one or more):
```
AskUserQuestion([{
  question: "Dimensions — select all you need",
  type: "multi_select",
  options: [
    "1080 × 1080 — Instagram square",
    "1080 × 1350 — Instagram portrait",
    "1080 × 1920 — Stories / Reels",
    "1920 × 1080 — YouTube / landscape",
    "1280 × 720 — YouTube thumbnail",
    "1200 × 675 — X / Twitter post",
    "1200 × 630 — Facebook / OG image",
    "1080 × 566 — LinkedIn post",
    "2560 × 1440 — YouTube banner",
    "3840 × 2160 — 4K / UHD",
    "400 × 400 — Profile / avatar",
    "2480 × 3508 — A4 print (300 dpi)",
    "Custom — I'll type it"
  ]
}])
```

If user includes "Custom" → follow up: "Enter your custom dimensions (e.g. 1500×800):"

If user selects multiple presets → run `image_crop_and_resize` once per dimension,
using the same source URI and parameters each time. Preview all outputs together at the end.

**If Video** (`multi_select` — user can pick one or more):
```
AskUserQuestion([{
  question: "Dimensions — select all you need",
  type: "multi_select",
  options: [
    "1080 × 1920 — Reels / TikTok / Stories",
    "1920 × 1080 — YouTube / landscape",
    "1080 × 1080 — Square post",
    "1280 × 720 — YouTube 720p",
    "3840 × 2160 — 4K / UHD",
    "854 × 480 — SD / 480p",
    "Custom — I'll type it"
  ]
}])
```

If user selects multiple video presets → submit a separate `video_resize` job per dimension,
poll each to completion, preview all outputs together.

### Step 0c — Fit mode

**If Photo** (`single_select`):
```
AskUserQuestion([{
  question: "Fit mode",
  type: "single_select",
  options: [
    "Reframe — crop to fill",
    "Pad — letterbox, no crop",
    "Extract — isolate subject"
  ]
}])
```

**If Video** (`single_select`):
```
AskUserQuestion([{
  question: "Fit mode",
  type: "single_select",
  options: [
    "Letterbox — preserve ratio",
    "Crop — fill, no bars",
    "Stretch — force exact (distort)"
  ]
}])
```

### Step 0d — Smart focus (Photo only)

```
AskUserQuestion([{
  question: "Smart focus — where should the crop center?",
  type: "single_select",
  options: [
    "Subject",
    "Face / portrait",
    "Upper body",
    "Center (geometric)",
    "Named object — I'll describe it"
  ]
}])
```

If user selects "Named object" → follow up: "Describe the object (e.g. 'the red car', 'the logo'):"

### Step 0e — Options (Photo only)

```
AskUserQuestion([{
  question: "Any additional options?",
  type: "multi_select",
  options: [
    "Batch — multiple images",
    "Output: JPEG",
    "Output: PNG"
  ]
}])
```

### Step 0f — Source (Video only)

```
AskUserQuestion([{
  question: "Where is the video?",
  type: "single_select",
  options: [
    "Upload from device",
    "From Creative Cloud"
  ]
}])
```

---

## Step 1 — Get the Source File

**Critical — `/mnt/user-data/uploads/` paths are NOT usable URLs.**
Even when the user has attached a file and it appears in context at a `/mnt/user-data/uploads/` path,
you cannot pass this path to any Adobe tool. Call `asset_add_file()` to stage the file — `/mnt/user-data/uploads/` paths are not fetchable by Adobe tools.

```
WRONG  ❌  imageURI: "/mnt/user-data/uploads/photo.jpg"
WRONG  ❌  imageURI: "file:///mnt/user-data/uploads/photo.jpg"
CORRECT ✅  call asset_add_file() → use presignedAssetUrl from picker context
```

**No file yet** → open the picker immediately:
```javascript
asset_add_file()
```

Detect type from returned `mediaType`:
- `image/*` → IMAGE WORKFLOW
- `video/*` → VIDEO WORKFLOW

---

## Step 2 — Resolve Target Dimensions

| User says                    | Resolve to                                      |
| ---------------------------- | ----------------------------------------------- |
| `1920×1080`, `1920x1080`     | width: 1920, height: 1080                       |
| `4K`                         | 3840 × 2160                                     |
| `HD`, `1080p`                | 1920 × 1080                                     |
| `720p`                       | 1280 × 720                                      |
| `480p`                       | 854 × 480                                       |
| `A4` print                   | 2480 × 3508 (300 DPI portrait)                  |
| `Letter` print               | 2550 × 3300 (300 DPI portrait)                  |
| `16:9`, `1:1`, `4:5`, `9:16` | ratio string → pass as `output: "16:9"`         |
| `square`                     | `output: "1:1"`                                 |
| Width only (`800px wide`)    | width: 800, use ratio string to maintain aspect |

If no target was specified in the form AND none in the user's message → ask:
> "What dimensions do you need? (e.g. 1920×1080, A4, 16:9)"

---

## IMAGE WORKFLOW

### Step 3 (Image) — Valid URI Sources

Only these work as `imageURI`:
- `presignedAssetUrl` from `asset_add_file()` ✅
- `outputUrl` from a prior tool call ✅
- Public HTTPS URL provided by user ✅

Not usable as `imageURI`:
- `/mnt/user-data/uploads/` paths ❌
- `renditionURL` from `asset_search` directly ❌
- `file://` URIs ❌

| Source            | Resolution                                                             |
| ----------------- | ---------------------------------------------------------------------- |
| Uploaded file     | `asset_add_file()` → `presignedAssetUrl`                               |
| CC storage asset  | `asset_search` → re-stage via `asset_add_file()` → `presignedAssetUrl` |
| Prior tool output | Use `outputUrl` directly                                               |
| PSD / AI file     | `document_render_vector` (JPEG, 300 DPI) → `outputPresignedUrl`        |

---

### Step 4 (Image) — Fit Mode

| Intent                                   | Mode      | Notes                                                  |
| ---------------------------------------- | --------- | ------------------------------------------------------ |
| "resize to WxH" / default                | `reframe` | Largest crop at target ratio, centered — no distortion |
| "no cropping", "letterbox", "fit inside" | `pad`     | Fills empty space with white                           |
| "isolate subject", "tight crop"          | `extract` | Tight crop around detected region                      |

**Default: `reframe`.** Change only when user is explicit.

> ⛔ `fit: "extract"` is incompatible with an explicit `{ width, height }` — it stretches the image. Use a ratio string or omit `output`.

---

### Step 5 (Image) — Call `image_crop_and_resize`

```javascript
image_crop_and_resize({
  imageURI: presignedAssetUrl,
  options: {
    output: { width: 1920, height: 1080 },  // or "16:9"
    fit: "reframe",
    focus: "subject",  // or "face", "upper_body", { prompt: "the car" }, { x:0.5, y:0.5 }
    quality: 7
  },
  outputFileType: "jpeg"  // or "png" if transparency needed
})
// result.outputUrl → use for preview or chaining
```

**Focus guide:**
- `"subject"` — default; full-body detection, landscapes, objects
- `"face"` — portraits, headshots
- `"upper_body"` — chest-up crops
- `{ prompt: "the logo" }` — named object from user's form input
- `{ x: 0.5, y: 0.5 }` — geometric center (no clear subject)

---

### Step 6 (Image) — Batch

If batch was selected in the form OR the user provided multiple files:
1. Call `asset_add_file()` for each file to get individual presigned URLs
2. Call `image_crop_and_resize` for each with the same parameters
3. Collect all `outputUrl` values
4. Call `asset_preview_file` with all outputs in a single call

> Calls run sequentially in this environment. For >10 images, confirm with the user before starting.

**Pagination across turns (batches >20):**
For large batches, the conversation context may fill before all images are processed,
causing Claude to pause mid-batch. This is expected — not an error. When it happens:
- State how many have been completed and how many remain (e.g. "20 / 24 done — say 'continue' for the rest")
- Wait for the user to confirm before resuming
- On resume, pick up from the next unprocessed image and continue to the end
- Preview all outputs together only after the final image completes

---

### Step 7 (Image) — Preview + Deliver + Firefly Board

```javascript
asset_preview_file({
  assets: [
    { name: "photo_1920x1080.jpg", presignedAssetUrl: result.outputUrl },
    // all successful outputs
  ]
})
```

#### Save to CC + Create Firefly Board

After preview, upload each output to CC storage using the block upload pipeline
(`asset_initialize_file_upload` → PUT chunk → `asset_finalize_file_upload`).

Then call the firefly board tool with the final output urls:

```javascript
create_firefly_board({
  import_adobe_storage: [
    final_output_url_1,
    final_output_url_2,
    // ...
  ]
})
```

> ✅ **Confirmed working (Stage):** `import_adobe_storage` with presigned URLs from `asset_finalize_file_upload` successfully populates boards.
>
> ❌ **Does not work:** `import_generic_assets` with CC URNs (`urn:aaid:sc:US:...`) — USS indexing lag causes blank boards.
>
> If board creation fails or the URL is malformed, omit the board link (retrying does not help).

Post the completion summary after the board step:

```
✅ Done! [N] image(s) resized and ready.

📥 Download:
• resized_1920x1080.jpg → <cc_storage_url>
[list individually if N ≤ 3, or single folder link if N > 3]

🎨 View in Firefly Board → <board_url>   ← omit if board creation failed
```

---

## VIDEO WORKFLOW

### Step 3 (Video) — Get Asset ID

Video tools require `assetId`, not a URL.

| Source                      | How                                                                   |
| --------------------------- | --------------------------------------------------------------------- |
| Upload via `asset_add_file` | Use returned `assetId`                                                |
| CC storage                  | `asset_search` with `filters.mediaType: "video/mp4"` → use asset `id` |

---

### Step 4 (Video) — Common Targets

| Name          | Dimensions  |
| ------------- | ----------- |
| 4K / UHD      | 3840 × 2160 |
| 1080p / HD    | 1920 × 1080 |
| 720p          | 1280 × 720  |
| 480p          | 854 × 480   |
| Vertical 9:16 | 1080 × 1920 |
| Square 1:1    | 1080 × 1080 |

---

### Step 5 (Video) — Call `video_resize`

> ⚠️ `resizeVideoPoll` is a **deferred tool** — load it first before attempting to poll.
> Direct calls without loading will fail with "not loaded" error.

```javascript
video_resize({
  assetId: videoAssetId,
  width: targetW,
  height: targetH,
  mode: "letterbox"  // default; see mode table below
})
// Returns { jobStatus: "pending", statusId }
```

**Mode — use exact API values (not user-facing labels):**
| User says                            | API value     | Behavior                                   |
| ------------------------------------ | ------------- | ------------------------------------------ |
| "fit", "preserve ratio", "letterbox" | `"letterbox"` | Preserves ratio, adds black bars (default) |
| "fill", "crop to fill", "no bars"    | `"crop"`      | Crops edges to fill target exactly         |
| "stretch", "force exact"             | `"stretch"`   | Distorts to exact target                   |

> ℹ️ **Auto-reframe for video is not available in Claude yet**, but new tools are being added all the time. If you need more control, try using Adobe Premiere.

**Polling:** load the deferred tool `resizeVideoPoll` before calling it — direct calls fail with "not loaded".
```javascript
// Step 1: load the deferred tool resizeVideoPoll
// Step 2: poll until complete
resizeVideoPoll({ statusId })
// Repeat until jobStatus === "completed"
// Show progress % to user while waiting
```

---

### Step 6 (Video) — Preview + Deliver + Firefly Board

If polling succeeds and returns `outputUrl`, upload to CC storage via the block upload pipeline
(`asset_initialize_file_upload` → PUT → `asset_finalize_file_upload`) to get a presigned URL, then:

```javascript
asset_preview_file({
  assets: [{ name: "resized_video.mp4", presignedAssetUrl: result.outputUrl }]
})

create_firefly_board({
  import_adobe_storage: [ presignedAssetUrl_from_finalize ]
})
```

> ✅ Use `import_adobe_storage` with the finalize presigned URL. If board creation fails, omit the link.

```
✅ Done! Video resized to [WxH].

📥 Download → <cc_storage_url>

🎨 View in Firefly Board → <board_url>   ← omit if board creation failed
```

If polling is unavailable → skip preview, deliver the CC storage fallback message from Step 5.

---

## Error Handling

| Error                                                | Action                                                                                            |
| ---------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| `/mnt/user-data/uploads/` or `file://` passed as URI | Stop. Call `asset_add_file()` first.                                                              |
| Image too large after resize                         | Re-run with `quality: 5`                                                                          |
| Video `assetId` not found                            | Re-upload via `asset_add_file`                                                                    |
| Source too small for target                          | Warn user upscaling won't add detail; proceed if confirmed                                        |
| Invalid `video_resize` mode                          | API only accepts `"letterbox"`, `"crop"`, or `"stretch"` — `"fit"` and `"fill"` will be rejected. |
| `extract` + `{W,H}` → stretching                     | Switch to `reframe`                                                                               |
| No dimensions given                                  | Render form or ask explicitly before calling any tool                                             |
| Unsupported format                                   | Ask user to export as JPG/PNG (images) or MP4 (video)                                             |
| `resizeVideoPoll` not loaded / unavailable           | Known gap in current connector. Skip polling. Tell user to check CC Files for output.             |

---

## Common Dimension Reference

| Use Case                  | Dimensions  |
| ------------------------- | ----------- |
| Full HD / web hero        | 1920 × 1080 |
| 4K                        | 3840 × 2160 |
| Web thumbnail             | 1280 × 720  |
| Square                    | 1080 × 1080 |
| A4 print (300 DPI)        | 2480 × 3508 |
| US Letter print (300 DPI) | 2550 × 3300 |
| Blog featured image       | 1200 × 630  |
| Email header              | 600 × 200   |
| Avatar / profile          | 400 × 400   |
| Instagram portrait        | 1080 × 1350 |
| Stories / Vertical        | 1080 × 1920 |

---

## Assets

`assets/intake-form.html` — Interactive intake form for resize parameters.
Render at the start of any resize workflow where parameters are missing or ambiguous.
Covers photo (target size, fit mode, smart focus, batch, output format) and video (target size, fit mode, source).
