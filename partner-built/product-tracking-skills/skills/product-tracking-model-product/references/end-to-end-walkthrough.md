# End-to-End Walkthrough: Loom-Style Video Messaging

This walkthrough shows the complete product tracking lifecycle for a fictional video messaging product called **Clipper** — from discovery through maintenance. It demonstrates how all seven skills work together.

---

## Phase 1-2: Discover the Product & Map Value

### The Conversation

**Engineer:** What product are we designing telemetry for?

**User:** Clipper — it's a video messaging tool for remote teams. Record quick videos and share them with teammates.

**Engineer:** In one sentence, what's the core value?

**User:** Replace meetings and long emails with quick video messages.

**Engineer:** What's the single most important action a user takes?

**User:** Recording a video.

**Engineer:** If a user signed up but never recorded a video, would they still get value?

**User:** Not really. Watching videos others share has some value, but recording is the point.

**Engineer:** So recording is your **primary value action**. What are the other critical actions?

**User:** 
1. Sharing the video (via link or embed)
2. Watching videos others shared
3. Adding comments to videos
4. Creating folders to organize videos

**Engineer:** Let me categorize these. Recording and sharing are **core** — they directly deliver value. Watching is **core** for recipients. Comments and folders are **supporting** — they enhance the experience but you could use Clipper without them.

**User:** That's right.

**Engineer:** What about the entity model?

**User:** We have users and workspaces. A user can be in multiple workspaces. Roles are admin, member, and viewer. We track the user's plan at the workspace level — free, pro, or enterprise.

**Engineer:** Any tracking in place today?

**User:** We have Segment set up, but it's tribal knowledge. Some stuff is tracked, some isn't. We don't have a plan document.

### The Output: `.telemetry/product.md`

```markdown
# Product: Clipper

**Last updated:** 2026-02-08
**Discovery by:** Product Tracking Skills

## Product Identity

**One-liner:** Video messaging tool that replaces meetings and long emails with quick async video
**Category:** collaboration-tools
**Collaboration model:** multiplayer (workspaces, sharing)

## Value Mapping

### Primary Value Action
**Record Video** — This is the action that, if it dropped to zero, would mean the product has failed. Users come to Clipper to record and share video messages. All tracking plan design centers on capturing this action and its context.

### Core Features (directly deliver value)
1. **Record Video** — The primary action. Capture screen, camera, or both.
2. **Share Video** — Distribute the recorded video via link, embed, or direct share.
3. **Watch Video** — Recipients view shared videos.

### Supporting Features (enable core actions)
1. **Comment on Video** — Add feedback at timestamps. Enhances value but not essential.
2. **Organize into Folders** — Structure content. Important for power users.
3. **Manage Workspace** — Admin functions, invites, settings.

*Core features become first-class events. Supporting features may be tracked at lower fidelity.*

## Entity Model

### Users
- **ID format:** `usr_` prefix + UUID
- **Roles:** admin, member, viewer
- **Multi-workspace:** Yes, users can belong to multiple workspaces

### User Traits
| Trait | Known at signup | Changes over time |
|-------|-----------------|-------------------|
| email | ✓ | rarely |
| name | ✓ | sometimes |
| role | After invite | sometimes |
| total_videos_recorded | No | yes (derived) |

### Workspaces (Accounts)
- **ID format:** `wsp_` prefix + UUID
- **Hierarchy:** Flat (workspaces contain users and videos)

### Workspace Traits
| Trait | Known at creation | Changes over time |
|-------|-------------------|-------------------|
| name | ✓ | rarely |
| plan | ✓ | yes |
| member_count | ✓ | yes |
| video_count | No | yes (derived) |

## Current State

- **Existing tracking:** Segment (analytics-next browser SDK)
- **Documentation:** None (tribal knowledge)
- **Known issues:** Inconsistent event naming, missing recording events, no workspace tracking

## Integration Targets

| Destination | Purpose | Priority |
|-------------|---------|----------|
| Segment | CDP, source of truth | High |
| Amplitude | Product analytics | High |
| Accoil | Engagement scoring | Medium |
| HubSpot | CRM sync | Medium |
```

---

## Phase 3: Design the Tracking Plan

### The Approach

Starting from the value mapping, we design the **ideal tracking plan** — what should exist, independent of what's currently implemented.

### The Output: `.telemetry/tracking-plan.yaml`

