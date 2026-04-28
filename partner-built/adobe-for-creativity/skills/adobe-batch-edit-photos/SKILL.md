---
name: "adobe-batch-edit-photos"
description: >
  Apply consistent photo adjustments across a set of images so they look
  like they were edited together. Use this skill whenever the user says
  "make my photos look cohesive", "give all these the same style", "apply
  a warm and golden feel to all of these", "make this cinematic", "match
  the look across my photos", "edit all my travel photos the same way",
  "batch edit these", "make these consistent", "fix my phone photos",
  or uploads a folder of photos and wants a unified, polished result.
  Also triggers for requests like "apply a preset to all of these",
  "make these look professional", or "they were shot in mixed lighting
  — can you fix them all". Outputs direct final image URLs plus an in-chat
  preview grid and optional Firefly Board link.
  Access: 🔐 Signed-In required | Gen AI: ❌
license: Apache-2.0
metadata:
  version: 1.0.0
  visibility: public
---

# Adobe Batch Edit Photos

A batch editing pipeline focused on **visual cohesion** — making a set of
photos look like they were edited together. The user picks a look (or
describes one), and Claude applies it consistently across every image using
Adobe creativity tools.

The core insight: users who want "cohesion" care less about per-image
perfection and more about the whole set reading as intentional. Prioritize
consistency of tone and color over squeezing the best out of any single image.

---

## Tool Reference

| Step                | Tool                                              | Notes                                          |
| ------------------- | ------------------------------------------------- | ---------------------------------------------- |
| Ingest              | `asset_add_file`                                  | Interactive file picker                        |
| Straighten          | `image_auto_straighten`                           | Per image                                      |
| Auto-tone           | `image_apply_auto_tone`                           | Per image, `type: "cameraRawFilter"`           |
| Exposure            | `image_adjust_exposure`                           | Batch — fine-tune option (brighter/darker)     |
| Highlights          | `image_adjust_highlights`                         | Batch — fine-tune option                       |
| Shadows             | `image_adjust_dark_portions`                      | Batch — fine-tune option                       |
| Bright areas        | `image_adjust_light_portions`                     | Batch — fine-tune option                       |
| Brightness/Contrast | `image_adjust_brightness_and_contrast`            | Batch, if requested                            |
| Vibrance/Saturation | `image_adjust_vibrance_and_saturation`            | Batch, if requested                            |
| Color temperature   | `image_adjust_color_temperature`                  | Batch — key for "warm", "cool", "golden" looks |
| Look preset         | `image_apply_preset`                              | Per image, core style vehicle                  |
| Face detect         | `image_select_subject` with `bodyParts: ["Face"]` | Per image, only if crop focus needed           |
| Background blur     | `image_apply_gaussian_blur`                       | Per image, only if explicitly requested        |
| Crop                | `image_crop_and_resize`                           | Per image, optional                            |
| Sample preview      | `asset_preview_file`                              | Before/after on image[0] only                  |
| Final preview       | `asset_preview_file`                              | Batch assets array                             |
| Firefly Board       | `create_firefly_board`                            | All edited outputs                             |

---

## Step 0 - prereq: Initialize Adobe Tools
Call `adobe_mandatory_init` first. This returns file handling rules and tool routing guidance required for the rest of the workflow.

```json
{ "skill_name": "adobe-batch-edit-photos", "skill_version": "1.0.0" }
```

---

## Step 1: Image Ingestion

Call `asset_add_file` with no parameters to open the file picker:

```
Tool: asset_add_file
Params: {}
```

---

## Step 2: Understand the Desired Look

Once URIs are obtained, scan the conversation to infer as many preferences
as possible before asking anything:

- **Look**: inferrable from words like "warm", "golden", "cinematic", "moody",
  "bright and airy", "muted", "film", "cool", "vibrant", "punchy"
- **Fine-tune tweaks**: inferrable from "recover highlights", "lift shadows",
  "more contrast", "blown out", "too dark", "more vibrant", "desaturate"
- **Crop**: inferrable from "no crop", "square", "1:1", "portrait crop", "keep framing", etc.

**Three cases:**

