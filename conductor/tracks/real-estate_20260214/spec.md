# Specification: Real Estate NZ Plugin (real-estate)

## Overview
This plugin transforms Claude into a specialist for New Zealand Real Estate Agents, focusing on the workflows of the Ray White network (Lower Hutt baseline). It covers the property lifecycle from prospecting to settlement, focusing on marketing, strategic appraisals, and strict REA/AML compliance.

## User Personas
- **Real Estate Agents (NZ):** Focus on conversion, high-quality marketing, and vendor management.
- **Sales Associates:** Focus on administration, listing drafting, and due diligence prep.

## Functional Requirements
- **Lead & CRM Management:**
    - **Golden Database Tagger:** Life-stage segmentation.
    - Voice-to-Text Cleaner and Hot Lead Detector.
    - Rainy Day Pivot and Vendor Feedback Synthesis.
- **Marketing Suite:** 
    - **Renovation ROI Estimator:** Advising on pre-sale value adds.
    - Trade Me listings, Social Teasers, and Pre-Listing Kits.
    - Suburb Decoder and Auction/Tender Openers.
- **Strategic Appraisal Suite:** 
    - **Market Cycle Adjuster:** Adapting strategy to Boom/Bust cycles.
    - **Investment Yield Calculator:** ROI analysis for investors.
    - Comparable sales analysis and Appraisal Evidence Pack.
- **Due Diligence & Compliance:**
    - **School Zone Future Proofing:** Border zone risk checks.
    - Scrutiny Engine (LIMs/Titles) and REA/AML Auditor.
- **Negotiation & Settlement:**
    - Method of Sale specialization and Multi-offer strategy.
    - Key Handover Checklist.

## Non-Functional Requirements
- **ToV Personalization:** Learning and mimicking the specific agent's brand voice.
- **Standard vs. Lite Modes:** Transactional vs. Strategic workflows.

## Acceptance Criteria
- Commands: `/manage-leads`, `/draft-listing`, `/generate-appraisal`, `/check-compliance`, `/prepare-negotiation`, `/audit-due-diligence`, `/vendor-report`.
- Successful handling of NZ-specific documents (LIM, AML forms, REA disclosures).

## Out of Scope
- Direct trust account management or legal settlement.
- Binding valuations (registered valuer only).
