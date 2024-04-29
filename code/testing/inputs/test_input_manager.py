import unittest
from collections import defaultdict

import os.path
import time
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from data_management.structure.data_loader import ResearchLoader, SummaryLoader
from data_management.structure.input import Entity, ResearchInput, SummaryInput


class TestResearchLoader(unittest.TestCase):
    def setUp(self):
        self.crmm_path = 'crmm_docs'
        self.crmm_file = 'CRMM_13'

        self.entity_dependency_list = [['org_1', 'sub_region_1', 'region_1'],
                                       ['org_2', 'sub_region_1', 'region_1'],
                                       ['org_3', 'sub_region_2', 'region_1'],
                                       ['org_4', 'sub_region_3', 'region_2'],
                                       ['org_5', 'sub_region_4', 'region_3']]

        self.capability_files = {"Capability 1": "Capability 1: Governance - Executive Level Engagement and Leadership",
                            "Capability 2": "Capability 2: Climate-Aware Planning",
                            "Capability 3": "Capability 3: Stakeholder and Community Collaboration",
                            "Capability 4": "Capability 4: Resilience and Adaptation Actions",
                            "Capability 5": "Capability 5: Customer Engagement and Coordination"}
    
    def test_read_capability_files(self):

        # Define expected dictionary format.
        expected_cap_dict = {key_str: 0 for key_str in self.capability_files.keys()}

        observed_cap_dict = ResearchLoader._read_capabilities(path=self.crmm_path, cap_file_names=self.capability_files)

        # Test keys are all there
        self.assertEqual(set([k for k in expected_cap_dict.keys()]), set([k for k in observed_cap_dict.keys()]))

        # Test that each is key is populated with a string
        self.assertTrue(all([len(obs_val) > 0 for obs_val in observed_cap_dict.values()]))

    def test_data_construction(self):
        
        entity_list = [Entity.from_dependency_chain(chain) for chain in self.entity_dependency_list]
        expected_data_size = 25
        entity_parent_set = set([chain.name for chain in entity_list])
        
        research_loader = ResearchLoader(capability_files=self.capability_files, 
                                         crmm_path=self.crmm_path, 
                                         crmm_file=self.crmm_file, 
                                         entities=entity_list)

        # Test data size: num_entities * num_capabilities
        self.assertEqual(len(research_loader), expected_data_size)

        # Test entities are defined properly, with lowest granularity entity assigned to parent of capability
        self.assertEqual(set([str(data.entity.parent) for data in research_loader.data]), entity_parent_set)

        # Test each element in data is ResearchInput type
        self.assertIsInstance(research_loader.data[0], ResearchInput)

        # Check if research_input is iterable
        self.assertTrue(iter(research_loader))

    def test_data_indexing(self):
        entity_list = [Entity.from_dependency_chain(chain) for chain in self.entity_dependency_list]
        
        cap_info = ResearchLoader._read_capabilities(path=self.crmm_path, cap_file_names=self.capability_files)
        with open(f'{self.crmm_path}/{self.crmm_file}.txt', "r", encoding='utf-8') as f:
            crmm = f.read()

        data_idx_0 = ResearchInput(crmm_info=crmm,
                                   entity=Entity(name="Capability 1", parent=entity_list[0]),
                                   cap_info=cap_info["Capability 1"])

        data_idx_7 = ResearchInput(crmm_info=crmm,
                                   entity=Entity(name="Capability 3", parent=entity_list[1]),
                                   cap_info=cap_info["Capability 3"])

        data_idx_25 = ResearchInput(crmm_info=crmm,
                                   entity=Entity(name="Capability 5", parent=entity_list[-1]),
                                   cap_info=cap_info["Capability 5"])
        
        research_loader = ResearchLoader(capability_files=self.capability_files, 
                                         crmm_path=self.crmm_path, 
                                         crmm_file=self.crmm_file, 
                                         entities=entity_list)

        # Test indexing
        self.assertEqual(research_loader[0], data_idx_0)
        self.assertEqual(research_loader[7], data_idx_7)
        self.assertEqual(research_loader[24], data_idx_25)

        # Test Iteration
        self.assertEqual(next(research_loader), data_idx_0)


