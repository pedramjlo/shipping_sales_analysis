SELECT * FROM ship_sales_data;



-- TOTAL SALES BY STATES
SELECT 
    state,
    ROUND(SUM(sales::int), 3) as Revenue
FROM ship_sales_data
GROUP BY state
ORDER BY Revenue DESC;


-- AVERAGE SALES BY STATES
SELECT 
    state,
    ROUND(AVG(sales::int), 3) as Revenue
FROM ship_sales_data
GROUP BY state
ORDER BY state;


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
        ROUND(SUM(sales::int), 3) AS Revenue
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
        category,
        sub_category,
        SUM(sales) AS Revenue
    FROM ship_sales_data
    GROUP BY state, category, sub_category
),
RANKED_SUB_CATEGORY AS (
    SELECT
        state,
        category,
        sub_category,
        Revenue,
        ROW_NUMBER() OVER (PARTITION BY state ORDER BY Revenue DESC) AS rn
    FROM TOP_SUB_CATEGORY
)
SELECT
    state,
    category,
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


-- MOST COMMON SHIP MODE CHOICE PER SUB-CATEGORY
WITH SHIPPING_CHOICE AS (
    SELECT
        ship_mode,
        category, 
        sub_category,
        count(ship_mode) as shipping_choice_count
    FROM ship_sales_data
    GROUP BY ship_mode, category, sub_category
),
RANKED_SHIPPING AS (
    SELECT
        ship_mode,
        category,
        sub_category,
        shipping_choice_count,
        ROW_NUMBER() OVER (PARTITION BY sub_category ORDER BY shipping_choice_count DESC) AS rn
    FROM SHIPPING_CHOICE
)
SELECT
    ship_mode,
    category,
    sub_category,
    shipping_choice_count
FROM RANKED_SHIPPING
WHERE rn = 1
ORDER BY category;




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


-- TOP-SPENDING CUSTOMERS OVERALL + ORDER COUNT + AVERAGE ORDER VALUE
WITH TOP_CUSTOMERS AS (
    SELECT
        customer_id,
        customer_name,
        SUM(sales::numeric) AS customer_spending,
        MIN(order_date) AS first_order,
        MAX(order_date) AS last_order,
        COUNT(DISTINCT order_id) AS order_count
    FROM ship_sales_data
    GROUP BY customer_id, customer_name
)
SELECT
    customer_id,
    customer_name,
    customer_spending,
    first_order,
    last_order,
    order_count,
    ROUND(customer_spending/order_count, 3) as avg_order_value
FROM TOP_CUSTOMERS
ORDER BY customer_spending DESC
LIMIT 20;





-- AVERAGE SHIPPING TIME PER SHIPPING MODE
SELECT 
    ship_mode,
    ROUND(AVG((ship_date::date) - (order_date::date)), 2) as average_ship_days
FROM ship_sales_data
GROUP BY ship_mode
ORDER BY average_ship_days ASC;



-- SALES BY SEASONALITY
WITH SALES_BY_SEASON AS (
    SELECT
        EXTRACT(YEAR FROM order_date::date) as Year,
        EXTRACT(MONTH FROM order_date::date) as Month,
        sales
    FROM ship_sales_data
    GROUP BY Year, Month, sales
),
SEASON_TABLE AS (
    SELECT
        Year,
        Month,
        sales,
        CASE
            WHEN Month IN (12, 1, 2) THEN 'Winter'
            WHEN Month IN (3, 4, 5) THEN 'Spring'
            WHEN Month IN (6, 7, 8) THEN 'Summer'
            WHEN Month IN (9, 10, 11) THEN 'Autumn'
            ELSE 'Unknown'
        END AS season
    FROM SALES_BY_SEASON
)
SELECT
    Year,
    season,
    ROUND(AVG(sales::int) , 3) as average_sales
FROM SEASON_TABLE
GROUP BY Year, season
ORDER BY Year, season;



-- AVERAGE ORDER VALUE BY SHIP MODE
WITH AVERAGE_VALUE AS (
    SELECT
        ship_mode,
        SUM(sales) / count(DISTINCT order_id) as order_value
    FROM ship_sales_data
    GROUP BY ship_mode
)
SELECT
    ship_mode,
    order_value
FROM AVERAGE_VALUE
ORDER BY order_value DESC;