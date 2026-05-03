# Minutes Calculation for Billing

Calculate usage minutes for Video SDK sessions and Meeting SDK meetings for billing and cost management.

## Overview

Zoom SDKs are billed based on **participant-minutes**. This guide covers how to track and calculate usage for accurate billing projections and cost optimization.

## Skills Needed

- **zoom-rest-api** - Reports API
- **webhooks** - Real-time tracking
- **zoom-video-sdk** - Session Quality API

## Billing Models

| SDK | Billing Unit | Calculation |
|-----|--------------|-------------|
| Video SDK | Participant-minutes | Sum of (each participant's session duration) |
| Meeting SDK | Host minutes | Based on meeting duration, not participant count |

**Example**: A 30-minute Video SDK session with 4 participants = 120 participant-minutes.

## Video SDK Usage Tracking

### Method 1: Session Quality API (Recommended)

Most accurate method using Zoom's built-in analytics.

```javascript
const axios = require('axios');

// Get session details including participant minutes
async function getSessionUsage(sessionId) {
  const response = await axios.get(
    `https://api.zoom.us/v2/videosdk/sessions/${sessionId}`,
    {
      headers: { 'Authorization': `Bearer ${accessToken}` }
    }
  );
  
  return {
    sessionName: response.data.session_name,
    startTime: response.data.start_time,
    endTime: response.data.end_time,
    totalMinutes: response.data.duration, // Total session minutes
    participantCount: response.data.participant_count
  };
}

// Get participant-level breakdown
async function getSessionParticipants(sessionId) {
  const response = await axios.get(
    `https://api.zoom.us/v2/videosdk/sessions/${sessionId}/participants`,
    {
      params: { page_size: 300 },
      headers: { 'Authorization': `Bearer ${accessToken}` }
    }
  );
  
  // Calculate participant-minutes
  const participants = response.data.participants.map(p => {
    const joinTime = new Date(p.join_time);
    const leaveTime = new Date(p.leave_time);
    const durationMinutes = (leaveTime - joinTime) / 1000 / 60;
    
    return {
      name: p.user_name,
      joinTime: p.join_time,
      leaveTime: p.leave_time,
      durationMinutes: Math.round(durationMinutes * 100) / 100
    };
  });
  
  const totalParticipantMinutes = participants.reduce(
    (sum, p) => sum + p.durationMinutes, 0
  );
  
  return {
    participants,
    totalParticipantMinutes: Math.round(totalParticipantMinutes * 100) / 100
  };
}

// Get all sessions in date range
async function getSessionsInRange(from, to) {
  const response = await axios.get(
    'https://api.zoom.us/v2/videosdk/sessions',
    {
      params: { from, to, page_size: 300 },
      headers: { 'Authorization': `Bearer ${accessToken}` }
    }
  );
  
  return response.data.sessions;
}

// Calculate monthly usage
async function calculateMonthlyUsage(year, month) {
  const from = `${year}-${String(month).padStart(2, '0')}-01`;
  const lastDay = new Date(year, month, 0).getDate();
  const to = `${year}-${String(month).padStart(2, '0')}-${lastDay}`;
  
  const sessions = await getSessionsInRange(from, to);
  
  let totalParticipantMinutes = 0;
  const sessionDetails = [];
  
  for (const session of sessions) {
    const participants = await getSessionParticipants(session.id);
    totalParticipantMinutes += participants.totalParticipantMinutes;
    
    sessionDetails.push({
      sessionId: session.id,
      sessionName: session.session_name,
      date: session.start_time,
      participantMinutes: participants.totalParticipantMinutes
    });
  }
  
  return {
    period: `${year}-${String(month).padStart(2, '0')}`,
    totalSessions: sessions.length,
    totalParticipantMinutes: Math.round(totalParticipantMinutes),
    sessions: sessionDetails
  };
}
```

### Method 2: Real-Time Webhook Tracking

Track usage in real-time as sessions happen.

```javascript
const express = require('express');
const app = express();

