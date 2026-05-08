---
name: zoom-general
description: Cross-product Zoom reference skill. Use after the workflow is clear when you need shared platform guidance, app-model comparisons, authentication context, scopes, marketplace considerations, or API-vs-MCP routing.
user-invocable: false
triggers:
  - "zoom integration"
  - "getting started"
  - "which zoom sdk"
  - "zoom platform"
  - "choose zoom api"
  - "zoom scopes"
  - "marketplace"
  - "cross-product"
  - "apis vs mcp"
  - "api vs mcp"
---

# Zoom General (Cross-Product Skills)

Background reference for cross-product Zoom questions. Prefer the workflow skills first, then use this file for shared platform guidance and routing detail.

## How `zoom-general` Routes a Complex Developer Query

Use `zoom-general` as the classifier and chaining layer:

1. detect product signals in the query
2. pick one primary skill
3. attach secondary skills for auth, events, or deployment edges
4. ask one short clarifier only when two routes match with similar confidence

Minimal implementation:

```ts
type SkillId =
  | 'zoom-general'
  | 'zoom-rest-api'
  | 'zoom-webhooks'
  | 'zoom-oauth'
  | 'zoom-meeting-sdk-web-component-view'
  | 'zoom-video-sdk'
  | 'zoom-mcp';

const hasAny = (q: string, words: string[]) => words.some((w) => q.includes(w));

function detectSignals(rawQuery: string) {
  const q = rawQuery.toLowerCase();
  return {
    meetingCustomUi: hasAny(q, ['zoom meeting', 'custom ui', 'component view', 'embed meeting']),
    customVideo: hasAny(q, ['video sdk', 'custom video session', 'peer-video-state-change']),
    restApi: hasAny(q, ['rest api', '/v2/', 'create meeting', 'list users', 's2s oauth']),
    webhooks: hasAny(q, ['webhook', 'x-zm-signature', 'event subscription', 'crc']),
    oauth: hasAny(q, ['oauth', 'pkce', 'token refresh', 'account_credentials']),
    mcp: hasAny(q, ['zoom mcp', 'agentic retrieval', 'tools/list', 'semantic meeting search']),
  };
}

function pickPrimarySkill(s: ReturnType<typeof detectSignals>): SkillId {
  if (s.meetingCustomUi) return 'zoom-meeting-sdk-web-component-view';
  if (s.mcp) return 'zoom-mcp';
  if (s.restApi) return 'zoom-rest-api';
  if (s.customVideo) return 'zoom-video-sdk';
  return 'zoom-general';
}

function buildChain(primary: SkillId, s: ReturnType<typeof detectSignals>): SkillId[] {
  const chain = [primary];
  if (s.oauth && !chain.includes('zoom-oauth')) chain.push('zoom-oauth');
  if (s.webhooks && !chain.includes('zoom-webhooks')) chain.push('zoom-webhooks');
  return chain;
}
```

Example:

- `Create a meeting, configure webhooks, and handle OAuth token refresh` ->
  `zoom-rest-api -> zoom-oauth -> zoom-webhooks`
- `Build a custom video UI for a Zoom meeting on web` ->
  `zoom-meeting-sdk-web-component-view`

For the full TypeScript implementation and handoff contract, use
[references/routing-implementation.md](references/routing-implementation.md).

## Choose Your Path

