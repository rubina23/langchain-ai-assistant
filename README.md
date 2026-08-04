# LangChain Chatboat

A structured AI assistant built with LangChain, Groq, Pydantic, and Streamlit.

The application automatically identifies whether a user's question is related to Programming, Math, or General topics and routes the question to the appropriate workflow.

## Features

- Programming question handling
- Math question handling
- General question handling
- Conditional routing with `RunnableBranch`
- Parallel execution with `RunnableParallel`
- Structured AI output using Pydantic
- Chat history using Streamlit session state
- Confidence score
- Question category
- Important keywords
- Interactive Streamlit UI
- Groq LLM integration

## Technologies Used

- Python
- LangChain
- LangChain Groq
- Groq
- Pydantic
- Streamlit
- python-dotenv
---

## LangChain Architecture

The application follows this workflow:
```

User Question
      ↓
RunnableBranch
      ↓
┌────────────┬──────────┬───────────┐
│Programming │  Math    │  General  │
└────────────┴──────────┴───────────┘
      ↓
RunnableParallel
      ↓
┌───────────────┬───────────────┐
│  Main Answer  │    Summary    │
└───────────────┴───────────────┘
      ↓
Structured Output
      ↓
Pydantic ChatResponse
      ↓
Streamlit UI

```

---

## Project Structure

```text
langchain_chatbot/
│
├── app.py
├── chatbot.py
├── prompts.py
├── schemas.py
│
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md

```
---

📄 File Description
```
app.py
```
Contains the Streamlit user interface and chat history.

```
chatbot.py
```
Contains the main LangChain workflow including:

- ChatGroq
- RunnableBranch
- RunnableParallel
- Structured output
- Final chain

```
prompts.py
```
Contains the prompts for:

- Programming
- Math
- General questions

```
schemas.py
```

Contains the Pydantic ChatResponse model used for structured AI output.

```
.env
```

Stores the Groq API key. Do not upload this file to GitHub.

```
.env.example
```
Provides an example environment variable format without exposing the real API key.

---

## ⚙️ Installation
1. Clone the repository
```
git clone https://github.com/rubina23/langchain-ai-assistant.git
cd langchain-ai-assistant
```

2. Create a virtual environment
```
python -m venv .venv
```

3. Activate the virtual environment

Windows PowerShell:
```
.venv\Scripts\Activate.ps1
```

4. Install dependencies
```
pip install -r requirements.txt
```

5. Create .env

Create a .env file in the project root:

```
GROQ_API_KEY=your_actual_groq_api_key
```

## ▶️ Run the Application

Start the Streamlit application:
```
streamlit run app.py
```
The application will open in your browser.

## Example Questions
Programming
```
What is a Python function?
```

Math
```
What is an algebraic equation?
```

General
```
What is the capital of Bangladesh?
```
---
## 📊 Structured Response

The application produces structured responses containing:

Answer
Summary
Confidence
Category
Keywords

Example:

```
Answer: A Python function is a reusable block of code...

Summary: A Python function is a reusable block of code.

Confidence: 99%

Category: Programming

Keywords:
Python, function, programming, code
```

## 🔀 Conditional Routing

RunnableBranch determines which workflow should process the question.

```
Programming → Programming Chain
Math        → Math Chain
Other       → General Chain
```

---


## ⚡Parallel Processing

RunnableParallel processes the answer and summary workflows in parallel.
```

                RunnableParallel
                 /             \
              Answer         Summary
```

## 🔐 Environment Variables

The application requires:
```
GROQ_API_KEY=your_groq_api_key
```
Never expose the real API key publicly.

