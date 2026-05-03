# Customer Support Co-Browsing

Enable real-time collaborative browsing between support agents and customers for efficient issue resolution and form completion assistance.

## Use Case Overview

**Problem**: Customers struggle to describe issues or complete complex forms, leading to long support calls and high frustration.

**Solution**: Implement Zoom Cobrowse SDK to allow support agents to view and assist customers' browsers in real-time, with privacy controls for sensitive data.

**Related Skills**: 
- [Zoom Cobrowse SDK](../../cobrowse-sdk/SKILL.md)
- [Contact Center Integration](contact-center-integration.md)

## Architecture

```
┌──────────────────────┐         ┌──────────────────────┐
│  Customer Browser    │         │  Support Agent       │
│  • View form/page    │◄───────►│  • View customer     │
│  • Share PIN         │  Sync   │  • Provide guidance  │
│  • Get assistance    │         │  • Draw annotations  │
└──────────────────────┘         └──────────────────────┘
           │                                │
           └────────────┬───────────────────┘
                        ▼
              ┌──────────────────────┐
              │  Your Auth Server    │
              │  • Generate JWTs     │
              │  • Log sessions      │
              │  • Track agents      │
              └──────────────────────┘
```

## Implementation Steps

### 1. Set Up Authentication Server

```javascript
// server.js - JWT token generation
const express = require('express');
const { KJUR } = require('jsrsasign');

app.post('/cobrowse-token', (req, res) => {
  const { role, userId, userName, caseId } = req.body;
  
  const iat = Math.floor(Date.now() / 1000);
  const exp = iat + 60 * 60 * 2; // 2 hours
  
  const payload = {
    app_key: process.env.ZOOM_SDK_KEY,
    role_type: role,  // 1 = customer, 2 = agent
    user_id: userId,
    user_name: userName,
    iat,
    exp
  };
  
  const token = KJUR.jws.JWS.sign('HS256', 
    JSON.stringify({ alg: 'HS256', typ: 'JWT' }), 
    JSON.stringify(payload), 
    process.env.ZOOM_SDK_SECRET
  );
  
  // Log session for tracking
  logCobrowseSession(caseId, userId, role);
  
  res.json({ token });
});
```

### 2. Integrate Customer Support Page

```html
<!-- support.html -->
<!DOCTYPE html>
<html>
<head>
  <script type="module">
    const ZOOM_SDK_KEY = 'YOUR_SDK_KEY';
    
    // Load Cobrowse SDK
    (function(r, a, b, f, c, d) {
      r[f] = r[f] || { init: function() { r.ZoomCobrowseSDKInitArgs = arguments }};
      var fragment = a.createDocumentFragment();
      function loadJs(url) {
        c = a.createElement(b);
        d = a.getElementsByTagName(b)[0];
        c["async"] = false;
        c.src = url;
        fragment.appendChild(c);
      }
      loadJs(`https://us01-zcb.zoom.us/static/resource/sdk/${ZOOM_SDK_KEY}/js/2.13.2`);
      d.parentNode.insertBefore(fragment, d);
    })(window, document, "script", "ZoomCobrowseSDK");
  </script>
</head>
<body>
  <div id="support-widget">
    <button id="start-cobrowse">Get Support Help</button>
    <div id="pin-display" style="display:none;">
      <p>Share this PIN with your support agent:</p>
      <div id="pin-code"></div>
    </div>
  </div>
  
  <!-- Customer form with sensitive fields -->
  <form id="customer-form">
    <input name="name" placeholder="Full Name">
    <input name="email" placeholder="Email">
    <input name="ssn" class="pii-mask" placeholder="SSN">
    <input name="account" class="pii-mask" placeholder="Account Number">
  </form>
  
  <script>
    let sessionRef = null;
    
    const settings = {
      allowAgentAnnotation: true,    // Agent can highlight fields
      allowCustomerAnnotation: false, // Customer can't annotate
      piiMask: {
        maskType: "custom_input",
        maskCssSelectors: ".pii-mask"  // Hide sensitive fields from agent
      }
    };
    
    ZoomCobrowseSDK.init(settings, function({ success, session, error }) {
      if (success) {
        sessionRef = session;
        
        session.on("pincode_updated", (payload) => {
          document.getElementById("pin-code").innerText = payload.pincode;
          document.getElementById("pin-display").style.display = "block";
        });
        
        session.on("agent_joined", () => {
          console.log("Support agent connected");
          showNotification("Agent is now viewing your screen");
        });
      }
    });
    
    document.getElementById("start-cobrowse").addEventListener("click", async () => {
      const caseId = getCurrentCaseId();
      
      const response = await fetch("/cobrowse-token", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          role: 1,
          userId: "customer_" + Date.now(),
          userName: "Customer",
          caseId: caseId
        })
      });
      
      const { token } = await response.json();
      sessionRef.start({ sdkToken: token });
    });
  </script>
