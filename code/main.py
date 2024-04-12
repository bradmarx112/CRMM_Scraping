import os
import argparse

from ACRRU.acrru import ACRRU


def parse_args(args=None):
    """ 
    Perform command-line argument parsing (other otherwise parse arguments with defaults). 
    To parse in an interative context (i.e. in notebook), add required arguments.
    These will go into args and will generate a list that can be passed in.
    For example: 
        parse_args('--start_step', 'research', ...)
    """
    parser = argparse.ArgumentParser(description="Let's train some neural nets!", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--start_step',           required=True,              choices=["research", "capability", "provider"],     help='The hierarchy level from where execution begins')
    parser.add_argument('--end_step',           required=True,              choices=["provider", "region",],  help='The hierarchy level to which to summarize')
    parser.add_argument('--model_type',           required=True,            choices=["openai"],  help='LLM to use in ACCRU')
    parser.add_argument('--agent_type',           required=True,            choices=["openai", "react"],  help='agent type to use in ACCRU')
    parser.add_argument('--verbose',         type=bool,   default=True,      help='Controls output printed during run')
    parser.add_argument('--config_path',      type=str,   default='inputs/acrru_config.json', help='Path to ACRRU config file')

    if args is None: 
        return parser.parse_args()      ## For calling through command line
    return parser.parse_args(args)      ## For calling through notebook.