# Engines

## Overview

The `engines` package contains the business logic of the Deterministic
Governance Core (DGC).

Each engine performs **one specific responsibility** within the governance
pipeline.

Unlike schemas, which simply represent data, engines transform one schema
into another.

The architecture intentionally follows the **Single Responsibility Principle
(SRP)** and promotes deterministic, testable behavior.

---

# Governance Pipeline

The governance pipeline is composed of four primary engines.

```text
SecurityEvent
        │
        ▼
Policy Engine
        │
        ▼
PolicyResult[]
        │
        ▼
Decision Engine
        │
        ▼
Decision
        │
        ▼
Execution Planner
        │
        ▼
ExecutionPlan
        │
        ▼
Execution Engine
        │
        ▼
ExecutionRun
```

Each engine accepts one schema as input and produces another schema as output.

---

# Engine Responsibilities

## Policy Engine

Input

```
SecurityEvent
```

Output

```
PolicyResult[]
```

Responsibilities

- Load governance policies
- Determine applicable policies
- Execute policy evaluators
- Return PolicyResults

The Policy Engine **does not**:

- Make governance decisions
- Contact external systems
- Execute remediation actions

---

## Decision Engine

Input

```
PolicyResult[]
```

Output

```
Decision
```

Responsibilities

- Analyze all policy results
- Apply governance rules
- Produce a single Decision

Example Decisions

```
Approved

Review Required

Denied
```

The Decision Engine has no knowledge of Jira, Slack, Kubernetes, AWS, or any
other technology-specific implementation.

---

## Execution Planner

Input

```
Decision
```

Output

```
ExecutionPlan
```

Responsibilities

- Translate a Decision into planned actions
- Build an immutable ExecutionPlan

Example Tasks

```
Notify Security Team

Create Incident

Request Review

Block Deployment
```

The planner performs **no external actions**.

Think of the Execution Planner as being conceptually similar to:

```
terraform plan
```

It describes what should happen but does not execute anything.

---

## Execution Engine

Input

```
ExecutionPlan
```

Output

```
ExecutionRun
```

Responsibilities

- Execute each ExecutionTask
- Locate the correct adapter
- Capture execution results
- Produce an ExecutionRun

Unlike the previous engines, the Execution Engine interacts with external
systems.

Examples include:

- Slack
- Jira
- Email
- Microsoft Teams
- ServiceNow
- PagerDuty

These integrations are isolated behind adapters.

---

# Design Philosophy

Each engine performs a single transformation.

```
Schema
        │
        ▼
Engine
        │
        ▼
New Schema
```

Because every engine has only one responsibility, the framework becomes:

- Easier to understand
- Easier to test
- Easier to maintain
- Easier to extend

---

# Deterministic Architecture

Everything before the Execution Engine is deterministic.

```
SecurityEvent

↓

PolicyResult

↓

Decision

↓

ExecutionPlan
```

Given the same event and the same policies, these engines will always produce
the same result.

Only the Execution Engine performs side effects by communicating with external
systems.

---

# Why Separate Planning from Execution?

Separating planning from execution provides several benefits.

```
Decision

↓

Execution Planner

↓

ExecutionPlan

↓

Review (Optional)

↓

Execution Engine
```

Advantages include:

- Plans can be reviewed before execution.
- Plans can be stored for auditing.
- Plans can be replayed for testing.
- Governance remains independent of external system failures.
- External integrations remain isolated from business logic.

---

# Educational Objectives

By completing the engine implementations, students will gain experience with:

- Layered architecture
- Deterministic processing
- Separation of concerns
- Policy-based governance
- Workflow orchestration
- Enterprise security automation
- Adapter design pattern
- Immutable data pipelines

---

# Summary

The engines form the heart of the Deterministic Governance Core.

Each engine has one job:

| Engine | Responsibility |
|---------|----------------|
| Policy Engine | Evaluate policies |
| Decision Engine | Make governance decisions |
| Execution Planner | Plan operational responses |
| Execution Engine | Execute the operational plan |

Together, these engines create a governance pipeline that is deterministic,
extensible, and suitable for enterprise security automation.