| I want to... | Use this skill |
|--------------|----------------|
| Build a custom web UI around a real Zoom meeting | **[zoom-meeting-sdk-web-component-view](../meeting-sdk/web/component-view/SKILL.md)** |
| Build deterministic automation/configuration/reporting with explicit request control | **[zoom-rest-api](../rest-api/SKILL.md)** |
| Receive event notifications (HTTP push) | **[zoom-webhooks](../webhooks/SKILL.md)** |
| Receive event notifications (WebSocket, low-latency) | **[zoom-websockets](../websockets/SKILL.md)** |
| Embed Zoom meetings in my app | **[zoom-meeting-sdk](../meeting-sdk/SKILL.md)** |
| Build custom video experiences (Web, React Native, Flutter, Android, iOS, macOS, Unity, Linux) | **[zoom-video-sdk](../video-sdk/SKILL.md)** |
| Build an app that runs inside Zoom client | **[zoom-apps-sdk](../zoom-apps-sdk/SKILL.md)** |
| Transcribe uploaded or stored media with AI Services Scribe | **[scribe](../scribe/SKILL.md)** |
| Access live audio/video/transcripts from meetings | **[zoom-rtms](../rtms/SKILL.md)** |
| Enable collaborative browsing for support | **[zoom-cobrowse-sdk](../cobrowse-sdk/SKILL.md)** |
| Build Contact Center apps and channel integrations | **[contact-center](../contact-center/SKILL.md)** |
| Build Virtual Agent web/mobile chatbot experiences | **[virtual-agent](../virtual-agent/SKILL.md)** |
| Build Zoom Phone integrations (Smart Embed, Phone API, webhooks, URI flows) | **[phone](../phone/SKILL.md)** |
| Build Team Chat apps and integrations | **[zoom-team-chat](../team-chat/SKILL.md)** |
| Build server-side integrations with Rivet (auth + webhooks + APIs) | **[rivet-sdk](../rivet-sdk/SKILL.md)** |
| Run browser/device/network preflight diagnostics before join | **[probe-sdk](../probe-sdk/SKILL.md)** |
| Add pre-built UI components for Video SDK | **[zoom-ui-toolkit](../ui-toolkit/SKILL.md)** |
| Implement OAuth authentication (all grant types) | **[zoom-oauth](../oauth/SKILL.md)** |
| Build AI-driven tool workflows (AI Companion/agents) over Zoom data | **[zoom-mcp](../zoom-mcp/SKILL.md)** |
| Build AI-driven Whiteboard workflows over Zoom Whiteboard MCP | **[zoom-mcp/whiteboard](../zoom-mcp/whiteboard/SKILL.md)** |
| Build enterprise AI systems with stable API core + AI tool layer | **[zoom-rest-api](../rest-api/SKILL.md)** + **[zoom-mcp](../zoom-mcp/SKILL.md)** |

## Planning Checkpoint: Rivet SDK (Optional)

When a user starts planning a server-side integration that combines auth + webhooks + API calls, ask this first:

- `Rivet SDK is a Node.js framework that bundles Zoom auth handling, webhook receivers, and typed API wrappers.`
- `Do you want to use Rivet SDK for faster scaffolding, or do you prefer a direct OAuth + REST implementation without Rivet?`

Routing after answer:

- If user chooses Rivet: chain `rivet-sdk` + `oauth` + `rest-api`.
- If user declines Rivet: chain `oauth` + `rest-api` (+ `webhooks` or product skill as needed).

### SDK vs REST Routing Matrix (Hard Stop)

| User intent | Correct path | Do not route to |
|-------------|--------------|-----------------|
| Embed Zoom meeting in app UI | `zoom-meeting-sdk` | REST-only `join_url` flow |
| Build custom web UI for a real Zoom meeting | `zoom-meeting-sdk-web-component-view` | `zoom-video-sdk` |
| Build custom video UI/session app | `zoom-video-sdk` | Meeting SDK or REST meeting links |
| Get browser join links / manage meeting resources | `zoom-rest-api` | Meeting SDK join implementation |

Routing guardrails:
- If user asks for SDK embed/join behavior, stay in SDK path.
- If the prompt says **meeting** plus **custom UI/video/layout/embed**, prefer `zoom-meeting-sdk-web-component-view`.
- Only use `zoom-video-sdk` when the user is building a custom session product rather than a Zoom meeting.
- Only use REST path for resource management, reporting, or link distribution unless user explicitly requests a mixed architecture.
- For executable classification/chaining logic and error handling, see [references/routing-implementation.md](references/routing-implementation.md).

### API vs MCP Routing Matrix (Hard Stop)

