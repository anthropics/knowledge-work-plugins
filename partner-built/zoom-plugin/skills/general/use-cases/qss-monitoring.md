# QSS Monitoring

Quality of Service Subscription for real-time meeting quality monitoring.

## Overview

QSS (Quality of Service Subscription) provides near real-time QoS telemetry for Zoom Meetings, Webinars, and Phone. IT teams can monitor network quality, diagnose issues, and track performance at scale.

## Skills Needed

- **webhooks** - Receive QSS events
- **zoom-rest-api** - QSS API endpoints

## What QSS Provides

### Quality Metrics

| Metric | Description |
|--------|-------------|
| Bitrate | Data transfer rate |
| Latency | Network delay |
| Jitter | Latency variation |
| Packet Loss | Lost data packets |
| Resolution | Video resolution |
| Frame Rate | Video FPS |
| CPU Usage | Client CPU load |

### Usage Metrics

| Metric | Description |
|--------|-------------|
| Device | Device type and model |
| Network | Network type and quality |
| Signaling Region | Connection region |
| Client Version | Zoom client version |
| Audio I/O | Audio device info |
| Video I/O | Camera info |

## Data Delivery

| Aspect | Details |
|--------|---------|
| **Frequency** | ~1 event per minute per participant |
| **Delivery** | Webhook events |
| **Retention** | 7 days via Webhook Logs API |
| **Products** | Meetings, Webinars, Phone |

## Prerequisites

- Business or Enterprise Zoom account
- QSS add-on subscription
- Webhook endpoint configured
- Internal dashboard system (recommended)

## Setup

### 1. Enable QSS

Contact Zoom sales to add QSS to your account.

### 2. Configure Webhooks

Subscribe to QSS events in your app's Event Subscriptions.

### 3. Handle Events

```javascript
app.post('/webhook', (req, res) => {
  const { event, payload } = req.body;
  
  if (event.startsWith('qss.')) {
    // Process QSS data
    const { meeting_id, participant_id, metrics } = payload;
    
    // Send to your monitoring dashboard
    dashboard.ingest({
      meetingId: meeting_id,
      participantId: participant_id,
      bitrate: metrics.bitrate,
      latency: metrics.latency,
      jitter: metrics.jitter,
      packetLoss: metrics.packet_loss
    });
  }
  
  res.status(200).send();
});
```

## Use Cases

| Use Case | Description |
|----------|-------------|
| **Network monitoring** | Track network quality across organization |
| **Troubleshooting** | Diagnose call quality issues in real-time |
| **Capacity planning** | Understand bandwidth usage patterns |
| **SLA compliance** | Monitor meeting quality for SLA reporting |
| **Proactive alerts** | Alert IT when quality degrades |

## Integration

QSS data can be integrated with:
- Splunk
- Datadog
- Grafana
- Custom dashboards
- ITSM tools

## Resources

- **QSS docs**: https://developers.zoom.us/docs/api/rest/qss-api/
- **QSS API reference**: https://developers.zoom.us/docs/api/rest/reference/qss/methods/
