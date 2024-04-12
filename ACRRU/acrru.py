from collections import defaultdict

from ACRRU.executor.accru_executor import ACRRUExecutor

from utils.planning.aggregation_planner import ExecutionPlanner
from utils.config import acrru_config

from inputs.data_loader import ACRRULoader, ResearchLoader, SummaryLoader

RESEARCH_FLAG = acrru_config['hierarchy'][0]

class ACRRU:

    def __init__(self, executor: ACRRUExecutor, crmm_file: str, crmm_path: str=acrru_config['crmm_doc_path']):
        self.executor = executor
        self.crmm_file = crmm_file
        self.crmm_path = crmm_path

    def orchestrate(self, 
                    initial_loader: ACRRULoader, 
                    planner: ExecutionPlanner,
                    notes: str = '', 
                    save_results: bool = True):
        """
        Orchestrates the research and summarization tasks defined in initialization. 
        For every step in the execution planner, ACRRU will run its executor on all the data
        in the loader. If there are more steps remaining, the output data will be put into a 
        SummaryLoader, and the executor will run again at the next granularity.
        """

        run_step = planner.get_next_step()
        loader = initial_loader

        # Perform research step if necessary
        if run_step == RESEARCH_FLAG:
            acrru_output = self.research(loader, notes, save_results)
            
            # This will be None if there are no summary tasks
            run_step = planner.get_next_step()

            # Build loader from research results for downstream summary tasks
            if not planner.completed:
                loader = SummaryLoader(task=run_step,
                                       crmm_path=self.crmm_path,
                                       crmm_file=self.crmm_file,
                                       entities=acrru_output)
        
        # Perform summary step(s) if necessary
        if run_step:

            acrru_output = self.summarize(loader, planner, notes, save_results)

        return acrru_output

    def summarize(self, 
                  loader: SummaryLoader, 
                  planner: ExecutionPlanner,
                  notes: str, 
                  save_results: bool) -> dict:
        """
        Iteratively summarize previously generated results until the target aggregation level
        in the hierarchy is reached. 
        """

        self.executor.set_mode(mode='summary')

        while True:
            # Get ACRRU response
            summary_output = self._run(loader=loader, notes=notes)

            # Save response (TBD)
            if save_results:
                pass

            run_step = planner.get_next_step()

            if run_step:
                # Any additional step after the first MUST be a summary task.
                loader = SummaryLoader(task=run_step,
                                       crmm_path=self.crmm_path,
                                       crmm_file=self.crmm_file,
                                       entities=acrru_output)
            else:
                break
        
        return summary_output

    def research(self, research_loader: ResearchLoader, notes: str, save_results: bool) -> dict:
        self.executor.set_mode(mode='research')

        research_output = self._run(research_loader, notes)

        # Save response (TBD)
        if save_results:
            pass

        return research_output


    def _run(self, loader: ACRRULoader, notes: str) -> dict:
        """
        Runs the ACRRU executor over all provided data for one pass.
        """
        # Dictionary to return. key=entity name, value= list of ACRRU response related to that entity
        output_dict = defaultdict(list)

        for model_input in loader:
            output = self.executor.execute(model_input, task=loader.task, notes=notes)
            output_dict[model_input.org_name].append(output)

        return output_dict

    def _save_results(self):
        raise NotImplementedError
    