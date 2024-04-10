from dataclasses import dataclass


@dataclass
class ACRRUInput:
    crmm_info: str
    org_name: str

    def construct_input(self):
        return self.__dict__

@dataclass
class ResearchInput(ACRRUInput):
    cap_info: str

@dataclass
class SummaryInput(ACRRUInput):
    agg_lvl: str
    summaries: str
