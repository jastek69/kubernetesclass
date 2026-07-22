# Policies

## Overview

The `policies` directory contains the governance policies used by the
Deterministic Governance Core (DGC).

Policies define **what** should be evaluated.

They do **not** contain the implementation used to evaluate those rules.

The evaluation logic resides in the `evaluators` package.

---

# Design Philosophy

A policy is configuration.

A policy is **not** code.

This separation allows governance rules to change without modifying the
application.

```text
Policy (Configuration)
        │
        ▼
Policy Engine
        │
        ▼
Evaluator (Code)
        │
        ▼
PolicyResult
```

---

# Policy Structure

Each policy is stored as a YAML document.

Example

```yaml
policy_id: latest_tag

name: Latest Image Tag

description: Ensure container images use approved tags.

enabled: true

severity: medium

category: Container Security

evaluation_module: latest_tag

parameters:

  allowed_tags:

    - latest

    - stable
```

---

# Policy Responsibilities

Policies define:

- Unique identifier
- Human-readable name
- Description
- Severity
- Category
- Evaluation module
- Parameters
- Enabled/Disabled state

Policies do **not** contain Python code.

---

# Policy Lifecycle

Policies follow this workflow.

```text
Policy YAML
        │
        ▼
Policy Engine
        │
        ▼
Select Evaluator
        │
        ▼
Execute Evaluator
        │
        ▼
PolicyResult
```

The Policy Engine loads the policy and determines which evaluator should be
used.

The evaluator performs the actual security analysis.

---

# Example Policies

Examples included with this project may include:

```
latest_tag.yaml

privileged_container.yaml

host_network.yaml

root_user.yaml

image_signature.yaml

public_bucket.yaml
```

Each policy is evaluated independently.

---

# Policy Parameters

Policies may include configurable parameters.

Example

```yaml
parameters:

  max_age_days: 30

  approved_registries:

    - public.ecr.aws

    - company.registry.local
```

Evaluators use these parameters during execution.

Changing a parameter does not require changing application code.

---

# Enabling and Disabling Policies

Policies can be enabled or disabled.

Example

```yaml
enabled: true
```

or

```yaml
enabled: false
```

Disabled policies are ignored by the Policy Engine.

---

# Severity Levels

Policies typically define a severity.

Examples

```
Low

Medium

High

Critical
```

Severity helps the Decision Engine determine the appropriate governance
response.

---

# Categories

Policies may also define categories.

Examples include:

- Container Security
- Kubernetes
- Identity
- IAM
- Networking
- Data Protection
- Compliance
- Logging
- Encryption

Categories assist with organization and reporting.

---

# Why YAML?

Using YAML provides several advantages.

- Easy to read
- Easy to modify
- Version control friendly
- Human-readable
- Platform independent

Security teams can review policies without reading Python code.

---

# Relationship to Evaluators

Policies define **what** should be evaluated.

Evaluators define **how** the evaluation is performed.

Example

```
latest_tag.yaml

↓

evaluation_module:

latest_tag

↓

evaluators/latest_tag.py
```

This separation keeps governance configuration independent from application
logic.

---

# Future Enhancements

Future versions of the DGC may support additional policy sources.

Examples include:

- Git repositories
- Amazon S3
- Databases
- REST APIs
- Open Policy Agent (OPA)
- Cedar
- Rego
- Common Expression Language (CEL)

Because the Policy Engine only loads policies, these enhancements can be
added without changing the overall architecture.

---

# Educational Objectives

After completing this section, students should understand:

- Policies are configuration.
- Evaluators contain code.
- The Policy Engine connects the two.
- Governance rules should be data-driven whenever possible.
- Separating configuration from implementation improves flexibility and
  maintainability.

---

# Summary

Policies answer one simple question:

> **What should be evaluated?**

Evaluators answer a different question:

> **How should it be evaluated?**

Keeping these responsibilities separate is one of the fundamental design
principles of the Deterministic Governance Core.
