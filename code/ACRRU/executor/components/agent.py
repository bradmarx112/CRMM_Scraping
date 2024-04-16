from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, initialize_agent, create_openai_tools_agent, create_react_agent, AgentType
from langchain_core.prompts import ChatPromptTemplate

from ACRRU.executor.components.prompt import construct_openai_prompt, construct_react_prompt


def construct_openai_agent(tools: list, llm_name: str, llm_temp: float,
                            sys_prompt: dict, human_prompt: dict):
                            
    openai_llm = ChatOpenAI(model=llm_name, temperature=llm_temp)
    prompt = construct_openai_prompt(sys_prompt, human_prompt)

    openai_agent = create_openai_tools_agent(openai_llm, tools, prompt)

    return openai_agent

def construct_react_agent(tools: list, llm_name: str, llm_temp: float,
                            sys_prompt: dict, human_prompt: dict):

    openai_llm = ChatOpenAI(model=llm_name, temperature=llm_temp)
    prompt = construct_react_prompt(sys_prompt, human_prompt)

    react_agent = create_react_agent(openai_llm, tools, prompt)

    return react_agent


# Define dictionary that holds agent generation function to use based on user choice. 
llm_agent_func_mapping = {'openai': construct_openai_agent,
                           'react': construct_react_agent}