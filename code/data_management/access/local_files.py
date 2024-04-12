import pandas as pd

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