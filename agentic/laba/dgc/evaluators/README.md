# Evaluators

## Overview

The `evaluators` package contains the implementation used to evaluate
governance policies.

Unlike the `policies` directory, which contains configuration, evaluators
contain executable Python code.

Each evaluator is responsible for evaluating **one specific type of policy**
and returning a `PolicyResult`.

---

# Design Philosophy

Evaluators answer one question:

> **How should this policy be evaluated?**

Policies answer a different question:

> **What should be evaluated?**

This separation allows governance policies to change independently from the
evaluation logic.

```text
Policy (YAML)
        │
        ▼
Policy Engine
        │
        ▼
Evaluator
        │
        ▼
PolicyResult
```

---

# Responsibilities

An evaluator should:

- Read the SecurityEvent
- Read the Policy
- Read policy parameters
- Perform the evaluation
- Return a PolicyResult

An evaluator should **not**:

- Load policy files
- Select policies
- Make governance decisions
- Contact external systems
- Create Jira tickets
- Send Slack notifications

Those responsibilities belong to other components of the DGC.

---

# Evaluator Lifecycle

```text
SecurityEvent
        │
        ▼
Policy
        │
        ▼
Evaluator
        │
        ▼
PolicyResult
```

Every evaluator follows the same workflow.

---

# Standard Interface

Each evaluator implements a single function.

```python
def evaluate(
    event,
    policy,
) -> PolicyResult:
```

The Policy Engine dynamically imports the evaluator specified by the policy
and executes this function.

---

# Example

Policy

```yaml
policy_id: latest_tag

evaluation_module: latest_tag
```

Policy Engine

```python
module = import_module(
    "evaluators.latest_tag"
)

result = module.evaluate(
    event,
    policy,
)
```

The Policy Engine does not know how the evaluator works.

It only knows that every evaluator implements the same interface.

---

# Example Evaluators

Examples may include:

```
latest_tag.py

privileged_container.py

host_network.py

root_user.py

image_signature.py

public_bucket.py
```

Each evaluator focuses on one security concern.

---

# Policy Parameters

Evaluators receive policy parameters from the Policy Engine.

Example

Policy

```yaml
parameters:

  approved_registries:

    - company.ecr.aws

  max_image_age_days: 30
```

Evaluator

```python
policy.parameters["approved_registries"]

policy.parameters["max_image_age_days"]
```

This allows policies to change without modifying evaluator code.

---

# Returning Results

Evaluators always return a `PolicyResult`.

Example

```python
return PolicyResult(

    policy_id=policy.policy_id,

    status="passed",

    message="Container image is compliant."
)
```

or

```python
return PolicyResult(

    policy_id=policy.policy_id,

    status="failed",

    message="Container is running as root."
)
```

Every evaluator returns the same schema regardless of the technology being
evaluated.

---

# One Responsibility Per Evaluator

Each evaluator should perform one evaluation.

Good examples

```
latest_tag.py

privileged_container.py

host_network.py
```

Avoid creating evaluators that perform multiple unrelated checks.

For example:

```
bad_security_check.py
```

should instead become

```
host_network.py

root_user.py

host_pid.py
```

Smaller evaluators are easier to test, maintain, and reuse.

---

# Deterministic Design

Evaluators should be deterministic.

Given the same:

- SecurityEvent
- Policy
- Parameters

the evaluator should always return the same PolicyResult.

Evaluators should avoid:

- Random values
- External API calls
- Database updates
- Side effects

Their responsibility is evaluation—not execution.

---

# Testing

Because evaluators have a single responsibility, they are straightforward to
unit test.

Typical test pattern:

```python
event = SecurityEvent(...)

policy = Policy(...)

result = evaluate(
    event,
    policy,
)

assert result.status == "passed"
```

---

# Educational Objectives

After completing this section, students should understand:

- Evaluators contain business logic.
- Policies contain configuration.
- The Policy Engine connects the two.
- Every evaluator returns the same PolicyResult schema.
- Small, focused evaluators are easier to test and maintain.

---

# Summary

Evaluators transform governance policies into evaluation results.

```
SecurityEvent
        │
        ▼
Policy
        │
        ▼
Evaluator
        │
        ▼
PolicyResult
```

Keeping evaluators small, deterministic, and focused on a single
responsibility is one of the core design principles of the Deterministic
Governance Core.