// In-memory storage (use database in production)
const activeSessions = new Map();
const usageRecords = [];

app.post('/webhook', express.json(), (req, res) => {
  const { event, payload } = req.body;
  
  switch (event) {
    case 'session.started':
      handleSessionStarted(payload);
      break;
    case 'session.ended':
      handleSessionEnded(payload);
      break;
    case 'session.participant_joined':
      handleParticipantJoined(payload);
      break;
    case 'session.participant_left':
      handleParticipantLeft(payload);
      break;
  }
  
  res.status(200).send();
});

function handleSessionStarted(payload) {
  const { object } = payload;
  activeSessions.set(object.id, {
    sessionId: object.id,
    sessionName: object.session_name,
    startTime: new Date(object.start_time),
    participants: new Map()
  });
}

function handleSessionEnded(payload) {
  const { object } = payload;
  const session = activeSessions.get(object.id);
  
  if (session) {
    // Calculate final usage for any remaining participants
    const endTime = new Date(object.end_time);
    let totalMinutes = 0;
    
    session.participants.forEach((participant, participantId) => {
      if (!participant.leaveTime) {
        participant.leaveTime = endTime;
      }
      const duration = (participant.leaveTime - participant.joinTime) / 1000 / 60;
      totalMinutes += duration;
    });
    
    // Record usage
    usageRecords.push({
      sessionId: object.id,
      sessionName: session.sessionName,
      startTime: session.startTime,
      endTime: endTime,
      totalParticipantMinutes: Math.round(totalMinutes * 100) / 100,
      participantCount: session.participants.size
    });
    
    activeSessions.delete(object.id);
  }
}

function handleParticipantJoined(payload) {
  const { object } = payload;
  const session = activeSessions.get(object.session_id);
  
  if (session) {
    session.participants.set(object.participant.participant_id, {
      name: object.participant.user_name,
      joinTime: new Date(object.participant.join_time),
      leaveTime: null
    });
  }
}

function handleParticipantLeft(payload) {
  const { object } = payload;
  const session = activeSessions.get(object.session_id);
  
  if (session) {
    const participant = session.participants.get(object.participant.participant_id);
    if (participant) {
      participant.leaveTime = new Date(object.participant.leave_time);
    }
  }
}

// Get current month usage
app.get('/usage/current-month', (req, res) => {
  const now = new Date();
  const startOfMonth = new Date(now.getFullYear(), now.getMonth(), 1);
  
  const monthlyRecords = usageRecords.filter(r => 
    new Date(r.startTime) >= startOfMonth
  );
  
  const totalMinutes = monthlyRecords.reduce(
    (sum, r) => sum + r.totalParticipantMinutes, 0
  );
  
  res.json({
    period: `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`,
    totalSessions: monthlyRecords.length,
    totalParticipantMinutes: Math.round(totalMinutes),
    records: monthlyRecords
  });
});
```

### Method 3: Client-Side Tracking

Track locally in your SDK application.

```javascript
// React Native / JavaScript SDK tracking
class UsageTracker {
  constructor() {
    this.sessionStart = null;
    this.participants = new Map();
  }
  
  onSessionJoin() {
    this.sessionStart = new Date();
  }
  
  onUserJoin(user) {
    this.participants.set(user.id, {
      name: user.name,
      joinTime: new Date(),
      leaveTime: null
    });
  }
  
  onUserLeave(user) {
    const participant = this.participants.get(user.id);
    if (participant) {
      participant.leaveTime = new Date();
    }
  }
  
  calculateUsage() {
    const now = new Date();
    let totalMinutes = 0;
    
    this.participants.forEach(participant => {
      const endTime = participant.leaveTime || now;
      const duration = (endTime - participant.joinTime) / 1000 / 60;
      totalMinutes += duration;
    });
    
    return {
      sessionDuration: (now - this.sessionStart) / 1000 / 60,
      totalParticipantMinutes: Math.round(totalMinutes * 100) / 100,
      participantCount: this.participants.size
    };
  }
  
