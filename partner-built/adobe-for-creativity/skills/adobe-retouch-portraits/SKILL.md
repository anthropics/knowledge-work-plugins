---
name: adobe-retouch-portraits
description: >
  Bulk-retouch a folder of portrait photos using Adobe tools —
  designed for wedding photographers and event photographers who need fast,
  walk-away batch processing. Use this skill when the user says "retouch my
  photos", "batch process these portraits", "process my wedding photos",
  "clean up this folder of images", "run my headshots through Adobe", or
  uploads/selects a folder of photos and wants them polished and ready to
  review. Automatically applies auto-straighten, auto-tone, and auto-light
  to every image. Outputs a preview grid and download folder.
  Access: 🔐 Signed-In required | Gen AI: ❌
license: Apache-2.0
metadata:
  version: 1.0.0
  visibility: public
---

# Adobe Retouch Portraits

A walk-away bulk retouching pipeline for photographers. The user selects their
images, optionally adds tweaks, and Claude runs the full batch using Adobe
for creativity tools.

---

## Tool Reference (Adobe for creativity connector)

| Step                  | Tool                                                        | Notes                                              |
| --------------------- | ----------------------------------------------------------- | -------------------------------------------------- |
| Ingest                | `asset_add_file`                                            | Interactive file picker                            |
| Straighten            | `image_auto_straighten`                                     | Per image                                          |
| Auto-Tone             | `image_apply_auto_tone` (cameraRawFilter)                   | Per image                                          |
| Exposure              | `image_adjust_exposure`                                     | Batch (`imageURIs` array)                          |
| Highlights            | `image_adjust_highlights`                                   | Batch                                              |
| Shadows               | `image_adjust_dark_portions`                                | Batch                                              |
| Brightness/Contrast   | `image_adjust_brightness_and_contrast`                      | Batch                                              |
| Vibrance/Saturation   | `image_adjust_vibrance_and_saturation`                      | Batch                                              |
| Face detection        | `image_select_subject` with `bodyParts: ["Face"]`           | To check for face presence                         |
| Adaptive Enhancements | `image_apply_preset`                                        | Per image, opt-in (see Step 5b)                    |
| Adaptive Blur BG      | `image_apply_preset` ("Adaptive: Blur Background - Subtle") | Replaces `image_apply_lens_blur` when selected     |
| Heavy blur            | `image_apply_gaussian_blur`                                 | Per image (if user requests, no adaptive selected) |
| Crop                  | `image_crop_and_resize`                                     | Per image                                          |
| Sample preview        | `asset_preview_file`                                        | Before/after on image[0] only                      |
| Final preview         | `asset_preview_file`                                        | All final URLs directly, no resize step            |
| Firefly Board         | `create_firefly_board`                                      | Source presigned URLs from ingestion               |

---

## Step 0 - prereq: Initialize Adobe Tools
Call `adobe_mandatory_init` first. This returns file handling rules and tool routing guidance required for the rest of the workflow.

```json
{ "skill_name": "adobe-retouch-portraits", "skill_version": "1.0.0" }
```

---

## Step 1: Image Ingestion

Call `asset_add_file` with no parameters. This renders an interactive UI where
the user can:
- **Browse CC storage** and select a folder or individual files
- **Upload from device** (local files)
- **In Cowork**: select a local folder path directly
```
Tool: asset_add_file
Params: {}
```

**Important:** `asset_add_file` returns `imageURIs: []` — this is expected and
NOT an error. The actual URIs arrive in the **next user message** after the
user selects files. Wait for that follow-up before continuing.

---

## Step 2: Announce Pipeline + Offer Options

Once URIs are obtained, check whether the user's message **already fully specifies** their enhancement, tweak, and crop preferences.

**If preferences are fully stated upfront** (e.g. "retouch with subject pop, no tweaks, crop 1:1"), skip `AskUserQuestion` entirely and go straight to the confirmation message. Map their stated preferences using the button→parameter table below.

**If preferences are not fully stated** (e.g. "please retouch them" with no further detail), post this message first:
```
📸 Got [N] photo(s)! The default pipeline will auto-straighten and auto-tone every image.

Let me know if you'd like any extras 👇
```

Then call `AskUserQuestion` with these three questions:

