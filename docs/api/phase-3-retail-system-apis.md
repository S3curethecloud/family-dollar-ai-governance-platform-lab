# Phase 3 — Retail System APIs & Data Contracts

## Summary

Phase 3 adds mock retail system APIs and data contracts for the Family Dollar AI Governance & Agentic Workflow Platform.

The purpose is to show how AI applications integrate with existing enterprise retail systems through controlled APIs, data contracts, ownership boundaries, logging requirements, and forbidden operations.

## Retail Systems Covered

- POS
- Inventory
- ERP
- CRM
- Supply Chain
- Identity

## Why This Matters

The AI Solutions Architect and Governance Lead role requires defining how AI applications integrate into Family Dollar's existing IT estate. This phase demonstrates that integration design explicitly covers system ownership, API contracts, auth requirements, logging, risk classification, and operational boundaries.

## API Endpoints Added

| Method | Path | Purpose |
|---|---|---|
| GET | `/v1/retail/systems` | List retail system contracts |
| GET | `/v1/retail/contracts/{system_id}` | Get one system contract |
| GET | `/v1/retail/inventory/low-stock` | Return low-stock mock inventory |
| GET | `/v1/retail/inventory/reorder-recommendations` | Return approval-gated reorder recommendations |
| GET | `/v1/retail/pos/stores/{store_id}/sales-summary` | Return aggregated sales summary |
| GET | `/v1/retail/crm/cases/{case_id}/support-context` | Return redacted customer support context |
| GET | `/v1/retail/erp/invoice-exceptions` | Return ERP invoice exception examples |
| GET | `/v1/retail/supply-chain/shipments` | Return supply-chain shipment examples |
| GET | `/v1/retail/identity/subjects/{subject_id}` | Return identity and role context |

## Data Contracts Added

- `data-contracts/pos-api.yaml`
- `data-contracts/inventory-api.yaml`
- `data-contracts/erp-api.yaml`
- `data-contracts/crm-api.yaml`
- `data-contracts/supply-chain-api.yaml`
- `data-contracts/identity-api.yaml`

## Key Governance Boundaries

- AI may read governed context only through approved APIs.
- AI may recommend but not execute operational actions.
- Payment data is restricted.
- CRM context must be redacted before AI use.
- Inventory reorder recommendations require human approval.
- Identity APIs provide authorization context only; they do not issue tokens or mutate roles.
- ERP workflows may summarize and recommend routing but cannot approve payments.
- Supply-chain workflows may summarize risk but cannot cancel shipments or commit supplier actions.

## Demo Talk Track

"After establishing the intake portal and risk-tiering backend, I added retail system APIs and data contracts. This shows how I would integrate AI applications into Family Dollar's existing IT estate without creating shadow integrations. Each system has an owner, auth requirement, logging requirement, allowed operations, forbidden operations, data sensitivity, SLA, and AI usage boundary. This is how I would partner with platform, infrastructure, data, application, and security teams before scaling AI workflows."

## Likely Interview Questions

1. How would you integrate an AI application with POS, inventory, ERP, CRM, and supply-chain systems?
2. What belongs in an API data contract?
3. How would you prevent AI from directly mutating enterprise systems?
4. How would you handle payment data in an AI workflow?
5. How would CRM data be redacted before AI use?
6. How would identity context be used without letting AI authorize users?
7. How would you define system ownership and SLA boundaries?
8. How would these contracts support auditability?
9. How would this scale from mock APIs to real enterprise integrations?
10. How would you use these APIs in an agentic inventory workflow?