**A — Everything clear from context:** Skip `AskUserQuestion` entirely. Post the confirmation message, then proceed directly to Step 2c (sample preview). Do NOT start the full batch — the preview and confirm gate always runs regardless of how clearly preferences were stated.

**B — Some things clear, some not:** Confirm what you've inferred upfront,
then call `AskUserQuestion` with only the questions that remain unanswered.
For example, if the look and a tweak are clear but crop isn't, post:
```
📷 Got [N] photo(s)! Based on what you said, I'll go with:
- Look: Moody & Cinematic
- Tweaks: Recover blown highlights

Just one thing — do you want a crop?
```
Then call `AskUserQuestion` with Question 3 only.

**C — Nothing specified:** Post the full intro and show all 3 questions:
```
📷 Got [N] photo(s)! I'll apply consistent edits across all of them so
the set looks cohesive.

What kind of look are you going for? 👇
```

The full `AskUserQuestion` questions (use only the ones that are still open):

```
Question 1 (single_select):
  question: "🎨 Pick a base look"
  options:
    - "Auto (balanced, neutral)"
    - "Warm & Golden — cozy, travel, golden hour"
    - "Bright & Airy — clean, light, lifestyle"
    - "Moody & Cinematic — dramatic, contrasty, desaturated"
    - "Cool & Fresh — clear skies, travel, blue tones"
    - "Vibrant & Punchy — vivid, bold, social-ready"
    - "Muted & Film — faded, analog, editorial"

Question 2 (multi_select):
  question: "🎛️ Fine-tune (optional)"
  options:
    - "Recover blown highlights"
    - "Lift dark shadows"
    - "Boost contrast"
    - "Boost color intensity"
    - "Desaturate / muted tones"
    - "Adjust exposure (brighter/darker)"
    - "Tune bright areas"
    - "Blur background (heavy)"
    - "None"

Question 3 (single_select):
  question: "✂️ Crop ratio? (optional)"
  options:
    - "No crop — keep original framing"
    - "1:1 square"
    - "4:5 portrait"
    - "16:9 wide"
    - "4:3 standard"

Question 4 (single_select):  [only ask if Q3 is not "No crop"]
  question: "🎯 How should the crop be framed?"
  options:
    - "Center — crop from center of image"
    - "Smart crop — detect subject/face and frame around it"
```

Wait for the user's reply before proceeding.

**Note on Question 4:** If the user's message already implies a framing preference
(e.g. "center crop", "crop to my face", "frame around the subject"), skip Q4 and
infer directly. If the user specifies a ratio but not a framing method, default to
Smart crop — it almost always produces a better result than a pure center cut.

### Look → Parameter Mapping

**Base look → `image_adjust_color_temperature` + `image_apply_preset` + adjustments:**

| Look              | Color Temp (a, b, luminance) | Preset                         | Saturation/Vibrance          | Brightness/Contrast |
| ----------------- | ---------------------------- | ------------------------------ | ---------------------------- | ------------------- |
| Auto (balanced)   | none                         | `Adaptive: Auto Tone`          | none                         | none                |
| Warm & Golden     | a=32, b=120, luminance=67    | `Adaptive: Subject - Warm Pop` | vibrance +15                 | none                |
| Bright & Airy     | a=20, b=60, luminance=62     | `Adaptive: Subject - Pop`      | saturation -10, vibrance +10 | brightness +15      |
| Moody & Cinematic | a=20, b=-50, luminance=45    | `Adaptive: Sky - Dark Drama`   | saturation -20               | contrast +25        |
| Cool & Fresh      | a=18, b=-123, luminance=45   | `Adaptive: Sky - Blue Drama`   | vibrance +10                 | none                |
| Vibrant & Punchy  | none                         | `Adaptive: Subject - Pop`      | vibrance +30, saturation +15 | contrast +10        |
| Muted & Film      | none                         | none                           | saturation -35, vibrance -10 | contrast +10        |