```yaml
# Tracking Plan: Clipper
# Generated: 2026-02-08
# Version: 1.0.0

meta:
  product: Clipper
  version: "1.0.0"
  created: "2026-02-08"
  updated: "2026-02-08"
  owner: product-team
  sdk: segment

naming:
  style: "Object Action"
  case: title
  examples:
    - "Video Recorded"
    - "Video Shared"
    - "Comment Added"

entities:
  user:
    id_property: userId
    id_format: "usr_*"
    traits:
      - name: email
        type: string
        pii: true
      - name: name
        type: string
      - name: created_at
        type: datetime
      - name: role
        type: string
        enum: [admin, member, viewer]

  workspace:
    id_property: groupId
    id_format: "wsp_*"
    traits:
      - name: name
        type: string
      - name: plan
        type: string
        enum: [free, pro, enterprise]
      - name: member_count
        type: integer
      - name: created_at
        type: datetime

events:
  # ═══════════════════════════════════════════════════════════════
  # LIFECYCLE
  # ═══════════════════════════════════════════════════════════════
  
  - name: User Signed Up
    category: lifecycle
    phase: core
    description: User creates a new account
    properties:
      - name: signup_source
        type: string
        enum: [organic, google, invite, referral]
        required: true
    expected_frequency: low
    triggers:
      - User completes signup form
      - User accepts workspace invite (creates account)

  - name: User Invited
    category: lifecycle
    phase: core
    description: Existing user invites someone to workspace
    properties:
      - name: invitee_email
        type: string
        required: true
        pii: true
      - name: role_assigned
        type: string
        enum: [admin, member, viewer]
        required: true
    expected_frequency: low
    triggers:
      - Admin sends workspace invitation

  - name: User Joined Workspace
    category: lifecycle
    phase: core
    description: User accepts invite and joins workspace
    properties:
      - name: invite_source
        type: string
        enum: [email, link]
        required: true
    expected_frequency: low
    triggers:
      - Invited user clicks invite link and joins

  # ═══════════════════════════════════════════════════════════════
  # CORE VALUE: Recording
  # ═══════════════════════════════════════════════════════════════
  
  - name: Recording Started
    category: core_value
    phase: core
    description: User begins recording a video
    properties:
      - name: recording_type
        type: string
        enum: [screen, camera, both]
        required: true
      - name: has_audio
        type: boolean
        required: true
    expected_frequency: high
    triggers:
      - User clicks record button
    notes: >
      This is a precursor to Video Recorded. Track it to understand
      recording abandonment (started but not completed).

  - name: Video Recorded
    category: core_value
    phase: core
    description: User completes recording a video
    properties:
      - name: video_id
        type: string
        required: true
      - name: recording_type
        type: string
        enum: [screen, camera, both]
        required: true
      - name: duration_seconds
        type: integer
        required: true
      - name: has_audio
        type: boolean
        required: true
      - name: has_transcript
        type: boolean
        required: true
    expected_frequency: high
    triggers:
      - User stops recording and video is saved
    notes: >
      PRIMARY VALUE ACTION. This is the most important event in the 
      tracking plan. A user who never records has not received value.

  # ═══════════════════════════════════════════════════════════════
  # CORE VALUE: Sharing
  # ═══════════════════════════════════════════════════════════════
  
  - name: Video Shared
    category: core_value
    phase: core
    description: User shares a video with others
    properties:
      - name: video_id
        type: string
        required: true
      - name: share_method
        type: string
        enum: [link, embed, email, slack]
        required: true
      - name: recipients_count
        type: integer
        required: false
    expected_frequency: high
    triggers:
      - User copies share link
      - User sends via integration
      - User embeds in external tool

  # ═══════════════════════════════════════════════════════════════
  # CORE VALUE: Viewing
  # ═══════════════════════════════════════════════════════════════
  
  - name: Video Viewed
    category: core_value
    phase: core
    description: Someone watches a shared video
    properties:
      - name: video_id
        type: string
        required: true
      - name: viewer_type
        type: string
        enum: [creator, team_member, external]
        required: true
      - name: watch_duration_seconds
        type: integer
        required: true
      - name: video_duration_seconds
        type: integer
        required: true
      - name: completion_percent
        type: integer
        required: true
    expected_frequency: high
    triggers:
      - Video playback reaches meaningful threshold (>3 seconds)
    notes: >
      For external viewers without accounts, use anonymous ID.
      completion_percent = watch_duration / video_duration * 100

  # ═══════════════════════════════════════════════════════════════
  # SUPPORTING: Comments
  # ═══════════════════════════════════════════════════════════════
  
  - name: Comment Added
    category: supporting
    phase: supporting
    description: User adds a comment to a video
    properties:
      - name: video_id
        type: string
        required: true
      - name: comment_type
        type: string
        enum: [text, emoji, drawing]
        required: true
      - name: timestamp_seconds
        type: integer
        required: false
        description: Video timestamp where comment is anchored (null for general comments)
    expected_frequency: medium
    triggers:
      - User submits a comment on a video

  # ═══════════════════════════════════════════════════════════════
  # SUPPORTING: Organization
  # ═══════════════════════════════════════════════════════════════
  
  - name: Folder Created
    category: supporting
    phase: supporting
    description: User creates a folder to organize videos
    properties:
      - name: folder_id
        type: string
        required: true
      - name: is_shared
        type: boolean
        required: true
    expected_frequency: low
    triggers:
      - User creates new folder

  - name: Video Organized
    category: supporting
    phase: supporting
    description: User moves video to a folder
    properties:
      - name: video_id
        type: string
        required: true
      - name: folder_id
        type: string
        required: true
    expected_frequency: low
    triggers:
      - User moves or assigns video to folder

  # ═══════════════════════════════════════════════════════════════
  # WORKSPACE MANAGEMENT
  # ═══════════════════════════════════════════════════════════════
  
  - name: Workspace Created
    category: lifecycle
    phase: core
    description: New workspace is created
    properties:
      - name: workspace_name
        type: string
        required: true
      - name: plan
        type: string
        enum: [free, pro, enterprise]
        required: true
    expected_frequency: low
    triggers:
      - User creates first workspace during signup
      - Existing user creates additional workspace

  - name: Plan Changed
    category: billing
    phase: core
    description: Workspace upgrades or downgrades plan
    properties:
      - name: previous_plan
        type: string
        enum: [free, pro, enterprise]
        required: true
      - name: new_plan
        type: string
        enum: [free, pro, enterprise]
        required: true
      - name: change_type
        type: string
        enum: [upgrade, downgrade]
        required: true
    expected_frequency: low
    triggers:
      - Admin changes workspace plan

  # ═══════════════════════════════════════════════════════════════
  # INTEGRATIONS
  # ═══════════════════════════════════════════════════════════════
  
  - name: Integration Connected
    category: configuration
    phase: supporting
    description: Workspace connects an integration
    properties:
      - name: integration_name
        type: string
        enum: [slack, notion, jira, linear, hubspot]
        required: true
    expected_frequency: low
    triggers:
      - Admin completes OAuth flow for integration
```

