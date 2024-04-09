from utils.config import acrru_config
from abc import ABC, abstractmethod


class ACRRUInput(ABC):
    def __init__(self, crmm_path: str, crmm_file: str, entities):
        
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
    

class ResearchInput(ACRRUInput):
    def __init__(self, capability_files: dict, crmm_path: str, crmm_file: str, entities):
        self.capability_dict = self._read_capabilities(crmm_path, capability_files)
        super(ResearchInput, self).__init__(crmm_path, crmm_file, entities)

    def construct_input(self, entities: list) -> list:
        # Input as list of dicts: each list element is dict of dicts for each capability
        input_list = []
        for entity in entities:
            input_list.append({capability: {
                'crmm_info': self.crmm, 
                'org_name': entity,
                'cap_info': cap_desc} 
            for capability, cap_desc in self.capability_dict.items()
            })

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


class SummaryInput(ACRRUInput):
    def __init__(self, agg_lvl: str, **kwargs):
        self.agg_lvl = agg_lvl
        super(SummaryInput, self).__init__(**kwargs)

    def construct_input(self, entities: dict) -> list:
        # Input as list of dicts: each list element is dict of inputs for agent executor run
        input_list = []
        for entity_name, reports in entities.items():
            input_list.append({
                'crmm_info': self.crmm,
                'agg_lvl': self.agg_lvl,
                'org_name': entity_name,
                'summaries': self._collect_reports(reports)})

        return input_list

    @staticmethod
    def _collect_reports(reports: dict) -> str:
        # Report dict structure: {[granular domain of report]: [text of report itself]}
        report_val_list = []
        for domain, report in reports.items():
            report_section = domain + '\n' + report
            report_val_list.append(report_section)

        fmt_rpt = '\n\n\n'.join(report_val_list)

        return fmt_rpt