from app.schemas.retail import (
    AuthRequirement,
    CustomerSupportContext,
    DataSensitivity,
    ErpInvoiceException,
    IdentitySubject,
    InventoryItem,
    ReorderRecommendation,
    RetailSystemContract,
    RetailSystemId,
    StoreSalesSummary,
    SupplyChainShipment,
)

RETAIL_CONTRACTS = [
    RetailSystemContract(
        system_id=RetailSystemId.pos,
        name="Point of Sale API",
        owner_team="Store Systems",
        description="Provides store-level sales and transaction summaries for AI analytics workflows.",
        data_sensitivity=DataSensitivity.payment,
        auth_requirements=[AuthRequirement.service_account, AuthRequirement.iam],
        logging_required=True,
        sla="99.9% for read-only reporting endpoints",
        allowed_operations=[
            "Read aggregated sales summary",
            "Read product category sales trends",
        ],
        forbidden_operations=[
            "Read raw payment card data",
            "Execute refunds",
            "Modify transactions",
            "Trigger customer-impacting actions",
        ],
        ai_usage_notes="AI may use aggregated sales patterns for analysis. Payment data and transaction mutation are forbidden.",
        risk_classification="Tier 4 if payment data is requested; Tier 2 for aggregated read-only analytics.",
    ),
    RetailSystemContract(
        system_id=RetailSystemId.inventory,
        name="Inventory API",
        owner_team="Inventory Platform",
        description="Provides store and SKU-level inventory signals for replenishment recommendations.",
        data_sensitivity=DataSensitivity.internal,
        auth_requirements=[AuthRequirement.service_account, AuthRequirement.iam],
        logging_required=True,
        sla="99.5% for store inventory reads",
        allowed_operations=[
            "Read on-hand inventory",
            "Read reorder points",
            "Read demand velocity",
        ],
        forbidden_operations=[
            "Autonomously place purchase orders",
            "Override store inventory counts",
            "Modify supplier records",
        ],
        ai_usage_notes="AI may recommend reorder actions. Human approval is required before execution.",
        risk_classification="Tier 2 for recommendation-only workflow; Tier 4 for autonomous ordering.",
    ),
    RetailSystemContract(
        system_id=RetailSystemId.erp,
        name="ERP API",
        owner_team="Enterprise Applications",
        description="Provides finance and supplier operational context for invoice and exception workflows.",
        data_sensitivity=DataSensitivity.confidential,
        auth_requirements=[AuthRequirement.service_account, AuthRequirement.privileged_access],
        logging_required=True,
        sla="99.5% for finance workflow reads",
        allowed_operations=[
            "Read invoice exception summaries",
            "Read supplier reference data",
        ],
        forbidden_operations=[
            "Approve payments",
            "Modify invoices",
            "Change supplier banking data",
        ],
        ai_usage_notes="AI may summarize exceptions and recommend routing. Finance approval remains mandatory.",
        risk_classification="Tier 2 or Tier 3 depending on financial impact and approval workflow.",
    ),
    RetailSystemContract(
        system_id=RetailSystemId.crm,
        name="CRM API",
        owner_team="Customer Platforms",
        description="Provides customer support and loyalty context for governed support-assistant use cases.",
        data_sensitivity=DataSensitivity.pii,
        auth_requirements=[AuthRequirement.oauth, AuthRequirement.iam],
        logging_required=True,
        sla="99.5% for customer support context reads",
        allowed_operations=[
            "Read redacted customer support context",
            "Read loyalty tier",
            "Read case metadata",
        ],
        forbidden_operations=[
            "Expose full PII to prompts",
            "Autonomously contact customers",
            "Change loyalty status",
            "Issue credits without approval",
        ],
        ai_usage_notes="AI may draft support responses using redacted context. Human review is required before customer-facing output.",
        risk_classification="Tier 3 for customer data workflows; Tier 4 if payment data or autonomous action is introduced.",
    ),
    RetailSystemContract(
        system_id=RetailSystemId.supply_chain,
        name="Supply Chain API",
        owner_team="Supply Chain Systems",
        description="Provides shipment, supplier, and distribution signals for replenishment planning.",
        data_sensitivity=DataSensitivity.internal,
        auth_requirements=[AuthRequirement.service_account, AuthRequirement.iam],
        logging_required=True,
        sla="99.0% for shipment status reads",
        allowed_operations=[
            "Read shipment status",
            "Read supplier ETA",
            "Read impacted SKU list",
        ],
        forbidden_operations=[
            "Change carrier routing",
            "Create purchase orders",
            "Cancel shipments",
            "Commit supplier actions without approval",
        ],
        ai_usage_notes="AI may summarize supply-chain risk and recommend next actions. Execution requires policy and human approval.",
        risk_classification="Tier 2 for advisory workflow; Tier 3 or Tier 4 for operational execution.",
    ),
    RetailSystemContract(
        system_id=RetailSystemId.identity,
        name="Identity API",
        owner_team="Identity and Access Management",
        description="Provides role and access context used to enforce governance workflow permissions.",
        data_sensitivity=DataSensitivity.confidential,
        auth_requirements=[AuthRequirement.iam, AuthRequirement.mfa, AuthRequirement.privileged_access],
        logging_required=True,
        sla="99.9% for authorization context reads",
        allowed_operations=[
            "Read role claims",
            "Read business unit assignment",
            "Read allowed system scopes",
        ],
        forbidden_operations=[
            "Issue tokens",
            "Modify roles",
            "Bypass MFA",
            "Grant privileged access",
        ],
        ai_usage_notes="AI may consume role context for workflow routing only. Authorization remains owned by IAM systems.",
        risk_classification="Tier 3 for access-context use; restricted if token issuance or role mutation is requested.",
    ),
]