  // Send to your backend periodically
  async reportUsage() {
    const usage = this.calculateUsage();
    await fetch('/api/usage', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(usage)
    });
  }
}
```

```cpp
// Windows/C++ SDK tracking
class UsageTracker : public IZoomVideoSDKDelegate {
private:
    std::chrono::system_clock::time_point sessionStart;
    struct ParticipantUsage {
        std::wstring name;
        std::chrono::system_clock::time_point joinTime;
        std::chrono::system_clock::time_point leaveTime;
        bool hasLeft = false;
    };
    std::map<std::wstring, ParticipantUsage> participants;
    
public:
    void onSessionJoin() override {
        sessionStart = std::chrono::system_clock::now();
    }
    
    void onUserJoin(IZoomVideoSDKUserHelper* helper,
                    IVideoSDKVector<IZoomVideoSDKUser*>* users) override {
        for (int i = 0; i < users->GetCount(); i++) {
            auto user = users->GetItem(i);
            ParticipantUsage usage;
            usage.name = user->getUserName();
            usage.joinTime = std::chrono::system_clock::now();
            participants[user->getUserID()] = usage;
        }
    }
    
    void onUserLeave(IZoomVideoSDKUserHelper* helper,
                     IVideoSDKVector<IZoomVideoSDKUser*>* users) override {
        for (int i = 0; i < users->GetCount(); i++) {
            auto user = users->GetItem(i);
            auto it = participants.find(user->getUserID());
            if (it != participants.end()) {
                it->second.leaveTime = std::chrono::system_clock::now();
                it->second.hasLeft = true;
            }
        }
    }
    
    double calculateTotalMinutes() {
        auto now = std::chrono::system_clock::now();
        double totalMinutes = 0;
        
        for (const auto& [id, participant] : participants) {
            auto endTime = participant.hasLeft ? participant.leaveTime : now;
            auto duration = std::chrono::duration_cast<std::chrono::minutes>(
                endTime - participant.joinTime
            );
            totalMinutes += duration.count();
        }
        
        return totalMinutes;
    }
};
```

## Meeting SDK Usage Tracking

### Reports API for Past Meetings

```javascript
// Get meeting usage from Reports API
async function getMeetingUsage(meetingId) {
  // Note: Double-encode UUID if it contains / or //
  const encodedId = meetingId.includes('/') 
    ? encodeURIComponent(encodeURIComponent(meetingId))
    : meetingId;
  
  const [meeting, participants] = await Promise.all([
    axios.get(
      `https://api.zoom.us/v2/report/meetings/${encodedId}`,
      { headers: { 'Authorization': `Bearer ${accessToken}` }}
    ),
    axios.get(
      `https://api.zoom.us/v2/report/meetings/${encodedId}/participants`,
      { 
        params: { page_size: 300 },
        headers: { 'Authorization': `Bearer ${accessToken}` }
      }
    )
  ]);
  
  // Calculate participant-minutes
  const participantMinutes = participants.data.participants.map(p => {
    const duration = p.duration; // Already in seconds
    return {
      name: p.name,
      email: p.user_email,
      durationMinutes: Math.round(duration / 60 * 100) / 100
    };
  });
  
  const totalParticipantMinutes = participantMinutes.reduce(
    (sum, p) => sum + p.durationMinutes, 0
  );
  
  return {
    meetingId: meetingId,
    topic: meeting.data.topic,
    startTime: meeting.data.start_time,
    endTime: meeting.data.end_time,
    hostMinutes: meeting.data.duration, // Meeting duration in minutes
    totalParticipantMinutes: Math.round(totalParticipantMinutes),
    participantCount: participants.data.participants.length,
    participants: participantMinutes
  };
}

