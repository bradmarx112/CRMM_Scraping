from langchain_core.prompts import (ChatPromptTemplate, SystemMessagePromptTemplate, PromptTemplate,
                                    HumanMessagePromptTemplate, MessagesPlaceholder)
from langchain.schema import AIMessage, HumanMessage, SystemMessage


def construct_openai_prompt(sys_prompt: dict, human_prompt: dict) -> ChatPromptTemplate:

    sys_msg = SystemMessagePromptTemplate(prompt=PromptTemplate(**sys_prompt))
    human_msg = HumanMessagePromptTemplate(prompt=PromptTemplate(**human_prompt))

    # OpenAI agents need placeholders for chat history and agent scratchpad.
    acrru_chat_prompt = ChatPromptTemplate.from_messages([
        sys_msg, 
        MessagesPlaceholder(variable_name='chat_history', optional=True),
        human_msg, 
        MessagesPlaceholder(variable_name='agent_scratchpad')
    ])

    return acrru_chat_prompt

# Define dictionary that holds prompt generation function to use based on user-chosen LLM. 
llm_prompt_func_mapping = {'openai': construct_openai_prompt}