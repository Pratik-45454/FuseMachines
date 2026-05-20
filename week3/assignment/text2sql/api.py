from fastapi import FastAPI, HTTPException  # type: ignore
from pydantic import BaseModel, field_validator  # type: ignore
from main import build_pipeline
from sql_generator import generate_summary

app = FastAPI(title="Text-to-SQL Agent", version="1.0")
pipeline = build_pipeline()


class Question(BaseModel):
    question: str

    @field_validator("question")
    @classmethod
    def must_not_be_empty(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Question cannot be empty.")
        if len(v) > 1000:
            raise ValueError("Question is too long (max 1000 characters).")
        return v


@app.get("/")
def health_check():
    return {"status": "running", "message": "Text-to-SQL Agent is live"}


@app.post("/agent/sql")
async def run_sql_agent(request: Question):
    initial_state = {
        "question": request.question,
        "decomposition": "",
        "sql": "",
        "execution_result": {},
        "retry_count": 0,
        "status": "",
        "error": None,
    }

    final_state = pipeline.invoke(initial_state)
    status = final_state["status"]
    result = final_state["execution_result"].get("result", [])

    summary = (
        generate_summary(request.question, result)
        if status == "success"
        else "Query failed after maximum retries."
    )

    return {
        "sql": final_state["sql"],
        "result": result,
        "summary": summary,
        "status": status,
    }
