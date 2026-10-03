# GOVQ

**AI-native governed execution core for autonomous AI systems.**

GOVQ is designed to keep organizations in control of what AI can see, decide, and do.

## Why GOVQ

Connecting an application to an AI model or API is easy.

The harder problem begins when AI is allowed to work with real data, real systems, real users, and real-world actions.

Before an AI system is allowed to perform a real action, an organization should be able to answer:

- What information was sent to the AI?
- What evidence did the AI rely on?
- Which policy applied?
- Was the AI authorized to perform the action?
- Was human approval required?
- Can the action be audited afterwards?

GOVQ places these controls directly in the AI execution path.

## Core Idea

```text
User / Application
        |
        v
    AI / Agent
        |
        v
      GOVQ
   /   |   \
Evidence Policy Authority
   \   |   /
 Human Approval
        |
        v
   Real Action
        |
        v
  Audit Receipt
```

> GOVQ does not give AI authority.  
> GOVQ gives organizations authority over AI.

## Execution Principle

GOVQ separates AI reasoning from execution authority.

```text
LLM / Agent proposes
        |
        v
GOVQ evaluates
        |
        +--> Evidence
        +--> Policy
        +--> Authority
        +--> Human Approval
        +--> Safety / Privacy
        |
        v
ALLOW / DENY / REQUIRE APPROVAL
        |
        v
Authorized application or tool executes
        |
        v
Audit Receipt
```

**LLM proposes. GOVQ authorizes. The application executes.**

## Governance Model

GOVQ is designed around six governance controls:

1. **Data Control**  
   Control what information may be exposed to AI and minimize unnecessary data transfer.

2. **Evidence Control**  
   Determine whether the information supporting an AI decision is sufficient and traceable.

3. **Policy Control**  
   Bind AI-assisted decisions to explicit organizational policies and rules.

4. **Authority Control**  
   Determine which actions an AI system is permitted to propose or perform.

5. **Human Control**  
   Require human approval when an action exceeds autonomous authority or reaches a defined risk threshold.

6. **Audit Control**  
   Record execution evidence, decisions, approvals, actions, and outcomes so the workflow can be reviewed afterwards.

## Current Architecture

GOVQ is designed as a model-agnostic control plane.

Self-hosted or cloud-hosted models may perform reasoning, classification, extraction, generation, or planning, but real-world execution must pass governance controls before an authorized application or tool is allowed to act.

High-level architecture:

```text
Legacy Website / Application
            |
            | HTTPS / API
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
      Governed Decision
            |
            v
 Authorized Application
       or Tool Action
            |
            v
       Audit Receipt
```

## Legacy Application Integration

GOVQ is intended to work with existing applications without requiring organizations to rebuild their entire system.

A legacy website or standalone E-Service can remain on its existing hosting environment while calling GOVQ through a governed API.

```text
Existing Application A ---\
Existing Application B ----+----> GOVQ ----> Shared Inference
Existing Application C ---/
```

Each organization can retain its own:

- data
- domain knowledge
- policy
- permissions
- business logic
- operational authority
- audit boundary

The shared governance infrastructure does not imply shared organizational policy.

## Self-Hosted Inference

GOVQ can work with self-hosted language models as well as external model providers.

For deployments where predictable infrastructure cost, data control, and reduced dependency on per-token external API billing are important, a centrally managed self-hosted model can be used as the inference layer.

The inference model is not the authority boundary.

GOVQ remains responsible for governance decisions around evidence, policy, authorization, approval, and audit.

## Trust Through Visible Evidence

A successful AI action is not enough.

Organizations also need to understand and verify:

- why the action was allowed
- which evidence supported it
- which policy was applied
- whether the AI had authority
- whether a human approved it
- what action was executed
- whether the result can be reconstructed later

GOVQ is designed so that governance evidence can be exposed through a **Cognitive Governance Dashboard**, not only hidden inside technical logs.

## Runtime Proof

The project prioritizes end-to-end runtime evidence rather than architecture diagrams alone.

Qualification and demonstration are expected to cover the complete execution path:

```text
Request
  |
  v
Evidence Check
  |
  v
Policy Evaluation
  |
  v
Authority Check
  |
  v
AI Reasoning
  |
  v
Governed Decision
  |
  +--> DENY
  |
  +--> REQUIRE HUMAN APPROVAL
  |
  +--> ALLOW
          |
          v
      Real Action
          |
          v
      Audit Receipt
```

