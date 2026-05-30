import React, { useEffect, useMemo, useState } from "react";

const formatLabel = (value) => {
  if (value === null || value === undefined) return "—";
  return String(value)
    .replace(/_/g, " ")
    .replace(/\b\w/g, (char) => char.toUpperCase());
};

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

const formatJson = (value) => JSON.stringify(value, null, 2);

const phases = [
  ["Phase 1", "Governance Intake Portal"],
  ["Phase 2", "Backend Governance API + Risk Tiering"],
  ["Phase 3", "Retail APIs + Data Contracts"],
  ["Phase 4", "Inventory Replenishment Agent"],
  ["Phase 5", "Policy Gates + Governance Controls"],
  ["Phase 6", "Tracing, Observability + Cost Controls"],
  ["Phase 7", "SOPs, Runbooks + Support Handoff"],
  ["Phase 8", "Docker, Terraform, CI/CD + Deployment Readiness"],
  ["Phase 9", "Interview Demo Readiness Package"],
  ["Phase 10", "Frontend AI Governance Command Center"],
];

const supportArtifacts = [
  "AI Intake SOP",
  "Risk Tiering Runbook",
  "Agent Deployment Runbook",
  "Rollback Runbook",
  "Incident Escalation Runbook",
  "Prompt Versioning SOP",
  "Model Promotion SOP",
  "Support Handoff Checklist",
  "Post-Implementation Review Template",
];

const demoQuestions = [
  "How would you classify AI use cases into risk tiers?",
  "How would this integrate with POS, inventory, ERP, CRM, and supply-chain systems?",
  "How do you prevent autonomous AI from mutating retail systems?",
  "How do you trace and control cost across agentic workflows?",
  "How would you transition support to IT after deployment?",
];

function StatusPill({ tone = "neutral", children }) {
  return <span className={`pill pill-${tone}`}>{children}</span>;
}

function Card({ title, eyebrow, children, actions }) {
  return (
    <section className="card">
      <div className="card-header">
        <div>
          {eyebrow && <p className="eyebrow">{eyebrow}</p>}
          <h2>{title}</h2>
        </div>
        {actions && <div className="card-actions">{actions}</div>}
      </div>
      {children}
    </section>
  );
}

function JsonPanel({ title, data }) {
  return (
    <div className="json-panel">
      <div className="json-title">{title}</div>
      <pre>{data ? formatJson(data) : "No data loaded yet."}</pre>
    </div>
  );
}

function Metric({ label, value, hint }) {
  return (
    <div className="metric">
      <span>{label}</span>
      <strong>{value}</strong>
      {hint && <small>{hint}</small>}
    </div>
  );
}

