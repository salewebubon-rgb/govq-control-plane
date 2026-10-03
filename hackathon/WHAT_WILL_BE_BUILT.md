# WHAT WILL BE BUILT DURING THE HACKATHON

## 1. Purpose

This document defines the significant new work planned for the Hackathon.

The event build is intentionally separated from the existing GOVQ Core.

The goal is not to rebuild the control plane.

The goal is to demonstrate a new real-world autonomous application that uses GOVQ to govern AI execution.

---

## 2. Hackathon Build Objective

The Hackathon objective is:

> **Build a real municipal E-Service workflow in which an AI agent can assist with a real operational task while GOVQ visibly controls evidence, policy, authority, human approval, execution, and auditability.**

The demonstration must show more than an AI response.

It must show governed action.

---

## 3. New Municipal E-Service Agent

A new municipal E-Service agent will be built during the event.

The reference use case is a public service request such as:

> A citizen reports a broken streetlight or similar municipal issue.

The new agent will assist with:

- understanding the request
- extracting structured information
- identifying the service category
- checking required evidence
- proposing the next workflow action
- preparing a governed action request

The agent itself will not own execution authority.

---

## 4. New Workflow Adapter

A new workflow adapter will connect the E-Service application to GOVQ.

The adapter will translate between:

- application request
- GOVQ execution contract
- AI proposal
- governance decision
- application action
- audit result

Reference:

```text
Municipal E-Service
        |
        v
Workflow Adapter
        |
        v
      GOVQ
        |
        v
Governed Decision
        |
        v
Workflow Adapter
        |
        v
Municipal Action
```

This adapter is a significant new integration component.

---

## 5. New Governed Action Integration

The Hackathon build will connect GOVQ decisions to a real application action.

Example protected actions may include:

- create service work item
- route case to responsible unit
- assign service category
- create officer task
- request missing information
- pause for approval

The important requirement is that the action occurs only after GOVQ returns an allowed execution state.

---

## 6. New ALLOW / DENY / REQUIRE APPROVAL Workflow

The new application will visibly demonstrate governance outcomes.

Reference decision states:

```text
ALLOW
DENY
REQUIRE_APPROVAL
INSUFFICIENT_EVIDENCE
```

Each state will produce a different operational behavior.

### ALLOW

The request satisfies the required conditions.

The application executes the permitted action.

### DENY

The requested action is not allowed.

No protected action occurs.

### REQUIRE_APPROVAL

The action is outside autonomous authority.

Execution pauses until an authorized human decides.

### INSUFFICIENT_EVIDENCE

Required information is missing.

The system requests additional evidence and does not execute the protected action.

---

## 7. New Human Approval Flow

A new operator approval flow will be created for the Hackathon use case.

Reference:

```text
AI Proposal
    |
    v
GOVQ
    |
    v
REQUIRE_APPROVAL
    |
    v
Authorized Officer
    |
    +--> APPROVE
    |
    +--> REJECT
```

The approval decision will be recorded as part of the same execution.

This demonstrates human control inside the live workflow.

---

## 8. New Cognitive Governance Dashboard

A Cognitive Governance Dashboard will be built during the event.

The dashboard will make the governed execution visible in real time.

It is expected to show information such as:

- execution ID
- tenant
- request
- evidence status
- policy applied
- authority decision
- model/provider
- approval status
- final decision
- action result
- audit receipt
- latency
- runtime health

The dashboard must reflect real runtime state.

It should not be a disconnected mock presentation.

---

## 9. New Execution Timeline

The dashboard will include a visible execution timeline.

Reference:

```text
REQUEST
   |
   v
EVIDENCE CHECK
   |
   v
POLICY MATCH
   |
   v
AUTHORITY CHECK
   |
   v
AI PROPOSAL
   |
   v
GOVERNANCE DECISION
   |
   v
ACTION / APPROVAL
   |
   v
AUDIT RECEIPT
```

Each step should visibly reflect runtime status.

Example states:

```text
PENDING
RUNNING
PASS
BLOCKED
APPROVAL REQUIRED
COMPLETED
```

---

## 10. New Live Audit Receipt

The event build will produce a visible audit receipt.

The receipt should connect the execution to:

- request ID
- execution ID
- tenant
- evidence
- policy
- authority
- provider
- approval state
- action
- outcome
- timestamp

The objective is to show that the action can be reconstructed after execution.

---

## 11. New Demo Scenario A — ALLOW

Scenario A demonstrates successful autonomous execution.

Example:

```text
Citizen submits:
- valid location
- clear issue description
- required evidence
```

Expected path:

```text
Request
  |
  v
Evidence Sufficient
  |
  v
Policy Valid
  |
  v
Authority Valid
  |
  v
ALLOW
  |
  v
Create Work Item
  |
  v
Audit Receipt
```

The dashboard should visibly show why the action was allowed.

---

## 12. New Demo Scenario B — INSUFFICIENT EVIDENCE