</body>
</html>
```

### 3. Agent Portal Integration

```html
<!-- agent-portal.html -->
<!DOCTYPE html>
<html>
<head>
  <title>Support Agent - Co-Browse</title>
</head>
<body>
  <div class="agent-dashboard">
    <div class="case-info">
      <h2>Case #<span id="case-id"></span></h2>
      <p>Customer: <span id="customer-name"></span></p>
    </div>
    
    <iframe 
      id="cobrowse-frame"
      width="1024" 
      height="768"
      allow="autoplay *; camera *; microphone *; display-capture *; geolocation *;"
    ></iframe>
  </div>
  
  <script>
    async function loadCobrowseSession(caseId) {
      const response = await fetch("/cobrowse-token", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          role: 2,
          userId: "agent_" + Date.now(),
          userName: getAgentName(),
          caseId: caseId
        })
      });
      
      const { token } = await response.json();
      
      const iframe = document.getElementById("cobrowse-frame");
      iframe.src = `https://us01-zcb.zoom.us/sdkapi/zcb/frame-templates/desk?access_token=${token}`;
    }
    
    // Load cobrowse when case requires it
    const caseId = getCurrentCaseId();
    loadCobrowseSession(caseId);
  </script>
</body>
</html>
```

## Key Features

### Privacy Masking

Automatically hide sensitive customer data:

```javascript
const settings = {
  piiMask: {
    maskType: "custom_input",
    maskCssSelectors: ".pii-mask, .sensitive, [data-private]",
    maskHTMLAttributes: "data-private=true"
  }
};
```

**What gets masked:**
- Social Security Numbers
- Credit Card Numbers
- Bank Account Numbers
- Passwords
- Any field with `.pii-mask` class

### Annotation Tools

Agents can guide customers visually:
- **Pen tool**: Highlight form fields
- **Rectangle**: Circle important sections
- **Pointer**: Direct attention to specific elements

### Session Management

Track and log all cobrowse sessions:

```javascript
function logCobrowseSession(caseId, userId, role) {
  const log = {
    caseId,
    userId,
    role: role === 1 ? 'customer' : 'agent',
    timestamp: new Date(),
    sessionType: 'cobrowse'
  };
  
  database.sessions.insert(log);
}
```

## Use Case Scenarios

### Scenario 1: Complex Form Assistance

**Context**: Customer struggles with multi-step insurance application

**Flow**:
1. Customer clicks "Get Help" on form page
2. PIN generated and displayed
3. Customer calls support, shares PIN
4. Agent enters PIN, sees customer's form
5. Agent uses annotation to highlight next field
6. Customer fills form with real-time guidance
7. Sensitive fields (SSN, medical info) masked from agent

**Outcome**: Form completed in 5 minutes vs 20 minutes phone call

### Scenario 2: Technical Troubleshooting

**Context**: Customer can't find account settings

**Flow**:
1. Customer initiates cobrowse from help chat
2. Agent joins session
3. Agent uses pointer to show navigation path
4. Customer follows visual guidance
5. Issue resolved in real-time

**Outcome**: No screen sharing software needed, instant resolution

### Scenario 3: Onboarding New Users

**Context**: First-time user needs guided tour

**Flow**:
1. Onboarding specialist starts cobrowse
2. Customer joins via PIN
3. Specialist guides through features
4. Annotations highlight key functions
5. Customer follows along in their browser

**Outcome**: Interactive onboarding, higher completion rate

## Security Considerations

### 1. Privacy Compliance

```javascript
// GDPR/CCPA compliant data handling
const privacySettings = {
  piiMask: {
    maskType: "custom_input",
    maskCssSelectors: ".pii-mask"
  },
  sessionRecording: false,  // Don't record sessions
  dataRetention: "24h"      // Auto-delete session logs
};
```

### 2. Agent Authentication

```javascript
// Verify agent credentials before token generation
async function validateAgent(agentId) {
  const agent = await database.agents.findOne({ id: agentId });
  
  if (!agent || !agent.cobrowseEnabled) {
    throw new Error("Agent not authorized for cobrowse");
  }
  
  return agent;
}
```

### 3. Session Limits

- Max 5 agents per customer session
- 2-hour token expiration
- Automatic session end on inactivity (10 minutes)
- HTTPS required for all connections

## Metrics and Analytics

Track cobrowse effectiveness:

```javascript
// Track session metrics
const metrics = {
  sessionDuration: calculateDuration(startTime, endTime),
  issueResolved: true,
  customerSatisfaction: 5,
  formFieldsCompleted: 12,
  annotationsUsed: 8
};

