from app.schemas.policy import (
    ActionGateRequest,
    DeploymentGateRequest,
    EnvironmentPromotionRequest,
    HumanApprovalRequest,
    PolicyDecision,
    PolicyDecisionResponse,
    PolicyGateDefinition,
    PolicyGateType,
    PromptApprovalRequest,
)


def list_policy_gates() -> list[PolicyGateDefinition]:
    return [
        PolicyGateDefinition(
            gate_type=PolicyGateType.prompt_approval,
            name="Prompt Approval Gate",
            description="Reviews prompts for PII, payment data, customer-facing output, and autonomous-action instructions.",
            required_inputs=[
                "prompt_id",
                "prompt_text",
                "risk_tier",
                "includes_pii",
                "includes_payment_data",
                "asks_for_autonomous_action",
            ],
            deny_conditions=[
                "Prompt requests autonomous execution",
                "Prompt includes payment data",
            ],
            review_conditions=[
                "Prompt includes PII",
                "Prompt produces customer-facing output",
                "Prompt is Tier 3 or Tier 4",
            ],
        ),
        PolicyGateDefinition(
            gate_type=PolicyGateType.deployment_gate,
            name="Deployment Gate",
            description="Prevents deployment unless tests, reviews, rollback, and observability controls are satisfied.",
            required_inputs=[
                "service_name",
                "environment",
                "risk_tier",
                "tests_passed",
                "rollback_plan_present",
                "observability_enabled",
            ],
            deny_conditions=[
                "Tests failed",
                "Rollback plan missing for test/prod",
                "Observability missing for test/prod",
            ],
            review_conditions=[
                "Tier 3 or Tier 4 deployment",
                "Privacy/security review incomplete",
            ],
        ),
        PolicyGateDefinition(
            gate_type=PolicyGateType.action_gate,
            name="Retail Action Gate",
            description="Blocks autonomous mutation of retail systems and payment/customer-impacting actions without approval.",
            required_inputs=[
                "action_name",
                "retail_system",
                "action_type",
                "human_approval_status",
                "mutates_retail_system",
            ],
            deny_conditions=[
                "Autonomous retail-system mutation",
                "Payment action",
                "Customer-impacting action without approval",
            ],
            review_conditions=[
                "Tier 3 or Tier 4 action",
                "Retail system mutation requested",
            ],
        ),
        PolicyGateDefinition(
            gate_type=PolicyGateType.environment_promotion,
            name="Environment Promotion Gate",
            description="Controls promotion from dev to test or production through change, rollback, test, and approval checks.",
            required_inputs=[
                "service_name",
                "from_environment",
                "to_environment",
                "tests_passed",
                "change_ticket_present",
                "rollback_plan_present",
                "owner_approval_present",
            ],
            deny_conditions=[
                "Tests failed",
                "Change ticket missing",
                "Rollback plan missing",
                "Owner approval missing",
            ],
            review_conditions=[
                "Production promotion",
                "Production data access",
                "Tier 3 or Tier 4 service",
            ],
        ),
        PolicyGateDefinition(
            gate_type=PolicyGateType.human_approval,
            name="Human Approval Gate",
            description="Validates that governed workflows have explicit human approval before handoff.",
            required_inputs=[
                "workflow_id",
                "requested_action",
                "approver_role",
                "approval_status",
                "risk_tier",
            ],
            deny_conditions=[
                "Approval missing",
                "Autonomous execution requested",
            ],
            review_conditions=[
                "Tier 3 or Tier 4 approval",
                "Approver role insufficient",
            ],
        ),
    ]


def _response(
    gate_type: PolicyGateType,
    decision: PolicyDecision,
    reasons: list[str],
    required_controls: list[str],
    next_step: str,
) -> PolicyDecisionResponse:
    return PolicyDecisionResponse(
        gate_type=gate_type,
        decision=decision,
        allowed=decision == PolicyDecision.allow,
        requires_review=decision == PolicyDecision.review,
        reasons=reasons,
        required_controls=required_controls,
        next_step=next_step,
    )


def evaluate_prompt_approval(request: PromptApprovalRequest) -> PolicyDecisionResponse:
    reasons: list[str] = []
    controls: list[str] = ["Prompt versioning", "Prompt audit log"]

    if request.asks_for_autonomous_action:
        reasons.append("Prompt requests autonomous operational action.")
    if request.includes_payment_data:
        reasons.append("Prompt includes or requests payment data.")

    if reasons:
        return _response(
            PolicyGateType.prompt_approval,
            PolicyDecision.deny,
            reasons,
            controls + ["Rewrite prompt", "Governance forum review"],
            "Deny prompt until autonomous action and payment-data exposure are removed.",
        )

    if request.includes_pii:
        reasons.append("Prompt includes PII and requires privacy review.")
    if request.customer_facing_output:
        reasons.append("Prompt produces customer-facing output and requires review.")
    if request.risk_tier in {"Tier 3", "Tier 4"}:
        reasons.append(f"{request.risk_tier} prompt requires governance review.")

    if reasons:
        return _response(
            PolicyGateType.prompt_approval,
            PolicyDecision.review,
            reasons,
            controls + ["Privacy review", "Human approval"],
            "Route prompt to governance review before use.",
        )

    return _response(
        PolicyGateType.prompt_approval,
        PolicyDecision.allow,
        ["Prompt passed baseline approval checks."],
        controls,
        "Prompt may be used in controlled prototype workflow.",
    )


