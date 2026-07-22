"""
engines/execution_planner.py

Deterministic Governance Core (DGC)

Execution Planner

The Execution Planner translates a governance Decision into an
ExecutionPlan.

The planner performs NO external actions.

Responsibilities
----------------
1. Read the Decision.
2. Determine required execution tasks.
3. Produce an ExecutionPlan.

The Execution Engine is responsible for actually performing
those tasks.
"""

from schemas.decision import Decision
from schemas.execution_plan import ExecutionPlan
from schemas.execution_task import ExecutionTask
from schemas.execution_task import ExecutionTaskPriority
from schemas.execution_task import ExecutionTaskType


class ExecutionPlanner:
    """
    Builds an ExecutionPlan from a Decision.
    """

    def __init__(self) -> None:
        pass

    ####################################################################
    #
    # Public Interface
    #
    ####################################################################

    def build_plan(
        self,
        decision: Decision,
    ) -> ExecutionPlan:
        """
        Build an execution plan.
        """

        tasks = self._build_tasks(decision)

        return ExecutionPlan(

            decision_id=decision.decision_id,

            tasks=tasks,

        )

    ####################################################################
    #
    # Task Planning
    #
    ####################################################################

    def _build_tasks(
        self,
        decision: Decision,
    ) -> list[ExecutionTask]:
        """
        Determine required execution tasks.
        """

        tasks: list[ExecutionTask] = []

        #
        # APPROVED
        #

        if decision.status == "approved":

            return tasks

        #
        # REVIEW REQUIRED
        #

        if decision.status == "review_required":

            tasks.append(

                ExecutionTask(

                    task_type=ExecutionTaskType.REQUEST_REVIEW,

                    priority=ExecutionTaskPriority.MEDIUM,

                    description="Security review required.",

                )

            )

            tasks.append(

                ExecutionTask(

                    task_type=ExecutionTaskType.NOTIFY,

                    priority=ExecutionTaskPriority.MEDIUM,

                    description="Notify security team.",

                )

            )

        #
        # DENIED
        #

        elif decision.status == "denied":

            tasks.append(

                ExecutionTask(

                    task_type=ExecutionTaskType.CREATE_INCIDENT,

                    priority=ExecutionTaskPriority.HIGH,

                    description="Create security incident.",

                )

            )

            tasks.append(

                ExecutionTask(

                    task_type=ExecutionTaskType.NOTIFY,

                    priority=ExecutionTaskPriority.HIGH,

                    description="Notify security team.",

                )

            )

            #
            # Future Examples
            #

            # tasks.append(
            #     ExecutionTask(
            #         task_type=ExecutionTaskType.BLOCK_DEPLOYMENT,
            #         priority=ExecutionTaskPriority.CRITICAL,
            #         description="Block production deployment.",
            #     )
            # )

            # tasks.append(
            #     ExecutionTask(
            #         task_type=ExecutionTaskType.WEBHOOK,
            #         priority=ExecutionTaskPriority.CRITICAL,
            #         description="Trigger PagerDuty incident.",
            #     )
            # )

        return tasks
