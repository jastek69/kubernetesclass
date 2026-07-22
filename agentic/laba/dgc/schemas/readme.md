# Schemas

## Overview

The `schemas` package contains the core data models used throughout the
Deterministic Governance Core (DGC).

These schemas represent the immutable objects that move between each engine
within the framework.

A schema **does not perform work**.

A schema simply represents data.

This separation allows the engines to remain deterministic, testable, and
easy to reason about.

---

## Data Flow

The DGC transforms one schema into another.


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

Notice that each engine accepts one schema and produces another.

---

## Why Schemas?

Using strongly typed schemas provides several benefits:

- Validation
- Consistent interfaces
- Deterministic processing
- Easier testing
- Better IDE support
- Self-documenting architecture

Rather than passing Python dictionaries throughout the application, each
component works with well-defined objects.

---

# Schema Overview

## SecurityEvent

Represents a normalized security event entering the governance pipeline.

Examples include:

- Amazon GuardDuty
- AWS Security Hub
- Amazon Inspector
- Kubernetes Admission Controller
- Trivy
- CloudTrail
- SIEM events

This is the starting point of the governance workflow.

---

## PolicyResult

Represents the result of evaluating a single policy.

Examples:

- Passed
- Failed
- Warning
- Skipped

The Policy Engine produces one PolicyResult for each applicable policy.

---

## Decision

Represents the governance decision after evaluating all PolicyResults.

Examples:

- Approved
- Review Required
- Denied

A Decision contains no execution logic.

---

## ExecutionPlan

Represents the planned operational response.

Examples:

- Create Incident
- Notify Security Team
- Request Review
- Block Deployment

The ExecutionPlan is similar in philosophy to a Terraform plan.

It describes what should happen but performs no actions.

---

## ExecutionTask

Represents a single action within an ExecutionPlan.

Examples include:

- CREATE_INCIDENT
- NOTIFY
- REQUEST_REVIEW
- EMAIL

ExecutionTasks are intentionally vendor-neutral.

For example:

CREATE_INCIDENT

may later become

- Jira
- ServiceNow
- Azure DevOps

without changing the planner.

---

## ExecutionResult

Represents the outcome of executing a single ExecutionTask.

Examples:

- Success
- Failure
- Error Message
- Execution Duration

---

## ExecutionRun

Represents the complete execution of an ExecutionPlan.

An ExecutionRun contains the results of every task executed by the
Execution Engine.

Unlike an ExecutionPlan, an ExecutionRun captures what actually happened.

---

# Design Philosophy

The Deterministic Governance Core separates planning from execution.

    ```
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

This separation provides several important advantages:

- Plans can be reviewed before execution.
- Plans can be audited.
- Plans can be stored.
- Plans are deterministic.
- Execution failures do not change governance decisions.
- External integrations remain isolated from governance logic.

---

# Immutable Objects

Schemas should be treated as immutable representations of a point in the
governance workflow.

Each schema answers a different question.


| Schema | Question Answered |
|---------|-------------------|
| SecurityEvent | What happened? |
| PolicyResult | How did a policy evaluate the event? |
| Decision | What governance decision was made? |
| ExecutionPlan | What should happen next? |
| ExecutionResult | What happened when a task executed? |
| ExecutionRun | What was the overall execution outcome? |


---

# Educational Goal

This project intentionally separates:

- Data (Schemas)
- Logic (Engines)
- Integrations (Adapters)

This architectural pattern keeps the governance core deterministic while
allowing organizations to integrate with external systems such as Slack,
Jira, ServiceNow, PagerDuty, Microsoft Teams, or custom APIs without
modifying the governance engines themselves.
