# Zoom Docs API

Authoritative endpoint inventory for Zoom Docs. This file mirrors the official Zoom API Hub OpenAPI document for this product area.

## Canonical Source

- OpenAPI JSON: https://developers.zoom.us/api-hub/zoom-docs/methods/endpoints.json
- Base URL: `https://api.zoom.us/v2`
- Authentication details: [authentication.md](authentication.md)

## Notes

- Endpoint methods and paths below are generated from the official Zoom API Hub `paths` object.
- Scope names are defined per operation and frequently use granular scope names. Check the API Hub operation page for the exact scopes before implementation.
- Use this file for endpoint discovery and inventory. Use `../examples/` for orchestration patterns, not as the canonical source of path names.

## Coverage

| Metric | Value |
|--------|-------|
| Endpoint operations | 16 |
| Path templates | 11 |
| Tags | 6 |

## Tag Index

| Tag | Operations |
|-----|------------|
| Collaborator | 4 |
| Export | 2 |
| File Management | 5 |
| File Uploads | 1 |
| General Access | 2 |
| Import | 2 |

## Endpoints by Tag

### Collaborator

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/docs/files/{fileId}/collaborators` | List collaborators of a file | `ListCollaborators` |
| POST | `/docs/files/{fileId}/collaborators` | Add collaborators for a file | `AddCollaborators` |
| DELETE | `/docs/files/{fileId}/collaborators/{collaboratorId}` | Remove a collaborator from a file | `RemoveACollaborator` |
| PATCH | `/docs/files/{fileId}/collaborators/{collaboratorId}` | Modify a collaborator’s role on a file | `ModifyCollaboratorRole` |

### Export

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| POST | `/docs/exports` | Create a file export | `Createafileexport` |
| GET | `/docs/exports/{exportId}/status` | Get file export status | `Getfileexportstatus` |

### File Management

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| POST | `/docs/files` | Create a new file | `CreateDoc` |
| DELETE | `/docs/files/{fileId}` | Delete a file | `DeleteFile` |
| GET | `/docs/files/{fileId}` | Get metadata of a file | `QueryFileMetadata` |
| PATCH | `/docs/files/{fileId}` | Modify metadata of a file | `ModifyMetadata` |
| GET | `/docs/files/{fileId}/children` | List all children of a file | `ListAllChildren` |

### File Uploads

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| POST | `/docs/file_uploads` | Create file upload for docs import or attachments | `Uploadfilefordocsimportorattachments` |

### General Access

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/docs/files/{fileId}/general_access_setting` | Get the general access setting of a file | `GetFileGeneralAccess` |
| PATCH | `/docs/files/{fileId}/general_access_setting` | Modify the general access setting of a file | `ModifyFileGeneralAccess` |

### Import

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| POST | `/docs/imports` | Create a new file by import | `Createanewfilebyimport` |
| GET | `/docs/imports/{importId}/status` | Get file import status | `Getdocsfileimportstatus` |
