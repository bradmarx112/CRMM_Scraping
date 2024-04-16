import pandas as pd

from utils.config import acrru_config

from data_management.structure.data_loader import ResearchLoader, SummaryLoader, ACRRULoader


def compile_electricity_providers(entity_path: str, coverage_path: str) -> pd.DataFrame:
    # Get list of electricity providers
    elec_industry_df = pd.read_csv(entity_path)
    # Get list of the territory electricity providers service. At the State/County level.
    service_territory_df = pd.read_csv(coverage_path)

    service_territory_df = service_territory_df.drop(
        [col for col in service_territory_df.columns if col not in ['Utility Number', 'State', 'County']], axis=1).reset_index(drop=True)

    # Only look at investor owned companies for now!
    investor_utils = elec_industry_df[elec_industry_df['Ownership'] == 'Investor Owned']
    # Drop some columns
    investor_utils = investor_utils.drop(
        [col for col in investor_utils.columns if col not in ['Utility Number', 'Utility Name']], axis=1).reset_index(drop=True)

    # Join investor owned utils with their reported coverage
    investor_util_coverage = investor_utils.merge(service_territory_df, on='Utility Number', how='inner')

    return investor_util_coverage


def create_loader_from_local(model_file_name: str, 
                             local_data_folder: str = acrru_config['local_file_path'],
                             research_requested: bool=False) -> ACRRULoader:
    '''
    Generates an ACRRULoader object for an arbitrary ACRRU run for entity data stored locally in a 
    .txt file. Creates a ResearchLoader when research_requested=True, or a SummaryLoader otherwise.

    The model description for the loader is specified by model_file_name. 
    '''
    
    # TODO: add logic for locally saved summary data
    entity_dict = {}
    if research_requested:
        target_file_name = 'research' 
        with open(f'.\\{local_data_folder}\\{target_file_name}_entities.txt', 'r') as f:
            for line in f:
                entity_dict[line] = None
        
        loader = ResearchLoader(capability_files=acrru_config['capabilities'], 
                                crmm_path=acrru_config['crmm_doc_path'],
                                crmm_file=model_file_name,
                                entities=entity_dict)
    else:
        target_file_name = 'summary'

    return loader

