# GOVQ — Governed AI Control Plane

**Governed execution for autonomous AI systems.**

GOVQ is a governed AI control plane designed to keep organizations in control of what AI can see, decide, and do.

> **LLM proposes. GOVQ authorizes. The application executes.**

---

## Why GOVQ

Connecting an application to an AI model is easy.

The harder problem begins when AI is allowed to work with:

- real organizational data
- real users
- real workflows
- real tools
- real operational actions

Before an AI-assisted action is allowed to proceed, an organization should be able to answer:

- What data was used?
- What evidence supported the decision?
- Which policy applied?
- Was the action authorized?
- Was human approval required?
- What action occurred?
- Can the execution be reconstructed afterwards?

GOVQ places these controls directly in the execution path.

---

## Core Idea

```text
User / Application
        |
        v
    AI / Agent
        |
        | proposes
        v
      GOVQ
        |
        | governs
        v
ALLOW / DENY / REQUIRE APPROVAL
        |
        v
Authorized Application / Tool
        |
        | executes
        v
   Real-World Action
        |
        v
    Audit Receipt
```

The AI model is not the authority boundary.

GOVQ is the governance boundary.

The application or authorized tool remains the execution boundary.

---

## Governance Model

GOVQ is organized around six primary controls:

1. **Data Control** — Controls what information may be exposed to AI.
2. **Evidence Control** — Determines whether supporting information is sufficient and traceable.
3. **Policy Control** — Binds execution to explicit organizational rules.
4. **Authority Control** — Determines whether the proposed action is permitted.
5. **Human Control** — Requires authorized human approval when autonomous authority is insufficient.
6. **Audit Control** — Makes the execution reconstructable after the action.

Detailed governance documentation:

- [`docs/03-governance-model.md`](docs/03-governance-model.md)

---

## Architecture

```text
Existing Application / E-Service
            |
            v
        GOVQ Gateway
            |
            v
      GOVQ Control Plane
            |
    +-------+--------+
    |       |        |
 Evidence  Policy  Authority
    |       |        |
    +-------+--------+
            |
      Human Approval
            |
            v
     Inference Layer
   Self-hosted / Cloud
            |
            v
      AI Proposal
            |
            v
     GOVQ Decision
            |
            v
Authorized Application / Tool
            |
            v
       Real Action
            |
            v
       Audit Receipt
```

The inference provider is replaceable. Governance remains independent of the model vendor.

Detailed architecture:

- [`docs/02-architecture.md`](docs/02-architecture.md)

---

## Legacy Application Integration

GOVQ is designed to work with existing applications without forcing organizations to rebuild their entire system.

```text
Existing App A ---\
Existing App B ----+----> GOVQ ----> Shared Inference
Existing App C ---/
```

Each application or organization can retain its own:

- data
- policy
- domain knowledge
- permissions
- operational authority
- audit boundary

Shared infrastructure does not imply shared governance authority.

---

## Self-Hosted and Cloud Inference

GOVQ can work with:

- self-hosted language models
- private inference services
- cloud LLM providers
- future model providers

Self-hosted inference can provide:

- predictable infrastructure cost
- centralized model management
- reduced dependence on per-token external API billing
- greater control over the inference environment

The inference model remains a reasoning component. It does not become the governance authority.

---

## Decision States

Reference GOVQ decision states include:

```text
ALLOW
DENY
REQUIRE_APPROVAL
INSUFFICIENT_EVIDENCE
```

These states are governance outcomes, not model opinions.

---

## Fail-Closed and Zero-Bypass

### Fail-Closed

```text
Uncertain State
      |
      v
Fail Closed
      |
      v
No Protected Action
```

### Zero-Bypass

Correct:

```text
AI Proposal
    |
    v
GOVQ
    |
    v
Authorized Tool
```

Incorrect:

```text
AI --------> Protected Tool
```

without the governed execution path.

---

## Visible Governance

The planned **Cognitive Governance Dashboard** is intended to expose runtime information such as:

- execution ID
- evidence status
- policy applied
- authority decision
- provider/model
- approval state
- final decision
- action result
- audit receipt
- latency
- runtime health

Engineering evidence and operational evidence should refer to the same execution.

---

## Current Status

- GOVQ Core architecture: Active development
- Governance contracts: Active development and qualification
- Evidence and policy mechanisms: Available in current architecture
- Provider abstraction: Available
- Self-hosted inference path: Available
- Cloud inference path: Optional
- Runtime qualification infrastructure: Active
- Governed action execution: Under development
- Human approval workflow: Under development
- Cognitive Governance Dashboard: Planned
- Municipal E-Service integration: Planned Hackathon build

Status descriptions in this repository represent the current public project state and should not be interpreted as production certification.

---

## Regional Codex Hackathon

GOVQ is being prepared as an existing governed AI foundation for a new real-world autonomous application build.

### Existing Before the Event

- GOVQ Core architecture
- governance contracts
- evidence and policy mechanisms
- authorization model
- audit and provenance model
- provider abstraction
- runtime qualification infrastructure
- self-hosted inference support
- existing Chat and Kiosk AI application experience

### Planned Significant New Build During the Event

- autonomous municipal E-Service agent
- workflow adapter
- governed action integration
- human approval flow
- Cognitive Governance Dashboard
- live execution trace
- live audit receipt
- end-to-end runtime demonstration

Hackathon boundary documentation:

- [`hackathon/WHAT_EXISTS_BEFORE.md`](hackathon/WHAT_EXISTS_BEFORE.md)
- [`hackathon/WHAT_WILL_BE_BUILT.md`](hackathon/WHAT_WILL_BE_BUILT.md)
- [`hackathon/DEMO_SCENARIOS.md`](hackathon/DEMO_SCENARIOS.md)

---

## Documentation

- [`docs/01-problem.md`](docs/01-problem.md) — real-world problem definition
- [`docs/02-architecture.md`](docs/02-architecture.md) — execution architecture
- [`docs/03-governance-model.md`](docs/03-governance-model.md) — six governance controls
- [`docs/04-evolution.md`](docs/04-evolution.md) — architectural evolution

---

## Examples

- [`examples/sample-request.json`](examples/sample-request.json)
- [`examples/sample-decision.json`](examples/sample-decision.json)
- [`examples/sample-receipt.json`](examples/sample-receipt.json)

These examples are illustrative public contracts and do not expose the private production implementation.

---

## Repository Purpose

This repository is a **public technical evidence package** for GOVQ.

It is intended to contain:

- architecture documentation
- governance documentation
- public execution examples
- selected technical evidence
- Hackathon build boundaries
- demo scenarios

The production GOVQ Core remains in a private repository.

This public repository must not contain:

- API keys
- secrets
- credentials
- private customer information
- production databases
- private source code
- sensitive operational configuration
- internal vulnerability details

---

## Public Repository Boundary

This repository documents GOVQ engineering architecture and selected public evidence.

It does not publish the complete private GOVQ implementation.

The public boundary exists to demonstrate technical direction, architecture, execution contracts, and selected evidence while protecting sensitive implementation details and operational data.

---

## Project Direction

GOVQ is being developed as a reusable governed AI control plane for applications that need more than AI-generated answers.

The long-term direction is to support AI systems that can reason and act while keeping organizations in control of:

**data, evidence, policy, authority, approval, execution, and accountability.**

> **AI may reason. GOVQ governs. The organization remains in control.**
