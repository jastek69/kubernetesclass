"""
engines/policy_engine.py

Deterministic Governance Core (DGC)

Policy Engine

The Policy Engine orchestrates policy evaluation.

Responsibilities
----------------
1. Load available policies.
2. Determine which policies apply to the incoming event.
3. Dispatch each policy to its evaluator.
4. Collect PolicyDecision objects.
5. Return the complete collection.

The Policy Engine intentionally contains NO security logic.
All security logic resides inside individual evaluation modules.
"""

from importlib import import_module

from schemas.evidence import Evidence
from schemas.policy import Policy
from schemas.policy_decision import PolicyDecision
from schemas.security_event import SecurityEvent


class PolicyEngine:
    """
    Orchestrates policy evaluation for a SecurityEvent.
    """

    def __init__(self) -> None:
        """
        Initialize the Policy Engine.

        Version 1 intentionally maintains no internal state.
        Policies are loaded for every evaluation to support
        future dynamic policy repositories.
        """
        pass

    ####################################################################
    #
    # Public Interface
    #
    ####################################################################

    def evaluate_event(
        self,
        event: SecurityEvent,
        evidence: list[Evidence],
    ) -> list[PolicyDecision]:
        """
        Evaluate a SecurityEvent against all applicable policies.

        Parameters
        ----------
        event:
            Normalized SecurityEvent.

        evidence:
            Evidence associated with the event.

        Returns
        -------
        list[PolicyDecision]
            One PolicyDecision for each evaluated policy.
        """

        policies = self._load_policies()

        applicable_policies = self._select_policies(
            event=event,
            policies=policies,
        )

        results: list[PolicyDecision] = []

        for policy in applicable_policies:

            decision = self._evaluate_policy(
                event=event,
                policy=policy,
                evidence=evidence,
            )

            results.append(decision)

        return results

    ####################################################################
    #
    # Policy Loading
    #
    ####################################################################

    def _load_policies(self) -> list[Policy]:
        """
        Load available policies.

        Version 1
        ---------
        Returns a hard-coded collection.

        Future
        ------
        This will likely become a PolicyRepository responsible for
        loading policies from:

        * Filesystem
        * YAML
        * JSON
        * Database
        * S3
        * Git Repository
        * REST API
        """

        return []

    ####################################################################
    #
    # Policy Selection
    #
    ####################################################################

    def _select_policies(
        self,
        event: SecurityEvent,
        policies: list[Policy],
    ) -> list[Policy]:
        """
        Determine which policies apply to this event.

        Version 1
        ---------
        Returns every enabled policy.

        Future
        ------
        Policy selection may consider:

        * Event Source
        * Event Category
        * Cloud Provider
        * Kubernetes
        * AI / MCP
        * Severity
        * Environment
        * Tags
        """

        return [

            policy

            for policy in policies

            if policy.enabled

        ]

    ####################################################################
    #
    # Policy Evaluation
    #
    ####################################################################

    def _evaluate_policy(
        self,
        event: SecurityEvent,
        policy: Policy,
        evidence: list[Evidence],
    ) -> PolicyDecision:
        """
        Execute the evaluator assigned to a policy.

        The evaluator module must expose:

            evaluate(
                event,
                policy,
                evidence
            ) -> PolicyDecision
        """

        module = import_module(
            policy.evaluation_module
        )

        return module.evaluate(
            event=event,
            policy=policy,
            evidence=evidence,
        )
