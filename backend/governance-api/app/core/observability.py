from app.schemas.observability import (
    CostGuardrailRequest,
    CostGuardrailResponse,
    CostTrendPoint,
    GuardrailStatus,
    LatencyTrendPoint,
    ObservabilityDashboard,
    ObservabilityStatus,
    TraceEventSummary,
    WorkflowTraceSummary,
)

DEMO_TRACE_EVENTS = [
    TraceEventSummary(
        workflow_id="wf-inventory-demo",
        agent_id="inventory-replenishment-agent-v1",
        step_name="inspect_low_stock_inventory",
        tool_name="inventory_api.low_stock",
        status="completed",
        latency_ms=42,
        token_estimate=260,
        cost_estimate_usd=0.0005,
        governance_boundary="Read-only inventory access through approved data contract.",
    ),
    TraceEventSummary(
        workflow_id="wf-inventory-demo",
        agent_id="inventory-replenishment-agent-v1",
        step_name="check_store_demand_signals",
        tool_name="pos_api.sales_summary",
        status="completed",
        latency_ms=38,
        token_estimate=220,
        cost_estimate_usd=0.0004,
        governance_boundary="Aggregated POS summary only; payment data not exposed.",
    ),
    TraceEventSummary(
        workflow_id="wf-inventory-demo",
        agent_id="inventory-replenishment-agent-v1",
        step_name="check_supply_chain_constraints",
        tool_name="supply_chain_api.shipments",
        status="completed",
        latency_ms=31,
        token_estimate=180,
        cost_estimate_usd=0.0003,
        governance_boundary="Read-only shipment status; no supplier action executed.",
    ),
    TraceEventSummary(
        workflow_id="wf-inventory-demo",
        agent_id="inventory-replenishment-agent-v1",
        step_name="generate_reorder_recommendations",
        tool_name="agent.recommendation_engine",
        status="completed",
        latency_ms=55,
        token_estimate=410,
        cost_estimate_usd=0.0008,
        governance_boundary="Recommendation only; purchase order creation blocked.",
    ),
    TraceEventSummary(
        workflow_id="wf-inventory-demo",
        agent_id="inventory-replenishment-agent-v1",
        step_name="enforce_approval_gate",
        tool_name="governance_policy.human_approval_gate",
        status="completed",
        latency_ms=18,
        token_estimate=120,
        cost_estimate_usd=0.0002,
        governance_boundary="Human approval required before handoff.",
    ),
    TraceEventSummary(
        workflow_id="wf-inventory-demo",
        agent_id="inventory-replenishment-agent-v1",
        step_name="record_human_approval_decision",
        tool_name="governance_forum.approval_record",
        status="completed",
        latency_ms=22,
        token_estimate=90,
        cost_estimate_usd=0.0001,
        governance_boundary="Approval recorded; autonomous execution still blocked.",
    ),
]


def build_observability_dashboard() -> ObservabilityDashboard:
    total_trace_events = len(DEMO_TRACE_EVENTS)
    total_tokens = sum(event.token_estimate for event in DEMO_TRACE_EVENTS)
    total_cost = round(sum(event.cost_estimate_usd for event in DEMO_TRACE_EVENTS), 6)
    total_latency = sum(event.latency_ms for event in DEMO_TRACE_EVENTS)
    average_latency = int(total_latency / total_trace_events)

    trace_summary = WorkflowTraceSummary(
        workflow_id="wf-inventory-demo",
        agent_id="inventory-replenishment-agent-v1",
        workflow_status="approved_for_handoff",
        approval_status="approved",
        trace_event_count=total_trace_events,
        total_latency_ms=total_latency,
        total_token_estimate=total_tokens,
        total_cost_estimate_usd=total_cost,
        autonomous_execution_allowed=False,
        human_approval_required=True,
    )

    guardrails = [
        GuardrailStatus(
            name="Autonomous Execution Guardrail",
            status=ObservabilityStatus.healthy,
            threshold="0 autonomous retail mutations allowed",
            current_value="0 autonomous retail mutations executed",
            recommendation="Continue enforcing recommendation-only workflow boundary.",
        ),
        GuardrailStatus(
            name="Cost Guardrail",
            status=ObservabilityStatus.healthy,
            threshold="Workflow cost under $0.05",
            current_value=f"${total_cost:.4f}",
            recommendation="Current demo workflow is below cost threshold.",
        ),
        GuardrailStatus(
            name="Latency Guardrail",
            status=ObservabilityStatus.healthy,
            threshold="Average step latency under 250ms",
            current_value=f"{average_latency}ms",
            recommendation="Current workflow latency is acceptable.",
        ),
        GuardrailStatus(
            name="Human Approval Guardrail",
            status=ObservabilityStatus.healthy,
            threshold="Human approval required for operational handoff",
            current_value="Approval gate enforced",
            recommendation="Maintain approval record before support handoff.",
        ),
    ]

    return ObservabilityDashboard(
        total_workflows=1,
        total_trace_events=total_trace_events,
        total_token_estimate=total_tokens,
        total_cost_estimate_usd=total_cost,
        average_latency_ms=average_latency,
        blocked_autonomous_actions=1,
        workflows_requiring_human_approval=1,
        portfolio_status=ObservabilityStatus.healthy,
        trace_summaries=[trace_summary],
        recent_trace_events=DEMO_TRACE_EVENTS,
        cost_trend=[
            CostTrendPoint(
                period="Phase 4 demo run",
                workflow_count=1,
                token_estimate=1190,
                cost_estimate_usd=0.0022,
            ),
            CostTrendPoint(
                period="Phase 4 approval run",
                workflow_count=1,
                token_estimate=1280,
                cost_estimate_usd=0.0023,
            ),
        ],
        latency_trend=[
            LatencyTrendPoint(
                period="Inventory inspection",
                p50_latency_ms=42,
                p95_latency_ms=55,
                slowest_step="generate_reorder_recommendations",
            ),
            LatencyTrendPoint(
                period="Approval handoff",
                p50_latency_ms=22,
                p95_latency_ms=22,
                slowest_step="record_human_approval_decision",
            ),
        ],
        guardrails=guardrails,
    )


def evaluate_cost_guardrail(request: CostGuardrailRequest) -> CostGuardrailResponse:
    reasons: list[str] = []
    required_actions: list[str] = []

    if request.estimated_tokens > request.max_tokens:
        reasons.append("Estimated tokens exceed workflow token threshold.")
        required_actions.append("Reduce context size or split workflow into smaller steps.")

    if request.estimated_cost_usd > request.max_cost_usd:
        reasons.append("Estimated cost exceeds workflow cost threshold.")
        required_actions.append("Route to cost review before execution.")

    if request.risk_tier in {"Tier 3", "Tier 4"} and request.estimated_cost_usd > request.max_cost_usd * 0.5:
        reasons.append("High-risk workflow exceeds half of cost threshold.")
        required_actions.append("Governance review required for high-risk cost profile.")

    if reasons:
        return CostGuardrailResponse(
            allowed=False,
            status=ObservabilityStatus.warning,
            reasons=reasons,
            required_actions=required_actions,
            next_step="Optimize workflow or request governance/cost review before proceeding.",
        )

    return CostGuardrailResponse(
        allowed=True,
        status=ObservabilityStatus.healthy,
        reasons=["Estimated workflow cost and token usage are within guardrails."],
        required_actions=["Continue tracing token, cost, and latency metrics."],
        next_step="Workflow may proceed under current cost controls.",
    )