**Fine-tune → tool parameters:**
- "Recover blown highlights" → `image_adjust_highlights` → `amount: -60`
- "Lift dark shadows" → `image_adjust_dark_portions` → `amount: +40`
- "Boost contrast" → `image_adjust_brightness_and_contrast` → `contrast: 30`
- "Boost color intensity" → `image_adjust_vibrance_and_saturation` → `vibrance: 30`
- "Desaturate / muted tones" → `image_adjust_vibrance_and_saturation` → `saturation: -30`
- "Adjust exposure (brighter/darker)" → `image_adjust_exposure` → `exposure: +0.5` (brighter) or `exposure: -0.5` (darker); infer direction from context, default to `+0.3` if unspecified
- "Tune bright areas" → `image_adjust_light_portions` → `amount: +20`
- "Blur background (heavy)" → `image_apply_gaussian_blur` → `blurRadius: 12, blurTarget: "background"`
- "None" → skip fine-tune step entirely

**Crop:**
- "No crop" → skip Step 7 entirely
- Ratio + "Center" → `image_crop_and_resize` with `fit: "reframe"`, that ratio as `output`, `align: { x: 0.5, y: 0.5 }` (pure center cut)
- Ratio + "Smart crop" → `image_crop_and_resize` with `fit: "reframe"`, that ratio as `output`, `focus: "face"` if portraits/people likely, else `focus: "subject"` (smart reframe around detected subject at the chosen ratio)

After receiving selections, confirm the settings back to the user:
```
✅ Got it — running with:
- Look: [selected look]
- Tweaks: [list if any, or "none"]
- Crop: [ratio or "no crop"] + [Center / Smart crop]
- Background blur: [yes/no]
```

Then proceed immediately to Step 2c (sample preview) — do not start the full batch yet.

---

## Step 2b: Large Batch Warning (N > 5)

Include this as part of the Step 2c confirmation prompt (after the before/after preview) when N > 5:
```
⏱ Estimated time for [N] images:
  6–10 → ~3–5 min
  11–20 → ~5–10 min
  20+ → 10+ min

Feel free to step away — I'll post a ✅ summary with download links when done.
```

---

## Step 2c: Sample Preview (Before/After on Image 1)

Before running the full batch, process the **first image only** through the complete pipeline (Steps 3–7) using the confirmed settings. This gives the user a real preview of exactly what will be applied to every image.

1. Run the full pipeline on `sourceURIs[0]` only (straighten → tone → look → fine-tune → blur → crop).
2. Call `asset_preview_file` directly with both the original source URL and the processed output URL — do NOT resize either through `image_crop_and_resize` first, as that introduces white bars or unwanted cropping:
```javascript
asset_preview_file({
  assets: [
    { name: "Before", presignedAssetUrl: sourceURIs[0] },
    { name: "After",  presignedAssetUrl: processed_url }
  ]
})
```

3. Post this message (append the large-batch timing note here if N > 5):
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
    - "🎛️ Adjust settings"
    - "❌ Cancel"
```

**If "Looks great":** Start the full batch on the remaining images (`sourceURIs[1…]`). Reuse the already-processed image[0] result — do not reprocess it.

**If "Adjust settings":** Re-show the full `AskUserQuestion` set from Step 2. Once new settings are confirmed, ask whether the user wants another preview or wants to go straight to the full batch:

```
Question (single_select):
  question: "Want to preview the new settings first, or run all images now?"
  options:
    - "👁 Preview first"
    - "🚀 Run all [N] images now"
```

- If "Preview first": repeat Step 2c with the new settings (process image[0] again, show before/after, offer the same Looks great / Adjust / Cancel gate).
- If "Run all now": start the full batch immediately on all `sourceURIs` with the new settings. Do not reuse the earlier image[0] result — reprocess it with the updated settings.
**If "Cancel":** Acknowledge and stop. Do not process any images.

---

## Step 3: Auto-Straighten (per image)

```
Tool: image_auto_straighten
Params:
  imageURIs: ["<source_uri_N>"]
  options:
    uprightMode: "auto"
    constrainCrop: true
```

Output: `results[0].outputUrl` → `straightened_urls[]`

On failure: use original URI, note "straighten skipped" for that image.

---

## Step 4: Auto-Tone (per image)

```
Tool: image_apply_auto_tone
Params:
  imageURI: "<straightened_url_N>"
  options:
    type: "cameraRawFilter"
  outputFileType: "jpeg"
