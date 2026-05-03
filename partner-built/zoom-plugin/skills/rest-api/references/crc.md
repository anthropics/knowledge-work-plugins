# Zoom Conference Room Connector API

Authoritative endpoint inventory for Conference Room Connector. This file mirrors the official Zoom API Hub OpenAPI document for this product area.

## Canonical Source

- OpenAPI JSON: https://developers.zoom.us/api-hub/crc/methods/endpoints.json
- Base URL: `https://api.zoom.us/v2`
- Authentication details: [authentication.md](authentication.md)

## Notes

- Endpoint methods and paths below are generated from the official Zoom API Hub `paths` object.
- Scope names are defined per operation and frequently use granular scope names. Check the API Hub operation page for the exact scopes before implementation.
- Use this file for endpoint discovery and inventory. Use `../examples/` for orchestration patterns, not as the canonical source of path names.

## Coverage

| Metric | Value |
|--------|-------|
| Endpoint operations | 20 |
| Path templates | 9 |
| Tags | 5 |

## Tag Index

| Tag | Operations |
|-----|------------|
| Account | 2 |
| Api Connector | 7 |
| Cisco/Polycom Rooms | 5 |
| Participant | 1 |
| Room Template | 5 |

## Endpoints by Tag

### Account

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/crc/managed_rooms/account_setting` | Get Cisco/Polycom Room Account Setting | `getCiscoPolycomRoomAccountSetting` |
| PATCH | `/crc/managed_rooms/account_setting` | Update Cisco/Polycom Room Account Setting | `UpdateCiscoPolycomRoomAccountSetting` |

### Api Connector

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/crc/api_connectors` | List API Connectors | `GetListAPIConnectors` |
| POST | `/crc/api_connectors` | Create an API Connector | `CreateAPIConnector` |
| DELETE | `/crc/api_connectors/{connectorId}` | Delete an API Connector | `DeleteAPIConnector` |
| GET | `/crc/api_connectors/{connectorId}` | Get an API Connector | `GetAPIConnector` |
| PATCH | `/crc/api_connectors/{connectorId}` | Update an API Connector | `UpdateAPIConnector` |
| GET | `/crc/api_connectors/{connectorId}/private_key` | Get an API Connector's private key | `GetanAPIConnector'sprivatekey` |
| PATCH | `/crc/api_connectors/{connectorId}/private_key` | Update an API Connector's private key | `UpdateAPIConnectorPrivateKey` |

### Cisco/Polycom Rooms

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/crc/managed_rooms` | List Managed Rooms | `ListManagedRooms` |
| POST | `/crc/managed_rooms` | Create a Managed Room | `CreateaManagedRoom` |
| DELETE | `/crc/managed_rooms/{deviceId}` | Delete a managed room | `Deleteamanagedroom` |
| GET | `/crc/managed_rooms/{deviceId}` | Get a Managed Room | `GetaManagedRoom` |
| PATCH | `/crc/managed_rooms/{deviceId}` | Update a Managed Room | `UpdateaManagedRoom` |

### Participant

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/crc/participant_identifier_code` | Get participant identifier code | `get_participant_identifier_code` |

### Room Template

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/crc/room_templates` | List Room Templates | `ListRoomTemplates` |
| POST | `/crc/room_templates` | Create a Room Template | `CreateaRoomTemplate` |
| DELETE | `/crc/room_templates/{templateId}` | Delete a room template | `Deletearoomtemplate` |
| GET | `/crc/room_templates/{templateId}` | Get a Room Template | `GetaRoomTemplate` |
| PATCH | `/crc/room_templates/{templateId}` | Update a Room Template | `UpdateaRoomTemplate` |
