
from utils.config import acrru_config
import time
import gspread


class GoogleSheetsLoggingAgent:

    def __init__(self, cred_path: str, file_name: str, tab_name: int):
        self.gsheet_connection = gspread.service_account(filename=cred_path)
        self.sheet_file = self.gsheet_connection.open(title=file_name)
        self.spreadsheet = self.sheet_file.get_worksheet(index=tab_name)

    def log_response(self, agent, agent_output, test_input_dict: dict, task: str, notes: str) -> None:

        log_data = self._collect_log_data(agent, agent_output, test_input_dict, task, notes)
        self._append_to_sheet(log_data)

    def _append_to_sheet(self, data: list) -> None:
        """
        Helper function which appends a list of values to the next available row of a specified Google Sheets tab.
        """

        if isinstance(data[0], list):
            for row in data:
                self.spreadsheet.append_row(row)
        
        else:
            self.spreadsheet.append_row(data)

    # Collect data to log 
    def _collect_log_data(self, agent, agent_output, test_input_dict: dict, task: str, notes: str) -> list:
        """
        Compiles all information about a provided ACRRU research output to be logged into a list. 
        """
        # Get timestamp
        cur_time = time.ctime(time.time())
        # Get intermediate queries the model called itself
        int_steps = '\n\n'.join([int_step[0].log.strip() for int_step in agent_output['intermediate_steps']])
        # Get the input template
        template = '\n'.join([f'{input_value.content}' for input_value in agent.steps[1].format_messages(**test_input_dict, agent_scratchpad=['']) if input_value.__class__.__name__ == 'SystemMessage'])
        # Get the input prompt
        prompt = '\n'.join([f'{input_value.content}' for input_value in agent.steps[1].format_messages(**test_input_dict, agent_scratchpad=['']) if input_value.__class__.__name__ == 'HumanMessage'])

        # Return a list of everything!
        return [cur_time, test_input_dict['org_name'], task, notes, 
            template, prompt, int_steps, agent_output['output']]