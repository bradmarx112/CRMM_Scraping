from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, initialize_agent, create_openai_tools_agent, create_self_ask_with_search_agent, AgentType, create_react_agent
from langchain_core.prompts import ChatPromptTemplate


def construct_openai_agent(tools: list, prompt: ChatPromptTemplate, llm_name: str, llm_temp: float):
    openai_llm = ChatOpenAI(model=llm_name, temperature=llm_temp)

    openai_agent = create_openai_tools_agent(openai_llm, tools, prompt)

    return openai_agent