// Get daily usage summary
async function getDailyUsageSummary(year, month) {
  const response = await axios.get(
    'https://api.zoom.us/v2/report/daily',
    {
      params: { year, month },
      headers: { 'Authorization': `Bearer ${accessToken}` }
    }
  );
  
  // Aggregate daily data
  const summary = response.data.dates.reduce((acc, day) => {
    acc.totalMeetings += day.meetings;
    acc.totalMinutes += day.meeting_minutes;
    acc.totalParticipants += day.participants;
    return acc;
  }, { totalMeetings: 0, totalMinutes: 0, totalParticipants: 0 });
  
  return {
    period: `${year}-${String(month).padStart(2, '0')}`,
    ...summary,
    dailyBreakdown: response.data.dates
  };
}

// Get user-specific meeting report
async function getUserMeetingReport(userId, from, to) {
  const response = await axios.get(
    `https://api.zoom.us/v2/report/users/${userId}/meetings`,
    {
      params: { from, to, page_size: 300 },
      headers: { 'Authorization': `Bearer ${accessToken}` }
    }
  );
  
  const totalMinutes = response.data.meetings.reduce(
    (sum, m) => sum + m.duration, 0
  );
  
  return {
    userId,
    period: { from, to },
    totalMeetings: response.data.meetings.length,
    totalHostMinutes: totalMinutes,
    meetings: response.data.meetings
  };
}
```

### Webhook-Based Tracking

```javascript
// Meeting SDK webhook events
app.post('/meeting-webhook', express.json(), (req, res) => {
  const { event, payload } = req.body;
  
  switch (event) {
    case 'meeting.started':
      handleMeetingStarted(payload);
      break;
    case 'meeting.ended':
      handleMeetingEnded(payload);
      break;
    case 'meeting.participant_joined':
      handleMeetingParticipantJoined(payload);
      break;
    case 'meeting.participant_left':
      handleMeetingParticipantLeft(payload);
      break;
  }
  
  res.status(200).send();
});

// Store in database for billing
async function handleMeetingEnded(payload) {
  const { object } = payload;
  
  await db.meetings.insert({
    meetingId: object.id,
    uuid: object.uuid,
    topic: object.topic,
    hostId: object.host_id,
    startTime: object.start_time,
    endTime: object.end_time,
    durationMinutes: object.duration,
    participantCount: object.participant_count
  });
}
```

## Cost Estimation

### Video SDK Cost Calculator

```javascript
// Pricing tiers (example - check current Zoom pricing)
const PRICING_TIERS = [
  { upTo: 10000, pricePerMinute: 0.0050 },
  { upTo: 50000, pricePerMinute: 0.0040 },
  { upTo: 100000, pricePerMinute: 0.0030 },
  { upTo: Infinity, pricePerMinute: 0.0025 }
];

function estimateMonthlyCost(participantMinutes) {
  let remaining = participantMinutes;
  let totalCost = 0;
  let previousLimit = 0;
  
  for (const tier of PRICING_TIERS) {
    const tierMinutes = Math.min(remaining, tier.upTo - previousLimit);
    if (tierMinutes <= 0) break;
    
    totalCost += tierMinutes * tier.pricePerMinute;
    remaining -= tierMinutes;
    previousLimit = tier.upTo;
  }
  
  return {
    participantMinutes,
    estimatedCost: Math.round(totalCost * 100) / 100,
    currency: 'USD'
  };
}