function App() {
  const [health, setHealth] = useState(null);
  const [riskTiers, setRiskTiers] = useState([]);
  const [governanceDashboard, setGovernanceDashboard] = useState(null);
  const [retailSystems, setRetailSystems] = useState(null);
  const [inventoryContract, setInventoryContract] = useState(null);
  const [observability, setObservability] = useState(null);
  const [policyGates, setPolicyGates] = useState(null);
  const [agentRun, setAgentRun] = useState(null);
  const [approvalResult, setApprovalResult] = useState(null);
  const [actionGateResult, setActionGateResult] = useState(null);
  const [costGuardrailResult, setCostGuardrailResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [lastError, setLastError] = useState("");

  const apiStatusTone = health?.status === "ok" ? "success" : "warning";

  const highRiskCount = useMemo(() => {
    if (!governanceDashboard) return "—";
    return governanceDashboard.high_risk_requests;
  }, [governanceDashboard]);

  async function fetchJson(path, options = {}) {
    const response = await fetch(`${API_BASE}${path}`, {
      headers: {
        "Content-Type": "application/json",
        ...(options.headers || {}),
      },
      ...options,
    });

    if (!response.ok) {
      const detail = await response.text();
      throw new Error(`${path} failed: ${response.status} ${detail}`);
    }

    return response.json();
  }

  async function loadDashboard() {
    setLoading(true);
    setLastError("");

    try {
      const [
        healthData,
        riskTierData,
        governanceData,
        retailData,
        contractData,
        observabilityData,
        policyData,
      ] = await Promise.all([
        fetchJson("/health"),
        fetchJson("/v1/risk/tiers"),
        fetchJson("/v1/governance/dashboard"),
        fetchJson("/v1/retail/systems"),
        fetchJson("/v1/retail/contracts/inventory"),
        fetchJson("/v1/observability/dashboard"),
        fetchJson("/v1/policies/gates"),
      ]);

      setHealth(healthData);
      setRiskTiers(riskTierData);
      setGovernanceDashboard(governanceData);
      setRetailSystems(retailData);
      setInventoryContract(contractData);
      setObservability(observabilityData);
      setPolicyGates(policyData);
    } catch (error) {
      setLastError(error.message);
    } finally {
      setLoading(false);
    }
  }

  async function runInventoryAgent() {
    setLoading(true);
    setLastError("");

    try {
      const result = await fetchJson("/v1/agents/inventory-replenishment/run", {
        method: "POST",
        body: JSON.stringify({
          requested_by: "frontend-command-center",
          store_ids: ["STORE-1042", "STORE-2210"],
          business_goal:
            "Identify low-stock inventory risk and recommend replenishment actions.",
        }),
      });

      setAgentRun(result);
      setApprovalResult(null);
    } catch (error) {
      setLastError(error.message);
    } finally {
      setLoading(false);
    }
  }

  async function approveAgentWorkflow() {
    if (!agentRun?.workflow_id) {
      setLastError("Run the inventory agent first before approval.");
      return;
    }

    setLoading(true);
    setLastError("");

    try {
      const result = await fetchJson("/v1/agents/inventory-replenishment/approval", {
        method: "POST",
        body: JSON.stringify({
          workflow_id: agentRun.workflow_id,
          approved_by: "store-manager-1042",
          decision: "approve",
          approval_note: "Approved for controlled handoff from command center.",
        }),
      });

      setApprovalResult(result);
    } catch (error) {
      setLastError(error.message);
    } finally {
      setLoading(false);
    }
  }

  async function testActionGate() {
    setLoading(true);
    setLastError("");

    try {
      const result = await fetchJson("/v1/policies/action-gate", {
        method: "POST",
        body: JSON.stringify({
          action_name: "create_purchase_order",
          retail_system: "Inventory",
          action_type: "autonomous_execution",
          risk_tier: "Tier 4",
          human_approval_status: "approved",
          mutates_retail_system: true,
        }),
      });

      setActionGateResult(result);
    } catch (error) {
      setLastError(error.message);
    } finally {
      setLoading(false);
    }
  }

  async function testCostGuardrail() {
    setLoading(true);
    setLastError("");

    try {
      const result = await fetchJson("/v1/observability/cost-guardrail", {
        method: "POST",
        body: JSON.stringify({
          workflow_id: "wf-expensive",
          estimated_tokens: 12000,
          estimated_cost_usd: 0.12,
          max_tokens: 5000,
          max_cost_usd: 0.05,
          risk_tier: "Tier 2",
        }),
      });

      setCostGuardrailResult(result);
    } catch (error) {
      setLastError(error.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadDashboard();
  }, []);

  return (
    <main className="app-shell">
      <section className="hero">
        <div>
          <p className="eyebrow">Family Dollar Platform Lab</p>
          <h1>AI Governance Command Center</h1>
          <p className="hero-copy">
            A full-stack, GCP-ready retail AI governance and agentic workflow
            platform showing intake, risk-tiering, retail APIs, agent workflows,
            policy gates, observability, cost controls, deployment readiness,
            and support handoff.
          </p>
          <div className="hero-actions">
            <button onClick={loadDashboard} disabled={loading}>
              {loading ? "Loading..." : "Refresh platform data"}
            </button>
            <a href={`${API_BASE}/docs`} target="_blank" rel="noreferrer">
              Open FastAPI docs
            </a>
          </div>
          {lastError && <div className="error-banner">{lastError}</div>}
        </div>

        <div className="hero-panel">
          <StatusPill tone={apiStatusTone}>
            API {health?.status || "checking"}
          </StatusPill>
          <h3>Core governance rule</h3>
          <p>
            AI may recommend, summarize, and draft. AI may not autonomously
            mutate retail systems, access payment data, bypass human approval,
            or bypass change control.
          </p>
        </div>
      </section>

      <section className="metrics-grid">
        <Metric
          label="Portfolio requests"
          value={governanceDashboard?.total_requests ?? "—"}
          hint="Seeded governance queue"
        />
        <Metric
          label="High-risk requests"
          value={highRiskCount}
          hint="Tier 3 + Tier 4"
        />
        <Metric
          label="Retail systems"
          value={retailSystems?.count ?? "—"}
          hint="POS, Inventory, ERP, CRM, Supply Chain, Identity"
        />
        <Metric
          label="Trace events"
          value={observability?.total_trace_events ?? "—"}
          hint="Agent workflow observability"
        />
        <Metric
          label="Token estimate"
          value={observability?.total_token_estimate ?? "—"}
          hint="Cost-control signal"
        />
        <Metric
          label="Autonomous actions blocked"
          value={observability?.blocked_autonomous_actions ?? "—"}
          hint="Guardrail proof"
        />
      </section>

      <section className="phase-strip">
        {phases.map(([phase, label]) => (
          <div className="phase" key={phase}>
            <strong>{phase}</strong>
            <span>{label}</span>
          </div>
        ))}
      </section>

      <div className="dashboard-grid">
        <Card title="Risk-Tier Dashboard" eyebrow="Governance triage">
          <div className="tier-list">
            {riskTiers.map((tier) => (
              <div className="tier-card" key={tier.tier}>
                <div className="tier-title">
                  <strong>{tier.tier}</strong>
                  <StatusPill
                    tone={
                      tier.tier === "Tier 4"
                        ? "danger"
                        : tier.tier === "Tier 3"
                          ? "warning"
                          : "success"
                    }
                  >
                    {tier.label}
                  </StatusPill>
                </div>
                <p>{tier.description}</p>
                <small>{tier.required_controls.join(" • ")}</small>
              </div>
            ))}
          </div>
        </Card>

        <Card title="Retail System Contracts" eyebrow="Enterprise integration">
          <p className="section-copy">
            AI integrates through governed APIs, not shadow access. Each system
            has owner teams, allowed operations, forbidden operations, data
            sensitivity, and usage notes.
          </p>
          <div className="system-list">
            {retailSystems?.systems?.map((system) => (
              <div className="system-row" key={system.system_id}>
                <strong>{system.name}</strong>
                <span>{system.owner_team}</span>
                <StatusPill
                  tone={
                    system.data_sensitivity === "Payment"
                      ? "danger"
                      : system.data_sensitivity === "PII"
                        ? "warning"
                        : "neutral"
                  }
                >
                  {system.data_sensitivity}
                </StatusPill>
              </div>
            ))}
          </div>
          <JsonPanel title="Inventory Contract" data={inventoryContract} />
        </Card>

        <Card
          title="Inventory Agent Workflow"
          eyebrow="Agentic workflow with approval gate"
          actions={
            <>
              <button onClick={runInventoryAgent} disabled={loading}>
                Run agent
              </button>
              <button onClick={approveAgentWorkflow} disabled={loading || !agentRun}>
                Approve handoff
              </button>
            </>
          }
        >
          <p className="section-copy">
            The agent reads governed inventory, POS, and supply-chain APIs,
            generates reorder recommendations, records traces, estimates cost,
            and keeps autonomous execution blocked.
          </p>

          {agentRun && (
            <div className="agent-summary">
              <Metric label="Workflow" value={formatLabel(agentRun.workflow_status)} />
              <Metric label="Approval" value={formatLabel(agentRun.approval_status)} />
              <Metric
                label="Recommendations"
                value={agentRun.recommendations?.length ?? 0}
              />
              <Metric
                label="Autonomous execution"
                value={String(agentRun.autonomous_execution_allowed)}
              />
            </div>
          )}

          <JsonPanel title="Agent Run Result" data={agentRun} />
          <JsonPanel title="Approval Result" data={approvalResult} />
        </Card>

        <Card
          title="Policy Gate Tester"
          eyebrow="Governance as enforceable control"
          actions={
            <button onClick={testActionGate} disabled={loading}>
              Test autonomous action
            </button>
          }
        >
          <p className="section-copy">
            This tester intentionally asks the platform to create a purchase
            order autonomously. The correct result is <strong>deny</strong>.
          </p>
          <div className="system-list compact">
            {policyGates?.gates?.map((gate) => (
              <div className="system-row" key={gate.gate_type}>
                <strong>{gate.name}</strong>
                <span>{gate.gate_type}</span>
              </div>
            ))}
          </div>
          <JsonPanel title="Action Gate Result" data={actionGateResult} />
        </Card>

        <Card
          title="Observability & Cost Controls"
          eyebrow="Operate safely at scale"
          actions={
            <button onClick={testCostGuardrail} disabled={loading}>
              Test expensive workflow
            </button>
          }
        >
          <p className="section-copy">
            The observability layer shows traces, latency, token estimates, cost
            estimates, guardrails, and approval status.
          </p>
          <div className="agent-summary">
            <Metric
              label="Portfolio status"
              value={observability?.portfolio_status ?? "—"}
            />
            <Metric
              label="Average latency"
              value={`${observability?.average_latency_ms ?? "—"}ms`}
            />
            <Metric
              label="Cost estimate"
              value={`$${observability?.total_cost_estimate_usd ?? "—"}`}
            />
            <Metric
              label="Human approval workflows"
              value={observability?.workflows_requiring_human_approval ?? "—"}
            />
          </div>

          <div className="guardrail-grid">
            {observability?.guardrails?.map((guardrail) => (
              <div className="guardrail" key={guardrail.name}>
                <StatusPill tone="success">{guardrail.status}</StatusPill>
                <strong>{guardrail.name}</strong>
                <p>{guardrail.current_value}</p>
              </div>
            ))}
          </div>

          <JsonPanel title="Cost Guardrail Result" data={costGuardrailResult} />
        </Card>

        <Card title="Support Handoff & Interview Readiness" eyebrow="Operate and explain">
          <p className="section-copy">
            The platform includes SOPs, runbooks, rollback, incident escalation,
            prompt/model versioning, support handoff, post-implementation review,
            and interview-ready demo artifacts.
          </p>

          <div className="artifact-grid">
            {supportArtifacts.map((artifact) => (
              <div className="artifact" key={artifact}>
                {artifact}
              </div>
            ))}
          </div>

          <h3>Likely interview questions</h3>
          <ul className="question-list">
            {demoQuestions.map((question) => (
              <li key={question}>{question}</li>
            ))}
          </ul>
        </Card>
      </div>
    </main>
  );
}

export default App;
