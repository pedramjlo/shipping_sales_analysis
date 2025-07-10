SELECT * FROM ship_sales_data;



-- TOTAL SALES BY STATES
SELECT 
    state,
    SUM(sales) as Revenue
FROM ship_sales_data
GROUP BY state
ORDER BY Revenue DESC;


-- TOTAL REVENUE BY CITY WITHIN STATES
WITH SALES_PER_CITY AS (
    SELECT
        city,
        state,
        SUM(sales) as Revenue
    FROM ship_sales_data
    GROUP BY city, state
)
SELECT
    city,
    state,
    Revenue
FROM SALES_PER_CITY
ORDER BY state, Revenue DESC;


-- AVERAGE SHIPPING TIME (DAYS) AFTER THE SUBMISSION OF THE ORDER PER STATE
WITH AVERAGE_SHIP_TIME AS (
    SELECT
        state,
        ROUND(AVG((ship_date::date) - (order_date::date)), 1) as average_ship_days
    FROM ship_sales_data
    GROUP BY state
) 
SELECT
    state,
    average_ship_days
FROM AVERAGE_SHIP_TIME
ORDER BY average_ship_days DESC;


-- TOP-SELLING CATEGORY BY STATE
WITH TOP_CATEGORY AS (
    SELECT
        state,
        category,
        SUM(sales) AS Revenue
    FROM ship_sales_data
    GROUP BY state, category
),
RANKED_CATEGORY AS (
    SELECT
        state,
        category,
        Revenue,
        ROW_NUMBER() OVER (PARTITION BY state ORDER BY Revenue DESC) AS rn
    FROM TOP_CATEGORY
)
SELECT
    state,
    category,
    Revenue AS category_revenue
FROM RANKED_CATEGORY
WHERE rn = 1
ORDER BY category_revenue DESC;



-- TOP-SELLING SUB-CATEGORIES BY STATE
WITH TOP_SUB_CATEGORY AS (
    SELECT
        state,
        sub_category,
        SUM(sales) AS Revenue
    FROM ship_sales_data
    GROUP BY state, sub_category
),
RANKED_SUB_CATEGORY AS (
    SELECT
        state,
        sub_category,
        Revenue,
        ROW_NUMBER() OVER (PARTITION BY state ORDER BY Revenue DESC) AS rn
    FROM TOP_SUB_CATEGORY
)
SELECT
    state,
    sub_category,
    Revenue AS category_revenue
FROM RANKED_SUB_CATEGORY
WHERE rn = 1
ORDER BY category_revenue DESC;


-- AVERAGE SHIPPING TIME PER CATEGORY
WITH AVERAGE_SHIPPING_DAYS AS (
    SELECT
        category,
        ROUND(AVG((ship_date::date) - (order_date::date)), 1) as average_ship_days
    FROM ship_sales_data
    GROUP BY category
)
SELECT
    category,
    average_ship_days
FROM AVERAGE_SHIPPING_DAYS
ORDER BY average_ship_days ASC;



-- AVERAGE SHIPPING TIME PER SUB-CATEGORY
WITH AVERAGE_SHIPPING_DAYS AS (
    SELECT
        sub_category,
        ROUND(AVG((ship_date::date) - (order_date::date)), 1) as average_ship_days
    FROM ship_sales_data
    GROUP BY sub_category
)
SELECT
    sub_category,
    average_ship_days
FROM AVERAGE_SHIPPING_DAYS
ORDER BY average_ship_days ASC;


-- TOP CUSTOMERS OVERALL 
WITH TOP_CUSTOMERS AS (
    SELECT
        customer_id,
        customer_name,
        SUM(sales::numeric) AS Customer_Spending,
        MIN(order_date) AS first_order,
        MAX(order_date) AS last_order,
        COUNT(DISTINCT order_id) AS Order_Count
    FROM ship_sales_data
    GROUP BY customer_id, customer_name
)
SELECT
    customer_id,
    customer_name,
    Customer_Spending,
    first_order,
    last_order,
    Order_Count,
    ROUND(Customer_Spending/Order_Count, 3) as avg_order_value
FROM TOP_CUSTOMERS
ORDER BY Customer_Spending DESC
LIMIT 20;




