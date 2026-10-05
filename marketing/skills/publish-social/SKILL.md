---
name: publish-social
description: Publish or schedule a finished social media post (text, images, or a video) to the connected social accounts through a social publishing tool, adapting the copy per platform and confirming before anything goes live. Use when the user wants to post, schedule, or cross-post content to TikTok, Instagram, YouTube, LinkedIn, Facebook, X, Threads, Pinterest, or Bluesky.
argument-hint: "<what to publish, where, and when>"
---

# Publish Social

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../../CONNECTORS.md).

Take a finished post and publish or schedule it on the connected social accounts using `~~social publishing`. Nothing is sent until the user confirms the final plan.

## Trigger

User runs `/publish-social`, or asks to post, publish, schedule, or cross-post content to one or more social platforms.

## Prerequisites

A `~~social publishing` tool must be connected and the target social accounts must already be linked inside it. If no tool is connected, stop and tell the user which tools are supported (see CONNECTORS.md) instead of trying to post through a platform's own API.

## Inputs

Gather the following from the user. If not provided, ask before proceeding:

1. **Content** — the text of the post, and any media (image paths or URLs, a video path or URL). Reuse the output of `/draft-content` when it exists.
2. **Platforms** — which of the connected platforms to post to. Default to the platforms the user named; never add platforms they did not mention.
3. **Profile / account** — when the tool manages several brands or clients, which one. List the available profiles from the tool and ask if there is more than one.
4. **Timing** — now, or a date and time (ask for the timezone if it is not obvious).
5. **Per-platform details** when the platform requires them: YouTube title and visibility, TikTok privacy level and whether it is AI-generated content, Pinterest board, Facebook page, first comment for LinkedIn or X.

## Process

### Step 1: Check what is connected

Use `~~social publishing` to list the profiles and the social accounts linked to each. Confirm that every requested platform has a working connection. If an account needs reconnecting, say so and point the user to the tool's account page rather than retrying.

### Step 2: Adapt the copy per platform

Starting from the single draft, produce one version per platform:

- **X** — keep within the character limit; threads only if the user asked for one.
- **LinkedIn** — professional tone, line breaks between ideas, hashtags at the end (3-5).
- **Instagram / Threads** — conversational, hashtags allowed, no raw URLs in the caption for Instagram (links do not render).
- **TikTok / YouTube Shorts** — short caption, a title for YouTube, the hashtags that matter.
- **Facebook / Pinterest / Bluesky** — platform-appropriate length; a Pinterest pin needs a board and benefits from a destination link.

Apply the brand voice if it is configured (see `brand-voice`). Keep the message identical across platforms; only the format changes.

### Step 3: Show the plan and confirm

Before calling any publishing operation, show a table: platform, profile, exact caption, media, time. Ask for an explicit confirmation. Treat "publish" as irreversible: a post that goes live is visible to the public immediately.

### Step 4: Publish or schedule

Call `~~social publishing` once with all confirmed platforms. For video and photos use the tool's media upload operation; for text-only posts use the text operation. When the user asked for a later time, schedule instead of publishing.

### Step 5: Verify and report

Publishing to several platforms is asynchronous. Poll the tool's status operation until it reports a final state, then report per platform: published (with the post URL when the platform returns one), scheduled (with the job id and time), or failed (with the platform's error and what the user should do, for example reconnect the account or shorten the caption). Do not re-send a post whose outcome is unknown; check its status first.

## Output

A per-platform results table, the URLs of the live posts, and the scheduled times for anything queued. If something failed, the exact reason and the next action.

Ask: "Would you like me to schedule the same post for another profile, or draft the follow-up?"