```
Question 1 (multi_select):
  question: "✨ Adaptive AI enhancements (select any — or none to skip)"
  options:
    - "All"
    - "Subject Pop — boost contrast & vibrance on the person"
    - "Warm Pop — warm, glowing subject lift"
    - "Whiten Teeth — brightens teeth (smiles only)"
    - "Blur Background — subtle bg blur, respects edges"
    - "Sky Drama (Blue) — deepen sky blue, outdoor only"
    - "Sky Drama (Dark) — moody dramatic sky, outdoor/editorial"
    - "None"

Question 2 (multi_select):
  question: "🎛️ Manual tweaks (select any — or none to skip)"
  options:
    - "Recover highlights"
    - "Lift shadows"
    - "More contrast"
    - "More vibrant"
    - "Desaturate (muted tones)"
    - "Heavy background blur"
    - "None"

Question 3 (single_select):
  question: "✂️ Crop ratio"
  options:
    - "Auto (landscape→4:3, portrait→3:4)"
    - "1:1 square"
    - "4:5 portrait"
    - "16:9 wide"
```

**Hold processing until the user replies with their selections.**

### Mapping button selections to parameters

**Adaptive enhancements:**
- "All" → run all six presets (apply skip conditions as normal: Whiten Teeth requires face, Sky presets require outdoor context)
- "Subject Pop" → `Adaptive: Subject - Pop`
- "Warm Pop" → `Adaptive: Subject - Warm Pop`
- "Whiten Teeth" → `Adaptive: Portrait - Whiten Teeth` (skip if no face detected)
- "Blur Background" → `Adaptive: Blur Background - Subtle` (skip Step 6 for that image)
- "Sky Drama (Blue)" → `Adaptive: Sky - Blue Drama`
- "Sky Drama (Dark)" → `Adaptive: Sky - Dark Drama`
- "None" → skip Step 5b entirely
**Manual tweaks:**
- "Recover highlights" → `image_adjust_highlights` → `amount: -60`
- "Lift shadows" → `image_adjust_dark_portions` → `amount: -40`
- "More contrast" → `image_adjust_brightness_and_contrast` → `contrast: 30`
- "More vibrant" → `image_adjust_vibrance_and_saturation` → `vibrance: 30`
- "Desaturate" → `image_adjust_vibrance_and_saturation` → `saturation: -30`
- "Heavy background blur" → `image_apply_gaussian_blur` → `blurRadius: 12, blurTarget: "background"` (do not combine with Blur Background adaptive preset)
- "None" → skip Step 4b entirely
**Crop:**
- "Auto" → landscape → `"4:3"`, portrait → `"3:4"`, focus: `"face"`
- "1:1 square" → `output: "1:1"`, focus: `"face"`
- "4:5 portrait" → `output: "4:5"`, focus: `"face"`
- "16:9 wide" → `output: "16:9"`, focus: `"face"`
All crop modes use `focus: "face"`. If no face is detected, fall back to `focus: "subject"`.

After receiving button selections, confirm the settings back to the user:
```
✅ Got it — running with:
- Auto-straighten + auto-tone + auto-light
- Adaptive enhancements: [list selected, or "none"]
- Manual tweaks: [list if any, or "none"]
- Crop: [ratio or "auto 4:3/3:4"]
- Blur: [adaptive / heavy / none]
```

---

## Step 2b: Large Batch Warning (N > 5)

Include this in the confirmation when N > 5:

```
⏱ Estimated time for [N] images:
  6–10 → ~3–5 min
  11–20 → ~5–10 min
  20+ → 10+ min

Feel free to step away — I'll post a ✅ completion summary with your
download links when done. (No Slack/email notifications available from here.)
```

---

## Step 2c: Sample Preview (Before/After on Image 1)

Before running the full batch, process the **first image only** through the complete pipeline (Steps 3–7) using the confirmed settings. This gives the user a real preview of exactly what will be applied to every image.

1. Run the full pipeline on `sourceURIs[0]` only (straighten → tone → tweaks → adaptive → blur → crop).
2. Call `asset_preview_file` directly with the original source URL and the processed output — do NOT resize either through `image_crop_and_resize` first, as that introduces white bars or unwanted cropping:
```javascript
asset_preview_file({
  assets: [
    { name: "Before", presignedAssetUrl: sourceURIs[0] },
    { name: "After",  presignedAssetUrl: processed_url }
  ]
})
```

3. Post this message:
```
👆 Here's a before/after preview using your first photo and the settings you selected.

How does it look?
```

4. Call `AskUserQuestion` with a single question:
```
Question (single_select):
  question: "Ready to run the full batch?"
  options:
    - "✅ Looks great — run all [N] images"
    - "🎛️ Adjust settings first"
    - "❌ Cancel"
```

Processing pauses here until the user responds — the gate catches issues before time is spent on the full batch.

**If "Looks great":** proceed to Step 3 for the remaining images. Reuse the already-processed image 1 result — do not reprocess it.

**If "Adjust settings":** return to Step 2 (`AskUserQuestion`) to re-collect preferences. Once new settings are confirmed, ask:

```
Question (single_select):
  question: "Want to preview the new settings first, or run all images now?"
  options:
    - "👁 Preview first"
    - "🚀 Run all [N] images now"
```

