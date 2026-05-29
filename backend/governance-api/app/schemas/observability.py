from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class ObservabilityStatus(str, Enum):
    healthy = "healthy"
    warning = "warning"
    critical = "critical"


class TraceEventSummary(BaseModel):
    workflow_id: str
    agent_id: str
    step_name: str
    tool_name: str
    status: str
    latency_ms: int
    token_estimate: int
    cost_estimate_usd: float
    governance_boundary: str


class WorkflowTraceSummary(BaseModel):
    workflow_id: str
    agent_id: str
    workflow_status: str
    approval_status: str
    trace_event_count: int
    total_latency_ms: int
    total_token_estimate: int
    total_cost_estimate_usd: float
    autonomous_execution_allowed: bool
    human_approval_required: bool


class CostTrendPoint(BaseModel):
    period: str
    workflow_count: int
    token_estimate: int
    cost_estimate_usd: float


class LatencyTrendPoint(BaseModel):
    period: str
    p50_latency_ms: int
    p95_latency_ms: int
    slowest_step: str


class GuardrailStatus(BaseModel):
    name: str
    status: ObservabilityStatus
    threshold: str
    current_value: str
    recommendation: str


class ObservabilityDashboard(BaseModel):
    total_workflows: int
    total_trace_events: int
    total_token_estimate: int
    total_cost_estimate_usd: float
    average_latency_ms: int
    blocked_autonomous_actions: int
    workflows_requiring_human_approval: int
    portfolio_status: ObservabilityStatus
    trace_summaries: List[WorkflowTraceSummary]
    recent_trace_events: List[TraceEventSummary]
    cost_trend: List[CostTrendPoint]
    latency_trend: List[LatencyTrendPoint]
    guardrails: List[GuardrailStatus]


class CostGuardrailRequest(BaseModel):
    workflow_id: str = "wf-demo"
    estimated_tokens: int = Field(..., ge=0)
    estimated_cost_usd: float = Field(..., ge=0)
    max_tokens: int = 5000
    max_cost_usd: float = 0.05
    risk_tier: str = "Tier 2"


class CostGuardrailResponse(BaseModel):
    allowed: bool
    status: ObservabilityStatus
    reasons: List[str]
    required_actions: List[str]
    next_step: str
