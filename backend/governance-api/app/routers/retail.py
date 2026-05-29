from fastapi import APIRouter, HTTPException

from app.data.retail_systems import (
    build_reorder_recommendations,
    get_contract,
    get_customer_context,
    get_identity_subject,
    get_sales_summary,
    list_contracts,
    list_erp_exceptions,
    list_low_stock_items,
    list_shipments,
)
from app.schemas.retail import (
    CustomerSupportContext,
    ErpInvoiceException,
    IdentitySubject,
    LowStockResponse,
    ReorderRecommendationResponse,
    RetailContractResponse,
    RetailSystemId,
    RetailSystemListResponse,
    StoreSalesSummary,
    SupplyChainShipment,
)

router = APIRouter()


@router.get("/systems", response_model=RetailSystemListResponse)
def get_retail_systems() -> RetailSystemListResponse:
    contracts = list_contracts()
    return RetailSystemListResponse(systems=contracts, count=len(contracts))


@router.get("/contracts/{system_id}", response_model=RetailContractResponse)
def get_retail_contract(system_id: RetailSystemId) -> RetailContractResponse:
    contract = get_contract(system_id)

    if contract is None:
        raise HTTPException(status_code=404, detail="Retail system contract not found.")

    return RetailContractResponse(contract=contract)


@router.get("/inventory/low-stock", response_model=LowStockResponse)
def get_low_stock_inventory() -> LowStockResponse:
    items = list_low_stock_items()
    return LowStockResponse(items=items, count=len(items))


@router.get("/inventory/reorder-recommendations", response_model=ReorderRecommendationResponse)
def get_reorder_recommendations() -> ReorderRecommendationResponse:
    recommendations = build_reorder_recommendations()
    return ReorderRecommendationResponse(
        recommendations=recommendations,
        count=len(recommendations),
    )


@router.get("/pos/stores/{store_id}/sales-summary", response_model=StoreSalesSummary)
def get_store_sales_summary(store_id: str) -> StoreSalesSummary:
    summary = get_sales_summary(store_id)

    if summary is None:
        raise HTTPException(status_code=404, detail="Store sales summary not found.")

    return summary


@router.get("/crm/cases/{case_id}/support-context", response_model=CustomerSupportContext)
def get_case_support_context(case_id: str) -> CustomerSupportContext:
    context = get_customer_context(case_id)

    if context is None:
        raise HTTPException(status_code=404, detail="Customer support context not found.")

    return context


@router.get("/erp/invoice-exceptions", response_model=list[ErpInvoiceException])
def get_invoice_exceptions() -> list[ErpInvoiceException]:
    return list_erp_exceptions()


@router.get("/supply-chain/shipments", response_model=list[SupplyChainShipment])
def get_supply_chain_shipments() -> list[SupplyChainShipment]:
    return list_shipments()


@router.get("/identity/subjects/{subject_id}", response_model=IdentitySubject)
def get_subject_access_context(subject_id: str) -> IdentitySubject:
    subject = get_identity_subject(subject_id)

    if subject is None:
        raise HTTPException(status_code=404, detail="Identity subject not found.")

    return subject