---

## Phase 4: Audit Reality vs. Plan

### The Process

We scan the existing codebase to find what's actually tracked, then compare against the ideal plan.

### Scanning the Codebase

```bash
# Find all Segment track() calls
rg "analytics\.track\(" --type ts --type tsx -A 2 src/

# Results show:
# src/recorder/VideoRecorder.tsx:  analytics.track('video_created', { duration })
# src/share/ShareModal.tsx:        analytics.track('shared_video', { method: shareType })
# src/auth/Signup.tsx:             analytics.track('signup_completed', { source })
# src/comments/CommentForm.tsx:    analytics.track('comment_posted', { videoId })
# src/Header.tsx:                  analytics.track('button_clicked', { button: 'record' })
# src/Header.tsx:                  analytics.track('button_clicked', { button: 'share' })
```

### The Output: `.telemetry/audits/2026-02-08.md`

```markdown
# Telemetry Audit: 2026-02-08

**Plan version:** 1.0.0
**Codebase:** src/
**SDK:** Segment (analytics-next)

## Summary: Ideal vs. Current

| Category | Count | Notes |
|----------|-------|-------|
| Events in ideal plan | 13 | Source of truth |
| Events in current implementation | 6 | What exists today |
| ✅ Correctly implemented | 0 | None match exactly |
| ❌ Missing relative to plan | 9 | Ideal exists, implementation doesn't |
| ⚠️ Exists but shouldn't | 2 | Implementation exists, not in plan |
| 🔧 Exists but malformed | 4 | Implementation doesn't match plan spec |

**Coverage:** 0% of ideal plan is implemented correctly.

---

## Missing Relative to Plan

*These events are defined in the ideal tracking plan but not found in code.*

| Event | Phase | Impact | Suggested Location |
|-------|-------|--------|-------------------|
| Recording Started | core | HIGH — understand abandonment | `src/recorder/VideoRecorder.tsx` |
| Video Viewed | core | HIGH — primary value for recipients | `src/player/VideoPlayer.tsx` |
| User Invited | core | MEDIUM — growth tracking | `src/workspace/InviteModal.tsx` |
| User Joined Workspace | core | MEDIUM — onboarding funnel | `src/auth/AcceptInvite.tsx` |
| Workspace Created | core | MEDIUM — account tracking | `src/workspace/CreateWorkspace.tsx` |
| Plan Changed | core | HIGH — revenue tracking | `src/billing/PlanSelector.tsx` |
| Integration Connected | supporting | LOW | `src/integrations/` |
| Folder Created | supporting | LOW | `src/folders/` |
| Video Organized | supporting | LOW | `src/folders/` |

---

## Exists But Shouldn't (Review Required)

*These events exist in code but are not in the ideal tracking plan.*

| Event | Location | Recommendation |
|-------|----------|----------------|
| `button_clicked` | `src/Header.tsx:42, :56` | **Remove.** Generic click tracking adds noise without insight. The specific actions (recording, sharing) should be tracked directly. |

---

## Exists But Malformed

*These events exist and have equivalents in the plan, but implementation doesn't match spec.*

| Current Event | Ideal Event | Issues | Location | Fix |
|--------------|-------------|--------|----------|-----|
| `video_created` | `Video Recorded` | Wrong name (snake_case, different verb). Missing: `recording_type`, `has_audio`, `has_transcript`. Has: `duration` (should be `duration_seconds`). | `src/recorder/VideoRecorder.tsx:88` | Rename event, add missing properties, rename duration property |
| `shared_video` | `Video Shared` | Wrong name format. Property `method` should be `share_method`. Missing: `video_id`. | `src/share/ShareModal.tsx:45` | Rename event and properties, add video_id |
| `signup_completed` | `User Signed Up` | Wrong name. Property `source` should be `signup_source`. | `src/auth/Signup.tsx:112` | Rename event and property |
| `comment_posted` | `Comment Added` | Wrong name. Missing: `comment_type`, `timestamp_seconds`. | `src/comments/CommentForm.tsx:67` | Rename event, add properties |

---

## SDK Configuration Issues

- [x] `identify()` called on login — **YES** (`src/auth/Login.tsx:34`)
- [ ] `group()` called for workspace context — **NO** — Workspaces not tracked. Add `group()` call when user switches workspace.
- [x] Error handling present — **YES** (try/catch around track calls)
- [ ] Non-blocking calls — **PARTIAL** — Some await analytics.track() in handlers

---

## Prioritized Fix List

### 🔴 Critical (Fix immediately)

1. **Add `Video Recorded` with correct schema** — This is the primary value action. Current `video_created` is malformed.
   - Location: `src/recorder/VideoRecorder.tsx`
   - Changes: Rename event, add `recording_type`, `has_audio`, `has_transcript`, rename `duration` → `duration_seconds`

2. **Add `Video Viewed` tracking** — Currently not tracked at all. Without this, you can't measure if shared videos are actually being watched.
   - Location: `src/player/VideoPlayer.tsx`
   - Add: New tracking call with completion metrics

3. **Add `group()` for workspace context** — Account-level analytics won't work without this.
   - Location: `src/workspace/WorkspaceProvider.tsx`
   - Add: `analytics.group(workspaceId, { name, plan, member_count })`

### 🟡 High (Fix this sprint)

4. **Fix `Video Shared` schema** — Core action, needs correct properties
5. **Fix `User Signed Up` schema** — Funnel starts here
6. **Add `Plan Changed` tracking** — Revenue visibility
7. **Add `Recording Started` tracking** — Understand abandonment

### 🟢 Low (Backlog)

8. **Remove `button_clicked` events** — Noise
9. **Add `Comment Added` with full schema**
10. **Add folder/organization events**
11. **Add integration events**

---

## Summary

The current tracking is incomplete and inconsistent. Core value actions are partially tracked but with wrong schemas. The biggest gap is `Video Viewed` — without it, Clipper can't measure recipient engagement.

Recommended approach:
1. Fix the 3 critical issues this week
2. Work through high-priority fixes over the next sprint
3. Address low-priority items as part of related feature work
```