```

Use `type: "cameraRawFilter"` for `image_apply_auto_tone`. Output: `results[0].outputUrl` → `toned_urls[]`

---

## Step 5: Apply the Look (per image)

Apply the look in this order per image, chaining outputs:

**5a: Color Temperature** (if the look requires it — see mapping table)

`image_adjust_color_temperature` supports a batch `imageURIs` array. Pass all toned
URLs at once for efficiency:
```
Tool: image_adjust_color_temperature
Params:
  imageURIs: ["<toned_url_1>", "<toned_url_2>", ...]
  options:
    a: <value from mapping>         # green-red axis (-128–127)
    b: <value from mapping>         # blue-yellow axis (-128–127)
    luminance: <value from mapping> # 0–100
```
Output: `results[N].outputUrl` → `color_temp_urls[]`

**5b: Look Preset** (if the look uses one — see mapping table)
```
Tool: image_apply_preset
Params:
  imageURI: "<color_temp_url_N>"
  options:
    presetName: "<preset from mapping>"
```

**5c: Vibrance / Saturation** (if the look requires it)
```
Tool: image_adjust_vibrance_and_saturation
Params:
  imageURIs: ["<previous_url_N>"]
  options:
    vibrance: <value>
    saturation: <value>
```

**5d: Brightness + Contrast** (if the look requires either — combine into one call)
```
Tool: image_adjust_brightness_and_contrast
Params:
  imageURIs: ["<previous_url_N>"]
  options:
    brightness: <value>   # omit if not needed for this look
    contrast: <value>     # omit if not needed for this look
```

Combining brightness and contrast into a single call saves a round trip and
produces the same result as two sequential calls.

The goal is consistency: apply the same parameter values to every image,
even if some images might technically look better with different values.
Cohesion beats perfection here.

**On 403 (entitlement) for `image_apply_preset`:** Skip the preset for all images.
Note in the delivery summary: "[Preset name] was skipped — not included in
your Adobe plan." Continue with the rest of the look adjustments.

---

## Step 6: Fine-Tune Adjustments (batch, if selected)

Apply user-selected tweaks across all images at once. All of these tools
accept a batch `imageURIs` array — chain from the look output:

```
Tool: image_adjust_highlights / image_adjust_dark_portions / image_adjust_brightness_and_contrast /
      image_adjust_vibrance_and_saturation / image_adjust_exposure / image_adjust_light_portions
Params:
  imageURIs: ["<look_url_1>", "<look_url_2>", ...]
  options:
    <values from mapping>
```

Run each selected tweak in sequence, chaining outputs. If "Boost contrast" is selected AND the look already calls `image_adjust_brightness_and_contrast` for brightness (e.g. Bright & Airy), merge them into a single call with both `brightness` and `contrast` values rather than running two separate calls.

**Background blur** (if selected, per image):
```
Tool: image_apply_gaussian_blur
Params:
  imageURIs: ["<url_N>"]
  options:
    blurRadius: 12
    blurTarget: "background"
```

---

## Step 7: Crop (per image, if requested)

If "No crop" was selected, skip this step entirely.

Both crop modes use the same `fit: "reframe"` at the chosen ratio — the
difference is in how the frame is positioned within the image.

**Center crop** — cuts to the target ratio from the geometric center:
```
Tool: image_crop_and_resize
Params:
  imageURI: "<adjusted_url_N>"
  options:
    output: "<ratio>"        # "1:1", "4:5", "16:9", "4:3"
    fit: "reframe"
    align: { x: 0.5, y: 0.5 } # geometric center
  outputFileType: "jpeg"
```

**Smart crop** — same ratio, but positions the frame around the detected
subject or face rather than the geometric center. The subject stays in frame
even if they're off-center in the original:
```
Tool: image_crop_and_resize
Params:
  imageURI: "<adjusted_url_N>"
  options:
    output: "<ratio>"   # "1:1", "4:5", "16:9", "4:3"
    fit: "reframe"
    focus: "face"       # or "subject" for non-portrait scenes
  outputFileType: "jpeg"