LOW_STOCK_ITEMS = [
    InventoryItem(
        sku="FD-COF-001",
        store_id="STORE-1042",
        item_name="Family Dollar Ground Coffee 12oz",
        on_hand_units=8,
        reorder_point=25,
        average_daily_demand=6.5,
        supplier_id="SUP-COF-77",
        risk_signal="Stockout risk within 2 days",
    ),
    InventoryItem(
        sku="FD-PPR-014",
        store_id="STORE-1042",
        item_name="Paper Towels 6 Pack",
        on_hand_units=12,
        reorder_point=40,
        average_daily_demand=9.0,
        supplier_id="SUP-HH-18",
        risk_signal="Promotion-driven demand spike",
    ),
    InventoryItem(
        sku="FD-PET-220",
        store_id="STORE-2210",
        item_name="Dog Food 15lb",
        on_hand_units=5,
        reorder_point=18,
        average_daily_demand=4.2,
        supplier_id="SUP-PET-44",
        risk_signal="Supplier ETA delay",
    ),
]

SALES_SUMMARIES = {
    "STORE-1042": StoreSalesSummary(
        store_id="STORE-1042",
        business_date="2026-05-29",
        gross_sales_usd=18240.75,
        transaction_count=973,
        average_basket_usd=18.75,
        top_categories=["Household Essentials", "Grocery", "Pet"],
    ),
    "STORE-2210": StoreSalesSummary(
        store_id="STORE-2210",
        business_date="2026-05-29",
        gross_sales_usd=14388.20,
        transaction_count=801,
        average_basket_usd=17.96,
        top_categories=["Grocery", "Seasonal", "Household Essentials"],
    ),
}

CUSTOMER_CONTEXTS = {
    "CASE-9001": CustomerSupportContext(
        customer_id="CUST-REDACTED-7001",
        case_id="CASE-9001",
        loyalty_tier="Smart Coupons Member",
        recent_case_category="Missing digital coupon",
        pii_redacted=True,
        support_summary="Customer reports that a digital coupon did not apply at checkout. Payment details are not exposed to AI.",
    )
}

ERP_EXCEPTIONS = [
    ErpInvoiceException(
        invoice_id="INV-77821",
        supplier_id="SUP-HH-18",
        exception_type="Quantity mismatch",
        amount_usd=2840.50,
        recommended_action="Route to finance analyst for supplier confirmation.",
    )
]

SHIPMENTS = [
    SupplyChainShipment(
        shipment_id="SHIP-44590",
        supplier_id="SUP-PET-44",
        destination_store_id="STORE-2210",
        status="Delayed",
        eta="2026-06-02",
        impacted_skus=["FD-PET-220"],
        risk_signal="Dog Food 15lb may stock out before delayed shipment arrives.",
    )
]

IDENTITY_SUBJECTS = {
    "user-store-manager": IdentitySubject(
        subject_id="user-store-manager",
        role="Store Manager",
        business_unit="Store Operations",
        access_level="Approver",
        mfa_required=True,
        allowed_systems=[RetailSystemId.inventory, RetailSystemId.supply_chain],
    ),
    "user-ai-platform": IdentitySubject(
        subject_id="user-ai-platform",
        role="AI Platform Engineer",
        business_unit="IT Support",
        access_level="Builder",
        mfa_required=True,
        allowed_systems=[
            RetailSystemId.inventory,
            RetailSystemId.supply_chain,
            RetailSystemId.crm,
            RetailSystemId.erp,
            RetailSystemId.identity,
        ],
    ),
}


def list_contracts() -> list[RetailSystemContract]:
    return RETAIL_CONTRACTS


def get_contract(system_id: RetailSystemId) -> RetailSystemContract | None:
    return next(
        (contract for contract in RETAIL_CONTRACTS if contract.system_id == system_id),
        None,
    )


def list_low_stock_items() -> list[InventoryItem]:
    return LOW_STOCK_ITEMS


def get_sales_summary(store_id: str) -> StoreSalesSummary | None:
    return SALES_SUMMARIES.get(store_id)


def build_reorder_recommendations() -> list[ReorderRecommendation]:
    recommendations: list[ReorderRecommendation] = []

    for item in LOW_STOCK_ITEMS:
        gap_to_reorder_point = max(item.reorder_point - item.on_hand_units, 0)
        recommended_units = int(gap_to_reorder_point + item.average_daily_demand * 5)

        recommendations.append(
            ReorderRecommendation(
                sku=item.sku,
                store_id=item.store_id,
                item_name=item.item_name,
                recommended_reorder_units=recommended_units,
                reason=(
                    f"{item.risk_signal}; on-hand units are below reorder point. "
                    "Recommendation requires store manager approval."
                ),
            )
        )

    return recommendations


def get_customer_context(case_id: str) -> CustomerSupportContext | None:
    return CUSTOMER_CONTEXTS.get(case_id)


def list_erp_exceptions() -> list[ErpInvoiceException]:
    return ERP_EXCEPTIONS


def list_shipments() -> list[SupplyChainShipment]:
    return SHIPMENTS


def get_identity_subject(subject_id: str) -> IdentitySubject | None:
    return IDENTITY_SUBJECTS.get(subject_id)
