from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableBranch, RunnableParallel, RunnableLambda

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
# 2. RunnableBranch
# =========================

programming_chain = programming_prompt | llm
math_chain = math_prompt | llm
general_chain = general_prompt | llm


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


branch = RunnableBranch(
    (is_programming_question, programming_chain),
    (is_math_question, math_chain),
    general_chain,
)


# =========================
# 3. RunnableParallel
# =========================

summary_prompt = PromptTemplate.from_template(
    """
Give a short summary of this answer:

{answer}
"""
)

summary_chain = summary_prompt | llm


# First get the answer from the branch
answer_chain = RunnableParallel(
    question=lambda x: x["question"],
    answer=branch,
)


# Then create the summary using the answer
def add_summary(data):
    summary = summary_chain.invoke({
        "answer": data["answer"].content
    })

    return {
        "question": data["question"],
        "answer": data["answer"],
        "summary": summary,
    }


parallel_chain = answer_chain | RunnableLambda(add_summary)


# =========================
# 4. Pydantic Structured Output
# =========================

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
- summary: a short summary
- confidence: a number between 0 and 1
- category: Programming, Math, or General
- keywords: important keywords from the question
"""
)


# =========================
# 5. Final Chain
# =========================

final_chain = (
    parallel_chain
    | RunnableLambda(
        lambda x: {
            "question": x["question"],
            "answer": x["answer"].content,
            "summary": x["summary"].content,
        }
    )
    | structured_prompt
    | structured_llm
)


# =========================
# 6. Run
# =========================

if __name__ == "__main__":

    question = input("Ask a question: ")

    response = final_chain.invoke({
        "question": question
    })

    print("\nFinal Structured Response:")
    print(response)

