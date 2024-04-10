from typing import Optional, Type, Union
from abc import ABC
from inputs.input import ACRRUInput, ResearchInput, SummaryInput
from inputs.data_loader import ACRRULoader

from utils.logging.google_sheets_agent import GoogleSheetsLoggingAgent
from utils.config import acrru_config
from langchain.agents import AgentExecutor


class ACRRU(ABC):
    def __init__(self, agent, tools: list, verbose: bool, return_intermediate_steps: bool, logger):
        self.agent = agent
        self.agent_executor = AgentExecutor(agent=self.agent, tools=tools, verbose=verbose, 
                                            return_intermediate_steps=return_intermediate_steps)
        self.logger = logger

    def execute(self, input: SummaryInput) -> dict:
        args = input.construct_input()
        summary_output = self.agent_executor.invoke(args)

        return summary_output

    def run(self, loader: ACRRULoader, log_response: bool = True, notes: str = ''):

        for model_input in loader:
            summary_output = self.execute(model_input)

            if log_response:
                self.logger.log_response(self.agent, 
                                         summary_output, 
                                         model_input.construct_input(),
                                         loader.task,
                                         notes)

    def _save_results(self):
        raise NotImplementedError