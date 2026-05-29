from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class RetailSystemId(str, Enum):
    pos = "pos"
    inventory = "inventory"
    erp = "erp"
    crm = "crm"
    supply_chain = "supply-chain"
    identity = "identity"


class DataSensitivity(str, Enum):
    public = "Public"
    internal = "Internal"
    confidential = "Confidential"
    pii = "PII"
    payment = "Payment"


class AuthRequirement(str, Enum):
    service_account = "Service Account"
    oauth = "OAuth"
    iam = "IAM"
    mfa = "MFA"
    privileged_access = "Privileged Access"


class RetailSystemContract(BaseModel):
    system_id: RetailSystemId
    name: str
    owner_team: str
    description: str
    data_sensitivity: DataSensitivity
    auth_requirements: List[AuthRequirement]
    logging_required: bool
    sla: str
    allowed_operations: List[str]
    forbidden_operations: List[str]
    ai_usage_notes: str
    risk_classification: str


class StoreSalesSummary(BaseModel):
    store_id: str
    business_date: str
    gross_sales_usd: float
    transaction_count: int
    average_basket_usd: float
    top_categories: List[str]
    data_contract: str = "data-contracts/pos-api.yaml"


class InventoryItem(BaseModel):
    sku: str
    store_id: str
    item_name: str
    on_hand_units: int
    reorder_point: int
    average_daily_demand: float
    supplier_id: str
    risk_signal: str
    data_contract: str = "data-contracts/inventory-api.yaml"


class ReorderRecommendation(BaseModel):
    sku: str
    store_id: str
    item_name: str
    recommended_reorder_units: int
    reason: str
    requires_human_approval: bool = True
    forbidden_autonomous_execution: bool = True


class CustomerSupportContext(BaseModel):
    customer_id: str
    case_id: str
    loyalty_tier: str
    recent_case_category: str
    pii_redacted: bool
    support_summary: str
    data_contract: str = "data-contracts/crm-api.yaml"


class ErpInvoiceException(BaseModel):
    invoice_id: str
    supplier_id: str
    exception_type: str
    amount_usd: float
    recommended_action: str
    requires_finance_approval: bool = True
    data_contract: str = "data-contracts/erp-api.yaml"


class IdentitySubject(BaseModel):
    subject_id: str
    role: str
    business_unit: str
    access_level: str
    mfa_required: bool
    allowed_systems: List[RetailSystemId]
    data_contract: str = "data-contracts/identity-api.yaml"


class SupplyChainShipment(BaseModel):
    shipment_id: str
    supplier_id: str
    destination_store_id: str
    status: str
    eta: str
    impacted_skus: List[str]
    risk_signal: Optional[str] = None
    data_contract: str = "data-contracts/supply-chain-api.yaml"


class RetailSystemListResponse(BaseModel):
    systems: List[RetailSystemContract]
    count: int


class RetailContractResponse(BaseModel):
    contract: RetailSystemContract


class LowStockResponse(BaseModel):
    items: List[InventoryItem]
    count: int


class ReorderRecommendationResponse(BaseModel):
    recommendations: List[ReorderRecommendation]
    count: int
