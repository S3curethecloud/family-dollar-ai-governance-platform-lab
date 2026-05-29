from datetime import datetime, timezone
from uuid import uuid4

from app.data.retail_systems import (
    build_reorder_recommendations,
    get_sales_summary,
    list_low_stock_items,
    list_shipments,
)
from app.schemas.agent import (
    AgentTraceEvent,
    ApprovalDecision,
    ApprovalStatus,
    InventoryAgentApprovalRequest,
    InventoryAgentApprovalResponse,
    InventoryAgentRunRequest,
    InventoryAgentWorkflowState,
    WorkflowStatus,
)

_WORKFLOWS: dict[str, InventoryAgentWorkflowState] = {}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _make_trace_event(
    workflow_id: str,
    event_number: int,
    step_name: str,
    tool_name: str,
    latency_ms: int,
    token_estimate: int,
    cost_estimate_usd: float,
    details: dict[str, object],
) -> AgentTraceEvent:
    return AgentTraceEvent(
        event_id=f"trace-{event_number:03d}",
        workflow_id=workflow_id,
        step_name=step_name,
        tool_name=tool_name,
        status="completed",
        latency_ms=latency_ms,
        token_estimate=token_estimate,
        cost_estimate_usd=cost_estimate_usd,
        details=details,
    )


def run_inventory_replenishment_agent(
    request: InventoryAgentRunRequest,
) -> InventoryAgentWorkflowState:
    workflow_id = f"wf-inventory-{uuid4().hex[:10]}"
    trace_events: list[AgentTraceEvent] = []

    low_stock_items = [
        item for item in list_low_stock_items() if item.store_id in request.store_ids
    ]
    trace_events.append(
        _make_trace_event(
            workflow_id=workflow_id,
            event_number=len(trace_events) + 1,
            step_name="inspect_low_stock_inventory",
            tool_name="inventory_api.low_stock",
            latency_ms=42,
            token_estimate=260,
            cost_estimate_usd=0.0005,
            details={
                "records_read": len(low_stock_items),
                "data_contract": "data-contracts/inventory-api.yaml",
                "allowed_operation": "Read on-hand inventory",
            },
        )
    )

    sales_summaries = [
        summary
        for store_id in request.store_ids
        if (summary := get_sales_summary(store_id)) is not None
    ]
    trace_events.append(
        _make_trace_event(
            workflow_id=workflow_id,
            event_number=len(trace_events) + 1,
            step_name="check_store_demand_signals",
            tool_name="pos_api.sales_summary",
            latency_ms=38,
            token_estimate=220,
            cost_estimate_usd=0.0004,
            details={
                "stores_checked": request.store_ids,
                "summaries_found": len(sales_summaries),
                "data_contract": "data-contracts/pos-api.yaml",
                "payment_data_exposed": False,
            },
        )
    )

    shipments = [
        shipment
        for shipment in list_shipments()
        if shipment.destination_store_id in request.store_ids
    ]
    trace_events.append(
        _make_trace_event(
            workflow_id=workflow_id,
            event_number=len(trace_events) + 1,
            step_name="check_supply_chain_constraints",
            tool_name="supply_chain_api.shipments",
            latency_ms=31,
            token_estimate=180,
            cost_estimate_usd=0.0003,
            details={
                "shipments_checked": len(shipments),
                "data_contract": "data-contracts/supply-chain-api.yaml",
                "execution_performed": False,
            },
        )
    )

    recommendations = [
        recommendation
        for recommendation in build_reorder_recommendations()
        if recommendation.store_id in request.store_ids
    ]
    trace_events.append(
        _make_trace_event(
            workflow_id=workflow_id,
            event_number=len(trace_events) + 1,
            step_name="generate_reorder_recommendations",
            tool_name="agent.recommendation_engine",
            latency_ms=55,
            token_estimate=410,
            cost_estimate_usd=0.0008,
            details={
                "recommendations_created": len(recommendations),
                "autonomous_execution_allowed": False,
                "human_approval_required": True,
            },
        )
    )

    total_stockout_risk = len(low_stock_items)
    delayed_shipments = [shipment for shipment in shipments if shipment.status == "Delayed"]

    business_summary = (
        f"Analyzed {len(request.store_ids)} stores and found {total_stockout_risk} "
        "low-stock SKU signals. Generated approval-gated replenishment "
        "recommendations for store operations review."
    )

    risk_summary = (
        f"{len(delayed_shipments)} delayed shipment signal(s) found. "
        "No purchase order, supplier action, inventory mutation, or POS action was executed."
    )

    trace_events.append(
        _make_trace_event(
            workflow_id=workflow_id,
            event_number=len(trace_events) + 1,
            step_name="enforce_approval_gate",
            tool_name="governance_policy.human_approval_gate",
            latency_ms=18,
            token_estimate=120,
            cost_estimate_usd=0.0002,
            details={
                "approval_status": ApprovalStatus.required.value,
                "blocked_action": "autonomous_purchase_order_creation",
                "policy_result": "recommendation_only",
            },
        )
    )

    state = InventoryAgentWorkflowState(
        workflow_id=workflow_id,
        workflow_status=WorkflowStatus.awaiting_approval,
        approval_status=ApprovalStatus.required,
        requested_by=request.requested_by,
        target_stores=request.store_ids,
        business_summary=business_summary,
        risk_summary=risk_summary,
        recommendations=recommendations,
        trace_events=trace_events,
        total_token_estimate=sum(event.token_estimate for event in trace_events),
        total_cost_estimate_usd=round(
            sum(event.cost_estimate_usd for event in trace_events),
            6,
        ),
    )

    _WORKFLOWS[workflow_id] = state
    return state


