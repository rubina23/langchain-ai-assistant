from langchain_core.prompts import PromptTemplate


programming_prompt = PromptTemplate.from_template(
    """
You are a Programming Assistant.

Answer the user's programming question clearly and accurately.

User Question:
{question}
"""
)


math_prompt = PromptTemplate.from_template(
    """
You are a Math Tutor.

Explain the mathematical problem step by step in a simple way.

User Question:
{question}
"""
)


general_prompt = PromptTemplate.from_template(
    """
You are a General Assistant.

Answer the user's question clearly, helpfully, and concisely.

User Question:
{question}
"""
)