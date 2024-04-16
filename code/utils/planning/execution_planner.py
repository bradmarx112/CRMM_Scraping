from utils.config import acrru_config


class HierarchyMismatchError(Exception): 
    def __init__(self, start, end, message="Improper order of aggregation requested."):
        self.start = start
        self.end = end
        self.message = f'{message} {start} does not come before {end}.'
        super().__init__(self.message)


class ExecutionPlanner:
    summary_hierarchy = {level: i for i, level in enumerate(acrru_config['hierarchy'])}

    def __init__(self, initial_step, end_step):
        self.execution_plan = self._construct_dependency_stack(initial_step, end_step)

    @property
    def completed(self):
        return self.execution_plan == []

    def _construct_dependency_stack(self, initial_step, end_step) -> list:
        # Make sure start gran is a dependency of target gran.
        if type(self).summary_hierarchy[initial_step] >= type(self).summary_hierarchy[end_step]:
            raise HierarchyMismatchError(initial_step, end_step)

        # Index portion of hierarchy list bookended by start and target granularity.
        stack = acrru_config['hierarchy'][type(self).summary_hierarchy[initial_step] + 1: \
                                          type(self).summary_hierarchy[end_step] + 1]

        return stack

    def get_next_step(self):
        next_agg = None
        if self.execution_plan:
            next_agg = self.execution_plan.pop(0)
        
        return next_agg

