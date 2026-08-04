
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import (
    RunnableBranch,
    RunnableParallel,
)

from schemas import ChatResponse
from prompts import (
    programming_prompt,
    math_prompt,
    general_prompt,
)

load_dotenv()


# =========================
# 1. LLM
# =========================

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)


# =========================
# 2. Routing Functions
# =========================

def is_programming_question(data):
    question = data["question"].lower()

    programming_keywords = [
        "python",
        "programming",
        "code",
        "coding",
        "function",
        "variable",
        "class",
        "javascript",
        "java",
    ]

    return any(
        keyword in question
        for keyword in programming_keywords
    )


def is_math_question(data):
    question = data["question"].lower()

    math_keywords = [
        "math",
        "calculate",
        "equation",
        "algebra",
        "geometry",
        "multiply",
        "divide",
        "plus",
        "minus",
    ]

    return any(
        keyword in question
        for keyword in math_keywords
    )


# ==========================================================
# # Summary Prompts
# ==========================================================

programming_summary_prompt = PromptTemplate.from_template(
    """
Give a short summary of the key points that should be
covered when answering this programming question.

User Question:
{question}
"""
)

math_summary_prompt = PromptTemplate.from_template(
    """
Give a short summary of the key points that should be
covered when answering this mathematics question.

User Question:
{question}
"""
)

general_summary_prompt = PromptTemplate.from_template(
    """
Give a short summary of the key points that should be
covered when answering this general question.

User Question:
{question}
"""
)


# ==========================================================
# # RunnableParallel
#
# Each branch now generates TWO outputs in parallel:
# 1. Answer
# 2. Summary
# ==========================================================

programming_parallel = RunnableParallel(
    answer=programming_prompt | llm,
    summary=programming_summary_prompt | llm,
)

math_parallel = RunnableParallel(
    answer=math_prompt | llm,
    summary=math_summary_prompt | llm,
)

general_parallel = RunnableParallel(
    answer=general_prompt | llm,
    summary=general_summary_prompt | llm,
)


# ==========================================================
# # RunnableBranch
#
# RunnableBranch selects the appropriate parallel pipeline.
# ==========================================================

branch = RunnableBranch(
    (is_programming_question, programming_parallel),
    (is_math_question, math_parallel),
    general_parallel,
)


# ==========================================================
# 3. Pydantic Structured Output
# ==========================================================

structured_llm = llm.with_structured_output(ChatResponse)


structured_prompt = PromptTemplate.from_template(
    """
You are a helpful AI assistant.

Create a structured response using the information below.

User Question:
{question}

Answer:
{answer}

Summary:
{summary}

Return:
- answer: the main answer
- summary: a short summary of the answer
- confidence: a number between 0 and 1
- category: Programming, Math, or General
- keywords: important keywords from the question
"""
)


# ==========================================================
# 4. Final Chain
# ==========================================================

# #
# The branch already returns answer + summary.
# We now prepare those outputs for the structured model.

final_chain = (
    RunnableParallel(
        question=lambda x: x["question"],
        result=branch,
    )
    | RunnableParallel(
        question=lambda x: x["question"],
        answer=lambda x: x["result"]["answer"].content,
        summary=lambda x: x["result"]["summary"].content,
    )
    | structured_prompt
    | structured_llm
)


# =========================
# 5. Run
# =========================

if __name__ == "__main__":

    question = input("Ask a question: ")

    response = final_chain.invoke({
        "question": question
    })

    print("\nFinal Structured Response:")
    print(response)