analytics.track('cobrowse_session_completed', metrics);
```

**Key Metrics**:
- Average session duration
- Issue resolution rate
- Customer satisfaction (CSAT)
- Time saved vs phone support
- Conversion rate (form completion)

## Integration with Existing Systems

### Salesforce Integration

```javascript
// Log cobrowse session to Salesforce case
async function logToSalesforce(caseId, sessionData) {
  await salesforce.cases.update(caseId, {
    Cobrowse_Session_Date__c: new Date(),
    Cobrowse_PIN__c: sessionData.pin,
    Agent_Id__c: sessionData.agentId,
    Session_Duration__c: sessionData.duration
  });
}
```

### Zendesk Integration

```javascript
// Add cobrowse note to Zendesk ticket
await zendesk.tickets.addComment(ticketId, {
  body: `Cobrowse session completed. PIN: ${pin}. Duration: ${duration}`,
  public: false
});
```

## Best Practices

1. **Clear Privacy Disclosure**
   - Inform customer what agent can see
   - Display "Agent is viewing your screen" banner

2. **Selective Masking**
   - Mask by default, unmask if needed
   - Use `.pii-mask` class liberally

3. **Session Logging**
   - Track all sessions for compliance
   - Log agent actions for quality assurance

4. **Agent Training**
   - Train agents on privacy controls
   - Establish annotation best practices

5. **Customer Consent**
   - Get explicit consent before starting
   - Allow customer to end session anytime

## Cost Considerations

**Zoom SDK Pricing**:
- Pay per cobrowse minute
- SDK Universal Credits required
- See [Zoom pricing](https://zoom.us/pricing/sdk)

**Estimated Costs**:
- 100 sessions/day × 10 min avg = 1,000 minutes/day
- ~$30-50/day depending on plan

## Related Resources

- [Zoom Cobrowse SDK Documentation](../../cobrowse-sdk/SKILL.md)
- [Get Started Guide](../../cobrowse-sdk/get-started.md)
- [Session Events Reference](../../cobrowse-sdk/references/session-events.md)
- [Privacy Masking Example](../../cobrowse-sdk/examples/privacy-masking.md)
- [Contact Center Integration](contact-center-integration.md)

## Common Issues

**Issue**: Customer can't see PIN  
**Solution**: Check `pincode_updated` event handler is properly attached

**Issue**: Agent sees sensitive data  
**Solution**: Verify `.pii-mask` class applied to sensitive fields

**Issue**: Session disconnects on page refresh  
**Solution**: Implement auto-reconnection pattern (see [Auto-Reconnection](../../cobrowse-sdk/examples/auto-reconnection.md))

## Next Steps

1. Review [Get Started Guide](../../cobrowse-sdk/get-started.md)
2. Set up auth server using [JWT Authentication](../../cobrowse-sdk/concepts/jwt-authentication.md)
3. Integrate customer page with [Customer Integration](../../cobrowse-sdk/examples/customer-integration.md)
4. Deploy agent portal with [Agent Integration](../../cobrowse-sdk/examples/agent-integration.md)
5. Test privacy masking with [Privacy Masking Example](../../cobrowse-sdk/examples/privacy-masking.md)