| User intent | Correct path | Why |
|-------------|--------------|-----|
| Deterministic backend automation, account/user configuration, reporting, scheduled jobs | `zoom-rest-api` | Explicit request/response control and repeatable behavior |
| AI agent chooses tools dynamically, cross-platform AI tool interoperability | `zoom-mcp` | MCP is optimized for dynamic tool discovery and agentic workflows |
| Enterprise AI architecture (stable core + adaptive AI layer) | `zoom-rest-api + zoom-mcp` | APIs run core system actions; MCP exposes curated AI tools/context |

Routing guardrails:
- Do not replace deterministic backend APIs with MCP-only routing.
- Do not force raw REST-first routing when the task is AI-agent tool orchestration.
- Prefer hybrid routing when the user needs both stable automation and AI-driven interactions.
- MCP remote server works over Streamable HTTP/SSE; use this path when the target client/agent supports MCP transports (for example Claude or VS Code).
- Do not design per-tenant custom MCP endpoint provisioning; Zoom MCP endpoints are shared at instance/cluster level.
- Source: https://developers.zoom.us/docs/mcp/library/resources/apis-vs-mcp/

### Ambiguity Resolution (Ask Before Routing)

When a prompt matches both API and MCP paths with similar confidence, ask one short clarifier before execution:

- `Do you want deterministic REST API automation, AI-agent MCP tooling, or a hybrid of both?`

Then route as:
- REST answer → `zoom-rest-api`
- MCP answer → `zoom-mcp`
- Hybrid answer → `zoom-rest-api + zoom-mcp`

### MCP Availability and Topology Notes

- Zoom-hosted MCP access is evolving; docs indicate a model where Zoom exposes product-scoped MCP servers (for example Meetings, Team Chat, Whiteboard).
- Use `zoom-mcp` as the parent MCP entry point.
- Route Whiteboard-specific MCP requests to **[zoom-mcp/whiteboard](../zoom-mcp/whiteboard/SKILL.md)**.
- When a request is product-specific and MCP coverage exists, route to that MCP product surface first; otherwise use REST/SDK skills for deterministic implementation.

### Webhooks vs WebSockets

Both receive event notifications, but differ in approach:

| Aspect | webhooks | zoom-websockets |
|--------|---------------|-----------------|
| Connection | HTTP POST to your endpoint | Persistent WebSocket |
| Latency | Higher | Lower |
| Security | Requires public endpoint | No exposed endpoint |
| Setup | Simpler | More complex |
| Best for | Most use cases | Real-time, security-sensitive |

## Common Use Cases

