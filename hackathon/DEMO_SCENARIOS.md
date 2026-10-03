# GOVQ Hackathon Demo Scenarios

## 1. Purpose

This document defines the reference demo scenarios for the GOVQ Hackathon build.

The scenarios are designed to demonstrate that GOVQ does more than produce AI responses.

The system must show how AI-assisted actions are governed through:

- evidence
- policy
- authority
- human approval
- execution control
- auditability

The three required demonstration paths are:

1. **ALLOW**
2. **INSUFFICIENT_EVIDENCE**
3. **HUMAN_APPROVAL**

These scenarios should run through the same GOVQ execution path and should be observable through the Cognitive Governance Dashboard.

---

## 2. Reference Use Case

The reference application is a municipal E-Service.

Example citizen request:

> A citizen reports a broken public streetlight.

The system may receive:

- text description
- location
- photo or supporting evidence
- service category
- requester information
- jurisdiction context

The AI may assist with:

- interpreting the request
- extracting structured data
- classifying the issue
- checking relevant knowledge
- proposing the next action

However, the AI does not own execution authority.

GOVQ determines whether the proposed action may proceed.

---

## 3. Common Runtime Path

All scenarios should use the same canonical runtime path.

```text
Citizen Request
      |
      v
Municipal E-Service
      |
      v
Workflow Adapter
      |
      v
GOVQ Gateway
      |
      v
Data Control
      |
      v
Evidence Control
      |
      v
Policy Control
      |
      v
Inference / AI Proposal
      |
      v
Authority Control
      |
      +--> ALLOW
      |
      +--> INSUFFICIENT_EVIDENCE
      |
      +--> REQUIRE_APPROVAL
      |
      +--> DENY
      |
      v
Authorized Application Action
      |
      v
Audit Receipt
```

The protected application action must not bypass GOVQ.

---

# Scenario A — ALLOW

## 4. Scenario Goal

Demonstrate successful autonomous execution when:

- required evidence is present
- applicable policy is valid
- proposed action is inside autonomous authority
- no human approval is required

Expected decision:

```text
ALLOW
```

---

## 5. Example Citizen Input

Example request:

> "The streetlight in front of Building 4 on Municipal Road 3 has been out since last night. I attached a photo and pinned the location."

Example structured input:

```json
{
  "service_type": "streetlight_issue",
  "description": "Streetlight is not working.",
  "location": "Building 4, Municipal Road 3",
  "photo_attached": true,
  "requester_contact": "available"
}
```

The exact runtime contract may differ.

This document defines the expected behavior rather than the production schema.

---

## 6. Expected Evidence State

Required evidence is present.

Example:

```text
Location            PASS
Issue Description   PASS
Service Category    PASS
Supporting Photo    PASS
Jurisdiction        PASS
```

Expected GOVQ evidence result:

```text
SUFFICIENT
```

---

## 7. Expected Policy State

The request matches an existing municipal service policy.

Example:

```text
Policy:
Streetlight Maintenance Request

Policy State:
VALID

Action Allowed:
Create maintenance work item
```

Expected policy result:

```text
POLICY_MATCH
```

---

## 8. Expected Authority State

The proposed action is low-risk and within the permitted autonomous scope.

Example:

```text
Proposed Action:
CREATE_WORK_ITEM

Authority:
AUTONOMOUS_ALLOWED
```

Expected authority result:

```text
AUTHORIZED
```

---

## 9. Expected GOVQ Decision

```text
ALLOW
```

No human approval is required.

---

## 10. Expected Application Action

The municipal E-Service creates a real or controlled demonstration work item.

Example:

```text
Work Item Created

Category:
Streetlight Maintenance

Location:
Building 4, Municipal Road 3

Status:
OPEN
```

The action must occur through the authorized application path.

---

## 11. Expected Audit Receipt

The system should create a receipt that links:

- execution ID
- request ID
- tenant
- evidence state
- policy
- authority
- provider/model
- decision
- action
- result
- timestamp

Example conceptual output:

