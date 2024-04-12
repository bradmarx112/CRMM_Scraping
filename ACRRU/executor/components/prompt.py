from langchain_core.prompts import (ChatPromptTemplate, SystemMessagePromptTemplate, PromptTemplate,
                                    HumanMessagePromptTemplate, MessagesPlaceholder, MessagePromptTemplate)
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


def construct_react_prompt(sys_prompt: dict, human_prompt: dict) -> ChatPromptTemplate:

    sys_msg = SystemMessagePromptTemplate(prompt=PromptTemplate(**sys_prompt))
    human_msg = HumanMessagePromptTemplate(prompt=PromptTemplate(**human_prompt))

    # Define specific react template required for react agent
    react_msg = SystemMessagePromptTemplate(prompt=PromptTemplate(
        template='''TOOLS:
                    ------

                    You have access to the following tools:

                    {tools}

                    To use a tool, please use the following format:

                    ```
                    Thought: Do I need to use a tool? Yes
                    Action: the action to take, should be one of [{tool_names}]
                    Action Input: the input to the action
                    Observation: the result of the action
                    ```

                    When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:

                    ```
                    Thought: Do I need to use a tool? No
                    Final Answer: [your response here]
                    ```

                    Begin!

                    Previous conversation history:
                    {chat_history}''', 
        input_variables=["tools", "tool_names", "chat_history"]))
    
    acrru_chat_prompt = ChatPromptTemplate.from_messages([
        sys_msg, 
        react_msg,
        human_msg, 
        MessagesPlaceholder(variable_name='agent_scratchpad')
    ])

    return acrru_chat_react_prompt
