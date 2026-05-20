import os
from dotenv import load_dotenv  # type: ignore
from langchain_google_genai import ChatGoogleGenerativeAI  # type: ignore
from prompts.prompts import DB_SCHEMA, DECOMPOSE_PROMPT, GENERATE_SQL_PROMPT, FIX_SQL_PROMPT

load_dotenv()

# Gemini LLM — temperature 0 for deterministic SQL output
llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0,
)


def _get_text(response) -> str:
    """Pull plain text out of an LLM response regardless of its format."""
    content = response.content
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                return block.get("text", "")
            if isinstance(block, str):
                return block
    return str(content)


def decompose_question(question: str) -> str:
    """Step 1 — Break a natural language question into structured query components."""
    prompt = DECOMPOSE_PROMPT.format(schema=DB_SCHEMA, question=question)
    return _get_text(llm.invoke(prompt))


def generate_sql(question: str, decomposition: str) -> str:
    """Step 2 — Convert the structured breakdown into a PostgreSQL SELECT query."""
    prompt = GENERATE_SQL_PROMPT.format(
        schema=DB_SCHEMA,
        decomposition=decomposition,
        question=question,
    )
    return _get_text(llm.invoke(prompt))


def fix_sql(question: str, sql: str, error: str) -> str:
    """Step 3 — Repair a failed SQL query given the error message."""
    prompt = FIX_SQL_PROMPT.format(
        schema=DB_SCHEMA,
        sql=sql,
        error=error,
        question=question,
    )
    return _get_text(llm.invoke(prompt))


def generate_summary(question: str, result: list) -> str:
    """Step 4 — Summarize query results in one plain-English sentence."""
    prompt = f"""
You are a data analyst. Summarize the SQL result below in a single clear sentence.

Question: {question}
Result: {result}

Rules:
- One sentence only
- Include specific numbers if present
- No markdown, no extra explanation
"""
    return _get_text(llm.invoke(prompt))


if __name__ == "__main__":
    q = "Get customer names and cities"
    print(f"Question: {q}\n")
    decomp = decompose_question(q)
    print(f"Decomposition:\n{decomp}\n")
    sql = generate_sql(q, decomp)
    print(f"Generated SQL:\n{sql}")