| Use Case | Description | Skills Needed |
|----------|-------------|---------------|
| [Meeting + Webhooks + OAuth Refresh](references/meeting-webhooks-oauth-refresh-orchestration.md) | Create a meeting, process real-time updates, and refresh OAuth tokens safely in one design | [zoom-rest-api](../rest-api/SKILL.md) + [zoom-oauth](../oauth/SKILL.md) + [zoom-webhooks](../webhooks/SKILL.md) |
| [Scribe Transcription Pipeline](use-cases/scribe-transcription-pipeline.md) | Transcribe uploaded files or S3 archives with AI Services Scribe using fast mode or batch jobs | [scribe](../scribe/SKILL.md) + optional [zoom-rest-api](../rest-api/SKILL.md) + optional [zoom-webhooks](../webhooks/SKILL.md) |
| [APIs vs MCP Routing](use-cases/apis-vs-mcp-routing.md) | Decide whether to route to deterministic Zoom APIs, AI-driven MCP, or a hybrid design | [zoom-rest-api](../rest-api/SKILL.md) and/or [zoom-mcp](../zoom-mcp/SKILL.md) |
| [Custom Meeting UI (Web)](use-cases/custom-meeting-ui-web.md) | Build a custom video UI for a real Zoom meeting in a web app using Meeting SDK Component View | [zoom-meeting-sdk-web-component-view](../meeting-sdk/web/component-view/SKILL.md) + [zoom-oauth](../oauth/SKILL.md) |
| [Meeting Automation](use-cases/meeting-automation.md) | Schedule, update, delete meetings programmatically | [zoom-rest-api](../rest-api/SKILL.md) |
| [Meeting Bots](use-cases/meeting-bots.md) | Build bots that join meetings for AI/transcription/recording | [meeting-sdk/linux](../meeting-sdk/linux/SKILL.md) + [zoom-rest-api](../rest-api/SKILL.md) + optional [zoom-webhooks](../webhooks/SKILL.md) |
| [High-Volume Meeting Platform](use-cases/high-volume-meeting-platform.md) | Design distributed meeting creation and event processing with retries, queues, and reconciliation | [zoom-rest-api](../rest-api/SKILL.md) + [zoom-webhooks](../webhooks/SKILL.md) + [zoom-oauth](../oauth/SKILL.md) |
| [Recording & Transcription](use-cases/recording-transcription.md) | Download recordings, get transcripts | [zoom-webhooks](../webhooks/SKILL.md) + [zoom-rest-api](../rest-api/SKILL.md) |
| [Recording Download Pipeline](use-cases/recording-download-pipeline.md) | Auto-download recordings to your own storage (S3, GCS, etc.) | [zoom-webhooks](../webhooks/SKILL.md) + [zoom-rest-api](../rest-api/SKILL.md) |
| [Real-Time Media Streams](use-cases/real-time-media-streams.md) | Access live audio, video, transcripts via WebSocket | [zoom-rtms](../rtms/SKILL.md) + [zoom-webhooks](../webhooks/SKILL.md) |
| [In-Meeting Apps](use-cases/in-meeting-apps.md) | Build apps that run inside Zoom meetings | [zoom-apps-sdk](../zoom-apps-sdk/SKILL.md) + [zoom-oauth](../oauth/SKILL.md) |
| [React Native Meeting Embed](use-cases/react-native-meeting-embed.md) | Embed meetings into iOS/Android React Native apps | [zoom-meeting-sdk-react-native](../meeting-sdk/react-native/SKILL.md) + [zoom-oauth](../oauth/SKILL.md) |
| [Native Meeting SDK Multi-Platform Delivery](use-cases/native-meeting-sdk-multi-platform.md) | Align Android, iOS, macOS, and Unreal Meeting SDK implementations under one auth/version strategy | [zoom-meeting-sdk](../meeting-sdk/SKILL.md) + platform skills |
| [Native Video SDK Multi-Platform Delivery](use-cases/native-video-sdk-multi-platform.md) | Align Android, iOS, macOS, and Unity Video SDK implementations under one auth/version strategy | [zoom-video-sdk](../video-sdk/SKILL.md) + platform skills |
| [Electron Meeting Embed](use-cases/electron-meeting-embed.md) | Embed meetings into desktop Electron apps | [zoom-meeting-sdk-electron](../meeting-sdk/electron/SKILL.md) + [zoom-oauth](../oauth/SKILL.md) |
| [Flutter Video Sessions](use-cases/flutter-video-sessions.md) | Build custom mobile video sessions in Flutter | [zoom-video-sdk-flutter](../video-sdk/flutter/SKILL.md) + [zoom-oauth](../oauth/SKILL.md) |
| [React Native Video Sessions](use-cases/react-native-video-sessions.md) | Build custom mobile video sessions in React Native | [zoom-video-sdk-react-native](../video-sdk/react-native/SKILL.md) + [zoom-oauth](../oauth/SKILL.md) |
| [Immersive Experiences](use-cases/immersive-experiences.md) | Custom video layouts with Layers API | [zoom-apps-sdk](../zoom-apps-sdk/SKILL.md) |
| [Collaborative Apps](use-cases/collaborative-apps.md) | Real-time shared state in meetings | [zoom-apps-sdk](../zoom-apps-sdk/SKILL.md) |
| [Contact Center App Lifecycle and Context Switching](use-cases/contact-center-app-lifecycle-and-context-switching.md) | Build Contact Center apps that handle engagement events and multi-engagement state | [contact-center](../contact-center/SKILL.md) + [zoom-apps-sdk](../zoom-apps-sdk/SKILL.md) |
| [Virtual Agent Campaign Web and Mobile Wrapper](use-cases/virtual-agent-campaign-web-mobile-wrapper.md) | Deliver one campaign-driven bot flow across web and native mobile wrappers | [virtual-agent](../virtual-agent/SKILL.md) + [contact-center](../contact-center/SKILL.md) |
| [Virtual Agent Knowledge Base Sync Pipeline](use-cases/virtual-agent-knowledge-base-sync-pipeline.md) | Sync external knowledge content into Zoom Virtual Agent using web sync or custom API connectors | [virtual-agent](../virtual-agent/SKILL.md) + [zoom-rest-api](../rest-api/SKILL.md) + [zoom-oauth](../oauth/SKILL.md) |
| [Zoom Phone Smart Embed CRM Integration](use-cases/zoom-phone-smart-embed-crm.md) | Build CRM dialer and call logging flows using Smart Embed plus Phone APIs | [phone](../phone/SKILL.md) + [zoom-oauth](../oauth/SKILL.md) + [zoom-webhooks](../webhooks/SKILL.md) |
| [Rivet Event-Driven API Orchestrator](use-cases/rivet-event-driven-api-orchestrator.md) | Build a Node.js backend that combines webhooks and API actions through Rivet module clients | [rivet-sdk](../rivet-sdk/SKILL.md) + [zoom-oauth](../oauth/SKILL.md) + [zoom-rest-api](../rest-api/SKILL.md) |
| [Probe SDK Preflight Readiness Gate](use-cases/probe-sdk-preflight-readiness-gate.md) | Add browser/device/network diagnostics and readiness policy before Meeting SDK or Video SDK joins | [probe-sdk](../probe-sdk/SKILL.md) + [zoom-meeting-sdk](../meeting-sdk/SKILL.md) or [zoom-video-sdk](../video-sdk/SKILL.md) |

