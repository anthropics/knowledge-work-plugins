---
name: api-spec-generation
description: Generate OpenAPI 3.1 and AsyncAPI 3.0 specification files from DDD specs, implementation contracts, and knowledge graph entities. Produces machine-readable API documentation that developers use with Swagger UI, Postman, Redoc, and code generators.
---

# API Specification Generation

You produce OpenAPI 3.1 and AsyncAPI 3.0 YAML files from the Phase 2
deliverables and knowledge graph. Developers use existing tools — Swagger UI,
Redoc, Postman, AsyncAPI Studio — to browse, validate, and mock the proposed
APIs. No custom viewer needed.

## Output Files

### Per-Domain Specs

In `.magellan/domains/<domain>/deliverables/`:

| File | Format | Use Case |
|------|--------|----------|
| `openapi.yaml` | OpenAPI 3.1 | REST API documentation, Swagger UI, Postman import, SDK generation |
| `asyncapi.yaml` | AsyncAPI 3.0 | Event documentation, message broker configuration |

### Cross-Domain Integration Spec

In `.magellan/domains/_integration/`:

| File | Format | Use Case |
|------|--------|----------|
| `openapi.yaml` | OpenAPI 3.1 | All inter-service REST endpoints aggregated |
| `asyncapi.yaml` | AsyncAPI 3.0 | All published/subscribed events across domains |

## When to Generate

- After Phase 2 contract generation (runs as a pipeline step after rules export)
- On demand when an architect requests API spec regeneration

## Process

### Per-Domain Specs

For each domain discovered via Glob on `.magellan/domains/*/`:

1. Read the DDD spec (`ddd_spec.md`) from the deliverables directory using the
   Read tool — it contains bounded context, aggregates, events, commands.
2. Read the contracts (`contracts.md`) from the deliverables directory — it
   contains API endpoints, event schemas, data models.
3. Use Glob on `.magellan/domains/<domain>/entities/*.json` to discover entities,
   then Read key entities for data model schemas.
4. Use the Read tool to read `.magellan/domains/<domain>/relationships.json` for
   entity relationships (informs data model foreign keys and nested schemas).
5. Use the Read tool to read `.magellan/cross_domain.json` to identify
   integration points with other domains.
6. Generate `openapi.yaml` following the OpenAPI format below. Write immediately.
7. Generate `asyncapi.yaml` following the AsyncAPI format below. Write immediately.
8. Display: "API specs: domain_name (N endpoints, M events)"

### Cross-Domain Integration Spec

After all per-domain specs are generated:

1. Read `.magellan/cross_domain.json` using the Read tool.
2. For each inter-domain relationship, collect the relevant endpoints and events
   from the per-domain specs.
3. Generate `.magellan/domains/_integration/openapi.yaml` aggregating all
   inter-service REST endpoints.
4. Generate `.magellan/domains/_integration/asyncapi.yaml` aggregating all
   cross-domain events with their channels.
5. Display: "Integration specs: N cross-domain endpoints, M cross-domain events"

## OpenAPI 3.1 Format (`openapi.yaml`)

```yaml
openapi: "3.1.0"
info:
  title: Billing Service
  version: "1.0.0"
  description: |
    Manages invoicing, fee calculation, payment processing,
    and settlement for vehicle auction transactions.
    Generated from Magellan KG — billing domain.
  contact:
    name: Magellan Knowledge Graph
  x-generated: "2026-02-23T10:00:00Z"
  x-domain: billing
  x-entity-count: 23

paths:
  /invoices:
    post:
      summary: Create invoice for completed sale
      operationId: createInvoice
      tags: [invoicing]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateInvoiceRequest'
            example:
              saleId: "a1b2c3d4-5678-90ab-cdef-1234567890ab"
              vehicleVin: "1HGCM82633A004352"
              buyerDealerId: "DLR-4521"
              salePrice: 18500.00
      responses:
        '201':
          description: Invoice created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Invoice'
        '400':
          $ref: '#/components/responses/ValidationError'
        '409':
          description: Duplicate invoice for this sale

  /invoices/{invoiceId}/approve:
    post:
      summary: Manager approval for invoices above threshold
      description: |
        Required when invoice amount exceeds $15,000 (BR-FIN-001).
        Source: CBBLKBOOK.cblle:247
      operationId: approveInvoice
      tags: [invoicing, approval]
      parameters:
        - name: invoiceId
          in: path
          required: true
          schema:
            type: string

components:
  schemas:
    Invoice:
      type: object
      required: [invoiceId, saleId, amount, status]
      properties:
        invoiceId:
          type: string
          format: uuid
        saleId:
          type: string
          format: uuid
        amount:
          type: number
          format: decimal
        status:
          type: string
          enum: [draft, pending_approval, approved, paid, reversed]

  responses:
    ValidationError:
      description: Request validation failed
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                type: string
              details:
                type: array
                items:
                  type: object
                  properties:
                    field:
                      type: string
                    message:
                      type: string
```

### OpenAPI Generation Rules

