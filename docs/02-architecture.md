# GOVQ Architecture

## 1. Purpose

GOVQ is designed as an AI-native governed execution control plane.

Its purpose is not to replace the application, the language model, or the organization's operational system.

Its purpose is to control how AI participates in real execution.

The architecture is based on one core principle:

> **LLM proposes. GOVQ authorizes. The application executes.**

This creates a clear separation between:

- AI reasoning
- governance
- execution authority
- operational action
- auditability

GOVQ is therefore positioned between autonomous AI capability and real-world execution.

## 2. High-Level Architecture

```text
User / Citizen / Operator
          |
          v
Existing Application / E-Service
          |
          | Governed Request
          v
      GOVQ Gateway
          |
          v
   GOVQ Control Plane
          |
          +--> Data Control
          +--> Evidence Control
          +--> Policy Control
          +--> Authority Control
          +--> Human Approval
          +--> Audit / Provenance
          |
          v
    Inference Layer
          |
          +--> Self-hosted LLM
          +--> Cloud LLM
          |
          v
    AI Proposal / Result
          |
          v
    GOVQ Final Decision
          |
          +--> ALLOW
          +--> DENY
          +--> REQUIRE APPROVAL
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

The AI model is not the authority boundary.

The GOVQ control plane is the governance boundary.

The application or authorized tool remains the execution boundary.

## 3. Architectural Separation

GOVQ separates the system into distinct responsibility layers.

### 3.1 Application Layer

The application is the real operational system.

Examples include:

- municipal E-Service
- school information system
- internal administrative system
- customer service portal
- IoT gateway
- business workflow
- legacy PHP/MySQL application

The application owns:

- user interaction
- business records
- operational data
- domain workflow
- final tool invocation
- real-world side effects

GOVQ does not need to replace the application.

### 3.2 GOVQ Gateway

The gateway is the controlled entry point into the GOVQ platform.

Its responsibilities may include:

- tenant identification
- request authentication
- request contract validation
- request normalization
- rate limiting
- correlation ID assignment
- execution ID creation
- request routing

```text
Application
    |
    v
GOVQ Gateway
    |
    +--> Authenticate
    +--> Identify Tenant
    +--> Validate Contract
    +--> Create Execution Context
    |
    v
GOVQ Control Plane
```

The gateway should not grant execution authority.

It prepares and validates the request before governance evaluation.

## 4. GOVQ Control Plane

The control plane is the core governance layer.

It determines whether AI-assisted execution is allowed to proceed.

### 4.1 Data Control

Data Control determines what information may be exposed to the AI system.

Responsibilities may include:

- data minimization
- PII filtering
- sensitive-field masking
- tenant boundary enforcement
- context selection
- provider exposure rules

```text
Application Data
      |
      v
Data Control
      |
      +--> Allowed Context
      +--> Redacted Context
      +--> Blocked Data
```

The AI should receive only the information required for the task.

### 4.2 Evidence Control

Evidence Control determines whether the information supporting a decision is sufficient and traceable.

Responsibilities may include:

- retrieval validation
- source identification
- evidence sufficiency checks
- evidence digest generation
- provenance binding
- missing-information detection

```text
Request
   |
   v
Evidence Retrieval
   |
   v
Evidence Validation
   |
   +--> SUFFICIENT
   +--> INSUFFICIENT
```

If required evidence is missing, the system should not continue by guessing.

### 4.3 Policy Control

Policy Control determines which organizational rule applies.

Responsibilities may include:

- policy lookup
- policy snapshot selection
- policy version binding
- policy decision input creation
- decision trace recording

```text
Tenant
  |
  v
Applicable Policy
  |
  v
Policy Snapshot
  |
  v
Governed Execution
```

An AI action should be explainable in relation to an identifiable rule or policy state.

### 4.4 Authority Control

Authority Control determines whether the proposed action is inside the allowed scope.

Responsibilities may include:

- action allowlists
- tool allowlists
- argument constraints
- role-based authority
- service-level authority
- capability limits
- action risk classification

```text
AI Proposal
    |
    v
Authority Check
    |
    +--> Authorized
    +--> Not Authorized
```

The model may propose an action.

It does not grant itself authority.

### 4.5 Human Approval

Human Approval is used when autonomous authority is insufficient.

Responsibilities may include:

- pause execution
- request approval
- identify authorized approver
- approve or reject
- resume or terminate execution
- record the approval decision

```text
AI Proposal
    |
    v
Authority Check
    |
    v
REQUIRE APPROVAL
    |
    v
Authorized Human
    |
    +--> APPROVE
    +--> REJECT
```

Human approval is part of the execution record.

### 4.6 Audit and Provenance

Audit and Provenance record how the execution occurred.

A complete execution should be able to connect:

- request
- tenant
- evidence
- policy
- provider
- AI proposal
- governance decision
- approval
- action
- outcome

```text
execution_id
    |
    +--> request
    +--> evidence
    +--> policy
    +--> authority
    +--> provider
    +--> approval
    +--> action
    +--> receipt