class TestSummaryLoader(unittest.TestCase):
    def setUp(self):
        self.crmm_path = 'crmm_docs'
        self.crmm_file = 'CRMM_13'

        self.entity_dependency_list = [['org_1', 'sub_region_1', 'region_1'],
                                       ['org_2', 'sub_region_1', 'region_1'],
                                       ['org_3', 'sub_region_2', 'region_1'],
                                       ['org_4', 'sub_region_3', 'region_2'],
                                       ['org_5', 'sub_region_4', 'region_3']]
    
    def test_collect_reports(self):

        ## SETUP
        # Simulate report rollup from upstream process
        entity_list = [Entity.from_dependency_chain(chain) for chain in self.entity_dependency_list]

        output_dict = defaultdict(list)
        for model_input in entity_list:
            output = {'output': f'this is the output text for {model_input.name}'}
            output['topic'] = model_input.name
            output_dict[str(model_input.get_parent())].append(output)

        expected_string_multichild = """org_1\nthis is the output text for org_1\n\n\norg_2\nthis is the output text for org_2"""

        expected_string_singlechild = """org_3\nthis is the output text for org_3"""

        ## RUN 
        observed_string_multichild = SummaryLoader._collect_reports(reports=output_dict['sub_region_1'])
        observed_string_singlechild = SummaryLoader._collect_reports(reports=output_dict['sub_region_2'])

        ## TEST
        # output with multiple child reports
        self.assertEqual(expected_string_multichild, observed_string_multichild)

        # output with one child report
        self.assertEqual(expected_string_singlechild, observed_string_singlechild)

    def test_data_construction(self):
        
        ## SETUP
        # Simulate report rollup from upstream process
        entity_list = [Entity.from_dependency_chain(chain) for chain in self.entity_dependency_list]

        output_dict = defaultdict(list)
        for model_input in entity_list:
            output = {'output': f'this is the output text for {model_input.name}'}
            output['topic'] = model_input.name
            output_dict[model_input.get_parent()].append(output)

        expected_data_size = 4

        entity_parent_set = set([str(chain.get_parent().get_parent()) for chain in entity_list])
        
        ## RUN
        summary_loader = SummaryLoader(task='sub region', crmm_path=self.crmm_path, 
                                         crmm_file=self.crmm_file, 
                                         entities=output_dict)
        
        ## TEST
        # Test data size: num unique sub regions
        self.assertEqual(len(summary_loader), expected_data_size)

        # Test entities are defined properly, with most aggregate entity assigned to parent of new entity
        self.assertEqual(set([str(data.entity.parent) for data in summary_loader.data]), entity_parent_set)

        # Test each element in data is ResearchInput type
        self.assertIsInstance(summary_loader.data[0], SummaryInput)

        # Check if research_input is iterable
        self.assertTrue(iter(summary_loader))

    def test_data_indexing(self):

        ## SETUP
        # Simulate report rollup from upstream process
        entity_list = [Entity.from_dependency_chain(chain) for chain in self.entity_dependency_list]

        output_dict = defaultdict(list)
        for model_input in entity_list:
            output = {'output': f'this is the output text for {model_input.name}'}
            output['topic'] = model_input.name
            output_dict[model_input.get_parent()].append(output)
        
        with open(f'{self.crmm_path}/{self.crmm_file}.txt', "r", encoding='utf-8') as f:
            crmm = f.read()

        data_idx_0 = SummaryInput(crmm_info=crmm,
                                  agg_lvl='sub region',
                                  entity=Entity(name="sub_region_1", parent=entity_list[0].get_parent()),
                                  summaries=SummaryLoader._collect_reports(reports=output_dict[entity_list[0].get_parent()]))

        data_idx_2 = SummaryInput(crmm_info=crmm,
                                  agg_lvl='sub region',
                                  entity=Entity(name="sub_region_3", parent=entity_list[3].get_parent()),
                                  summaries=SummaryLoader._collect_reports(reports=output_dict[entity_list[3].get_parent()]))
        
        ## RUN
        summary_loader = SummaryLoader(task='sub region', 
                                         crmm_path=self.crmm_path, 
                                         crmm_file=self.crmm_file, 
                                         entities=output_dict)

        ## TEST
        # Test indexing
        self.assertEqual(summary_loader[0], data_idx_0)
        self.assertEqual(summary_loader[2], data_idx_2)

        # Test Iteration
        self.assertEqual(next(summary_loader), data_idx_0)


if __name__ == '__main__':
    unittest.main()
