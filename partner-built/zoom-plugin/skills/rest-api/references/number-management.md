# Zoom Number Management API

Authoritative endpoint inventory for Number Management. This file mirrors the official Zoom API Hub OpenAPI document for this product area.

## Canonical Source

- OpenAPI JSON: https://developers.zoom.us/api-hub/number-management/methods/endpoints.json
- Base URL: `https://api.zoom.us/v2`
- Authentication details: [authentication.md](authentication.md)

## Notes

- Endpoint methods and paths below are generated from the official Zoom API Hub `paths` object.
- Scope names are defined per operation and frequently use granular scope names. Check the API Hub operation page for the exact scopes before implementation.
- Use this file for endpoint discovery and inventory. Use `../examples/` for orchestration patterns, not as the canonical source of path names.

## Coverage

| Metric | Value |
|--------|-------|
| Endpoint operations | 28 |
| Path templates | 17 |
| Tags | 6 |

## Tag Index

| Tag | Operations |
|-----|------------|
| Cloud Peering Provider Exchange | 5 |
| Phone Numbers | 6 |
| Phone Plan | 1 |
| Setting | 4 |
| SMS Campaigns | 4 |
| SMS Consent | 8 |

## Endpoints by Tag

### Cloud Peering Provider Exchange

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/number_management/carrier/peering_numbers` | List peering phone numbers for provider | `Listpeeringphonenumbersforprovider` |
| DELETE | `/number_management/peering_numbers` | Remove peering phone numbers | `deletePeeringPhoneNumbers` |
| GET | `/number_management/peering_numbers` | List peering phone numbers | `listPeeringPhoneNumbers` |
| PATCH | `/number_management/peering_numbers` | Update peering phone numbers | `updatePeeringPhoneNumbers` |
| POST | `/number_management/peering_numbers` | Add peering phone numbers | `addPeeringPhoneNumbers` |

### Phone Numbers

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| PATCH | `/number_management/allocation` | Allocate/Unallocate phone numbers | `AllocateNumber` |
| POST | `/number_management/byoc_numbers` | Add BYOC phone numbers | `AddBYOCPhoneNumber` |
| DELETE | `/number_management/numbers` | Delete phone numbers | `DeleteNumbers` |
| GET | `/number_management/numbers` | List phone numbers | `listPhoneNumbers` |
| GET | `/number_management/numbers/{phoneNumberId}` | Get a phone number | `getPhoneNumber` |
| PATCH | `/number_management/numbers/{phoneNumberId}` | Update a phone number | `updatePhoneNumberDetail` |

### Phone Plan

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/number_management/plan` | List phone number plan information | `Listphonenumberplaninformation` |

### Setting

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/number_management/ported_numbers/orders` | List ported numbers | `Listportednumbers` |
| GET | `/number_management/ported_numbers/orders/{orderId}` | Get ported numbers details | `Getportednumbersdetails` |
| GET | `/number_management/sip_groups` | List SIP groups | `ListSIPgroups` |
| GET | `/number_management/sip_trunks` | List BYOC SIP trunks | `ListBYOCSIPtrunks` |

### SMS Campaigns

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/number_management/sms_campaigns` | List SMS campaigns | `listAccountSMSCampaigns` |
| GET | `/number_management/sms_campaigns/{smsCampaignId}` | Get an SMS campaign | `GetSMSCampaign` |
| DELETE | `/number_management/sms_campaigns/{smsCampaignId}/phone_numbers` | Unassign phone number from SMS campaign | `unassignCampaignPhoneNumber` |
| POST | `/number_management/sms_campaigns/{smsCampaignId}/phone_numbers` | Assign a phone number to SMS campaign | `assignCampaignPhoneNumbers` |

### SMS Consent

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| DELETE | `/number_management/sms_consent` | Delete SMS consent policies | `DeleteSMSConsents` |
| GET | `/number_management/sms_consent` | List SMS consent policies | `ListSMSConsents` |
| POST | `/number_management/sms_consent` | Create an SMS consent policy | `CreateSMSConsent` |
| GET | `/number_management/sms_consent/{consentId}` | Get an SMS consent policy | `GetSMSConsent` |
| PATCH | `/number_management/sms_consent/{consentId}` | Update an SMS consent policy | `UpdateSMSConsent` |
| DELETE | `/number_management/sms_consent/{consentId}/phone_numbers` | Unassign phone numbers from SMS consent policy | `UnassignPhoneNumbersFromConsent` |
| GET | `/number_management/sms_consent/{consentId}/phone_numbers` | List phone numbers assigned to SMS consent policy | `ListConsentPhoneNumbers` |
| POST | `/number_management/sms_consent/{consentId}/phone_numbers` | Assign phone numbers to SMS consent policy | `AssignPhoneNumbersToConsent` |