// Project usage for the month
function projectMonthlyUsage(currentUsage, dayOfMonth, daysInMonth) {
  const dailyAverage = currentUsage / dayOfMonth;
  const projectedTotal = dailyAverage * daysInMonth;
  
  return {
    currentUsage,
    dailyAverage: Math.round(dailyAverage),
    projectedMonthlyUsage: Math.round(projectedTotal),
    projectedCost: estimateMonthlyCost(projectedTotal)
  };
}
```

### Year-to-Date (YTD) Usage

Calculate cumulative usage from the start of the year.

```javascript
// Calculate YTD usage for Video SDK
async function getYTDUsage() {
  const now = new Date();
  const year = now.getFullYear();
  const currentMonth = now.getMonth() + 1;
  
  // Fetch all months in parallel
  const monthPromises = [];
  for (let month = 1; month <= currentMonth; month++) {
    monthPromises.push(calculateMonthlyUsage(year, month));
  }
  
  const monthlyResults = await Promise.all(monthPromises);
  
  // Aggregate YTD totals
  const ytdTotals = monthlyResults.reduce((acc, month) => {
    acc.totalSessions += month.totalSessions;
    acc.totalParticipantMinutes += month.totalParticipantMinutes;
    return acc;
  }, { totalSessions: 0, totalParticipantMinutes: 0 });
  
  // Monthly breakdown for trending
  const monthlyBreakdown = monthlyResults.map(m => ({
    period: m.period,
    sessions: m.totalSessions,
    participantMinutes: m.totalParticipantMinutes
  }));
  
  // Calculate month-over-month growth
  const growthRates = [];
  for (let i = 1; i < monthlyBreakdown.length; i++) {
    const prev = monthlyBreakdown[i - 1].participantMinutes;
    const curr = monthlyBreakdown[i].participantMinutes;
    growthRates.push({
      period: monthlyBreakdown[i].period,
      growthRate: prev > 0 ? ((curr - prev) / prev * 100).toFixed(1) + '%' : 'N/A'
    });
  }
  
  return {
    year,
    asOfDate: now.toISOString().split('T')[0],
    ytdTotals: {
      totalSessions: ytdTotals.totalSessions,
      totalParticipantMinutes: Math.round(ytdTotals.totalParticipantMinutes),
      estimatedCost: estimateMonthlyCost(ytdTotals.totalParticipantMinutes)
    },
    monthlyBreakdown,
    growthRates,
    averageMonthlyUsage: Math.round(ytdTotals.totalParticipantMinutes / currentMonth)
  };
}

// Calculate YTD usage for Meeting SDK (via Reports API)
async function getMeetingSDKYTDUsage() {
  const now = new Date();
  const year = now.getFullYear();
  const currentMonth = now.getMonth() + 1;
  
  // Fetch daily reports for each month
  const monthPromises = [];
  for (let month = 1; month <= currentMonth; month++) {
    monthPromises.push(getDailyUsageSummary(year, month));
  }
  
  const monthlyResults = await Promise.all(monthPromises);
  
  // Aggregate YTD
  const ytdTotals = monthlyResults.reduce((acc, month) => {
    acc.totalMeetings += month.totalMeetings;
    acc.totalMinutes += month.totalMinutes;
    acc.totalParticipants += month.totalParticipants;
    return acc;
  }, { totalMeetings: 0, totalMinutes: 0, totalParticipants: 0 });
  
  return {
    year,
    asOfDate: now.toISOString().split('T')[0],
    ytdTotals,
    monthlyBreakdown: monthlyResults.map(m => ({
      period: m.period,
      meetings: m.totalMeetings,
      minutes: m.totalMinutes,
      participants: m.totalParticipants
    })),
    averageMonthly: {
      meetings: Math.round(ytdTotals.totalMeetings / currentMonth),
      minutes: Math.round(ytdTotals.totalMinutes / currentMonth),
      participants: Math.round(ytdTotals.totalParticipants / currentMonth)
    }
  };
}

// Compare YTD to previous year
async function getYTDComparison() {
  const now = new Date();
  const currentYear = now.getFullYear();
  const currentMonth = now.getMonth() + 1;
  
  // Get current YTD
  const currentYTD = await getYTDUsage();
  
  // Get same period last year (Jan through current month)
  const lastYearPromises = [];
  for (let month = 1; month <= currentMonth; month++) {
    lastYearPromises.push(calculateMonthlyUsage(currentYear - 1, month));
  }
  
  const lastYearResults = await Promise.all(lastYearPromises);
  const lastYearTotal = lastYearResults.reduce(
    (sum, m) => sum + m.totalParticipantMinutes, 0
  );
  
  const yearOverYearChange = lastYearTotal > 0
    ? ((currentYTD.ytdTotals.totalParticipantMinutes - lastYearTotal) / lastYearTotal * 100)
    : null;
  
  return {
    currentYear: {
      year: currentYear,
      totalParticipantMinutes: currentYTD.ytdTotals.totalParticipantMinutes
    },
    previousYear: {
      year: currentYear - 1,
      totalParticipantMinutes: Math.round(lastYearTotal),
      note: `Same period (Jan-${currentMonth})`
    },
    yearOverYearChange: yearOverYearChange !== null 
      ? yearOverYearChange.toFixed(1) + '%' 
      : 'N/A (no prior year data)'
  };
}

