import os
import argparse

from utils.config import acrru_config
from utils.logging.google_sheets_agent import GoogleSheetsLoggingAgent
from utils.planning.execution_planner import ExecutionPlanner

from data_management.structure.data_loader import ResearchLoader, SummaryLoader
from data_management.access.local_files import create_loader_from_local

from ACRRU.executor.components.agent import llm_agent_func_mapping
from ACRRU.executor.components.tools import active_tools
from ACRRU.executor.accru_executor import ACRRUExecutor

from ACRRU.acrru import ACRRU


def parse_args(args=None):
    """ 
    Perform command-line argument parsing (other otherwise parse arguments with defaults). 
    To parse in an interative context (i.e. in notebook), add required arguments.
    These will go into args and will generate a list that can be passed in.
    For example: 
        parse_args('--initial_step', 'research', ...)
    """
    parser = argparse.ArgumentParser(description="Parameters for a single ACRRU run.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--initial_step',           required=True,              choices=["research", "capability", "provider"],     help='The hierarchy level from where execution begins')
    parser.add_argument('--end_step',           required=True,              choices=["capability", "provider", "region",],  help='The hierarchy level to which to summarize')
    parser.add_argument('--model_type',           required=True,            choices=["openai"],  help='LLM to use in ACCRU')
    parser.add_argument('--agent_type',           required=True,            choices=["openai", "react"],  help='Agent type to use in ACCRU')
    parser.add_argument('--data_source',         type=str,   required=True,      choices=["local", "db"], help='Controls data source of entities to evaluate')
    parser.add_argument('--model_file_name',   type=str, required=True,    help='The model description text to use in agent prompts.')
    parser.add_argument('--verbose',          type=bool,  default=True,      help='Controls output printed during run')
    # parser.add_argument('--config_path',      type=str,   default='inputs/acrru_config.json', help='Path to ACRRU config file')
    parser.add_argument('--gsheet_log',       type=bool,  default=True,      help='Controls logging output to Google Sheets record')
    parser.add_argument('--notes',            type=str,   default='',      help='Notes to include in metadata or logging for the given run.')
    parser.add_argument('--save_results',     type=bool,   default=True,      help='Controls saving output to database.')
    parser.add_argument('--execution_cooldown',     type=int,   default=5,      help='Number of seconds to wait between entity executions.')
    if args is None: 
        return parser.parse_args()      ## For calling through command line
    return parser.parse_args(args)      ## For calling through notebook.


def main(args):
    research_requested = args.initial_step == 'research'
    
    # Build starting data loader for run
    if args.data_source == 'local':
        initial_loader = create_loader_from_local(local_data_folder=acrru_config['local_file_path'], 
                                                  research_requested=research_requested,
                                                  model_file_name=args.model_file_name)

    # Define configs of interest
    model_config = acrru_config['models'][args.model_type]
    prompt_config = acrru_config['prompts']

    # Construct Langchain agents for research and summary
    target_agent_func = llm_agent_func_mapping[args.agent_type]

    research_agent = target_agent_func(active_tools, llm_name=model_config['model_name'],
                                    llm_temp=model_config['model_temp'], 
                                    sys_prompt=prompt_config['sys_msgs']['sys_research'],
                                    human_prompt=prompt_config['human_msgs']['hmn_research'])
    summary_agent = target_agent_func(active_tools, llm_name=model_config['model_name'],
                                    llm_temp=model_config['model_temp'], 
                                    sys_prompt=prompt_config['sys_msgs']['sys_summary'],
                                    human_prompt=prompt_config['human_msgs']['hmn_summary'])

    # Construct Google Sheets Logger if requested
    if args.gsheet_log:
        logger = GoogleSheetsLoggingAgent(cred_path=acrru_config['GSHEETS_ACCT_CRED_PATH'],
                                          file_name=acrru_config['logging']['gsheets']['filename'],
                                          tab_name=acrru_config['logging']['gsheets']['tabname'])
    else:
        logger = None

    # Construct ACRRU Executor
    executor = ACRRUExecutor(research_agent=research_agent, summary_agent=summary_agent, tools=active_tools,
                             verbose=args.verbose, return_intermediate_steps=True, logger=logger)

    # Construct execution planner
    planner = ExecutionPlanner(initial_step=args.initial_step, end_step=args.end_step)

    # Construct ACRRU 
    acrru = ACRRU(executor=executor, crmm_file=args.model_file_name, execution_cooldown=args.execution_cooldown)

    # Run ACRRU for all requested research and summary steps
    final_acrru_output = acrru.orchestrate(initial_loader=initial_loader,
                                           planner=planner,
                                           notes=args.notes,
                                           save_results=args.save_results)

if __name__ == '__main__':
    main(parse_args(("--initial_step", "research", "--end_step", "region", "--model_type", "openai", "--agent_type", "openai", "--data_source", "local", "--model_file_name", "CRMM_Header", "--notes", "Milwaukee City Testing", "--execution_cooldown", "3")))
