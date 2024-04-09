import unittest

import os.path
import time
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from inputs.input_manager import ResearchInput, SummaryInput

class TestACRRUInput(unittest.TestCase):
    def setUp(self):
        self.crmm_path = 'crmm_docs'
        self.crmm_file = 'CRMM_13'
        self.entities = ['entity1', 'entity2']
        self.capability_files = {"Capability 1": "Capability 1: Governance - Executive Level Engagement and Leadership",
                            "Capability 2": "Capability 2: Climate-Aware Planning",
                            "Capability 3": "Capability 3: Stakeholder and Community Collaboration",
                            "Capability 4": "Capability 4: Resilience and Adaptation Actions",
                            "Capability 5": "Capability 5: Customer Engagement and Coordination"}
        
    def test_research_input(self):
        
        research_input = ResearchInput(capability_files=self.capability_files, crmm_path=self.crmm_path, crmm_file=self.crmm_file, entities=self.entities)

        # Check if research_input is iterable
        self.assertTrue(iter(research_input))

        # Test indexing
        self.assertEqual(research_input[0]['Capability 1']['org_name'], 'entity1')
        self.assertEqual(research_input[1]['Capability 2']['org_name'], 'entity2')

    def test_summary_input(self):
        agg_lvl = 'provider'
        summary_input = SummaryInput(agg_lvl=agg_lvl, crmm_path=self.crmm_path, crmm_file=self.crmm_file, entities={'entity1': {'domain1': 'report1'}, 'entity2': {'domain2': 'report2'}})

        # Check if summary_input is iterable
        self.assertTrue(iter(summary_input))

        # Test indexing
        self.assertEqual(summary_input[0]['org_name'], 'entity1')
        self.assertEqual(summary_input[1]['org_name'], 'entity2')

    def test_invalid_index(self):
        research_input = ResearchInput(capability_files=self.capability_files, crmm_path=self.crmm_path, crmm_file=self.crmm_file, entities=self.entities)

        # Test accessing out of bounds index
        with self.assertRaises(IndexError):
            research_input[len(research_input)]

if __name__ == '__main__':
    unittest.main()