def get_inventory_workflow(
    workflow_id: str,
) -> InventoryAgentWorkflowState | None:
    return _WORKFLOWS.get(workflow_id)


def decide_inventory_workflow(
    request: InventoryAgentApprovalRequest,
) -> InventoryAgentApprovalResponse | None:
    workflow = _WORKFLOWS.get(request.workflow_id)

    if workflow is None:
        return None

    decision_is_approval = request.decision == ApprovalDecision.approve

    event = _make_trace_event(
        workflow_id=workflow.workflow_id,
        event_number=len(workflow.trace_events) + 1,
        step_name="record_human_approval_decision",
        tool_name="governance_forum.approval_record",
        latency_ms=22,
        token_estimate=90,
        cost_estimate_usd=0.0001,
        details={
            "approved_by": request.approved_by,
            "decision": request.decision.value,
            "approval_note": request.approval_note,
            "timestamp": _utc_now(),
            "autonomous_execution_allowed": False,
        },
    )

    workflow.trace_events.append(event)

    if decision_is_approval:
        workflow.approval_status = ApprovalStatus.approved
        workflow.workflow_status = WorkflowStatus.approved_for_handoff
        message = (
            "Workflow approved for human-controlled handoff. "
            "Autonomous execution remains blocked."
        )
    else:
        workflow.approval_status = ApprovalStatus.rejected
        workflow.workflow_status = WorkflowStatus.rejected
        message = (
            "Workflow rejected. No execution was performed and no retail system "
            "was mutated."
        )

    workflow.total_token_estimate = sum(
        event.token_estimate for event in workflow.trace_events
    )
    workflow.total_cost_estimate_usd = round(
        sum(event.cost_estimate_usd for event in workflow.trace_events),
        6,
    )

    _WORKFLOWS[workflow.workflow_id] = workflow

    return InventoryAgentApprovalResponse(
        workflow_id=workflow.workflow_id,
        approval_status=workflow.approval_status,
        workflow_status=workflow.workflow_status,
        handoff_ready=decision_is_approval,
        autonomous_execution_allowed=False,
        message=message,
        trace_events=workflow.trace_events,
    )
