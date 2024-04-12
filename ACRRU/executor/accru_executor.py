from typing import Optional, Type, Union
from abc import ABC
from inputs.input import ACRRUInput, ResearchInput, SummaryInput
from inputs.data_loader import ACRRULoader

from utils.logging.google_sheets_agent import GoogleSheetsLoggingAgent
from utils.config import acrru_config
from langchain.agents import AgentExecutor


class ACRRUExecutor:
    def __init__(self, research_agent, summary_agent, \
                 tools: list, verbose: bool, \
                 return_intermediate_steps: bool, logger):

        # Define executor dictionary that can be toggled in the get_mode method for either ACRRU task.
        self.agent_executor_dict = {'research': AgentExecutor(
                                                agent=self.research_agent, tools=tools, verbose=verbose, 
                                                return_intermediate_steps=return_intermediate_steps),

                                    'summary': AgentExecutor(
                                                agent=self.summary_agent, tools=tools, verbose=verbose, 
                                                return_intermediate_steps=return_intermediate_steps)}
        self.logger = logger
        self.agent_executor = None

    def set_mode(self, mode: str) -> None:
        """Toggles between the research executor and summary executor"""

        self.agent_executor = self.agent_executor_dict[mode]

    def execute(self, input_args: ACRRUInput, mode: str, task: str, notes: str) -> dict:
        args = input_args.construct_input()
        output = self.agent_executor.invoke(args)

        if self.logger:
            self.logger.log_response(self.agent, output, args, task, notes)

        return output