"""
engines/execution_engine.py

Deterministic Governance Core (DGC)

Execution Engine

Executes an immutable ExecutionPlan by delegating each
ExecutionTask to the appropriate adapter.

Responsibilities
----------------
1. Read ExecutionPlan
2. Locate adapter
3. Execute task
4. Capture ExecutionResult
5. Return ExecutionRun

The Execution Engine does NOT:

- Make governance decisions
- Evaluate policies
- Build execution plans
"""

from adapters.adapter_registry import AdapterRegistry

from schemas.execution_plan import ExecutionPlan
from schemas.execution_result import ExecutionResult
from schemas.execution_run import ExecutionRun


class ExecutionEngine:

    """
    Executes an ExecutionPlan.
    """

    def __init__(self):

        self.registry = AdapterRegistry()

    ####################################################################
    #
    # Public Interface
    #
    ####################################################################

    def execute(
        self,
        plan: ExecutionPlan,
    ) -> ExecutionRun:

        results: list[ExecutionResult] = []

        print(f"\nExecuting Plan: {plan.plan_id}")

        for task in plan.tasks:

            result = self._execute_task(task)

            results.append(result)

        return ExecutionRun(

            plan_id=plan.plan_id,

            decision_id=plan.decision_id,

            event_id=plan.event_id,

            results=results,

        )

    ####################################################################
    #
    # Task Execution
    #
    ####################################################################

    def _execute_task(
        self,
        task,
    ) -> ExecutionResult:

        print(f"Executing Task: {task.task_type}")

        adapter = self.registry.get(task.task_type)

        return adapter.execute(task)