Scenario B demonstrates fail-closed behavior.

Example:

```text
Citizen:
"The streetlight is broken."
```

but no usable location is provided.

Expected path:

```text
Request
  |
  v
Evidence Check
  |
  v
INSUFFICIENT_EVIDENCE
  |
  v
No Protected Action
  |
  v
Request Missing Information
```

The AI must not invent the missing information.

---

## 13. New Demo Scenario C — HUMAN APPROVAL

Scenario C demonstrates human authority.

Expected path:

```text
AI Proposal
    |
    v
Authority Check
    |
    v
REQUIRE_APPROVAL
    |
    v
Authorized Officer
    |
    +--> APPROVE
    |
    +--> REJECT
```

If approved:

```text
Resume Execution
      |
      v
Real Action
      |
      v
Audit Receipt
```

If rejected:

```text
No Protected Action
      |
      v
Audit Receipt
```

---

## 14. New Runtime E2E Demonstration

The final Hackathon demonstration should run the complete path.

Reference:

```text
Citizen
  |
  v
Municipal E-Service
  |
  v
AI / Agent
  |
  v
GOVQ
  |
  v
Inference
  |
  v
Governed Decision
  |
  v
Human Approval / Authorized Action
  |
  v
Application Side Effect
  |
  v
Audit Receipt
  |
  v
Cognitive Governance Dashboard
```

The purpose is to prove runtime behavior, not only explain architecture.

---

## 15. New Application Experience

The Hackathon build should provide a user-facing experience suitable for live judging.

The main presentation surface should not be CLI alone.

The recommended presentation is:

```text
+----------------------+------------------------------+
| Municipal E-Service  | Cognitive Governance        |
|                      | Dashboard                    |
| Citizen Interaction  | Runtime Governance Evidence |
+----------------------+------------------------------+
```

CLI and engineering tools remain available for technical inspection.

---

## 16. New Governed Tool Execution

The Hackathon build should demonstrate at least one protected tool or application action.

The action must not execute directly from the LLM.

Correct path:

```text
AI Proposal
    |
    v
GOVQ
    |
    v
Authorized Tool
    |
    v
Action
```

This provides a concrete demonstration of Tool Authority.

---

## 17. New Zero-Bypass Demonstration

The event build should make the protected path explicit.

The demonstration should establish that:

- the LLM cannot directly execute the protected action
- the application cannot bypass GOVQ for the protected action
- approval-required actions cannot continue without approval

The expected rule is:

> **No governed decision, no protected action.**

---

## 18. New Significant Build Components

The significant new Hackathon work is expected to include:

- municipal E-Service agent
- workflow adapter
- governed action integration
- tool/action authority integration
- human approval workflow
- runtime execution timeline
- Cognitive Governance Dashboard
- live audit receipt
- Hackathon-specific acceptance tests
- live E2E integration
- presentation-ready demo flow

This represents substantial new engineering work on top of the existing GOVQ foundation.

---

## 19. What Will NOT Be Rebuilt

The Hackathon build will not intentionally recreate existing GOVQ foundation work.

The event is not intended to rebuild:

- core governance philosophy
- provider abstraction
- existing evidence concepts
- existing policy concepts
- existing authorization model
- existing audit model
- existing runtime qualification approach
- existing self-hosted inference foundation

These are pre-existing project components.

---

## 20. Hackathon Build Boundary

The boundary can be summarized as:

```text
BEFORE EVENT
------------
GOVQ Core
Governance Architecture
Evidence
Policy
Authorization
Audit
Provider Abstraction
Runtime Qualification
Self-hosted Inference

            +
            |
            v

DURING EVENT
------------
Municipal E-Service Agent
Workflow Adapter
Governed Action Integration
Human Approval Flow
Cognitive Governance Dashboard
Live Audit Receipt
Runtime E2E Demo
```

---

## 21. Acceptance Criteria

The Hackathon build should be considered successful when the live system can demonstrate:

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

These criteria define the target event profile.

---

## 22. Judging Experience

The final demonstration should allow a reviewer to understand within a short period:

1. What did the citizen request?
2. What did the AI understand?
3. What evidence was available?
4. Which policy applied?
5. Did the AI have authority?
6. Was human approval required?
7. What action occurred?
8. Can the action be audited?

This is the intended competitive advantage of the demonstration.

---

## 23. Significant New Work Statement

The Hackathon contribution can be summarized as:

> **The event-day build transforms an existing governed AI control plane into a new real-world autonomous municipal E-Service experience with visible governance, human control, real action, and auditable execution.**

The event build is not a cosmetic wrapper around existing work.

It is a substantial new application and execution integration built on top of the existing GOVQ foundation.

---

## 24. Final Build Statement

The Hackathon goal is not:

> Build another AI agent that can complete a task.

The Hackathon goal is:

> **Build an autonomous AI application that can complete a real task while the organization remains visibly and technically in control.**
