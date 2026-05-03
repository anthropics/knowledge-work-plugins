# Zoom Commerce API

Authoritative endpoint inventory for Commerce. This file mirrors the official Zoom API Hub OpenAPI document for this product area.

## Canonical Source

- OpenAPI JSON: https://developers.zoom.us/api-hub/commerce/methods/endpoints.json
- Base URL: `https://api.zoom.us/v2`
- Authentication details: [authentication.md](authentication.md)

## Notes

- Endpoint methods and paths below are generated from the official Zoom API Hub `paths` object.
- Scope names are defined per operation and frequently use granular scope names. Check the API Hub operation page for the exact scopes before implementation.
- Use this file for endpoint discovery and inventory. Use `../examples/` for orchestration patterns, not as the canonical source of path names.

## Coverage

| Metric | Value |
|--------|-------|
| Endpoint operations | 33 |
| Path templates | 31 |
| Tags | 8 |

## Tag Index

| Tag | Operations |
|-----|------------|
| Account Management | 4 |
| Billing | 3 |
| Deal Registration | 5 |
| Order | 4 |
| Platform | 3 |
| Product Catalog | 3 |
| Quote | 6 |
| Subscription | 5 |

## Endpoints by Tag

### Account Management

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| POST | `/commerce/account` | Create an end customer account | `createAccount` |
| POST | `/commerce/account/{accountKey}/contacts` | Add contacts to an existing end customer or your own account. | `addAccountContact` |
| GET | `/commerce/accounts` | Get the list of all accounts associated with a Zoom Partner/Sub-Reseller, by the account type | `getAllAccounts` |
| GET | `/commerce/accounts/{accountKey}` | Get the account details for a Zoom Partner/Subreseller/End Customer | `getAccountDetails` |

### Billing

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/commerce/billing_documents` | Gets all billing documents for a distributor or a reseller | `getAllBillingDocs` |
| GET | `/commerce/billing_documents/{documentNumber}/document` | Gets the PDF document for the billing document ID | `downloadBillingDoc` |
| GET | `/commerce/invoices/{invoiceNumber}` | Get detailed information about a specific invoice for a distributor or a reseller | `getInvoiceDetail` |

### Deal Registration

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/commerce/campaigns` | Retrieves all valid Zoom Campaigns which a deal registration can be associated with. | `getCampaigns` |
| POST | `/commerce/deal_registration` | Creates a new deal registration for a partner | `createDealReg` |
| GET | `/commerce/deal_registrations` | Gets all valid Deal Registrations for a partner | `getAllDealRegs` |
| GET | `/commerce/deal_registrations/{dealRegKey}` | Get details of a deal registration by registration number | `getDealRegDetails` |
| PATCH | `/commerce/deal_registrations/{dealRegKey}` | Updates an existing deal registration | `Updatesanexistingdealregistration` |

### Order

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| POST | `/commerce/order` | Create a subscription order for a Zoom partner | `createOrder` |
| POST | `/commerce/order/preview` | Preview delta order metrics and subscriptions in an order | `createOrderPreview` |
| GET | `/commerce/orders` | Gets all orders for a Zoom partner. | `getAllOrders` |
| GET | `/commerce/orders/{orderReferenceId}` | Get order details by order reference ID | `getOrderDetails` |

### Platform

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| POST | `/commerce/file` | Upload an attachment pdf file in context of a deal registration or quote | `uploadFile` |
| GET | `/commerce/files/{associatedReferenceId}/details` | Gets details of all files associated with a quote or deal registration | `allFileDetails` |
| GET | `/commerce/files/{documentReferenceId}` | Download a file associated with a quote or deal registration. | `downloadFile.` |

### Product Catalog

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| POST | `/commerce/catalog` | Gets Zoom Product Catalog for a Zoom Partner | `getOffers` |
| GET | `/commerce/catalog/{offerId}` | Gets the details for a Zoom product or offer. | `getOfferDetail` |
| GET | `/commerce/pricebooks` | Gets the pricebook in a downloadable file | `downloadPricebook` |

### Quote

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| POST | `/commerce/quote` | Create a subscription quote for a Zoom Partner | `createQuote` |
| POST | `/commerce/quote/preview` | Preview delta quote metrics and subscriptions in a quote | `createQuotePreview` |
| GET | `/commerce/quotes` | Gets all quotes for a Zoom partner | `getAllQuotes` |
| GET | `/commerce/quotes/{quoteReferenceId}` | Get quote details by quote reference ID | `getQuoteDetails` |
| PATCH | `/commerce/quotes/{quoteReferenceId}` | Update a subscription quote for a Zoom partner | `updateQuote` |
| PATCH | `/commerce/quotes/{quoteReferenceId}/fulfillment` | Submits a subscription quote for provisioning | `provisionQuote` |

### Subscription

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/commerce/subscriptions` | Gets paid subscriptions for a Zoom partner. | `getAllSubscriptions` |
| GET | `/commerce/subscriptions/{subscriptionNumber}` | Gets subscription details for a given subscription number | `getSubscriptionDetails` |
| GET | `/commerce/subscriptions/{subscriptionNumber}/versions` | Gets subscription changes/versions for a given subscription number. | `getSubscriptionVersions` |
| GET | `/commerce/trials` | Get trial subscriptions for a Zoom partner | `getAllTrialSubscriptions` |
| GET | `/commerce/trials/{trialReferenceId}` | Get trial details for an end customer by their Zoom account number or the trial ID | `getTrialDetails` |
