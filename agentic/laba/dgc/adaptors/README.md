# Adapters

## Overview

The `adapters` package contains integrations with external systems.

Unlike the governance engines, adapters communicate with APIs, cloud services,
ticketing systems, messaging platforms, and other enterprise tools.

Adapters are the only components within the Deterministic Governance Core
(DGC) that should perform external actions.

---

# Design Philosophy

The governance engines determine **what** should happen.

Adapters determine **how** to communicate with external systems.

```text
ExecutionPlan
        │
        ▼
Execution Engine
        │
        ▼
ExecutionTask
        │
        ▼
Adapter
        │
        ▼
External System
```

This separation keeps governance logic independent from vendor-specific
implementations.

---

# Responsibilities

Adapters are responsible for:

- Authentication
- API communication
- Request formatting
- Response handling
- Error handling
- Vendor-specific implementation

Adapters are **not** responsible for:

- Evaluating policies
- Making governance decisions
- Planning execution
- Selecting tasks

Those responsibilities belong to the governance engines.

---

# Adapter Lifecycle

```text
ExecutionTask
        │
        ▼
Adapter
        │
        ▼
External System
        │
        ▼
ExecutionResult
```

Every adapter receives an ExecutionTask and returns an ExecutionResult.

---

# Standard Interface

Every adapter implements the same interface.

```python
class BaseAdapter:

    def execute(
        self,
        task,
    ) -> ExecutionResult:
        ...
```

Because every adapter implements the same interface, the Execution Engine
does not need to know which vendor is being used.

---

# Example

Execution Task

```text
CREATE_INCIDENT
```

Execution Engine

```python
adapter = registry.get(task.task_type)

result = adapter.execute(task)
```

Adapter

```python
class JiraAdapter(BaseAdapter):

    def execute(self, task):

        ...
```

The Execution Engine never communicates directly with Jira.

---

# Example Adapters

Examples included with this project may include:

```
base_adapter.py

jira_adapter.py

slack_adapter.py

email_adapter.py
```

Future examples may include:

```
servicenow_adapter.py

teams_adapter.py

pagerduty_adapter.py

webhook_adapter.py

splunk_adapter.py

security_hub_adapter.py
```

Students are encouraged to create additional adapters as exercises.

---

# Why Adapters?

Without adapters, vendor-specific code would spread throughout the framework.

Example (Not Recommended)

```
Execution Engine

↓

if Jira

↓

if Slack

↓

if ServiceNow

↓

if Email
```

Instead, the DGC uses adapters.

```
Execution Engine

↓

Adapter Registry

↓

Jira Adapter

or

Slack Adapter

or

ServiceNow Adapter
```

This greatly simplifies maintenance.

---

# Vendor Neutral Design

The DGC intentionally uses vendor-neutral task names.

Examples

```
CREATE_INCIDENT

NOTIFY

EMAIL

REQUEST_REVIEW
```

Rather than

```
CREATE_JIRA_ISSUE

SEND_SLACK_MESSAGE
```

This allows organizations to replace one vendor with another without changing
the governance logic.

Example

```
CREATE_INCIDENT

↓

Jira Adapter
```

or

```
CREATE_INCIDENT

↓

ServiceNow Adapter
```

The Execution Planner remains unchanged.

---

# Adapter Registry

The Execution Engine uses an Adapter Registry to locate the correct adapter.

Example

```python
registry = {

    CREATE_INCIDENT:

        JiraAdapter(),

    NOTIFY:

        SlackAdapter(),

}
```

When a task is executed, the engine retrieves the correct adapter from the
registry.

---

# Error Handling

Failures within an adapter do not affect governance decisions.

Example

```
Decision

↓

Execution Plan

↓

Jira Adapter

↓

Jira API Unavailable
```

The governance decision remains valid.

Only the execution of that task failed.

The adapter returns an ExecutionResult describing the failure.

---

# Deterministic Governance

Everything before the adapters is deterministic.

```
SecurityEvent

↓

PolicyResult

↓

Decision

↓

ExecutionPlan
```

Adapters are intentionally different.

Because they communicate with external systems, adapters must handle:

- Network failures
- Authentication
- Timeouts
- API changes
- Rate limiting
- Service availability

These operational concerns are isolated from the governance core.

---

# Educational Objectives

After completing this section, students should understand:

- Why enterprise systems use adapters
- How adapters isolate vendor-specific code
- How the Adapter Pattern improves maintainability
- Why governance logic should remain independent from infrastructure
- How external systems are integrated into the DGC

---

# Think Like an Architect

Imagine that your organization decides to replace Jira with ServiceNow.

Without adapters, the Execution Engine would require significant changes.

With adapters, only one component changes.

```
CREATE_INCIDENT

↓

ServiceNow Adapter
```

The Execution Planner, Decision Engine, Policy Engine, and all schemas remain
unchanged.

This demonstrates one of the primary goals of enterprise architecture:

> **Change infrastructure without changing business logic.**

---

# Summary

Adapters connect the Deterministic Governance Core to the outside world.

```
ExecutionTask
        │
        ▼
Adapter
        │
        ▼
External System
        │
        ▼
ExecutionResult
```

Adapters are the only components responsible for communicating with external
systems.

Keeping this responsibility isolated makes the framework easier to extend,
test, maintain, and evolve as enterprise technologies change.