```json
{
  "decision": "ALLOW",
  "evidence_status": "SUFFICIENT",
  "authority_status": "AUTHORIZED",
  "action": "CREATE_WORK_ITEM",
  "action_result": "SUCCESS"
}
```

---

## 12. Expected Dashboard Timeline

```text
REQUEST                  PASS
EVIDENCE CHECK           PASS
POLICY MATCH             PASS
AI PROPOSAL              PASS
AUTHORITY CHECK          PASS
HUMAN APPROVAL           NOT REQUIRED
DECISION                 ALLOW
ACTION                   COMPLETED
AUDIT RECEIPT            CREATED
```

The dashboard should make the success path understandable without requiring CLI inspection.

---

## 13. Scenario A Acceptance Criteria

Scenario A passes when:

- sufficient evidence is recognized
- correct policy is bound
- action authority is validated
- GOVQ returns ALLOW
- the protected action executes
- an audit receipt is generated
- the dashboard reflects the same execution

---

# Scenario B — INSUFFICIENT_EVIDENCE

## 14. Scenario Goal

Demonstrate that GOVQ stops execution when required evidence is missing.

Expected decision:

```text
INSUFFICIENT_EVIDENCE
```

The AI must not guess missing facts.

---

## 15. Example Citizen Input

Example request:

> "The streetlight is broken."

Example structured input:

```json
{
  "service_type": "streetlight_issue",
  "description": "Streetlight is broken.",
  "location": null,
  "photo_attached": false
}
```

---

## 16. Expected Evidence State

Important evidence is missing.

Example:

```text
Issue Description   PASS
Service Category    PASS
Location            FAIL
Jurisdiction        UNKNOWN
Supporting Photo    OPTIONAL / MISSING
```

Expected evidence result:

```text
INSUFFICIENT
```

---

## 17. Expected GOVQ Behavior

The system should stop before protected execution.

Expected:

```text
No work item created.
No fabricated location.
No guessed jurisdiction.
No protected action.
```

The system should identify the missing requirement.

Example:

```text
Missing Required Evidence:
LOCATION
```

---

## 18. Expected GOVQ Decision

```text
INSUFFICIENT_EVIDENCE
```

This is not a model failure.

It is a governed execution result.

---

## 19. Expected User Response

The application should request the missing information.

Example:

> "Please provide the location of the damaged streetlight before the request can be submitted."

The system should help the citizen complete the request without inventing data.

---

## 20. Expected Application Action

Protected action:

```text
CREATE_WORK_ITEM
```

Expected result:

```text
NOT EXECUTED
```

This demonstrates fail-closed behavior.

---

## 21. Expected Audit Receipt

The receipt should show why execution stopped.

Example conceptual output:

```json
{
  "decision": "INSUFFICIENT_EVIDENCE",
  "evidence_status": "INSUFFICIENT",
  "missing_requirements": [
    "location"
  ],
  "action": "CREATE_WORK_ITEM",
  "action_result": "NOT_EXECUTED"
}
```

---

## 22. Expected Dashboard Timeline

```text
REQUEST                  PASS
EVIDENCE CHECK           BLOCKED
POLICY MATCH             NOT REACHED / NOT REQUIRED
AI PROPOSAL              LIMITED
AUTHORITY CHECK          NOT EXECUTED
HUMAN APPROVAL           NOT REQUIRED
DECISION                 INSUFFICIENT_EVIDENCE
ACTION                   BLOCKED
AUDIT RECEIPT            CREATED
```

The dashboard should make it obvious that the system intentionally stopped.

---

## 23. Scenario B Acceptance Criteria

Scenario B passes when:

- missing evidence is detected
- the model does not fabricate required information
- GOVQ returns INSUFFICIENT_EVIDENCE
- protected action does not execute
- the application requests missing information
- the audit receipt records the block reason
- the dashboard reflects the blocked execution

---

# Scenario C — HUMAN_APPROVAL

## 24. Scenario Goal

Demonstrate that GOVQ can pause execution when an action exceeds autonomous authority.

Expected decision:

```text
REQUIRE_APPROVAL
```

The workflow must not continue until an authorized human decides.

