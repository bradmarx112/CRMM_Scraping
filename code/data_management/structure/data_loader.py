from utils.config import acrru_config
from data_management.structure.input import ResearchInput, SummaryInput
from abc import ABC, abstractmethod
from typing import List


class ACRRULoader(ABC):
    def __init__(self, task, crmm_path: str, crmm_file: str, entities: dict):
        
        self.task = task
        self.crmm = self._read_crmm(crmm_path, crmm_file)
        self.data = self.construct_input(entities)
        self.index = 0

    @staticmethod
    def _read_crmm(path, file) -> str:
        with open(f'{path}/{file}.txt', "r", encoding='utf-8') as f:
            crmm = f.read()
        
        return crmm

    def __iter__(self):
        return self

    def __getitem__(self, index):
        return self.data[index]

    def __next__(self):
        if self.index < len(self.data):
            result = self.data[self.index]
            self.index += 1
            return result
        else:
            self.index = 0  # Reset index for next iteration
            raise StopIteration
    
    def __len__(self):
        return len(self.data)

    @abstractmethod
    def construct_input(self, entities: list):
        ...


class ResearchLoader(ACRRULoader):
    def __init__(self, capability_files: dict, crmm_path: str, crmm_file: str, entities: dict):
        self.capability_dict = self._read_capabilities(crmm_path, capability_files)
        super(ResearchLoader, self).__init__('research', crmm_path, crmm_file, entities)

    def construct_input(self, entities: dict) -> List[ResearchInput]:
        # Input as list of ResearchInput Dataclasses: each list element is input object for each capability
        # Input length = num. entities * num. capabilities
        input_list = []
        for entity in entities.keys():
            input_list.extend(
                ResearchInput(**{
                'crmm_info': self.crmm, 
                'org_name': entity,
                'cap_info': cap_desc})
            for capability, cap_desc in self.capability_dict.items()
            )

        return input_list

    @staticmethod
    def _read_capabilities(path: str, cap_file_names: dict) -> dict:
        cap_dict = {}
        # Read each CRMM Capability description text file, and store them in a dictionary
        for cap_file_name in cap_file_names.keys():
            with open(f'{path}/{cap_file_name}.txt', "r", encoding='utf-8') as f:
                cap = f.read()
            cap_dict[cap_file_name] = cap

        return cap_dict


class SummaryLoader(ACRRULoader):
    def __init__(self, **kwargs):
        super(SummaryLoader, self).__init__(**kwargs)
        self.task = task.capitalize() + ' Summary'

    def construct_input(self, entities: dict) -> List[SummaryInput]:
        # Input as list of SummaryInput Dataclasses: each list element is input object for agent executor run
        input_list = []
        for entity_name, data in entities.items():
            input_list.append(
                SummaryInput(**{
                'crmm_info': self.crmm,
                'agg_lvl': self.agg_lvl,
                'org_name': entity_name,
                'summaries': self._collect_reports(data)})
                )

        return input_list

    @staticmethod
    def _collect_reports(reports: dict) -> str:
        # Report dict structure: {[granular domain of report]: [Agent output of prev granularity]}
        report_val_list = []
        for domain, report in reports.items():
            report_section = domain + '\n' + report['output']
            report_val_list.append(report_section)

        fmt_rpt = '\n\n\n'.join(report_val_list)

        return fmt_rpt