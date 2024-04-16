from langchain.tools import BraveSearch, BaseTool, StructuredTool, tool

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.utilities.tavily_search import TavilySearchAPIWrapper

from utils.config import acrru_config

search = TavilySearchAPIWrapper()
tavily_tool = TavilySearchResults(api_wrapper=search, **acrru_config['tools']['tavily'])

brave_tool = BraveSearch.from_api_key(api_key=acrru_config['BRAVE_API_KEY'], search_kwargs=acrru_config['tools']['brave'], 
                description='a search engine. useful to use when other tools do not return results.')

active_tools = [tavily_tool]