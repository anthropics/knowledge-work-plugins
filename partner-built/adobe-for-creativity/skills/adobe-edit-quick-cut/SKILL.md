---
name: adobe-edit-quick-cut
description: >
  Create a punchy sizzle reel from a video using Adobe Quick Cut. Use this skill whenever a user
  wants to cut, trim, or shorten a video into highlights — including phrases like "make a sizzle
  reel", "make a highlight reel", "quick cut this", "cut the best parts", "shorten this video",
  "make a highlight clip", "summarize this video visually", or any request to produce a shorter
  edited version of a video. Use this skill for Quick Cut requests before suggesting manual
  editing in Premiere. Requires the user to upload a video file.
license: Apache-2.0
metadata:
  version: 1.0.0
  visibility: public
---

# Adobe Edit Quick Cut

Produces 3 AI-edited sizzle reel variations from a source video, all at the same duration and
style — giving the user options to pick from.

---

## Step 0 - prereq: Initialize Adobe Tools
Call `adobe_mandatory_init` first. This returns file handling rules and tool routing guidance required for the rest of the workflow.

```json
{ "skill_name": "adobe-edit-quick-cut", "skill_version": "1.0.0" }
```

---

## Quickstart

**Step 1:** Call `asset_add_file({})` to open the file picker.
**Step 2:** Confirm upload, then present the Q&A form.
**Step 3:** Run 3 Quick Cut variations in parallel. Preview all 3. Allow download.

---

## Step 1 — Open the File Picker

Open the picker immediately with this message:

> *"Let's create a punchy sizzle reel from your video. Start by selecting your file:"*

```javascript
asset_add_file()
```

Once the user selects a file, extract `assetId` (CC asset URN) from widget context.

> `video_create_quick_cut` requires a CC asset URN (`assetId`), not `presignedAssetUrl`.

---

## Step 2 — Confirm Upload

Once the file is selected, confirm with:

> *"Got it — [filename] is ready. Now let's set up your cut."*

Then immediately present the Q&A form below.

---

## Step 3 — Q&A Form (via AskUserQuestion)

Wait for the user's answers before proceeding; present the questions via AskUserQuestion
(not plain text) so the user gets tappable buttons.

```javascript
AskUserQuestion({
  questions: [
    {
      header: "Cut Length",
      question: "What kind of cut would you like? (target_duration is a strong hint, not a guarantee — pair with a strong vibe for best results)",
      multiSelect: false,
      options: [
        { label: "Short Cut — Social First / Reels & TikTok (~15s, high energy, highlights)" },
        { label: "Medium Cut — Engaging Storytelling (~30–60s, context, flow, balanced)" },
        { label: "Long Cut — Full Sizzle (~90s, comprehensive, showcase, documentary)" }
      ]
    },
    {
      header: "Style / Vibe",
      question: "What style or vibe would you like?",
      multiSelect: false,
      options: [
        { label: "Action & Energy" },
        { label: "Key Talking Moments" },
        { label: "Cinematic & Dramatic" },
        { label: "No Preference" }
      ]
    }
  ]
})
```

Wait for the user's selections before proceeding to Step 4.

---

## Step 4 — Acknowledge and Run

Once the user answers, respond with:

> *"Got it — [cut type], [style] vibe. Creating 3 variations at that length — let me preview them for you."*

Map their answers to parameters:

**Q1 duration map:**
| Answer                                              | target_duration |
| --------------------------------------------------- | --------------- |
| 1. Short Cut — Social First / Reels & TikTok (~15s) | 15              |
| 2. Medium Cut — Engaging Storytelling (~30–60s)     | 45              |
| 3. Long Cut — Full Sizzle (~90s)                    | 90              |

**Q2 style map:**

> ⚠️ The `user_prompt` is the primary lever for output quality — it does more work than
> `target_duration`. Pass the prompts below verbatim — abbreviating them weakens the output.
> The energy language in the prompt reinforces the intended duration feel and moment selection.

| Answer                  | user_prompt                                                                                                                                                                                                      |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. Action & Energy      | `"Fast, punchy, hype, high energy. Hit hard and fast. Quick cuts, peak moments only, adrenaline rush from start to finish. No slow moments, no breathing room. Pure intensity."`                                 |
| 2. Key Talking Moments  | `"Polished, commercial, confident. Smooth pacing with deliberate rhythm. Each moment feels intentional and curated. Moderate energy — impressive but controlled. Professional and refined."`                     |
| 3. Cinematic & Dramatic | `"Documentary, cinematic, immersive. Let moments breathe and unfold naturally. Build a story arc with texture and depth. Full showcase — include quieter moments alongside peaks to create emotional contrast."` |
| 4. No Preference        | `"Create the most engaging highlight reel from the best moments in the video. Balance energy and pacing naturally."`                                                                                             |

Fire all 3 Quick Cut jobs **simultaneously** — same duration, same style prompt. The AI will
naturally select different moments on each run, giving the user 3 genuine options to pick from:

