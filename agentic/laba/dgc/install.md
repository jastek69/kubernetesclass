# Deterministic Governance Core (DGC)

# Installation Guide

## Overview

This project is intentionally built in stages.

Students are encouraged to complete each stage before moving to the next.
The architecture is layered, meaning that later components depend on earlier
components.

Do **not** attempt to build the Execution Engine first.

Follow the installation order below.

---

# Phase 1 — Project Setup

Clone the repository.

```bash
git clone <repository-url>

cd deterministic-governance-core
```

Create a virtual environment.

```bash
python -m venv .venv
```

Activate the environment.

Windows

```powershell
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

Install project dependencies.

```bash
pip install -r requirements.txt
```

---

# Phase 2 — Understand the Architecture

Before writing any code, review the documentation.

Read:

```
README.md

schemas/README.md

engines/README.md

policies/README.md
```

Understanding the architecture first will make the remaining labs much easier.

---

# Phase 3 — Schemas

Begin by reviewing the schemas.

Recommended order:

```
SecurityEvent

↓

PolicyResult

↓

Decision

↓

ExecutionTask

↓

ExecutionPlan

↓

ExecutionResult

↓

ExecutionRun
```

These schemas form the language spoken by the entire framework.

---

# Phase 4 — Policies

Review the policy files.

Examples:

```
latest_tag.yaml

privileged_container.yaml

host_network.yaml
```

These policies describe governance rules.

Policies contain **configuration**, not code.

---

# Phase 5 — Evaluators

Review the evaluator modules.

Examples:

```
latest_tag.py

privileged_container.py

host_network.py
```

Evaluators contain the logic used to evaluate policies.

Each evaluator returns a PolicyResult.

---

# Phase 6 — Policy Engine

Study the Policy Engine.

Responsibilities:

- Load policies
- Select applicable policies
- Execute evaluators
- Return PolicyResults

The Policy Engine performs no governance decisions.

---

# Phase 7 — Decision Engine

Study the Decision Engine.

Responsibilities:

- Analyze PolicyResults
- Produce a Decision

Example outcomes:

```
Approved

Review Required

Denied
```

---

# Phase 8 — Execution Planner

Study the Execution Planner.

Responsibilities:

- Read a Decision
- Produce an ExecutionPlan

No external systems are contacted.

This is conceptually similar to:

```
terraform plan
```

The planner determines what should happen but performs no actions.

---

# Phase 9 — Execution Engine

Study the Execution Engine.

Responsibilities:

- Read an ExecutionPlan
- Locate adapters
- Execute tasks
- Produce an ExecutionRun

Unlike previous engines, this component communicates with external systems.

---

# Phase 10 — Adapters

Review each adapter.

Examples:

```
Slack Adapter

Jira Adapter

Email Adapter

Webhook Adapter

PagerDuty Adapter (Optional)
```

Adapters isolate vendor-specific code from the governance framework.

Students may replace adapters without modifying the engines.

---

# Recommended Build Order

```
Schemas
      │
      ▼
Policies
      │
      ▼
Evaluators
      │
      ▼
Policy Engine
      │
      ▼
Decision Engine
      │
      ▼
Execution Planner
      │
      ▼
Execution Engine
      │
      ▼
Adapters
```

---

# Example Workflow

A completed governance workflow looks like this.

```python
event = SecurityEvent(...)

policy_results = policy_engine.evaluate_event(event)

decision = decision_engine.evaluate(policy_results)

execution_plan = execution_planner.build_plan(decision)

execution_run = execution_engine.execute(execution_plan)
```

---

# Learning Objectives

After completing this project, students should understand:

- Schema-driven architecture
- Policy-based governance
- Deterministic decision making
- Separation of planning and execution
- Adapter design pattern
- Enterprise automation architecture
- SOAR fundamentals
- Infrastructure-as-Code design principles
- Extensible security frameworks

---

# Next Steps

Future enhancements may include:

- ServiceNow integration
- Microsoft Teams integration
- PagerDuty integration
- AWS Step Functions
- EventBridge
- Bedrock AI decision support
- Amazon Q integration
- OPA integration
- Cedar policy support
- Rego policy support
- CEL policy support

These enhancements can be added without changing the core governance architecture.

---

Happy Building!

Remember the guiding philosophy of the Deterministic Governance Core:

> **Schemas describe reality. Engines transform reality. Adapters interact with reality.**
