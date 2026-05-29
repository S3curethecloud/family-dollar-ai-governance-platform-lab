import { useMemo, useState } from "react";
import { sampleRequests } from "./data/sampleRequests.js";

const initialForm = {
  businessUnit: "Store Operations",
  requester: "",
  useCase: "",
  retailSystem: "Inventory",
  dataSensitivity: "Internal",
  customerData: false,
  paymentData: false,
  operationalImpact: "Store-level operations",
  expectedBusinessValue: "",
  modelType: "Agentic workflow with retrieval",
  autonomousActionLevel: "Recommend only",
  humanApprovalRequired: true,
  dependencies: "",
  targetReleaseWindow: "Q3 pilot"
};

const tierDescriptions = {
  "Tier 1": "Low risk: internal productivity use case with limited data sensitivity and no operational execution.",
  "Tier 2": "Moderate risk: business workflow support, internal data, limited customer impact, human approval required.",
  "Tier 3": "High risk: customer data, sensitive decisions, cross-system dependencies, or customer-facing output.",
  "Tier 4": "Restricted: payment data, autonomous action, regulated impact, or executive approval required."
};

function scoreRisk(form) {
  let score = 0;

  const sensitivityScore = {
    Public: 0,
    Internal: 1,
    Confidential: 2,
    PII: 3,
    Payment: 5
  };

  const autonomyScore = {
    "Summarize only": 0,
    "Recommend only": 1,
    "Draft response": 2,
    "Autonomous action": 5
  };

  const impactScore = {
    "Internal productivity": 0,
    "Back-office operations": 1,
    "Store-level operations": 2,
    "Customer-facing support": 3,
    "Supply-chain operations": 3,
    "Enterprise-critical operations": 4
  };

  score += sensitivityScore[form.dataSensitivity] ?? 1;
  score += autonomyScore[form.autonomousActionLevel] ?? 1;
  score += impactScore[form.operationalImpact] ?? 1;

  if (form.customerData) score += 2;
  if (form.paymentData) score += 5;

  const dependencyCount = form.dependencies
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean).length;

  if (dependencyCount >= 3) score += 2;
  if (dependencyCount === 2) score += 1;

  const tier =
    form.paymentData || form.autonomousActionLevel === "Autonomous action"
      ? "Tier 4"
      : score >= 8
        ? "Tier 3"
        : score >= 4
          ? "Tier 2"
          : "Tier 1";

  return {
    score,
    tier,
    humanApprovalRequired:
      form.humanApprovalRequired || tier === "Tier 3" || tier === "Tier 4"
  };
}

function nextRequestId(existingRequests) {
  return `FD-AI-${String(existingRequests.length + 1).padStart(3, "0")}`;
}