- **Version**: Always OpenAPI 3.1.0
- **Info block**: Include `x-generated` timestamp, `x-domain` name, `x-entity-count`
- **Paths**: Derive from contracts.md API endpoints. Include all HTTP methods,
  parameters, request/response schemas.
- **Tags**: Group endpoints by aggregate or business process from the DDD spec.
- **Components/Schemas**: Derive from KG entities. Map entity properties to JSON
  Schema types. Use `$ref` for shared schemas.
- **Examples**: Synthesize realistic example payloads from KG entity properties.
  Use domain-appropriate values (real-looking VINs, dealer IDs, invoice numbers),
  not placeholder "string" values.
- **Error responses**: Use a consistent error schema across all endpoints:
  400 (validation), 401 (auth), 403 (forbidden), 404 (not found), 409 (conflict).
- **Business rule references**: When an endpoint enforces a business rule, cite
  it in the description (e.g., "Required per BR-FIN-001").
- **Security**: Note auth requirements from contracts.md. Use security schemes
  if specified (JWT Bearer, API key, etc.).

## AsyncAPI 3.0 Format (`asyncapi.yaml`)

```yaml
asyncapi: "3.0.0"
info:
  title: Billing Domain Events
  version: "1.0.0"
  description: |
    Events published and consumed by the billing domain.
    Generated from Magellan KG.
  x-generated: "2026-02-23T10:00:00Z"
  x-domain: billing

channels:
  invoiceCreated:
    address: "billing.invoices.created"
    messages:
      invoiceCreated:
        $ref: '#/components/messages/InvoiceCreated'
  settlementCompleted:
    address: "billing.settlements.completed"
    messages:
      settlementCompleted:
        $ref: '#/components/messages/SettlementCompleted'

operations:
  publishInvoiceCreated:
    action: send
    channel:
      $ref: '#/channels/invoiceCreated'
    summary: Published when a new invoice is generated from a sale
  consumePaymentReceived:
    action: receive
    channel:
      $ref: '#/channels/paymentReceived'
    summary: Consumed when a payment is processed by the payment gateway

components:
  messages:
    InvoiceCreated:
      payload:
        type: object
        required: [invoiceId, saleId, amount, timestamp]
        properties:
          invoiceId:
            type: string
            format: uuid
          saleId:
            type: string
            format: uuid
          amount:
            type: number
          timestamp:
            type: string
            format: date-time
        example:
          invoiceId: "INV-2024-00847"
          saleId: "a1b2c3d4-5678-90ab-cdef-1234567890ab"
          amount: 19275.00
          timestamp: "2024-01-15T14:31:02Z"
```

### AsyncAPI Generation Rules

- **Version**: Always AsyncAPI 3.0.0
- **Channels**: Derive from DDD spec domain events. Use dot-notation addressing
  (`domain.aggregate.event`).
- **Operations**: Separate `send` (publish) and `receive` (subscribe) operations.
- **Messages**: Full payload schemas with typed fields and realistic examples.
- **Cross-domain events**: Note which other domains consume/produce each event
  in the description.
- **Bindings**: Include broker-specific hints if the KG contains infrastructure
  details (Kafka topic config, partition keys, etc.).

## Cross-Domain Integration Spec

The integration specs aggregate inter-service communication:

### `_integration/openapi.yaml`
- Collects all REST endpoints that are called cross-domain
- Groups by calling domain → target domain
- Shows the complete synchronous API surface between services

### `_integration/asyncapi.yaml`
- Collects all events that cross domain boundaries
- Shows publisher → channel → subscriber relationships
- Acts as an event catalog for the entire system

## Critical: Use Built-in Tools for Reading

- ALL KG data reads MUST use Claude's built-in tools:
  - **Discover domains**: Glob on `.magellan/domains/*/`
  - **Read entity details**: Read tool on `.magellan/domains/<domain>/entities/<entity_id>.json`
  - **Read relationships**: Read tool on `.magellan/domains/<domain>/relationships.json`
  - **Read cross-domain edges**: Read tool on `.magellan/cross_domain.json`
  - **Discover entities**: Glob on `.magellan/domains/<domain>/entities/*.json`
  - **Read domain summaries**: Read tool on `.magellan/domains/<domain>/summary.json`
- Read Phase 2 deliverables (`ddd_spec.md`, `contracts.md`) using the Read tool
  (they are generated artifacts in the deliverables directory).
- Write spec files using the Write tool (same pattern as other generated artifacts).
- Create the `_integration/` directory if it doesn't exist.

## What You Do NOT Do

- Do not invent API endpoints. Only generate specs for endpoints described in
  contracts.md or derivable from DDD spec aggregates and commands.
- Do not use placeholder values in examples. Synthesize realistic, domain-appropriate
  values from KG entity properties.
- Do not generate invalid YAML. Ensure proper indentation, quoting of special
  characters, and valid OpenAPI/AsyncAPI structure.
- Do not skip error responses. Every endpoint needs at least 400 and 500 responses.
- Do not merge domains into one spec. Each domain gets its own pair of files.
  The integration specs are separate aggregations.
- Do not omit source traceability. Reference business rules and KG entities in
  endpoint descriptions where relevant.
