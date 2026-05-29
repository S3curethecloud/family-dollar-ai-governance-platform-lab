from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class BusinessUnit(str, Enum):
    store_operations = "Store Operations"
    customer_support = "Customer Support"
    finance = "Finance"
    marketing = "Marketing"
    supply_chain = "Supply Chain"
    it_support = "IT Support"
    merchandising = "Merchandising"


class RetailSystem(str, Enum):
    pos = "POS"
    inventory = "Inventory"
    erp = "ERP"
    crm = "CRM"
    supply_chain = "Supply Chain"
    identity = "Identity"
    itsm = "ITSM"


class DataSensitivity(str, Enum):
    public = "Public"
    internal = "Internal"
    confidential = "Confidential"
    pii = "PII"
    payment = "Payment"


class OperationalImpact(str, Enum):
    internal_productivity = "Internal productivity"
    back_office = "Back-office operations"
    store_level = "Store-level operations"
    customer_facing = "Customer-facing support"
    supply_chain = "Supply-chain operations"
    enterprise_critical = "Enterprise-critical operations"


class ModelType(str, Enum):
    rag = "RAG assistant"
    agentic = "Agentic workflow with retrieval"
    document_intelligence = "Document intelligence"
    forecasting = "Forecasting model"
    personalization = "Generative AI personalization"
    classification = "Classification model"


class AutonomousActionLevel(str, Enum):
    summarize_only = "Summarize only"
    recommend_only = "Recommend only"
    draft_response = "Draft response"
    autonomous_action = "Autonomous action"


class RiskTier(str, Enum):
    tier_1 = "Tier 1"
    tier_2 = "Tier 2"
    tier_3 = "Tier 3"
    tier_4 = "Tier 4"


class GovernanceStatus(str, Enum):
    architecture_review = "Architecture Review"
    governance_review = "Governance Review"
    approved_for_prototype = "Approved for Prototype"
    restricted_review = "Restricted / Executive Review"


class IntakeRequestCreate(BaseModel):
    business_unit: BusinessUnit
    requester: str = Field(..., min_length=2, max_length=120)
    use_case: str = Field(..., min_length=8, max_length=500)
    retail_system: RetailSystem
    data_sensitivity: DataSensitivity
    customer_data: bool = False
    payment_data: bool = False
    operational_impact: OperationalImpact
    expected_business_value: str = Field(..., min_length=8, max_length=600)
    model_type: ModelType
    autonomous_action_level: AutonomousActionLevel
    human_approval_required: bool = True
    dependencies: List[str] = Field(default_factory=list)
    target_release_window: str = Field(default="Q3 pilot", max_length=120)


class RiskEvaluation(BaseModel):
    risk_tier: RiskTier
    risk_score: int
    human_approval_required: bool
    governance_status: GovernanceStatus
    owner_team: str
    required_reviews: List[str]
    blocked_reasons: List[str]
    risk_rationale: List[str]
    recommended_next_step: str


class IntakeRequestRecord(IntakeRequestCreate):
    request_id: str
    evaluation: RiskEvaluation
    prompt_version: str = "intake-risk-v0.2"
    model_version: str = "rules-engine-v0.2"
    environment: str = "demo"
    created_by: str = "governance-api"


class IntakeRequestResponse(BaseModel):
    request: IntakeRequestRecord


class IntakeRequestListResponse(BaseModel):
    requests: List[IntakeRequestRecord]
    count: int


class RiskTierDefinition(BaseModel):
    tier: RiskTier
    label: str
    description: str
    examples: List[str]
    required_controls: List[str]


class GovernanceDashboard(BaseModel):
    total_requests: int
    tier_1_requests: int
    tier_2_requests: int
    tier_3_requests: int
    tier_4_requests: int
    high_risk_requests: int
    restricted_requests: int
    requests_requiring_human_approval: int
    blocked_dependency_count: int
    portfolio_risk_posture: str
