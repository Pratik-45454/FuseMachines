import json
import os
from datetime import datetime
from database import get_connection
from validator import validate_sql, clean_sql

LOG_FILE = os.path.join(os.path.dirname(__file__), "logs", "query_log.json")


def _load_logs() -> list:
    """Read existing log entries from disk."""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    return []


def _save_log(entry: dict):
    """Append a single log entry to the log file."""
    logs = _load_logs()
    logs.append(entry)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2, default=str)


def execute_sql(sql: str, question: str, retry_count: int = 0) -> dict:
    """
    Validate and run a SQL query against PostgreSQL.
    Returns a structured result dict with status, result rows, and any error.
    """
    sql = clean_sql(sql)

    # Block unsafe queries before touching the database
    check = validate_sql(sql)
    if not check["is_valid"]:
        entry = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "sql": sql,
            "status": "blocked",
            "error": check["reason"],
            "retry_count": retry_count,
            "result": [],
        }
        _save_log(entry)
        return entry

    # Run the query — connection is always closed via finally
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(sql)

        rows = cur.fetchall()
        columns = [col[0] for col in cur.description]
        result = [dict(zip(columns, row)) for row in rows]
        cur.close()

        entry = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "sql": sql,
            "status": "success",
            "error": None,
            "retry_count": retry_count,
            "result": result[:5],  # log only the first 5 rows
        }

    except Exception as e:
        entry = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "sql": sql,
            "status": "failed",
            "error": str(e),
            "retry_count": retry_count,
            "result": [],
        }

    finally:
        if conn:
            conn.close()

    _save_log(entry)
    return entry


if __name__ == "__main__":
    res = execute_sql(
        'SELECT "customerName", "city" FROM customers LIMIT 3;',
        "Get customer names and cities",
    )
    print(f"Status : {res['status']}")
    print(f"Error  : {res['error']}")
    print(f"Results: {res['result']}")
