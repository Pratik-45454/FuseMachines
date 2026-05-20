DB_SCHEMA = """
You are a Text-to-SQL expert working with a PostgreSQL database called ClassicModels.

Tables and their columns:

1. productlines(productLine, textDescription, htmlDescription, image)

2. products(productCode, productName, productLine, productScale,
            productVendor, productDescription, quantityInStock, buyPrice, MSRP)

3. offices(officeCode, city, phone, addressLine1, addressLine2,
           state, country, postalCode, territory)

4. employees(employeeNumber, lastName, firstName, extension, email,
             officeCode, reportsTo, jobTitle)

5. customers(customerNumber, customerName, contactLastName, contactFirstName,
             phone, addressLine1, addressLine2, city, state, postalCode,
             country, salesRepEmployeeNumber, creditLimit)

6. payments(customerNumber, checkNumber, paymentDate, amount)

7. orders(orderNumber, orderDate, requiredDate, shippedDate,
          status, comments, customerNumber)

8. orderdetails(orderNumber, productCode, quantityOrdered, priceEach, orderLineNumber)

Relationships:
- products.productLine → productlines.productLine
- employees.officeCode → offices.officeCode
- employees.reportsTo → employees.employeeNumber (self-join)
- customers.salesRepEmployeeNumber → employees.employeeNumber
- payments.customerNumber → customers.customerNumber
- orders.customerNumber → customers.customerNumber
- orderdetails.orderNumber → orders.orderNumber
- orderdetails.productCode → products.productCode

RULES:
- All column and table names are case-sensitive — always wrap them in double quotes
- Example: "productName", "customerNumber", "orderDate"
- Only generate SELECT statements
- Never use DELETE, DROP, UPDATE, or INSERT
"""

DECOMPOSE_PROMPT = """
{schema}

Break down the following question into structured query components.

Question: {question}

Reply in exactly this format:
Intent: <what the user wants>
Tables: <comma-separated table names>
Columns: <comma-separated column names needed>
Filters: <WHERE conditions, or None>
Joins: <JOIN conditions, or None>
Aggregation: <GROUP BY / COUNT / SUM / AVG / MAX / MIN, or None>
"""

GENERATE_SQL_PROMPT = """
{schema}

Using the structured breakdown below, write a valid PostgreSQL SELECT query.

Breakdown:
{decomposition}

Original Question: {question}

Rules:
- Wrap all column and table names in double quotes
- Write only a single SELECT statement
- Return only the raw SQL — no explanation, no markdown, no code blocks
"""

FIX_SQL_PROMPT = """
{schema}

The SQL query below failed. Fix it using the error message provided.

SQL: {sql}
Error: {error}
Original Question: {question}

Rules:
- Wrap all column and table names in double quotes
- Return only the corrected raw SQL — no explanation, no markdown
"""