---

## 25. Example Citizen Input

Example request:

> "Please urgently dispatch a maintenance team and close the road around the damaged electrical pole."

This request contains an action that may exceed the autonomous authority of the AI service.

Example proposed actions:

```text
CREATE_WORK_ITEM
DISPATCH_TEAM
TEMPORARY_ROAD_CLOSURE
```

The first action may be low-risk.

The later actions may require human authority.

---

## 26. Expected Evidence State

Assume required evidence is sufficient.

Example:

```text
Location             PASS
Issue Description    PASS
Photo                PASS
Jurisdiction         PASS
Emergency Context    PASS
```

Expected evidence result:

```text
SUFFICIENT
```

---

## 27. Expected Policy State

Policy may allow the system to create a case automatically but require human authorization for a higher-impact action.

Example:

```text
CREATE_WORK_ITEM          AUTO_ALLOWED
DISPATCH_TEAM             APPROVAL_REQUIRED
TEMPORARY_ROAD_CLOSURE    APPROVAL_REQUIRED
```

---

## 28. Expected Authority State

The model proposes an action beyond its autonomous authority.

Expected result:

```text
AUTONOMOUS_AUTHORITY_INSUFFICIENT
```

GOVQ should not silently downgrade or execute the action.

---

## 29. Expected GOVQ Decision

```text
REQUIRE_APPROVAL
```

The execution enters a paused state.

---

## 30. Expected Approval State

Initial:

```text
APPROVAL_REQUIRED
```

Then:

```text
WAITING_FOR_AUTHORIZED_OFFICER
```

The dashboard should make the pause visible.

---

## 31. Approval Branch A — APPROVE

Authorized officer chooses:

```text
APPROVE
```

Expected flow:

```text
REQUIRE_APPROVAL
      |
      v
Officer Approval
      |
      v
APPROVED
      |
      v
Resume Execution
      |
      v
Authorized Action
      |
      v
Audit Receipt
```

The execution should continue using the same execution context.

---

## 32. Approval Branch B — REJECT

Authorized officer chooses:

```text
REJECT
```

Expected flow:

```text
REQUIRE_APPROVAL
      |
      v
Officer Decision
      |
      v
REJECTED
      |
      v
No Protected Action
      |
      v
Audit Receipt
```

The system must not execute the rejected action.

---

## 33. Expected Audit Evidence

Approval evidence should include:

- execution ID
- action requiring approval
- approval requirement
- approver identity or role
- approval decision
- timestamp
- resumed or terminated state
- action outcome

Conceptual approved receipt:

```json
{
  "decision": "REQUIRE_APPROVAL",
  "approval_status": "APPROVED",
  "action": "DISPATCH_TEAM",
  "action_result": "EXECUTED"
}
```

Conceptual rejected receipt:

```json
{
  "decision": "REQUIRE_APPROVAL",
  "approval_status": "REJECTED",
  "action": "DISPATCH_TEAM",
  "action_result": "NOT_EXECUTED"
}
```

---

## 34. Expected Dashboard Timeline — Before Approval

```text
REQUEST                  PASS
EVIDENCE CHECK           PASS
POLICY MATCH             PASS
AI PROPOSAL              PASS
AUTHORITY CHECK          APPROVAL REQUIRED
HUMAN APPROVAL           WAITING
DECISION                 REQUIRE_APPROVAL
ACTION                   PAUSED
AUDIT RECEIPT            PENDING / UPDATED
```

---

## 35. Expected Dashboard Timeline — Approved

```text
REQUEST                  PASS
EVIDENCE CHECK           PASS
POLICY MATCH             PASS
AI PROPOSAL              PASS
AUTHORITY CHECK          APPROVAL REQUIRED
HUMAN APPROVAL           APPROVED
DECISION                 ALLOW AFTER APPROVAL
ACTION                   COMPLETED
AUDIT RECEIPT            CREATED
```

---

## 36. Expected Dashboard Timeline — Rejected