```

Collect as `final_urls[]`. If no crop: `final_urls[]` = outputs from Step 6.

---

## Step 8: Preview

Pass the final output URLs directly to `asset_preview_file` — do NOT run them through `image_crop_and_resize` first. Adding a resize step introduces white bars (from `fit: "pad"`) or crops subjects (from `fit: "reframe"`). `asset_preview_file` handles its own thumbnailing correctly.

```javascript
asset_preview_file({
  assets: [
    { name: "photo_1.jpg", presignedAssetUrl: final_url_1 },
    // ... one per image
  ]
})
```

If `asset_preview_file` fails, present the final output URLs as plain text links in the completion summary.

**Before/after preview (Step 2c):** Same rule applies — pass the original source URL and the processed URL directly to `asset_preview_file`. Do not resize either.

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

- `create_firefly_board` returns a board URL. Extract it and store as `board_url`.
- If `board_url` is present and non-empty, include it in the completion message.
- If the call throws an error or returns no URL: omit the board link and note "Firefly Board unavailable" in the summary (retrying does not help).
Then post the completion message. The preview grid is included in every completion message. The board link is included whenever `board_url` was returned.

**If N ≤ 3:**
```
✅ Done! [N] photos edited with a consistent [look name] look.

📥 Download:
• Photo 1 → <final_url_1>
• ...

🎨 View in Firefly Board → <board_url>   ← always include if board_url is set

Look applied: [look name] → [brief description of what was applied]
```

**If N > 3:**
```
✅ Done! [N] photos edited with a consistent [look name] look.

📥 Your edited photos:
• Photo 1 → <final_url_1>
• Photo 2 → <final_url_2>
• ...

🎨 View in Firefly Board → <board_url>   ← always include if board_url is set

Look applied: [look name] → [brief description of what was applied]
```

---

## Verbosity Rule

Report only: major stage starts, per-image failures (logged once), and the final summary.
- When a major stage starts (e.g. "Applying Warm & Golden look to [N] images…")
- Any per-image failure (log once, continue)
- Final summary with grid + download links

---

## Output Extraction

All pipeline tools return:
```json
{ "results": [{ "success": true, "outputUrl": "https://..." }] }
```

Read `results[N].outputUrl`. On `success: false` → see Error Handling.

---

## Error Handling

| Situation                                           | Action                                                                                                                                                                                                   |
| --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `image_apply_preset` returns 403                    | Skip preset for all images (Pattern 1). Note in summary. Continue with other look steps.                                                                                                                 |
| Any tone/color tool returns 403                     | Skip that step. Note in summary. Continue.                                                                                                                                                               |
| Any tool returns "No approval received"             | Treat the same as a 403 entitlement error. For optional steps (presets, fine-tune adjustments, preview), skip and note in summary. Retrying does not help for this error — continue per the rules above. |
| Any tool returns 401                                | Ask user to re-authenticate via Adobe OAuth and retry.                                                                                                                                                   |
| `asset_add_file` shows no files                     | Remind user to select files in the picker.                                                                                                                                                               |
| URI starts with `dcx*.adobe.io`                     | Call `read_widget_context` for real presigned S3 URL.                                                                                                                                                    |
| `image_auto_straighten` fails                       | Use original URI; note "straighten skipped".                                                                                                                                                             |
| `image_apply_auto_tone` fails                       | Use straightened URI; note in summary.                                                                                                                                                                   |
| Any adjustment tool fails                           | Use previous step's output; note in summary.                                                                                                                                                             |
| `image_apply_gaussian_blur` fails                   | Use previous output; note "blur skipped".                                                                                                                                                                |
| `image_crop_and_resize` fails                       | Use blur/adjusted output as final; note in summary.                                                                                                                                                      |
| `asset_preview_file` returns "No approval received" | Present final output URLs as plain text links in the summary instead.                                                                                                                                    |
| All steps fail on one image                         | Return original URI; flag clearly in summary.                                                                                                                                                            |

---

## Hard Constraints

- Every image in the batch is processed; failures are flagged rather than silently skipped.
- `image_apply_auto_tone` is called with `type: "cameraRawFilter"`.
- Apply the **same parameter values** to every image in the batch (cohesion over perfection).
- Adaptive presets are off by default — only run them as part of a look.
- Background blur uses `image_apply_gaussian_blur` with `blurTarget: "background"` (`image_apply_lens_blur` is not used here).
- Completion is posted as a clear in-chat message (no push notifications).
