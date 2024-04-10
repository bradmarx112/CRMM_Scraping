import unittest

import os.path
import time
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from inputs.data_loader import ResearchLoader, SummaryLoader

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
        
    def test_research_loader(self):
        
        research_loader = ResearchLoader(capability_files=self.capability_files, crmm_path=self.crmm_path, crmm_file=self.crmm_file, entities=self.entities)

        # Check if research_input is iterable
        self.assertTrue(iter(research_loader))

        # Test indexing
        self.assertEqual(research_loader[0].org_name, 'entity1')
        self.assertEqual(research_loader[1].org_name, 'entity1')
        self.assertEqual(research_loader[5].org_name, 'entity2')

    def test_summary_loader(self):
        agg_lvl = 'provider'
        summary_loader = SummaryLoader(agg_lvl=agg_lvl, crmm_path=self.crmm_path, crmm_file=self.crmm_file, entities={'entity1': {'domain1': 'report1'}, 'entity2': {'domain2': 'report2'}})

        # Check if summary_input is iterable
        self.assertTrue(iter(summary_loader))

        # Test indexing
        self.assertEqual(summary_loader[0].org_name, 'entity1')
        self.assertEqual(summary_loader[1].org_name, 'entity2')

    def test_invalid_index(self):
        research_loader = ResearchLoader(capability_files=self.capability_files, crmm_path=self.crmm_path, crmm_file=self.crmm_file, entities=self.entities)

        # Test accessing out of bounds index
        with self.assertRaises(IndexError):
            research_loader[len(research_loader)]

if __name__ == '__main__':
    unittest.main()