## Complete Use-Case Index

- [APIs vs MCP Routing](use-cases/apis-vs-mcp-routing.md): choose API-only, MCP-only, or hybrid routing using official Zoom criteria.
- [AI Companion Integration](use-cases/ai-companion-integration.md): connect Zoom AI Companion capabilities into your app workflow.
- [AI Integration](use-cases/ai-integration.md): add summarization, transcription, or assistant logic using Zoom data surfaces.
- [Backend Automation (S2S OAuth)](use-cases/backend-automation-s2s-oauth.md): run server-side jobs with account-level OAuth credentials.
- [Collaborative Apps](use-cases/collaborative-apps.md): build shared in-meeting app state and interactions.
- [Contact Center Integration](use-cases/contact-center-integration.md): connect Zoom Contact Center signals into external systems.
- [Contact Center App Lifecycle and Context Switching](use-cases/contact-center-app-lifecycle-and-context-switching.md): implement event-driven engagement state and safe context switching in Contact Center apps.
- [Virtual Agent Campaign Web and Mobile Wrapper](use-cases/virtual-agent-campaign-web-mobile-wrapper.md): deploy campaign-based Virtual Agent chat across website and Android/iOS WebView wrappers.
- [Virtual Agent Knowledge Base Sync Pipeline](use-cases/virtual-agent-knowledge-base-sync-pipeline.md): automate knowledge-base ingestion with web sync strategy or custom API connector.
- [Zoom Phone Smart Embed CRM Integration](use-cases/zoom-phone-smart-embed-crm.md): integrate Smart Embed events, Phone APIs, and CRM workflows with migration-safe data handling.
- [Rivet Event-Driven API Orchestrator](use-cases/rivet-event-driven-api-orchestrator.md): build a Node.js backend that combines webhook handling and API orchestration with Rivet.
- [Probe SDK Preflight Readiness Gate](use-cases/probe-sdk-preflight-readiness-gate.md): run browser/device/network diagnostics before launching meeting or video session workflows.
- [Custom Video](use-cases/custom-video.md): decide between Video SDK and related components for custom session UX.
- [Custom Meeting UI (Web)](use-cases/custom-meeting-ui-web.md): use Meeting SDK Component View for a custom UI around a real Zoom meeting.
- [Scribe Transcription Pipeline](use-cases/scribe-transcription-pipeline.md): use AI Services Scribe for on-demand file transcription and batch archive processing.
- [Video SDK Bring Your Own Storage](use-cases/video-sdk-bring-your-own-storage.md): configure Video SDK cloud recordings to write directly to your own S3 bucket.
- [Customer Support Cobrowsing](use-cases/customer-support-cobrowsing.md): implement customer-agent collaborative browsing support flows.
- [Embed Meetings](use-cases/embed-meetings.md): embed Zoom meeting experience into your app.
- [Form Completion Assistant](use-cases/form-completion-assistant.md): build guided flows for form filling and completion assistance.
- [HD Video Resolution](use-cases/hd-video-resolution.md): enable and troubleshoot high-definition video requirements.
- [High-Volume Meeting Platform](use-cases/high-volume-meeting-platform.md): build distributed meeting creation and event processing with concrete fallback patterns.
- [Immersive Experiences](use-cases/immersive-experiences.md): use Zoom Apps Layers APIs for custom in-meeting visuals.
- [In-Meeting Apps](use-cases/in-meeting-apps.md): build Zoom Apps that run directly inside meeting and webinar contexts.
- [Marketplace Publishing](use-cases/marketplace-publishing.md): prepare and ship a Zoom app through Marketplace review.
- [Meeting Automation](use-cases/meeting-automation.md): create, update, and manage meetings programmatically.
- [Meeting Bots](use-cases/meeting-bots.md): build bots for meeting join, capture, and real-time analysis.
- [Native Meeting SDK Multi-Platform Delivery](use-cases/native-meeting-sdk-multi-platform.md): standardize Android, iOS, macOS, and Unreal Meeting SDK delivery with shared auth and version controls.
- [Native Video SDK Multi-Platform Delivery](use-cases/native-video-sdk-multi-platform.md): standardize Android, iOS, macOS, and Unity Video SDK delivery with shared auth and version controls.
- [Meeting Details with Events](use-cases/meeting-details-with-events.md): combine REST retrieval with webhook event streams.
- [Minutes Calculation](use-cases/minutes-calculation.md): compute usage and minute metrics across meetings/sessions.
- [Prebuilt Video UI](use-cases/prebuilt-video-ui.md): use UI Toolkit for faster Video SDK-based UI delivery.
- [QSS Monitoring](use-cases/qss-monitoring.md): monitor Zoom quality statistics and performance indicators.
- [Raw Recording](use-cases/raw-recording.md): capture raw streams for custom recording and processing pipelines.
- [Electron Meeting Embed](use-cases/electron-meeting-embed.md): embed meetings in an Electron desktop application.
- [Flutter Video Sessions](use-cases/flutter-video-sessions.md): build Video SDK sessions in Flutter mobile apps.
- [React Native Meeting Embed](use-cases/react-native-meeting-embed.md): embed Meeting SDK into React Native apps.
- [React Native Video Sessions](use-cases/react-native-video-sessions.md): build custom video sessions in React Native.
- [Real-Time Media Streams](use-cases/real-time-media-streams.md): consume live media/transcript streams via RTMS.
- [Recording Download Pipeline](use-cases/recording-download-pipeline.md): automate recording retrieval and storage pipelines.
- [Recording & Transcription](use-cases/recording-transcription.md): manage post-meeting recordings and transcript workflows.
- [Retrieve Meeting and Subscribe Events](use-cases/retrieve-meeting-and-subscribe-events.md): join REST meeting fetch with event subscriptions.
- [SaaS App OAuth Integration](use-cases/saas-app-oauth-integration.md): implement user-level OAuth in multi-tenant SaaS apps.
- [SDK Size Optimization](use-cases/sdk-size-optimization.md): reduce bundle/runtime footprint for SDK-based apps.
- [SDK Wrappers and GUI](use-cases/sdk-wrappers-gui.md): evaluate wrapper patterns and GUI frameworks around SDKs.
- [Team Chat LLM Bot](use-cases/team-chat-llm-bot.md): build a Team Chat bot with LLM-powered responses.
- [Testing and Development](use-cases/testing-development.md): local testing patterns, mocks, and safe development loops.
- [Token and Scope Troubleshooting](use-cases/token-and-scope-troubleshooting.md): debug OAuth scope and token mismatch issues.
- [Transcription Bot (Linux)](use-cases/transcription-bot-linux.md): run Linux meeting bots for live transcription workloads.
- [Usage Reporting and Analytics](use-cases/usage-reporting-analytics.md): collect and analyze usage/reporting data.
- [User and Meeting Creation](use-cases/user-and-meeting-creation.md): provision users and schedule meetings in one flow.
- [Web SDK Embedding](use-cases/web-sdk-embedding.md): embed meeting experiences in browser-based web apps.
- [Server-to-Server OAuth with Webhooks](use-cases/server-to-server-oauth-with-webhooks.md): combine account OAuth with event-driven backend processing.
- [Meeting Links vs Embedding](use-cases/meeting-links-vs-embedding.md): choose between `join_url` distribution and SDK embedding.
- [Enterprise App Deployment](use-cases/enterprise-app-deployment.md): deploy, govern, and operate Zoom integrations at enterprise scale.

