import re

# Only SELECT queries are allowed
BLOCKED_KEYWORDS = [
    "DELETE", "DROP", "UPDATE", "INSERT",
    "TRUNCATE", "ALTER", "CREATE", "REPLACE",
    "GRANT", "REVOKE", "EXEC", "EXECUTE",
]


def validate_sql(sql: str) -> dict:
    """
    Check whether a SQL query is safe to run.
    Returns a dict with 'is_valid' (bool) and 'reason' (str).
    """
    if not sql or not sql.strip():
        return {"is_valid": False, "reason": "No SQL query was generated."}

    upper = sql.upper().strip()

    if not upper.startswith("SELECT"):
        return {
            "is_valid": False,
            "reason": f"Query must begin with SELECT. Got: {sql[:50]}",
        }

    for keyword in BLOCKED_KEYWORDS:
        if re.search(r"\b" + keyword + r"\b", upper):
            return {
                "is_valid": False,
                "reason": f"Disallowed keyword found: {keyword}",
            }

    if sql.count(";") > 1:
        return {
            "is_valid": False,
            "reason": "Multiple statements detected — only one query allowed.",
        }

    return {"is_valid": True, "reason": "SQL passed validation."}


def clean_sql(sql: str) -> str:
    """
    Strip markdown formatting from LLM output and normalize the SQL string.
    Ensures the query ends with a semicolon.
    """
    sql = re.sub(r"```sql", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"```", "", sql)
    sql = sql.strip()

    if not sql.endswith(";"):
        sql += ";"

    return sql


if __name__ == "__main__":
    samples = [
        "SELECT * FROM customers;",
        "DELETE FROM customers;",
        "SELECT * FROM orders; DROP TABLE orders;",
        "UPDATE products SET price = 0;",
        "",
    ]
    for q in samples:
        result = validate_sql(q)
        print(f"Query  : {q[:40]}")
        print(f"Valid  : {result['is_valid']} | {result['reason']}")
        print("---")