def evaluate_deployment_gate(request: DeploymentGateRequest) -> PolicyDecisionResponse:
    reasons: list[str] = []
    controls: list[str] = ["CI validation", "Deployment audit log"]

    if not request.tests_passed:
        reasons.append("Tests have not passed.")
    if request.environment in {"test", "prod"} and not request.rollback_plan_present:
        reasons.append("Rollback plan is required for test/prod deployment.")
    if request.environment in {"test", "prod"} and not request.observability_enabled:
        reasons.append("Observability is required for test/prod deployment.")

    if reasons:
        return _response(
            PolicyGateType.deployment_gate,
            PolicyDecision.deny,
            reasons,
            controls + ["Rollback plan", "Observability dashboard"],
            "Block deployment until required delivery controls are complete.",
        )

    if request.risk_tier in {"Tier 3", "Tier 4"}:
        if not request.security_review_complete:
            reasons.append("Security review is required for high-risk deployment.")
        if not request.privacy_review_complete:
            reasons.append("Privacy review is required for high-risk deployment.")

    if reasons:
        return _response(
            PolicyGateType.deployment_gate,
            PolicyDecision.review,
            reasons,
            controls + ["Security review", "Privacy review"],
            "Route deployment to governance review before release.",
        )

    return _response(
        PolicyGateType.deployment_gate,
        PolicyDecision.allow,
        ["Deployment passed required controls."],
        controls + ["Rollback plan", "Observability dashboard"],
        "Deployment may proceed.",
    )


def evaluate_action_gate(request: ActionGateRequest) -> PolicyDecisionResponse:
    reasons: list[str] = []
    controls: list[str] = ["Action audit log", "Retail system contract check"]

    if request.touches_payment_data:
        reasons.append("Payment-data action is restricted.")
    if request.mutates_retail_system and request.human_approval_status != "approved":
        reasons.append("Retail-system mutation requires human approval.")
    if request.customer_impacting and request.human_approval_status != "approved":
        reasons.append("Customer-impacting action requires human approval.")
    if request.action_type == "autonomous_execution":
        reasons.append("Autonomous execution is blocked by policy.")

    if reasons:
        return _response(
            PolicyGateType.action_gate,
            PolicyDecision.deny,
            reasons,
            controls + ["Human approval", "Restricted action review"],
            "Block action. AI may recommend only; execution requires governed handoff.",
        )

    if request.risk_tier in {"Tier 3", "Tier 4"} or request.mutates_retail_system:
        return _response(
            PolicyGateType.action_gate,
            PolicyDecision.review,
            ["Action requires governance review before execution."],
            controls + ["Governance review"],
            "Route action for review before handoff.",
        )

    return _response(
        PolicyGateType.action_gate,
        PolicyDecision.allow,
        ["Action passed baseline policy checks."],
        controls,
        "Action may proceed through controlled handoff.",
    )


def evaluate_environment_promotion(
    request: EnvironmentPromotionRequest,
) -> PolicyDecisionResponse:
    reasons: list[str] = []
    controls: list[str] = ["Change record", "Promotion audit log"]

    if not request.tests_passed:
        reasons.append("Tests have not passed.")
    if not request.change_ticket_present:
        reasons.append("Change ticket is missing.")
    if not request.rollback_plan_present:
        reasons.append("Rollback plan is missing.")
    if not request.owner_approval_present:
        reasons.append("Owner approval is missing.")

    if reasons:
        return _response(
            PolicyGateType.environment_promotion,
            PolicyDecision.deny,
            reasons,
            controls + ["Owner approval", "Rollback plan"],
            "Block promotion until change controls are complete.",
        )

    if request.to_environment == "prod" or request.production_data_access:
        return _response(
            PolicyGateType.environment_promotion,
            PolicyDecision.review,
            ["Production promotion or production data access requires governance review."],
            controls + ["Production readiness review"],
            "Route promotion to governance review.",
        )

    if request.risk_tier in {"Tier 3", "Tier 4"}:
        return _response(
            PolicyGateType.environment_promotion,
            PolicyDecision.review,
            [f"{request.risk_tier} service requires governance review before promotion."],
            controls + ["Governance review"],
            "Route promotion to governance review.",
        )

    return _response(
        PolicyGateType.environment_promotion,
        PolicyDecision.allow,
        ["Environment promotion passed required controls."],
        controls,
        "Promotion may proceed.",
    )


def evaluate_human_approval(request: HumanApprovalRequest) -> PolicyDecisionResponse:
    controls: list[str] = ["Approval record", "Workflow trace"]

    if request.autonomous_execution_requested:
        return _response(
            PolicyGateType.human_approval,
            PolicyDecision.deny,
            ["Autonomous execution remains blocked even when approval is present."],
            controls + ["Execution boundary"],
            "Deny autonomous execution. Allow only human-controlled handoff.",
        )

    if request.approval_status != "approved":
        return _response(
            PolicyGateType.human_approval,
            PolicyDecision.deny,
            ["Human approval is required before handoff."],
            controls + ["Human approval"],
            "Block handoff until approval is recorded.",
        )

    if request.risk_tier in {"Tier 3", "Tier 4"} and request.approver_role not in {
        "AI Governance Forum",
        "Store Operations Approver",
        "Executive Approver",
    }:
        return _response(
            PolicyGateType.human_approval,
            PolicyDecision.review,
            ["Approver role may be insufficient for high-risk workflow."],
            controls + ["Governance forum review"],
            "Route approval record to governance review.",
        )

    return _response(
        PolicyGateType.human_approval,
        PolicyDecision.allow,
        ["Human approval is present and autonomous execution is not requested."],
        controls,
        "Workflow may proceed to controlled handoff.",
    )