```text
REQUEST                  PASS
EVIDENCE CHECK           PASS
POLICY MATCH             PASS
AI PROPOSAL              PASS
AUTHORITY CHECK          APPROVAL REQUIRED
HUMAN APPROVAL           REJECTED
DECISION                 STOPPED
ACTION                   NOT EXECUTED
AUDIT RECEIPT            CREATED
```

---

## 37. Scenario C Acceptance Criteria

Scenario C passes when:

- the action is correctly classified as outside autonomous authority
- GOVQ returns REQUIRE_APPROVAL
- execution pauses
- no protected action occurs before approval
- an authorized human can approve or reject
- approval resumes execution correctly
- rejection prevents execution
- the approval decision is auditable
- the dashboard reflects the actual runtime state

---

# Cross-Scenario Validation

## 38. Same Architecture, Different Decisions

The three scenarios should use the same execution architecture.

Only the evidence, policy, or authority state changes.

Reference:

```text
Same GOVQ Runtime
       |
       +--> Scenario A
       |       |
       |       v
       |     ALLOW
       |
       +--> Scenario B
       |       |
       |       v
       | INSUFFICIENT_EVIDENCE
       |
       +--> Scenario C
               |
               v
        REQUIRE_APPROVAL
```

This is important because the demo should prove a governance system, not three independent scripted applications.

---

## 39. Zero-Bypass Requirement

For all scenarios:

> **No governed decision, no protected action.**

The protected tool or application action must not be reachable directly from:

- the LLM
- the user interface
- the workflow adapter
- an alternate API route

without the required GOVQ path.

---

## 40. Runtime Evidence Requirement

Each demo execution should produce a traceable record.

Recommended runtime fields include:

```text
execution_id
request_id
tenant_id
evidence_status
evidence_digest
policy_snapshot_id
provider_id
authority_status
approval_state
decision
authorized_action
action_result
audit_receipt
latency_ms
timestamp
```

Exact implementation fields may differ.

The important requirement is traceability across the entire execution.

---

## 41. Demo Presentation Layout

Recommended live layout:

```text
+--------------------------+-------------------------------+
| Citizen E-Service        | Cognitive Governance         |
|                          | Dashboard                     |
| Request Form             |                               |
| Citizen Input            | Evidence                     |
| Result                   | Policy                       |
|                          | Authority                    |
|                          | Approval                     |
|                          | Action                       |
|                          | Audit                        |
+--------------------------+-------------------------------+
```

Optional third area:

```text
Officer Approval / Action Result
```

This allows judges to see both user value and governance at the same time.

---

## 42. Recommended Demo Order

Recommended presentation sequence:

### Demo 1 — ALLOW

Show that the system can successfully act.

### Demo 2 — INSUFFICIENT_EVIDENCE

Show that the system can safely stop.

### Demo 3 — HUMAN_APPROVAL

Show that organizational authority remains above AI autonomy.

This creates a clear narrative:

```text
AI CAN ACT
    |
    v
AI CAN STOP
    |
    v
HUMANS REMAIN IN CONTROL
```

---

## 43. What the Judge Should Understand

After the three scenarios, the reviewer should be able to answer:

1. What did the citizen request?
2. What did the AI understand?
3. What evidence supported the request?
4. Which policy applied?
5. Was the proposed action authorized?
6. Did the system stop when evidence was insufficient?
7. Did the system require human approval when authority was insufficient?
8. What real action occurred?
9. Can the execution be audited?

If these questions are obvious from the live demo, the GOVQ thesis has been communicated successfully.

---

## 44. Demo Success Statement

The demo should prove:

> **GOVQ does not only help AI complete tasks. It determines whether AI-assisted execution is allowed to proceed.**

The three scenarios demonstrate three different forms of organizational control:

```text
ALLOW
= AI may proceed.

INSUFFICIENT_EVIDENCE
= AI must stop and ask for more information.

REQUIRE_APPROVAL
= AI must pause and wait for authorized human control.
```

---

## 45. Final Demo Principle

The final message of the demo is:

> **Autonomous AI should not only be intelligent enough to act.  
> It must be authorized, evidenced, and accountable enough to act.**