```

The objective is reconstructability.

## 5. Inference Layer

The inference layer performs AI reasoning.

It may contain:

- self-hosted LLM
- local inference server
- private model service
- commercial cloud LLM
- future model provider

```text
GOVQ Control Plane
        |
        v
Provider Abstraction
        |
        +--> Self-hosted Qwen
        +--> Cloud Provider
        +--> Future Provider
```

GOVQ should not be tightly coupled to a single model vendor.

The model provider is replaceable.

The governance layer remains.

## 6. Self-Hosted Inference Architecture

```text
Legacy App A ---\
Legacy App B ----+----> GOVQ ----> Self-hosted LLM
Legacy App C ---/
```

This allows multiple existing applications to use a shared AI infrastructure.

Potential advantages include:

- predictable infrastructure cost
- centralized model management
- centralized capacity management
- reduced dependence on external per-token billing
- stronger control over inference infrastructure
- simplified adoption for legacy applications

The self-hosted model remains an inference component.

It is not the governance authority.

## 7. Control Plane and Inference Plane Separation

Even when both initially run on the same physical server, they remain separate architectural responsibilities.

```text
+-----------------------------+
|      GOVQ CONTROL PLANE     |
|                             |
| Evidence                    |
| Policy                      |
| Authority                   |
| Approval                    |
| Audit                       |
+-------------+---------------+
              |
              | Provider Contract
              v
+-----------------------------+
|       INFERENCE PLANE       |
|                             |
| Self-hosted LLM             |
| Cloud LLM                   |
| Future Provider             |
+-----------------------------+
```

This separation allows the inference layer to change without redesigning governance.

## 8. Execution Boundary

The most important execution rule is:

> **The AI model does not directly own real-world action authority.**

Correct flow:

```text
AI proposes
    |
    v
GOVQ evaluates
    |
    v
Governed Decision
    |
    v
Authorized Application / Tool
    |
    v
Real Action
```

Incorrect flow:

```text
AI
 |
 v
Direct Production Action
```

The application or authorized tool remains responsible for performing the actual side effect.

## 9. Decision States

Core decision states include:

```text
ALLOW
DENY
REQUIRE_APPROVAL
INSUFFICIENT_EVIDENCE
```

### ALLOW

The request satisfies required evidence, policy, and authority conditions.

### DENY

The request is not permitted.

### REQUIRE_APPROVAL

The request cannot be executed autonomously.

### INSUFFICIENT_EVIDENCE

The system does not have enough verified information to continue safely.

## 10. Canonical Execution Flow

```text
1. Receive Request
        |
        v
2. Identify Tenant
        |
        v
3. Validate Request Contract
        |
        v
4. Apply Data Controls
        |
        v
5. Retrieve / Validate Evidence
        |
        v
6. Bind Policy
        |
        v
7. Build Governed Context
        |
        v
8. Invoke Inference Provider
        |
        v
9. Receive AI Proposal
        |
        v
10. Validate Proposal
        |
        v
11. Check Authority
        |
        +--> DENY
        +--> REQUIRE_APPROVAL
        +--> ALLOW
                |
                v
12. Authorized Application Executes
                |
                v
13. Record Outcome
                |
                v
14. Generate Audit Receipt
```

Every real-world action should be traceable through this path.

## 11. Fail-Closed Principle

GOVQ should fail closed when execution safety cannot be established.

Examples include:

- missing evidence
- invalid policy snapshot
- unauthorized action
- provider failure
- malformed model output
- uncertain tool result
- missing approval
- tenant mismatch
- invalid execution state

```text
Uncertain State
      |
      v
Fail Closed
      |
      v
No Protected Action
```

The system should prefer no action over an ungoverned action.

## 12. Tool Authority

Tool execution should be governed by:

- tool registration
- tool allowlist
- tenant scope
- role scope
- argument constraints
- execution policy
- retry policy
- timeout policy
- audit requirements

```text
AI Proposal
    |
    v
Tool Request
    |
    v
GOVQ Tool Authority
    |
    +--> ALLOW
    +--> DENY
    +--> REQUIRE APPROVAL
```

The tool layer should never become a bypass around GOVQ.

## 13. Zero-Bypass Principle

Protected actions must not bypass the control plane.

Correct:

```text
Application
    |
    v
GOVQ
    |
    v
Authorized Tool
```

Incorrect:

```text
Application
    |
    +------------------> Tool
```

or:

```text
LLM
 |
 +---------------------> Tool
```

This is the basis of Zero-Bypass qualification.

## 14. Multi-Tenant Architecture

```text
Tenant A Application ---\
Tenant B Application ----+----> GOVQ Control Plane
Tenant C Application ---/              |
                                        v
                                Shared Inference
```

Tenant-specific controls may include:

- tenant ID
- policy namespace
- knowledge namespace
- permission namespace
- credential boundary
- audit partition
- provider configuration
- rate limits
- execution quotas

Shared infrastructure must not imply shared authority.

## 15. Legacy Web Integration

```text
+----------------------------------+
| Legacy Hosting                   |
|                                  |
| Existing Website                 |
| Standalone E-Service             |
| MySQL                            |
+----------------+-----------------+
                 |
                 | HTTPS
                 v
