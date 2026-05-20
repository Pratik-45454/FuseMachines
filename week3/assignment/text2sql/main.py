from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END  # type: ignore
from sql_generator import decompose_question, generate_sql, fix_sql
from executor import execute_sql
from validator import clean_sql
from dotenv import load_dotenv  # type: ignore

load_dotenv()

MAX_RETRIES = 3


# ── Pipeline state shared across all nodes ────────────────────────────────────

class PipelineState(TypedDict):
    question: str
    decomposition: str
    sql: str
    execution_result: dict
    retry_count: int
    status: str
    error: Optional[str]


# ── Nodes ─────────────────────────────────────────────────────────────────────

def decompose_node(state: PipelineState) -> PipelineState:
    """Node 1: Break the question into structured components."""
    print(f"\n[INFO] Decomposing: {state['question']}")
    decomposition = decompose_question(state["question"])
    print(f"[INFO] Decomposition:\n{decomposition}")
    return {**state, "decomposition": decomposition}


def generate_sql_node(state: PipelineState) -> PipelineState:
    """Node 2: Turn the decomposition into a SQL query."""
    print("\n[INFO] Generating SQL...")
    sql = generate_sql(state["question"], state["decomposition"])
    sql = clean_sql(sql)
    print(f"[INFO] SQL:\n{sql}")
    return {**state, "sql": sql}


def execute_node(state: PipelineState) -> PipelineState:
    """Node 3: Run the SQL against PostgreSQL."""
    print("\n[INFO] Executing SQL...")
    result = execute_sql(state["sql"], state["question"], state["retry_count"])
    print(f"[INFO] Status: {result['status']}")
    if result["error"]:
        print(f"[ERROR] {result['error']}")
    return {
        **state,
        "execution_result": result,
        "status": result["status"],
        "error": result["error"],
    }


def retry_node(state: PipelineState) -> PipelineState:
    """Node 4: Ask Gemini to fix the SQL, then try again."""
    attempt = state["retry_count"] + 1
    print(f"\n[INFO] Retry attempt {attempt}...")
    fixed = fix_sql(state["question"], state["sql"], state["error"])
    fixed = clean_sql(fixed)
    print(f"[INFO] Fixed SQL:\n{fixed}")
    return {**state, "sql": fixed, "retry_count": attempt}


def output_node(state: PipelineState) -> PipelineState:
    """Node 5: Print a summary of what happened."""
    result = state["execution_result"]
    sep = "=" * 60
    print(f"\n{sep}\nFINAL OUTPUT\n{sep}")
    print(f"Question : {state['question']}")
    print(f"SQL      : {state['sql']}")
    print(f"Status   : {state['status']}")
    print(f"Retries  : {state['retry_count']}")
    if result.get("result"):
        print(f"Results  : {len(result['result'])} rows returned")
        for row in result["result"][:3]:
            print(f"  -> {row}")
    else:
        print(f"Error    : {state['error']}")
    print(sep)
    return state


# ── Routing logic after execution ─────────────────────────────────────────────

def route_after_execution(state: PipelineState) -> str:
    """
    After executing SQL:
    - success → output
    - failed + retries left → retry
    - failed + max retries hit → output anyway
    """
    if state["status"] == "success":
        return "output"
    if state["retry_count"] < MAX_RETRIES:
        return "retry"
    print("\n[WARNING] Max retries reached.")
    return "output"


# ── Graph assembly ────────────────────────────────────────────────────────────

def build_pipeline():
    graph = StateGraph(PipelineState)

    graph.add_node("decompose", decompose_node)
    graph.add_node("generate_sql", generate_sql_node)
    graph.add_node("execute", execute_node)
    graph.add_node("retry", retry_node)
    graph.add_node("output", output_node)

    graph.set_entry_point("decompose")
    graph.add_edge("decompose", "generate_sql")
    graph.add_edge("generate_sql", "execute")
    graph.add_edge("retry", "execute")
    graph.add_edge("output", END)

    graph.add_conditional_edges(
        "execute",
        route_after_execution,
        {"output": "output", "retry": "retry"},
    )

    return graph.compile()


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    pipeline = build_pipeline()

    # Save pipeline diagram
    graph_image = pipeline.get_graph().draw_mermaid_png()
    with open("pipeline_graph.png", "wb") as f:
        f.write(graph_image)
    print("Graph saved as pipeline_graph.png")

    test_questions = [
        "List all products",
        "Get orders with customer names",
    ]

    for question in test_questions:
        initial_state = {
            "question": question,
            "decomposition": "",
            "sql": "",
            "execution_result": {},
            "retry_count": 0,
            "status": "",
            "error": None,
        }
        pipeline.invoke(initial_state)
        print("\n")