CLI tests and qualification harnesses provide technical evidence.

The Cognitive Governance Dashboard is intended to make the same governed execution understandable to operators, users, and reviewers.

## Current Status

- GOVQ Core: Active development
- Governance contracts: Active development and qualification
- Evidence and policy mechanisms: Available in the current architecture
- Provider abstraction: Available
- Self-hosted LLM path: Available
- Cloud LLM path: Optional
- Runtime qualification infrastructure: Active
- Governed action execution: Under development
- Human approval workflow: Under development
- Cognitive Governance Dashboard: Planned
- Real-world E-Service integration: Planned Hackathon build

Status labels in this repository describe the current public project state and should not be interpreted as production certification.

## Regional Codex Hackathon

GOVQ is being prepared as an existing technical foundation for a real-world governed AI build.

### Existing Before the Event

The current project foundation includes:

- GOVQ Core architecture
- governance contracts
- evidence mechanisms
- policy mechanisms
- authorization model
- audit and provenance model
- provider abstraction
- runtime and qualification infrastructure
- self-hosted inference support
- existing AI application experience including Chat and Kiosk workloads

### Planned Hackathon Build

The planned significant new build during the Hackathon includes:

- autonomous municipal E-Service agent
- real-world workflow adapter
- governed action integration
- Cognitive Governance Dashboard
- ALLOW / DENY / HUMAN APPROVAL workflow
- live execution trace
- live audit receipt
- end-to-end production-like demonstration

The goal is not to rebuild GOVQ during the event.

The goal is to demonstrate how an existing governed execution core can enable autonomous AI to work with a real-world application safely, visibly, and accountably.

## Demo Direction

The reference demonstration uses a municipal E-Service workflow.

Example scenarios:

### Scenario A — ALLOW

A citizen submits a sufficiently complete service request.

GOVQ verifies the required evidence and policy, confirms that the requested action is within authorized scope, and allows the E-Service application to create the work item.

### Scenario B — INSUFFICIENT EVIDENCE

A request is missing required information.

GOVQ blocks execution and requests the missing information instead of allowing the agent to guess or act without sufficient evidence.

### Scenario C — HUMAN APPROVAL

A proposed action exceeds autonomous authority.

GOVQ pauses execution, requires approval from an authorized human operator, and resumes only after the approval decision is recorded.

## Cognitive Governance Dashboard

The dashboard is intended to expose live governed execution using information such as:

- execution ID
- tenant
- request or mission
- evidence status
- policy applied
- authority decision
- model or provider
- human approval status
- final decision
- action result
- audit receipt
- latency and runtime health

Its purpose is to make governance observable and understandable, while lower-level CLI and qualification evidence remain available for deeper technical review.

## Design Principles

GOVQ follows several core principles:

- **Governance in the execution path**
- **Model-agnostic architecture**
- **Evidence before action**
- **Explicit authority boundaries**
- **Human approval where required**
- **Fail-closed behavior for uncertain execution**
- **Traceable decisions and actions**
- **Legacy-system compatibility**
- **Separation of reasoning from authority**
- **Reusable governance across multiple applications**

## Repository Purpose

This public repository is a technical evidence package for GOVQ.

It is intended to contain:

- public architecture documentation
- governance model documentation
- selected diagrams
- sample contracts
- sample requests and decisions
- qualification summaries
- selected runtime evidence
- Hackathon build boundaries
- Hackathon demo scenarios

The production GOVQ Core remains in a private repository.

This repository must not contain:

- API keys
- secrets
- credentials
- private customer information
- production databases
- private source code
- internal vulnerability details
- sensitive operational configuration

## Repository Structure

```text
govq-public/
├── README.md
├── assets/
├── diagrams/
├── docs/
├── evidence/
├── examples/
└── hackathon/
```

## Development Boundary

The public repository documents the architecture and selected technical evidence.

Private production implementation remains separate.

This separation allows GOVQ to demonstrate technical maturity and runtime evidence without exposing sensitive implementation details, customer information, or production credentials.

## Project Direction

GOVQ is being developed as a reusable governed AI control plane for applications that need more than AI-generated answers.

The long-term direction is to support AI systems that can reason and act while keeping organizations in control of:

**data, evidence, policy, authority, approval, execution, and accountability.**
