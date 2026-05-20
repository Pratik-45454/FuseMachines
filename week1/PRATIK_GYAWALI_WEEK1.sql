1. 
select * from customers where customers.creditLimit>20000

2.
SELECT
    CONCAT(e.firstName,' ', e.lastName) as FullName, e.reportsTo, m.firstName, m.jobTitle
FROM
    employees e
JOIN employees m ON
    e.reportsTo = m.employeeNumber
WHERE
    m.jobTitle = 'VP Sales'

3.
select * from customers c where (c.state is not null) and (c.country = 'USA') and (c.creditLimit BETWEEN 100000 and 200000)

4.
select * from employees e 
inner join employees m on e.reportsTo = m.employeeNumber where m.jobTitle like '%Sales Manager%'

5. 
SELECT
    c.country,
    AVG(c.creditLimit) as avg_creditLimit
FROM
    customers c
GROUP BY
    c.country


6. 
SELECT
    COUNT(o.orderNumber) AS total_orders
FROM
    orders o
INNER JOIN customers ON o.customerNumber = customers.customerNumber
GROUP BY
    o.orderDate,
    customers.customerName

7. 
SELECT
    CONCAT(e.firstName, ' ', e.lastName) as full_name,
    e.jobTitle,
    (
    SELECT
        COUNT(*)
    FROM
        employees m
    WHERE
        m.reportsTo = e.employeeNumber
) as number_reported
FROM
    employees e


8. SELECT
    m.employeeNumber AS supervisor_number,
    COUNT(e.employeeNumber) AS number_supervised
FROM
    employees e
INNER JOIN employees m WHERE
    e.reportsTo = m.employeeNumber
GROUP BY
    m.employeeNumber


9.WITH
    avg_credit_limit AS(
    SELECT
        AVG(creditLimit) AS avg_credit
    FROM
        customers
)
SELECT
    c.customerName
FROM
    customers c
WHERE
    c.creditLimit >(
    SELECT
        avg_credit
    FROM
        avg_credit_limit
)


10. WITH ranked_customers AS (
    SELECT 
        customerNumber, 
        customerName, 
        creditLimit, 
        DENSE_RANK() OVER (ORDER BY creditLimit DESC) AS rnk
    FROM customers
)
SELECT customerNumber, customerName, creditLimit, rnk
FROM ranked_customers
WHERE rnk = 3;


11. SELECT
    COUNT(e.employeeNumber)
FROM
    employees e
GROUP BY
    e.officeCode


12. SELECT
    COUNT(c.customerNumber) AS number_of_customers,
    e.officeCode AS officeCode
FROM
    customers c
INNER JOIN employees e ON
    c.salesRepEmployeeNumber = e.employeeNumber
GROUP BY
    e.officeCode


13. SELECT
    SUM(p.amount) AS total_amount,
    o.city,
    o.state
FROM
	payments p
INNER JOIN customers c ON
	p.customerNumber = c.customerNumber
INNER JOIN employees e ON
	c.salesRepEmployeeNumber = e.employeeNumber
INNER JOIN offices o ON
	e.officeCode = o.officeCode
GROUP BY
    o.officeCode,
    o.city,
    o.state,
    o.country


14. SELECT 
	sum(od.quantityOrdered*od.priceEach) as total_sales, o.city
FROM
	orderdetails od
INNER JOIN orders ord ON
	od.orderNumber = ord.orderNumber
INNER JOIN customers c ON
	ord.customerNumber = c.customerNumber
INNER JOIN employees e ON
	c.salesRepEmployeeNumber = e.employeeNumber
INNER JOIN offices o ON
	e.officeCode = o.officeCode
GROUP BY
    o.officeCode,
    o.city,
    o.state,
    o.country

15. with sales_view as (
SELECT 
	sum(od.quantityOrdered*od.priceEach) as total_sales, o.city, o.officeCode
FROM
	orderdetails od
INNER JOIN orders ord ON
	od.orderNumber = ord.orderNumber
INNER JOIN customers c ON
	ord.customerNumber = c.customerNumber
INNER JOIN employees e ON
	c.salesRepEmployeeNumber = e.employeeNumber
INNER JOIN offices o ON
	e.officeCode = o.officeCode

GROUP BY
    o.officeCode,
    o.city,
    o.state,
    o.country
),payment_view as (
SELECT
    SUM(p.amount) AS total_amount,
    o.city,
    o.state,
    o.officeCode
FROM
	payments p
INNER JOIN customers c ON
	p.customerNumber = c.customerNumber
INNER JOIN employees e ON
	c.salesRepEmployeeNumber = e.employeeNumber
INNER JOIN offices o ON
	e.officeCode = o.officeCode
GROUP BY
    o.officeCode,
    o.city,
    o.state,
    o.country
)

select s.total_sales - p.total_amount, s.city from payment_view p inner join sales_view s on p.officeCode = s.officeCode

16. SELECT
    c.creditLimit,
    c.creditLimit/(
	SELECT
	SUM(cu.creditLimit) AS proportion_in_country
	FROM
	customers cu
	WHERE
	cu.country = c.country) as proportion_in_country
FROM
    customers c

17.
CREATE VIEW customer_or_view AS 
SELECT 
    c.customerName, 
    CONCAT(c.addressLine1, ' ', c.addressLine2) AS full_address
FROM 
    customers c 
INNER JOIN orders o ON c.customerNumber = o.customerNumber
INNER JOIN orderdetails od ON od.orderNumber = o.orderNumber;

SELECT * FROM customer_order_view;

18.
UPDATE customers
SET country = 'NewCountry'
WHERE customerNumber = 1;

19.
DELETE FROM payments
WHERE amount < 20000;

20.
INSERT INTO payments (customerNumber, amount, paymentDate, checkNumber)
VALUES (1, 5000, '2026-05-04', 'CHK12345');
