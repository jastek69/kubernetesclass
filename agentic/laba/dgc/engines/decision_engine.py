"""
engines/decision_engine.py

Deterministic Governance Core (DGC)

Decision Engine

The Decision Engine is responsible for producing a single
governance Decision from a collection of PolicyResults.

Responsibilities
----------------
1. Validate PolicyResults.
2. Summarize evaluation outcomes.
3. Apply governance rules.
4. Produce a single Decision.

The Decision Engine intentionally contains NO security logic.
Security evaluation is performed by the Policy Engine.
Operational execution is handled by the Execution Engine.
"""

from collections import Counter

from schemas.decision import Decision
from schemas.policy_result import PolicyResult


class DecisionEngine:
    """
    Produces a governance Decision from PolicyResults.
    """

    def __init__(self) -> None:
        """
        Version 1 maintains no internal state.
        """
        pass

    ####################################################################
    #
    # Public Interface
    #
    ####################################################################

    def evaluate_policy_results(
        self,
        policy_results: list[PolicyResult],
    ) -> Decision:
        """
        Produce a governance decision.
        """

        self._validate(policy_results)

        summary = self._summarize(policy_results)

        return self._build_decision(
            summary=summary,
            policy_results=policy_results,
        )

    ####################################################################
    #
    # Validation
    #
    ####################################################################

    def _validate(
        self,
        policy_results: list[PolicyResult],
    ) -> None:
        """
        Validate incoming PolicyResults.
        """

        if not policy_results:
            raise ValueError(
                "No PolicyResults supplied."
            )

    ####################################################################
    #
    # Summary
    #
    ####################################################################

    def _summarize(
        self,
        policy_results: list[PolicyResult],
    ) -> Counter:
        """
        Count policy outcomes.
        """

        return Counter(
            result.status
            for result in policy_results
        )

    ####################################################################
    #
    # Decision
    #
    ####################################################################

    def _build_decision(
        self,
        summary: Counter,
        policy_results: list[PolicyResult],
    ) -> Decision:
        """
        Build the final governance decision.

        Version 1

            Any FAILED policy
                -> DENY

            Any WARNING
                -> REVIEW_REQUIRED

            Otherwise
                -> APPROVED
        """

        #
        # Simple deterministic governance
        #

        if summary["failed"] > 0:

            status = "denied"

            rationale = (
                "One or more policies failed."
            )

        elif summary["warning"] > 0:

            status = "review_required"

            rationale = (
                "Policy warnings require review."
            )

        else:

            status = "approved"

            rationale = (
                "All policies passed."
            )

        return Decision(

            status=status,

            rationale=rationale,

            policy_result_ids=[
                result.policy_result_id
                for result in policy_results
            ],

            passed=summary["passed"],

            failed=summary["failed"],

            warnings=summary["warning"],

            skipped=summary["skipped"],

            errors=summary["error"],
        )