function App() {
  const [requests, setRequests] = useState(sampleRequests);
  const [form, setForm] = useState(initialForm);

  const riskPreview = useMemo(() => scoreRisk(form), [form]);

  const stats = useMemo(() => {
    const total = requests.length;
    const highRisk = requests.filter((request) =>
      ["Tier 3", "Tier 4"].includes(request.riskTier)
    ).length;
    const restricted = requests.filter((request) => request.riskTier === "Tier 4").length;
    const approved = requests.filter((request) =>
      ["Approved for Prototype", "Architecture Review"].includes(request.status)
    ).length;

    return { total, highRisk, restricted, approved };
  }, [requests]);

  function updateForm(field, value) {
    setForm((current) => ({ ...current, [field]: value }));
  }

  function submitRequest(event) {
    event.preventDefault();

    const evaluatedRisk = scoreRisk(form);

    const newRequest = {
      id: nextRequestId(requests),
      ...form,
      humanApprovalRequired: evaluatedRisk.humanApprovalRequired,
      riskTier: evaluatedRisk.tier,
      status:
        evaluatedRisk.tier === "Tier 4"
          ? "Restricted / Executive Review"
          : evaluatedRisk.tier === "Tier 3"
            ? "Governance Review"
            : "Architecture Review",
      ownerTeam:
        evaluatedRisk.tier === "Tier 4"
          ? "AI Governance Forum"
          : "AI Platform + Retail Systems"
    };

    setRequests((current) => [newRequest, ...current]);
    setForm(initialForm);
  }

  return (
    <main className="app-shell">
      <section className="hero">
        <div>
          <p className="eyebrow">Family Dollar AI Platform Demo</p>
          <h1>AI Governance Intake Portal</h1>
          <p className="hero-copy">
            Capture AI ideas from business teams, map them to retail systems,
            preview risk tiers, expose dependencies, and prepare each request
            for architecture review, governance forum triage, and controlled delivery.
          </p>
          <div className="hero-actions">
            <a href="#intake-form">Submit AI Request</a>
            <a href="#governance-dashboard" className="secondary-action">
              View Governance Queue
            </a>
          </div>
        </div>

        <aside className="hero-panel">
          <h2>Demo Narrative</h2>
          <p>
            This portal proves the operating model behind safe AI delivery:
            intake, risk tiering, dependency mapping, prioritization, release
            governance, and human approval before operational execution.
          </p>
        </aside>
      </section>

      <section id="governance-dashboard" className="stats-grid">
        <article className="stat-card">
          <span>Total AI Requests</span>
          <strong>{stats.total}</strong>
        </article>
        <article className="stat-card">
          <span>High-Risk Requests</span>
          <strong>{stats.highRisk}</strong>
        </article>
        <article className="stat-card">
          <span>Restricted Review</span>
          <strong>{stats.restricted}</strong>
        </article>
        <article className="stat-card">
          <span>Active Delivery Candidates</span>
          <strong>{stats.approved}</strong>
        </article>
      </section>

      <section className="content-grid">
        <form id="intake-form" className="intake-card" onSubmit={submitRequest}>
          <div className="section-heading">
            <p className="eyebrow">Governance Intake</p>
            <h2>New AI Use Case Request</h2>
          </div>

          <label>
            Business Unit
            <select
              value={form.businessUnit}
              onChange={(event) => updateForm("businessUnit", event.target.value)}
            >
              <option>Store Operations</option>
              <option>Customer Support</option>
              <option>Finance</option>
              <option>Marketing</option>
              <option>Supply Chain</option>
              <option>IT Support</option>
              <option>Merchandising</option>
            </select>
          </label>

          <label>
            Requester
            <input
              value={form.requester}
              onChange={(event) => updateForm("requester", event.target.value)}
              placeholder="Example: Regional Operations Director"
              required
            />
          </label>

          <label>
            Requested AI Use Case
            <textarea
              value={form.useCase}
              onChange={(event) => updateForm("useCase", event.target.value)}
              placeholder="Describe the AI capability, business problem, and desired outcome."
              required
            />
          </label>

          <div className="two-column">
            <label>
              Retail System Touched
              <select
                value={form.retailSystem}
                onChange={(event) => updateForm("retailSystem", event.target.value)}
              >
                <option>POS</option>
                <option>Inventory</option>
                <option>ERP</option>
                <option>CRM</option>
                <option>Supply Chain</option>
                <option>Identity</option>
                <option>ITSM</option>
              </select>
            </label>

            <label>
              Data Sensitivity
              <select
                value={form.dataSensitivity}
                onChange={(event) => updateForm("dataSensitivity", event.target.value)}
              >
                <option>Public</option>
                <option>Internal</option>
                <option>Confidential</option>
                <option>PII</option>
                <option>Payment</option>
              </select>
            </label>
          </div>

          <div className="checkbox-row">
            <label>
              <input
                type="checkbox"
                checked={form.customerData}
                onChange={(event) => updateForm("customerData", event.target.checked)}
              />
              Customer data involved
            </label>

            <label>
              <input
                type="checkbox"
                checked={form.paymentData}
                onChange={(event) => updateForm("paymentData", event.target.checked)}
              />
              Payment data involved
            </label>
          </div>

          <div className="two-column">
            <label>
              Operational Impact
              <select
                value={form.operationalImpact}
                onChange={(event) => updateForm("operationalImpact", event.target.value)}
              >
                <option>Internal productivity</option>
                <option>Back-office operations</option>
                <option>Store-level operations</option>
                <option>Customer-facing support</option>
                <option>Supply-chain operations</option>
                <option>Enterprise-critical operations</option>
              </select>
            </label>

            <label>
              Model Type
              <select
                value={form.modelType}
                onChange={(event) => updateForm("modelType", event.target.value)}
              >
                <option>RAG assistant</option>
                <option>Agentic workflow with retrieval</option>
                <option>Document intelligence</option>
                <option>Forecasting model</option>
                <option>Generative AI personalization</option>
                <option>Classification model</option>
              </select>
            </label>
          </div>

          <div className="two-column">
            <label>
              Autonomous Action Level
              <select
                value={form.autonomousActionLevel}
                onChange={(event) =>
                  updateForm("autonomousActionLevel", event.target.value)
                }
              >
                <option>Summarize only</option>
                <option>Recommend only</option>
                <option>Draft response</option>
                <option>Autonomous action</option>
              </select>
            </label>

            <label>
              Target Release Window
              <select
                value={form.targetReleaseWindow}
                onChange={(event) => updateForm("targetReleaseWindow", event.target.value)}
              >
                <option>Q3 prototype</option>
                <option>Q3 pilot</option>
                <option>Q4 controlled rollout</option>
                <option>Blocked pending governance</option>
                <option>Future roadmap candidate</option>
              </select>
            </label>
          </div>

          <label>
            Expected Business Value
            <textarea
              value={form.expectedBusinessValue}
              onChange={(event) =>
                updateForm("expectedBusinessValue", event.target.value)
              }
              placeholder="Example: reduce stockouts, improve customer support response time, reduce manual finance review."
              required
            />
          </label>

          <label>
            Dependencies
            <textarea
              value={form.dependencies}
              onChange={(event) => updateForm("dependencies", event.target.value)}
              placeholder="Example: Inventory API, Supply Chain API, Identity API, legal review"
            />
          </label>

          <label className="approval-toggle">
            <input
              type="checkbox"
              checked={form.humanApprovalRequired}
              onChange={(event) =>
                updateForm("humanApprovalRequired", event.target.checked)
              }
            />
            Human approval required before execution
          </label>

          <button type="submit">Submit to Governance Queue</button>
        </form>

        <aside className="risk-card">
          <div className="section-heading">
            <p className="eyebrow">Automated Risk Preview</p>
            <h2>{riskPreview.tier}</h2>
          </div>

          <p className="tier-description">{tierDescriptions[riskPreview.tier]}</p>

          <dl className="risk-factors">
            <div>
              <dt>Risk score</dt>
              <dd>{riskPreview.score}</dd>
            </div>
            <div>
              <dt>Human approval</dt>
              <dd>{riskPreview.humanApprovalRequired ? "Required" : "Optional"}</dd>
            </div>
            <div>
              <dt>Retail system</dt>
              <dd>{form.retailSystem}</dd>
            </div>
            <div>
              <dt>Autonomy</dt>
              <dd>{form.autonomousActionLevel}</dd>
            </div>
          </dl>

          <div className="policy-note">
            <strong>Governance rule:</strong> AI may recommend, summarize, or draft.
            Human or policy approval is required before operational execution,
            customer-impacting actions, payment-related use cases, or restricted release.
          </div>
        </aside>
      </section>

      <section className="queue-section">
        <div className="section-heading">
          <p className="eyebrow">Governance Forum Queue</p>
          <h2>AI Portfolio Intake</h2>
        </div>

        <div className="request-grid">
          {requests.map((request) => (
            <article key={request.id} className="request-card">
              <div className="request-header">
                <span>{request.id}</span>
                <strong className={`tier-badge ${request.riskTier.replace(" ", "-").toLowerCase()}`}>
                  {request.riskTier}
                </strong>
              </div>

              <h3>{request.useCase}</h3>
              <p>{request.expectedBusinessValue}</p>

              <div className="request-meta">
                <span>{request.businessUnit}</span>
                <span>{request.retailSystem}</span>
                <span>{request.status}</span>
              </div>

              <dl>
                <div>
                  <dt>Dependencies</dt>
                  <dd>{request.dependencies || "None listed"}</dd>
                </div>
                <div>
                  <dt>Release window</dt>
                  <dd>{request.targetReleaseWindow}</dd>
                </div>
                <div>
                  <dt>Owner team</dt>
                  <dd>{request.ownerTeam}</dd>
                </div>
              </dl>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}

export default App;