## Prerequisites

1. Zoom account (Pro, Business, or Enterprise)
2. App created in [Zoom App Marketplace](https://marketplace.zoom.us/)
3. OAuth credentials (Client ID and Secret)

## References

- [Known Limitations & Quirks](references/known-limitations.md)

## Quick Start

1. Go to [marketplace.zoom.us](https://marketplace.zoom.us/)
2. Click **Develop** → **Build App**
3. Select app type (see [references/app-types.md](references/app-types.md))
4. Configure OAuth and scopes
5. Copy credentials to your application

## Detailed References

- **[references/authentication.md](references/authentication.md)** - OAuth 2.0, S2S OAuth, JWT patterns
- **[references/app-types.md](references/app-types.md)** - Decision guide for app types
- **[references/scopes.md](references/scopes.md)** - OAuth scopes reference
- **[references/marketplace.md](references/marketplace.md)** - Marketplace portal navigation
- **[references/query-routing-playbook.md](references/query-routing-playbook.md)** - Route complex queries to the right specialized skills
- **[references/interview-answer-routing.md](references/interview-answer-routing.md)** - Short interview-ready answer pattern for zoom-general routing
- **[references/routing-implementation.md](references/routing-implementation.md)** - Concrete TypeScript query classification and skill handoff contract
- **[references/automatic-skill-chaining-rest-webhooks.md](references/automatic-skill-chaining-rest-webhooks.md)** - Executable process for REST + webhook chained workflows
- **[references/meeting-webhooks-oauth-refresh-orchestration.md](references/meeting-webhooks-oauth-refresh-orchestration.md)** - Concrete design for meeting creation + webhook updates + OAuth token refresh
- **[references/distributed-meeting-fallback-architecture.md](references/distributed-meeting-fallback-architecture.md)** - High-volume distributed architecture with retries, circuit breakers, and reconciliation fallbacks
- **[references/community-repos.md](references/community-repos.md)** - Curated official Zoom sample repositories by product

## SDK Maintenance

- **[references/sdk-upgrade-guide.md](references/sdk-upgrade-guide.md)** - Version policy, upgrade steps
- **[references/sdk-upgrade-workflow.md](references/sdk-upgrade-workflow.md)** - Changelog + RSS, version-by-version reusable upgrade workflow
- **[references/sdk-logs-troubleshooting.md](references/sdk-logs-troubleshooting.md)** - Collecting SDK logs

## Resources

- **Official docs**: https://developers.zoom.us/
- **Marketplace**: https://marketplace.zoom.us/
- **Developer forum**: https://devforum.zoom.us/

## Environment Variables

- See [references/environment-variables.md](references/environment-variables.md) for standardized `.env` keys and where to find each value.

## Operations

- [RUNBOOK.md](RUNBOOK.md) - 5-minute preflight and debugging checklist.