- If "Preview first": repeat Step 2c with the new settings (reprocess image 1, show before/after, offer the gate again).
- If "Run all now": start the full batch immediately on all images with the new settings. Do not reuse the earlier image 1 result — reprocess it with the updated settings.
**If "Cancel":** stop and let the user know they can restart any time.

---

## Step 3: Auto-Straighten (per image)

Loop one image at a time (no batch support):

```
Tool: image_auto_straighten
Params:
  imageURIs: ["<source_uri_N>"]
  options:
    uprightMode: "auto"
    constrainCrop: true
```

**Output:** `results[0].outputUrl` → collect as `straightened_urls[]`

On failure: use original URI, note "straighten skipped" for that image.

---

## Step 4: Auto-Tone (per image)

```
Tool: image_apply_auto_tone
Params:
  imageURIs: ["<straightened_url_N>"]
```

**Output:** `results[0].outputUrl` → collect as `toned_urls[]`

---

## Step 4b: Optional Tone Adjustments (batch)

If the user requested tonal tweaks, apply in this order using batch arrays,
chaining each step's output into the next:

1. `image_adjust_exposure` — pass `imageURIs: [all toned_urls]`
2. `image_adjust_highlights`
3. `image_adjust_dark_portions`
4. `image_adjust_light_portions`
5. `image_adjust_brightness_and_contrast`
6. `image_adjust_vibrance_and_saturation`
---

## Step 5: Adaptive Enhancements (per image, opt-in only)

Only run this step if the user selected one or more adaptive enhancements. Run each selected preset in sequence, chaining outputs. The order below is recommended but not required by the tools:

1. `Adaptive: Subject - Pop` (if selected)
2. `Adaptive: Subject - Warm Pop` (if selected — do not combine with Subject Pop; pick one or let user decide)
3. `Adaptive: Portrait - Whiten Teeth` (if selected AND face detected via `image_select_subject`)
4. `Adaptive: Blur Background - Subtle` (if selected — skip Step 6 entirely for this image)
5. `Adaptive: Sky - Blue Drama` (if selected AND not skipped due to indoor context)
6. `Adaptive: Sky - Dark Drama` (if selected AND not skipped due to indoor context)
```
Tool: image_apply_preset
Params:
  imageURI: "<toned_url_N>"   # chain from previous step's output
  options:
    presetName: "<exact preset name from list above>"
```

**Output:** `results[0].outputUrl` → chain as input to next preset or Step 6.

**Skip conditions:**
- Whiten Teeth: skip if `image_select_subject` face check returned no face
- Sky presets: skip if session context suggests indoor/studio (user said "headshots", "studio", "office", etc.). If ambiguous, attempt — no visible effect on indoor shots.
- Subject Pop + Warm Pop: these serve similar purposes. If the user selected both, apply both. But if the result looks over-processed, note in the summary that combining them may be heavy-handed.
**On 403 (entitlement):** Skip the preset, note it in the delivery summary ("Adaptive [name] was skipped — not included in your Adobe plan"). Continue with other presets and the rest of the pipeline.

---

## Step 6: Background Blur (per image)

**Skip this step entirely** if the user selected "Blur Background" in Step 5b — the adaptive preset already handled it.

**No blur selected:** skip this step entirely.

**Heavy blur** (if user explicitly requested and did NOT select adaptive blur):
```
Tool: image_apply_gaussian_blur
Params:
  imageURIs: ["<url_N>"]
  options:
    blurRadius: 12
    blurTarget: "background"
```

On failure: use previous step's output, note "blur skipped" for that image.

**Output:** `results[0].outputUrl`

---

## Step 7: Crop (per image)

**Default behavior:**
- Landscape image → crop to `"4:3"`, focus: `"face"`
- Portrait image → crop to `"3:4"`, focus: `"face"`
- User-specified ratio (1:1, 4:5, 16:9, etc.) → use that, focus: `"face"`
- If no face is detected by the crop tool, fall back to `focus: "subject"`
```
Tool: image_crop_and_resize
Params:
  imageURI: "<blur_url_N>"
  options:
    output: "4:3"          # or "3:4" / user choice
    fit: "reframe"
    focus: "face"          # falls back to "subject" if no face detected
  outputFileType: "jpeg"
```

**These are the final full-resolution deliverables.** Collect as `final_urls[]`.

---

## Step 8: Final Preview + Download Links + Firefly Board

Pass the final output URLs directly to `asset_preview_file` — do NOT run them through `image_crop_and_resize` first, as that introduces white bars or unwanted cropping. `asset_preview_file` handles its own thumbnailing correctly.

Call `asset_preview_file` for every run, regardless of batch size:

