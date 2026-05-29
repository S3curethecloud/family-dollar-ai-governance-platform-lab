from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class PolicyDecision(str, Enum):
    allow = "allow"
    deny = "deny"
    review = "review"


class PolicyGateType(str, Enum):
    prompt_approval = "prompt_approval"
    deployment_gate = "deployment_gate"
    action_gate = "action_gate"
    environment_promotion = "environment_promotion"
    human_approval = "human_approval"


class PolicyGateDefinition(BaseModel):
    gate_type: PolicyGateType
    name: str
    description: str
    required_inputs: List[str]
    deny_conditions: List[str]
    review_conditions: List[str]


class PolicyDecisionResponse(BaseModel):
    gate_type: PolicyGateType
    decision: PolicyDecision
    allowed: bool
    requires_review: bool
    reasons: List[str]
    required_controls: List[str]
    next_step: str


class PromptApprovalRequest(BaseModel):
    prompt_id: str = "inventory-agent-prompt-v0.4"
    prompt_text: str = Field(..., min_length=8)
    risk_tier: str = "Tier 2"
    includes_pii: bool = False
    includes_payment_data: bool = False
    asks_for_autonomous_action: bool = False
    customer_facing_output: bool = False


class DeploymentGateRequest(BaseModel):
    service_name: str
    environment: str = "dev"
    risk_tier: str = "Tier 2"
    tests_passed: bool
    security_review_complete: bool = False
    privacy_review_complete: bool = False
    rollback_plan_present: bool = False
    observability_enabled: bool = False
    human_approval_required: bool = True


class ActionGateRequest(BaseModel):
    action_name: str
    retail_system: str
    action_type: str
    risk_tier: str = "Tier 2"
    human_approval_status: str = "required"
    mutates_retail_system: bool = False
    touches_payment_data: bool = False
    customer_impacting: bool = False


class EnvironmentPromotionRequest(BaseModel):
    service_name: str
    from_environment: str = "dev"
    to_environment: str = "test"
    risk_tier: str = "Tier 2"
    tests_passed: bool
    change_ticket_present: bool
    rollback_plan_present: bool
    owner_approval_present: bool
    production_data_access: bool = False


class HumanApprovalRequest(BaseModel):
    workflow_id: str
    requested_action: str
    approver_role: str
    approval_status: str
    risk_tier: str = "Tier 2"
    autonomous_execution_requested: bool = False


class PolicyGateListResponse(BaseModel):
    gates: List[PolicyGateDefinition]
    count: int
