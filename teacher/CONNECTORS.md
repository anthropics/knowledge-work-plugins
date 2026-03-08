# Teacher Plugin Connectors

This plugin connects to educational tools to help teachers plan lessons, create assessments, provide feedback, and communicate with families.

## Available Connectors

### Learning Management Systems

| Connector | Purpose | What You Can Do |
|-----------|---------|-----------------|
| **Google Classroom** | Class management | Create assignments, post announcements, grade work |
| **Canvas** | Course management | Create modules, quizzes, gradebook integration |
| **Moodle** | Course platform | Add resources, create activities, grade |

### Productivity & Communication

| Connector | Purpose | What You Can Do |
|-----------|---------|-----------------|
| **Google Drive** | File storage | Access lesson materials, student work |
| **Gmail** | Email | Communicate with students and families |
| **Google Calendar** | Scheduling | Plan lessons, set reminders, share schedules |
| **Notion** | Organization | Manage lesson plans, student data |
| **Slack** | Team communication | Collaborate with colleagues |

## Setup Instructions

### Google Suite (Classroom, Drive, Gmail, Calendar)

1. Sign in to your Google account
2. Visit [Google Cloud Console](https://console.cloud.google.com/)
3. Create a new project or select existing one
4. Enable the following APIs:
   - Google Classroom API
   - Gmail API
   - Google Drive API
   - Google Calendar API
5. Create OAuth credentials
6. Add redirect URIs as prompted

### Canvas

1. Sign in to Canvas as an administrator
2. Go to Settings > Developer Keys
3. Click + Developer Key
4. Choose "LTI" or "API" key type
5. Fill in required fields
6. Copy API keys and configure

### Moodle

1. Sign in as administrator
2. Go to Site Administration > Plugins > Web Services > Mobile
3. Enable "Mobile service"
4. Create a service and add functions
5. Create a token for your user
6. Configure with your site URL and token

## Connector Best Practices

### For All Tools
- Review privacy and security settings
- Use appropriate permission levels
- Test connections before class use
- Keep credentials secure

### Data Privacy
- Follow FERPA guidelines
- Obtain necessary consents
- Limit data sharing to what's essential
- Review tool privacy policies

### Troubleshooting

**Connection Issues**
- Check API quotas and limits
- Verify credentials are current
- Review error messages carefully
- Test individual API endpoints

**Permission Errors**
- Review OAuth scopes requested
- Check user permission levels
- Re-authorize if needed
- Contact administrator for help