```javascript
asset_preview_file({
  assets: [
    { name: "portrait_1.jpg", presignedAssetUrl: final_url_1 },
    { name: "portrait_2.jpg", presignedAssetUrl: final_url_2 },
    // ... one entry per image
  ]
})
```

### Create Firefly Board

Call the firefly board tool with the final output urls as follows:

```javascript
create_firefly_board({
  import_adobe_storage: [
    final_output_url_1,
    final_output_url_2,
    // ...
  ]
})
```

**Board link handling:**
- Extract the returned URL and store as `board_url`.
- If `board_url` is present and non-empty, include it in the completion message.
- If the call fails or returns no URL: note "Firefly Board unavailable" in the summary (retrying does not help).
Then post the completion message. The preview grid is included in every completion message. The board link is included whenever `board_url` was returned.

**If N ≤ 3** — list individual links:
```
✅ All done! [N] portraits retouched and ready.

📥 Download your full-resolution portraits:
• Portrait 1 → <final_url_1>
• Portrait 2 → <final_url_2>

🎨 View in Firefly Board → <board_url>   ← always include if board_url is set

Pipeline applied: Auto-straighten → Auto-tone (Camera Raw) → [tweaks if any]
→ [adaptive enhancements if any] → [blur if any] → Crop [ratio]
```

**If N > 3** — list all links:
```
✅ All done! [N] portraits retouched and ready.

📥 Your retouched portraits:
• Portrait 1 → <final_url_1>
• Portrait 2 → <final_url_2>
• ...

🎨 View in Firefly Board → <board_url>   ← always include if board_url is set

Pipeline applied: Auto-straighten → Auto-tone (Camera Raw) → [tweaks if any]
→ [adaptive enhancements if any] → [blur if any] → Crop [ratio]
```

---

## Verbosity Rule

Built for large batches — report only: per-stage start, individual failures (logged once), and the final summary.
- When a pipeline stage begins for the whole batch (e.g. "Straightening [N] images...")
- If an individual image fails (log once, continue)
- Final completion summary with grid + download links
---

## Output Extraction Reference

All pipeline tools return:
```json
{ "results": [{ "success": true, "outputUrl": "https://..." }] }
```

Output is read from `results[N].outputUrl`. On `success: false` see Error Handling.

---

## Error Handling

| Situation                                                 | Action                                                                                                                                                                                                           |
| --------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `image_apply_preset` (adaptive) returns 403 (entitlement) | Skip that preset (Pattern 1). Note in delivery summary: "[Preset name] was skipped — your Adobe plan does not include this feature." Retrying does not resolve a 403 entitlement — note the skip in the summary. |
| Any tool returns 401 (not authenticated)                  | Ask the user to re-authenticate via Adobe OAuth and retry                                                                                                                                                        |
| `asset_add_file` shows no files                           | Wait; remind user to select files in the picker                                                                                                                                                                  |
| `image_auto_straighten` fails                             | Pass original URI to Step 4; note "straighten skipped"                                                                                                                                                           |
| `image_apply_auto_tone` fails                             | Pass straightened URI forward; note in summary                                                                                                                                                                   |
| Any tone adjustment fails                                 | Log and continue with previous step's output                                                                                                                                                                     |
| `image_select_subject` (face check) fails                 | Skip Whiten Teeth preset for that image; continue                                                                                                                                                                |
| `image_apply_preset` (adaptive) fails                     | Use previous step's output; note "[preset name] skipped" in summary                                                                                                                                              |
| `image_apply_gaussian_blur` fails                         | Use previous step's output; note "blur skipped"                                                                                                                                                                  |
| `image_crop_and_resize` fails                             | Use blur output as final; note in summary                                                                                                                                                                        |
| `asset_preview_file` fails                                | Present final output URLs as plain text links in the summary.                                                                                                                                                    |
| All steps fail on one image                               | Return original URI; flag clearly in summary                                                                                                                                                                     |
| Dead end                                                  | Report the failure clearly and offer to retry.                                                                                                                                                                   |

---

## Hard Constraints

- Every image in the batch is processed; failures are flagged rather than silently skipped.
- `image_apply_auto_tone` is called with `type: "cameraRawFilter"`.
- Adaptive enhancements are **off by default** — only run them if the user explicitly selects them.
- Background blur is handled by the "Adaptive: Blur Background - Subtle" preset (or `image_apply_gaussian_blur` for heavy blur); `image_apply_lens_blur` is not used here.
- When "Blur Background" adaptive preset is selected, Step 6 is skipped for that image (the two steps are mutually exclusive).
- Whiten Teeth preset only runs when a face is detected via `image_select_subject`.
- Push notifications (Slack/email/text) are not available from here; completion is communicated through an in-chat summary.
