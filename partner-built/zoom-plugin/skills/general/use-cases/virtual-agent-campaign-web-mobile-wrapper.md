# Virtual Agent Campaign Web and Mobile Wrapper

Use this flow when you want one Virtual Agent campaign strategy across website and native mobile wrappers.

## When to Use

- You already run campaign-based web embed and need consistent mobile behavior.
- You need native app callbacks for exit or support handoff while keeping web bot logic.
- You want to avoid rebuilding bot UI natively on each platform.

## Skill Chain

1. [virtual-agent](../../virtual-agent/SKILL.md)
2. [virtual-agent/web](../../virtual-agent/web/SKILL.md)
3. [virtual-agent/android](../../virtual-agent/android/SKILL.md) or [virtual-agent/ios](../../virtual-agent/ios/SKILL.md)
4. [contact-center](../../contact-center/SKILL.md)

## Typical Flow

1. Configure campaign targeting and publish bot flow.
2. Validate web behavior with campaign controls and event listeners.
3. Embed the same campaign URL in Android/iOS WebView containers.
4. Inject bridge handlers for exit, common commands, and `support_handoff`.
5. Apply URL governance (`_self`, `_blank`, `window.open`) consistently.
6. Release with shared monitoring for engagement start/end metrics.

## References

- [Virtual Agent Root Skill](../../virtual-agent/SKILL.md)
- [Web Lifecycle and Events](../../virtual-agent/web/concepts/lifecycle-and-events.md)
- [Android JS Bridge Patterns](../../virtual-agent/android/examples/js-bridge-patterns.md)
- [iOS JS Bridge Patterns](../../virtual-agent/ios/examples/js-bridge-patterns.md)
