from enum import Enum
from typing import List

from pydantic import BaseModel, Field

from app.schemas.retail import ReorderRecommendation


class WorkflowStatus(str, Enum):
    completed = "completed"
    awaiting_approval = "awaiting_approval"
    approved_for_handoff = "approved_for_handoff"
    rejected = "rejected"


class ApprovalStatus(str, Enum):
    not_requested = "not_requested"
    required = "required"
    approved = "approved"
    rejected = "rejected"


class AgentTraceEvent(BaseModel):
    event_id: str
    workflow_id: str
    step_name: str
    tool_name: str
    status: str
    latency_ms: int
    token_estimate: int
    cost_estimate_usd: float
    details: dict[str, object] = Field(default_factory=dict)


class InventoryAgentRunRequest(BaseModel):
    requested_by: str = "ai-platform-demo"
    store_ids: List[str] = Field(default_factory=lambda: ["STORE-1042", "STORE-2210"])
    business_goal: str = (
        "Identify low-stock inventory risk and recommend replenishment actions."
    )


class InventoryAgentWorkflowState(BaseModel):
    workflow_id: str
    agent_id: str = "inventory-replenishment-agent-v1"
    workflow_status: WorkflowStatus
    approval_status: ApprovalStatus
    requested_by: str
    target_stores: List[str]
    prompt_version: str = "inventory-agent-prompt-v0.4"
    model_version: str = "rules-plus-gemini-sim-v0.4"
    rollback_status: str = "not_required_no_execution_performed"
    business_summary: str
    risk_summary: str
    recommendations: List[ReorderRecommendation]
    trace_events: List[AgentTraceEvent]
    total_token_estimate: int
    total_cost_estimate_usd: float
    autonomous_execution_allowed: bool = False
    human_approval_required: bool = True


class ApprovalDecision(str, Enum):
    approve = "approve"
    reject = "reject"


class InventoryAgentApprovalRequest(BaseModel):
    workflow_id: str
    approved_by: str
    decision: ApprovalDecision
    approval_note: str = "Reviewed by store operations approver."


class InventoryAgentApprovalResponse(BaseModel):
    workflow_id: str
    approval_status: ApprovalStatus
    workflow_status: WorkflowStatus
    handoff_ready: bool
    autonomous_execution_allowed: bool = False
    message: str
    trace_events: List[AgentTraceEvent]