---

## Phase 5: Implement & Fix

### Generated Code: `instrumentation/tracking.ts`

```typescript
// Auto-generated from tracking-plan.yaml v1.0.0
// Auto-generated — regenerate with the implementation skill

import { AnalyticsBrowser } from '@segment/analytics-next';

// Types
export interface UserTraits {
  email?: string;
  name?: string;
  created_at?: string;
  role?: 'admin' | 'member' | 'viewer';
}

export interface WorkspaceTraits {
  name: string;
  plan: 'free' | 'pro' | 'enterprise';
  member_count: number;
  created_at?: string;
}

export interface VideoRecordedEvent {
  video_id: string;
  recording_type: 'screen' | 'camera' | 'both';
  duration_seconds: number;
  has_audio: boolean;
  has_transcript: boolean;
}

export interface VideoSharedEvent {
  video_id: string;
  share_method: 'link' | 'embed' | 'email' | 'slack';
  recipients_count?: number;
}

export interface VideoViewedEvent {
  video_id: string;
  viewer_type: 'creator' | 'team_member' | 'external';
  watch_duration_seconds: number;
  video_duration_seconds: number;
  completion_percent: number;
}

// ... more event types ...

// Analytics instance
let analytics: AnalyticsBrowser;

export function initAnalytics(writeKey: string) {
  analytics = AnalyticsBrowser.load({ writeKey });
}

// Identity
export function identifyUser(userId: string, traits: UserTraits) {
  analytics.identify(userId, traits);
}

export function groupWorkspace(workspaceId: string, traits: WorkspaceTraits) {
  analytics.group(workspaceId, traits);
}

// Core Value Events
export function trackVideoRecorded(properties: VideoRecordedEvent) {
  analytics.track('Video Recorded', properties);
}

export function trackVideoShared(properties: VideoSharedEvent) {
  analytics.track('Video Shared', properties);
}

export function trackVideoViewed(properties: VideoViewedEvent) {
  analytics.track('Video Viewed', properties);
}

// ... more event functions ...
```

