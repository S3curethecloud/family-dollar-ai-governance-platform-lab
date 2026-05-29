from fastapi import APIRouter, HTTPException

from app.core.inventory_agent import (
    decide_inventory_workflow,
    get_inventory_workflow,
    run_inventory_replenishment_agent,
)
from app.schemas.agent import (
    InventoryAgentApprovalRequest,
    InventoryAgentApprovalResponse,
    InventoryAgentRunRequest,
    InventoryAgentWorkflowState,
)

router = APIRouter()


@router.post(
    "/inventory-replenishment/run",
    response_model=InventoryAgentWorkflowState,
)
def run_inventory_agent(
    payload: InventoryAgentRunRequest,
) -> InventoryAgentWorkflowState:
    return run_inventory_replenishment_agent(payload)


@router.get(
    "/inventory-replenishment/workflows/{workflow_id}",
    response_model=InventoryAgentWorkflowState,
)
def get_inventory_agent_workflow(
    workflow_id: str,
) -> InventoryAgentWorkflowState:
    workflow = get_inventory_workflow(workflow_id)

    if workflow is None:
        raise HTTPException(status_code=404, detail="Inventory agent workflow not found.")

    return workflow


@router.post(
    "/inventory-replenishment/approval",
    response_model=InventoryAgentApprovalResponse,
)
def approve_inventory_agent_workflow(
    payload: InventoryAgentApprovalRequest,
) -> InventoryAgentApprovalResponse:
    approval = decide_inventory_workflow(payload)

    if approval is None:
        raise HTTPException(status_code=404, detail="Inventory agent workflow not found.")

    return approval
