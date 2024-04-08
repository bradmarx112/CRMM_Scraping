from typing import Optional, Type, Union
from abc import ABC

from utils.logging.google_sheets_agent import GoogleSheetsLoggingAgent
from utils.config import acrru_config
from langchain.agents import AgentExecutor



class ACRRU(ABC):
    def __init__(self, agent, tools: list, verbose: bool, return_intermediate_steps: bool, logger):
        self.agent = agent
        self.agent_executor = AgentExecutor(agent=self.agent, tools=tools, verbose=verbose, 
                                            return_intermediate_steps=return_intermediate_steps)
        self.logger = logger

    @abstractmethod
    def execute(self, args: dict) -> dict:
        ...


class ACRRUSummarizer(ACRRU):
    def __init__(self, agg_lvl: str):
        super(ACRRUSummarizer, self).__init__(**kwargs)
        self.agg_lvl = agg_lvl

    def execute(self, args: dict) -> dict:
        summary_output = self.agent_executor.invoke(args)

        return summary_output