+----------------------------------+
| GOVQ Cloud Platform              |
|                                  |
| GOVQ Gateway                     |
| GOVQ Control Plane               |
| Audit / Governance               |
| Provider Abstraction             |
| Self-hosted Inference            |
+----------------------------------+
```

The customer application does not need to host:

- Docker
- LLM runtime
- GPU
- model weights
- governance engine

The application only needs a governed API integration.

## 16. Reference Municipal E-Service Architecture

```text
Citizen
   |
   v
Municipal E-Service
   |
   | Request
   v
GOVQ Gateway
   |
   v
GOVQ Control Plane
   |
   +--> Data Check
   +--> Evidence Check
   +--> Policy Check
   +--> Authority Check
   +--> Human Approval
   |
   v
Inference Provider
   |
   v
AI Proposal
   |
   v
GOVQ Decision
   |
   +--> DENY
   +--> INSUFFICIENT_EVIDENCE
   +--> REQUIRE_APPROVAL
   +--> ALLOW
           |
           v
Municipal E-Service
           |
           v
Create / Route Work Item
           |
           v
Audit Receipt
```

The E-Service remains the system performing the operational action.

GOVQ controls whether execution is allowed.

## 17. Cognitive Governance Dashboard Architecture

The Cognitive Governance Dashboard is an observability and explainability surface for governed execution.

```text
GOVQ Runtime
    |
    +--> Execution Events
    +--> Evidence State
    +--> Policy State
    +--> Authority State
    +--> Approval State
    +--> Action State
    +--> Audit State
             |
             v
Cognitive Governance Dashboard
```

The dashboard may display:

- execution ID
- tenant
- request
- evidence status
- policy applied
- authority decision
- provider / model
- human approval status
- final decision
- action result
- audit receipt
- latency
- runtime health

The dashboard should reflect real runtime state.

## 18. Engineering Evidence and Operational Evidence

### Engineering Evidence

Examples:

- CLI output
- qualification harness
- contract tests
- runtime probes
- zero-bypass tests
- fail-closed tests
- source review

### Operational Evidence

Examples:

- governance timeline
- evidence state
- policy binding
- authority result
- approval state
- action result
- audit receipt

Both forms of evidence should refer to the same execution.

## 19. Runtime Qualification Boundary

The architecture should be considered qualified only when the full execution path has been validated.

```text
Request
  |
  v
Gateway
  |
  v
Governance
  |
  v
Inference
  |
  v
Decision
  |
  v
Authorized Action
  |
  v
Audit Receipt
```

Passing isolated unit tests is not sufficient to prove the entire governed execution path.

## 20. Hackathon Architecture Profile

The Hackathon profile should demonstrate:

- one real application
- one governed execution path
- self-hosted or selected inference provider
- evidence validation
- policy binding
- authority checking
- human approval
- real action
- audit receipt
- Cognitive Governance Dashboard
- runtime E2E evidence

Reference acceptance profile:

```text
Provider Authority        PASS
Evidence Control          PASS
Policy Binding            PASS
Tool Authority            PASS
Action Authorization      PASS
Human Approval            PASS
Audit Receipt             PASS
Zero-Bypass               PASS
Runtime E2E               PASS
```

## 21. Future Production Extensions

Future production architecture may add:

- multi-tenant administration
- tenant provisioning
- rate limiting
- job queues
- inference scheduling
- horizontal inference workers
- provider failover
- usage metering
- billing
- multi-region deployment
- advanced observability
- disaster recovery
- policy management UI
- knowledge management UI
- credential vault
- enterprise IAM
- device gateways
- IoT and Physical AI integration

These are extensions of the architecture.

They are not required to prove the core governed execution model.

## 22. Architectural Principles

The GOVQ architecture follows these principles:

1. **Governance is in the execution path.**
2. **The model is not the authority boundary.**
3. **Reasoning and execution authority are separated.**
4. **Evidence is required before protected action.**
5. **Policy is explicit and identifiable.**
6. **Authority is evaluated before execution.**
7. **Human approval is a first-class execution state.**
8. **Protected actions fail closed.**
9. **Every protected action is auditable.**
10. **Legacy applications can integrate without full replacement.**
11. **The inference provider is replaceable.**
12. **Shared infrastructure must preserve tenant isolation.**
13. **Runtime evidence is more important than architecture claims alone.**
14. **The same governed execution should be visible to engineers and operators.**

## 23. Architecture Summary

```text
Application
    |
    v
AI / Agent
    |
    | proposes
    v
GOVQ Control Plane
    |
    | governs
    v
Decision
    |
    | authorizes
    v
Application / Tool
    |
    | executes
    v
Real-World Action
    |
    v
Audit Receipt
```

The fundamental architectural statement is:

> **AI may reason.  
> GOVQ governs.  
> The organization remains in control.**