// Project full year usage based on YTD
function projectAnnualUsage(ytdMinutes, currentMonth) {
  const monthsRemaining = 12 - currentMonth;
  const monthlyAverage = ytdMinutes / currentMonth;
  const projectedRemaining = monthlyAverage * monthsRemaining;
  const projectedAnnual = ytdMinutes + projectedRemaining;
  
  return {
    ytdMinutes: Math.round(ytdMinutes),
    projectedAnnualMinutes: Math.round(projectedAnnual),
    projectedAnnualCost: estimateMonthlyCost(projectedAnnual),
    monthlyAverage: Math.round(monthlyAverage),
    confidence: currentMonth >= 6 ? 'high' : currentMonth >= 3 ? 'medium' : 'low'
  };
}
```

### Usage Dashboard

```javascript
// Build a usage dashboard
async function getUsageDashboard() {
  const now = new Date();
  const year = now.getFullYear();
  const month = now.getMonth() + 1;
  const dayOfMonth = now.getDate();
  const daysInMonth = new Date(year, month, 0).getDate();
  
  // Get current month usage
  const usage = await calculateMonthlyUsage(year, month);
  
  // Calculate projections
  const projection = projectMonthlyUsage(
    usage.totalParticipantMinutes,
    dayOfMonth,
    daysInMonth
  );
  
  // Get previous month for comparison
  const prevMonth = month === 1 ? 12 : month - 1;
  const prevYear = month === 1 ? year - 1 : year;
  const previousUsage = await calculateMonthlyUsage(prevYear, prevMonth);
  
  return {
    currentMonth: {
      period: usage.period,
      totalSessions: usage.totalSessions,
      totalParticipantMinutes: usage.totalParticipantMinutes,
      estimatedCost: estimateMonthlyCost(usage.totalParticipantMinutes)
    },
    projection: {
      projectedMinutes: projection.projectedMonthlyUsage,
      projectedCost: projection.projectedCost,
      dailyAverage: projection.dailyAverage
    },
    previousMonth: {
      period: previousUsage.period,
      totalParticipantMinutes: previousUsage.totalParticipantMinutes,
      monthOverMonthChange: (
        (usage.totalParticipantMinutes - previousUsage.totalParticipantMinutes) /
        previousUsage.totalParticipantMinutes * 100
      ).toFixed(1) + '%'
    },
    topSessions: usage.sessions
      .sort((a, b) => b.participantMinutes - a.participantMinutes)
      .slice(0, 10)
  };
}
```

## Best Practices

### Accurate Tracking

1. **Use webhooks for real-time**: More accurate than periodic API polling
2. **Handle reconnections**: Participants may disconnect and rejoin
3. **Account for time zones**: Store all times in UTC
4. **Deduplicate participants**: Same user may rejoin multiple times

### Cost Optimization

1. **Monitor daily usage**: Set up alerts for unusual spikes
2. **Track by use case**: Identify which features consume most minutes
3. **Optimize session duration**: Encourage efficient meetings
4. **Review participant patterns**: Identify inactive participants

### Data Retention

| Data Source | Retention Period |
|-------------|------------------|
| Session Quality API | 30 days |
| Reports API (meetings) | 12 months |
| Reports API (participants) | 1 month |
| Webhook events | Store your own |

## Related Resources

- **Video SDK Session Quality**: https://developers.zoom.us/docs/video-sdk/session-quality/
- **Reports API**: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#tag/Reports
- **Usage reporting guide**: See `usage-reporting-analytics.md`
- **Webhooks reference**: See `webhooks` skill