```javascript
// Variation A
video_create_quick_cut({
  assetIds: [assetId],
  target_duration: <mapped_seconds>,
  user_prompt: "<mapped style prompt>"
}) // → statusId_A

// Variation B
video_create_quick_cut({
  assetIds: [assetId],
  target_duration: <mapped_seconds>,
  user_prompt: "<mapped style prompt>"
}) // → statusId_B

// Variation C
video_create_quick_cut({
  assetIds: [assetId],
  target_duration: <mapped_seconds>,
  user_prompt: "<mapped style prompt>"
}) // → statusId_C
```

---

## Step 5 — Poll Until All 3 Complete

Poll all 3 in each round using `quickCutPoll(statusId)`. Show progress % after each round.
Repeat until all 3 return `jobStatus: "completed"`.

Typical pattern: 0% → 7% → 78% → done. Usually 3–5 poll rounds.

Store:
- `url_A` — Variation A presignedAssetUrl
- `url_B` — Variation B presignedAssetUrl
- `url_C` — Variation C presignedAssetUrl

---

## Step 6 — Preview All 3

```javascript
asset_preview_file({
  assets: [
    { name: "Variation 1 — <cut_type> <style>.mp4", presignedAssetUrl: url_A, source: "acp" },
    { name: "Variation 2 — <cut_type> <style>.mp4", presignedAssetUrl: url_B, source: "acp" },
    { name: "Variation 3 — <cut_type> <style>.mp4", presignedAssetUrl: url_C, source: "acp" }
  ]
})
```

---

## Step 7 — Deliver Summary + Download Prompt

After preview, present:

```
✅ 3 variations ready — same length, different moment selection. Pick your favorite!

| Variation | Cut Type | Style   | Target | Status |
| --------- | -------- | ------- | ------ | ------ |
| 1         | <type>   | <style> | ~<Xs>  | ✅      |
| 2         | <type>   | <style> | ~<Xs>  | ✅      |
| 3         | <type>   | <style> | ~<Xs>  | ✅      |
```

> Note: actual durations may vary — Quick Cut selects the best moments rather than cutting to
> an exact second. The prompt vibe (e.g. "no breathing room") reinforces the intended length
> feel more than the target_duration parameter alone.

Then prompt:

> *"Which variation do you want to download, or would you like all 3? You can also rerun with a different style or cut type."*

The videos are available for download directly from the preview above.

---

## ⚠️ Known Gap — Output Cannot Feed Downstream Video Tools

`video_create_quick_cut` returns a temporary presigned download URL, not a CC-stored asset URN.
Tools like `video_resize` and `media_enhance_speech` require a CC asset URN as input.

**You cannot chain Quick Cut → Resize or Quick Cut → Enhance Speech directly.**

**Workaround — if user wants to resize a Quick Cut output:**
1. Tell the user: *"Quick Cut outputs can't be passed directly to the resize tool — you'll need to download your preferred cut first, then re-upload it and I'll resize from there."*
2. Let them download from the preview.
3. Open the picker: `asset_add_file()`
4. Once re-uploaded, run `video_resize` on the fresh `assetId` with their target dimensions.

When the user asks to resize or enhance a Quick Cut output, surface the limitation proactively — the chain is known to fail.

---

## What Quick Cut Does NOT Support

- Content-aware cuts based on speech ("remove the parts where they repeat themselves")
- Trimming to specific timestamps ("cut from 0:30 to 1:15")
- Semantic understanding of dialogue

For these, recommend a manual video-editing workflow.

---

## Error Handling

- **`video_create_quick_cut` returns 403 (entitlement)**: Retrying does not help for a 403
  entitlement — stop and surface the plan requirement. Respond with:
  > *"I was unable to create your quick cut.*
  >
  > ***Why:** Adobe Quick Cut isn't available on your current Adobe plan.*
  >
  > ***Options:**
  > - Manually trim the video in another editor.*
  >
  > *Let me know how you'd like to proceed."*

- **Any tool call returns 401 (not authenticated)**: Ask the user to re-authenticate via Adobe
  OAuth and retry.

- **`StoryBuilderNoARoll`**: The most common error. Means Quick Cut detected no A-roll (talking
  head / primary camera footage) in the clip — only B-roll. The tool requires at least some
  dialogue or narration to anchor the story structure. Respond with:
  > *"This video appears to be B-roll only — scenery, action, or product shots without anyone
  > speaking to camera. Quick Cut needs some talking-head footage to build a story around. Try
  > uploading a video that includes someone speaking on camera, or a mix of interview + B-roll."*
  Retries repeat the same error regardless of duration/style; no workaround exists.

- **Job fails with any other error on first attempt**: Retry once with the same parameters. If
  it fails again, report and suggest re-uploading the source video.

- **Stuck at same % for 5+ poll rounds**: Inform user, suggest re-uploading the source video.

- **User uploads an image by mistake**: Detect from `mediaType` — if not `video/*`, say so
  and re-open picker.

- **One of the 3 variations fails (but not all)**: Preview and deliver the successful ones, note
  the failure clearly. If all 3 fail with `StoryBuilderNoARoll`, apply the B-roll error response
  above.