### Integration Example

```typescript
// Before (malformed)
analytics.track('video_created', { duration: videoLength });

// After (correct)
import { trackVideoRecorded } from './instrumentation/tracking';

trackVideoRecorded({
  video_id: video.id,
  recording_type: 'screen',
  duration_seconds: video.durationSeconds,
  has_audio: video.hasAudio,
  has_transcript: video.hasTranscript
});
```

---

## Phase 6: Maintain Over Time

### Three Months Later: New Feature Ships

Clipper adds **AI-powered video summaries**. Time to update the tracking plan.

### The Conversation

**User:** We're shipping AI summaries — users can generate a text summary of any video.

**Engineer:** Got it. That's a new core feature since it directly enhances the value of recorded videos. Let me add the tracking.

### Updates to `.telemetry/tracking-plan.yaml`

```yaml
# Added in version 1.1.0

  - name: Summary Generated
    category: core_value
    phase: core
    description: AI generates a summary for a video
    added_version: "1.1.0"
    properties:
      - name: video_id
        type: string
        required: true
      - name: video_duration_seconds
        type: integer
        required: true
      - name: summary_length_words
        type: integer
        required: true
      - name: generation_time_ms
        type: integer
        required: true
    expected_frequency: medium
    triggers:
      - User clicks "Generate Summary" button
      - Auto-summary enabled for workspace
```

### Update to `.telemetry/changelog.md`

```markdown
## [1.1.0] - 2026-05-15

### Added
- `Summary Generated` event for new AI summary feature
  - Properties: `video_id`, `video_duration_seconds`, `summary_length_words`, `generation_time_ms`

### Context
AI summaries shipped in product release 2.4. This is a core value feature — it enhances the value of every recorded video. Tracking generation time to monitor performance and costs.
```

### Regenerate Instrumentation

```typescript
// Added to instrumentation/tracking.ts

export interface SummaryGeneratedEvent {
  video_id: string;
  video_duration_seconds: number;
  summary_length_words: number;
  generation_time_ms: number;
}

export function trackSummaryGenerated(properties: SummaryGeneratedEvent) {
  analytics.track('Summary Generated', properties);
}
```

---

## The Complete `.telemetry/` Folder

After all phases, the folder structure looks like:

```
.telemetry/
├── product.md                    # Product understanding (Phase 1-2)
├── tracking-plan.yaml            # Canonical plan v1.1.0 (Phase 3, 6)
├── tracking-plan-summary.md      # Human-readable summary
├── changelog.md                  # Version history (Phase 6)
└── audits/
    ├── 2026-02-08.md            # Initial audit (Phase 4)
    └── 2026-05-20.md            # Post-AI-summary audit
```

---

## Key Takeaways

1. **Phases are explicit.** At every point, you know which phase you're in and what's expected.

2. **Value mapping drives prioritization.** The "primary value action" concept justifies why some events are critical and others are backlog.

3. **Ideal vs. current is always clear.** The audit explicitly separates "what should exist" from "what does exist." No defensive confusion.

4. **Artifacts persist.** Three months later, the maintenance phase has full context because `.telemetry/product.md` is still there.

5. **Templates accelerate, customization matters.** Starting from `collaboration-tools` template would have given 60% of this plan — the rest is Clipper-specific.

6. **Maintenance is ongoing.** The tracking plan evolves with the product. Version 1.1.0 happens naturally when features ship.
