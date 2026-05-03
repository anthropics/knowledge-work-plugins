# Zoom Tasks API

Authoritative endpoint inventory for Tasks. This file mirrors the official Zoom API Hub OpenAPI document for this product area.

## Canonical Source

- OpenAPI JSON: https://developers.zoom.us/api-hub/tasks/methods/endpoints.json
- Base URL: `https://api.zoom.us/v2`
- Authentication details: [authentication.md](authentication.md)

## Notes

- Endpoint methods and paths below are generated from the official Zoom API Hub `paths` object.
- Scope names are defined per operation and frequently use granular scope names. Check the API Hub operation page for the exact scopes before implementation.
- Use this file for endpoint discovery and inventory. Use `../examples/` for orchestration patterns, not as the canonical source of path names.

## Coverage

| Metric | Value |
|--------|-------|
| Endpoint operations | 14 |
| Path templates | 8 |
| Tags | 4 |

## Tag Index

| Tag | Operations |
|-----|------------|
| Assignee | 3 |
| Collaborator | 3 |
| Comment | 3 |
| Tasks | 5 |

## Endpoints by Tag

### Assignee

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/tasks/items/{taskId}/assignees` | Get assignees of a task | `GetAssigneesOfATask` |
| POST | `/tasks/items/{taskId}/assignees` | Add assignees to a task | `addTasksAssignees` |
| DELETE | `/tasks/items/{taskId}/assignees/{userId}` | Remove Assignee from task | `removeTaskAssignee` |

### Collaborator

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/tasks/items/{taskId}/collaborators` | Get collaborators of a task | `Getcollaboratorsofatask` |
| POST | `/tasks/items/{taskId}/collaborators` | Add collaborators to a task | `addTasksCollaborators` |
| DELETE | `/tasks/items/{taskId}/collaborators/{userId}` | Remove collaborator from task | `removeTaskCollaborator` |

### Comment

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/tasks/items/{taskId}/comments` | Get a task's comments | `GetAV1TasksComment` |
| POST | `/tasks/items/{taskId}/comments` | Add a comment to task | `addComment` |
| DELETE | `/tasks/items/{taskId}/comments/{commentId}` | Delete a task's comment | `DeleteTaskComment` |

### Tasks

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/tasks/items` | List tasks | `getMyTasks` |
| POST | `/tasks/items` | Create a new task | `createTask` |
| DELETE | `/tasks/items/{taskId}` | Delete a task | `deleteTask` |
| GET | `/tasks/items/{taskId}` | Get task details | `getTaskDetail` |
| PATCH | `/tasks/items/{taskId}` | Update task fields | `updateTask` |
